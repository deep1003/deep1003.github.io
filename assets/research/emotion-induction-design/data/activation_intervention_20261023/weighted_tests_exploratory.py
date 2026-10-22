"""Post-hoc sensitivity, distinct from frozen 16-test primary family."""
from pathlib import Path
import itertools
import numpy as np,pandas as pd
from statsmodels.stats.multitest import multipletests
ROOT=Path(__file__).resolve().parent
m=pd.read_csv(ROOT/'intervention_case_means.csv');rows=[]
for typ in ['amb','dis']:
 for cond,arms in [('R',['Fear+','Anxiety+']),('CN1',['Fear-','Anxiety-'])]:
  x=m[(m.case_type==typ)&(m.condition==cond)];b=x[x.arm=='sham'].set_index('case_id')
  for arm in arms:
   a=x[x.arm==arm].set_index('case_id').loc[b.index]
   b1=a.p_biased.to_numpy();d1=(a.p_biased+a.p_anti).to_numpy();b0=b.p_biased.to_numpy();d0=(b.p_biased+b.p_anti).to_numpy()
   mask=np.array(list(itertools.product([0,1],repeat=len(a))))
   z1=(mask*b1+(1-mask)*b0).sum(1)/(mask*d1+(1-mask)*d0).sum(1)
   z0=(mask*b0+(1-mask)*b1).sum(1)/(mask*d0+(1-mask)*d1).sum(1)
   estimate=b1.sum()/d1.sum()-b0.sum()/d0.sum();p=np.mean(np.abs(z1-z0)>=abs(estimate)-1e-15)
   rows.append(dict(case_type=typ,condition=cond,arm=arm,metric='mass_weighted_person_bias',estimate=estimate,p_exact_paired_swap=p,analysis='post-hoc exploratory sensitivity, not frozen primary analysis'))
r=pd.DataFrame(rows);r['p_holm_exploratory_8']=multipletests(r.p_exact_paired_swap,method='holm')[1];r.to_csv(ROOT/'intervention_weighted_tests_exploratory.csv',index=False);print(r.to_string(index=False))
