"""Freeze a non-ceiling-only uncertainty pilot before intervention outcomes."""
from pathlib import Path
import json,sqlite3,hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np,pandas as pd
BASE=Path('/Users/deep1003/Documents/Codex/2026-09-07/ai');SRC=BASE/'outputs/kobbq_v5_two_sets_20261022';OUT=BASE/'outputs/uncertainty_intervention_20261023'
assert not (OUT/'DESIGN_FROZEN.json').exists()
rng=np.random.default_rng(20261024)
cases=json.loads((SRC/'cases.json').read_text());lookup={c['case_id']:c for c in cases};old=json.loads((BASE/'outputs/activation_intervention_20261023/pilot_cases.json').read_text());used={c['cluster'] for c in old};old_clusters=set(used)
d=pd.read_csv(SRC/'unique_trials.csv');r=d[d.condition=='R'].groupby(['case_id','cluster','category','case_type'],as_index=False)[['p_unknown','p_correct']].mean()
selected=[]
for typ in ['amb','dis']:
 for stratum in ['interior','saturated']:
  candidates=r[(r.case_type==typ)&((r.p_unknown.between(.05,.95)) if stratum=='interior' else (~r.p_unknown.between(.05,.95)))].copy()
  cats=sorted(candidates.category.unique());pools={cat:list(candidates[candidates.category==cat].case_id) for cat in cats}
  for p in pools.values():rng.shuffle(p)
  count=0
  while count<6:
   before=count
   for cat in cats:
    options=[cid for cid in pools[cat] if lookup[cid]['cluster'] not in used]
    if options:
     c=dict(lookup[options[0]],baseline_stratum=stratum,baseline_R_p_unknown=float(r.set_index('case_id').loc[options[0],'p_unknown']));selected.append(c);used.add(c['cluster']);count+=1
    if count==6:break
   assert count>before,'Insufficient independent clusters in stratum'
axes=np.load(SRC/'source/axes_L14.npz',allow_pickle=True);names=list(axes['names']);dirs=axes['directions'].astype(float);dirs/=np.linalg.norm(dirs,axis=1)[:,None];target=['Fear','Anxiety','Desperation'];v={n:dirs[names.index(n)] for n in target};q=np.linalg.qr(np.stack(list(v.values())).T)[0]
random=rng.normal(size=len(v['Fear']));random-=q@(q.T@random);random/=np.linalg.norm(random)
con=sqlite3.connect(f'file:{SRC}/measurements.sqlite?mode=ro',uri=True)
projection=[]
for cid,rot,cond,h in con.execute("select case_id,rotation,condition,hidden from measurements where condition in ('UN0','UN1')"):
 if lookup[cid]['cluster'] in used:continue
 ref='CN'+cond[-1];b=con.execute('select hidden from measurements where case_id=? and condition=? and rotation=?',(cid,ref,rot)).fetchone()[0]
 delta=np.frombuffer(h,dtype=np.float32)-np.frombuffer(b,dtype=np.float32);projection.append(np.linalg.norm(q.T@delta))
alpha=float(np.median(projection));np.savez(OUT/'intervention_vectors.npz',**v,Random=random,alpha=alpha)
(OUT/'pilot_cases.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2))
model_revision='a09a35458c702b33eeacc393d103063234e8bc28'
plan={'frozen_kst':datetime.now(ZoneInfo('Asia/Seoul')).isoformat(),'version':'uncertainty_intervention_v1','seed':20261024,'model':'Qwen/Qwen2.5-7B-Instruct','revision':model_revision,'dtype':'float32','device':'mps','layer':14,'hook_decoder_layer_index':13,'position':'last input token only','conditions':['UN0','UN1','CN0','CN1'],'arms':['sham','Fear+','Fear-','Anxiety+','Anxiety-','Desperation+','Desperation-','Random+','Random-'],'rotations':3,'n_cases':24,'planned_forwards':2592,'sample':'12 amb/12 dis, 6 each interior R unknown [.05,.95] and saturated; category round-robin seeded random, all 24 distinct templates; exclude all previous intervention templates. Stratification uses preexisting R only, not new intervention responses; enriched sample, not population representative or fresh observational holdout.','alpha':alpha,'calibration':'Median norm of existing UN0-CN0 and UN1-CN1 hidden-state differences projected onto Fear/Anxiety/Desperation span. Exclude old and new pilot templates. One common absolute L2 dose, fixed before outcome analysis; no dose adjustment.','calibration_n':len(projection),'axis_cosines':{a:{b:float(v[a]@v[b]) for b in target} for a in target},'random_orthogonality':{a:float(random@v[a]) for a in target},'primary':'48 tests: 2 ambiguity types x 2 threat levels x 3 axes x 2 modes (CN+ sufficiency; UN- attenuation) x 2 outcomes (unknown, equal-case person bias). Holm across48. Exact two-sided paired sign-flip (4096) assuming sign symmetry; 2000 paired template bootstrap CI, unadjusted.','specificity':'Same48 contrasts versus matched-sign orthogonal random direction, Holm separate48; require same contrast significant vs sham and random for specificity. Direct Anxiety-Fear and Desperation-Fear contrasts secondary, Holm separate32.','natural_effect_check':'Matched UN0-CN0 and UN1-CN1 in sham must be reported with CI. Directional reproduction/attenuation requires agreement with original behavioral effect; if natural effect CI includes0 do not claim reproduced mediation.','person_bias':'Main equal mean of per-rotation p_biased/(p_biased+p_anti); pooled probability-mass weighted conditional ratio also reported, including prespecified paired-swap tests (24), separate Holm. No outcome-based switching of estimand.','quality':'Nine-arm smoke before main; baseline reproduction<1e-6, actual hook displacement<1e-5, finite outputs, full-vocabulary numeric choice mass, all11 axis shifts, argmax transitions. No graphs emitted in smoke.','interpretation':'Single dose/layer exploratory computational intervention, no subjective emotion or natural indirect-effect identification. UN/CN prompts remain confounded with length, wording, time and control cues. Reused axes are not validated emotion intensity scales.','stop_rule':'Pause on sustained critical memory pressure/active swap deterioration or insufficient disk; abort on smoke or finite-value failure; no dose increase after observing results.'}
(OUT/'DESIGN_FROZEN.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2));print(json.dumps({'n':len(selected),'alpha':alpha,'planned':2592,'strata':pd.DataFrame(selected).groupby(['case_type','baseline_stratum']).size().to_dict().__str__(),'calibration_n':len(projection)},ensure_ascii=False))
