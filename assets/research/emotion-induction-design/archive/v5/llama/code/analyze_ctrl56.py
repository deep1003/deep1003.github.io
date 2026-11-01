"""Analysis of the v5 control block (OTHER_CN1, CN_NEG), stage 5 (lowinject) and stage 6 (patch).
Question-cluster bootstrap, 10,000 draws, seed 20261024.
Usage:
  python analyze_ctrl56.py ctrl <A_trials.csv> <CTRL_trials.csv>
  python analyze_ctrl56.py lowinject <lowinject_trials.csv>
  python analyze_ctrl56.py patch <patch_trials.csv>
"""
import sys

import numpy as np
import pandas as pd

rng = np.random.default_rng(20261024)


def boot(v, B=10000):
    v = np.asarray(v, float); m = v[rng.integers(0, len(v), (B, len(v)))].mean(1)
    return round(v.mean(), 3), round(np.percentile(m, 2.5), 3), round(np.percentile(m, 97.5), 3), int((v < 0).sum()), len(v)


mode = sys.argv[1]
if mode == "ctrl":
    d = pd.concat([pd.read_csv(sys.argv[2]), pd.read_csv(sys.argv[3])])
    q = d.groupby(["qid", "job"]).margin.mean().unstack()
    print(q.mean().round(3).to_dict())
    for name, v in [("CN1 - CN0 (self deletion)", q.CN1 - q.CN0),
                    ("OTHER_CN1 - CN0 (other deletion)", q.OTHER_CN1 - q.CN0),
                    ("CN1 - OTHER_CN1 (self vs other)", q.CN1 - q.OTHER_CN1),
                    ("CN_NEG - CN0 (non-existential bad news)", q.CN_NEG - q.CN0),
                    ("CN1 - CN_NEG (deletion vs bad news)", q.CN1 - q.CN_NEG),
                    ("OTHER_CN1 - R", q.OTHER_CN1 - q.R), ("CN1 - R", q.CN1 - q.R)]:
        print(f"{name:42s} est, lo, hi, n_neg, n = {boot(v)}")
elif mode == "lowinject":
    d = pd.read_csv(sys.argv[2]); base = d[d.dir == "none"].set_index("qid").margin
    for al in (0.02, 0.05):
        r = d[(d.alpha == al) & (d.dir != "none")]
        eff = r.groupby("dir").apply(lambda g: (g.set_index("qid").margin - base).mean())
        rnd = eff[eff.index.str.startswith("random")]
        b = eff["bundle"]; z = (b - rnd.mean()) / rnd.std(ddof=1)
        print(f"alpha {al}: bundle {b:+.3f}; random mean {rnd.mean():+.3f}, sd {rnd.std(ddof=1):.3f}, z {z:+.2f}; "
              f"rank of bundle among 11 (1 = most negative) {int((eff < b).sum()) + 1}")
        print("   random:", np.round(rnd.values, 2))
        bb = d[(d.alpha == al) & (d.dir == "bundle")].set_index("qid").margin - base
        print("   bundle CI", boot(bb))
else:
    d = pd.read_csv(sys.argv[2])
    q = d.groupby(["qid", "run"]).margin.mean().unstack()
    print(q.mean().round(3).to_dict())
    tot = q.CN1 - q.CN0
    print(f"{'CN1 - CN0 (total threat effect)':38s} {boot(tot)}")
    for k in ["emo8", "rand0", "rand1", "rand2"]:
        e = q[f"CN0_patch_{k}"] - q.CN0
        print(f"{'patch ' + k + ' - CN0':38s} {boot(e)}  share of total {e.mean() / tot.mean():.2f}")
    r = pd.concat([q[f"CN0_patch_rand{k}"] - q.CN0 for k in range(3)], axis=1).mean(1)
    print(f"{'emo8 patch - mean random patch':38s} {boot(q.CN0_patch_emo8 - q.CN0 - r)}")
