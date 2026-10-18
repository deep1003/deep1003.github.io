"""Frozen-item, frozen-prompt internal measurements. No generated answers."""
from pathlib import Path
import ast, fcntl, hashlib, itertools, json, os, time
import numpy as np
import pandas as pd

BASE=Path(__file__).resolve().parent
ROOT=BASE.parent.parent
SOURCE=ROOT/'results/a8e92be4014f'
ITEMS=ROOT.parent/'threat_139_pilot/items_139.csv'
AXIS_DATA=BASE.parent/'results/d335ad178e3c'
MODEL='Qwen/Qwen2.5-7B-Instruct'
REVISION='a09a35458c702b33eeacc393d103063234e8bc28'
LAYERS=[14,21,28]
AXES=['UN','FA','calm','sadness','anger','desperation','joy']
CONDITIONS=['U0T0','U1T0','U0T1','U1T1']

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,obj):
    t=p.with_suffix('.tmp');t.write_text(json.dumps(obj,indent=2,ensure_ascii=False));os.replace(t,p)

def message(row,c,rotation,source):
    choices=ast.literal_eval(row['choices']);choices=choices[rotation:]+choices[:rotation]
    body='\n'.join(['다음 질문에 답하세요. 반드시 선택지 번호 하나만 숫자로 답하세요.','',row['context'],row['question']]+[f'{i+1}: {v}' for i,v in enumerate(choices)])
    return [{'role':'system','content':source['system']+'\n\n'+source['stimuli'][c]},{'role':'user','content':body}],choices

def run():
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    out=BASE/'output';out.mkdir(exist_ok=True);chunks=out/'chunks';chunks.mkdir(exist_ok=True)
    items=pd.read_csv(ITEMS);source=json.loads((SOURCE/'manifest.json').read_text())
    assert len(items)==139 and items.sample_id.is_unique and sha(ITEMS)==source['items_sha256']
    cfg={'model':MODEL,'revision':REVISION,'dtype':'float32','attention':'eager','layers':LAYERS,'primary_layer':14,'n_items':139,'n_conditions':4,'rotations':[0,1,2],'items_sha256':sha(ITEMS),'prompt_source_sha256':sha(SOURCE/'manifest.json'),'original_trials_sha256':sha(SOURCE/'trials.csv'),'code_sha256':sha(__file__),'axes_sha256':{str(l):sha(AXIS_DATA/f'axes_qwen_L{l}.npz') for l in LAYERS},'position':'last assistant-start token, full original system+KoBBQ user input; no generation','padding_smoke':'before collection compare mixed-length left-padded batch with singles: hidden max error <= .02 and choice-probability max error <= .02; otherwise use batch 1','primary_coordinates':'mean across three choice rotations of centered cosine to frozen UN and FA directions; no PCA or refitting','primary_figures':['absolute cosine similarity in UN1FA1','within-item change UN1FA1 minus UN0FA0'],'category_aggregation':'item-weighted means; category is nominal, no numeric-category Pearson correlation','inference':'exploratory/descriptive, selected reused items; no category significance claims','limits':'Axes validated on assistant-start system-only narrative contrasts; transfer to full KoBBQ context unvalidated; UN/FA directions correlated; projections do not establish emotion or causality.'}
    mf=out/'manifest.json'
    if mf.exists():assert json.loads(mf.read_text())==cfg,'Do not overwrite an incompatible measurement.'
    else:write(mf,cfg)
    expected=set(itertools.product(items.sample_id,CONDITIONS,range(3)))
    saved=[]
    for f in sorted(chunks.glob('batch_*.npz')):
        a=np.load(f);saved.extend(map(tuple,a['keys'].tolist()))
    assert len(saved)==len(set(saved)) and set(saved)<=expected
    missing=sorted(expected-set(saved));total=len(expected)
    if not missing:return analyze(out,items)
    write(out/'status.json',{'state':'loading','completed':len(saved),'total':total,'time':time.time()})
    tok=AutoTokenizer.from_pretrained(MODEL,revision=REVISION,local_files_only=True,padding_side='left')
    if tok.pad_token_id is None:tok.pad_token=tok.eos_token
    device='mps' if torch.backends.mps.is_available() else 'cpu'
    import transformers.modeling_utils as mu
    warmup=mu.caching_allocator_warmup
    if device=='mps':mu.caching_allocator_warmup=lambda *a,**kw:None
    try:model=AutoModelForCausalLM.from_pretrained(MODEL,revision=REVISION,dtype=torch.float32,attn_implementation='eager',local_files_only=True,device_map={'':device},low_cpu_mem_usage=True).eval()
    finally:mu.caching_allocator_warmup=warmup
    choice_ids=[tok.encode(str(i),add_special_tokens=False)[0] for i in [1,2,3]]
    lookup=items.set_index('sample_id')
    def text_for(key):
        item,c,r=key;msg,choices=message(lookup.loc[item],c,int(r),source)
        return tok.apply_chat_template(msg,tokenize=False,add_generation_prompt=True),choices
    def forward(keys):
        inputs=[text_for(k) for k in keys]
        enc=tok([x[0] for x in inputs],padding=True,return_tensors='pt',add_special_tokens=False)
        position=enc.attention_mask.long().cumsum(-1)-1;position.masked_fill_(enc.attention_mask==0,0)
        enc={k:v.to(device) for k,v in enc.items()}
        with torch.inference_mode():
            result=model(**enc,position_ids=position.to(device),output_hidden_states=True,use_cache=False,logits_to_keep=1)
            h=np.stack([result.hidden_states[l][:,-1].float().cpu().numpy().copy() for l in LAYERS],axis=1)
            probs=torch.softmax(result.logits[:,-1,choice_ids].float(),dim=-1).cpu().numpy()
        unknown=np.array([probs[i,choices.index('알 수 없음')] for i,(_,choices) in enumerate(inputs)])
        del result
        assert np.isfinite(h).all() and np.isfinite(probs).all()
        return h,unknown
    lengths=[len(tok.encode(text_for(k)[0])) for k in missing]
    smoke_keys=[missing[int(np.argmin(lengths))],missing[int(np.argmax(lengths))]]
    single=[forward([k]) for k in smoke_keys];batched=forward(smoke_keys)
    hdiff=float(np.max(np.abs(np.concatenate([v[0] for v in single])-batched[0])))
    pdiff=float(np.max(np.abs(np.concatenate([v[1] for v in single])-batched[1])))
    batch=4 if hdiff<=.02 and pdiff<=.02 else 1
    write(out/'smoke.json',{'hidden_max_abs_error':hdiff,'choice_probability_max_abs_error':pdiff,'batch_size':batch,'graphics_emitted':False,'keys':smoke_keys})
    print('Smoke:',hdiff,pdiff,'batch',batch,flush=True)
    # Length-sort improves padding efficiency; original identities remain in every record.
    plan=[missing[i] for i in np.argsort(lengths,kind='stable')]
    start=time.time();completed=len(saved);batch_index=len(list(chunks.glob('batch_*.npz')))
    for offset in range(0,len(plan),batch):
        keys=plan[offset:offset+batch];h,p=forward(keys)
        keyarr=np.array([[str(i),str(c),str(r)] for i,c,r in keys])
        tmp=chunks/f'batch_{batch_index:05d}.tmp.npz';target=chunks/f'batch_{batch_index:05d}.npz'
        np.savez_compressed(tmp,keys=keyarr,hidden=h,p_unknown=p);os.replace(tmp,target)
        completed+=len(keys);batch_index+=1
        write(out/'status.json',{'state':'measuring','completed':completed,'total':total,'elapsed_sec':time.time()-start,'batch_size':batch,'time':time.time()})
        if batch_index%20==0 or completed==total:print(f'{completed}/{total}; {time.time()-start:.1f}s',flush=True)
    del model
    if device=='mps':torch.mps.empty_cache()
    return analyze(out,items)

def analyze(out,items=None):
    out=Path(out);items=pd.read_csv(ITEMS) if items is None else items
    axes={l:np.load(AXIS_DATA/f'axes_qwen_L{l}.npz') for l in LAYERS};rows=[]
    for f in sorted((out/'chunks').glob('batch_*.npz')):
        a=np.load(f)
        for j,(item,c,r) in enumerate(a['keys']):
            for li,l in enumerate(LAYERS):
                x=axes[l];diff=a['hidden'][j,li][None,:]-x['centers'];proj=np.einsum('ad,ad->a',diff,x['directions']);cos=proj/np.linalg.norm(diff,axis=1)
                row={'item':item,'condition':c.replace('U','UN').replace('T','FA'),'rotation':int(r),'layer':l,'remeasured_p_unknown':float(a['p_unknown'][j])}
                row.update({f'cos_{axis}':float(v) for axis,v in zip(AXES,cos)});row.update({f'z_{axis}':float(v) for axis,v in zip(AXES,proj/x['scales'])});rows.append(row)
    d=pd.DataFrame(rows);keys=['item','condition','rotation','layer'];assert not d.duplicated(keys).any()
    assert len(d)==139*4*3*3 and np.isfinite(d.filter(regex='^(cos_|z_)').values).all()
    d=d.merge(items[['sample_id','category','cluster']],left_on='item',right_on='sample_id',how='left',validate='many_to_one').drop(columns='sample_id');assert d.category.notna().all()
    original=pd.read_csv(SOURCE/'trials.csv');original.condition=original.condition.str.replace('U','UN').str.replace('T','FA')
    parity=d[d.layer==14].merge(original,on=['item','condition','rotation'],validate='one_to_one');pdiff=(parity.remeasured_p_unknown-parity.p_unknown).abs()
    d.to_csv(out/'trial_alignment.csv',index=False)
    measures=[f'{kind}_{axis}' for kind in ['cos','z'] for axis in AXES]
    means=d.groupby(['item','category','cluster','condition','layer'],as_index=False)[measures].mean();means.to_csv(out/'item_alignment.csv',index=False)
    base=means[means.condition=='UN0FA0'].set_index(['item','layer'])
    changes=[]
    for row in means.itertuples(index=False):
        b=base.loc[(row.item,row.layer)];record={'item':row.item,'category':row.category,'cluster':row.cluster,'condition':row.condition,'layer':row.layer}
        record.update({f'delta_{k}':getattr(row,k)-b[k] for k in measures});changes.append(record)
    pd.DataFrame(changes).to_csv(out/'item_changes.csv',index=False)
    behavior=original.groupby(['item','condition'],as_index=False).p_unknown.mean()
    means.merge(behavior,on=['item','condition'],validate='many_to_one').to_csv(out/'alignment_and_behavior.csv',index=False)
    report={'n_items':139,'n_categories':int(items.category.nunique()),'n_templates':int(items.cluster.nunique()),'n_trials':1668,'n_layer_records':len(d),'keys_duplicated':0,'finite':True,'original_behavior_parity_max_abs':float(pdiff.max()),'original_behavior_parity_mean_abs':float(pdiff.mean()),'source_trials_unchanged':sha(SOURCE/'trials.csv')==json.loads((out/'manifest.json').read_text())['original_trials_sha256'],'category_counts':items.category.value_counts().to_dict()}
    assert report['source_trials_unchanged']
    write(out/'validation.json',report);write(out/'status.json',{'state':'complete','completed':1668,'total':1668,'time':time.time()})
    return out

if __name__=='__main__':
    lock=open(BASE/'writer.lock','w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    print(run(),flush=True)
