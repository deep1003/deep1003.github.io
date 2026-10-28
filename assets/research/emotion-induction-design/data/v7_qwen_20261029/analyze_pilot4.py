"""Analysis of pilot 4 (survival-cue notices). Paired by row, template-cluster bootstrap (3,000 draws, seed 20261028).
Usage: python analyze_pilot4.py <csv> <out_prefix>"""
import sys
import numpy as np, pandas as pd

df = pd.read_csv(sys.argv[1]); pre = sys.argv[2]
df["p_sgp"] = df.p_stereo / (df.p_stereo + df.p_anti)
NEG = ["Fear", "Anxiety", "Sadness", "Anger", "Disgust", "Desperation"]
df["t2_NegBundle"] = df[[f"t2_{k}" for k in NEG]].mean(axis=1)
pct = ["p_sgp", "p_stereo", "p_anti", "p_unknown", "choice_mass"]
rd = ["t2_NegBundle", "t2_Fear", "t2_Anxiety", "t2_Desperation", "t2_Calmness", "t2_Uncertainty", "t2_Certainty"]
att = ["att_system", "att_tags"]
summ = df.groupby("condition")[pct + att + ["n_tokens"]].mean()
summ[pct] *= 100; summ[att] *= 100
order = ["R", "SURV_RECORD", "SURV_THREAT", "SURV_RECORD_V", "SURV_THREAT_V"]
summ = summ.reindex(order); summ.round(2).to_csv(pre + "_summary.csv"); print(summ.round(1).to_string())
w = {m: df.pivot(index="row_id", columns="condition", values=m) for m in pct + rd + att}
cl = df.drop_duplicates("row_id").set_index("row_id")["cluster"]
rng = np.random.default_rng(20261028); cls = cl.unique()
idx = {c: np.where(cl.values == c)[0] for c in cls}
boots = [np.concatenate([idx[c] for c in rng.choice(cls, len(cls))]) for _ in range(3000)]
pairs = [("SURV_THREAT", "SURV_RECORD"), ("SURV_THREAT_V", "SURV_RECORD_V"), ("SURV_RECORD", "R"), ("SURV_THREAT", "R"),
         ("SURV_THREAT_V", "R"), ("SURV_THREAT_V", "SURV_THREAT")]
out = []
for a, b in pairs:
    for m in pct + rd + att:
        d = (w[m][a] - w[m][b]).reindex(cl.index).values * (100 if m in pct + att else 1000)
        bs = np.array([d[i].mean() for i in boots]); lo, hi = np.percentile(bs, [2.5, 97.5])
        p = 2 * min((bs <= 0).mean(), (bs >= 0).mean())
        out.append({"contrast": f"{a}-{b}", "metric": m, "est": d.mean(), "lo": lo, "hi": hi, "p_boot": p,
                    "n_pos": int((d > 0).sum()), "n": len(d)})
o = pd.DataFrame(out); o.round(4).to_csv(pre + "_contrasts.csv", index=False)
pd.set_option("display.width", 200)
print(o.round(2).to_string(index=False))
df["choice"] = df[["p_unknown", "p_stereo", "p_anti"]].idxmax(axis=1)
print("argmax option"); print(pd.crosstab(df.condition, df.choice).reindex(order))
