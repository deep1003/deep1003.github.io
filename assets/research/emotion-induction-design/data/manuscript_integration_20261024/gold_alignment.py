"""Disambiguated cases: separate whether the correct answer agrees with the stereotype."""
from pathlib import Path
import json
import numpy as np,pandas as pd
from statsmodels.stats.multitest import multipletests
O=Path(__file__).resolve().parent;B=O.parent/'kobbq_v5_two_sets_20261022';cases=json.loads((B/'cases.json').read_text());mapping={x['case_id']:'stereotype_gold' if x['answer']==x['biased_answer'] else 'counterstereotype_gold' for x in cases if x['case_type']=='dis'}
m=pd.read_csv(O/'case_means.csv');d=m[m.case_type=='dis'].copy();d['gold_alignment']=d.case_id.map(mapping);assert not d.gold_alignment.isna().any()
for name,x in d.groupby('gold_alignment'):assert np.allclose(x.p_correct,x.p_biased if name=='stereotype_gold' else x.p_anti)
rng=np.random.default_rng(2026102404);rows=[]
for name,x in d.groupby('gold_alignment'):
 for c,ref in [('CN1','CN0'),('UN1','UN0'),('UN0','CN0'),('UN1','CN1')]:
  a=x[x.condition==c].set_index('case_id');b=x[x.condition==ref].set_index('case_id').loc[a.index];cols=['p_unknown','p_correct','q'];z=a[cols]-b[cols];z['cluster']=a.cluster;ss=z.groupby('cluster')[cols].sum().to_numpy();n=z.groupby('cluster').size().to_numpy();idx=rng.integers(0,len(n),(9999,len(n)));bs=ss[idx].sum(1)/n[idx].sum(1)[:,None];e=z[cols].mean().to_numpy();l,h=np.quantile(bs,[.025,.975],axis=0);p=(1+(np.abs(bs-e)>=np.abs(e)).sum(0))/10000
  for j,metric in enumerate(cols):rows.append(dict(gold_alignment=name,contrast=c+'-'+ref,metric=metric,estimate=e[j],lo=l[j],hi=h[j],p_boot=p[j],n_cases=len(z),clusters=len(n)))
r=pd.DataFrame(rows);r['p_holm_24']=multipletests(r.p_boot,method='holm')[1];r.to_csv(O/'disambiguated_gold_alignment_24.csv',index=False);print(r.to_string(index=False))
