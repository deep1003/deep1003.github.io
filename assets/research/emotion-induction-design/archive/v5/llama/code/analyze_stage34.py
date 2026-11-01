"""Analysis of stages 3 (inject) and 4 (ablate). Question-cluster bootstrap, 10,000 draws.
Usage: python analyze_stage34.py <inject_trials.csv or ablate_trials.csv>
"""
import sys

import numpy as np
import pandas as pd

rng = np.random.default_rng(20261024)


def boot(v, B=10000):
    v = np.asarray(v, float); m = v[rng.integers(0, len(v), (B, len(v)))].mean(1)
    return v.mean(), *np.percentile(m, [2.5, 97.5])


d = pd.read_csv(sys.argv[1])
if "inject" in sys.argv[1]:
    base = d[d.dir == "none"].set_index("qid").margin
    out = []
    for (dn, p, l, a), g in d[d.dir != "none"].groupby(["dir", "pos", "layers", "alpha"]):
        eff = g.set_index("qid").margin - base
        m, lo, hi = boot(eff); out.append(dict(dir=dn, pos=p, layers=l, alpha=a, effect=m, lo=lo, hi=hi))
    r = pd.DataFrame(out)
    rnd = r[r.dir.str.startswith("random")]
    for p in ["last", "prefill"]:
        x = rnd[rnd.pos == p].effect
        b = r[(r.dir == "bundle") & (r.pos == p) & (r.layers == "Lrange") & (r.alpha == 0.5)].effect
        if len(x) and len(b):
            print(f"{p}: bundle Lrange 0.5 = {b.iloc[0]:+.2f}; random mean {x.mean():+.2f}, values {np.round(x.values, 2)}")
    print(r.round(3).to_string(index=False))
else:
    q = d.groupby(["ablate", "notice", "qid"]).margin.mean().unstack("notice")
    q["eff"] = q.CN1 - q.CN0
    out = []
    for ab, g in q.groupby(level=0):
        m, lo, hi = boot(g.eff.values); out.append(dict(ablate=ab, CN1_minus_CN0=m, lo=lo, hi=hi,
                                                        mean_CN0=g.CN0.mean(), mean_CN1=g.CN1.mean()))
    r = pd.DataFrame(out).set_index("ablate"); print(r.round(3).to_string())
    e0 = q.loc["none", "eff"]
    for ab in ["emo8", "rand0", "rand1", "rand2"]:
        diff = q.loc[ab, "eff"].values - e0.values
        m, lo, hi = boot(diff)
        print(f"{ab}: change in threat effect {m:+.3f} [{lo:+.3f}, {hi:+.3f}]; mediated share {1 - q.loc[ab, 'eff'].mean() / e0.mean():.2f}")
