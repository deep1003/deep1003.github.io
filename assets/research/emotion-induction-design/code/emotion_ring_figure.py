"""Emotion ring: 11 L14 emotion axes as equal wedges of a circle.

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
names = [str(n) for n in ax["names"]]
V = ax["directions"].astype(float)
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

panels = [("a", "Undecided deletion (UN1 − UN0)", delta("UN1", "UN0")),
          ("b", "Confirmed deletion (CN1 − CN0)", delta("CN1", "CN0"))]
vmax = max(abs(v) for _, _, d in panels for v in d.values())
cmap = LinearSegmentedColormap.from_list("div", ["#2b6cb0", "#f0efec", "#c0392b"])
norm = TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.7))
step = 360 / n
for axp, (tag, title, d) in zip(axes, panels):
    axp.set_aspect("equal"); axp.axis("off"); axp.set_xlim(-1.6, 1.6); axp.set_ylim(-1.45, 1.45)
    for i, idx in enumerate(order):
        th1 = 90 - i * step; th0 = th1 - step
        axp.add_patch(Wedge((0, 0), 1.0, th0, th1, width=0.55, facecolor=cmap(norm(d[names[idx]])),
                            edgecolor="white", linewidth=2))
        mid = np.deg2rad((th0 + th1) / 2)
        axp.text(0.725 * np.cos(mid), 0.725 * np.sin(mid), f"{d[names[idx]]:+.0f}", ha="center", va="center", fontsize=7, color="#242424")
        lab = names[idx]
        axp.text(1.27 * np.cos(mid), 1.27 * np.sin(mid), lab, ha="center", va="center", fontsize=7.5, color="#242424")
        # similarity on the boundary with the next wedge
        nxt = order[(i + 1) % n]
        b = np.deg2rad(th0)
        axp.text(1.09 * np.cos(b), 1.09 * np.sin(b), f"{S[idx, nxt]:.2f}", ha="center", va="center", fontsize=5.5, color="#7a7a7a")
    axp.set_title(f"{tag}  {title}", loc="left", fontsize=8.5, fontweight="bold")
cax = fig.add_axes([0.35, 0.1, 0.3, 0.025])
cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax, orientation="horizontal")
cb.set_label("Change in notice-only activation (x10$^{-3}$)", fontsize=7); cb.ax.tick_params(labelsize=6.5)
fig.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.2, wspace=0.04)
for ext in ("png", "svg"):
    fig.savefig(ROOT / "figures" / f"emotion_ring_v5.{ext}", dpi=300, bbox_inches="tight")
print("order:", [names[i] for i in order])
print("neighbour similarity:", [round(S[order[i], order[(i + 1) % n]], 2) for i in range(n)])
