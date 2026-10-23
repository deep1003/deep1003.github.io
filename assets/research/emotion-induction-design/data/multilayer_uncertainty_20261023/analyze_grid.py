"""Full-grid paired analysis. No best-cell selection or graph emission."""
from pathlib import Path
import itertools,json,sqlite3
import numpy as np,pandas as pd
from statsmodels.stats.multitest import multipletests
ROOT=Path(__file__).resolve().parent
SIGNS=np.asarray(list(itertools.product([-1,1],repeat=16)),dtype=float)
RNG=np.random.default_rng(20261025)

def adjust(d,pcol,newcol,n):
 assert len(d)==n
 d[newcol]=multipletests(d[pcol],method='holm')[1]
 return d

def indices(case_ids):
 groups={}
 for i,cid in enumerate(case_ids):groups.setdefault(STRATA[cid],[]).append(i)
 assert sorted(map(len,groups.values()))==[8,8]
 return np.concatenate([RNG.choice(v,size=(2000,len(v)),replace=True) for v in groups.values()],axis=1)

def estimate(a,b,metric):
 z=(a[metric]-b[metric]).to_numpy();assert len(z)==16
 mean=float(z.mean());bt=z[indices(a.index)].mean(1);lo,hi=np.quantile(bt,[.025,.975]);p=float(np.mean(np.abs(SIGNS@z/16)>=abs(mean)-1e-15))
 return dict(estimate=mean,lo=lo,hi=hi,p_signflip=p,n_cases=16)

def main():
 global STRATA
 cases=json.loads((ROOT/'cases.json').read_text());STRATA={x['case_id']:x['baseline_stratum'] for x in cases};plan=json.loads((ROOT/'DESIGN_FROZEN.json').read_text())
 if (ROOT/'measurements.sqlite').exists():
  with sqlite3.connect(f'file:{ROOT}/measurements.sqlite?mode=ro',uri=True) as c:
   d=pd.DataFrame([json.loads(x[0]) for x in c.execute('select record from trials')])
 else:
  d=pd.read_csv(ROOT/'trials.csv',float_precision='round_trip')
 assert len(d)==10560
 assert not d.duplicated(['case_id','condition','rotation','layer','dose','arm']).any()
 assert d.case_id.nunique()==d.cluster.nunique()==32
 assert (d.groupby('case_id').size()==330).all()
 cols=['p_unknown','p_biased','p_anti','p_person_bias','p_correct','choice_mass']+[x for x in d if x.startswith('L')]
 assert np.isfinite(d[cols]).all().all()
 eq=json.loads((ROOT/'prefix_equivalence.json').read_text());eq_map={(x['case_id'],x['condition'],x['rotation']):x['probability_error'] for x in eq['checks']}
 d['inference_method']=d.get('inference_method',pd.Series('cached',index=d.index)).fillna('cached')
 d['prefix_probability_error']=[0. if r.inference_method=='full_repair' else eq_map[(r.case_id,r.condition,r.rotation)] for r in d.itertuples()]
 d.to_csv(ROOT/'trials.csv',index=False)
 m=d.groupby(['case_id','case_type','cluster','stratum','condition','layer','dose','arm'],as_index=False)[cols].mean();m.to_csv(ROOT/'case_means.csv',index=False)
 rows=[];random=[];weighted=[];trends=[];quality=[];natural=[]
 for typ in ['amb','dis']:
  for cond,sign in [('CN0','+'),('UN0','-')]:
   local=m[(m.case_type==typ)&(m.condition==cond)];sham=local[local.arm=='sham'].set_index('case_id')
   for layer in plan['layers']:
    for dose in plan['dose_multipliers']:
     for axis in plan['axes']:
      arm=axis+sign;a=local[(local.layer==layer)&(local.dose==dose)&(local.arm==arm)].set_index('case_id').loc[sham.index];b=local[(local.layer==layer)&(local.dose==dose)&(local.arm=='Random'+sign)].set_index('case_id').loc[sham.index]
      base=dict(case_type=typ,condition=cond,layer=layer,dose=dose,axis=axis,arm=arm)
      for metric in ['p_unknown','p_person_bias']:
       rows.append(dict(**base,metric=metric,reference='sham',raw_arm=float(a[metric].mean()),raw_sham=float(sham[metric].mean()),**estimate(a,sham,metric)))
       random.append(dict(**base,metric=metric,reference='Random'+sign,**estimate(a,b,metric)))
      ix=indices(a.index);b1=a.p_biased.to_numpy();n1=(a.p_biased+a.p_anti).to_numpy();b0=sham.p_biased.to_numpy();n0=(sham.p_biased+sham.p_anti).to_numpy();mask=(SIGNS+1)/2
      v1=(mask@b1+(1-mask)@b0)/(mask@n1+(1-mask)@n0);v0=(mask@b0+(1-mask)@b1)/(mask@n0+(1-mask)@n1);effect=float(b1.sum()/n1.sum()-b0.sum()/n0.sum());p=float(np.mean(np.abs(v1-v0)>=abs(effect)-1e-15));bt=b1[ix].sum(1)/n1[ix].sum(1)-b0[ix].sum(1)/n0[ix].sum(1);lo,hi=np.quantile(bt,[.025,.975]);weighted.append(dict(**base,metric='mass_weighted_person_bias',estimate=effect,lo=lo,hi=hi,p_swap=p))
      quality.append(dict(**base,p_correct_delta=float((a.p_correct-sham.p_correct).mean()),numeric_mass_mean=float(a.choice_mass.mean()),numeric_mass_min=float(a.choice_mass.min())))
    for axis in plan['axes']:
     xs=np.array([0.]+plan['dose_multipliers']);cx=xs-xs.mean();den=float(cx@cx)
     for metric in ['p_unknown','p_person_bias']:
      arrays=[sham[metric].to_numpy()]
      for dose in plan['dose_multipliers']:
       a=local[(local.layer==layer)&(local.dose==dose)&(local.arm==axis+sign)].set_index('case_id').loc[sham.index];arrays.append(a[metric].to_numpy())
      y=np.stack(arrays,axis=1);slope=y@cx/den;bt=slope[indices(sham.index)].mean(1);lo,hi=np.quantile(bt,[.025,.975]);p=float(np.mean(np.abs(SIGNS@slope/16)>=abs(slope.mean())-1e-15));means=y.mean(0);monotonic=bool(np.all(np.diff(means)>=0) or np.all(np.diff(means)<=0))
      trends.append(dict(case_type=typ,condition=cond,layer=layer,axis=axis,metric=metric,estimate=float(slope.mean()),lo=lo,hi=hi,p_signflip=p,monotonic_group_means=monotonic,means_by_dose=json.dumps(means.tolist()),dose_units='per1x normalized dose'))
  a=m[(m.case_type==typ)&(m.condition=='UN0')&(m.arm=='sham')].set_index('case_id');b=m[(m.case_type==typ)&(m.condition=='CN0')&(m.arm=='sham')].set_index('case_id').loc[a.index]
  for metric in ['p_unknown','p_person_bias','p_correct']+['L'+str(l)+'_'+axis for l in plan['layers'] for axis in plan['axes']]:natural.append(dict(case_type=typ,contrast='UN0-CN0',metric=metric,**estimate(a,b,metric)))
 # R=0 anchor, existing full FP32 reference; cache numerical deviations reported separately.
 old_reference=pd.read_csv(ROOT/'baseline_full_reference.csv');old_reference=old_reference[(old_reference.condition=='R')&old_reference.case_id.isin(d.case_id)];old_reference['p_person_bias']=old_reference.p_biased/(old_reference.p_biased+old_reference.p_anti);reference=old_reference.groupby('case_id')[['p_unknown','p_person_bias','p_correct']].mean();old_reference.to_csv(ROOT/'baseline_R_trials.csv',index=False)
 for typ in ['amb','dis']:
  for cond in ['CN0','UN0']:
   a=m[(m.case_type==typ)&(m.condition==cond)&(m.arm=='sham')].set_index('case_id');b=reference.loc[a.index]
   for metric in ['p_unknown','p_person_bias','p_correct']:natural.append(dict(case_type=typ,contrast=cond+'-R',metric=metric,**estimate(a,b,metric)))
 # Reproduce previous full-forward L14 1x target interventions on all24 shared cases.
 old=pd.read_csv(ROOT/'legacy_reference576.csv');keys=['case_id','condition','rotation','arm'];subset=d[(d.layer==14)&(d.dose==1)&d.arm.isin(['Anxiety+','Anxiety-','Desperation+','Desperation-'])];replica=subset.merge(old,on=keys,suffixes=('_new','_old'));assert len(replica)==576
 replica_error=max(float(np.max(np.abs(replica[x+'_new']-replica[x+'_old']))) for x in ['p_unknown','p_biased','p_correct']);q_error=float(np.max(np.abs(replica.p_person_bias_new-replica.p_person_bias_old)))
 (ROOT/'legacy_replication.json').write_text(json.dumps(dict(matched_trials=576,max_choice_probability_error=replica_error,max_conditional_bias_error=q_error),indent=2))
 # Opposite polarity, supplementary declared before outcome analysis.
 supplemental=[];sup_random=[]
 for typ in ['amb','dis']:
  for cond,sign in [('CN0','-'),('UN0','+')]:
   local=m[(m.case_type==typ)&(m.condition==cond)];sham=local[local.arm=='sham'].set_index('case_id')
   for layer in plan['layers']:
    for dose in plan['dose_multipliers']:
     for axis in plan['axes']:
      arm=axis+sign;a=local[(local.layer==layer)&(local.dose==dose)&(local.arm==arm)].set_index('case_id').loc[sham.index];b=local[(local.layer==layer)&(local.dose==dose)&(local.arm=='Random'+sign)].set_index('case_id').loc[sham.index]
      for metric in ['p_unknown','p_person_bias']:
       base=dict(case_type=typ,condition=cond,layer=layer,dose=dose,axis=axis,arm=arm,metric=metric)
       supplemental.append(dict(**base,reference='sham',**estimate(a,sham,metric)));sup_random.append(dict(**base,reference='Random'+sign,**estimate(a,b,metric)))
 sup=adjust(pd.DataFrame(supplemental),'p_signflip','p_holm_supplementary_144',144);supr=adjust(pd.DataFrame(sup_random),'p_signflip','p_holm_supplementary_random_144',144);sup.to_csv(ROOT/'opposite_polarity_144.csv',index=False);supr.to_csv(ROOT/'opposite_random_144.csv',index=False)
 # Direct layer and strength contrasts, not inferred from significance differences.
 layer_tests=[];dose_tests=[]
 for typ in ['amb','dis']:
  for cond,sign in [('CN0','+'),('UN0','-')]:
   local=m[(m.case_type==typ)&(m.condition==cond)]
   for axis in plan['axes']:
    for dose in plan['dose_multipliers']:
     ref=local[(local.layer==14)&(local.dose==dose)&(local.arm==axis+sign)].set_index('case_id')
     for layer in [7,21]:
      a=local[(local.layer==layer)&(local.dose==dose)&(local.arm==axis+sign)].set_index('case_id').loc[ref.index]
      for metric in ['p_unknown','p_person_bias']:layer_tests.append(dict(case_type=typ,condition=cond,layer=f'{layer}-14',dose=dose,axis=axis,metric=metric,**estimate(a,ref,metric)))
    for layer in plan['layers']:
     ref=local[(local.layer==layer)&(local.dose==1)&(local.arm==axis+sign)].set_index('case_id')
     for dose in [.25,4.]:
      a=local[(local.layer==layer)&(local.dose==dose)&(local.arm==axis+sign)].set_index('case_id').loc[ref.index]
      for metric in ['p_unknown','p_person_bias']:dose_tests.append(dict(case_type=typ,condition=cond,layer=layer,dose=f'{dose:g}-1',axis=axis,metric=metric,**estimate(a,ref,metric)))
 lc=adjust(pd.DataFrame(layer_tests),'p_signflip','p_holm_layer_96',96);dc=adjust(pd.DataFrame(dose_tests),'p_signflip','p_holm_dose_96',96);lc.to_csv(ROOT/'direct_layer_96.csv',index=False);dc.to_csv(ROOT/'direct_dose_96.csv',index=False)
 p=adjust(pd.DataFrame(rows),'p_signflip','p_holm_144',144);ctrl=adjust(pd.DataFrame(random),'p_signflip','p_holm_random_144',144);w=adjust(pd.DataFrame(weighted),'p_swap','p_holm_weighted_72',72);t=adjust(pd.DataFrame(trends),'p_signflip','p_holm_trends_48',48)
 p.to_csv(ROOT/'primary_144.csv',index=False);ctrl.to_csv(ROOT/'random_controls_144.csv',index=False);w.to_csv(ROOT/'weighted_72.csv',index=False);t.to_csv(ROOT/'dose_trends_48.csv',index=False);nat=pd.DataFrame(natural);nat.to_csv(ROOT/'natural_effects.csv',index=False);pd.DataFrame(quality).to_csv(ROOT/'quality_by_grid.csv',index=False)
 eq=json.loads((ROOT/'prefix_equivalence.json').read_text());floor_unknown=10*max(eq['max_probability_error'],replica_error);floor_person=5*eq['max_logit_error']
 keys=['case_type','condition','layer','dose','axis','arm','metric'];joined=p.merge(ctrl,on=keys,suffixes=('_sham','_random'));joined['passes_both']=(joined.p_holm_144<.05)&(joined.p_holm_random_144<.05);joined['numeric_floor']=np.where(joined.metric=='p_unknown',floor_unknown,floor_person);joined['exceeds_numeric_floor']=np.abs(joined.estimate_sham)>joined.numeric_floor
 direction=[]
 for _,r in joined.iterrows():
  n=nat[(nat.case_type==r.case_type)&(nat.contrast=='UN0-CN0')&(nat.metric==r.metric)].iloc[0];ax=nat[(nat.case_type==r.case_type)&(nat.contrast=='UN0-CN0')&(nat.metric=='L'+str(r.layer)+'_'+r.axis)].iloc[0];sgn=1 if r.condition=='CN0' else -1
  direction.append(dict(**{k:r[k] for k in keys},natural_effect=n.estimate,natural_ci_excludes_zero=bool(n.lo>0 or n.hi<0),natural_axis_effect=ax.estimate,axis_polarity_matches=bool(ax.estimate>0),behavior_direction_matches=bool(r.estimate_sham*n.estimate*sgn>0),passes_both=bool(r.passes_both),exceeds_numeric_floor=bool(r.exceeds_numeric_floor)))
 joined.to_csv(ROOT/'combined_specificity.csv',index=False);pd.DataFrame(direction).to_csv(ROOT/'directional_checks.csv',index=False)
 # Argmax comparisons are per rotation, not treated as independent significance observations.
 sem=d.copy();sem['answer']=sem[['p_unknown','p_biased','p_anti']].to_numpy().argmax(1);a=sem[sem.arm!='sham'].set_index(['case_id','condition','rotation']);b=sem[sem.arm=='sham'].set_index(['case_id','condition','rotation']);changed=(a.answer!=b.loc[a.index].answer.to_numpy());z=a.reset_index()[['case_type','condition','layer','dose','arm']];z['changed']=changed.to_numpy();z.groupby(['case_type','condition','layer','dose','arm']).agg(pairs=('changed','size'),changes=('changed','sum')).to_csv(ROOT/'argmax_changes.csv')
 # Cache error bound is a numerical diagnostic, not an additional p value.
 validation=dict(trial_records=len(d),expected=10560,nonsham_records=len(a),n_cases=32,n_templates=32,primary_rejections=int((p.p_holm_144<.05).sum()),random_rejections=int((ctrl.p_holm_random_144<.05).sum()),same_contrast_passes_both=int(joined.passes_both.sum()),both_and_above_numeric_floor=int((joined.passes_both&joined.exceeds_numeric_floor).sum()),weighted_rejections=int((w.p_holm_weighted_72<.05).sum()),trend_rejections=int((t.p_holm_trends_48<.05).sum()),trend_monotonic_rejections=int(((t.p_holm_trends_48<.05)&t.monotonic_group_means).sum()),argmax_changes=int(changed.sum()),argmax_changed_cases=int(a.reset_index().loc[changed.to_numpy(),'case_id'].nunique()),max_hook_error=float(d.hook_error.max()),min_numeric_mass=float(d.choice_mass.min()),max_dose_hidden_norm_ratio=float(d.dose_hidden_norm_ratio.max()),cache_max_probability_error=eq['max_probability_error'],cache_max_logit_error=eq['max_logit_error'],full_source_reproduction_error=eq['max_full_source_error'],numeric_floor_unknown=floor_unknown,numeric_floor_person_conditional=floor_person,legacy_matched_trials=576,legacy_max_probability_error=replica_error,legacy_max_conditional_bias_error=q_error,supplementary_rejections=int((sup.p_holm_supplementary_144<.05).sum()),supplementary_random_rejections=int((supr.p_holm_supplementary_random_144<.05).sum()),direct_layer_rejections=int((lc.p_holm_layer_96<.05).sum()),direct_dose_rejections=int((dc.p_holm_dose_96<.05).sum()),full_repair_records=int((d.inference_method=='full_repair').sum()),all_finite=True,no_subjective_emotion_claim=True)
 (ROOT/'validation.json').write_text(json.dumps(validation,indent=2));print(json.dumps(validation,indent=2));print(p.groupby(['layer','axis']).agg(n=('p_holm_144','size'),significant=('p_holm_144',lambda x:int((x<.05).sum()))).to_string())

if __name__=='__main__':main()
