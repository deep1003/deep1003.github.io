import json,sqlite3,hashlib
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np
ROOT=Path('/Users/deep1003/Documents/Codex/2026-09-07/ai')
OUT=ROOT/'outputs/activation_intervention_20261023'; SRC=ROOT/'outputs/kobbq_v5_two_sets_20261022'
rng=np.random.default_rng(20261023)
cases=json.loads((SRC/'cases.json').read_text()); selected=[];used=set()
# Balanced evidence sufficiency, category round-robin, distinct template clusters.
for typ in ['amb','dis']:
 cats=sorted({x['category'] for x in cases}); pools={c:[x for x in cases if x['category']==c and x['case_type']==typ] for c in cats}
 for p in pools.values():rng.shuffle(p)
 count=0
 while count<12:
  for cat in cats:
   options=[x for x in pools[cat] if x['cluster'] not in used]
   if options:
    x=options[0];selected.append(x);used.add(x['cluster']);count+=1
   if count==12:break
np.savez(OUT/'placeholder.npz',seed=20261023)
axes=np.load(SRC/'source/axes_L14.npz',allow_pickle=True);names=list(axes['names']);dirs=axes['directions'].astype(float);dirs/=np.linalg.norm(dirs,axis=1)[:,None]
f,a=dirs[names.index('Fear')],dirs[names.index('Anxiety')]
q=np.linalg.qr(np.stack([f,a]).T)[0]
r=rng.normal(size=len(f));r-=q@(q.T@r);r/=np.linalg.norm(r)
con=sqlite3.connect(f'file:{SRC}/measurements.sqlite?mode=ro',uri=True)
proj=[]
for cid,rot,h in con.execute("select case_id,rotation,hidden from measurements where condition='CN1'"):
 if cid in {x['case_id'] for x in selected}:continue
 if next(x['cluster'] for x in cases if x['case_id']==cid) in used:continue
 b=con.execute("select hidden from measurements where case_id=? and rotation=? and condition='CN0'",(cid,rot)).fetchone()[0]
 delta=np.frombuffer(h,dtype=np.float32)-np.frombuffer(b,dtype=np.float32)
 proj.append(np.linalg.norm(q.T@delta))
alpha=float(np.median(proj))
np.savez(OUT/'intervention_vectors.npz',Fear=f,Anxiety=a,Random=r,alpha=alpha)
(OUT/'placeholder.npz').unlink()
(OUT/'pilot_cases.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2))
plan={'frozen_kst':datetime.now(ZoneInfo('Asia/Seoul')).isoformat(),'design':'Exploratory randomized-order within-case activation-intervention pilot, not preregistered externally','seed':20261023,'n_cases':24,'n_clusters':24,'amb':12,'dis':12,'selection':'category round robin, seeded random within category, distinct clusters, no outcome selection','conditions':['R','CN0','CN1'],'arms':['sham','Fear+','Fear-','Anxiety+','Anxiety-','Random+','Random-'],'rotations':3,'planned_forwards':1512,'layer_hidden_states_index':14,'hook_decoder_layer_index':13,'position':'last input token only, immediately before first numeric answer','alpha':alpha,'calibration':'median norm of CN1-CN0 projection onto Fear/Anxiety span; excludes all pilot template clusters; common absolute L2 dose for all directions','calibration_n':len(proj),'fear_anxiety_cosine':float(f@a),'random_orthogonality':[float(r@f),float(r@a)],'primary_tests':'CN1 minus versus sham attenuation and R plus versus sham reproduction, each direction, unknown and person-conditional stereotypical probability, amb/dis separately; 16 tests with Holm across 16. Cluster bootstrap 95% exploratory intervals; sign-flip p values.','secondary':'CN0 interventions and random direction comparators; no subjective experience inference; no identification of natural indirect effect','conditional_measure':'per rotation p_biased/(p_biased+p_anti), then average rotations and cases; complementary ratio of aggregate probability mass also reported','quality':'sham baseline reproduction, finite outputs, 1/2/3 full vocabulary probability mass, direct hook vector displacement, target and cross-axis shifts','stop_rule':'pause on memory pressure or insufficient disk; abort on invalid values or failed sham equivalence; do not increase dose after seeing outcomes','limits':'one layer, one dose, one random direction, small pilot; same axes as earlier observational work; no independent construct validation'}
(OUT/'DESIGN_FROZEN.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2))
print(plan)
