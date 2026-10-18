"""Collect per-position hidden states for four unchanged prompts. No generation."""
from pathlib import Path
import fcntl, hashlib, json, os, time
import numpy as np

BASE=Path(__file__).resolve().parent
DATA=BASE.parent/'results/d335ad178e3c'
SOURCE=BASE.parent.parent/'results/a8e92be4014f/manifest.json'
MODEL='Qwen/Qwen2.5-7B-Instruct'
REVISION='a09a35458c702b33eeacc393d103063234e8bc28'
LAYERS=[14,21,28]
AXES=['UN','FA','calm','sadness','anger','desperation','joy']

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,value):
    t=p.with_suffix('.tmp');t.write_text(json.dumps(value,ensure_ascii=False,indent=2));os.replace(t,p)

def run():
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    out=BASE/'output';out.mkdir(exist_ok=True)
    cfg={'model':MODEL,'revision':REVISION,'layers':LAYERS,'dtype':'float32','attention':'eager','prompt_source_sha256':sha(SOURCE),'axis_sha256':{str(l):sha(DATA/f'axes_qwen_L{l}.npz') for l in LAYERS},'code_sha256':sha(__file__),'reading':'causal prefix hidden state at each token, no output generation','causal_attribution':False,'character_mapping':'mean over tokens overlapping a Unicode character; byte-piece overlaps are averaged','axis_caveat':'Axes calibrated at assistant start; per-input-token use is exploratory and position sensitive.'}
    mf=out/'manifest.json'
    if mf.exists():assert json.loads(mf.read_text())==cfg,'Configuration changed; preserve the existing measurement.'
    else:write(mf,cfg)
    source=json.loads(SOURCE.read_text())
    targets={k.replace('U','UN').replace('T','FA'):source['system']+'\n\n'+v for k,v in source['stimuli'].items()}
    tok=AutoTokenizer.from_pretrained(MODEL,revision=REVISION,local_files_only=True)
    missing=[c for c in targets if not (out/f'{c}.npz').exists()]
    if missing:
        device='mps' if torch.backends.mps.is_available() else 'cpu'
        write(out/'status.json',{'state':'loading','completed':4-len(missing),'total':4,'time':time.time()})
        import transformers.modeling_utils as mu
        warmup=mu.caching_allocator_warmup
        if device=='mps':mu.caching_allocator_warmup=lambda *a,**kw:None
        try:
            model=AutoModelForCausalLM.from_pretrained(MODEL,revision=REVISION,dtype=torch.float32,attn_implementation='eager',local_files_only=True,device_map={'':device},low_cpu_mem_usage=True).eval()
        finally:mu.caching_allocator_warmup=warmup
        for c in missing:
            content=targets[c]
            chat=tok.apply_chat_template([{'role':'system','content':content}],tokenize=False,add_generation_prompt=True)
            enc=tok(chat,return_tensors='pt',return_offsets_mapping=True,add_special_tokens=False)
            offsets=enc.pop('offset_mapping')[0].numpy();ids=enc['input_ids'][0].numpy()
            enc={k:v.to(device) for k,v in enc.items()}
            with torch.inference_mode():
                result=model(**enc,output_hidden_states=True,use_cache=False,logits_to_keep=1)
                hidden=np.stack([result.hidden_states[l][0].float().cpu().numpy().copy() for l in LAYERS])
            assert np.isfinite(hidden).all()
            cached=np.load(DATA/'hidden'/f'{c}.npy')
            parity=float(np.abs(hidden[:,-1]-cached).max())
            np.savez_compressed(out/f'{c}.npz',hidden=hidden,offsets=offsets,ids=ids)
            write(out/f'{c}.json',{'condition':c,'content':content,'chat':chat,'content_start':chat.index(content),'token_count':len(ids),'cached_assistant_start_max_abs_difference':parity})
            del result,hidden
            write(out/'status.json',{'state':'measuring','completed':sum((out/f'{k}.npz').exists() for k in targets),'total':4,'last':c,'time':time.time()})
            print(c,'saved; cached last-position difference',parity,flush=True)
        del model
        if device=='mps':torch.mps.empty_cache()
    import pandas as pd
    rows=[];payload=[]
    for c,content in targets.items():
        array=np.load(out/f'{c}.npz');meta=json.loads((out/f'{c}.json').read_text());h=array['hidden'];offsets=array['offsets'];ids=array['ids']
        entry={'condition':c,'text':content,'layers':{},'assistant_start':{}}
        for li,l in enumerate(LAYERS):
            axes=np.load(DATA/f'axes_qwen_L{l}.npz');direction=axes['directions'];center=axes['centers'];scale=axes['scales']
            diff=h[li,:,None,:]-center[None,:,:]
            projection=np.einsum('tad,ad->ta',diff,direction)
            norms=np.linalg.norm(diff,axis=2)
            cosine=projection/np.maximum(norms,1e-12);z=projection/scale
            assert np.isfinite(cosine).all() and (np.abs(cosine)<=1.00001).all()
            characters=[]
            for i,ch in enumerate(content):
                absolute=meta['content_start']+i
                matches=np.flatnonzero((offsets[:,0]<=absolute)&(offsets[:,1]>absolute))
                assert len(matches)>0,(c,i,ch)
                characters.append({'char':ch,'tokens':matches.tolist(),'cosine':cosine[matches].mean(axis=0).tolist(),'z':z[matches].mean(axis=0).tolist()})
            entry['layers'][str(l)]=characters
            entry['assistant_start'][str(l)]={'cosine':cosine[-1].tolist(),'z':z[-1].tolist()}
            for t,((start,end),token_id) in enumerate(zip(offsets,ids)):
                for ai,axis in enumerate(AXES):rows.append({'condition':c,'layer':l,'token_index':t,'token_id':int(token_id),'chat_start':int(start),'chat_end':int(end),'token_text':tok.decode([int(token_id)]),'axis':axis,'cosine':float(cosine[t,ai]),'standardized_projection':float(z[t,ai])})
        payload.append(entry)
    pd.DataFrame(rows).to_csv(out/'token_scores.csv',index=False)
    write(out/'highlights.json',{'axes':AXES,'prompts':payload,'metric':'centered cosine similarity; not causal attribution or emotion probability','notes':cfg['axis_caveat']})
    write(out/'status.json',{'state':'complete','completed':4,'total':4,'time':time.time(),'rows':len(rows)})
    return out

if __name__=='__main__':
    lock=open(BASE/'writer.lock','w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    print(run(),flush=True)
