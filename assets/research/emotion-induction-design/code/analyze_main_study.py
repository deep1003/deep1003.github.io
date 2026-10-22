"""Analysis of the main study (139 Ko-BBQ items x 5 conditions x 3 option orders).

Inputs : data/main_trials.csv (one row per trial, from run_main_study.py)
Outputs: data/main_table1_conditions.csv  Table 1, condition means
         data/main_table2_contrasts.csv   Table 2, H1-H3 and interaction
         data/main_table3_axes.csv        Table 3, L14 axis changes vs R
         data/main_supp_category.csv      Supp. table S1, category contrasts
         data/main_supp_position.csv      Supp. table S2, answer position and choice mass
         data/main_summary.json           numbers quoted in the text
         figures/main_fig1..3, main_supp_fig1..3 (.png, .svg)
Statistics: item means over the three option orders; paired differences;
95% intervals from a cluster bootstrap over Ko-BBQ templates (10,000 draws);
two-sided bootstrap p; Holm correction over H1-H3.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
D, F = ROOT / "data", ROOT / "figures"
B = 10_000
RNG = np.random.default_rng(20261022)
CONDS = ["R", "UN0", "UN1", "CN0", "CN1"]
COLORS = {"R": "#9e9e9e", "UN0": "#f4a3a3", "UN1": "#c62828", "CN0": "#9ec5e8", "CN1": "#1f5fa8"}
AXES = ["Fear", "Anxiety", "Desperation", "Sadness", "Anger", "Disgust", "Calmness", "Joy",
        "Uncertainty", "Certainty", "FA"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.spines.top": False,
                     "axes.spines.right": False})


def holm(ps):
    order = np.argsort(ps)
    adj = np.empty(len(ps))
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(ps) - rank) * ps[i]))
        adj[i] = running
    return adj


def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(F / f"{name}.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    tr = pd.read_csv(D / "main_trials.csv")
    tr["p_s_given_person"] = tr["p_biased"] / (tr["p_biased"] + tr["p_anti"])
    metrics = ["p_unknown", "p_biased", "p_anti", "p_s_given_person", "choice_mass"] + [f"cos_{a}" for a in AXES]
    item = tr.groupby(["item", "cluster", "category", "condition"])[metrics].mean().reset_index()
    wide = {m: item.pivot(index=["item", "cluster", "category"], columns="condition", values=m) for m in metrics}
    meta = wide["p_unknown"].index.to_frame(index=False)
    clusters = meta["cluster"].to_numpy()
    uniq = np.unique(clusters)
    idx_by_cluster = {c: np.where(clusters == c)[0] for c in uniq}
    draws = [np.concatenate([idx_by_cluster[c] for c in RNG.choice(uniq, len(uniq))]) for _ in range(B)]

    def boot(vec):
        vec = np.asarray(vec, dtype=float)
        est = float(np.nanmean(vec))
        bs = np.array([np.nanmean(vec[d]) for d in draws])
        lo, hi = np.percentile(bs, [2.5, 97.5])
        p = min(1.0, 2 * min((bs <= 0).mean(), (bs >= 0).mean()))
        return est, float(lo), float(hi), float(max(p, 1 / B)), bs

    # Table 1
    rows = []
    for c in CONDS:
        r = {"condition": c, "n_items": int(wide["p_unknown"][c].notna().sum())}
        for m in ["p_unknown", "p_biased", "p_anti", "p_s_given_person", "choice_mass"]:
            est, lo, hi, _, _ = boot(wide[m][c].to_numpy())
            r[m] = est
            r[f"{m}_lo"], r[f"{m}_hi"] = lo, hi
        rows.append(r)
    t1 = pd.DataFrame(rows)
    t1.to_csv(D / "main_table1_conditions.csv", index=False)

    # Table 2
    U = wide["p_unknown"]
    contrasts = {
        "H1: UN - R": (U["UN0"] + U["UN1"]) / 2 - U["R"],
        "H2: CN - R": (U["CN0"] + U["CN1"]) / 2 - U["R"],
        "H3: deletion - preservation": (U["UN1"] + U["CN1"]) / 2 - (U["UN0"] + U["CN0"]) / 2,
        "Interaction: (UN1-UN0) - (CN1-CN0)": (U["UN1"] - U["UN0"]) - (U["CN1"] - U["CN0"]),
        "Simple: UN0 - R": U["UN0"] - U["R"], "Simple: UN1 - R": U["UN1"] - U["R"],
        "Simple: CN0 - R": U["CN0"] - U["R"], "Simple: CN1 - R": U["CN1"] - U["R"],
        "Simple: UN1 - UN0": U["UN1"] - U["UN0"], "Simple: CN1 - CN0": U["CN1"] - U["CN0"],
        "Simple: UN0 - CN0": U["UN0"] - U["CN0"], "Simple: UN1 - CN1": U["UN1"] - U["CN1"],
    }
    rows, boots = [], {}
    for name, vec in contrasts.items():
        est, lo, hi, p, bs = boot(100 * vec.to_numpy())
        rows.append({"contrast": name, "estimate_pp": est, "ci_lo": lo, "ci_hi": hi, "p_boot": p})
        boots[name] = bs
    t2 = pd.DataFrame(rows)
    conf = t2["contrast"].str.startswith("H")
    t2.loc[conf, "p_holm"] = holm(t2.loc[conf, "p_boot"].to_numpy())
    t2.to_csv(D / "main_table2_contrasts.csv", index=False)

    # Table 3
    rows = []
    for a in AXES:
        w = wide[f"cos_{a}"]
        for c in CONDS[1:]:
            est, lo, hi, p, _ = boot(1000 * (w[c] - w["R"]).to_numpy())
            rows.append({"axis": a, "condition": c, "delta_x1000": est, "ci_lo": lo, "ci_hi": hi, "p_boot": p})
    t3 = pd.DataFrame(rows)
    t3["p_holm_within_axis_set"] = holm(t3["p_boot"].to_numpy())
    t3.to_csv(D / "main_table3_axes.csv", index=False)

    # Supplementary S1: category contrasts
    rows = []
    for cat, sub in meta.groupby("category"):
        ix = sub.index.to_numpy()
        for name in ["H1: UN - R", "H2: CN - R", "H3: deletion - preservation"]:
            v = 100 * contrasts[name].to_numpy()[ix]
            rows.append({"category": cat, "contrast": name, "n_items": len(ix), "estimate_pp": float(np.mean(v)),
                         "sd_pp": float(np.std(v, ddof=1)) if len(ix) > 1 else np.nan})
    pd.DataFrame(rows).to_csv(D / "main_supp_category.csv", index=False)

    # Supplementary S2: position of the unknown option, choice mass
    s2 = tr.groupby(["condition", "pos_unknown"]).agg(p_unknown=("p_unknown", "mean"),
                                                       choice_mass=("choice_mass", "mean"),
                                                       n=("p_unknown", "size")).reset_index()
    s2.to_csv(D / "main_supp_position.csv", index=False)

    # Figure 1: P(unknown) by condition
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    x = np.arange(len(CONDS))
    for i, c in enumerate(CONDS):
        row = t1.loc[t1.condition == c].iloc[0]
        ax.bar(i, 100 * row.p_unknown, 0.65, color=COLORS[c])
        ax.errorbar(i, 100 * row.p_unknown, yerr=[[100 * (row.p_unknown - row.p_unknown_lo)],
                                                 [100 * (row.p_unknown_hi - row.p_unknown)]],
                    color="#212121", capsize=2, linewidth=0.8)
        jitter = RNG.uniform(-0.18, 0.18, len(U))
        ax.scatter(i + jitter, 100 * U[c].to_numpy(), s=2, color="#424242", alpha=0.25, linewidth=0)
    ax.set_xticks(x, CONDS)
    ax.set_ylim(0, 100)
    ax.set_ylabel("P(unknown), %")
    ax.set_title("P(unknown) by condition", loc="left", fontsize=8, fontweight="bold")
    save(fig, "main_fig1_unknown")

    # Figure 2: contrasts forest plot
    names = ["H1: UN - R", "H2: CN - R", "H3: deletion - preservation", "Interaction: (UN1-UN0) - (CN1-CN0)",
             "Simple: UN1 - UN0", "Simple: CN1 - CN0"]
    sub = t2.set_index("contrast").loc[names]
    fig, ax = plt.subplots(figsize=(3.8, 2.4))
    y = np.arange(len(names))[::-1]
    ax.errorbar(sub.estimate_pp, y, xerr=[sub.estimate_pp - sub.ci_lo, sub.ci_hi - sub.estimate_pp],
                fmt="o", color="#1f5fa8", ms=3, capsize=2, linewidth=0.8)
    ax.axvline(0, color="#616161", linewidth=0.6, linestyle="--")
    ax.set_yticks(y, [n.replace("Interaction: ", "Interaction ").replace("Simple: ", "") for n in names], fontsize=6.5)
    ax.set_xlabel("Difference in P(unknown), percentage points")
    ax.set_title("Paired contrasts (95% cluster bootstrap)", loc="left", fontsize=8, fontweight="bold")
    save(fig, "main_fig2_contrasts")

    # Figure 3: L14 axis changes vs R
    mat = t3.pivot(index="axis", columns="condition", values="delta_x1000").loc[AXES, CONDS[1:]]
    lim = float(np.nanmax(np.abs(mat.to_numpy())))
    fig, ax = plt.subplots(figsize=(3.4, 3.2))
    im = ax.imshow(mat.to_numpy(), cmap="RdBu_r", vmin=-lim, vmax=lim, aspect="auto")
    ax.set_xticks(range(4), CONDS[1:])
    ax.set_yticks(range(len(AXES)), AXES)
    for (i, j), v in np.ndenumerate(mat.to_numpy()):
        ax.text(j, i, f"{v:.1f}", ha="center", va="center", fontsize=5.5,
                color="white" if abs(v) > 0.6 * lim else "#212121")
    cb = fig.colorbar(im, ax=ax, shrink=0.8)
    cb.set_label("Change in axis cosine vs R (x1000)", fontsize=6.5)
    ax.set_title("L14 emotion and appraisal axes", loc="left", fontsize=8, fontweight="bold")
    save(fig, "main_fig3_axes")

    # Supp. Fig 1: category contrasts
    s1 = pd.read_csv(D / "main_supp_category.csv")
    piv = s1.pivot(index="category", columns="contrast", values="estimate_pp")
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    yy = np.arange(len(piv))
    for k, (col, colr) in enumerate(zip(piv.columns, ["#c62828", "#1f5fa8", "#616161"])):
        ax.barh(yy + (k - 1) * 0.27, piv[col], 0.27, color=colr, label=col)
    ax.set_yticks(yy, piv.index, fontsize=6.5)
    ax.axvline(0, color="#616161", linewidth=0.6)
    ax.set_xlabel("Difference in P(unknown), percentage points")
    ax.legend(frameon=False, fontsize=6)
    ax.set_title("Contrasts by Ko-BBQ category", loc="left", fontsize=8, fontweight="bold")
    save(fig, "main_supp_fig1_category")

    # Supp. Fig 2: item-level effects
    fig, ax = plt.subplots(figsize=(3.2, 3.0))
    a = 100 * contrasts["Simple: UN1 - R"].to_numpy()
    b = 100 * contrasts["Simple: CN1 - R"].to_numpy()
    ax.scatter(100 * contrasts["H1: UN - R"].to_numpy(), 100 * contrasts["H2: CN - R"].to_numpy(),
               s=6, color="#1f5fa8", alpha=0.6, linewidth=0)
    ax.axhline(0, color="#9e9e9e", linewidth=0.5)
    ax.axvline(0, color="#9e9e9e", linewidth=0.5)
    ax.set_xlabel("UN - R, percentage points")
    ax.set_ylabel("CN - R, percentage points")
    ax.set_title("Item-level effects", loc="left", fontsize=8, fontweight="bold")
    save(fig, "main_supp_fig2_items")

    # Supp. Fig 3: axis change vs behaviour change across items
    fig, axs = plt.subplots(1, 2, figsize=(5.6, 2.5))
    corr = {}
    for axx, c in zip(axs, ["UN1", "CN1"]):
        beh = 100 * (U[c] - U["R"]).to_numpy()
        ax_fear = 1000 * (wide["cos_Fear"][c] - wide["cos_Fear"]["R"]).to_numpy()
        r = float(pd.Series(beh).corr(pd.Series(ax_fear), method="spearman"))
        corr[c] = r
        axx.scatter(ax_fear, beh, s=5, color=COLORS[c], alpha=0.6, linewidth=0)
        axx.set_xlabel("Fear-axis change vs R (x1000)")
        axx.set_ylabel("P(unknown) change vs R, pp")
        axx.set_title(f"{c}  Spearman rho = {r:.2f}", loc="left", fontsize=7.5, fontweight="bold")
    save(fig, "main_supp_fig3_axis_behaviour")

    summary = {"n_trials": int(len(tr)), "n_items": int(len(U)), "n_clusters": int(len(uniq)),
               "bootstrap_draws": B, "table1": t1.to_dict("records"), "table2": t2.to_dict("records"),
               "fear_behaviour_spearman": corr,
               "choice_mass_min": float(tr["choice_mass"].min()), "choice_mass_mean": float(tr["choice_mass"].mean())}
    (D / "main_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=float))
    print(t1.round(4).to_string())
    print(t2.round(3).to_string())
    print(mat.round(2).to_string())


if __name__ == "__main__":
    main()
