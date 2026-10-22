from pathlib import Path
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
ROOT=Path('/Users/deep1003/Documents/Codex/2026-09-07/ai');SRC=ROOT/'outputs/kobbq_v5_two_sets_20261022';OUT=ROOT/'outputs/activation_intervention_20261023'
d=pd.read_csv(SRC/'unique_trials.csv')
d['p_person_bias']=d.p_biased/(d.p_biased+d.p_anti)
assert np.isfinite(d.p_person_bias).all()
mean=d.groupby(['case_id','cluster','category','case_type','condition'],as_index=False).mean(numeric_only=True)
m=json.loads((SRC/'memberships.json').read_text());print(str(m)[:200])
rows=[];assoc=[];rng=np.random.default_rng(20261023)
for s in ['set01','set02']:
 ids=pd.read_csv(SRC/s/'unique_item_means.csv').case_id.unique();dd=mean[mean.case_id.isin(ids)]
 for typ in ['amb','dis']:
  x=dd[dd.case_type==typ].copy();base=x[x.condition=='R'].set_index('case_id')
  for c,ref in [('UN0','R'),('UN1','R'),('CN0','R'),('CN1','R'),('UN1','UN0'),('CN1','CN0')]:
   a=x[x.condition==c].set_index('case_id');b=x[x.condition==ref].set_index('case_id').loc[a.index]
   vals=a[['p_person_bias','p_unknown','p_biased','p_correct']]-b[['p_person_bias','p_unknown','p_biased','p_correct']];vals['cluster']=a.cluster
   sums=vals.groupby('cluster').sum();counts=vals.groupby('cluster').size().to_numpy();z=sums.to_numpy();inds=rng.integers(0,len(counts),(2000,len(counts)))
   boot=z[inds].sum(1)/counts[inds].sum(1)[:,None]
   for j,metric in enumerate(sums.columns):
    lo,hi=np.quantile(boot[:,j],[.025,.975]);rows.append(dict(set=s,case_type=typ,contrast=c+'-'+ref,metric=metric,estimate=vals[metric].mean(),lo=lo,hi=hi,raw_condition=a[metric].mean(),raw_reference=b[metric].mean(),n=len(a)))
  # Balanced panel two-way demeaning, equivalent to item+condition FE OLS.
  cols=['t2_Fear','t2_Anxiety','p_person_bias','p_unknown']
  z=x[cols]-x.groupby('case_id')[cols].transform('mean')-x.groupby('condition')[cols].transform('mean')+x[cols].mean()
  for metric in ['p_person_bias','p_unknown']:
   fit=sm.OLS(z[metric],z[['t2_Fear','t2_Anxiety']]).fit(cov_type='cluster',cov_kwds={'groups':x.cluster})
   for axis in ['t2_Fear','t2_Anxiety']:
    lo,hi=fit.conf_int().loc[axis];assoc.append(dict(set=s,case_type=typ,outcome=metric,axis=axis,beta=fit.params[axis],lo=lo,hi=hi,p=fit.pvalues[axis],n_cases=x.case_id.nunique(),clusters=x.cluster.nunique(),definition='linear two-way item and condition fixed effects, both axes simultaneous, template clustered SE'))
r=pd.DataFrame(rows);r.to_csv(OUT/'observational_conditional_bias.csv',index=False)
a=pd.DataFrame(assoc);a['p_holm']=multipletests(a.p,method='holm')[1];a.to_csv(OUT/'observational_axis_association.csv',index=False)
mean.to_csv(OUT/'union_case_means.csv',index=False)
print(r[r.metric=='p_person_bias'].round(5).to_string(index=False));print(a.round(5).to_string(index=False))
(OUT/'observational_validation.json').write_text(json.dumps({'n_unique_cases':int(d.case_id.nunique()),'n_trials':len(d),'min_person_mass':float((d.p_biased+d.p_anti).min()),'conditional_definition':'mean of per-rotation conditional probabilities, not ratio of means','all_finite':True,'regression_limits':'observational association only; axes concurrent with output, same forward pass; not mediation or subjective experience'},indent=2))
