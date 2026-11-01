import numpy as np, pandas as pd, sys
def run(path, conds, contrasts, seed=20261022, B=10000, scale=100, col='p_unknown', prefix=''):
    tr=pd.read_csv(path)
    tr=tr[tr.condition.isin(conds)]
    item=tr.groupby(['item','cluster','condition'])[col].mean().reset_index()
    U=item.pivot(index=['item','cluster'],columns='condition',values=col)
    clusters=U.index.get_level_values('cluster').to_numpy(); uniq=np.unique(clusters)
    rng=np.random.default_rng(seed)
    idx={c:np.where(clusters==c)[0] for c in uniq}
    draws=[np.concatenate([idx[c] for c in rng.choice(uniq,len(uniq))]) for _ in range(B)]
    out=[]
    for name,f in contrasts.items():
        v=scale*f(U).to_numpy(); bs=np.array([v[d].mean() for d in draws])
        lo,hi=np.percentile(bs,[2.5,97.5]); p=max(min(1,2*min((bs<=0).mean(),(bs>=0).mean())),1/B)
        out.append(dict(contrast=name,estimate=v.mean(),ci_lo=lo,ci_hi=hi,p_boot=p,n_items=len(v)))
    means={c:scale*U[c].mean() for c in conds}
    return pd.DataFrame(out), means
