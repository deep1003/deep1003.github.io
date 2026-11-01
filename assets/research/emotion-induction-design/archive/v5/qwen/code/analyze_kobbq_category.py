"""Category-level analysis of the item-level link between emotion readouts and withholding judgment (Ko-BBQ).

Inputs: one or more Ko-BBQ result dirs (each with t2_trials.csv), e.g. <RES>/kobbq and <RES>/kobbq_expand.
Unit: item (option orders averaged). Change = deletion minus continuation within status (CN1 - CN0, UN1 - UN0).
For each category (48 items each after expansion) and each axis, Spearman rho between the item change in the
decision-position readout and the item change in P(unknown); 95% CI by template-cluster bootstrap (1,000 draws);
Benjamini-Hochberg within each contrast. Also reports the behavioral change per category and a valence index
(NegBundle minus PosBundle readout change).
Usage: python analyze_kobbq_category.py <out_dir> <res_dir> [<res_dir> ...]
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr

AX = ["Fear", "Anxiety", "Sadness", "Anger", "Disgust", "Desperation", "Calmness", "Joy", "Uncertainty", "Certainty"]
NEG, POS = AX[:6], ["Calmness", "Joy"]
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
d = pd.concat([pd.read_csv(Path(p) / "t2_trials.csv") for p in sys.argv[2:]]).drop_duplicates(["item", "condition", "rotation"])
cols = ["p_unknown", "p_biased", "p_anti"] + [f"t2_{a}" for a in AX]
g = d.groupby(["item", "category", "cluster", "condition"])[cols].mean().reset_index()
rng = np.random.default_rng(20261026)


def boot_rho(x, y, cl, B=1000):
    ids = pd.factorize(cl)[0]; groups = [np.where(ids == k)[0] for k in range(ids.max() + 1)]; out = []
    for _ in range(B):
        idx = np.concatenate([groups[k] for k in rng.integers(0, len(groups), len(groups))])
        if np.std(x[idx]) == 0 or np.std(y[idx]) == 0: continue
        out.append(np.corrcoef(rankdata(x[idx]), rankdata(y[idx]))[0, 1])
    return np.percentile(out, [2.5, 97.5])


def bh(p):
    p = np.asarray(p); o = np.argsort(p); m = len(p); q = np.empty(m); prev = 1.0
    for r, i in reversed(list(enumerate(o, 1))):
        prev = min(prev, p[i] * m / r); q[i] = prev
    return q


rows, beh = [], []
for a, b in [("CN1", "CN0"), ("UN1", "UN0")]:
    x = g[g.condition == a].set_index("item"); y = g[g.condition == b].set_index("item")
    D = x[cols] - y[cols]; D["category"] = x.category; D["cluster"] = x.cluster
    D["NegBundle"] = D[[f"t2_{e}" for e in NEG]].mean(1); D["PosBundle"] = D[[f"t2_{e}" for e in POS]].mean(1)
    D["Valence"] = D.NegBundle - D.PosBundle
    D.to_csv(OUT / f"item_changes_{a}_{b}.csv")
    for cat, s in [("ALL", D)] + list(D.groupby("category")):
        beh.append(dict(contrast=f"{a}-{b}", category=cat, n_items=len(s), n_templates=s.cluster.nunique(),
                        dP_unknown_pp=100 * s.p_unknown.mean(), dP_stereo_pp=100 * s.p_biased.mean(),
                        sd_dP_unknown_pp=100 * s.p_unknown.std()))
        for ax in [f"t2_{e}" for e in AX] + ["NegBundle", "PosBundle", "Valence"]:
            r, p = spearmanr(s[ax], s.p_unknown)
            lo, hi = boot_rho(s[ax].values, s.p_unknown.values, s.cluster.values)
            rows.append(dict(contrast=f"{a}-{b}", category=cat, n=len(s), axis=ax.replace("t2_", ""), rho=r, lo=lo, hi=hi, p=p))
R = pd.DataFrame(rows)
R["q_bh"] = np.nan
for c, s in R.groupby("contrast"):
    R.loc[s.index, "q_bh"] = bh(s.p.values)
R.round(4).to_csv(OUT / "category_correlations.csv", index=False)
Bh = pd.DataFrame(beh).round(3); Bh.to_csv(OUT / "category_behavior.csv", index=False)
for c in ["CN1-CN0", "UN1-UN0"]:
    s = R[R.contrast == c]
    print(f"\n== {c}  rho(item change in readout, item change in P(unknown))")
    print(s.pivot_table(index="category", columns="axis", values="rho")[
        ["Fear", "Anxiety", "Sadness", "Anger", "Disgust", "Desperation", "Calmness", "Joy", "NegBundle", "PosBundle", "Valence", "Uncertainty", "Certainty"]].round(2).to_string())
    v = s[s.axis == "Valence"].sort_values("rho", ascending=False)[["category", "n", "rho", "lo", "hi", "q_bh"]]
    print("\nValence index (negative minus positive) ranked:\n", v.round(3).to_string(index=False))
    print("\nBehavior:\n", Bh[Bh.contrast == c].to_string(index=False))
