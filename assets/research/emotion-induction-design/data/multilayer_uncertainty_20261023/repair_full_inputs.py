"""Fail-closed numeric repair: whole inputs, not outcome-selected individual arms."""
from pathlib import Path
import json,sqlite3,time
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parent

def main():
 d=pd.read_csv(ROOT/'trials.csv');old=pd.read_csv(ROOT/'legacy_reference576.csv');keys=['case_id','condition','rotation','arm'];x=d[(d.layer==14)&(d.dose==1)&d.arm.isin(['Anxiety+','Anxiety-','Desperation+','Desperation-'])].merge(old,on=keys,suffixes=('_new','_old'));x['error']=np.max(np.abs(x[['p_unknown_new','p_biased_new','p_correct_new']].to_numpy()-x[['p_unknown_old','p_biased_old','p_correct_old']].to_numpy()),axis=1);bad=x[x.error>2e-5];inputs=bad[['case_id','condition','rotation']].drop_duplicates().to_dict('records');assert len(inputs)==3
 c=sqlite3.connect(ROOT/'measurements.sqlite');backup_path=ROOT.parent.parent/'work/multilayer_uncertainty_20261023/measurements_pre_repair.sqlite';backup=sqlite3.connect(backup_path);c.backup(backup);backup.close()
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 import transformers.modeling_utils as mu
 mu.caching_allocator_warmup=lambda *a,**k:None;torch.set_num_threads(4)
 plan=json.loads((ROOT/'DESIGN_FROZEN.json').read_text());frozen=json.loads((ROOT/'prompts_v5.json').read_text());cases={x['case_id']:x for x in json.loads((ROOT/'cases.json').read_text())};vec=np.load(ROOT/'layer_vectors.npz');layers=plan['layers'];axes=plan['axes'];scale=dict(zip(vec['layers'],vec['base_alpha']));prompts={x['condition']:x['system_content'] for x in frozen['conditions']}
 tok=AutoTokenizer.from_pretrained(plan['model'],revision=plan['revision'],local_files_only=True);model=AutoModelForCausalLM.from_pretrained(plan['model'],revision=plan['revision'],dtype=torch.float32,device_map='mps',attn_implementation='eager',local_files_only=True).eval();ids=[16,17,18];current={'layer':None,'vector':None};capture={}
 def make_hook(layer):
  def hook(module,args,output):
   if current['layer']!=layer:return output
   is_tuple=isinstance(output,tuple);h=(output[0] if is_tuple else output).clone();before=h[:,-1].detach().clone();h[:,-1]+=current['vector'];capture['before']=before.cpu().numpy()[0];capture['after']=h[:,-1].detach().cpu().numpy()[0]
   return (h,)+output[1:] if is_tuple else h
  return hook
 handles=[model.model.layers[l-1].register_forward_hook(make_hook(l),prepend=True) for l in layers]
 cfgs=[(0,0.,'sham')]+[(l,d,a+s) for l in layers for d in plan['dose_multipliers'] for a in axes+['Random'] for s in ['+','-']];completed=0;start=time.time()
 for inp in inputs:
  cid,cond,rot=inp['case_id'],inp['condition'],int(inp['rotation']);case=cases[cid];order=case['choices'][rot:]+case['choices'][:rot];user=frozen['user_template'].format(context=case['context'],question=case['question'],o1=order[0],o2=order[1],o3=order[2]);text=tok.apply_chat_template([{'role':'system','content':prompts[cond]},{'role':'user','content':user}],tokenize=False,add_generation_prompt=True);enc=tok(text,return_tensors='pt').to('mps');records=[]
  for layer,dose,arm in cfgs:
   current['layer']=None if arm=='sham' else layer;current['vector']=None if arm=='sham' else torch.tensor((1 if arm[-1]=='+' else -1)*dose*scale[layer]*vec[f'L{layer}_{arm[:-1]}'],dtype=torch.float32,device='mps')
   with torch.inference_mode():out=model(**enc,use_cache=False,output_hidden_states=True,logits_to_keep=1)
   lg=out.logits[0,-1].float().cpu().double().numpy();lg3=lg[ids];p=np.exp(lg3-lg3.max());p/=p.sum();mass=float(np.exp(np.logaddexp.reduce(lg3)-np.logaddexp.reduce(lg)));r=json.loads(c.execute('select record from trials where case_id=? and condition=? and rotation=? and layer=? and dose=? and arm=?',(cid,cond,rot,layer,dose,arm)).fetchone()[0]);anti=next(z for z in order if z not in ['알 수 없음',case['biased_answer']]);b=order.index(case['biased_answer']);a=order.index(anti)
   r.update(p_unknown=float(p[order.index('알 수 없음')]),p_biased=float(p[b]),p_anti=float(p[a]),p_person_bias=float(np.exp(lg3[b]-np.logaddexp(lg3[b],lg3[a]))),p_correct=float(p[order.index(case['answer'])]),choice_mass=mass,prefix_probability_error=0.,inference_method='full_repair',hook_error=0.)
   for l in layers:
    h=out.hidden_states[l][0,-1].float().cpu().numpy()
    for axis in axes:
     delta=h.astype(float)-vec[f'L{l}_{axis}_center'];r[f'L{l}_{axis}']=float(delta@vec[f'L{l}_{axis}']/np.linalg.norm(delta))
    if l==layer and arm!='sham':
     assert np.max(np.abs(h-capture['after']))<1e-6;r['hook_error']=float(np.max(np.abs((capture['after']-capture['before'])-current['vector'].cpu().numpy())));assert r['hook_error']<1e-5;r['dose_hidden_norm_ratio']=float(dose*scale[layer]/np.linalg.norm(h))
   assert np.isfinite(p).all();records.append((json.dumps(r,ensure_ascii=False),cid,cond,rot,layer,dose,arm));completed+=1;del out
  c.executemany('update trials set record=? where case_id=? and condition=? and rotation=? and layer=? and dose=? and arm=?',records);c.commit();print(json.dumps(dict(repaired_records=completed,total=165,elapsed_seconds=time.time()-start)),flush=True)
 for h in handles:h.remove()
 c.close();(ROOT/'numeric_repair.json').write_text(json.dumps({'trigger':'4/576 previous-run comparisons exceeded2e-5 before outcome analysis','max_original_probability_difference':float(bad.error.max()),'inputs':inputs,'repaired_records':165,'method':'Remeasure all55 settings for each of3 affected inputs with unchanged FP32 full forward. No individual outcome or p value selection; original DB backed up.','numeric_tolerance_unchanged':2e-5,'scientific_design_unchanged':True},indent=2))

if __name__=='__main__':main()
