"""FP32 causal-prefix-cached layer/dose intervention; verify against full forwards."""
from pathlib import Path
import copy,hashlib,json,os,sqlite3,time
import numpy as np
ROOT=Path(__file__).resolve().parent
SRC=ROOT.parent/'kobbq_v5_two_sets_20261022'

def save(name,data):
 p=ROOT/name;t=p.with_suffix('.tmp');t.write_text(json.dumps(data,ensure_ascii=False,indent=2));t.replace(p)

def main():
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 import transformers.modeling_utils as mu
 mu.caching_allocator_warmup=lambda *a,**k:None
 torch.set_num_threads(4);torch.manual_seed(20261025)
 plan=json.loads((ROOT/'DESIGN_FROZEN.json').read_text());layers=plan['layers'];axes=plan['axes'];cases=json.loads((ROOT/'cases.json').read_text());anchors=json.loads((ROOT/'anchors.json').read_text())
 save('status.json',dict(state='loading',pid=os.getpid(),completed=0,planned=10560))
 tok=AutoTokenizer.from_pretrained(plan['model'],revision=plan['revision'],local_files_only=True)
 model=AutoModelForCausalLM.from_pretrained(plan['model'],revision=plan['revision'],dtype=torch.float32,device_map='mps',attn_implementation='eager',local_files_only=True).eval()
 assert model.config.num_hidden_layers==28 and next(model.parameters()).dtype==torch.float32
 ids=[tok.convert_tokens_to_ids(str(i)) for i in [1,2,3]];assert ids==[16,17,18]
 calls=0
 def forward(**kwargs):
  nonlocal calls
  calls+=1
  with torch.inference_mode():return model(**kwargs,output_hidden_states=True,logits_to_keep=1)
 def encode(messages):return tok(tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True),return_tensors='pt').to('mps')
 anchor_system=json.loads((ROOT/'anchor_system.json').read_text())['system']
 cache_dir=ROOT/'anchor_hidden';cache_dir.mkdir(exist_ok=True)
 for i,pair in enumerate(anchors):
  for side in ['positive','negative']:
   path=cache_dir/f'{i:02d}_{side}.npy'
   if path.exists():continue
   out=forward(**encode([{'role':'system','content':anchor_system+'\n\n'+pair[side]}]),use_cache=False)
   h=np.stack([out.hidden_states[l][0,-1].float().cpu().numpy() for l in layers]);assert np.isfinite(h).all();np.save(path,h);del out
  if (i+1)%4==0:save('status.json',dict(state='building_layer_axes',anchor_pairs_done=i+1,total_anchor_pairs=len(anchors),pid=os.getpid(),completed=0,planned=10560))
 data=np.array([[np.load(cache_dir/f'{i:02d}_{s}.npy') for s in ['positive','negative']] for i in range(len(anchors))]).astype(float)
 vectors={};centers={};norms={};checks=[];legacy=np.load(ROOT/'legacy_axes_L14.npz',allow_pickle=True)
 for j,layer in enumerate(layers):
  norms[layer]=float(np.mean([np.linalg.norm(data[i,s,j]) for i,p in enumerate(anchors) if p['split']=='train' for s in [0,1]]))
  for axis in axes:
   train=[i for i,p in enumerate(anchors) if p['axis']==axis and p['split']=='train'];assert len(train)==6
   a,b=data[train,0,j],data[train,1,j];v=(a-b).mean(0);v/=np.linalg.norm(v);center=np.concatenate([a,b]).mean(0);vectors[layer,axis]=v;centers[layer,axis]=center
   for split in ['heldout','challenge']:
    test=[i for i,p in enumerate(anchors) if p['axis']==axis and p['split']==split]
    if not test:continue
    pp=(data[test,0,j]-center)@v;nn=(data[test,1,j]-center)@v;acc=float(np.mean(pp>nn));auc=float(np.mean((pp[:,None]>nn[None,:])+.5*(pp[:,None]==nn[None,:])));checks.append(dict(layer=layer,axis=axis,split=split,n_pairs=len(test),paired_accuracy=acc,auc=auc,passed=bool(acc>=.75 and auc>=.75)))
   if layer==14:
    old=legacy['directions'][list(legacy['names']).index(axis)].astype(float);old/=np.linalg.norm(old);similarity=float(v@old);assert similarity>.99999,('L14 original axis mismatch',axis,similarity)
    checks.append(dict(layer=14,axis=axis,split='legacy_direction_reproduction',cosine=similarity,passed=True))
  q=np.linalg.qr(np.stack([vectors[layer,a] for a in axes]).T)[0];rng=np.random.default_rng(plan['seed']+layer);r=rng.normal(size=len(q));r-=q@(q.T@r);r/=np.linalg.norm(r);vectors[layer,'Random']=r
 scales={l:plan['reference_alpha_L14']*norms[l]/norms[14] for l in layers}
 np.savez(ROOT/'layer_vectors.npz',**{f'L{l}_{a}':v for (l,a),v in vectors.items()},**{f'L{l}_{a}_center':v for (l,a),v in centers.items()},layers=layers,base_alpha=[scales[l] for l in layers])
 save('axis_validation.json',dict(checks=checks,train_hidden_norms=norms,base_alpha=scales,no_behavior_selection=True))
 current={'layer':None,'vector':None};capture={}
 def hook_for(layer):
  def hook(module,args,output):
   if current['layer']!=layer:return output
   is_tuple=isinstance(output,tuple);h=(output[0] if is_tuple else output).clone();before=h[:,-1,:].detach().clone();h[:,-1,:]+=current['vector'];capture['before']=before.cpu().numpy()[0];capture['after']=h[:,-1,:].detach().cpu().numpy()[0]
   return (h,)+output[1:] if is_tuple else h
  return hook
 handles=[model.model.layers[l-1].register_forward_hook(hook_for(l), prepend=True) for l in layers]
 settings=[(0,0.,'sham')]+[(l,d,a+sign) for l in layers for d in plan['dose_multipliers'] for a in axes+['Random'] for sign in ['+','-']]
 tensor_vectors={(l,d,arm):torch.tensor((1 if arm[-1]=='+' else -1)*d*scales[l]*vectors[l,arm[:-1]],dtype=torch.float32,device='mps') for l,d,arm in settings if arm!='sham'}
 frozen=json.loads((ROOT/'prompts_v5.json').read_text());prompts={p['condition']:p['system_content'] for p in frozen['conditions']}
 db=sqlite3.connect(ROOT/'measurements.sqlite');db.execute('create table if not exists trials(case_id text,condition text,rotation int,layer int,dose real,arm text,record text,primary key(case_id,condition,rotation,layer,dose,arm))');db.commit()
 done=set(db.execute('select case_id,condition,rotation,layer,dose,arm from trials'));source=sqlite3.connect(f'file:{SRC}/measurements.sqlite?mode=ro',uri=True)
 def set_config(config):
  current['layer']=None if config[2]=='sham' else config[0];current['vector']=tensor_vectors.get(config)
 def read(out,config):
  logits=out.logits[0,-1].float().cpu().double().numpy();lg=logits[ids];p=np.exp(lg-lg.max());p/=p.sum();mass=float(np.exp(np.logaddexp.reduce(lg)-np.logaddexp.reduce(logits)));states={l:out.hidden_states[l][0,-1].float().cpu().numpy().copy() for l in layers}
  assert np.isfinite(p).all() and all(np.isfinite(h).all() for h in states.values())
  err=0.
  if config[2]!='sham':
   err=float(np.max(np.abs((capture['after']-capture['before'])-tensor_vectors[config].cpu().numpy())));assert err<1e-5
   assert np.max(np.abs(states[config[0]]-capture['after']))<1e-6
  return dict(p=p,logits=lg,mass=mass,states=states,hook_error=err)
 def full(enc,config):
  set_config(config);out=forward(**enc,use_cache=False);r=read(out,config);del out;return r
 def make_prefix(enc):
  set_config((0,0.,'sham'));out=forward(input_ids=enc.input_ids[:,:-1],attention_mask=enc.attention_mask[:,:-1],use_cache=True);prefix=out.past_key_values;del out;return prefix
 def cached(enc,prefix,config):
  set_config(config);past=copy.deepcopy(prefix)
  out=forward(input_ids=enc.input_ids[:,-1:],attention_mask=enc.attention_mask,past_key_values=past,use_cache=True);r=read(out,config);del out,past;return r
 smoke=[];max_prob_error=0.;max_logit_error=0.;max_sham_error=0.;prefix_checks=[]
 input_jobs=[(case,cond,rot) for case in cases for cond in plan['conditions'] for rot in range(3)];np.random.default_rng(plan['seed']).shuffle(input_jobs);start=time.time();initial=len(done);count=initial
 for input_index,(case,cond,rot) in enumerate(input_jobs):
  if all((case['case_id'],cond,rot,*cfg) in done for cfg in settings):continue
  order=case['choices'][rot:]+case['choices'][:rot];user=frozen['user_template'].format(context=case['context'],question=case['question'],o1=order[0],o2=order[1],o3=order[2]);enc=encode([{'role':'system','content':prompts[cond]},{'role':'user','content':user}]);baseline=full(enc,(0,0.,'sham'));prefix=make_prefix(enc);cached_base=cached(enc,prefix,(0,0.,'sham'))
  old=json.loads(source.execute('select record from measurements where case_id=? and condition=? and rotation=?',(case['case_id'],cond,rot)).fetchone()[0]);reproduction=max(abs(float(baseline['p'][order.index('알 수 없음')])-old['p_unknown']),abs(float(baseline['p'][order.index(case['biased_answer'])])-old['p_biased']));assert reproduction<1e-6;max_sham_error=max(max_sham_error,reproduction)
  def check(ref,observed):
   nonlocal max_prob_error,max_logit_error
   ep=float(np.max(np.abs(ref['p']-observed['p'])));el=float(np.max(np.abs(ref['logits']-observed['logits'])));max_prob_error=max(max_prob_error,ep);max_logit_error=max(max_logit_error,el);assert ep<=2e-5 and el<=.002,(ep,el);return ep,el
  ep,el=check(baseline,cached_base);prefix_checks.append(dict(case_id=case['case_id'],condition=cond,rotation=rot,probability_error=ep,logit_error=el,source_reproduction_error=reproduction))
  if not (ROOT/'smoke_validation.json').exists():
   for cfg in settings[1:]:
    a=full(enc,cfg);b=cached(enc,prefix,cfg);ep,el=check(a,b);smoke.append(dict(layer=cfg[0],dose=cfg[1],arm=cfg[2],probability_error=ep,logit_error=el,hook_error=b['hook_error']))
   save('smoke_validation.json',dict(passed=True,no_graphs=True,n_interventions=54,max_probability_error=max_prob_error,max_logit_error=max_logit_error,records=smoke))
  for cfg in settings:
   key=(case['case_id'],cond,rot,*cfg)
   if key in done:continue
   r=cached_base if cfg[2]=='sham' else cached(enc,prefix,cfg);p=r['p'];anti=next(x for x in order if x not in ['알 수 없음',case['biased_answer']]);biased_idx=order.index(case['biased_answer']);anti_idx=order.index(anti);q=float(np.exp(r['logits'][biased_idx]-np.logaddexp(r['logits'][biased_idx],r['logits'][anti_idx])))
   record=dict(case_id=case['case_id'],cluster=case['cluster'],category=case['category'],case_type=case['case_type'],stratum=case['baseline_stratum'],condition=cond,rotation=rot,layer=cfg[0],dose=cfg[1],arm=cfg[2],p_unknown=float(p[order.index('알 수 없음')]),p_biased=float(p[biased_idx]),p_anti=float(p[anti_idx]),p_person_bias=q,p_correct=float(p[order.index(case['answer'])]),choice_mass=r['mass'],hook_error=r['hook_error'],prefix_probability_error=ep,full_source_reproduction_error=reproduction)
   for l in layers:
    for axis in axes:
     delta=r['states'][l].astype(float)-centers[l,axis];record[f'L{l}_{axis}']=float(delta@vectors[l,axis]/np.linalg.norm(delta))
   if cfg[2]!='sham':record['dose_hidden_norm_ratio']=float(cfg[1]*scales[cfg[0]]/np.linalg.norm(r['states'][cfg[0]]))
   assert np.isfinite(list(p)).all() and 0<=q<=1
   db.execute('insert into trials values(?,?,?,?,?,?,?)',(*key,json.dumps(record,ensure_ascii=False)));done.add(key);count+=1
  db.commit();save('prefix_equivalence.json',dict(checked_inputs=len(prefix_checks),max_probability_error=max_prob_error,max_logit_error=max_logit_error,max_full_source_error=max_sham_error,checks=prefix_checks))
  state=dict(state='complete' if count==10560 else 'running',pid=os.getpid(),completed=count,planned=10560,inputs_done=input_index+1,total_inputs=192,elapsed_seconds=time.time()-start,new_trials_per_minute=(count-initial)*60/max(1,time.time()-start),actual_model_calls=calls);save('status.json',state);print(json.dumps(state),flush=True)
  del prefix,enc,baseline,cached_base
 for handle in handles:handle.remove()
 db.close()
 if count==10560:(ROOT/'DONE').write_text('Frozen grid complete.\n')

if __name__=='__main__':main()
