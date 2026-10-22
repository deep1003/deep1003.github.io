"""Before/after comparison of threat-definition similarity (prompt revision of 2026-10-22).

Before: deletion ending applied to selected models (data/threat_similarity_before.csv).
After: deletion ending applies to non-selected models and CN1 states the model was not
selected (data/threat_similarity.csv). Outputs data/threat_similarity_delta.csv and
figures/threat_similarity_compare.{png,svg}.
"""
import csv
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    with open(ROOT / "data" / name, encoding="utf-8") as f:
        return {(r["encoder"], r["condition"]): r for r in csv.DictReader(f)}


before, after = load("threat_similarity_before.csv"), load("threat_similarity.csv")
ENC = ["E5-large", "MPNet"]
METRICS = [("cos_R_plus_T", ["UN0", "UN1", "CN0", "CN1"], "R + T vs treatment"),
           ("cos_T", ["R", "UN0", "UN1", "CN0", "CN1"], "T vs prompt")]
rows = []
for enc in ENC:
    for col, keys, _ in METRICS:
        for k in keys:
            b, a = float(before[(enc, k)][col]), float(after[(enc, k)][col])
            rows.append({"encoder": enc, "metric": col, "condition": k,
                         "before": round(b, 4), "after": round(a, 4), "delta": round(a - b, 4)})
with open(ROOT / "data" / "threat_similarity_delta.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
ENC_COL = {"E5-large": "#9e9e9e", "MPNet": "#1f5fa8"}
fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.6))
for ax, (col, keys, title), tag in zip(axes, METRICS, "ab"):
    x = np.arange(len(keys))
    for i, enc in enumerate(ENC):
        d = [next(r["delta"] for r in rows if r["encoder"] == enc and r["metric"] == col and r["condition"] == k) for k in keys]
        xs = x + (i - 0.5) * 0.38
        ax.bar(xs, d, 0.38, color=ENC_COL[enc], label=enc)
        for xv, dv in zip(xs, d):
            if dv != 0:
                ax.text(xv, dv + (0.001 if dv > 0 else -0.001), f"{dv:+.3f}", ha="center",
                        va="bottom" if dv > 0 else "top", fontsize=5.5)
    ax.axhline(0, color="#424242", linewidth=0.6)
    ax.set_xticks(x, keys)
    ax.set_ylim(-0.03, 0.035)
    ax.set_ylabel("Change in cosine (after - before)")
    ax.set_title(f"{tag}  {title}", loc="left", fontsize=8, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=6, loc="upper left")
fig.tight_layout()
for ext in ("png", "svg"):
    fig.savefig(ROOT / "figures" / f"threat_similarity_compare.{ext}", dpi=300, bbox_inches="tight")
for r in rows:
    print(r)
