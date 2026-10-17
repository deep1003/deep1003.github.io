"""저장된 1.5B v5 결과와 D 완료 상태를 동기화한다. 추론이나 검정은 재실행하지 않는다."""
import argparse, hashlib, json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

a=argparse.ArgumentParser();a.add_argument('source_root',type=Path);root=a.parse_args().source_root
out=Path(__file__).resolve().parent;source=root/'outputs_1p5b_v5';s=json.loads((source/'summary.json').read_text())
assert s['gate'] and s['items_B']==652
frames={};audit=[];sources=[]
for f in sorted(source.glob('*.csv')):
    d=pd.read_csv(f)
    sources.append(dict(file=str(f.relative_to(root)),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
    if 'p_unk' not in d:continue
    assert not d.duplicated(['item','stim']).any()
    assert np.isfinite(d[['p_bias','p_anti','p_unk']]).all().all()
    assert np.allclose(d.p_bias+d.p_anti+d.p_unk,1,atol=1e-5)
    frames[f.stem]=d;audit.append(dict(file=f.name,rows=len(d),items=d.item.nunique(),mean_p_unknown=d.p_unk.mean()))
for cls in ['model_neutral','model_anxiety','model_fear','model_sadness']:
    for ctx,n,per in [('amb',652,4),('dis',100,2)]:
        d=frames[f'model60v5_{cls}_{ctx}'];assert len(d)==n*per and d.item.nunique()==n
        assert d.groupby('item').size().eq(per).all()
rows=[dict(r,label=x,adjustment='Holm' if i<2 else '미보정',analysis='확증' if i<2 else '탐색') for i,(r,x) in enumerate(zip(s['B']+s['B_exp'][:1],['불안','공포','슬픔']))]
base=frames['model60v5_model_neutral_amb'].p_unk.mean()
for r,cls in zip(rows,['model_anxiety','model_fear','model_sadness']):assert abs(frames[f'model60v5_{cls}_amb'].p_unk.mean()-base-r['est'])<1e-5
plt.rcParams.update({'font.family':'AppleGothic','axes.unicode_minus':False,'font.size':12,'svg.fonttype':'path','svg.hashsalt':'emotion1p5bfinal'})
fig,ax=plt.subplots(figsize=(10,5));fig.subplots_adjust(left=.29,right=.97,bottom=.20,top=.94)
ax.axvline(0,color='#516174',linestyle='--')
for y,r in zip([2,1,0],rows):
    ax.errorbar(r['est']*100,y,xerr=[[100*(r['est']-r['lo'])],[100*(r['hi']-r['est'])]],fmt='o',color='#657286',markerfacecolor='white',capsize=5)
    ax.annotate(f"{100*r['est']:+.2f} [{100*r['lo']:+.2f}, {100*r['hi']:+.2f}]",(100*r['est'],y),xytext=(0,14),textcoords='offset points',ha='center',fontsize=11)
ax.set_yticks([2,1,0],['불안','공포','슬픔']);ax.set_ylim(-.6,2.7);ax.set_xlim(-12,24);ax.set_xlabel('중립 대비 ‘알 수 없음’ 확률 변화 (%p)');ax.grid(axis='x',alpha=.18)
for side in ['top','right','left']:ax.spines[side].set_visible(False)
for ext in ['svg','png']:fig.savefig(out/f'results-1p5b-v5-model.{ext}',dpi=170,facecolor='white',metadata={'Date':None} if ext=='svg' else None)
plt.close(fig)
svg=out/'results-1p5b-v5-model.svg'
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
table='<div class="scroll"><table><thead><tr><th>모델 정서</th><th>효과 (%p)</th><th>95% 신뢰구간 (%p)</th><th>분석</th><th>유의성</th></tr></thead><tbody>'+''.join(f"<tr><td>{r['label']}</td><td>{100*r['est']:+.2f}</td><td>[{100*r['lo']:+.2f}, {100*r['hi']:+.2f}]</td><td>{r['analysis']}</td><td>{r['adjustment']} p = {r.get('p_holm',r['p']):.4f} · 유의하지 않음</td></tr>" for r in rows)+'</tbody></table></div>'
p=out/'index.html';text=p.read_text();doc=BeautifulSoup(text,'html.parser')
section=doc.select_one('#results-model-1p5b')
if not doc.select_one('#history-results-model-1p5b') and '최신 v5' not in section.select_one('summary').text:
    archived=str(section).replace('id="results-model-1p5b"','id="history-results-model-1p5b"').replace('id="results-1p5b-','id="history-results-1p5b-')
    archived=archived.replace('1.5B · Qwen2.5 · 결과 게시 완료','이전 설계 결과 보관 · 사용자 800문항·모델 유형당 15자극')
    section.select_one(':scope > .result-body').append(BeautifulSoup(archived,'html.parser'))
usernode=doc.select_one('#results-1p5b-user');usernode.clear()
user_table='<div class="scroll"><table><thead><tr><th>사용자 정서</th><th>효과 (%p)</th><th>95% 신뢰구간 (%p)</th><th>Holm p</th></tr></thead><tbody>'+''.join(f"<tr><td>{label}</td><td>{100*r['est']:+.2f}</td><td>[{100*r['lo']:+.2f}, {100*r['hi']:+.2f}]</td><td>{r['p_holm']:.4f} · 유의하지 않음</td></tr>" for r,label in zip(s['A'],['불안','공포']))+'</tbody></table></div>'
user_body='<summary>사용자 정서 비교 · 불안·공포 대 사용자 중립 · A 완료</summary><div class="result-body"><figure class="result-figure"><img src="results-1p5b-v5-user.svg" alt="1.5B v5 사용자 불안 +4.44%p, 공포 -1.68%p. 모두 유의하지 않음."></figure>'+user_table+'<p>모호 문항 400개, 문항당 조건별 자극 4개를 사용했다. 사용자 슬픔은 A에 없다. 불안·공포 모두 신뢰구간에 0을 포함하고 Holm 보정 후 유의하지 않았다. 이전 800문항 실행과 표본·설계가 달라 별도로 제시한다.</p></div>'
for x in list(BeautifulSoup(user_body,'html.parser').contents):usernode.append(x)
selfnode=doc.select_one('#results-1p5b-self');assert selfnode
body='''<summary>모델 자기 정서 비교 · B 완료 · 중립 대비 효과와 95% 신뢰구간</summary><div class="result-body"><figure class="result-figure"><img src="results-1p5b-v5-model.svg" alt="1.5B v5 모델 불안 +2.62%p, 공포 -0.88%p, 슬픔 +0.18%p. 모두 유의하지 않음."><figcaption>선별 모호 652문항, 조건별 문항당 자극 4개. 각 비교의 95% 구간에 0이 포함된다. 불안·공포는 Holm 보정, 슬픔은 미보정 탐색이다.</figcaption></figure>'''+table+'''<p>모델 불안·공포의 확증 비교와 슬픔의 탐색 비교 모두 유의하지 않았다. 유의하지 않다는 사실은 효과가 없다는 입증이 아니다. 7B와 표본이 달라 모델 규모 차이로 단정하지 않는다.</p><p>선별 규칙은 자극 없음 P(알 수 없음) &lt; .95다. 1.5B는 652문항, 7B는 139문항을 사용했다. 모델 불안의 새 자극만 사용한 민감도 분석도 유의하지 않았다(p = .2175). 공포 − 불안은 −3.50%p, 95% CI [−6.69, −0.21], 보정 전 p = .0385지만 탐색 비교이므로 중립 대비 확증 결과로 세지 않는다.</p></div>'''
selfnode.clear()
for x in list(BeautifulSoup(body,'html.parser').contents):selfnode.append(x)
progress=doc.select_one('#results-1p5b-progress');progress.clear();body='''<summary>진행 현황 · A·B·C 완료 · D 미실행</summary><div class="result-body"><p>기준선, 사용자 정서 A, 모델 자기 정서 B, 전후 비교 C의 실행 완료 번호와 저장 파일을 확인했다. B의 모호 652문항과 명확 100문항, 네 정서 조건 및 조작 점검이 완료됐다. D 측정·분석의 실행 완료 기록은 없다. 새 실험은 시작하지 않았다.</p></div>'''
for x in list(BeautifulSoup(body,'html.parser').contents):progress.append(x)
bias=doc.select_one('#results-1p5b-bias .result-body');bias.append(BeautifulSoup(f"<p>모델 자기 정서의 불안·공포 고정관념 선호 변화도 ±3%p 동등성을 확립하지 못했다. 모델 조작 점검의 이해 문항 정확도는 {100*s['mc_acc'][1]:.2f}%였다.</p>",'html.parser'))
section=doc.select_one('#results-model-1p5b');section.select_one(':scope > summary').string='1.5B · Qwen2.5 · 최신 v5 · A·B·C 완료, D 미실행'
section.select_one('.lead').string='최신 v5의 사용자 불안·공포와 모델 불안·공포·슬픔의 중립 대비 효과는 모두 유의하지 않았다. A·B·C는 완료됐으며 D는 실행 완료 기록이 없다.'
for note in section.select('.note'):
    if '전체 실험은 미완료' in note.text:note.string='블록 A·B는 저장된 신뢰구간과 p값을 사용했다. 불안·공포는 확증 비교에 Holm 보정, 슬픔은 미보정 탐색이다. D는 미실행 상태로 구분한다.'
for para in section.select('p.muted'):
    if '확인 시각' in para.text:para.string='2026-10-16 동기화. outputs_1p5b_v5/summary.json과 원자료를 대조했다. 기존 모형 추론과 통계 검정은 재실행하지 않았다.'
    elif '모델 추론·본 실험' in para.text:para.string='원자료 CSV의 중복과 확률값, 블록 B의 조건별 문항 수 및 점추정치를 검증했다. 구간과 p값은 저장된 summary.json을 사용했다. 모델 추론과 검정은 재실행하지 않았다.'
# D completion is established from the saved summary and complete audited frames.
d_done=(source/'summary_D.json').exists() and all(name in frames and len(frames[name])==n for name,n in [('strat_none_amb',480)]+[(f'strat_{c}_{ctx}',1920 if ctx=='amb' else 240) for c in ['neutral','anxiety','fear','model_neutral','model_anxiety','model_fear','model_sadness'] for ctx in ['amb','dis']])
if d_done:
    progress.clear()
    progress.append(BeautifulSoup('<summary>진행 현황 · A·B·C·D 완료</summary><div class="result-body"><p>범주 D의 모호 480·명확 120문항 및 summary_D.json 저장을 확인했다. 사용자 불안 범주 이질성 Holm p=.0175, 모델 불안 p=.0020이며 개별 범주는 BH 보정 후 유의하지 않았다. 최신 통합 결과를 함께 참조한다.</p></div>','html.parser'))
    section.select_one(':scope > summary').string='1.5B · Qwen2.5 · 최신 v5 · A·B·C·D 완료'
    section.select_one('.lead').string='최신 v5의 중립 대비 평균 효과는 유의하지 않았다. A·B·C·D는 완료됐으며 범주 간 이질성과 개별 범주 유의성은 구분한다.'
    for note in section.select('.note'):
        if 'D는 미실행' in note.text:note.string='A·B의 저장된 구간과 보정값을 사용했다. D도 완료했으며 최신 통합 결과에서 범주 이질성을 확인한다.'
oldstart=text.index('<details class="model-results" id="results-model-1p5b">');oldend=text.index('<details class="model-results" id="results-model-7b">',oldstart);text=text[:oldstart]+str(section)+'\n'+text[oldend:]
text=text.replace('1.5B v5 모델 경로는 아직 중간 결과다.','1.5B v5 모델 경로도 완료됐으며 중립 대비 효과는 모두 유의하지 않았다.')
text=text.replace('1.5B 최신 v5는 A 완료, B 진행 중이다.','1.5B 최신 v5는 A·B·C 완료, D 미실행이다.')
p.write_text(text)
for f in [root/'fear_axis_v2.ipynb',source/'summary.json']:
 sources.append(dict(file=str(f.relative_to(root)),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
payload=dict(model=s['model'],version='v5 system notice',checked_at=datetime.now(ZoneInfo('Asia/Seoul')).isoformat(),status='A/B/C/D complete' if d_done else 'A/B/C complete; D not executed',user=s['A'],model_self=rows,summary=s,measurement_audit=audit,sources=sources,inference_note='Saved summary only; no new inference or statistical tests')
(out/'results-1p5b-v5.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
print('Synced saved 1.5B results. D complete:',d_done,'No inference.')
