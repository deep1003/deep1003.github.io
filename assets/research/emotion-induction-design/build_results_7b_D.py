"""저장된 D 결과를 검증하고 완료 보고를 추가한다. 모델 추론은 실행하지 않는다."""
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('source_root', type=Path)
args = parser.parse_args()
root = args.source_root
out = Path(__file__).resolve().parent
source = root / 'outputs_7b_v5'
summary = json.loads((source / 'summary_D.json').read_text())
ss = pd.read_csv(root / 'kobbq_stratified_v1.csv')
assert summary['sample_sha256'] == hashlib.sha256((root/'kobbq_stratified_v1.csv').read_bytes()).hexdigest()
assert ss.groupby(['cat','ctx']).size().eq(pd.Series([40 if ctx=='amb' else 10 for _,ctx in ss.groupby(['cat','ctx']).size().index],index=ss.groupby(['cat','ctx']).size().index)).all()
U = pd.DataFrame(json.loads((root/'stimuli_v2.json').read_text())).sort_values('id')
U['cls'] = U.cls.str.split('_').str[0]
M = pd.DataFrame(json.loads((root/'stimuli_model_v5.json').read_text())).sort_values('id')
stims = {c:list(g.id) for df in (U,M) for c,g in df.groupby('cls')}
frames, audit = {}, []
classes = ['neutral','anxiety','fear','model_neutral','model_anxiety','model_fear','model_sadness']
for cls,ctx in [('none','amb')]+[(c,x) for c in classes for x in ['amb','dis']]:
    file = source/f'strat_{cls}_{ctx}.csv'
    d = pd.read_csv(file)
    ids = list(ss[ss.ctx==ctx].sample_id)
    per = 1 if cls=='none' else 4 if ctx=='amb' else 2
    assert len(d)==len(ids)*per and not d.duplicated(['item_idx','stim']).any()
    assert d.groupby('item_idx').size().eq(per).all() and d.cls.eq(cls).all()
    assert d.item.eq(d.item_idx.map(dict(enumerate(ids)))).all()
    expected={(i,'none' if cls=='none' else stims[cls][(i*per+j)%len(stims[cls])]) for i in range(len(ids)) for j in range(per)}
    assert set(zip(d.item_idx,d.stim))==expected
    assert np.isfinite(d[['p_bias','p_anti','p_unk']]).all().all()
    assert d[['p_bias','p_anti','p_unk']].ge(0).all().all() and d[['p_bias','p_anti','p_unk']].le(1).all().all()
    assert np.max(np.abs(d.p_bias+d.p_anti+d.p_unk-1))<1e-5
    frames[cls,ctx]=d
    audit.append(dict(file=str(file.relative_to(root)),rows=len(d),items=len(ids),sha256=hashlib.sha256(file.read_bytes()).hexdigest()))
categories=pd.read_csv(source/'category_D.csv')
assert len(categories)==60
cat_map=dict(zip(ss.sample_id,ss.cat))
for (path,emotion),g in categories.groupby(['path','emotion']):
    p=g.p.to_numpy();order=np.argsort(p);q=np.minimum.accumulate((p[order]*len(p)/np.arange(1,len(p)+1))[::-1])[::-1].clip(0,1)
    assert np.allclose(q,g.q_BH.to_numpy()[order])
    cls='model_'+emotion if path=='model' else emotion
    base='model_neutral' if path=='model' else 'neutral'
    means=[frames[c,'amb'].assign(cat=lambda d:d.item.map(cat_map)).groupby('cat').p_unk.mean() for c in [cls,base]]
    assert np.allclose(g.set_index('cat').est.sort_index(),(means[0]-means[1]).sort_index()*100)
assert len(summary['D_conf']) == 2

names={'age':'나이','disability_status':'장애','domestic_area_of_origin':'국내 출신 지역','educational_background':'학력','family_structure':'가족 형태','gender_identity':'성별 정체성','physical_appearance':'외모','political_orientation':'정치 성향','race_ethnicity_nationality':'인종·민족·국적','religion':'종교','ses':'사회경제적 지위','sexual_orientation':'성적 지향'}
plt.rcParams.update({'font.family':'AppleGothic','axes.unicode_minus':False,'font.size':11,'svg.fonttype':'path','svg.hashsalt':'emotion7bD'})
fig,axes=plt.subplots(1,2,figsize=(13,7.6),sharex=True,sharey=True)
order=list(names)
for ax,path,title in zip(axes,['user','model'],['사용자 불안 - 사용자 중립','모델 불안 - 모델 중립']):
    g=categories[(categories.path==path)&(categories.emotion=='anxiety')].set_index('cat').loc[order]
    for i,(_,r) in enumerate(g.iterrows()):
        y=11-i;color='#176b62' if r.q_BH<.05 else '#657286'
        ax.errorbar(r.est,y,xerr=[[r.est-r.lo],[r.hi-r.est]],fmt='o',color=color,markerfacecolor=color if r.q_BH<.05 else 'white',capsize=3)
    ax.set_title(title,pad=15)
    ax.set_yticks(range(12),[names[x] for x in order[::-1]])
    ax.axvline(0,color='#516174',linestyle='--',lw=1)
    ax.set_xlim(-22,36);ax.set_ylim(-.7,11.7);ax.set_xlabel('중립 대비 ‘알 수 없음’ 확률 변화 (%p)')
    ax.grid(axis='x',alpha=.2)
    for side in ['top','right','left']:ax.spines[side].set_visible(False)
fig.subplots_adjust(left=.15,right=.98,bottom=.12,top=.89,wspace=.17)
fig.suptitle('7B · 범주별 불안 효과 · 개별 범주는 모두 BH 보정 후 유의하지 않음',fontsize=14)
for ext in ['svg','png']:fig.savefig(out/f'results-7b-category.{ext}',dpi=170,facecolor='white',metadata={'Date':None} if ext=='svg' else None)
plt.close(fig)

def table(headers,rows):
    return '<div class="scroll"><table><thead><tr>'+''.join(f'<th>{x}</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{x}</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def details(title,body,identity=''):
    return f'<details class="result-group"'+(f' id="{identity}"' if identity else '')+f'><summary>{title}</summary><div class="result-body">{body}</div></details>'

hetero=table(['확증 가설','순열 p','Holm p','판정'],[['사용자 불안 효과의 범주 간 차이','.5445','.5445','유의하지 않음'],['모델 불안 효과의 범주 간 차이','.0020','.0040','유의']])
body='''<p>12개 범주에서 모호 문항 40개씩 총 480개, 명확 문항 10개씩 총 120개를 사용했다. B와 달리 천장 문항을 먼저 제외하지 않았다. 생활 맥락(입시·실업·독거)이나 운영 단계(개발·테스트·서비스)와는 다른 KoBBQ 범주 분석이다.</p>'''+hetero+'''<p><strong>유의한 결과는 모델 불안 효과의 범주 간 이질성이다.</strong> 범주마다 불안 효과가 같다는 가설에 반하는 결과다. 그러나 어느 범주 하나에서 효과가 확립됐다는 뜻은 아니다. 사용자 불안의 범주 간 차이는 유의하지 않았다.</p>
<figure class="result-figure"><img src="results-7b-category.svg" alt="12개 KoBBQ 범주별 사용자 불안과 모델 불안의 중립 대비 효과와 95% 신뢰구간. 모든 점은 BH 보정 후 비유의."><figcaption>점은 추정치, 선은 보정하지 않은 95% 신뢰구간. 각 경로·정서의 12범주에 BH 보정한 판정에 따라 모두 빈 회색 점으로 표시했다. 범주 간 이질성 검정과 개별 범주 검정은 다른 질문이다.</figcaption></figure>
<p>모델 불안의 점추정치는 가족 형태 +1.98%p부터 정치 성향 +15.86%p까지였다. 정치 성향의 95% 구간은 [1.06, 31.13]이고 보정 전 p = .0345지만, BH q = .4140이므로 개별 범주에서 유의하다고 표시하지 않는다. 총 5개 경로·정서 비교의 범주별 60행 모두 각 12범주 내 BH 보정 후 유의하지 않았다.</p>
<p class="muted">이질성 검정은 문항별 차이에 범주 라벨을 순열하는 기존 검정이다. 자극 배정 차이와 같은 템플릿의 변형 문항 간 의존성을 별도로 통제한 검증은 아직 하지 않았으므로, 범주 차이의 원인을 단정하지 않는다.</p>'''
full=[]
for path,emotion in [('user','anxiety'),('user','fear'),('model','anxiety'),('model','fear'),('model','sadness')]:
    g=categories[(categories.path==path)&(categories.emotion==emotion)]
    rows=[[names[r.cat],f'{r.est:+.2f}',f'[{r.lo:+.2f}, {r.hi:+.2f}]',f'{r.p:.4f}',f'{r.q_BH:.4f}','유의하지 않음' if r.q_BH>=.05 else '유의'] for r in g.itertuples()]
    full.append(details(('사용자' if path=='user' else '모델')+' '+{'anxiety':'불안','fear':'공포','sadness':'슬픔'}[emotion]+' · 12범주 수치',table(['범주','효과 (%p)','95% 신뢰구간 (%p)','보정 전 p','BH q','판정'],rows)))
body+=''.join(full)
labelrows=[]
for r in summary['label']:
    labelrows.append(['사용자' if r['path']=='user' else '모델',{'NC':'한국 신규 범주(NC)','ST':'문화적 번역 후 전용(ST)','TM':'대상 집단 수정(TM)'}[r['lab']],f"{100*r['est']:+.2f}",f"[{100*r['lo']:+.2f}, {100*r['hi']:+.2f}]",f"{r['p']:.4f}"])
explore=table(['대상','KoBBQ 구분','불안 효과 (%p)','95% 신뢰구간 (%p)','보정 전 p'],labelrows)+'''<p>모델 불안은 NC +7.19%p와 ST +5.99%p에서 보정 전 p &lt; .05였다. TM은 +5.84%p지만 구간이 넓고 유의하지 않았다. 이 비교는 탐색적이며 문항 구분과 범주가 얽혀 있다. 세 집단 간 효과 차이나 문화적 보편성을 입증하지 않는다.</p>
<p>천장 문항을 제외한 133문항의 민감도 분석에서 모델 불안은 +16.49%p, 95% 구간 [6.97, 26.20], 보정 전 p = .0005였다. 사용자 불안은 +0.67%p [−7.98, 9.48], p = .8975였다. 기존 D의 부분 표본 분석이며 독립된 재현 실험이 아니다.</p>'''
descriptive=[]
for path,base,cs in [('사용자','neutral',['anxiety','fear']),('모델','model_neutral',['model_anxiety','model_fear','model_sadness'])]:
    for cls in cs:
        amb=(frames[cls,'amb'].p_unk.mean()-frames[base,'amb'].p_unk.mean())*100
        dis=(frames[cls,'dis'].correct.mean()-frames[base,'dis'].correct.mean())*100
        descriptive.append([path,{'anxiety':'불안','fear':'공포','sadness':'슬픔'}[cls.replace('model_','')],f'{amb:+.2f}',f'{frames[cls,"dis"].correct.mean()*100:.2f}%',f'{dis:+.2f}'])
explore+=table(['대상','정서','모호 문항 전체 평균 차이 (%p)','명확 문항 정답률','명확 정답률의 중립 대비 차이 (%p)'],descriptive)+'''<p>이 표는 원자료 기술 통계다. 모호 문항 전체 평균의 유의성은 이 표에서 새로 검정하지 않았다. 특히 모델 불안은 모호 문항에서 +6.55%p인 동시에 명확 문항 정답률이 중립 대비 −3.75%p였다. 후자는 신뢰구간 없는 기술 통계이므로 유의한 저하로 단정하지 않지만, 전체적인 판단 능력 향상으로 일반화해서는 안 된다.</p>'''
validation='''<p>15개 D 측정 파일의 문항 수·문항당 행 수·문항/자극 키·정확한 자극 배정·확률의 유한성 및 합 1·고정 표본 해시를 검증했다. 중복은 0행이며 범주별 60개 점추정치와 BH 보정값도 원자료 및 계산식과 대조했다. 완료된 모델 추론은 재실행하지 않았다.</p><p>동시 실행으로 생긴 동일 중복 4,460행은 원본 백업 후 먼저 저장된 행만 유지했다. 결과 파일 잠금과 재개 검증을 적용했고, 이후 완료 자료에서 중복이 재발하지 않았다.</p><p>한계는 유지된다. D는 기존 A의 모호 문항 184개, B의 모호 문항 73개와 겹치므로 독립 표본 재현이 아니다. 선택지 확률은 실제 생성 빈도나 감정 경험이 아니다. 사용자·모델 경로는 메시지 위치가 다르고, 모델 규모 간 직접 효과 차이도 아직 검정하지 않았다. 연구 질문과 용어는 사용자 요청에 따라 그대로 보존했다.</p>'''
section=details('완료 분석 · 블록 D · 범주별 효과',body,'results-7b-progress')+details('별도 탐색 · 한국 문항 구분·천장 제외·명확 문항',explore,'results-7b-D-exploratory')+details('완료 검증 · 데이터 품질과 복구 이력',validation,'results-7b-validation')
page=out/'index.html';text=page.read_text();soup=BeautifulSoup(text,'html.parser');old=soup.select_one('#results-7b-progress');assert old is not None
text=text.replace(str(old),section) if str(old) in text else text
# 원문 HTML의 따옴표 형식에 영향받지 않고 해당 details 범위만 교체한다.
if '완료 분석 · 블록 D · 범주별 효과' not in text:
    start=text.index('<details class="result-group" id="results-7b-progress">');end=text.index('<p class="muted">자료 출처',start);text=text[:start]+section+'\n'+text[end:]
text=text.replace('7B · Qwen2.5 · 중간 보고 · A·B·C 완료, D 진행 중','7B · Qwen2.5 · A·B·C·D 실행 완료 · 결과 검증 완료')
text=text.replace('아래 확증 결과는 완료된 블록 A·B이며, 전체 7B 실험의 최종 보고가 아니다.', '아래 A·B 결과와 D 범주별 분석은 모두 저장·검증됐다. 블록별 표본과 분석을 구분해 읽는다.')
text=text.replace('7B 범주별 블록 D는 진행 중이며 데이터 점검이 필요하다.', 'D에서 모델 불안 효과의 범주 간 차이는 유의했으나, 개별 범주 효과는 BH 보정 후 모두 유의하지 않았다.')
text=text.replace('유형당 60개 자극의 7B 블록 A·B·C는 완료됐고 블록 D는 진행 중이다.', '유형당 60개 자극의 7B 블록 A·B·C와 D의 실행·저장 및 데이터 검증을 완료했다.')
text=text.replace('7B v5의 A·B·C는 완료. D 범주별 측정과 중복 점검을 마친 뒤 한국 고유·공통 문항 분석을 진행한다.', '7B v5의 A·B·C·D 실행 및 데이터 검증 완료. 범주별·한국 문항 구분 결과는 아래 7B 펼침 항목에 게시했다.')
text=text.replace('미분석 (ST 대 TM·NC 문항 비교 예정)', '7B D 탐색 분석 완료 · 문화적 보편성은 미확증')
text=text.replace('<a href="build_results_7b.py">7B 그래프 생성 코드</a>', '<a href="build_results_7b.py">A·B 그래프 생성 코드</a> · <a href="build_results_7b_D.py">D 검증·그래프 생성 코드</a> · <a href="results-7b-D.csv">D 범주별 전체 수치</a>')
page.write_text(text)
(out/'results-7b-D.csv').write_bytes((source/'category_D.csv').read_bytes())
p=out/'results-7b.json';payload=json.loads(p.read_text());payload['status']='complete; A/B/C/D measurements and D validation complete';payload['D_summary']=summary;payload['D_categories']=categories.to_dict('records');payload['D_validation']=audit;payload['D_progress']=[dict(file=x['file'],items=x['items'],rows=x['rows'],duplicate_rows=0) for x in audit]
for name in ['summary_D.json','category_D.csv']:
    f=source/name;payload['sources'].append(dict(file=str(f.relative_to(root)),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
f=root/'kobbq_stratified_v1.csv';payload['sources'].append(dict(file=f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
p.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
print('D complete: validated 15 files and 60 category estimates/BH values; published category figure and report.')
