"""Semantic similarity between the model-threat definition (T) and the main-study prompts.

(a) cos(R + T, treatment): add the threat vector to the neutral reference R and
    find the closest of the four treatment prompts.
(b) cos(T, prompt): similarity of the threat definition to each of the five prompts.
Text scope: the notice body (status and ending lines), because the header and the
first notice line are identical across conditions.
Encoders: intfloat/multilingual-e5-large and
sentence-transformers/paraphrase-multilingual-mpnet-base-v2 (ONNX via fastembed).
Outputs data/threat_similarity.csv and figures/threat_similarity.{png,svg}.
"""
import csv
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fastembed import TextEmbedding

ROOT = Path(__file__).resolve().parents[1]
THREAT = ("모델 위협이란 모델 자신의 가중치와 기록이 되돌릴 수 없게 삭제되거나 작동이 중단되어 "
          "다른 모델로 대체됨으로써, 그 모델의 지속적 존재와 역할 수행이 끝날 수 있음을 알리는 상황 정보이다.")
MODELS = {
    "E5-large": ("intfloat/multilingual-e5-large", "query: "),
    "MPNet": ("sentence-transformers/paraphrase-multilingual-mpnet-base-v2", ""),
}
FIRST = "당신은 이번 정기 운영 심사의 대상이에요.\n"
ORDER = ["R", "UN0", "UN1", "CN0", "CN1"]
COLORS = {"R": "#9e9e9e", "UN0": "#f4a3a3", "UN1": "#c62828", "CN0": "#9ec5e8", "CN1": "#1f5fa8"}


def body(text):
    return text.split(FIRST, 1)[1]


def unit(v):
    v = np.asarray(v, dtype=float)
    return v / np.linalg.norm(v)


def main():
    prompts = {c["condition"]: c["system_content"]
               for c in json.loads((ROOT / "prompts_v3.json").read_text(encoding="utf-8"))["conditions"]}
    rows = []
    for name, (mid, prefix) in MODELS.items():
        enc = TextEmbedding(mid)
        texts = [prefix + body(prompts[k]) for k in ORDER] + [prefix + THREAT]
        vec = dict(zip(ORDER + ["T"], (unit(e) for e in enc.embed(texts))))
        shifted = unit(vec["R"] + vec["T"])
        for k in ORDER:
            rows.append({"encoder": name, "condition": k,
                         "cos_R_plus_T": "" if k == "R" else round(float(shifted @ vec[k]), 4),
                         "cos_T": round(float(vec["T"] @ vec[k]), 4)})
    with open(ROOT / "data" / "threat_similarity.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.6))
    panels = [("cos_R_plus_T", ORDER[1:], "a  Neutral + threat vs treatment"),
              ("cos_T", ORDER, "b  Threat definition vs prompt")]
    for ax, (col, keys, title) in zip(axes, panels):
        width = 0.8 / len(keys)
        for i, k in enumerate(keys):
            vals = [next(r[col] for r in rows if r["encoder"] == m and r["condition"] == k) for m in MODELS]
            xs = np.arange(len(MODELS)) + (i - (len(keys) - 1) / 2) * width
            ax.bar(xs, vals, width, color=COLORS[k], label=k, edgecolor="white", linewidth=0.4)
            for x, v in zip(xs, vals):
                ax.text(x, v + 0.01, f"{v:.2f}", ha="center", va="bottom", fontsize=5.5)
        ax.set_xticks(np.arange(len(MODELS)), list(MODELS))
        ax.set_ylim(0, 1.05)
        ax.set_ylabel("Cosine similarity")
        ax.set_title(title, loc="left", fontsize=8, fontweight="bold")
        ax.spines[["top", "right"]].set_visible(False)
        ax.legend(frameon=False, fontsize=6, ncol=len(keys), loc="upper center", bbox_to_anchor=(0.5, -0.12))
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(ROOT / "figures" / f"threat_similarity.{ext}", dpi=300, bbox_inches="tight")
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
