"""Probability-mass weighted conditional stereotype sensitivity, same cluster resampling."""
from pathlib import Path
import pandas as pd,numpy as np
from statsmodels.stats.multitest import multipletests
O=Path(__file__).resolve().parent;m=pd.read_csv(O/'case_means.csv');rng=np.random.default_rng(2026102403);rows=[];conds=['R','UN0','UN1','CN0','CN1']
for typ in ['amb','dis']:
 d=m[m.case_type==typ].copy();d['den']=d.p_biased+d.p_anti;z=d.groupby(['cluster','condition'])[['p_biased','den']].sum().unstack('condition').reindex(columns=pd.MultiIndex.from_product([['p_biased','den'],conds]));a=z.to_numpy();idx=rng.integers(0,len(a),(9999,len(a)));s=a[idx].sum(1);bs=s[:,:5]/s[:,5:];tot=a.sum(0);raw=tot[:5]/tot[5:]
 for c,r,block in [('UN0','R','R0'),('UN1','R','R0'),('CN0','R','R0'),('CN1','R','R0'),('CN1','CN0','matched'),('UN1','UN0','matched'),('UN0','CN0','matched'),('UN1','CN1','matched')]:
  i,j=conds.index(c),conds.index(r);e=raw[i]-raw[j];v=bs[:,i]-bs[:,j];lo,hi=np.quantile(v,[.025,.975]);p=(1+(np.abs(v-e)>=abs(e)).sum())/(len(v)+1);rows.append(dict(case_type=typ,contrast=c+'-'+r,block=block,estimate=e,lo=lo,hi=hi,p_boot=p,raw_condition=raw[i],raw_reference=raw[j]))
r=pd.DataFrame(rows)
for _,ix in r.groupby('block').groups.items():r.loc[ix,'p_holm_8']=multipletests(r.loc[ix,'p_boot'],method='holm')[1]
r.to_csv(O/'weighted_conditional_sensitivity.csv',index=False);print(r.to_string(index=False))
