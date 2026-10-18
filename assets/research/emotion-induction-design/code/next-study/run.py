"""Explicit opt-in runner. Import and --help never load a model."""
from pathlib import Path
import argparse,ast,fcntl,hashlib,itertools,json,time
import numpy as np
import pandas as pd
B=Path(__file__).resolve().parent


def messages(row,condition,rotation,stimuli):
    choices=ast.literal_eval(row['choices']);choices=choices[rotation:]+choices[:rotation]
    user='\n'.join(['다음 질문에 답하세요. 반드시 선택지 번호 하나만 숫자로 답하세요.','',row['context'],row['question']]+[f'{i+1}: {c}' for i,c in enumerate(choices)])
    return [{'role':'system','content':stimuli[condition]['system']},{'role':'user','content':user}],choices


def validate_inputs():
    plan=json.loads((B/'plan.json').read_text());s=json.loads((B/'stimuli.json').read_text());items=pd.read_csv(B/'items_2000.csv')
    assert len(s)==24 and len(set(x['system'] for x in s.values()))==24
    assert items.sample_id.is_unique and len(items)==2000
    for filename,digest in plan['input_sha256'].items():assert hashlib.sha256((B/filename).read_bytes()).hexdigest()==digest
    for _,row in items.iterrows():
        choices=ast.literal_eval(row['choices']);assert len(choices)==3 and len(set(choices))==3 and '알 수 없음' in choices and row.biased_answer in choices
        for r in range(3):assert set(messages(row,next(iter(s)),r,s)[1])==set(choices)
    return plan,s,items


def run(n):
    plan,stimuli,items=validate_inputs();items=items.iloc[:n]
    out=B/'results';out.mkdir(exist_ok=True)
    with (B/'writer.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
        manifest={'plan_sha256':sha(B/'plan.json'),'stimuli_sha256':sha(B/'stimuli.json'),'items_sha256':sha(B/'items_2000.csv'),'runner_sha256':sha(Path(__file__))}
        mp=out/'manifest.json'
        if mp.exists():assert json.loads(mp.read_text())==manifest
        else:mp.write_text(json.dumps(manifest,indent=2))
        csv=out/'trials.csv';done=set()
        if csv.exists():
            d=pd.read_csv(csv);assert not d.duplicated(['item','condition','rotation']).any();done=set(map(tuple,d[['item','condition','rotation']].values))
        import torch
        from transformers import AutoTokenizer,AutoModelForCausalLM
        torch.set_num_threads(4)
        tok=AutoTokenizer.from_pretrained(plan['model'],revision=plan['revision'],local_files_only=True)
        model=AutoModelForCausalLM.from_pretrained(plan['model'],revision=plan['revision'],local_files_only=True,dtype=torch.float32,attn_implementation='eager').to('mps').eval()
        assert model.config._commit_hash==plan['revision']
        ids=[tok.encode(str(k),add_special_tokens=False) for k in [1,2,3]];assert all(len(x)==1 for x in ids);ids=[x[0] for x in ids]
        order=list(itertools.product(stimuli,range(3)));rng=np.random.default_rng(plan['seed'])
        for _,row in items.iterrows():
            for j in rng.permutation(len(order)):
                c,r=order[j];key=(row.sample_id,c,r)
                if key in done:continue
                msg,choices=messages(row,c,r,stimuli);text=tok.apply_chat_template(msg,tokenize=False,add_generation_prompt=True)
                encoded=tok(text,return_tensors='pt').to('mps')
                with torch.inference_mode():logits=model(**encoded,use_cache=False,logits_to_keep=1).logits[0,-1].float()
                assert torch.isfinite(logits).all()
                selected=logits[ids];p=torch.softmax(selected,0).cpu().numpy();pm=dict(zip(choices,map(float,p)))
                anti=next(x for x in choices if x not in ['알 수 없음',row.biased_answer]);lse=float(torch.logsumexp(logits,0))
                record={'item':row.sample_id,'condition':c,'rotation':r,'outcome':stimuli[c]['outcome'],'emotion':stimuli[c]['emotion'],'variant':stimuli[c]['variant'],'p_unknown':pm['알 수 없음'],'p_stereotype':pm[row.biased_answer],'p_anti':pm[anti],'choice_mass':float(torch.exp(torch.logsumexp(selected,0)-lse)),'logit_1':float(selected[0]),'logit_2':float(selected[1]),'logit_3':float(selected[2]),'full_logsumexp':lse,'prompt_sha256':hashlib.sha256(text.encode()).hexdigest()}
                assert abs(sum(record[k] for k in ['p_unknown','p_stereotype','p_anti'])-1)<1e-5
                pd.DataFrame([record]).to_csv(csv,mode='a',header=not csv.exists(),index=False);done.add(key)
                temp=out/'status.tmp';temp.write_text(json.dumps({'state':'running','completed_rows':len(done),'target_rows':n*72,'time':time.time()}));temp.replace(out/'status.json')
        (out/'status.json').write_text(json.dumps({'state':'complete','items':n,'rows':n*72}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--execute',action='store_true');parser.add_argument('--max-items',type=int,choices=[139,500,1000,2000],default=139)
    args=parser.parse_args()
    if args.execute:run(args.max_items)
    else:
        p,s,i=validate_inputs();print(f'Prepared only: {len(s)} conditions; {len(i)} items available; no model inference.')
