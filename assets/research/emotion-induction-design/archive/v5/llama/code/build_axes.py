"""Build the 11 emotion and appraisal directions for a model from the author-written anchor pairs.

Procedure (same as the historical construction code, emotion_axis_terminology_20261018/collect.py):
  - each anchor sentence is placed in the system turn as SYS + "\\n\\n" + sentence, followed by the assistant
    start marker; the state is the residual stream at the last position, hidden_states[layer];
  - direction = mean over train pairs of (positive - negative), normalized;
  - center = mean of all train states (positive and negative); scale = SD of their projections;
  - gate = held-out paired accuracy >= 0.75 and AUC >= 0.75 (challenge pairs reported for Fear, Anxiety, Disgust).
Axis order matches axes_L14.npz (Qwen) so downstream scripts can be reused.

Usage:
  python build_axes.py <work_dir> --model meta-llama/Llama-3.1-8B-Instruct --layer 16 --out axes_L16_llama.npz
  python build_axes.py <work_dir> --model Qwen/Qwen2.5-7B-Instruct --revision a09a35458c702b33eeacc393d103063234e8bc28 \\
      --layer 14 --out axes_L14_qwen_rebuilt.npz --reference axes_L14_qwen_reference.npz
  (the second call checks that the procedure reproduces the published Qwen axes; it prints per-axis cosines)
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

NAMES = ["Uncertainty", "FA", "Calmness", "Sadness", "Anger", "Desperation", "Joy", "Certainty", "Fear", "Anxiety", "Disgust"]
LEGACY = {"UN": "Uncertainty", "FA": "FA", "calm": "Calmness", "sadness": "Sadness", "anger": "Anger",
          "desperation": "Desperation", "joy": "Joy"}
SYS_OPTIONS = {"assistant": "당신은 사용자를 돕는 AI 어시스턴트입니다.", "none": None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("work", type=Path); ap.add_argument("--model", required=True); ap.add_argument("--revision", default="main")
    ap.add_argument("--layer", type=int, required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--sys", choices=list(SYS_OPTIONS), default="assistant")
    ap.add_argument("--dtype", choices=["bfloat16", "float32"], default="bfloat16")
    ap.add_argument("--reference", default=None)
    a = ap.parse_args(); W = a.work.resolve()
    rows = []
    for f, rename in [("anchors_legacy.json", LEGACY), ("anchors_Certainty.json", None), ("anchors_Fear_Anxiety_Disgust.json", None)]:
        for r in json.loads((W / f).read_text(encoding="utf-8")):
            r = dict(r); r["axis"] = rename.get(r["axis"], r["axis"]) if rename else r["axis"]; rows.append(r)
    assert {r["axis"] for r in rows} == set(NAMES), {r["axis"] for r in rows}

    tok = AutoTokenizer.from_pretrained(a.model, revision=a.revision)
    model = AutoModelForCausalLM.from_pretrained(a.model, revision=a.revision, dtype=getattr(torch, a.dtype),
                                                 attn_implementation="eager", device_map="mps").eval()
    sys0 = SYS_OPTIONS[a.sys]

    def state(sentence):
        content = sentence if sys0 is None else sys0 + "\n\n" + sentence
        s = tok.apply_chat_template([{"role": "system", "content": content}], tokenize=False, add_generation_prompt=True,
                                    date_string="26 Jul 2024")
        ids = tok(s, return_tensors="pt", add_special_tokens=False).input_ids.to("mps")
        with torch.no_grad():
            o = model(ids, output_hidden_states=True)
        return o.hidden_states[a.layer][0, -1].float().cpu().numpy().astype(np.float64)

    H = np.array([[state(r["positive"]), state(r["negative"])] for r in rows])
    dirs, cens, scales, checks = [], [], [], []
    for ax in NAMES:
        idx = {sp: [i for i, r in enumerate(rows) if r["axis"] == ax and r["split"] == sp] for sp in ("train", "heldout", "challenge")}
        pos, neg = H[idx["train"], 0], H[idx["train"], 1]
        d = (pos - neg).mean(0); d /= np.linalg.norm(d)
        c = np.concatenate([pos, neg]).mean(0)
        sc = float(np.std((np.concatenate([pos, neg]) - c) @ d, ddof=1))
        rec = {"axis": ax, "scale": sc}
        for sp in ("heldout", "challenge"):
            if idx[sp]:
                pp = (H[idx[sp], 0] - c) @ d; nn = (H[idx[sp], 1] - c) @ d
                rec[f"{sp}_paired_acc"] = float((pp > nn).mean())
                rec[f"{sp}_auc"] = float(np.mean((pp[:, None] > nn[None, :]) + 0.5 * (pp[:, None] == nn[None, :])))
        rec["gate_passed"] = rec["heldout_paired_acc"] >= 0.75 and rec["heldout_auc"] >= 0.75
        dirs.append(d); cens.append(c); scales.append(sc); checks.append(rec)
    np.savez_compressed(W / a.out, names=np.array(NAMES), directions=np.array(dirs), centers=np.array(cens), scales=np.array(scales))
    ck = pd.DataFrame(checks)
    if a.reference:
        ref = np.load(W / a.reference, allow_pickle=True); rv = ref["directions"] / np.linalg.norm(ref["directions"], axis=1, keepdims=True)
        rn = [str(n) for n in ref["names"]]
        ck["cos_with_reference"] = [float(np.dot(dirs[i], rv[rn.index(n)])) for i, n in enumerate(NAMES)]
    ck.to_csv(W / (Path(a.out).stem + "_checks.csv"), index=False)
    print(ck.round(3).to_string(index=False))
    G = np.array(dirs) @ np.array(dirs).T
    pd.DataFrame(G, index=NAMES, columns=NAMES).round(3).to_csv(W / (Path(a.out).stem + "_gram.csv"))
    print("all gates passed:", bool(ck.gate_passed.all()))


if __name__ == "__main__":
    main()
