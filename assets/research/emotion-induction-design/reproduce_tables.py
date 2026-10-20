"""Current master descriptive tables and paired Reference effects from saved data."""
from pathlib import Path
import pandas as pd,numpy as np,json
P=Path(__file__).resolve().parent;D=P/'data';I=pd.read_csv(D/'items_139.csv');B=pd.read_csv(D/'behavior_6_conditions.csv');A=pd.read_csv(D/'axis_cosines_6_conditions.csv');AX=['Fear','Anxiety','Anger','Disgust','Calmness','Sadness','Desperation','Joy','Certainty','Uncertainty'];C=['U0T0','U0T1','U1T0','U1T1','C1T0','C1T1'];means=[];contrasts=[];category=[]
def calc(q,info):
 codes=pd.Categorical(info.cluster).codes;n=codes.max()+1;w=np.random.default_rng(20261018).multinomial(n,np.ones(n)/n,size=10000)[:,codes].astype(float);w/=w.sum(axis=1,keepdims=True)
 def stats(v):
  v=np.asarray(v,float);lo,hi=np.quantile(w@v,[.025,.975]);return dict(estimate=float(v.mean()),median=float(np.median(v)),ci_low=float(lo),ci_high=float(hi))
 out=[dict(kind='mean',term=c,**stats(q[c])) for c in C]
 for label,cols in [('UN',['U1T0','U1T1']),('CN',['C1T0','C1T1'])]:out.append(dict(kind='contrast',term=label+'_vs_Reference',**stats(q[cols].mean(axis=1)-q[['U0T0','U0T1']].mean(axis=1))))
 return out
for metric in ['p_unknown']+AX:
 q=(B.groupby(['item','condition'])[metric].mean().unstack() if metric=='p_unknown' else A[A.axis==metric].groupby(['item','condition']).cosine.mean().unstack()).reindex(index=I.sample_id,columns=C)
 for r in calc(q,I):
  rec=dict(population='all139',items=139,clusters=91,metric=metric,**r);(means if r['kind']=='mean' else contrasts).append(rec)
 for cat,info in I.groupby('category',sort=True):
  for r in calc(q.reindex(info.sample_id),info):category.append(dict(population='all139',category=cat,items=len(info),clusters=info.cluster.nunique(),metric=metric,**r))
pd.DataFrame(means).to_csv(D/'condition_means.csv',index=False);pd.DataFrame(contrasts).to_csv(D/'paired_contrasts.csv',index=False);pd.DataFrame(category).to_csv(D/'category_results.csv',index=False)
m=json.loads((P/'CURRENT_MASTER.json').read_text());(P/'CURRENT_MAIN.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
print('Master tables regenerated; selected139 only; no model inference.')
