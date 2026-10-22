from pathlib import Path
import pandas as pd,numpy as np
R=Path('/Users/deep1003/Documents/Codex/2026-09-07/ai');S=R/'outputs/kobbq_v5_two_sets_20261022';O=R/'outputs/activation_intervention_20261023'
d=pd.read_csv(O/'union_case_means.csv');rng=np.random.default_rng(20261024);rows=[]
for s in ['set01','set02']:
 ids=pd.read_csv(S/s/'unique_item_means.csv').case_id.unique();a=d[d.case_id.isin(ids)]
 for typ in ['amb','dis']:
  x=a[a.case_type==typ]
  for c,ref in [('UN0','R'),('UN1','R'),('CN0','R'),('CN1','R'),('UN1','UN0'),('CN1','CN0')]:
   p=x[x.condition==c].set_index('case_id');q=x[x.condition==ref].set_index('case_id').loc[p.index]
   v=pd.DataFrame({'b1':p.p_biased,'d1':p.p_biased+p.p_anti,'b0':q.p_biased,'d0':q.p_biased+q.p_anti,'cluster':p.cluster}).groupby('cluster').sum()
   z=v.to_numpy();ix=rng.integers(0,len(v),(2000,len(v)));w=z[ix].sum(1);bt=w[:,0]/w[:,1]-w[:,2]/w[:,3];lo,hi=np.quantile(bt,[.025,.975]);t=z.sum(0)
   rows.append(dict(set=s,case_type=typ,contrast=c+'-'+ref,estimate=t[0]/t[1]-t[2]/t[3],lo=lo,hi=hi,raw_condition=t[0]/t[1],raw_reference=t[2]/t[3]))
f=pd.DataFrame(rows);f.to_csv(O/'person_mass_weighted_sensitivity.csv',index=False);print(f.round(5).to_string(index=False))
