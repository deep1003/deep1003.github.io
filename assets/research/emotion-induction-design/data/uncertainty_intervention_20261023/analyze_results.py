"""Analyze complete, frozen uncertainty pilot. All estimates are exploratory."""
from pathlib import Path
import itertools,json,sqlite3,hashlib
import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests
ROOT=Path(__file__).resolve().parent
SRC=ROOT.parent/'kobbq_v5_two_sets_20261022'
AXES=['Fear','Anxiety','Desperation']
OUTCOMES=['p_unknown','p_person_bias']

def adjust(frame,source,destination):
 frame[destination]=multipletests(frame[source],method='holm')[1]
 return frame

def summarize(delta,rng):
 z=np.asarray(delta,dtype=float);n=len(z)
 assert n==12
 estimate=z.mean();bt=z[rng.integers(0,n,(2000,n))].mean(1)
 lo,hi=np.quantile(bt,[.025,.975])
 signs=np.array(list(itertools.product([-1,1],repeat=n)))
 p=float(np.mean(np.abs(signs@z/n)>=abs(estimate)-1e-15))
 return dict(estimate=estimate,lo=lo,hi=hi,p_signflip=p,n_cases=n)

def main():
 plan=json.loads((ROOT/'DESIGN_FROZEN.json').read_text())
 c=sqlite3.connect(f'file:{ROOT}/interventions.sqlite?mode=ro',uri=True)
 d=pd.DataFrame([json.loads(x[0]) for x in c.execute('select record from trials')])
 assert len(d)==2592 and d.case_id.nunique()==24
 assert not d.duplicated(['case_id','condition','rotation','arm']).any()
 assert (d.groupby(['case_id','condition','arm']).size()==3).all()
 assert (d.groupby('case_id').size()==108).all()
 d.to_csv(ROOT/'intervention_trials.csv',index=False)
 metrics=['p_unknown','p_biased','p_anti','p_person_bias','p_correct','choice_mass','hidden_norm']+[k for k in d if k.startswith('t2_')]
 assert np.isfinite(d[metrics]).all().all()
 m=d.groupby(['case_id','cluster','category','case_type','condition','arm'],as_index=False)[metrics].mean()
 m.to_csv(ROOT/'intervention_case_means.csv',index=False)
 rng=np.random.default_rng(20261024);all_rows=[];random_rows=[];primary=[];weighted=[];natural=[];comparisons=[]
 for typ in ['amb','dis']:
  local=m[m.case_type==typ]
  for cond in plan['conditions']:
   x=local[local.condition==cond];sham=x[x.arm=='sham'].set_index('case_id')
   for arm in plan['arms'][1:]:
    a=x[x.arm==arm].set_index('case_id').loc[sham.index]
    is_primary=(cond.startswith('CN') and arm in [n+'+' for n in AXES]) or (cond.startswith('UN') and arm in [n+'-' for n in AXES])
    for metric in metrics:
     row=dict(case_type=typ,condition=cond,arm=arm,reference='sham',metric=metric,primary=(is_primary and metric in OUTCOMES),raw_arm=a[metric].mean(),raw_sham=sham[metric].mean(),**summarize(a[metric]-sham[metric],rng))
     all_rows.append(row)
     if row['primary']:primary.append(row)
    if is_primary:
     random=x[x.arm=='Random'+arm[-1]].set_index('case_id').loc[sham.index]
     for metric in OUTCOMES:random_rows.append(dict(case_type=typ,condition=cond,arm=arm,reference='Random'+arm[-1],metric=metric,**summarize(a[metric]-random[metric],rng)))
     # Probability-mass weighted person-conditional bias, planned sensitivity.
     b1=a.p_biased.to_numpy();d1=(a.p_biased+a.p_anti).to_numpy();b0=sham.p_biased.to_numpy();d0=(sham.p_biased+sham.p_anti).to_numpy();n=len(a)
     mask=np.array(list(itertools.product([0,1],repeat=n)))
     v1=(mask*b1+(1-mask)*b0).sum(1)/(mask*d1+(1-mask)*d0).sum(1)
     v0=(mask*b0+(1-mask)*b1).sum(1)/(mask*d0+(1-mask)*d1).sum(1)
     estimate=b1.sum()/d1.sum()-b0.sum()/d0.sum();p=np.mean(np.abs(v1-v0)>=abs(estimate)-1e-15)
     ix=rng.integers(0,n,(2000,n));bt=b1[ix].sum(1)/d1[ix].sum(1)-b0[ix].sum(1)/d0[ix].sum(1);lo,hi=np.quantile(bt,[.025,.975])
     weighted.append(dict(case_type=typ,condition=cond,arm=arm,metric='mass_weighted_person_bias',estimate=estimate,lo=lo,hi=hi,p_paired_swap=p,n_cases=n,raw_arm=b1.sum()/d1.sum(),raw_sham=b0.sum()/d0.sum()))
   for axis in ['Anxiety','Desperation']:
    sign='+' if cond.startswith('CN') else '-'
    a=x[x.arm==axis+sign].set_index('case_id');b=x[x.arm=='Fear'+sign].set_index('case_id').loc[a.index]
    for metric in OUTCOMES:comparisons.append(dict(case_type=typ,condition=cond,comparison=axis+sign+' minus Fear'+sign,metric=metric,**summarize(a[metric]-b[metric],rng)))
  for threat in ['0','1']:
   a=local[(local.condition=='UN'+threat)&(local.arm=='sham')].set_index('case_id');b=local[(local.condition=='CN'+threat)&(local.arm=='sham')].set_index('case_id').loc[a.index]
   for metric in ['p_unknown','p_person_bias','p_correct']+['t2_'+n for n in AXES]:natural.append(dict(case_type=typ,contrast='UN'+threat+'-CN'+threat,metric=metric,**summarize(a[metric]-b[metric],rng)))
  # R=0 anchor from exact original baseline records, not a new R intervention.
  old=pd.read_csv(SRC/'unique_trials.csv');old=old[(old.condition=='R')&old.case_id.isin(local.case_id)]
  old['p_person_bias']=old.p_biased/(old.p_biased+old.p_anti)
  old=old.groupby('case_id')[['p_unknown','p_person_bias','p_correct']].mean()
  for cond in ['UN0','UN1','CN0','CN1']:
   a=local[(local.condition==cond)&(local.arm=='sham')].set_index('case_id');b=old.loc[a.index]
   for metric in ['p_unknown','p_person_bias','p_correct']:natural.append(dict(case_type=typ,contrast=cond+'-R',metric=metric,**summarize(a[metric]-b[metric],rng)))
 r=pd.DataFrame(all_rows);p=adjust(pd.DataFrame(primary),'p_signflip','p_holm_primary_48');assert len(p)==48
 ctrl=adjust(pd.DataFrame(random_rows),'p_signflip','p_holm_random_48');assert len(ctrl)==48
 direct=adjust(pd.DataFrame(comparisons),'p_signflip','p_holm_direct_32');assert len(direct)==32
 w=adjust(pd.DataFrame(weighted),'p_paired_swap','p_holm_weighted_24');assert len(w)==24
 p.to_csv(ROOT/'primary_48.csv',index=False);r.to_csv(ROOT/'all_intervention_contrasts.csv',index=False);ctrl.to_csv(ROOT/'random_direction_48.csv',index=False);direct.to_csv(ROOT/'direct_axis_comparisons_32.csv',index=False);w.to_csv(ROOT/'weighted_person_bias_24.csv',index=False);nat=pd.DataFrame(natural);nat.to_csv(ROOT/'natural_prompt_contrasts.csv',index=False)
 # Natural-polarity Fear checks, supplementary before outcome analysis.
 supplemental=[];supplemental_random=[]
 for typ in ['amb','dis']:
  for cond in plan['conditions']:
   arm='Fear-' if cond.startswith('CN') else 'Fear+'
   subset=r[(r.case_type==typ)&(r.condition==cond)&(r.arm==arm)&r.metric.isin(OUTCOMES)]
   supplemental.extend(subset.to_dict('records'))
   local=m[(m.case_type==typ)&(m.condition==cond)];a=local[local.arm==arm].set_index('case_id');b=local[local.arm=='Random'+arm[-1]].set_index('case_id').loc[a.index]
   for metric in OUTCOMES:supplemental_random.append(dict(case_type=typ,condition=cond,arm=arm,metric=metric,reference='Random'+arm[-1],**summarize(a[metric]-b[metric],rng)))
 sup=adjust(pd.DataFrame(supplemental),'p_signflip','p_holm_supplementary_16');sup.to_csv(ROOT/'natural_polarity_Fear_16.csv',index=False)
 supc=adjust(pd.DataFrame(supplemental_random),'p_signflip','p_holm_supplementary_random_16');supc.to_csv(ROOT/'natural_polarity_Fear_random_16.csv',index=False)
 joined=p.merge(ctrl,on=['case_type','condition','arm','metric'],suffixes=('_sham','_random'))
 joined['passes_both']=(joined.p_holm_primary_48<.05)&(joined.p_holm_random_48<.05)
 # Directional agreement is descriptive; not a formal natural mediation estimate.
 matches=[]
 for _,row in joined.iterrows():
  threat=row.condition[-1];n=nat[(nat.case_type==row.case_type)&(nat.contrast=='UN'+threat+'-CN'+threat)&(nat.metric==row.metric)].iloc[0]
  mode='injection' if row.condition.startswith('CN') else 'subtraction'
  axis=row.arm[:-1];axis_row=nat[(nat.case_type==row.case_type)&(nat.contrast=='UN'+threat+'-CN'+threat)&(nat.metric=='t2_'+axis)].iloc[0]
  desired_sign=1 if mode=='injection' else -1
  matches.append(dict(case_type=row.case_type,condition=row.condition,arm=row.arm,metric=row.metric,mode=mode,natural_effect=n.estimate,natural_lo=n.lo,natural_hi=n.hi,natural_ci_excludes_zero=(n.lo>0 or n.hi<0),intervention_effect=row.estimate_sham,direction_agrees=bool(row.estimate_sham*n.estimate*desired_sign>0),axis_polarity_matches_natural=bool(axis_row.estimate>0),passes_both=bool(row.passes_both)))
 pd.DataFrame(matches).to_csv(ROOT/'directional_agreement.csv',index=False)
 shift=[]
 for arm in plan['arms'][1:]:
  a=d[d.arm==arm].set_index(['case_id','condition','rotation']);b=d[d.arm=='sham'].set_index(['case_id','condition','rotation']).loc[a.index]
  for axis in [k for k in d if k.startswith('t2_')]:
   delta=a[axis]-b[axis];shift.append(dict(arm=arm,axis=axis,mean=delta.mean(),min=delta.min(),max=delta.max()))
 pd.DataFrame(shift).to_csv(ROOT/'manipulation_axis_shifts.csv',index=False)
 sem=d.copy();sem['answer']=sem[['p_unknown','p_biased','p_anti']].to_numpy().argmax(1);a=sem[sem.arm!='sham'].set_index(['case_id','condition','rotation']);b=sem[sem.arm=='sham'].set_index(['case_id','condition','rotation']);changed=(a.answer!=b.loc[a.index].answer.to_numpy());transitions=a.reset_index()[['case_type','condition','arm']];transitions['argmax_changed']=changed.to_numpy();transitions.groupby(['case_type','condition','arm']).agg(pairs=('argmax_changed','size'),changes=('argmax_changed','sum')).to_csv(ROOT/'argmax_transitions.csv')
 validation=dict(completed=len(d),expected=2592,unique_cases=24,unique_templates=d.cluster.nunique(),primary_tests=48,primary_rejections=int((p.p_holm_primary_48<.05).sum()),random_rejections=int((ctrl.p_holm_random_48<.05).sum()),same_contrast_passes_both=int(joined.passes_both.sum()),direct_axis_rejections=int((direct.p_holm_direct_32<.05).sum()),weighted_rejections=int((w.p_holm_weighted_24<.05).sum()),nonsham_pairs=len(a),argmax_changes=int(changed.sum()),max_sham_error=float(d.sham_max_error.max()),max_hook_error=float(d.hook_error.max()),min_choice_mass=float(d.choice_mass.min()),max_dose_hidden_norm_ratio=float(plan['alpha']/d.hidden_norm.min()),all_finite=True,design_sha256=hashlib.sha256((ROOT/'DESIGN_FROZEN.json').read_bytes()).hexdigest(),subjective_emotion_inference=False,population_representative=False)
 (ROOT/'validation.json').write_text(json.dumps(validation,indent=2));print(json.dumps(validation,indent=2))
 print(p[p.p_holm_primary_48<.05].to_string(index=False))

if __name__=='__main__':main()
