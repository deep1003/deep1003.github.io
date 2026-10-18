"""Real EXAONE block16 activation collection; fixed anchors and heldout gates."""
from pathlib import Path
import json,subprocess,time,hashlib,fcntl,importlib.util
import numpy as np,pandas as pd
B=Path(__file__).resolve().parent;ROOT=B.parent
spec=importlib.util.spec_from_file_location('original',ROOT/'reference_experiment.py');ref=importlib.util.module_from_spec(spec);spec.loader.exec_module(ref)
AXES=['UN','FA','calm','sadness','anger','desperation','joy'];CONDITIONS=['U0T0','U0T1','U1T0','U1T1']
EXE=ROOT.parent/'ministral3_8b_uncertainty139_20261017/internal_probe/build/bin/exaone-capture'
WEIGHTS='/Users/deep1003/.ollama/models/blobs/sha256-fffbdeec0c334b27ebb42cbdd75a3e869cf9a3efc45abd7b3e6d739343089038'
CACHE=B/'cache';CACHE.mkdir(exist_ok=True)
def status(**d):
 d.update(updated_at=time.time());p=B/'status.json';t=p.with_suffix('.tmp');t.write_text(json.dumps(d,indent=2));t.replace(p)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def prompt(content,user=None):
 return '[|system|]'+content+'[|endofturn|]\n'+('[|user|]'+user+'\n' if user is not None else '')+'[|assistant|]'
class Worker:
 def __init__(self):
  self.log=(B/'backend.log').open('ab');self.p=subprocess.Popen([str(EXE),'-m',WEIGHTS,'-ngl','99','-c','4096','-b','512','-ub','512'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.log,text=True,bufsize=1)
 def score(self,text,key,keep_tokens=False,force=False):
  target=CACHE/(key+'.npz');meta=CACHE/(key+'.json')
  if target.exists() and meta.exists() and not force:return np.load(target),json.loads(meta.read_text())
  p=CACHE/(key+'.txt');p.write_text(text);self.p.stdin.write(str(p)+'\n');self.p.stdin.flush();line=self.p.stdout.readline();assert line,'Activation backend stopped';raw=json.loads(line);shape=list(map(int,Path(str(p)+'.shape').read_text().split()));assert shape[0]==4096 and shape[1]==raw['n_tokens']
  h=np.fromfile(str(p)+'.bin',dtype=np.float32).reshape(shape[1],shape[0]);assert np.isfinite(h).all() and raw['all_vocab_finite'];l=np.array(raw['logits']);pr=np.exp(l-l.max());pr/=pr.sum()
  saved=dict(last=h[-1].copy(),p=pr)
  if keep_tokens:saved['hidden']=h.copy()
  np.savez_compressed(target,**saved);raw.update(prompt_sha256=sha(p),shape=shape);meta.write_text(json.dumps(raw,indent=2));Path(str(p)+'.bin').unlink();Path(str(p)+'.shape').unlink();return np.load(target),raw
 def close(self):self.p.stdin.close();self.p.wait(timeout=60);self.log.close()
def run():
 items=pd.read_csv(ROOT/'items_139.csv');anchors=json.loads((B/'anchors.json').read_text());lookup=items.set_index('sample_id');behavior=pd.read_csv(ROOT/'results/trials.csv').set_index(['item','condition','rotation'])
 cfg=dict(model='EXAONE3.5-7.8B',weights=WEIGHTS,quantization='same Q4_K_M blob as behavior',backend_commit='f2f667b02dc76d675395ae3b14546c8108d26387',block_index=15,hidden_state_layer=16,n_blocks=32,depth_fraction=.5,position='post-block residual at last assistant-start token; per-token causal residual for M4',anchors_sha256=sha(B/'anchors.json'),items_sha256=sha(ROOT/'items_139.csv'),behavior_sha256=sha(ROOT/'results/trials.csv'),code_sha256=sha(__file__),binary_sha256=sha(EXE),axis_gate=dict(heldout_pair_accuracy=.75,heldout_auc=.75),smoke=dict(hidden_repeat_max=.02,probability_repeat_max=.005,behavior_probability_parity=.02),limits='Fixed authored axes; narrative-to-KoBBQ and token-position transfer are exploratory. Cosine similarity is neither emotion probability nor causal token attribution. No cross-model alignment scale equivalence.')
 mf=B/'manifest.json'
 if mf.exists():assert json.loads(mf.read_text())==cfg
 else:mf.write_text(json.dumps(cfg,indent=2))
 worker=Worker()
 try:
  status(state='smoke',completed=0,total=1812)
  first=items.iloc[0];messages,_=ref.messages(first,'U0T0',0);text=prompt(messages[0]['content'],messages[1]['content']);a,_=worker.score(text,'smoke_a');r,_=worker.score(text,'smoke_repeat',force=True)
  hd=float(abs(a['last']-r['last']).max());pdiff=float(abs(a['p']-r['p']).max());assert hd<=.02 and pdiff<.005
  (B/'smoke.json').write_text(json.dumps(dict(passed=True,hidden_repeat_error=hd,probability_repeat_error=pdiff,graphics_emitted=False),indent=2))
  vectors=[]
  for i,row in enumerate(anchors):
   pair=[]
   for side in ['positive','negative']:
    arr,_=worker.score(prompt(ref.SYS+'\n\n'+row[side]),f'anchor_{i:03d}_{side}');pair.append(arr['last'])
   vectors.append(pair);status(state='anchors',completed=2*(i+1),total=1812)
  vectors=np.array(vectors);directions=[];centers=[];scales=[];checks=[]
  for axis in AXES:
   train=[i for i,r in enumerate(anchors) if r['axis']==axis and r['split']=='train'];test=[i for i,r in enumerate(anchors) if r['axis']==axis and r['split']=='heldout'];pos=vectors[train,0].astype(float);neg=vectors[train,1].astype(float);direction=(pos-neg).mean(0);direction/=np.linalg.norm(direction);center=np.concatenate([pos,neg]).mean(0);scale=np.std((np.concatenate([pos,neg])-center)@direction,ddof=1);assert scale>1e-9;pp=(vectors[test,0]-center)@direction;nn=(vectors[test,1]-center)@direction;acc=float((pp>nn).mean());auc=float(np.mean((pp[:,None]>nn[None,:])+.5*(pp[:,None]==nn[None,:])));checks.append(dict(axis=axis,paired_accuracy=acc,auc=auc,passed=acc>=.75 and auc>=.75));directions.append(direction);centers.append(center);scales.append(scale)
  pd.DataFrame(checks).to_csv(B/'heldout_checks.csv',index=False);np.savez_compressed(B/'axes_exaone_L16.npz',directions=directions,centers=centers,scales=scales)
  # Never lower heldout thresholds to complete a figure.
  failed=[r['axis'] for r in checks if not r['passed']]
  if failed:status(state='blocked_axis_validation',failed_axes=failed,completed=140,total=1812);return
  directions=np.array(directions);centers=np.array(centers);rows=[];max_parity=0.
  for count,(item,c,rotation) in enumerate([(i,c,r) for i in items.sample_id for c in CONDITIONS for r in range(3)],1):
   m,choices=ref.messages(lookup.loc[item],c,rotation);arr,_=worker.score(prompt(m[0]['content'],m[1]['content']),f'trial_{count-1:04d}');diff=arr['last'][None,:]-centers;cos=np.einsum('ad,ad->a',diff,directions)/np.linalg.norm(diff,axis=1);assert np.isfinite(cos).all();parity=abs(float(arr['p'][choices.index('알 수 없음')])-float(behavior.loc[(item,c,rotation),'p_unknown']));max_parity=max(max_parity,parity);assert parity<=.02,f'Behavior parity failed: {parity}'
   r=dict(item=item,condition=c.replace('U','UN').replace('T','FA'),rotation=rotation,layer=16,category=lookup.loc[item,'category'],cluster=lookup.loc[item,'cluster']);r.update({'cos_'+axis:float(v) for axis,v in zip(AXES,cos)});rows.append(r)
   status(state='items',completed=140+count,total=1812,behavior_parity_max=max_parity)
  trial=pd.DataFrame(rows);assert len(trial)==1668 and not trial.duplicated(['item','condition','rotation']).any();trial.to_csv(B/'trial_alignment.csv',index=False);trial.groupby(['item','condition','category','cluster','layer'],as_index=False)[['cos_'+a for a in AXES]].mean().to_csv(B/'item_alignment.csv',index=False)
  payload=[];tokenrows=[]
  for c in CONDITIONS:
   content=ref.SYS+'\n\n'+ref.CONDITIONS[c];text=prompt(content);arr,meta=worker.score(text,'prompt_'+c,keep_tokens=True);pieces=[bytes.fromhex(x) for x in meta['pieces_hex']];decoded=b''.join(pieces);target=text.encode();start=decoded.find(target);assert start>=0,'Decoded token pieces do not exactly reconstruct prompt';content_start=start+target.find(content.encode());offsets=np.cumsum([0]+[len(x) for x in pieces]);h=arr['hidden'];diff=h[:,None,:]-centers[None,:,:];cos=np.einsum('tad,ad->ta',diff,directions)/np.linalg.norm(diff,axis=2);assert np.isfinite(cos).all();chars=[];absolute=content_start
   for ch in content:
    end=absolute+len(ch.encode());idx=np.flatnonzero((offsets[:-1]<end)&(offsets[1:]>absolute));assert len(idx)>0;chars.append(dict(char=ch,tokens=idx.tolist(),cosine=cos[idx].mean(0).tolist()));absolute=end
   name=c.replace('U','UN').replace('T','FA');payload.append(dict(condition=name,text=content,layers={'16':chars}));
   for t,piece in enumerate(pieces):
    for ai,axis in enumerate(AXES):tokenrows.append(dict(condition=name,token_index=t,piece_hex=piece.hex(),axis=axis,cosine=float(cos[t,ai])))
  (B/'highlights.json').write_text(json.dumps(dict(axes=AXES,prompts=payload),ensure_ascii=False));pd.DataFrame(tokenrows).to_csv(B/'token_scores.csv',index=False)
  (B/'validation.json').write_text(json.dumps(dict(n_trials=1668,n_items=139,n_clusters=91,n_prompts=4,all_axes_passed=True,all_finite=True,all_character_bytes_matched=True,behavior_parity_max=max_parity),indent=2));status(state='measured',completed=1812,total=1812)
 finally:worker.close()
 import render_publish
 render_publish.finish();status(state='complete',completed=1812,total=1812)
if __name__=='__main__':
 with (B/'writer.lock').open('w') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  try:run()
  except Exception as e:status(state='error',error=repr(e));raise
