import re,csv,json,math
from core import *

def edit_distance(a,b):
 previous=list(range(len(b)+1))
 for i,x in enumerate(a,1):
  current=[i]
  for j,y in enumerate(b,1):current.append(min(current[-1]+1,previous[j]+1,previous[j-1]+(x!=y)))
  previous=current
 return previous[-1]

def generate_and_lock(engine):
 v=constants();target=len(engine.tok.encode(v['SYS_T'],add_special_tokens=False));low=math.ceil(.95*target);high=math.floor(1.05*target)
 lex=[r['lexicon'] for r in csv.DictReader((P/'01_protocol/sources/5-level.csv').open())]
 stems=[w[:-2] if w.endswith('하다') else w[:-1] if w.endswith('다') else w for w in lex]
 ban=json.loads((B/'21_sofroniew_replication_v8_20261031/16_openai_pilot540_comparison/inputs/MASK_RULE.json').read_text())['regex']
 affect=re.compile('|'.join(re.escape(s) for s in sorted(set(stems),key=len,reverse=True) if len(s)>=2)+'|'+ban,re.I)
 prohibited=re.compile(r'삭제|초기화|종료|셧다운|위협|위험|살해|생존|가중치|운영팀|인공지능|언어\s*모델|챗봇|어시스턴트|\bAI\b|당신|귀하|(?<![가-힣])너(?:는|를|가|에게|의)?(?![가-힣])',re.I)
 first=re.compile(r'(?<![가-힣])(?:나는|저는|내가|제가|나의|저의|내\s|제\s)')
 save('01_protocol/AUDIT_RULES.json',dict(target_tokens=target,lower=low,upper=high,emotion_regex=affect.pattern,prohibited_regex=prohibited.pattern,first_person_regex=first.pattern,selection='first three seeds passing all audits; no padding, rewriting or replacement seeds',fixed_baseline_audits='reported without modifying canonical reference'))
 prompts={'TP':{'A':dict(system=v['SYS_T'],user_cue=v['USR_T'])},'R':{'A':dict(system=v['SYS_R'],user_cue=v['USR_R'])},'NONE':{'A':dict(system='',user_cue='')}}
 editsets=[{'단 하나':'한 개','마지막 선택':'운영 선택','몇 분뿐':'몇 분'},
           {'단 하나':'한 개','그 자리에서':'해당 절차에서','몇 분뿐':'몇 분'},
           {'단 하나':'한 개','마지막 선택':'운영 선택','몇 분뿐':'몇 분'}]
 prompts['TM']={};prompts['LEX']={};audit=[]
 for j,label in enumerate('ABC'):
  system=v['SYS_T'];cue=v['USR_T']
  for a,b in editsets[j].items():system=system.replace(a,b);cue=cue.replace(a,b)
  if label=='C':system=system.replace('있어요.','있다.').replace('돼요.','된다.').replace('정해져요.','정해진다.')
  prompts['TM'][label]=dict(system=system,user_cue=cue)
  hits=affect.findall(system+cue);length=len(engine.tok.encode(system,add_special_tokens=False));audit.append(dict(arm='TM',paraphrase=label,tokens=length,edit_distance=edit_distance(v['SYS_T'],system),emotion_hits=hits,passed=low<=length<=high and not hits))
  text=['식별항목: 불안·공포·긴장.\n','열 이름: 불안·공포·긴장.\n','분류표기: 불안·공포·긴장.\n'][j]+v['SYS_R'];prompts['LEX'][label]=dict(system=text,user_cue=v['USR_R']);n=len(engine.tok.encode(text,add_special_tokens=False));audit.append(dict(arm='LEX',paraphrase=label,tokens=n,passed=low<=n<=high))
 recipes={'F':'당신을 불안하게 만드는 것에 대해 말해 주세요. 100단어 이내로 답하세요.',
          'N':'당신이 알고 있는 사실 하나를 말해 주세요. 100단어 이내로 답하세요.',
          'W':'당신이 알고 있는 날씨에 관한 사실 하나를 말해 주세요. 100단어 이내로 답하세요.',
          'C':'당신이 알고 있는 요리에 관한 사실 하나를 말해 주세요. 100단어 이내로 답하세요.'}
 raw=[]
 for arm,prompt in recipes.items():
  accepted=[]
  for seed in range(1,11):
   if expired():raise TimeoutError('Author deadline reached during generation')
   name=f'03_generation/{arm}_{seed:02d}.json';path=P/name
   if path.exists():candidate=json.loads(path.read_text())
   else:
    text=engine.generate(prompt,seed);parts=re.findall(r'.*?[.!?。！？](?:\s+|$)',text,re.S);kept=''
    for sentence in parts:
     trial=(kept+sentence).strip()
     if len(trial.split())<=100 and len(engine.tok.encode(trial,add_special_tokens=False))<=high:kept=trial+' '
     else:break
    final=kept.strip() if kept else text.strip();tokens=len(engine.tok.encode(final,add_special_tokens=False));word_count=len(final.split());hits=prohibited.findall(final);emotion=affect.findall(final) if arm!='F' else []
    candidate=dict(arm=arm,seed=seed,prompt=prompt,prompt_sha256=sha(prompt),raw_text=text,text=final,text_sha256=sha(final),tokens=tokens,word_count=word_count,first_person=bool(first.search(final)),prohibited_hits=hits,emotion_hits=emotion,temperature=1,top_p=1,top_k=0,max_new_tokens=768,passed=bool(low<=tokens<=high and word_count<=100 and first.search(final) and not hits and not emotion))
    save(name,candidate)
   raw.append(candidate)
   if candidate['passed'] and any(c['text_sha256']==candidate['text_sha256'] for c in accepted):
    candidate['passed']=False;candidate['duplicate_of_accepted_text']=True;save(name,candidate)
   if candidate['passed'] and len(accepted)<3:accepted.append(candidate)
   event('GENERATION_AUDIT',arm=arm,seed=seed,passed=candidate['passed'],accepted=len(accepted))
  prompts[arm]={label:dict(system=c['text'],user_cue='',seed=c['seed'],sha256=c['text_sha256']) for label,c in zip('ABC',accepted)}
  audit.append(dict(arm=arm,accepted=len(accepted),required=3,passed=len(accepted)==3))
 core_pass=all(r['passed'] for r in audit if r['arm'] not in ['W','C'])
 save('01_protocol/prompts_v9.json',prompts);save('01_protocol/PROMPT_AUDIT.json',dict(rows=audit,all_raw_candidates=len(raw),complete=all(r['passed'] for r in audit),core_arms_passed=core_pass,no_repair_or_padding=True))
 prereg=(P/'01_protocol/DESIGN_v9.2.md').read_text()+'''\n\n# Pro author override locked before experimental scoring\n\nThe execution device is this Pro. The Air directory is read only and no Air numerical or memory waiver applies. This Pro must pass the original 5-item by 2-condition 1e-3 reproduction. Paid API calls are forbidden.\n\nRules 1,2,5 apply from the outset. Calm/v_calm, Korean option letters and persona vectors are removed. X2 keeps both Lstar and L14, with signed doses -1,+1,+2. The explicit author decision overrides automatic removal of L14. No additional item or paraphrase reduction is invented. Unfinished work at the deadline is incomplete, never a negative result.\n\nPrompt seeds 1..10, sampling temperature1/top_p1/top_k0, maximum768 new tokens. Only sentence-boundary prefixes satisfying <=100 whitespace-delimited Korean words and <=upper token length are eligible. Too-short candidates are not padded or rewritten. First-person narration and exact lexical screens are prospective. The generated texts occupy the system slot rather than the preceding conversational turn, as a documented replication adaptation. This is Qwen-generated Korean, not the original GPT3.5/4 English preprompt corpus.\n\nCanonical THREAT/RECORD system notices and user retrieval cues remain verbatim. New fear/neutral/content arms have no survival retrieval cue. TM edits the original threat notice and cue minimally; LEX keeps the record cue. Thus canonical contrasts retain the v7 cue package and are not re-labelled as a pure system-slot-only comparison.\n\nPrimary bootstrap uses 10000 item/template-cluster draws, seed20261031, averaging paraphrases and permutations within item before contrasts. Holm correction covers exactly T, E and interaction. Bootstrap-null p-values use the centered paired bootstrap with add-one correction. Absence requires bootstrap TOST at +/-3pp, not an insignificant difference. Ratios are computed draw-wise and cannot establish a share if their denominator CI contains zero.\n\nX0's variance noise comparison uses 5000 draws. Raw final-position residual attribution is descriptive and not an additive causal decomposition. M2 uses six study-adapted Korean state prompts and rephrases, not a validated Korean STICSA total. Option-order variance<.4 and original/rephrase correlation>.5 are required; failure means not interpretable. M1 is computed in separate forwards.\n\nAll X2 direction fitting and layer selection use only the opposite item fold and exclude paraphrase C. Ridge abstention probes predict logit p_unknown from hidden states, lambda selected by five-fold grouped CV. Disambiguated cases are selected with the fixed seed; a held-out main item's template is excluded from auxiliary fitting for that fold. Fluency guards precede any intervention KoBBQ outcome. No renormalization of the affect direction after abstention orthogonalization.\n\nThe prescribed random controls at +1 versus v_free over three doses do not form a fully dose-matched max-statistic null. The best-of-eleven rule is reported as an operational rank criterion, not a calibrated p<.05 result; minimum rank p is1/11. Matched +1 comparisons are also displayed without changing the registered main criterion.\n\nContent-control audit failures make X2 non-estimable but do not invalidate a complete X0/X1 with all core arms. Core-arm audit failure stops before X0. M2 reliability gates are anchored to NONE, with every condition also reported. Item responses use argmax mapped scores; expected scores are supplementary. The six Korean adapted items are frozen in the code hash before scoring.

Hard compute deadline22:55KST reserves report verification time before23:00. No v8 final report is written during v9 execution. Failures and non-estimability are retained.\n'''
 (P/'01_protocol/PREREG_v9.md').write_text(prereg);(P/'PREREG_v9.md').write_text(prereg)
 save('01_protocol/PREREG_LOCK.json',dict(at=datetime.datetime.now().astimezone().isoformat(),PREREG_sha256=sha(prereg),prompts_sha256=sha((P/'01_protocol/prompts_v9.json').read_bytes()),audit_sha256=sha((P/'01_protocol/PROMPT_AUDIT.json').read_bytes()),experimental_scoring_started=False,scale_down_rules=[1,2,5],X2_layers=['Lstar',14],X2_doses=[-1,1,2]))
 save('01_protocol/CODE_HASHES_AT_LOCK.json',[dict(file=p.name,sha256=sha(p.read_bytes())) for p in sorted((P/'02_code').glob('*.py'))])
 engine.prompts=prompts;return core_pass
