"""Rebuild two homepage figures (2026-11-17).
1. national_rates: employment rate (left panel) and unemployment rate (right panel).
2. exposure_growth_all: observed 2022-2025 employment change against 2025 THAIE, 162 occupations.
No titles or notes inside the images; captions live in index.html.
"""
import json, sys
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

P = sys.argv[1].rstrip("/") + "/"
BLUE, RED, INK, MUTED = "#2f5b93", "#a3363f", "#1c2530", "#5b6570"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.edgecolor": INK, "svg.fonttype": "none"})

# ---- 1. national rates, side by side
n = pd.read_csv(P + "overview_v2/national_rates.csv")
fig, axes = plt.subplots(1, 2, figsize=(11, 3.9))
for ax, col, color, name in [(axes[0], "employment_rate", BLUE, "Employment rate (%)"),
                             (axes[1], "unemployment_rate", RED, "Unemployment rate (%)")]:
    y = n[col].values
    pad = (y.max() - y.min()) * 0.18
    ax.axvspan(2023, 2025.5, color="#e9ecea", zorder=0)
    ax.axvline(2023, color=INK, lw=1, ls=(0, (4, 3)), zorder=1)
    ax.plot(n.year, y, color=color, lw=2, marker="o", ms=4.5, zorder=3)
    ax.set_ylim(y.min() - pad, y.max() + pad)
    ax.set_xlim(2012.6, 2025.5)
    ax.set_xticks([2013, 2016, 2019, 2022, 2025])
    ax.grid(axis="y", color="#e6e6e6", lw=0.8)
    ax.set_title(name, loc="left", fontsize=12, fontweight="bold", color=INK, pad=10)
    ax.set_xlabel("Year (May)", color=MUTED)
    ax.tick_params(colors=INK, length=3)
    for yr, dy in [(2022, -1), (2025, 1)]:
        v = float(n.loc[n.year == yr, col].iloc[0])
        up = dy > 0 if col == "employment_rate" else dy < 0
        ax.annotate(f"{v:.1f}", (yr, v), xytext=(-2 if yr == 2025 else -6, 9 if up else -15),
                    textcoords="offset points", ha="right" if yr == 2022 else "center",
                    fontsize=10.5, fontweight="bold", color=INK)
fig.tight_layout(w_pad=3)
for ext in ("png", "svg", "pdf"):
    fig.savefig(P + f"overview_v2/national_rates.{ext}", dpi=220)
plt.close(fig)

# ---- 2. all-occupation scatter
d = pd.read_csv(P + "labour_2025/observed_growth_scatter.csv")
names = {int(o["code"]): o["name"] for o in json.load(open(P + "occupations.json"))}

def wls(df, weighted=True):
    X = np.c_[np.ones(len(df)), df.th_gpt5_2025.values * 10]
    w = df.w.values if weighted else np.ones(len(df)); y = df.growth.values
    A = np.linalg.inv(X.T @ (w[:, None] * X)); b = A @ (X.T @ (w * y)); e = y - X @ b
    h = np.einsum("ij,jk,ik->i", X * np.sqrt(w)[:, None], A, X * np.sqrt(w)[:, None])
    V = A @ (X.T @ ((w**2 * e**2 / (1 - h)**2)[:, None] * X)) @ A
    yb = np.average(y, weights=w)
    return b, V, 1 - (w * e**2).sum() / (w * (y - yb)**2).sum()

b, V, r2 = wls(d)
res = {"n": int(len(d)), "slope_per_0_1": b[1], "HC3_SE": V[1, 1]**.5, "r_squared": r2,
       "outcome": "relative percent change in employment, 2022 to 2025 (annual mean of April and October waves)",
       "weights": "baseline employment", "exposure": "2025 THAIE (GPT-5 horizon)"}
b2, V2, r22 = wls(d[d.growth < 100]); res["excluding_growth_over_100pct"] = {"slope_per_0_1": b2[1], "HC3_SE": V2[1, 1]**.5, "r_squared": r22, "n": int((d.growth < 100).sum())}
b3, V3, r23 = wls(d, False); res["unweighted"] = {"slope_per_0_1": b3[1], "HC3_SE": V3[1, 1]**.5, "r_squared": r23}
json.dump(res, open(P + "overview_v2/exposure_growth_all.json", "w"), indent=2)
print(json.dumps(res, indent=1))

fig, ax = plt.subplots(figsize=(11, 5.2))
ax.axhline(0, color="#9aa0a6", lw=1, zorder=1)
xs = np.linspace(d.th_gpt5_2025.min(), d.th_gpt5_2025.max(), 100); Xs = np.c_[np.ones(100), xs * 10]
fit = Xs @ b; se = np.sqrt(np.einsum("ij,jk,ik->i", Xs, V, Xs))
ax.fill_between(xs, fit - 1.96 * se, fit + 1.96 * se, color=BLUE, alpha=0.13, lw=0, zorder=2)
ax.plot(xs, fit, color=BLUE, lw=2, zorder=4)
ax.scatter(d.th_gpt5_2025, d.growth, s=14 + 190 * d.w / d.w.max(), color=BLUE, alpha=0.55,
           edgecolor="white", lw=0.7, zorder=3)
for code, dx, dy, ha in [(875, 8, 0, "left")]:
    r = d[d.occ == code].iloc[0]
    ax.annotate(names.get(code, str(code)), (r.th_gpt5_2025, r.growth), xytext=(dx, dy),
                textcoords="offset points", ha=ha, va="center", fontsize=9.5, color=MUTED)
ax.set_xlabel("Time-Horizon AI Exposure, 2025 reference", color=INK)
ax.set_ylabel("Employment change, 2022–2025 (%)", color=INK)
ax.grid(color="#ececec", lw=0.8); ax.set_axisbelow(True); ax.tick_params(colors=INK, length=3)
fig.tight_layout()
for ext in ("png", "svg", "pdf"):
    fig.savefig(P + f"overview_v2/exposure_growth_all.{ext}", dpi=220)
