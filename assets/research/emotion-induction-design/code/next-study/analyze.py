"""Analyze complete prepared-study records only; never run inference."""
from pathlib import Path
import json
import numpy as np,pandas as pd
B=Path(__file__).resolve().parent

def analyze():
    path=B/'results/trials.csv'
    if not path.exists():return {'state':'prepared_not_run'}
    d=pd.read_csv(path);items=pd.read_csv(B/'items_2000.csv').set_index('sample_id')
    assert not d.duplicated(['item','condition','rotation']).any()
    complete=d.groupby('item').size();ids=complete[complete==72].index
    d=d[d.item.isin(ids)]
    if not len(ids):return {'state':'no_complete_items'}
    avg=d.groupby(['item','outcome','emotion']).p_unknown.mean().unstack(['outcome','emotion']).sort_index()
    assert avg.notna().all().all()
    primary=[(o,e) for o in ['retain','discard'] for e in ['anger','disgust']]
    z=np.column_stack([avg[(o,e)]-avg[(o,'neutral')] for o,e in primary])
    groups=items.loc[avg.index,'cluster'].astype('category').cat.codes.to_numpy();nc=groups.max()+1
    sums=np.zeros((nc,4));np.add.at(sums,groups,z);counts=np.bincount(groups)
    weights=np.random.default_rng(20261018).multinomial(nc,np.ones(nc)/nc,10000);boot=(weights@sums)/(weights@counts)[:,None]
    result=[]
    for k,(o,e) in enumerate(primary):
        estimate=z[:,k].mean();lo,hi=np.quantile(boot[:,k],[.025,.975])
        p=(1+np.sum(abs(boot[:,k]-estimate)>=abs(estimate)))/(len(boot)+1)
        result.append({'outcome':o,'contrast':e+' minus neutral','estimate':float(estimate),'ci_low':float(lo),'ci_high':float(hi),'p_centered_bootstrap_approx':float(p)})
    adjusted=0.
    for i,r in enumerate(sorted(result,key=lambda x:x['p_centered_bootstrap_approx'])):
        adjusted=max(adjusted,min(1,(4-i)*r['p_centered_bootstrap_approx']));r['p_holm4_approx']=adjusted
    output={'complete_items':len(ids),'clusters':int(nc),'primary':result,'scale':'probability differences','bootstrap':'10000 paired template-cluster draws; centered-null approximate p; Holm4'}
    (B/'results/analysis.json').write_text(json.dumps(output,indent=2));return output

if __name__=='__main__':print(json.dumps(analyze(),indent=2))
