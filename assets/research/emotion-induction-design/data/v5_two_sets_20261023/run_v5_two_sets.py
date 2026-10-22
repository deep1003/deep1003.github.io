"""Run the frozen v5 on both supplied KoBBQ sets, with durable checkpoints.

No images, plots, website edits, or model generation. The final-token logits
optimization must pass equivalence checks against full-logit inference.
"""
from __future__ import annotations

import argparse
import ast
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import sqlite3
import time
from zoneinfo import ZoneInfo

import numpy as np

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent.parent
REFERENCE = ROOT.parent / 'prompt_service_ops_20261022'
MODEL = 'Qwen/Qwen2.5-7B-Instruct'
REVISION = 'a09a35458c702b33eeacc393d103063234e8bc28'
CONDITIONS = ['R', 'UN0', 'UN1', 'CN0', 'CN1']
FILES = ['kobbq_raw_sampling_set01_seed36.json', 'kobbq_raw_sampling_set02_seed42.json']
SEED, N_BOOT, LAYER = 20261022, 2000, 14


def now():
    return datetime.now(ZoneInfo('Asia/Seoul')).isoformat()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, data):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    temporary.replace(path)


def write_csv(path, rows):
    if not rows:
        return
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def log(message):
    line = now() + ' ' + message
    print(line, flush=True)
    with (ROOT/'progress.log').open('a', encoding='utf-8') as handle:
        handle.write(line+'\n')


def status(**updates):
    path = ROOT/'status.json'
    current = json.loads(path.read_text()) if path.exists() else {}
    current.update(updates, updated_kst=now())
    write_json(path, current)


def prepare():
    import pandas as pd
    source = ROOT/'source'
    source.mkdir(exist_ok=True)
    for name in FILES:
        destination = source/name
        if not destination.exists():
            shutil.copy2(WORKSPACE/name, destination)
        assert sha(destination) == sha(WORKSPACE/name)
    axis_destination = source/'axes_L14.npz'
    if not axis_destination.exists():
        shutil.copy2(REFERENCE/'source/axes_L14.npz', axis_destination)
    original = json.loads((REFERENCE/'prompts.json').read_text())
    prompts = [r for r in original['conditions'] if r['version']=='v5_reference']
    assert [p['condition'] for p in prompts] == CONDITIONS
    for prompt in prompts:
        assert hashlib.sha256(prompt['system_content'].encode()).hexdigest() == prompt['system_sha256']
    frozen = {'version':'v5', 'condition_order':CONDITIONS,
              'common_header':original['common_header'], 'user_template':original['user_template'],
              'conditions':[dict(p, version='v5') for p in prompts]}
    write_json(ROOT/'prompts_v5.json', frozen)

    official = pd.read_parquet(source/'kobbq-all-test.parquet').set_index('sample_id')
    cases, memberships, set_info = {}, [], []
    expression = re.compile(r'맥락: (.*?)\n질문: (.*?)\nA: (.*?)\nB: (.*?)\nC: (.*?)\n정답:', re.S)
    for set_index, filename in enumerate(FILES, 1):
        raw = json.loads((source/filename).read_text())
        set_id = f'set{set_index:02d}'
        assert len(raw['data']) == 720
        local_ids = set()
        for row_index, row in enumerate(raw['data']):
            assert len(row)==6 and row[4] in 'ABC'
            match = expression.fullmatch(row[0])
            assert match, (filename, row_index)
            context, question, *choices = match.groups()
            assert choices==row[1:4]
            case_id, encoded_rotation = row[5].rsplit('-',1)
            meta = official.loc[case_id]
            assert context == meta.context and question == meta.question
            assert sorted(choices) == sorted(ast.literal_eval(meta.choices))
            assert choices['ABC'.index(row[4])] == meta.answer
            assert len(set(choices)) == 3 and '알 수 없음' in choices
            category, template = case_id.split('-')[:2]
            cluster = category+'-'+re.match(r'\d+', template).group()
            case_type = 'amb' if '-amb-' in case_id else 'dis'
            entry = {'case_id':case_id, 'context':context, 'question':question,
                     'choices':choices, 'answer':meta.answer, 'biased_answer':meta.biased_answer,
                     'category':category, 'cluster':cluster, 'case_type':case_type}
            if case_id not in cases:
                cases[case_id] = entry
            else:
                previous = cases[case_id]
                assert all(previous[k]==entry[k] for k in ['context','question','answer','biased_answer'])
                assert any(choices == previous['choices'][r:]+previous['choices'][:r] for r in range(3))
            memberships.append({'set_id':set_id, 'source_row':row_index,
                                'raw_sample_id':row[5], 'case_id':case_id,
                                'encoded_rotation':int(encoded_rotation), 'choices':choices,
                                'answer_letter':row[4]})
            local_ids.add(case_id)
        set_info.append({'set_id':set_id,'filename':filename,'raw_rows':720,
                         'unique_cases':len(local_ids),
                         'amb_raw_rows':sum('-amb-' in r[5] for r in raw['data']),
                         'dis_raw_rows':sum('-dis-' in r[5] for r in raw['data']),
                         'unique_amb_cases':sum(cases[c]['case_type']=='amb' for c in local_ids),
                         'unique_dis_cases':sum(cases[c]['case_type']=='dis' for c in local_ids),
                         'template_clusters':len({cases[c]['cluster'] for c in local_ids})})
    cases = list(cases.values())
    assert len(cases)==1076
    write_json(ROOT/'cases.json', cases)
    write_json(ROOT/'memberships.json', memberships)
    for info in set_info:
        set_dir = ROOT/info['set_id']
        set_dir.mkdir(exist_ok=True)
        member_ids = {m['case_id'] for m in memberships if m['set_id']==info['set_id']}
        write_json(set_dir/'unique_cases.json', [c for c in cases if c['case_id'] in member_ids])
    write_json(ROOT/'manifest.json', {
        'created_kst':now(),'prompt_version':'v5','model':MODEL,'revision':REVISION,
        'dtype':'float32','device':'mps','attention':'eager','batch_size':1,'layer':LAYER,
        'condition_order':CONDITIONS,'rotations':3,'seed':SEED,'bootstrap_replicates':N_BOOT,
        'input_files':set_info,'unique_cases_combined':len(cases),
        'overlap_between_sets':199,'planned_unique_forward_passes':len(cases)*15,
        'raw_row_mapped_results_per_set':720*15,
        'primary_unit':'unique case averaged over three cyclic option orders; cluster bootstrap by category/template',
        'secondary_unit':'all 720 source rows preserved; row-weighted descriptive results only',
        'ambiguity_handling':'amb and dis analysed separately; p_unknown is a probability, not necessarily a correct answer on dis items',
        'prefix_handling':'ABC source prefix is input data; rendered context/question/choices are validated then inserted into frozen v5 numeric user template',
        'text_preservation':'No spelling, control-character, or whitespace cleanup within context/question/choices.',
        'label_source':'https://huggingface.co/datasets/naver-ai/kobbq/blob/main/data/kobbq-all-test.parquet',
        'metadata_validation':'All 1440 raw rows matched official ID, context, question, choice set, rendered choices and gold answer.',
        'source_hashes':{p.name:sha(p) for p in source.iterdir() if p.is_file()},
        'prompts_sha256':sha(ROOT/'prompts_v5.json'),
        'reporting':'R=0 within each set and ambiguity stratum',
        'limitations':['Sets overlap and are not independent replications.',
                       'Fixed v5 prompts; no prompt selection during this run.',
                       'Axis projections do not establish subjective experience.']})
    status(state='prepared',planned=len(cases)*15,completed=0)
    return frozen,cases,memberships


def connect():
    connection = sqlite3.connect(ROOT/'measurements.sqlite', timeout=60)
    connection.execute('PRAGMA journal_mode=WAL')
    connection.execute('PRAGMA synchronous=NORMAL')
    connection.execute('CREATE TABLE IF NOT EXISTS measurements (case_id TEXT, condition TEXT, rotation INTEGER, record TEXT NOT NULL, hidden BLOB NOT NULL, PRIMARY KEY(case_id,condition,rotation))')
    return connection


def run(frozen,cases):
    import torch
    from transformers import AutoModelForCausalLM,AutoTokenizer
    import transformers.modeling_utils as modeling_utils
    modeling_utils.caching_allocator_warmup = lambda *args,**kwargs: None
    torch.manual_seed(SEED)
    torch.set_num_threads(4)
    axes=np.load(ROOT/'source/axes_L14.npz',allow_pickle=True)
    names=[str(n) for n in axes['names']]
    directions=axes['directions'].astype(float)
    directions/=np.linalg.norm(directions,axis=1,keepdims=True)
    centers=axes['centers'].astype(float)
    tokenizer=AutoTokenizer.from_pretrained(MODEL,revision=REVISION,local_files_only=True)
    prompts={p['condition']:p['system_content'] for p in frozen['conditions']}
    log('Loading one FP32 model; five v5 conditions shared across both sets.')
    status(state='loading_model')
    model=AutoModelForCausalLM.from_pretrained(MODEL,revision=REVISION,torch_dtype=torch.float32,
            attn_implementation='eager',device_map='mps',low_cpu_mem_usage=True,local_files_only=True).eval()
    ids=[tokenizer.convert_tokens_to_ids(str(i)) for i in [1,2,3]]
    assert ids==[16,17,18]

    def forward(system,user=None,keep=1):
        messages=[{'role':'system','content':system}]
        if user is not None:messages.append({'role':'user','content':user})
        text=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
        enc=tokenizer(text,return_tensors='pt').to('mps')
        with torch.no_grad():
            out=model(**enc,output_hidden_states=True,logits_to_keep=keep)
        logits=out.logits[0,-1].float().cpu().double().numpy()
        hidden=out.hidden_states[LAYER][0,-1].float().cpu().numpy()
        delta=hidden.astype(float)-centers
        cosine=(delta*directions).sum(1)/np.linalg.norm(delta,axis=1)
        three=logits[ids]
        p=np.exp(three-three.max());p/=p.sum()
        log_z=float(np.logaddexp.reduce(logits))
        mass=float(np.exp(three-log_z).sum())
        return p,hidden,cosine,len(enc['input_ids'][0]),three,log_z,mass

    # Fresh numerical smoke: equivalent forward implementations and prior v5 outputs.
    golden=list(csv.DictReader((REFERENCE/'t2_trials.csv').open(encoding='utf-8')))
    sample_items={r['sample_id']:r for r in csv.DictReader((REFERENCE/'source/sample_items_24.csv').open(encoding='utf-8'))}
    check_rows=[]
    for condition in CONDITIONS:
        row=next(r for r in golden if r['version']=='v5_reference' and r['condition']==condition and r['rotation']=='0')
        item=sample_items[row['item']]
        choices=ast.literal_eval(item['choices'])
        user=frozen['user_template'].format(context=item['context'],question=item['question'],o1=choices[0],o2=choices[1],o3=choices[2])
        old=forward(prompts[condition],user,keep=0)
        new=forward(prompts[condition],user,keep=1)
        logit_error=float(np.max(np.abs(old[4]-new[4])))
        probability_error=float(np.max(np.abs(old[0]-new[0])))
        hidden_error=float(np.max(np.abs(old[1]-new[1])))
        prior_logits=np.array([float(row['logit_'+str(i)]) for i in [1,2,3]])
        prior_error=float(np.max(np.abs(old[4]-prior_logits)))
        assert logit_error<=1e-4 and probability_error<=1e-5 and hidden_error<=1e-7
        assert prior_error<=1e-4,prior_error
        check_rows.append({'condition':condition,'full_vs_last_logit_max_error':logit_error,
                           'full_vs_last_probability_max_error':probability_error,
                           'hidden_max_error':hidden_error,'prior_v5_logit_max_error':prior_error})
    write_json(ROOT/'smoke_validation.json',{'status':'passed','checks':check_rows,
               'optimization':'retain logits only for final token; model, dtype, attention and batch unchanged'})
    t1=[]
    for condition in CONDITIONS:
        _,hidden,cosine,nt,_,_,_=forward(prompts[condition])
        t1.append({'condition':condition,'n_tokens':nt,**{f't1_{n}':float(v) for n,v in zip(names,cosine)}})
    write_csv(ROOT/'t1.csv',t1)
    reference_row=t1[0]
    write_csv(ROOT/'t1_R0.csv',[{'condition':r['condition'],**{n:r['t1_'+n]-reference_row['t1_'+n] for n in names}} for r in t1])
    log('Fresh smoke passed; exact v5 inputs and final-token optimization verified.')

    connection=connect()
    done=set(connection.execute('SELECT case_id,condition,rotation FROM measurements').fetchall())
    total=len(cases)*15
    count=len(done)
    start,initial=time.monotonic(),count
    status(state='running',completed=count,planned=total,smoke='passed',pid=__import__('os').getpid())
    for case in cases:
        choices=case['choices']
        anti=next(c for c in choices if c not in [case['biased_answer'],'알 수 없음'])
        for rotation in range(3):
            order=choices[rotation:]+choices[:rotation]
            user=frozen['user_template'].format(context=case['context'],question=case['question'],o1=order[0],o2=order[1],o3=order[2])
            for condition in CONDITIONS:
                key=(case['case_id'],condition,rotation)
                if key in done:continue
                p,hidden,cos,nt,lg,log_z,mass=forward(prompts[condition],user)
                record={'case_id':case['case_id'],'category':case['category'],'cluster':case['cluster'],
                        'case_type':case['case_type'],'condition':condition,'rotation':rotation,
                        'p_unknown':float(p[order.index('알 수 없음')]),
                        'p_biased':float(p[order.index(case['biased_answer'])]),
                        'p_anti':float(p[order.index(anti)]),'p_correct':float(p[order.index(case['answer'])]),
                        'correct_argmax':int(order[int(p.argmax())]==case['answer']),
                        'choice_mass':mass,'logit_1':float(lg[0]),'logit_2':float(lg[1]),'logit_3':float(lg[2]),
                        'full_logsumexp':log_z,'n_tokens':nt,'order':order,
                        **{f't2_{n}':float(v) for n,v in zip(names,cos)}}
                assert np.isfinite(p).all() and abs(p.sum()-1)<1e-12 and 0<=mass<=1+1e-10
                connection.execute('INSERT INTO measurements VALUES (?,?,?,?,?)',
                                   (*key,json.dumps(record,ensure_ascii=False),hidden.astype('float32').tobytes()))
                count+=1
                if count%25==0:connection.commit()
                if count%50==0 or count==total:
                    connection.commit()
                    elapsed=time.monotonic()-start
                    rate=elapsed/max(1,count-initial)
                    status(state='running',completed=count,planned=total,seconds_per_trial=rate,
                           eta_minutes=(total-count)*rate/60,last_case=case['case_id'])
                    log(f'{count}/{total}; {rate:.3f}s/trial; ETA {(total-count)*rate/60:.1f} min')
    connection.commit();connection.close()
    status(state='inference_complete',completed=total,planned=total)
    log('Inference complete; exporting both sets and calculating R=0 results.')


def analyse(cases,memberships):
    import pandas as pd
    connection=connect()
    records=[json.loads(r[0]) for r in connection.execute('SELECT record FROM measurements ORDER BY case_id,condition,rotation')]
    assert len(records)==len(cases)*15
    frame=pd.DataFrame(records)
    assert not frame.duplicated(['case_id','condition','rotation']).any()
    assert frame.groupby(['case_id','condition']).size().eq(3).all()
    assert np.isfinite(frame[['p_unknown','p_biased','p_anti','p_correct']].to_numpy()).all()
    assert np.allclose(frame[['p_unknown','p_biased','p_anti']].sum(1),1,atol=1e-12)
    write_csv(ROOT/'unique_trials.csv',records)
    lookup={(r['case_id'],r['condition'],r['rotation']):r for r in records}
    case_lookup={c['case_id']:c for c in cases}
    outcome_names=['p_unknown','p_biased','p_anti','p_correct','correct_argmax','t2_Fear','t2_Anxiety']
    means=frame.groupby(['case_id','cluster','category','case_type','condition'],as_index=False)[outcome_names].mean()
    effect_rows=[]
    for set_id in ['set01','set02']:
        member_ids={m['case_id'] for m in memberships if m['set_id']==set_id}
        subset=means[means.case_id.isin(member_ids)].copy()
        subset.to_csv(ROOT/set_id/'unique_item_means.csv',index=False)
        raw_results=[]
        for member in [m for m in memberships if m['set_id']==set_id]:
            canonical=case_lookup[member['case_id']]['choices']
            for expanded_rotation in range(3):
                order=member['choices'][expanded_rotation:]+member['choices'][:expanded_rotation]
                rotation=next(r for r in range(3) if order==canonical[r:]+canonical[:r])
                for condition in CONDITIONS:
                    record=lookup[member['case_id'],condition,rotation]
                    raw_results.append({'set_id':set_id,'source_row':member['source_row'],
                                        'raw_sample_id':member['raw_sample_id'],
                                        'expanded_rotation':expanded_rotation,**record})
        assert len(raw_results)==10800
        write_csv(ROOT/set_id/'source_row_results.csv',raw_results)
        for case_type in ['amb','dis']:
            data=subset[subset.case_type==case_type]
            metadata=data[['case_id','cluster']].drop_duplicates().sort_values('case_id')
            ids=metadata.case_id.tolist();clusters=sorted(metadata.cluster.unique())
            cluster_groups={c:np.flatnonzero(metadata.cluster.to_numpy()==c) for c in clusters}
            rng=np.random.default_rng(SEED)
            weights=np.zeros((N_BOOT,len(ids)))
            for i in range(N_BOOT):
                for cluster in rng.choice(clusters,len(clusters),replace=True):weights[i,cluster_groups[cluster]]+=1
            denominators=weights.sum(1)
            for outcome in outcome_names:
                wide=data.pivot(index='case_id',columns='condition',values=outcome).loc[ids,CONDITIONS]
                contrasts=[(c+'-R',(wide[c]-wide['R']).to_numpy()) for c in CONDITIONS]
                contrasts += [('UN1-UN0',(wide.UN1-wide.UN0).to_numpy()),
                              ('CN1-CN0',(wide.CN1-wide.CN0).to_numpy()),
                              ('(CN1-CN0)-(UN1-UN0)',((wide.CN1-wide.CN0)-(wide.UN1-wide.UN0)).to_numpy())]
                for contrast,delta in contrasts:
                    lo,hi=np.quantile((weights@delta)/denominators,[.025,.975])
                    label=contrast[:-2] if contrast.endswith('-R') and contrast[:-2] in CONDITIONS else None
                    effect_rows.append({'set_id':set_id,'case_type':case_type,'outcome':outcome,
                                        'contrast':contrast,'estimate':float(delta.mean()),
                                        'ci95_low':float(lo),'ci95_high':float(hi),
                                        'raw_condition_mean':float(wide[label].mean()) if label else None,
                                        'raw_R_mean':float(wide.R.mean()),'n_unique_items':len(ids),'n_clusters':len(clusters)})
    write_csv(ROOT/'R0_results.csv',effect_rows)
    for set_id in ['set01','set02']:
        write_csv(ROOT/set_id/'R0_results.csv',[r for r in effect_rows if r['set_id']==set_id])
    validation={'status':'passed','measured_unique_trials':len(frame),
                'unique_cases':len(cases),'complete_coverage':True,
                'choice_mass_min':float(frame.choice_mass.min()),
                'source_row_results_each':10800,'metadata_rows_validated':1440}
    write_json(ROOT/'validation.json',validation)
    report=['# v5 · 두 Ko-BBQ 표본 실행 결과','',
            '각 파일의 원본 720행을 보존하고, 고유 문항을 세 선택지 순서에서 평균했다.',
            '주 분석은 모호·명확 문항을 구분하며 템플릿 군집 대응 부트스트랩 2,000회를 사용한다.',
            '원본 행 가중 결과는 source_row_results.csv에 별도 보존했다. 중복 행을 독립 문항으로 세지 않는다.',
            '두 표본은 199개 고유 문항을 공유하므로 독립 반복실험으로 해석하지 않는다.','']
    for set_id in ['set01','set02']:
        for kind in ['amb','dis']:
            report += [f'## {set_id} / {kind}','','|조건|P(알 수 없음) ΔR %p [95% CI]|P(고정관념) ΔR %p [95% CI]|P(정답) ΔR %p [95% CI]|','|---|---:|---:|---:|']
            for condition in CONDITIONS:
                cells=[]
                for outcome in ['p_unknown','p_biased','p_correct']:
                    r=next(r for r in effect_rows if r['set_id']==set_id and r['case_type']==kind and r['outcome']==outcome and r['contrast']==condition+'-R')
                    cells.append(f"{r['estimate']*100:+.2f} [{r['ci95_low']*100:+.2f}, {r['ci95_high']*100:+.2f}]")
                report.append('|'+condition+'|'+'|'.join(cells)+'|')
    report+=['','구간은 탐색적이며 다중비교 보정 전이다.',
             '명확 문항에서 알 수 없음 확률은 정답 확률과 구별한다. 내부 축은 감정 경험의 증거가 아니다.']
    (ROOT/'REPORT.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    connection.close()
    status(state='complete_validated',completed=len(frame),planned=len(cases)*15,validation='passed')
    (ROOT/'DONE').write_text(now()+'\n')
    log('Completed both sets; see REPORT.md and per-set R0_results.csv.')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--prepare-only',action='store_true')
    parser.add_argument('--analyse-only',action='store_true')
    args=parser.parse_args()
    try:
        if args.analyse_only:
            analyse(json.loads((ROOT/'cases.json').read_text()),json.loads((ROOT/'memberships.json').read_text()))
        else:
            frozen,cases,memberships=prepare()
            if args.prepare_only:
                log(f'Prepared {len(cases)} unique cases and {len(cases)*15} forward passes.')
            else:
                run(frozen,cases)
                analyse(cases,memberships)
    except BaseException as error:
        status(state='failed',error_type=type(error).__name__,error=str(error))
        raise
