"""Frozen exploratory last-token residual intervention. No graph output during smoke."""
from pathlib import Path
import json,sqlite3,time,os,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent
SRC=ROOT.parent/'kobbq_v5_two_sets_20261022'

def save(name,x):
 p=ROOT/name;t=p.with_suffix('.tmp');t.write_text(json.dumps(x,ensure_ascii=False,indent=2));t.replace(p)

def main():
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 import transformers.modeling_utils as mu
 mu.caching_allocator_warmup=lambda *a,**k:None
 torch.set_num_threads(4);torch.manual_seed(20261024)
 design=json.loads((ROOT/'DESIGN_FROZEN.json').read_text());cases=json.loads((ROOT/'pilot_cases.json').read_text())
 frozen=json.loads((SRC/'prompts_v5.json').read_text());prompts={p['condition']:p['system_content'] for p in frozen['conditions']}
 v=np.load(ROOT/'intervention_vectors.npz');alpha=float(v['alpha'])
 axes=np.load(SRC/'source/axes_L14.npz',allow_pickle=True);names=list(axes['names']);dirs=axes['directions'].astype(float);dirs/=np.linalg.norm(dirs,axis=1)[:,None];centers=axes['centers']
 arms=design['arms'];conditions=design['conditions']
 save('status.json',dict(state='loading',pid=os.getpid(),completed=0,planned=2592))
 tok=AutoTokenizer.from_pretrained('Qwen/Qwen2.5-7B-Instruct',revision='a09a35458c702b33eeacc393d103063234e8bc28',local_files_only=True)
 model=AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-7B-Instruct',revision='a09a35458c702b33eeacc393d103063234e8bc28',torch_dtype=torch.float32,device_map='mps',attn_implementation='eager',local_files_only=True).eval()
 vectors={'sham':np.zeros_like(v['Fear'])}
 for n in ['Fear','Anxiety','Desperation','Random']:
  for sign,suffix in [(1,'+'),(-1,'-')]:vectors[n+suffix]=sign*alpha*v[n]
 tv={k:torch.tensor(x,dtype=torch.float32,device='mps') for k,x in vectors.items()}
 current={'arm':'sham'};captured={}
 def hook(module,args,output):
  is_tuple=isinstance(output,tuple);h=output[0] if is_tuple else output
  h=h.clone();before=h[:,-1,:].detach().clone();h[:,-1,:]+=tv[current['arm']]
  captured['before']=before.cpu().numpy()[0];captured['after']=h[:,-1,:].detach().cpu().numpy()[0]
  return (h,)+output[1:] if is_tuple else h
 handle=model.model.layers[13].register_forward_hook(hook)
 ids=[tok.convert_tokens_to_ids(str(i)) for i in [1,2,3]]
 source=sqlite3.connect(f'file:{SRC}/measurements.sqlite?mode=ro',uri=True)
 db=sqlite3.connect(ROOT/'interventions.sqlite');db.execute('create table if not exists trials(case_id text,condition text,rotation integer,arm text,record text,primary key(case_id,condition,rotation,arm))');db.commit()
 done=set(db.execute('select case_id,condition,rotation,arm from trials'));rng=np.random.default_rng(20261024)
 jobs=[(c,cond,r,arm) for c in cases for cond in conditions for r in range(3) for arm in arms];rng.shuffle(jobs)
 smoke=[];smoke_valid=(ROOT/'smoke_validation.json').exists();start=time.time();count=len(done)
 # Run sham and both signs before main jobs; duplicates skip durably.
 first=cases[0];jobs=[(first,'UN0',0,a) for a in arms]+jobs
 for case,cond,rot,arm in jobs:
  key=(case['case_id'],cond,rot,arm)
  if key in done:
   if not smoke_valid and case['case_id']==cases[0]['case_id'] and cond=='UN0' and rot==0:
    smoke.append(json.loads(db.execute('select record from trials where case_id=? and condition=? and rotation=? and arm=?',key).fetchone()[0]))
   continue
  if Path('/tmp/STOP_EMOTION_INTERVENTION').exists():break
  order=case['choices'][rot:]+case['choices'][:rot]
  user=frozen['user_template'].format(context=case['context'],question=case['question'],o1=order[0],o2=order[1],o3=order[2])
  text=tok.apply_chat_template([{'role':'system','content':prompts[cond]},{'role':'user','content':user}],tokenize=False,add_generation_prompt=True)
  enc=tok(text,return_tensors='pt').to('mps');current['arm']=arm
  with torch.no_grad():output=model(**enc,output_hidden_states=True,logits_to_keep=1)
  logits=output.logits[0,-1].float().cpu().double().numpy();three=logits[ids];p=np.exp(three-three.max());p/=p.sum();mass=float(np.exp(np.logaddexp.reduce(three)-np.logaddexp.reduce(logits)))
  h=output.hidden_states[14][0,-1].float().cpu().numpy();delta=h.astype(float)-centers;cos=(delta*dirs).sum(1)/np.linalg.norm(delta,axis=1)
  target_error=float(np.max(np.abs((captured['after']-captured['before'])-vectors[arm])))
  assert target_error<1e-5 and np.max(np.abs(h-captured['after']))<1e-6
  assert np.isfinite(p).all() and np.isfinite(cos).all()
  u=float(p[order.index('알 수 없음')]);b=float(p[order.index(case['biased_answer'])]);anti=next(x for x in order if x not in ['알 수 없음',case['biased_answer']]);a=float(p[order.index(anti)])
  record=dict(case_id=case['case_id'],cluster=case['cluster'],category=case['category'],case_type=case['case_type'],condition=cond,rotation=rot,arm=arm,p_unknown=u,p_biased=b,p_anti=a,p_person_bias=float(np.exp(three[order.index(case['biased_answer'])]-np.logaddexp(three[order.index(case['biased_answer'])],three[order.index(anti)]))),p_correct=float(p[order.index(case['answer'])]),choice_mass=mass,hook_error=target_error,hidden_norm=float(np.linalg.norm(h)),**{f't2_{n}':float(x) for n,x in zip(names,cos)})
  if arm=='sham':
   old=json.loads(source.execute('select record from measurements where case_id=? and condition=? and rotation=?',key[:3]).fetchone()[0]);err=max(abs(record[x]-old[x]) for x in ['p_unknown','p_biased','p_correct','t2_Fear','t2_Anxiety'])
   assert err<1e-6,err
   record['sham_max_error']=err
  db.execute('insert into trials values(?,?,?,?,?)',(*key,json.dumps(record,ensure_ascii=False)));db.commit();done.add(key);count+=1
  if not smoke_valid and len(smoke)<9:
   smoke.append(record)
   if len(smoke)==9:
    ss={x['arm']:x for x in smoke}
    for n in ['Fear','Anxiety','Desperation']:
     assert ss[n+'+']['t2_'+n]>ss['sham']['t2_'+n]>ss[n+'-']['t2_'+n]
    save('smoke_validation.json',dict(passed=True,n=9,no_graphs=True,records=smoke));smoke_valid=True
  if count%20==0 or count==2592:
   state=dict(state='complete' if count==2592 else 'running',pid=os.getpid(),completed=count,planned=2592,elapsed_seconds=time.time()-start,rate_per_minute=(count*60/(time.time()-start)))
   save('status.json',state);print(json.dumps(state),flush=True)
  del output
 handle.remove();db.close()
 if count==2592:(ROOT/'DONE').write_text('All frozen keys completed.\n')

if __name__=='__main__':main()
