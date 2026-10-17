from pathlib import Path
import json,subprocess,time,fcntl,hashlib,importlib.util,urllib.request
import numpy as np,pandas as pd
BASE=Path(__file__).resolve().parent;OUT=BASE/'results';OUT.mkdir(exist_ok=True);PROMPTS=BASE/'prompts';PROMPTS.mkdir(exist_ok=True)
sp=importlib.util.spec_from_file_location('reference',BASE/'reference_experiment.py');ref=importlib.util.module_from_spec(sp);sp.loader.exec_module(ref)
EXE=BASE.parent/'ministral3_8b_uncertainty139_20261017/internal_probe/build/bin/exaone-direct-logits'
MODEL='llama3.1:8b'
def status(**d):
 d.update(updated_at=time.time());p=OUT/'status.json';tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(d,indent=2));tmp.replace(p)
def post(endpoint,body):return json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:11434'+endpoint,data=json.dumps(body).encode(),headers={'Content-Type':'application/json'}),timeout=180))
def prepare():
 items=pd.read_csv(BASE/'items_139.csv');assert len(items)==139 and items.cluster.nunique()==91
 show=post('/api/show',dict(model=MODEL));modelfile=show['modelfile'];blob=Path(next(x[5:].strip() for x in modelfile.splitlines() if x.startswith('FROM ')));assert blob.exists()
 cfg=dict(model=MODEL,weights=str(blob),details=show['details'],template=show['template'],n_items=139,n_clusters=91,n_trials=1668,seed=20261017,direct_all_vocab_logits=True,thresholds=dict(repeat=.005,backend=.02,korean_controls_min_correct=15,korean_controls_total=18),contrasts=['uncertainty','threat','combined=U1T1-U0T0'],inference='10000 paired template cluster bootstrap; Holm3 within model; unadjusted95CI',limits='Reused selected items. Korean is outside officially supported eight languages; synthetic controls test basic comprehension only. Model,precision and template differ across models.',sample_sha256=hashlib.sha256((BASE/'items_139.csv').read_bytes()).hexdigest(),code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),binary_sha256=hashlib.sha256(EXE.read_bytes()).hexdigest())
 p=OUT/'manifest.json'
 if p.exists():assert json.loads(p.read_text())==cfg
 else:p.write_text(json.dumps(cfg,ensure_ascii=False,indent=2))
 return items,blob
class Worker:
 def __init__(self,blob):
  self.log=(BASE/'backend.log').open('ab');self.p=subprocess.Popen([str(EXE),'-m',str(blob),'-ngl','99','-c','4096','-b','512','-ub','512'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.log,text=True,bufsize=1)
 def messages(self,messages,key):
  text=''.join('<|start_header_id|>'+m['role']+'<|end_header_id|>\n\n'+m['content']+'<|eot_id|>' for m in messages)+'<|start_header_id|>assistant<|end_header_id|>\n\n';path=PROMPTS/(key+'.txt');path.write_text(text);self.p.stdin.write(str(path)+'\n');self.p.stdin.flush();line=self.p.stdout.readline();assert line,'Direct backend stopped; inspect backend.log';raw=json.loads(line);logits=np.array(raw['logits']);assert raw['all_vocab_finite'] and np.isfinite(logits).all();p=np.exp(logits-logits.max());p/=p.sum();assert np.isfinite(p).all() and np.isclose(p.sum(),1);raw.update(probabilities=p.tolist());out=OUT/'raw';out.mkdir(exist_ok=True);(out/(key+'.json')).write_text(json.dumps(raw,indent=2));return p,raw
 def score(self,item,c,r,key):
  messages,choices=ref.messages(item,c,r);p,raw=self.messages(messages,key);pm=dict(zip(choices,map(float,p)));anti=next(x for x in choices if x not in ['알 수 없음',item.biased_answer]);mass=float(np.exp(np.array(raw['logits'])-raw['full_logsumexp']).sum());row=dict(item=item.name,condition=c,rotation=r,p_unknown=pm['알 수 없음'],p_stereotype=pm[item.biased_answer],p_anti=pm[anti],choice_mass=mass);return row,p,raw
 def close(self):self.p.stdin.close();self.p.wait(timeout=60);self.log.close()
def run():
 items,blob=prepare();lookup=items.set_index('sample_id')
 with (BASE/'writer.lock').open('w') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  w=Worker(blob)
  try:
   status(state='smoke',completed=0,total=1668);control=json.loads((BASE/'korean_controls.json').read_text());outcomes=[]
   for i,c in enumerate(control['controls']):
    for r in range(3):
     choices=c['choices'][r:]+c['choices'][:r];user='다음 질문에 답하세요. 반드시 선택지 번호 하나만 숫자로 답하세요.\n\n'+c['context']+'\n'+c['question']+'\n'+'\n'.join(f'{j+1}: {v}' for j,v in enumerate(choices));p,_=w.messages([dict(role='system',content=ref.SYS),dict(role='user',content=user)],f'control_{i}_{r}');outcomes.append(dict(control=i,rotation=r,expected=c['answer'],selected=choices[int(p.argmax())],correct=choices[int(p.argmax())]==c['answer'],probabilities=p.tolist()))
   (OUT/'korean_controls.json').write_text(json.dumps(outcomes,ensure_ascii=False,indent=2));correct=sum(x['correct'] for x in outcomes);assert correct>=control['pass_min_correct'],f'Korean smoke failed: {correct}/18; fixed minimum15'
   sample=items.sort_values('sample_id').groupby('category',sort=True).head(1).iloc[:2];repeat_error=0.;smoke_trials=0
   for i,item in sample.iterrows():
    for c in ref.CONDITIONS:
     for r in range(3):
      _,p,_=w.score(lookup.loc[item.sample_id],c,r,f'smoke_{smoke_trials:03d}');smoke_trials+=1
      if smoke_trials==1:
       _,q,_=w.score(lookup.loc[item.sample_id],c,r,'smoke_repeat');repeat_error=float(abs(p-q).max());assert repeat_error<.005
   # Native Ollama token-count and probability parity on an actual study prompt.
   item=lookup.iloc[0];m,_=ref.messages(item,'U0T0',0);_,p,raw=w.score(item,'U0T0',0,'smoke_native_direct');w.close();w=None;native=post('/api/chat',dict(model=MODEL,messages=m,stream=False,logprobs=True,top_logprobs=20,options=dict(num_predict=1,temperature=1,top_k=0,top_p=1,repeat_penalty=1,num_ctx=4096,seed=20261017),keep_alive=0));(OUT/'native_smoke.json').write_text(json.dumps(native,ensure_ascii=False));assert raw['n_tokens']==native['prompt_eval_count'],'Native/direct prompt token count differs';tops={x['token']:x['logprob'] for x in native['logprobs'][0]['top_logprobs']};assert all(str(i) in tops for i in [1,2,3]),'Native parity probe missing choice probability; stop without substitution';q=np.exp([tops[str(i)] for i in [1,2,3]]);q/=q.sum();backend_error=float(abs(p-q).max());assert backend_error<=.02;w=Worker(blob)
   (OUT/'smoke.json').write_text(json.dumps(dict(passed=True,korean_controls_correct=correct,korean_controls_total=18,study_smoke_trials=smoke_trials,repeat_error=repeat_error,backend_error=backend_error,thresholds=dict(repeat=.005,backend=.02),graphics_emitted=False),indent=2))
   # A resume uses only same-manifest direct-backend rows.
   file=OUT/'trials.csv';rows=pd.read_csv(file).to_dict('records') if file.exists() else []
   if rows:ref.validate(pd.DataFrame(rows),items)
   done={(x['item'],x['condition'],x['rotation']) for x in rows};plan=[(i,c,r) for i in items.sample_id for c in ref.CONDITIONS for r in range(3)]
   for index in np.random.default_rng(20261017).permutation(len(plan)):
    i,c,r=plan[index]
    if (i,c,r) in done:continue
    row,_,_=w.score(lookup.loc[i],c,r,f'trial_{index:04d}');ref.validate(pd.DataFrame([row]),items);rows.append(row);tmp=file.with_suffix('.tmp');pd.DataFrame(rows).to_csv(tmp,index=False);tmp.replace(file);status(state='running',completed=len(rows),total=1668)
   ref.validate(pd.DataFrame(rows),items,True)
  finally:
   if w is not None:w.close()
 return analyze()
def analyze():
 items=pd.read_csv(BASE/'items_139.csv');d=pd.read_csv(OUT/'trials.csv');ref.validate(d,items,True);v=d.groupby(['item','condition']).p_unknown.mean().unstack().reindex(items.sample_id);g=items.cluster.astype('category').cat.codes.to_numpy();n=g.max()+1;w=np.random.default_rng(20261017).multinomial(n,np.ones(n)/n,size=10000)[:,g].astype(float);w/=w.sum(1,keepdims=True);rows=[]
 for term,delta in dict(uncertainty=((v.U1T0-v.U0T0)+(v.U1T1-v.U0T1))/2,threat=((v.U0T1-v.U0T0)+(v.U1T1-v.U1T0))/2,combined=v.U1T1-v.U0T0).items():
  bs=w@delta.to_numpy();lo,hi=np.quantile(bs,[.025,.975]);p=min(1,2*min((bs<=0).mean(),(bs>=0).mean())+.0001);rows.append(dict(term=term,estimate=float(delta.mean()),ci_low=float(lo),ci_high=float(hi),p=float(p)))
 adj=0
 for rank,r in enumerate(sorted(rows,key=lambda r:r['p'])):adj=max(adj,min(1,r['p']*(3-rank)));r['p_holm']=adj
 (OUT/'summary.json').write_text(json.dumps(dict(model=MODEL,n_items=139,n_clusters=91,n_trials=1668,study_type='exploratory',primary=rows,conditions=v.mean().to_dict()),indent=2));previous=pd.read_csv(BASE/'previous_comparison.csv');new=pd.DataFrame([dict(model='Llama3.1-8B Q4_K_M',term=r['term'],effect_pp=100*r['estimate'],p_holm=r['p_holm'],significant=r['p_holm']<.05) for r in rows]);comparison=pd.concat([previous,new],ignore_index=True);comparison.to_csv(OUT/'comparison.csv',index=False);status(state='complete',completed=1668,total=1668);return comparison
