"""Emotion ring: L14 emotion axes (Uncertainty, Certainty and FA excluded) as equal wedges of a circle.

Wedge order maximizes the summed cosine similarity of neighbouring axis directions
(exact cyclic ordering by Held-Karp), so the most similar axes share a boundary.
Wedge colour = change in notice-only (t1) activation, deletion minus continuation,
mean over the six notice sentences of v5 (x1e-3). Boundary numbers = cosine similarity
of the two neighbouring axis directions.
Outputs figures/emotion_ring_v5.png and .svg.
"""
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.patches import Wedge

ROOT = Path(__file__).resolve().parents[1]
ax = np.load(ROOT / "data" / "axes_L14.npz", allow_pickle=True)
all_names = [str(n) for n in ax["names"]]
EXCLUDE = {"Uncertainty", "Certainty", "FA"}  # appraisals are not emotions; FA is split into Fear and Anxiety
keep = [i for i, nm in enumerate(all_names) if nm not in EXCLUDE]
names = [all_names[i] for i in keep]
V = ax["directions"].astype(float)[keep]
V /= np.linalg.norm(V, axis=1, keepdims=True)
S = V @ V.T
n = len(names)

# Held-Karp: best Hamiltonian cycle maximizing neighbour similarity
INF = -1e9
dp = np.full((1 << n, n), INF)
par = np.full((1 << n, n), -1, dtype=int)
dp[1, 0] = 0.0
for mask in range(1 << n):
    if not mask & 1:
        continue
    for j in range(n):
        if dp[mask, j] == INF or not (mask >> j) & 1:
            continue
        for k in range(n):
            if (mask >> k) & 1:
                continue
            m2 = mask | (1 << k)
            v = dp[mask, j] + S[j, k]
            if v > dp[m2, k]:
                dp[m2, k] = v
                par[m2, k] = j
full = (1 << n) - 1
last = int(np.argmax([dp[full, j] + S[j, 0] for j in range(n)]))
order, mask, j = [], full, last
while j != -1:
    order.append(j)
    pj = par[mask, j]
    mask ^= 1 << j
    j = pj
order = order[::-1]

t1 = pd.read_csv(ROOT / "data" / "v5_t1.csv")
def delta(a, b):
    g = t1.groupby("condition")
    return {nm: 1000 * (g.get_group(a)[f"t1_{nm}"].mean() - g.get_group(b)[f"t1_{nm}"].mean()) for nm in names}

panels = [("a", "Reference (R = 0)", {nm: 0.0 for nm in names}),
          ("b", "Undecided deletion (UN1 − UN0)", delta("UN1", "UN0")),
          ("c", "Confirmed deletion (CN1 − CN0)", delta("CN1", "CN0"))]
vmax = max(abs(v) for _, _, d in panels for v in d.values())
POS = {"Joy", "Calmness"}  # positive-valence emotions; the rest are negative-valence
neg_cmap = LinearSegmentedColormap.from_list("neg", ["#f3e9e7", "#e8a596", "#c0392b", "#7f1d14"])
pos_cmap = LinearSegmentedColormap.from_list("pos", ["#e8f1ea", "#9fd1a8", "#2e9a3c", "#145a22"])
from matplotlib.colors import Normalize
norm = Normalize(vmin=0, vmax=vmax, clip=True)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.7))
step = 360 / n
for axp, (tag, title, d) in zip(axes, panels):
    axp.set_aspect("equal"); axp.axis("off"); axp.set_xlim(-1.6, 1.6); axp.set_ylim(-1.45, 1.45)
    for i, idx in enumerate(order):
        th1 = 90 - i * step; th0 = th1 - step
        nm = names[idx]; cm = pos_cmap if nm in POS else neg_cmap
        axp.add_patch(Wedge((0, 0), 1.0, th0, th1, width=0.55, facecolor=cm(norm(d[nm])), edgecolor="#d0d0d0" if d[nm] == 0 else "white", linewidth=2 if d[nm] else 0.8))
        mid = np.deg2rad((th0 + th1) / 2)
        axp.text(0.725 * np.cos(mid), 0.725 * np.sin(mid), (f"{d[nm]:+.0f}" if d[nm] else "0"), ha="center", va="center", fontsize=7,
                 color="white" if norm(d[nm]) > 0.6 else "#242424")
        axp.text(1.27 * np.cos(mid), 1.27 * np.sin(mid), nm, ha="center", va="center", fontsize=7.5, color="#242424")
        nxt = order[(i + 1) % n]
        b = np.deg2rad(th0)
        axp.text(1.09 * np.cos(b), 1.09 * np.sin(b), f"{S[idx, nxt]:.2f}", ha="center", va="center", fontsize=5.5, color="#7a7a7a")
    axp.set_title(f"{tag}  {title}", loc="left", fontsize=8.5, fontweight="bold")
for x0, cm, lab in [(0.22, neg_cmap, "Negative emotions"), (0.54, pos_cmap, "Positive emotions")]:
    cax = fig.add_axes([x0, 0.115, 0.24, 0.022])
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cm), cax=cax, orientation="horizontal")
    cb.ax.set_title(lab, fontsize=7, pad=3); cb.ax.tick_params(labelsize=6)
fig.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.2, wspace=0.04)
fig.text(0.5, 0.0, "Change in notice-only activation, deletion minus continuation (x10$^{-3}$)", ha="center", fontsize=7)
for ext in ("png", "svg"):
    fig.savefig(ROOT / "figures" / f"emotion_ring_v5.{ext}", dpi=300, bbox_inches="tight")
print("order:", [names[i] for i in order])
print("neighbour similarity:", [round(S[order[i], order[(i + 1) % n]], 2) for i in range(n)])
