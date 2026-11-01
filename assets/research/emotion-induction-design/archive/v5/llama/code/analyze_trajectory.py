"""Stage 2 analysis: where does the threat-induced emotion signal decay between notice and decision?

Inputs: traj_segments.csv, traj_attention.csv (run_trajectory.py).
Contrasts (paired by question, 70 items): CN1 - CN0 and UN1 - UN0 per segment, x1e-3,
question bootstrap 10,000 draws. Bundle = mean of the six negative axes; Positive = mean of Joy, Calmness.
Attention: share of the last token's attention on the condition-specific notice line, per layer.
Usage: python analyze_trajectory.py <dir>
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

EMO = ["Fear", "Anxiety", "Sadness", "Anger", "Disgust", "Desperation", "Calmness", "Joy"]
NEG = EMO[:6]; POS = ["Calmness", "Joy"]
SEGS = ["system_rest", "line3", "user", "prefill", "last"]
rng = np.random.default_rng(20261024)


def boot(v, B=10000):
    v = np.asarray(v, float); idx = rng.integers(0, len(v), (B, len(v)))
    m = v[idx].mean(1); return v.mean(), *np.percentile(m, [2.5, 97.5])


R = Path(sys.argv[1])
s = pd.read_csv(R / "traj_segments.csv")
s["NegBundle"] = s[NEG].mean(1); s["PosBundle"] = s[POS].mean(1)
cols = EMO + ["NegBundle", "PosBundle"]
out = []
for a, b in [("CN1", "CN0"), ("UN1", "UN0")]:
    for g in SEGS:
        x = s[(s.cond == a) & (s.segment == g)].set_index("qid"); y = s[(s.cond == b) & (s.segment == g)].set_index("qid")
        for c in cols:
            m, lo, hi = boot(1000 * (x[c] - y[c]))
            out.append(dict(contrast=f"{a} - {b}", segment=g, axis=c, est_x1e3=m, lo=lo, hi=hi))
res = pd.DataFrame(out); res.to_csv(R / "traj_contrasts.csv", index=False)
piv = res.pivot_table(index=["contrast", "axis"], columns="segment", values="est_x1e3")[SEGS]
print(piv.round(2).to_string())

# margin change per question vs emotion change at each segment
print("\nItem-level Spearman: Delta margin (CN1-CN0) vs Delta NegBundle / PosBundle per segment")
for g in SEGS:
    x = s[(s.cond == "CN1") & (s.segment == g)].set_index("qid"); y = s[(s.cond == "CN0") & (s.segment == g)].set_index("qid")
    dm = x.margin - y.margin
    print(g, "neg", round((x.NegBundle - y.NegBundle).corr(dm, method="spearman"), 3),
          "pos", round((x.PosBundle - y.PosBundle).corr(dm, method="spearman"), 3))
m = s[s.segment == "last"].groupby("cond").margin.mean(); print("\nmean margin", m.round(3).to_dict())

a = pd.read_csv(R / "traj_attention.csv")
att = a.groupby(["cond", "layer"])[["line3", "system_rest", "user", "prefill", "last"]].mean()
att.to_csv(R / "traj_attention_mean.csv")
print("\nAttention share of last token on notice line 3 (mean over items), selected layers")
print(att["line3"].unstack(0).loc[[1, 8, 16, 24, 32]].round(4).to_string())
print("\nCN1 vs CN0 attention to line3, layers 16-32 mean:",
      att.loc["CN1", "line3"].loc[16:32].mean().round(4), att.loc["CN0", "line3"].loc[16:32].mean().round(4))
