"""Descriptive pooled correlations, clustered by source template; no causal identification."""
from pathlib import Path
import numpy as np,pandas as pd
from statsmodels.stats.multitest import multipletests
O=Path(__file__).resolve().parent;m=pd.read_csv(O/'case_means.csv');rng=np.random.default_rng(2026102402);rows=[]
for typ in ['amb','dis']:
 d=m[m.case_type==typ]
 for axis in ['t2_Fear','t2_Anxiety','t2_Desperation']:
  for metric in ['p_unknown','q']:
   z=d[['cluster',axis,metric]].copy();x=z[axis].to_numpy();y=z[metric].to_numpy();z['n']=1;z['x']=x;z['y']=y;z['xx']=x*x;z['yy']=y*y;z['xy']=x*y
   sums=z.groupby('cluster')[['n','x','y','xx','yy','xy']].sum().to_numpy();idx=rng.integers(0,len(sums),(9999,len(sums)));a=sums[idx].sum(1);n,xs,ys,xx,yy,xy=a.T;bs=(xy-xs*ys/n)/np.sqrt((xx-xs*xs/n)*(yy-ys*ys/n));r=np.corrcoef(x,y)[0,1];lo,hi=np.quantile(bs,[.025,.975]);p=(1+(np.abs(bs-r)>=abs(r)).sum())/(len(bs)+1);rows.append(dict(case_type=typ,axis=axis,metric=metric,r=r,lo=lo,hi=hi,p_boot=p,n_cases=d.case_id.nunique(),clusters=len(sums)))
r=pd.DataFrame(rows);r['p_holm_12']=multipletests(r.p_boot,method='holm')[1];r.to_csv(O/'raw_correlations_12.csv',index=False);print(r.to_string(index=False))
