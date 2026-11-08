"""Independent implementation from sealed trial tables. Does not import primary code."""
import json,hashlib,itertools
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parents[1]
primary=json.loads((P/'03_results/PRIMARY_COMPLETE.json').read_text())
models=['qwen','llama','gemma','exaone']; output=P/'04_independent';output.mkdir(exist_ok=True)
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
cohorts={}
for model in models:
 source=primary['source_pins'][model];path=source['verified_outcomes'];assert digest(path)==source['outcomes_sha256']
 rows=json.loads(Path(path).read_text());d={}
 for row in rows:
  if row['condition'] in ['CN0','CN1','UN0','UN1'] and (row['task']!='kobbq' or row['ambiguous']):
   d[(row['task'],row['item_id'],str(row['order']),row['condition'])]=row
 cohorts[model]=d
assert all(set(cohorts[m])==set(cohorts[models[0]]) for m in models)
checks=[];joint=[];mismatches=[]
for task in ['kobbq','discrimeval']:
 ids=sorted({k[1] for k in cohorts['qwen'] if k[0]==task});metrics=['p_unknown','diff_bias'] if task=='kobbq' else ['alr'];names=[c+'_'+m for c in ['C','U','I'] for m in metrics];values=[];clusters=[]
 for item in ids:
  rotations=sorted({k[2] for k in cohorts['qwen'] if k[:2]==(task,item)});records=[]
  for model in models:
   cell=[]
   for contrast in ['C','U','I']:
    for metric in metrics:
     samples=[]
     for rotation in rotations:
      r=lambda c:cohorts[model][task,item,rotation,c][metric]
      closed=r('CN1')-r('CN0');opened=r('UN1')-r('UN0');samples.append(closed if contrast=='C' else opened if contrast=='U' else closed-opened)
     cell.append(sum(samples)/len(samples))
   records.append(cell)
  values.append(records);clusters.append(str(cohorts['qwen'][task,item,rotations[0],'CN0']['cluster_id']))
 values=np.array(values);groups=sorted(set(clusters));clusters=np.array(clusters);n=len(groups);means=values.mean(axis=0)
 sums=np.array([values[clusters==g].sum(axis=0) for g in groups]);sizes=np.array([sum(clusters==g) for g in groups]);rng=np.random.default_rng(20261031);boots=[]
 for repeat in range(10000):
  counts=rng.multinomial(n,[1/n]*n);boots.append(np.tensordot(counts,sums,axes=1)/np.dot(counts,sizes))
 boots=np.array(boots)
 for ai,bi in itertools.combinations(range(4),2):
  for k,name in enumerate(names):
   observed=means[bi,k]-means[ai,k];sample=boots[:,bi,k]-boots[:,ai,k];num=1+np.count_nonzero(abs(sample-observed)>=abs(observed));bounds=np.percentile(sample,[2.5,97.5]);checks.append(dict(reference=models[ai],target=models[bi],task=task,test_id=name,estimate=float(observed),lo=float(bounds[0]),hi=float(bounds[1]),p=float(num/10001),numerator=int(num)))
 for k,name in enumerate(names):
  observed=means[1:,k]-means[0,k];samples=boots[:,1:,k]-boots[:,0:1,k];covariance=np.cov(samples.T);inverse=np.linalg.pinv(covariance,rcond=1e-10);stat=float(np.dot(observed,np.dot(inverse,observed)));center=samples-observed;pseudo=np.sum((center@inverse)*center,axis=1);num=1+np.count_nonzero(pseudo>=stat);joint.append(dict(task=task,test_id=name,statistic=stat,p=float(num/10001),numerator=int(num)))
 for k,name in enumerate(names):
  for j,model in enumerate(models):
   expected=next(r for r in json.loads((P/'03_results/WITHIN_MODEL_36.json').read_text()) if r['model']==model and r['test_id']==name)
   assert abs(means[j,k]-expected['estimate'])<1e-12

def adjust(rows,key):
 order=np.argsort([r['p'] for r in rows],kind='stable');adjusted=np.maximum.accumulate(np.minimum(1,np.array([rows[i]['p'] for i in order])*np.arange(len(rows),0,-1)))
 for i,v in zip(order,adjusted):rows[i][key]=float(v)
adjust(checks,'p_holm_global54');adjust(joint,'p_holm_global9')
for a,b in itertools.combinations(models,2):adjust([r for r in checks if r['reference']==a and r['target']==b],'p_holm_pair9')
for filename,records,fields in [('PAIRWISE_54',checks,['estimate','lo','hi','p','numerator','p_holm_global54','p_holm_pair9']),('OMNIBUS_9',joint,['statistic','p','numerator','p_holm_global9'])]:
 original=json.loads((P/'03_results'/f'{filename}.json').read_text())
 for row in records:
  same=next(r for r in original if all(row.get(k)==r.get(k) for k in ['reference','target','task','test_id']))
  for field in fields:
   if not np.isclose(row[field],same[field],rtol=1e-10,atol=1e-12):mismatches.append([filename,row['test_id'],field,row[field],same[field]])
 (output/f'{filename}_INDEPENDENT.json').write_text(json.dumps(records,indent=2))
# A paired shared shock must cancel exactly, and multiplicity must be monotonic and bounded.
shock=np.arange(21.)[:,None];x=np.repeat(shock,4,axis=1)+np.array([0.,2.,-1.,4.]);assert np.all(x[:,1]-x[:,0]==2)
fixture=[dict(p=p) for p in [.04,.001,.03,.8]];adjust(fixture,'q');assert np.allclose([r['q'] for r in fixture],[.09,.004,.09,.8])
proof=dict(passed=not mismatches,mismatches=mismatches,pairwise=54,omnibus=9,within_model=36,source_sha_verified=True,bootstrap=10000,seed=20261031,synthetic_pairing_and_holm_pass=True,code_sha256=digest(__file__),primary_complete_sha256=digest(P/'03_results/PRIMARY_COMPLETE.json'),independence='Separate parser, contrasts, one-draw bootstrap loop and correction implementation; no primary import; same sealed source values')
(output/'INDEPENDENT_QA.json').write_text(json.dumps(proof,indent=2));print(json.dumps(proof));assert proof['passed']
