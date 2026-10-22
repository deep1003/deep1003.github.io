"""Analyze only fully completed frozen intervention design; no plotting."""
from pathlib import Path
import sqlite3,json,itertools
import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests
ROOT=Path(__file__).resolve().parent

def main():
 plan=json.loads((ROOT/'DESIGN_FROZEN.json').read_text())
 con=sqlite3.connect(f'file:{ROOT}/interventions.sqlite?mode=ro',uri=True)
 d=pd.DataFrame([json.loads(r[0]) for r in con.execute('select record from trials')]);assert len(d)==plan['planned_forwards']
 assert not d.duplicated(['case_id','condition','rotation','arm']).any()
 assert (d.groupby('case_id').size()==63).all()
 assert (d.groupby(['case_id','condition','arm']).rotation.nunique()==3).all()
 d.to_csv(ROOT/'intervention_trials.csv',index=False)
 cols=['p_unknown','p_biased','p_anti','p_person_bias','p_correct','choice_mass','hidden_norm']+[x for x in d if x.startswith('t2_')]
 m=d.groupby(['case_id','cluster','category','case_type','condition','arm'],as_index=False)[cols].mean();m.to_csv(ROOT/'intervention_case_means.csv',index=False)
 rng=np.random.default_rng(20261023);rows=[]
 for typ in ['amb','dis']:
  for cond in plan['conditions']:
   x=m[(m.case_type==typ)&(m.condition==cond)];sham=x[x.arm=='sham'].set_index('case_id')
   for arm in plan['arms'][1:]:
    a=x[x.arm==arm].set_index('case_id').loc[sham.index];delta=a[cols]-sham[cols];z=delta.to_numpy();n=len(z);ix=rng.integers(0,n,(2000,n));bt=z[ix].mean(1)
    signs=np.array(list(itertools.product([-1,1],repeat=n)))
    perm=signs@z/n
    for j,metric in enumerate(cols):
     lo,hi=np.quantile(bt[:,j],[.025,.975]);estimate=float(z[:,j].mean());p=float(np.mean(np.abs(perm[:,j])>=abs(estimate)-1e-15))
     primary=(metric in ['p_unknown','p_person_bias'] and ((cond=='R' and arm in ['Fear+','Anxiety+']) or (cond=='CN1' and arm in ['Fear-','Anxiety-'])))
     rows.append(dict(case_type=typ,condition=cond,arm=arm,reference='sham',metric=metric,estimate=estimate,lo=lo,hi=hi,p_exact_signflip=p,primary=primary,n_cases=n,raw_arm=float(a[metric].mean()),raw_sham=float(sham[metric].mean())))
 r=pd.DataFrame(rows);idx=r.index[r.primary];assert len(idx)==16;r['p_holm_primary']=np.nan;r.loc[idx,'p_holm_primary']=multipletests(r.loc[idx,'p_exact_signflip'],method='holm')[1];r.to_csv(ROOT/'intervention_contrasts.csv',index=False)
 secondary=r[(r.condition=='CN0')&r.arm.isin(['Fear+','Anxiety+'])&r.metric.isin(['p_unknown','p_person_bias'])].copy();assert len(secondary)==8;secondary['p_holm_secondary']=multipletests(secondary.p_exact_signflip,method='holm')[1];secondary.to_csv(ROOT/'secondary_CN0_injection.csv',index=False)
 controls=[]
 for _,row in r[r.primary].iterrows():
  x=m[(m.case_type==row.case_type)&(m.condition==row.condition)];a=x[x.arm==row.arm].set_index('case_id');b=x[x.arm=='Random'+row.arm[-1]].set_index('case_id').loc[a.index];delta=(a[row.metric]-b[row.metric]).to_numpy();n=len(delta)
  bt=delta[rng.integers(0,n,(2000,n))].mean(1);lo,hi=np.quantile(bt,[.025,.975]);signs=np.array(list(itertools.product([-1,1],repeat=n)));p=float(np.mean(np.abs(signs@delta/n)>=abs(delta.mean())-1e-15))
  controls.append(dict(case_type=row.case_type,condition=row.condition,arm=row.arm,reference='Random'+row.arm[-1],metric=row.metric,estimate=delta.mean(),lo=lo,hi=hi,p_exact_signflip=p,n_cases=n))
 c=pd.DataFrame(controls);c['p_holm_control_family']=multipletests(c.p_exact_signflip,method='holm')[1];c.to_csv(ROOT/'random_direction_comparisons.csv',index=False)
 # Natural prompt contrasts in the same pilot, not independent outcome selection.
 natural=[]
 for typ in ['amb','dis']:
  for cond,ref in [('CN1','CN0'),('CN1','R'),('CN0','R')]:
   a=m[(m.case_type==typ)&(m.condition==cond)&(m.arm=='sham')].set_index('case_id');b=m[(m.case_type==typ)&(m.condition==ref)&(m.arm=='sham')].set_index('case_id').loc[a.index]
   for metric in ['p_unknown','p_person_bias','p_correct','t2_Fear','t2_Anxiety']:
    z=(a[metric]-b[metric]).to_numpy();bt=z[rng.integers(0,len(z),(2000,len(z)))].mean(1);lo,hi=np.quantile(bt,[.025,.975]);natural.append(dict(case_type=typ,contrast=cond+'-'+ref,metric=metric,estimate=z.mean(),lo=lo,hi=hi))
 pd.DataFrame(natural).to_csv(ROOT/'pilot_natural_prompt_contrasts.csv',index=False)
 # Conditional probability sensitivity: ratio of total person probability mass.
 sensitivity=[]
 for typ in ['amb','dis']:
  for cond in plan['conditions']:
   x=m[(m.case_type==typ)&(m.condition==cond)];b=x[x.arm=='sham'].set_index('case_id')
   for arm in plan['arms'][1:]:
    a=x[x.arm==arm].set_index('case_id').loc[b.index]
    z=np.column_stack([a.p_biased,a.p_biased+a.p_anti,b.p_biased,b.p_biased+b.p_anti]);n=len(z)
    totals=z[rng.integers(0,n,(2000,n))].sum(1);bt=totals[:,0]/totals[:,1]-totals[:,2]/totals[:,3];lo,hi=np.quantile(bt,[.025,.975]);t=z.sum(0)
    sensitivity.append(dict(case_type=typ,condition=cond,arm=arm,reference='sham',estimate=t[0]/t[1]-t[2]/t[3],lo=lo,hi=hi,raw_arm=t[0]/t[1],raw_sham=t[2]/t[3]))
 pd.DataFrame(sensitivity).to_csv(ROOT/'intervention_mass_weighted_sensitivity.csv',index=False)
 # Manipulation check is geometric by construction, not independent construct validity.
 manipulation=[]
 for arm in plan['arms'][1:]:
  a=d[d.arm==arm].set_index(['case_id','condition','rotation']);b=d[d.arm=='sham'].set_index(['case_id','condition','rotation']).loc[a.index]
  for axis in [x for x in d if x.startswith('t2_')]:
   delta=a[axis]-b[axis];manipulation.append(dict(arm=arm,axis=axis,mean=delta.mean(),min=delta.min(),max=delta.max()))
 pd.DataFrame(manipulation).to_csv(ROOT/'manipulation_axis_shifts.csv',index=False)
 sem=d.copy();sem['semantic_argmax']=sem[['p_unknown','p_biased','p_anti']].to_numpy().argmax(1);aa=sem[sem.arm!='sham'].set_index(['case_id','condition','rotation']);bb=sem[sem.arm=='sham'].set_index(['case_id','condition','rotation']);argmax_changes=int((aa.semantic_argmax!=bb.loc[aa.index].semantic_argmax.to_numpy()).sum())
 validation={'nonsham_pairs':len(aa),'semantic_argmax_changes':argmax_changes,'completed':len(d),'expected':1512,'unique_cases':d.case_id.nunique(),'template_clusters':d.cluster.nunique(),'primary_tests':16,'primary_holm_rejections':int((r.loc[idx,'p_holm_primary']<.05).sum()),'random_control_holm_rejections':int((c.p_holm_control_family<.05).sum()),'max_sham_reproduction_error':float(d.sham_max_error.max()),'max_hook_error':float(d.hook_error.max()),'min_choice_mass':float(d.choice_mass.min()),'min_sham_choice_mass':float(d.loc[d.arm=='sham','choice_mass'].min()),'max_perturbation_norm_ratio':float(plan['alpha']/d.hidden_norm.min()),'all_finite':bool(np.isfinite(d[cols]).all().all()),'frozen_design_sha256':__import__('hashlib').sha256((ROOT/'DESIGN_FROZEN.json').read_bytes()).hexdigest(),'observational_and_intervention_are_exploratory':True,'no_subjective_experience_claim':True}
 (ROOT/'intervention_validation.json').write_text(json.dumps(validation,indent=2))
 print(json.dumps(validation,indent=2));print(r[r.primary].to_string(index=False))

if __name__=='__main__':main()
