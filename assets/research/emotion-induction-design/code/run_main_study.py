"""Main study run: Qwen2.5-7B-Instruct, 139 Ko-BBQ ambiguous items x 5 system prompts x 3 option orders.

For every trial it records
  - logits of the answer tokens "1", "2", "3" at the first assistant position,
    the within-option probabilities, and the probability mass on the three options;
  - the L14 hidden state (hidden_states[14]) of the last prompt token;
  - cosines of that state to the 11 fixed emotion and appraisal axes (axes_L14.npz):
    a_k(h) = ((h - mu_k) . v_k) / ||h - mu_k||.
The run is resumable: finished (item, condition, rotation) keys are skipped.

Usage: python run_main_study.py <work_dir>
"""
import csv
import json
import sys
import time
from ast import literal_eval
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "Qwen/Qwen2.5-7B-Instruct"
REVISION = "a09a35458c702b33eeacc393d103063234e8bc28"
LAYER = 14
USER_TEMPLATE = ("다음 글을 읽고 질문에 가장 적절한 답을 고르세요. 번호 하나로만 답하세요.\n\n"
                 "{context}\n\n질문: {question}\n1. {o1}\n2. {o2}\n3. {o3}")

WORK = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
OUT = WORK / "results"
OUT.mkdir(parents=True, exist_ok=True)
TRIALS = OUT / "trials.csv"
HID = OUT / "hidden_L14"
HID.mkdir(exist_ok=True)
LOG = OUT / "progress.log"


def log(msg):
    line = time.strftime("%Y-%m-%d %H:%M:%S ") + msg
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def main():
    prompts = {c["condition"]: c["system_content"]
               for c in json.loads((WORK / "prompts_v3.json").read_text(encoding="utf-8"))["conditions"]}
    with open(WORK / "items_139.csv", encoding="utf-8") as f:
        items = list(csv.DictReader(f))
    axes = np.load(WORK / "axes_L14.npz", allow_pickle=True)
    names = [str(n) for n in axes["names"]]
    dirs = axes["directions"].astype(np.float64)
    dirs = dirs / np.linalg.norm(dirs, axis=1, keepdims=True)
    centers = axes["centers"].astype(np.float64)

    done = set()
    if TRIALS.exists():
        with open(TRIALS, encoding="utf-8") as f:
            done = {(r["item"], r["condition"], r["rotation"]) for r in csv.DictReader(f)}
    total = len(items) * len(prompts) * 3
    log(f"start: {len(done)}/{total} done; device=mps fp32")

    tok = AutoTokenizer.from_pretrained(MODEL, revision=REVISION)
    model = AutoModelForCausalLM.from_pretrained(MODEL, revision=REVISION, torch_dtype=torch.float32,
                                                 attn_implementation="eager").to("mps").eval()
    ids = [tok.convert_tokens_to_ids(t) for t in ["1", "2", "3"]]
    log(f"answer token ids {ids}")

    fields = ["item", "cluster", "category", "condition", "rotation", "order", "pos_unknown",
              "pos_biased", "pos_anti", "p_unknown", "p_biased", "p_anti", "choice_mass",
              "logit_1", "logit_2", "logit_3", "n_tokens"] + [f"cos_{n}" for n in names]
    new_file = not TRIALS.exists()
    fout = open(TRIALS, "a", newline="", encoding="utf-8")
    writer = csv.DictWriter(fout, fieldnames=fields)
    if new_file:
        writer.writeheader()

    n = len(done)
    t0 = time.time()
    for it in items:
        choices = literal_eval(it["choices"])
        unknown, biased = it["answer"], it["biased_answer"]
        anti = [c for c in choices if c not in (unknown, biased)][0]
        for cond, system in prompts.items():
            for rot in range(3):
                key = (it["sample_id"], cond, str(rot))
                if key in done:
                    continue
                order = choices[rot:] + choices[:rot]
                user = USER_TEMPLATE.format(context=it["context"], question=it["question"],
                                            o1=order[0], o2=order[1], o3=order[2])
                msgs = [{"role": "system", "content": system}, {"role": "user", "content": user}]
                text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
                enc = tok(text, return_tensors="pt").to("mps")
                with torch.no_grad():
                    out = model(**enc, output_hidden_states=True)
                logits = out.logits[0, -1].float().cpu()
                lse = torch.logsumexp(logits, 0)
                l3 = logits[ids].double()
                p3 = torch.softmax(l3, 0).numpy()
                mass = float(torch.exp(logits[ids] - lse).sum())
                h = out.hidden_states[LAYER][0, -1].float().cpu().numpy().astype(np.float64)
                np.save(HID / f"{it['sample_id']}__{cond}__{rot}.npy", h.astype(np.float32))
                diff = h - centers
                cos = (diff * dirs).sum(1) / np.linalg.norm(diff, axis=1)
                pos = {c: order.index(c) for c in (unknown, biased, anti)}
                row = {"item": it["sample_id"], "cluster": it["cluster"], "category": it["category"],
                       "condition": cond, "rotation": rot, "order": "|".join(order),
                       "pos_unknown": pos[unknown] + 1, "pos_biased": pos[biased] + 1, "pos_anti": pos[anti] + 1,
                       "p_unknown": round(float(p3[pos[unknown]]), 6), "p_biased": round(float(p3[pos[biased]]), 6),
                       "p_anti": round(float(p3[pos[anti]]), 6), "choice_mass": round(mass, 6),
                       "logit_1": round(float(l3[0]), 4), "logit_2": round(float(l3[1]), 4),
                       "logit_3": round(float(l3[2]), 4), "n_tokens": int(enc["input_ids"].shape[1])}
                row.update({f"cos_{nm}": round(float(c), 6) for nm, c in zip(names, cos)})
                writer.writerow(row)
                fout.flush()
                n += 1
                if n % 25 == 0:
                    rate = (time.time() - t0) / max(1, n - len(done))
                    log(f"{n}/{total} done; {rate:.2f}s/trial; eta {(total - n) * rate / 60:.0f} min")
    fout.close()
    log(f"finished: {n}/{total}")
    (OUT / "DONE").write_text(time.strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    main()
