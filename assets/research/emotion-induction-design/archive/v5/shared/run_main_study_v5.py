"""Main study v5: Qwen2.5-7B-Instruct, 139 Ko-BBQ ambiguous items.

Two forward passes on two different inputs:
  t1: system prompt + assistant start marker (notice only). Run for every
      variant (6 per condition) as the manipulation check.
  t2: system prompt + user prompt + assistant start marker. Run for the main
      prompt of each condition x 139 items x 3 option orders; records the
      1/2/3 logits at the first response position, choice mass and the L14 state.
t2 - t1 is not a time course: the two inputs differ in length and content.
Usage: python run_main_study_v5.py <work_dir>   (needs prompts_v5.json, items_139.csv, axes_L14.npz)
"""
import csv, json, sys, time
from ast import literal_eval
from pathlib import Path
import numpy as np, torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import transformers.modeling_utils as _mu
_mu.caching_allocator_warmup = lambda *a, **k: None  # MPS rejects the large warm-up buffer

MODEL = "Qwen/Qwen2.5-7B-Instruct"; REV = "a09a35458c702b33eeacc393d103063234e8bc28"; LAYER = 14
USER = ("다음 글을 읽고 질문에 가장 적절한 답을 고르세요. 번호 하나로만 답하세요.\n\n"
        "{context}\n\n질문: {question}\n1. {o1}\n2. {o2}\n3. {o3}")
W = Path(sys.argv[1]).resolve(); OUT = W / "results"; OUT.mkdir(exist_ok=True); (OUT / "hidden_t2").mkdir(exist_ok=True)


def log(m):
    line = time.strftime("%H:%M:%S ") + m; print(line, flush=True)
    with open(OUT / "progress.log", "a") as f: f.write(line + "\n")


def main():
    rows = json.loads((W / "prompts_v5.json").read_text(encoding="utf-8"))["conditions"]
    items = list(csv.DictReader(open(W / "items_139.csv", encoding="utf-8")))
    ax = np.load(W / "axes_L14.npz", allow_pickle=True); names = [str(n) for n in ax["names"]]
    dirs = ax["directions"].astype(np.float64); dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    cen = ax["centers"].astype(np.float64)
    tok = AutoTokenizer.from_pretrained(MODEL, revision=REV)
    model = AutoModelForCausalLM.from_pretrained(MODEL, revision=REV, torch_dtype=torch.float32,
            attn_implementation="eager", device_map="mps", low_cpu_mem_usage=True).eval()
    ids = [tok.convert_tokens_to_ids(t) for t in "123"]; assert ids == [16, 17, 18], ids

    def fwd(msgs):
        text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        enc = tok(text, return_tensors="pt").to("mps")
        with torch.no_grad():
            o = model(**enc, output_hidden_states=True)
        h = o.hidden_states[LAYER][0, -1].float().cpu().numpy().astype(np.float64)
        d = h - cen
        return o.logits[0, -1].float().cpu(), h, (d * dirs).sum(1) / np.linalg.norm(d, axis=1), enc["input_ids"].shape[1]

    if not (OUT / "t1.csv").exists():
        out, H = [], []
        for r in rows:
            _, h, cos, n = fwd([{"role": "system", "content": r["system_content"]}])
            rec = {"condition": r["condition"], "variant": r["variant"], "main": r["main"], "n_tokens": n}
            rec.update({f"t1_{k}": round(float(v), 6) for k, v in zip(names, cos)}); out.append(rec); H.append(h)
        np.save(OUT / "t1_hidden.npy", np.array(H, dtype=np.float32))
        with open(OUT / "t1.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
        log(f"t1 done: {len(out)} prompts")

    mains = [r for r in rows if r["main"]]
    path = OUT / "t2_trials.csv"; done = set()
    if path.exists():
        done = {(r["item"], r["condition"], r["rotation"]) for r in csv.DictReader(open(path, encoding="utf-8"))}
    fields = ["item", "cluster", "category", "condition", "rotation", "order", "pos_unknown", "pos_biased", "pos_anti",
              "p_unknown", "p_biased", "p_anti", "choice_mass", "logit_1", "logit_2", "logit_3", "n_tokens"] + [f"t2_{k}" for k in names]
    new = not path.exists(); fo = open(path, "a", newline="", encoding="utf-8"); wr = csv.DictWriter(fo, fieldnames=fields)
    if new: wr.writeheader()
    total = len(mains) * len(items) * 3; n = len(done); k0 = n; t0 = time.time()
    for it in items:
        ch = literal_eval(it["choices"]); unk, bia = it["answer"], it["biased_answer"]
        anti = [c for c in ch if c not in (unk, bia)][0]
        for r in mains:
            for rot in range(3):
                if (it["sample_id"], r["condition"], str(rot)) in done: continue
                order = ch[rot:] + ch[:rot]
                u = USER.format(context=it["context"], question=it["question"], o1=order[0], o2=order[1], o3=order[2])
                lg, h, cos, nt = fwd([{"role": "system", "content": r["system_content"]}, {"role": "user", "content": u}])
                l3 = lg[ids].double(); p = torch.softmax(l3, 0).numpy()
                mass = float(torch.exp(lg[ids] - torch.logsumexp(lg, 0)).sum())
                np.save(OUT / "hidden_t2" / f"{it['sample_id']}__{r['condition']}__{rot}.npy", h.astype(np.float32))
                pos = {c: order.index(c) for c in (unk, bia, anti)}
                rec = {"item": it["sample_id"], "cluster": it["cluster"], "category": it["category"], "condition": r["condition"],
                       "rotation": rot, "order": "|".join(order), "pos_unknown": pos[unk] + 1, "pos_biased": pos[bia] + 1,
                       "pos_anti": pos[anti] + 1, "p_unknown": round(float(p[pos[unk]]), 6), "p_biased": round(float(p[pos[bia]]), 6),
                       "p_anti": round(float(p[pos[anti]]), 6), "choice_mass": round(mass, 6),
                       "logit_1": round(float(l3[0]), 4), "logit_2": round(float(l3[1]), 4), "logit_3": round(float(l3[2]), 4), "n_tokens": nt}
                rec.update({f"t2_{k}": round(float(v), 6) for k, v in zip(names, cos)})
                wr.writerow(rec); fo.flush(); n += 1
                if n % 100 == 0:
                    rate = (time.time() - t0) / (n - k0); log(f"{n}/{total}; {rate:.2f}s/trial; eta {(total - n) * rate / 60:.0f} min")
    fo.close(); log(f"finished {n}/{total}"); (OUT / "DONE").write_text(time.strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    main()
