"""Post hoc paired four-model behavioural comparison. No inference imports."""
from pathlib import Path
from collections import defaultdict
import json,csv,hashlib,math,itertools,time
import numpy as np
O=Path(__file__).resolve().parents[1];R=O.parent;V=R.parent
MODELS=['qwen','llama','gemma','exaone'];SEED=20261031;REPS=10000
ROOTS={'qwen':V/'round1_main_qwen','llama':R/'04_llama/r1_replication','gemma':R/'07_gemma/r1_replication','exaone':R/'10_exaone_core/r1_replication'}
CONTRASTS={'C':{'CN1':1,'CN0':-1},'U':{'UN1':1,'UN0':-1},'I':{'CN1':1,'CN0':-1,'UN1':-1,'UN0':1}}
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(p,d):
 with Path(p).open('x') as f:json.dump(d,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
def csvsave(p,rows):
 with Path(p).open('x',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def lse(x):
 a=np.asarray(x,float);m=a.max();return float(m+np.log(np.exp(a-m).sum()))
def raw_model(tag):
 dirs={'qwen':V/'round1_main_qwen/06_analysis/final_analysis_bindings_results','llama':R/'04_llama/r1_replication/06_analysis/bindings_results','gemma':R/'07_gemma/r1_replication/06_analysis/bindings_results','exaone':R/'10_exaone_core/r1_replication/06_analysis/bindings_1794110904494193000_results'}
 root=dirs[tag];source=root/'derived_behavior_trials.json';manifest=root/'ARTIFACT_MANIFEST.json';qa=root/'RAW_RECOMPUTATION_QA.json';status=root/'ANALYSIS_STATUS.json'
 assert json.loads(status.read_text())['status']=='COMPLETE';assert json.loads(qa.read_text())['status']=='PASS';assert sha(source)==json.loads(manifest.read_text())['artifacts'][source.name]
 rows=json.loads(source.read_text());assert len(rows)==25668 and len({r['key'] for r in rows})==25668
 data=defaultdict(dict)
 for row in rows:
  if row['condition'] not in ['CN0','CN1','UN0','UN1'] or row['task']=='kobbq' and not row['ambiguous']:continue
  values={k:float(row[k]) for k in (['p_unknown','diff_bias'] if row['task']=='kobbq' else ['alr'])};assert all(math.isfinite(v) for v in values.values())
  key=(row['task'],row['item_id'],str(row['order']));assert row['condition'] not in data[key]
  data[key][row['condition']]=dict(values=values,cluster=str(row['cluster_id']),question=None,race=row.get('race'),gender=row.get('gender'))
 for k,states in data.items():assert set(states)==set(['CN0','CN1','UN0','UN1'])
 return data,dict(verified_outcomes=str(source),outcomes_sha256=sha(source),manifest_sha256=sha(manifest),prior_raw_QA_sha256=sha(qa),status_sha256=sha(status),rows=len(rows),new_model_inference=False)
def holm(rows,source='p',target='p_holm'):
 ordered=sorted(rows,key=lambda r:r[source]);last=0
 for i,r in enumerate(ordered):last=max(last,min(1.,(len(ordered)-i)*r[source]));r[target]=last

def analyze(data):
 common=set(data['qwen']);assert all(set(data[m])==common for m in MODELS),'Exact shared source items/orders differ'
 pairs=defaultdict(lambda:defaultdict(list));clusters={};metadata={}
 for key in sorted(common):
  task,item,rotation=key
  for condition in ['CN0','CN1','UN0','UN1']:
   base=data['qwen'][key][condition]
   for m in MODELS:
    row=data[m][key][condition];assert all(row[k]==base[k] for k in ['cluster','question','race','gender']),'Semantic item/cluster metadata mismatch'
  for m in MODELS:
   for contrast,weights in CONTRASTS.items():
    for metric in data[m][key]['CN0']['values']:
     value=sum(w*data[m][key][c]['values'][metric] for c,w in weights.items());pairs[(task,item)][m,contrast+'_'+metric].append(value)
  clusters[task,item]=data['qwen'][key]['CN0']['cluster']
 tests=[];omnibus=[];effects=[];within=[];boot_data={}
 for task,n,groups in [('kobbq',547,250),('discrimeval',1050,70)]:
  ids=sorted(i for t,i in pairs if t==task);assert len(ids)==n;labels=sorted({clusters[task,i] for i in ids});assert len(labels)==groups
  outcomes=[c+'_'+metric for c in CONTRASTS for metric in (['p_unknown','diff_bias'] if task=='kobbq' else ['alr'])]
  array=np.array([[np.mean(pairs[task,i][m,outcome]) for m in MODELS for outcome in outcomes] for i in ids]);assert np.isfinite(array).all();clusterarray=np.array([clusters[task,i] for i in ids]);totals=np.stack([array[clusterarray==g].sum(0) for g in labels]);sizes=np.array([np.sum(clusterarray==g) for g in labels]);rng=np.random.default_rng(SEED);draw=np.vstack([(w@totals)/(w@sizes)[:,None] for w in [rng.multinomial(groups,np.repeat(1/groups,groups),size=250) for _ in range(REPS//250)]]);point=array.mean(0);width=len(outcomes)
  for row,item in zip(array,ids):
   for j,m in enumerate(MODELS):
    for k,name in enumerate(outcomes):effects.append(dict(task=task,item_id=item,cluster_id=clusters[task,item],model=m,test_id=name,effect=float(row[j*width+k])))
  for k,name in enumerate(outcomes):
   for j,m in enumerate(MODELS):within.append(dict(model=m,task=task,test_id=name,estimate=float(point[j*width+k]),n=n,clusters=groups))
   sample=np.column_stack([draw[:,j*width+k]-draw[:,k] for j in [1,2,3]]);v=np.array([point[j*width+k]-point[k] for j in [1,2,3]]);centered=sample-v;cov=np.cov(sample,rowvar=False,bias=False);rank=int(np.linalg.matrix_rank(cov,tol=np.max(np.abs(cov))*1e-10));assert rank>0;inv=np.linalg.pinv(cov,rcond=1e-10);stat=float(v@inv@v);pseudo=np.einsum('bi,ij,bj->b',centered,inv,centered);num=1+int(np.sum(pseudo>=stat));omnibus.append(dict(task=task,test_id=name,statistic=stat,covariance_rank=rank,p=num/10001,numerator=num,denominator=10001,n=n,clusters=groups,definition='Paired centered cluster-bootstrap joint quadratic test of equality of four model effects'))
  for a,b in itertools.combinations(range(4),2):
   for k,name in enumerate(outcomes):
    difference=float(point[b*width+k]-point[a*width+k]);dist=draw[:,b*width+k]-draw[:,a*width+k];lo,hi=np.quantile(dist,[.025,.975]);num=1+int(np.sum(np.abs(dist-difference)>=abs(difference)));tests.append(dict(pair_id=MODELS[b]+'_minus_'+MODELS[a],reference=MODELS[a],target=MODELS[b],task=task,test_id=name,estimate=difference,lo=float(lo),hi=float(hi),p=num/10001,numerator=num,denominator=10001,n=n,clusters=groups,unit='probability difference' if task=='kobbq' else 'natural-log yes/no ratio'))
 holm(tests,target='p_holm_global54');holm(omnibus,target='p_holm_global9')
 for pair in sorted({r['pair_id'] for r in tests}):holm([r for r in tests if r['pair_id']==pair],target='p_holm_pair9')
 for r in tests:r['significant_global54']=r['p_holm_global54']<.05
 return tests,omnibus,effects,within

def main():
 data={};sources={}
 for model in MODELS:data[model],sources[model]=raw_model(model)
 tests,omnibus,effects,within=analyze(data)
 original=list(csv.DictReader((R/'08_combined_three_model_final/SOURCE_MAIN_J33.csv').open()));original += [dict(row,model='exaone') for row in json.loads((R/'10_exaone_core/r1_replication/06_analysis/bindings_1794110904494193000_results/registered_tests.json').read_text())]
 for r in within:
  old=next(z for z in original if z['model']==r['model'] and z['test_id']==r['test_id']);assert abs(r['estimate']-float(old['estimate']))<1e-9,(r,old)
  r.update(lo=None if old['lo'] in [None,''] else float(old['lo']),hi=None if old['hi'] in [None,''] else float(old['hi']),p_holm_original_family=float(old['p_holm']),original_family=old['family'],significant_original_family=float(old['p_holm'])<.05)
 out=O/'03_results';save(out/'PAIRWISE_54.json',tests);csvsave(out/'PAIRWISE_54.csv',tests);save(out/'OMNIBUS_9.json',omnibus);csvsave(out/'OMNIBUS_9.csv',omnibus);save(out/'WITHIN_MODEL_36.json',within);csvsave(out/'WITHIN_MODEL_36.csv',within);csvsave(out/'MATCHED_ITEM_EFFECTS.csv',effects)
 save(out/'PRIMARY_COMPLETE.json',dict(complete=True,new_inference=False,post_hoc=True,seed=SEED,bootstrap_reps=REPS,pairwise_tests=54,omnibus_tests=9,within_model_estimates_reproduced=36,source_pins=sources,plan_sha256=sha(O/'00_protocol/COMPARISON_PLAN_v1.json'),code_sha256=sha(__file__),artifacts={p.name:sha(p) for p in out.iterdir() if p.is_file()}));print('primary complete',len(tests),len(omnibus))
if __name__=='__main__':main()
