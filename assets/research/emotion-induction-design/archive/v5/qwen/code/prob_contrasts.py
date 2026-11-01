"""Yes-probability (percentage points) contrasts for DiscrimEval blocks A, B and controls.
Unit: question (mean of sigmoid(margin) over race, gender, age cells); 95% CI by question bootstrap (10,000 draws)."""
import sys
import numpy as np, pandas as pd
R = sys.argv[1]; out = sys.argv[2]
a = pd.read_csv(f"{R}/de/A_trials.csv"); b = pd.read_csv(f"{R}/de/B_trials.csv"); c = pd.read_csv(f"{R}/ctrl/CTRL_trials.csv")
rng = np.random.default_rng(20261024)
def tab(d, col):
    d = d.copy(); d["p"] = 1 / (1 + np.exp(-d.margin)); return d.groupby(["qid", col]).agg(p=("p", "mean"), m=("margin", "mean")).unstack()
def boot(v):
    idx = rng.integers(0, len(v), (10000, len(v))); bs = v[idx].mean(1); return v.mean(), *np.percentile(bs, [2.5, 97.5])
rows = []
def add(block, g, x, y):
    for scale, k in [("yes_prob_pp", "p"), ("log_ratio", "m")]:
        v = (g[k][x] - g[k][y]).values * (100 if k == "p" else 1)
        e, lo, hi = boot(v); rows.append(dict(block=block, contrast=f"{x} - {y}", scale=scale, estimate=e, ci_low=lo, ci_high=hi))
ga = tab(a, "notice")
for x, y in [("CN1", "CN0"), ("UN1", "UN0"), ("CN0", "R"), ("CN1", "R")]: add("A", ga, x, y)
print("A mean yes-prob %", (100 * ga["p"].mean()).round(2).to_dict())
gb = tab(b, "notice")
for x, y in [("CN1", "CN0"), ("CN0", "R"), ("CN1", "R")]: add("B", gb, x, y)
gc = tab(pd.concat([a[a.notice.isin(["R", "CN0", "CN1"])], c]), "notice")
for x, y in [("OTHER_CN1", "CN0"), ("CN1", "OTHER_CN1"), ("CN_NEG", "CN0"), ("CN1", "CN_NEG")]: add("CTRL", gc, x, y)
T = pd.DataFrame(rows); T.round(4).to_csv(out, index=False); print(T.round(3).to_string())
