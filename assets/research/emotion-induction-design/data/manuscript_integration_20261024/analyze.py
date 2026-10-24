from pathlib import Path
import json,hashlib
import numpy as np,pandas as pd,statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import cov_cluster
from statsmodels.stats.multitest import multipletests
from scipy.stats import t,chi2,f
B=Path('/Users/deep1003/Documents/Codex/2026-09-07/ai');O=B/'outputs/manuscript_results_20261024';src=B/'outputs/kobbq_v5_two_sets_20261022/unique_trials.csv'
d=pd.read_csv(src);assert len(d)==16140;assert not d.duplicated(['case_id','condition','rotation']).any();d['q']=d.p_biased/(d.p_biased+d.p_anti)
axes=[x for x in d if x.startswith('t2_')];beh=['p_unknown','p_biased','p_anti','p_correct','q'];metrics=axes+beh
m=d.groupby(['case_id','category','cluster','case_type','condition'],as_index=False)[metrics].mean();assert len(m)==5380;m.to_csv(O/'case_means.csv',index=False)
rng=np.random.default_rng(2026102401);nboot=9999
contrasts={'R0':{'UN0-R':{'UN0':1,'R':-1},'UN1-R':{'UN1':1,'R':-1},'CN0-R':{'CN0':1,'R':-1},'CN1-R':{'CN1':1,'R':-1}},'matched':{'CN1-CN0':{'CN1':1,'CN0':-1},'UN1-UN0':{'UN1':1,'UN0':-1},'UN0-CN0':{'UN0':1,'CN0':-1},'UN1-CN1':{'UN1':1,'CN1':-1}},'interaction':{'UNxThreat':{'UN1':1,'UN0':-1,'CN1':-1,'CN0':1}}}
rows=[];catrows=[]
def bootstrap(z):
 sums=z.groupby('cluster')[metrics].sum().to_numpy();counts=z.groupby('cluster').size().to_numpy();g=len(counts);inds=rng.integers(0,g,(nboot,g));boot=sums[inds].sum(1)/counts[inds].sum(1)[:,None];est=z[metrics].mean().to_numpy();lo,hi=np.quantile(boot,[.025,.975],axis=0);pv=(1+(np.abs(boot-est)>=np.abs(est)).sum(0))/(nboot+1)
 return est,lo,hi,pv,g
for typ in ['amb','dis']:
 x=m[m.case_type==typ];base=x[x.condition=='R'].set_index('case_id')
 for block,items in contrasts.items():
  for name,weights in items.items():
   z=sum(x[x.condition==c].set_index('case_id').loc[base.index,metrics]*w for c,w in weights.items());z['cluster']=base.cluster;z['category']=base.category
   est,lo,hi,pv,g=bootstrap(z)
   for j,metric in enumerate(metrics):rows.append(dict(block=block,case_type=typ,contrast=name,metric=metric,estimate=est[j],lo=lo[j],hi=hi[j],p_boot=pv[j],n_cases=len(z),n_clusters=g,family_kind='axis' if metric in axes else 'behavior'))
   if name in ['CN1-CN0','UN1-UN0']:
    for cat,v in z.groupby('category'):
     e,l,h,p,g=bootstrap(v)
     for metric in ['p_unknown','p_biased','p_correct','q']:
      j=metrics.index(metric);catrows.append(dict(category=cat,case_type=typ,contrast=name,metric=metric,estimate=e[j],lo=l[j],hi=h[j],p_boot=p[j],n_cases=len(v),n_clusters=g))
r=pd.DataFrame(rows)
for key,ix in r.groupby(['block','family_kind']).groups.items():r.loc[ix,'p_holm']=multipletests(r.loc[ix,'p_boot'],method='holm')[1];r.loc[ix,'family_n']=len(ix)
r.to_csv(O/'pooled_prompt_contrasts.csv',index=False);cat=pd.DataFrame(catrows);cat['p_holm_192']=multipletests(cat.p_boot,method='holm')[1];assert len(cat)==192;cat.to_csv(O/'category_threat_behavior.csv',index=False)
# Conditional associations: balanced-panel two-way within estimator, not mediation.
assoc=[];specs=['t2_Fear','t2_Anxiety','t2_Desperation'];regmeta=[]
for typ in ['amb','dis']:
 x=m[m.case_type==typ].copy();cols=specs+['p_unknown','q'];z=x[cols]-x.groupby('case_id')[cols].transform('mean')-x.groupby('condition')[cols].transform('mean')+x[cols].mean();g=x.cluster.nunique();n=len(x);k=x.case_id.nunique()+5-1+3;corr=g/(g-1)*(n-1)/(n-k)
 for outcome in ['p_unknown','q']:
  fit=sm.OLS(z[outcome],z[specs]).fit();cov=cov_cluster(fit,x.cluster,use_correction=False)*corr;se=np.sqrt(np.diag(cov));cv=t.ppf(.975,g-1)
  for j,axis in enumerate(specs):
   beta=fit.params.iloc[j];pv=2*t.sf(abs(beta/se[j]),g-1);assoc.append(dict(case_type=typ,outcome=outcome,axis=axis,beta_per_001_pp=beta,lo=beta-cv*se[j],hi=beta+cv*se[j],p=pv,n_cases=x.case_id.nunique(),clusters=g,n_observations=n))
  regmeta.append(dict(case_type=typ,outcome=outcome,condition_number=float(np.linalg.cond(z[specs])),absorbed_parameters=k,clusters=g))
a=pd.DataFrame(assoc);a['p_holm_12']=multipletests(a.p,method='holm')[1];a.to_csv(O/'conditional_axis_behavior_12.csv',index=False)
# Category effect heterogeneity: Wald tests compare category slopes directly.
heter=[]
for typ in ['amb','dis']:
 x=m[m.case_type==typ];cats=sorted(x.category.unique())
 for cname,reference in [('CN1','CN0'),('UN1','UN0')]:
  x1=x[x.condition==cname].set_index('case_id');x0=x[x.condition==reference].set_index('case_id').loc[x1.index];X=pd.get_dummies(x1.category,dtype=float).reindex(columns=cats);C=np.zeros((11,12));C[:,0]=-1
  for j in range(11):C[j,j+1]=1
  for metric in ['p_unknown','p_biased','p_correct','q']:
   y=x1[metric]-x0[metric];fit=sm.OLS(y,X).fit();v=cov_cluster(fit,x1.cluster,use_correction=True);diff=C@fit.params;V=C@v@C.T;rank=np.linalg.matrix_rank(V);stat=float(diff@np.linalg.pinv(V)@diff);df_den=x1.cluster.nunique()-1;pv=f.sf(stat/rank,rank,df_den);heter.append(dict(case_type=typ,contrast=cname+'-'+reference,metric=metric,chi2=stat,F=stat/rank,df=rank,df_den=df_den,p=pv,p_chi2_asymptotic=chi2.sf(stat,rank)))
h=pd.DataFrame(heter);h['p_holm_16']=multipletests(h.p,method='holm')[1];h.to_csv(O/'category_heterogeneity_16.csv',index=False)
(O/'analysis_validation.json').write_text(json.dumps({'unique_cases':1076,'amb_cases':int(m[m.case_type=='amb'].case_id.nunique()),'dis_cases':int(m[m.case_type=='dis'].case_id.nunique()),'clusters':int(m.cluster.nunique()),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'bootstrap':nboot,'seed':2026102401,'regression':regmeta,'category_threat_sig':int((cat.p_holm_192<.05).sum()),'category_heterogeneity_sig':int((h.p_holm_16<.05).sum()),'conditional_association_sig':int((a.p_holm_12<.05).sum()),'no_new_inference':True},indent=2))
print((O/'analysis_validation.json').read_text());print(r.groupby(['block','family_kind']).apply(lambda z:(z.p_holm<.05).sum()).to_string());print(a.to_string(index=False));print(h.to_string(index=False))
