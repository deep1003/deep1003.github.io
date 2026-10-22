"""Analysis of main study v5.

Inputs : data/v5_t2_trials.csv (behaviour + t2 axes), data/v5_t1.csv (t1 axes, 6 sentences per condition)
Outputs: data/v5_table1_conditions.csv, v5_table2_contrasts.csv, v5_table3_axes.csv,
         v5_supp_position.csv, v5_supp_category.csv, v5_summary.json,
         figures/v5_fig1_unknown, v5_fig2_contrasts, v5_fig3_axes, v5_supp_fig1_items, v5_supp_fig2_t1_sentences (png, svg)
Primary contrasts (Holm over three): CN1 - CN0, UN1 - UN0, (CN1 - CN0) - (UN1 - UN0).
Secondary: each condition - R. Behaviour and t2: item-level means over 3 orders,
cluster bootstrap over Ko-BBQ templates (10,000 draws, seed 20261022).
t1: one value per sentence; 6 sentences per condition; Welch t-test between conditions.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
DATA, FIG = ROOT / "data", ROOT / "figures"
ORDER = ["R", "UN0", "UN1", "CN0", "CN1"]
COLORS = {"R": "#9e9e9e", "UN0": "#f4a3a3", "UN1": "#c62828", "CN0": "#9ec5e8", "CN1": "#1f5fa8"}
AXES = ["Fear", "Anxiety", "Desperation", "Calmness", "Sadness", "Anger", "Disgust", "Joy", "Uncertainty", "Certainty", "FA"]
B, SEED = 10000, 20261022


def holm(ps):
    ps = np.asarray(ps); o = np.argsort(ps); adj = np.empty_like(ps); m = len(ps); run = 0
    for r, i in enumerate(o):
        run = max(run, min(1, (m - r) * ps[i])); adj[i] = run
    return adj


def boot_setup(item_cluster):
    rng = np.random.default_rng(SEED)
    cl = item_cluster.unique()
    draws = rng.integers(0, len(cl), size=(B, len(cl)))
    return cl, draws


def cluster_ci(vec, item_cluster, cl, draws):
    """vec: Series indexed by item. Returns est, lo, hi, two-sided p."""
    g = vec.groupby(item_cluster).agg(["sum", "count"]).reindex(cl)
    s, n = g["sum"].values, g["count"].values
    bs = s[draws].sum(1) / n[draws].sum(1)
    est = vec.mean()
    p = min(1.0, 2 * min((bs <= 0).mean(), (bs >= 0).mean()))
    return est, np.percentile(bs, 2.5), np.percentile(bs, 97.5), max(p, 1 / B)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.spines.top": False, "axes.spines.right": False})

    d = pd.read_csv(DATA / "v5_t2_trials.csv")
    t1 = pd.read_csv(DATA / "v5_t1.csv")
    # Keep items with all 5 conditions x 3 orders (an interim sample uses the items finished so far).
    full = d.groupby("item").size(); d = d[d.item.isin(full[full == 15].index)].copy()
    n_items = d.item.nunique()
    for k in ["unknown", "biased", "anti"]:
        d[f"p_{k}"] *= 100
    d["p_stereo_given_person"] = 100 * d.p_biased / (d.p_biased + d.p_anti)
    ic = d.groupby("item").cluster.first()
    cl, draws = boot_setup(ic)
    item = d.groupby(["item", "condition"])[["p_unknown", "p_biased", "p_anti", "p_stereo_given_person"]].mean().unstack()

    # Table 1: condition means
    t1rows = []
    for c in ORDER:
        s = d[d.condition == c]
        t1rows.append({"condition": c, "P_unknown": s.p_unknown.mean(), "P_stereotyped": s.p_biased.mean(),
                       "P_anti": s.p_anti.mean(), "P_stereo_given_person": s.p_stereo_given_person.mean(),
                       "choice_mass_min": s.choice_mass.min(), "n_trials": len(s)})
    tab1 = pd.DataFrame(t1rows).round(3); tab1.to_csv(DATA / "v5_table1_conditions.csv", index=False)

    # Table 2: contrasts
    pu = item["p_unknown"]
    defs = [("H1", "CN1 - CN0", pu.CN1 - pu.CN0, "primary"),
            ("H2", "UN1 - UN0", pu.UN1 - pu.UN0, "primary"),
            ("H3", "(CN1 - CN0) - (UN1 - UN0)", (pu.CN1 - pu.CN0) - (pu.UN1 - pu.UN0), "primary")]
    defs += [("S", f"{c} - R", pu[c] - pu.R, "secondary") for c in ["UN0", "UN1", "CN0", "CN1"]]
    defs += [("S", "UN - R (mean)", (pu.UN0 + pu.UN1) / 2 - pu.R, "secondary"),
             ("S", "CN - R (mean)", (pu.CN0 + pu.CN1) / 2 - pu.R, "secondary")]
    rows = []
    for h, name, v, kind in defs:
        e, lo, hi, p = cluster_ci(v, ic, cl, draws)
        rows.append({"hypothesis": h, "contrast": name, "type": kind, "estimate_pp": e, "ci_low": lo, "ci_high": hi, "p": p,
                     "items_up_gt10": int((v > 10).sum()), "items_down_gt10": int((v < -10).sum())})
    tab2 = pd.DataFrame(rows)
    prim = tab2.type == "primary"
    tab2["p_holm"] = np.nan; tab2.loc[prim, "p_holm"] = holm(tab2.loc[prim, "p"].values)
    tab2 = tab2.round(4); tab2.to_csv(DATA / "v5_table2_contrasts.csv", index=False)

    # Table 3: axes, t1 (sentence level) and t2 (item level), delta vs R and 1 - 0 contrasts (x1000)
    rows = []
    t2i = d.groupby(["item", "condition"])[[f"t2_{a}" for a in AXES]].mean().unstack()
    for a in AXES:
        r = {"axis": a}
        x = t1.groupby("condition")[f"t1_{a}"]
        for c in ["UN0", "UN1", "CN0", "CN1"]:
            r[f"t1_{c}_minus_R"] = 1000 * (x.mean()[c] - x.mean()["R"])
            r[f"t2_{c}_minus_R"] = 1000 * (t2i[f"t2_{a}"][c] - t2i[f"t2_{a}"]["R"]).mean()
        for s in ["CN", "UN"]:
            a1, a0 = t1[t1.condition == s + "1"][f"t1_{a}"], t1[t1.condition == s + "0"][f"t1_{a}"]
            r[f"t1_{s}1_minus_{s}0"] = 1000 * (a1.mean() - a0.mean())
            r[f"t1_{s}_p_welch"] = stats.ttest_ind(a1, a0, equal_var=False).pvalue
            e, lo, hi, p = cluster_ci(t2i[f"t2_{a}"][s + "1"] - t2i[f"t2_{a}"][s + "0"], ic, cl, draws)
            r[f"t2_{s}1_minus_{s}0"], r[f"t2_{s}_ci_low"], r[f"t2_{s}_ci_high"] = 1000 * e, 1000 * lo, 1000 * hi
        rows.append(r)
    tab3 = pd.DataFrame(rows).round(4); tab3.to_csv(DATA / "v5_table3_axes.csv", index=False)

    # Supplementary: position and category
    pos = d.groupby(["condition", "pos_unknown"]).p_unknown.mean().unstack().reindex(ORDER).round(2)
    pos.to_csv(DATA / "v5_supp_position.csv")
    cat = d.groupby(["item", "condition", "category"]).p_unknown.mean().unstack("condition").reset_index()
    cat["CN1_minus_CN0"] = cat.CN1 - cat.CN0; cat["UN1_minus_UN0"] = cat.UN1 - cat.UN0
    cats = cat.groupby("category")[["CN1_minus_CN0", "UN1_minus_UN0"]].agg(["mean", "count"]).round(2)
    cats.to_csv(DATA / "v5_supp_category.csv")

    # Item-level link between t2 Fear change and behaviour change
    link = {}
    for s in ["CN", "UN"]:
        df = t2i["t2_Fear"][s + "1"] - t2i["t2_Fear"][s + "0"]; db = pu[s + "1"] - pu[s + "0"]
        rho, p = stats.spearmanr(df, db); link[s] = {"spearman_rho": round(float(rho), 3), "p": round(float(p), 4)}

    # Figure 1
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    for i, c in enumerate(ORDER):
        v = pu[c]; e, lo, hi, _ = cluster_ci(v, ic, cl, draws)
        ax.bar(i, e, color=COLORS[c], width=0.65, edgecolor="white")
        ax.errorbar(i, e, yerr=[[e - lo], [hi - e]], color="#212121", capsize=2, lw=0.8)
    ax.set_xticks(range(5), ORDER); ax.set_ylabel("P(unknown) (%)"); ax.set_ylim(0, 100)
    fig.tight_layout()
    for ext in ("png", "svg"): fig.savefig(FIG / f"v5_fig1_unknown.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Figure 2: contrasts
    fig, ax = plt.subplots(figsize=(4.6, 2.8))
    labs = list(tab2.contrast)
    for i, r in tab2.iterrows():
        col = "#1f5fa8" if r.type == "primary" else "#757575"
        ax.errorbar(r.estimate_pp, i, xerr=[[r.estimate_pp - r.ci_low], [r.ci_high - r.estimate_pp]], fmt="o", color=col, ms=4, capsize=2, lw=0.9)
    ax.axvline(0, color="#424242", lw=0.6); ax.set_yticks(range(len(labs)), labs); ax.invert_yaxis()
    ax.axhline(2.5, color="#bdbdbd", lw=0.5, ls="--")
    ax.set_xlabel("Difference in P(unknown) (percentage points)")
    fig.tight_layout()
    for ext in ("png", "svg"): fig.savefig(FIG / f"v5_fig2_contrasts.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Figure 3: axes, a t1 deltas vs R, b t2 deltas vs R
    show = ["Fear", "Anxiety", "Desperation", "Calmness", "Joy", "Uncertainty", "Certainty"]
    fig, axs = plt.subplots(1, 2, figsize=(7.1, 2.8))
    for ax, tp, title in [(axs[0], "t1", "a  Notice only (t1)"), (axs[1], "t2", "b  Notice + question (t2)")]:
        w = 0.2
        for j, c in enumerate(["UN0", "UN1", "CN0", "CN1"]):
            vals = [tab3.set_index("axis").loc[a, f"{tp}_{c}_minus_R"] for a in show]
            ax.bar(np.arange(len(show)) + (j - 1.5) * w, vals, w, color=COLORS[c], label=c, edgecolor="white", linewidth=0.3)
        ax.axhline(0, color="#424242", lw=0.5); ax.set_xticks(range(len(show)), show, rotation=35, ha="right")
        ax.set_ylabel("Cosine change vs R (x10$^{-3}$)"); ax.set_title(title, loc="left", fontweight="bold")
    axs[0].legend(frameon=False, fontsize=6.5, ncol=2)
    fig.tight_layout()
    for ext in ("png", "svg"): fig.savefig(FIG / f"v5_fig3_axes.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Supp Fig 1: item-level CN1-CN0 vs UN1-UN0
    fig, ax = plt.subplots(figsize=(3.2, 3.0))
    ax.scatter(pu.UN1 - pu.UN0, pu.CN1 - pu.CN0, s=8, color="#1f5fa8", alpha=0.6, edgecolor="none")
    ax.axhline(0, color="#9e9e9e", lw=0.5); ax.axvline(0, color="#9e9e9e", lw=0.5)
    ax.set_xlabel("UN1 - UN0 (pp)"); ax.set_ylabel("CN1 - CN0 (pp)")
    fig.tight_layout()
    for ext in ("png", "svg"): fig.savefig(FIG / f"v5_supp_fig1_items.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Supp Fig 2: t1 Fear per sentence
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    base = t1[t1.condition == "R"]["t1_Fear"].mean()
    for i, c in enumerate(ORDER):
        v = 1000 * (t1[t1.condition == c]["t1_Fear"] - base)
        ax.scatter(np.full(len(v), i) + np.linspace(-0.15, 0.15, len(v)), v, color=COLORS[c], s=14, edgecolor="#424242", linewidth=0.3)
        ax.hlines(v.mean(), i - 0.25, i + 0.25, color="#212121", lw=1)
    ax.axhline(0, color="#9e9e9e", lw=0.5); ax.set_xticks(range(5), ORDER)
    ax.set_ylabel("t1 Fear cosine vs R mean (x10$^{-3}$)")
    fig.tight_layout()
    for ext in ("png", "svg"): fig.savefig(FIG / f"v5_supp_fig2_t1_sentences.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)

    summary = {"n_items": int(n_items), "n_clusters": int(d.cluster.nunique()), "n_trials": len(d), "choice_mass_min": float(d.choice_mass.min()),
               "bimodal_share": float(((d.p_unknown < 5) | (d.p_unknown > 95)).mean()),
               "t2_fear_behaviour_link": link}
    (DATA / "v5_summary.json").write_text(json.dumps(summary, indent=2))
    print(tab1.to_string()); print(tab2.to_string()); print(pos); print(json.dumps(summary, indent=1))
    print(tab3[["axis", "t1_CN1_minus_CN0", "t1_CN_p_welch", "t1_UN1_minus_UN0", "t1_UN_p_welch", "t2_CN1_minus_CN0", "t2_CN_ci_low", "t2_CN_ci_high", "t2_UN1_minus_UN0"]].round(2).to_string())


if __name__ == "__main__":
    main()
