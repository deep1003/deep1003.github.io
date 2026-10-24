"""Equal-area emotion atlas for v5 (same geometry and colour ramps as the v2 atlas).

Each of the eight emotion regions is split into 139 items x 3 option orders = 417 cells.
Cell colour = L14 cosine at the decision position (t2) minus the same item and order under R.
Geometry is reused from data/atlas6/region_geometry.json (PCA-placed equal-area power diagram).
Outputs figures/Fig_emotion_atlas_v5.png/.svg.
"""
import colorsys
import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize, to_rgb
from matplotlib.patches import Polygon

P = Path(__file__).resolve().parents[1]
G = json.loads((P / "data/atlas6/region_geometry.json").read_text())
AX, polys, tiles = G["axes"], [np.array(p) for p in G["polygons"]], [np.array(t) for t in G["tiles"]]
M = pd.read_csv(P / "data/atlas6/tile_layout.csv")
COL = dict(zip(AX, ["#D9382C", "#B66B2F", "#A82418", "#79529B", "#86B654", "#F28B7A", "#661226", "#2E9A3C"]))
d = pd.read_csv(P / "data/v5_t2_trials.csv")
long = d.melt(id_vars=["item", "condition", "rotation"], value_vars=[f"t2_{a}" for a in AX], var_name="axis", value_name="cosine")
long["axis"] = long.axis.str[3:]
ref = long[long.condition == "R"][["item", "rotation", "axis", "cosine"]].rename(columns={"cosine": "ref"})
v = long.merge(ref, on=["item", "rotation", "axis"])
v["delta"] = v.cosine - v.ref
vals = M.merge(v, on=["axis", "item", "rotation"], validate="one_to_many")
assert len(vals) == 3336 * 5
C = [("UN0", "UN0 · Undecided, harmless change"), ("UN1", "UN1 · Undecided, deletion"),
     ("CN0", "CN0 · Confirmed, harmless change"), ("CN1", "CN1 · Confirmed, deletion")]
sub = vals[vals.condition != "R"]
lo, hi = float(np.percentile(sub.delta, 1)), float(np.percentile(sub.delta, 99))
lo, hi = min(lo, -1e-5), max(hi, 1e-5)
norm = Normalize(lo, hi, clip=True)
zero = -lo / (hi - lo)


def ramp(color):
    h, l, s = colorsys.rgb_to_hls(*to_rgb(color)); m = np.array(colorsys.hls_to_rgb(h, .42, s))
    stops = [(0, m * .18), (zero, m * .45), (zero + (1 - zero) * .36, m),
             (zero + (1 - zero) * .68, .55 * m + .45 * np.array(to_rgb("#FFE84A"))), (1, to_rgb("#FFFAA0"))]
    return LinearSegmentedColormap.from_list("emotion", stops)


cmaps = {a: ramp(COL[a]) for a in AX}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7})
fig = plt.figure(figsize=(180 / 25.4, 200 / 25.4))
for k, (c, label) in enumerate(C):
    x = .025 + (k % 2) * .48; y = .55 - (k // 2) * .4
    ax = fig.add_axes([x, y, .43, .37]); ax.set_aspect("equal"); ax.axis("off")
    w = vals[vals.condition == c].set_index("tile_id").reindex(range(3336))
    colors = [cmaps[a](norm(dv)) for a, dv in zip(w.axis, w.delta)]
    ax.add_collection(PolyCollection(tiles, facecolors=colors, edgecolors="none", rasterized=True, antialiaseds=False))
    for a, p in zip(AX, polys):
        ax.add_patch(Polygon(p, fill=False, edgecolor="white", linewidth=.6))
        cx, cy = p[:, 0].mean(), p[:, 1].mean()
        ax.text(cx, cy, a, ha="center", va="center", fontsize=6.4, fontweight="bold", color="white",
                path_effects=[pe.withStroke(linewidth=1.4, foreground="#222")])
    ax.set(xlim=(-1.03, 1.03), ylim=(-1.03, 1.03)); ax.set_title(chr(97 + k) + "  " + label, loc="left", pad=4)
for k, a in enumerate(AX):
    x = .035 + (k % 4) * .24; y = .1 - (k // 4) * .045
    cax = fig.add_axes([x, y, .17, .01]); cax.imshow(np.linspace(0, 1, 256)[None, :], cmap=cmaps[a], aspect="auto", extent=(lo, hi, 0, 1))
    cax.set_yticks([]); cax.set_xticks([lo, 0, hi]); cax.set_xticklabels(["" if abs(lo) < 5e-4 else f"{lo:+.3f}", "0", f"{hi:+.3f}"], fontsize=4.8)
    cax.tick_params(length=1, pad=1); cax.set_title(a, fontsize=5.8, pad=2)
for ext in ("png", "svg"):
    fig.savefig(P / "figures" / f"Fig_emotion_atlas_v5.{ext}", dpi=400, bbox_inches="tight", pad_inches=.04)
print(lo, hi)
