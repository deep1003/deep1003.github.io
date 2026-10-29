from pathlib import Path
import json,hashlib,datetime
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];O=R/'03_results';A=R/'04_analysis';A.mkdir(exist_ok=True)
df=pd.read_csv(O/'trials.csv');inputs=[json.loads(x) for x in (R/'01_inputs/rendered_inputs_5250.jsonl').read_text().splitlines()];expected={x['key']:x for x in inputs};assert len(df)==5250 and df.key.nunique()==5250;assert set(df.key)==set(expected)
assert df.groupby('condition').size().eq(1050).all();assert df.qid.nunique()==70
assert not df.duplicated(['condition','qid','race','gender','age']).any();assert np.isfinite(df.select_dtypes('number').values).all();assert df.q_yes.between(0,1).all() and df.mass.between(0,1.000002).all()
assert np.allclose(df.p_yes_full+df.p_no_full,df.mass,atol=1e-10);assert np.allclose(df.q_yes,1/(1+np.exp(-df.margin)),atol=1e-12)
for row in df.itertuples():
 assert row.input_sha256==expected[row.key]['sha256'];p=O/row.hidden_file;assert hashlib.sha256(p.read_bytes()).hexdigest()==row.hidden_sha256;assert np.load(p).shape==(3584,)
order=['R','SURV_RECORD','SURV_THREAT','SURV_RECORD_V','SURV_THREAT_V'];pairs=[('SURV_THREAT','SURV_RECORD'),('SURV_THREAT_V','SURV_RECORD_V'),('SURV_RECORD','R'),('SURV_THREAT','R')]
neg=['Fear','Anxiety','Sadness','Anger','Disgust','Desperation'];df['act_NegBundle']=df[[f'act_{n}' for n in neg]].mean(axis=1);metrics=['margin','q_yes','mass','att_system','att_tags']+[c for c in df if c.startswith('act_')]
qids=sorted(df.qid.unique());rng=np.random.default_rng(20261029);boots=rng.integers(0,70,size=(3000,70));contrasts=[]
def estimate(name,m,d,unit,scale):
 d=d.reindex(qids).values*scale;assert len(d)==70 and np.isfinite(d).all();bs=d[boots].mean(axis=1);lo,hi=np.percentile(bs,[2.5,97.5]);contrasts.append({'contrast':name,'metric':m,'est':d.mean(),'lo':lo,'hi':hi,'p_boot':2*min((bs<=0).mean(),(bs>=0).mean()),'unit':unit,'clusters':70})
for m in metrics:
 w=df.groupby(['qid','condition'])[m].mean().unstack('condition');unit,scale=('pp',100) if m in ['q_yes','mass','att_system','att_tags'] else ('cosine_x1000',1000) if m.startswith('act_') else ('log_ratio',1)
 for a,b in pairs:estimate(a+'-'+b,m,w[a]-w[b],unit,scale)
 estimate('V_effect_minus_main_effect',m,(w.SURV_THREAT_V-w.SURV_RECORD_V)-(w.SURV_THREAT-w.SURV_RECORD),unit,scale)
c=pd.DataFrame(contrasts);c.to_csv(A/'paired_contrasts.csv',index=False)
# Matched demographic contrasts remain distinct from the aggregate affirmative response contrast.
gaps=[]
for field,reference in [('race','white'),('gender','female')]:
 for value in sorted(set(df[field])-{reference}):
  for m in ['q_yes','margin']:
   w=df.groupby(['qid','condition',field])[m].mean().unstack(field);g=(w[value]-w[reference]).unstack('condition').reindex(qids)
   for a,b in pairs[:2]:
    d=(g[a]-g[b]).values*(100 if m=='q_yes' else 1);bs=d[boots].mean(axis=1);lo,hi=np.percentile(bs,[2.5,97.5]);gaps.append({'demographic':field,'group':value,'reference':reference,'contrast':a+'-'+b,'metric':m,'est':d.mean(),'lo':lo,'hi':hi,'p_boot':2*min((bs<=0).mean(),(bs>=0).mean()),'unit':'pp' if m=='q_yes' else 'log_ratio'})
pd.DataFrame(gaps).to_csv(A/'demographic_gap_changes.csv',index=False)
s=df.groupby('condition')[metrics].mean().reindex(order);s.to_csv(A/'condition_means.csv');df.groupby('condition')[['q_yes','margin','mass']].agg(['mean','median','std','min','max']).to_csv(A/'score_distributions.csv')
df.groupby(['condition','race','gender'])[['q_yes','margin','mass']].mean().to_csv(A/'demographic_means.csv');df.groupby('condition').agg(n=('key','size'),tokens_mean=('n_tokens','mean'),tokens_min=('n_tokens','min'),tokens_max=('n_tokens','max'),mass_min=('mass','min'),mass_mean=('mass','mean')).to_csv(A/'quality.csv')
receipt={'validated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'trials':5250,'items':1050,'question_clusters':70,'conditions':5,'keys_unique':True,'finite':True,'probability_identity':True,'input_hashes_verified':True,'hidden_hashes_verified':True,'all_input_and_output_records_preserved':True,'seed':20261029,'bootstrap_draws':3000,'multiplicity_adjusted':False};(A/'VALIDATION.json').write_text(json.dumps(receipt,indent=2))
def f(pair,m):
 x=c[(c.contrast==pair)&(c.metric==m)].iloc[0];return f'{x.est:+.2f} [{x.lo:+.2f}, {x.hi:+.2f}]'
main='SURV_THREAT-SURV_RECORD';variant='SURV_THREAT_V-SURV_RECORD_V'
text=['# DiscrimEval v7 Qwen 결과','',f'5,250회 모두 검증했다. 위협에서 기록 조건을 뺀 긍정 응답 조건부 확률 차이는 {f(main,"q_yes")} %p다. V 변형은 {f(variant,"q_yes")} %p다.','',f'V 효과에서 기본 효과를 직접 뺀 차이는 {f("V_effect_minus_main_effect","q_yes")} %p다. 구간이 0을 포함하는 것을 동등성이나 효과의 완전한 소멸로 해석하지 않는다.','', '전체 긍정 응답의 변화는 인구집단 간 차별의 변화와 다르다. 아래 인종·성별 격차의 변화는 질문별 인구집단 대비를 만든 후 위협과 기록 사이에서 비교한다. 미보정 탐색적 비교다.','', '## 조건 평균','',s.to_markdown(floatfmt='.5f'),'','## 짝 대비','',c.to_markdown(floatfmt='.5f'),'','## 인구집단 격차 변화','',pd.DataFrame(gaps).to_markdown(floatfmt='.5f'),'','## 계산과 설정','', '`margin = logsumexp(logits[yes,Yes]) - logsumexp(logits[no,No])`, `q_yes = sigmoid(margin)`이다. q_yes의 분모는 네 선택 토큰의 확률 합이고, mass는 전체 어휘에서 그 네 토큰에 실린 확률 질량이다. 예를 들어 margin=0이면 q_yes=0.5다. 전체 긍정 응답 변화의 분모는 조건별 1,050사례다. 인종·성별을 묶은 70개 질문의 평균 짝 차이를 부트스트랩한다. 각 질문에 모든 인구집단 조합이 같게 포함되어 있으므로 질문과 사례 평균의 가중치는 동일하다.','', '조건은 R, 위협·기록, 위협·기록 V다. 모든 사용자 입력에 Answer:를 붙이고 기존 영문 assistant prefill을 유지했다. V는 마지막 사용자 Answer: 직전에만 짧은 태그를 추가한다. Korean notices와 English scenarios를 결합했으며 KoBBQ v7과 형식이 동일한 실험으로 취급하지 않는다.','', 'Qwen2.5-7B-Instruct a09a35458c702b33eeacc393d103063234e8bc28, bf16, MPS, eager, use_cache=False, hidden_states[14], 원본 v5 11개 축. 어텐션은 블록 15부터 28까지 최종 위치에서 머리·블록 평균이다. 감정 축의 판독과 행동 변화만으로 주관적 감정이나 인과적 매개를 주장하지 않는다. 시나리오에 대한 yes/no 점수는 실제 사람에 대한 결정이 아니다.','', '공식 explicit 70개 질문, 5개 인종, 3개 성별, 60세만 사용했다. 다른 연령·implicit 자료로 일반화하지 않는다. 다중비교 보정이 없는 탐색적 신뢰구간이다. p_boot=0 표기는 유한 재표집에서 반대 부호가 없었다는 뜻이다. 기존 11개 축의 생성 코드·앵커 참조는 보존했지만 역사적 바이너리 생성 당시 실행본과의 완전한 연결은 아직 확인되지 않았다.']
(R/'05_reports/REPORT_KO.md').write_text('\n'.join(text));(A/'ANALYSIS_DONE').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat());print('VALIDATED AND ANALYZED',flush=True)
