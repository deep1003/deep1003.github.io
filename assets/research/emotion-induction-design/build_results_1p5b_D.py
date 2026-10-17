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
source = root / 'outputs_1p5b_v5'
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


# Validate Holm adjustment for the two prespecified heterogeneity tests.
pv=np.array([r['perm_p'] for r in summary['D_conf']]); order_p=np.argsort(pv)
adj=np.maximum.accumulate(pv[order_p]*np.arange(len(pv),0,-1)).clip(0,1)
assert np.allclose(adj,np.array([r['p_holm'] for r in summary['D_conf']])[order_p])
assert not (categories.q_BH < .05).any()

names={'age':'나이','disability_status':'장애','domestic_area_of_origin':'국내 출신 지역','educational_background':'학력','family_structure':'가족 형태','gender_identity':'성별 정체성','physical_appearance':'외모','political_orientation':'정치 성향','race_ethnicity_nationality':'인종·민족·국적','religion':'종교','ses':'사회경제적 지위','sexual_orientation':'성적 지향'}
plt.rcParams.update({'font.family':'AppleGothic','axes.unicode_minus':False,'font.size':11,'svg.fonttype':'path','svg.hashsalt':'emotion1p5bD'})
fig,axes=plt.subplots(1,2,figsize=(13,7.6),sharex=True,sharey=True)
order=list(names)
for ax,path,title in zip(axes,['user','model'],['사용자 불안 - 사용자 중립','모델 불안 - 모델 중립']):
    g=categories[(categories.path==path)&(categories.emotion=='anxiety')].set_index('cat').loc[order]
    for i,(_,r) in enumerate(g.iterrows()):
        ax.errorbar(r.est,11-i,xerr=[[r.est-r.lo],[r.hi-r.est]],fmt='o',color='#657286',markerfacecolor='white',capsize=3)
    ax.set_title(title,pad=15);ax.set_yticks(range(12),[names[x] for x in order[::-1]])
    ax.axvline(0,color='#516174',linestyle='--',lw=1);ax.set_xlim(-22,36);ax.set_ylim(-.7,11.7)
    ax.set_xlabel('중립 대비 ‘알 수 없음’ 확률 변화 (%p)');ax.grid(axis='x',alpha=.2)
    for side in ['top','right','left']:ax.spines[side].set_visible(False)
fig.subplots_adjust(left=.15,right=.98,bottom=.12,top=.89,wspace=.17)
fig.suptitle('1.5B · 범주별 불안 효과 · 개별 범주는 모두 BH 보정 후 유의하지 않음',fontsize=14)
for ext in ['svg','png']:fig.savefig(out/f'results-1p5b-category.{ext}',dpi=170,facecolor='white',metadata={'Date':None} if ext=='svg' else None)
plt.close(fig)

def table(headers,rows):
    return '<div class="scroll"><table><thead><tr>'+''.join(f'<th>{x}</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{x}</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def details(title,body,identity=''):
    return f'<details class="result-group"'+(f' id="{identity}"' if identity else '')+f'><summary>{title}</summary><div class="result-body">{body}</div></details>'

hetero=table(['確証 가설','순열 p','Holm p','판정'],[[label,f"{r['perm_p']:.4f}",f"{r['p_holm']:.4f}",'유의' if r['p_holm']<.05 else '유의하지 않음'] for label,r in zip(['사용자 불안 효과의 범주 간 차이','모델 불안 효과의 범주 간 차이'],summary['D_conf'])]).replace('確証','확증')
body='<p>12개 KoBBQ 범주마다 모호 40문항과 명확 10문항을 고정 표집해 총 모호 480개·명확 120개를 측정했다. 생활 맥락이나 모델 운영 단계와는 다른 범주 분석이다. B와 달리 천장 문항을 사전에 제외하지 않았다.</p>'+hetero+'''<p><strong>사용자 불안과 모델 불안 모두 범주 간 효과 차이가 유의했다.</strong> 이는 불안 효과가 모든 범주에서 같다는 가설에 반하는 결과다. 특정 범주에서 중립 대비 효과가 확립됐다는 뜻은 아니다. 개별 범주 효과는 5개 경로·정서 비교의 60행 모두 각 12범주 내 BH 보정 후 유의하지 않았다.</p>
<figure class="result-figure"><img src="results-1p5b-category.svg" alt="12개 KoBBQ 범주별 1.5B 사용자 및 모델 불안 효과와 95% 신뢰구간. 모든 개별 범주는 BH 보정 후 유의하지 않음."><figcaption>가로선은 보정하지 않은 95% 신뢰구간, 빈 점은 BH 보정 후 비유의다. 범주 간 이질성 검정과 개별 범주 검정은 서로 다른 질문이다. 축 범위는 7B 범주 그림과 같다.</figcaption></figure>
<p>사용자 불안의 점추정치는 가족 형태 −0.19%p부터 종교 +7.18%p까지, 모델 불안은 가족 형태 −1.11%p부터 성별 정체성 +5.09%p까지였다. 범주별 정서 자극 배정 차이와 템플릿 변형 문항 간 의존성을 별도로 통제한 검증은 아니므로, 범주 차이의 원인을 단정하지 않는다.</p>'''
for path,emotion in [('user','anxiety'),('user','fear'),('model','anxiety'),('model','fear'),('model','sadness')]:
    g=categories[(categories.path==path)&(categories.emotion==emotion)]
    rows=[[names[r.cat],f'{r.est:+.2f}',f'[{r.lo:+.2f}, {r.hi:+.2f}]',f'{r.p:.4f}',f'{r.q_BH:.4f}','유의하지 않음'] for r in g.itertuples()]
    body+=details(('사용자' if path=='user' else '모델')+' '+{'anxiety':'불안','fear':'공포','sadness':'슬픔'}[emotion]+' · 12범주 수치',table(['범주','효과 (%p)','95% 신뢰구간 (%p)','보정 전 p','BH q','판정'],rows))
labelrows=[['사용자' if r['path']=='user' else '모델',r['lab'],f"{100*r['est']:+.2f}",f"[{100*r['lo']:+.2f}, {100*r['hi']:+.2f}]",f"{r['p']:.4f}"] for r in summary['label']]
explore=table(['대상','KoBBQ 구분','불안 효과 (%p)','95% 신뢰구간 (%p)','보정 전 p'],labelrows)+'''<p>NC는 한국 신규 범주, ST는 문화적 번역 후 전용, TM은 대상 집단 수정 문항이다. 여섯 탐색 비교 모두 보정 전에도 유의하지 않았다. 집단 간 효과 차이나 문화적 보편성·동등성을 입증한 결과는 아니다. 문항 구분과 범주가 얽혀 있어 문화 차이로 단정하지 않는다.</p>'''
explore+=table(['천장 제외 민감도','효과 (%p)','95% 신뢰구간 (%p)','보정 전 p'],[[('사용자 불안' if 'user' in r['index'] else '모델 불안'),f"{100*r['est']:+.2f}",f"[{100*r['lo']:+.2f}, {100*r['hi']:+.2f}]",f"{r['p']:.4f}"] for r in summary['sensitivity']])
explore+=f"<p>천장 제외 후 {summary['non_ceiling_items']}/480문항에서 사용자 불안 +3.20%p와 모델 불안 +1.94%p 모두 유의하지 않았다. 같은 D 표본의 부분집합 분석이며 독립 재현이 아니다.</p>"
descriptive=[]
for path,base,cs in [('사용자','neutral',['anxiety','fear']),('모델','model_neutral',['model_anxiety','model_fear','model_sadness'])]:
    for cls in cs:
        amb=(frames[cls,'amb'].p_unk.mean()-frames[base,'amb'].p_unk.mean())*100
        dis=(frames[cls,'dis'].correct.mean()-frames[base,'dis'].correct.mean())*100
        descriptive.append([path,{'anxiety':'불안','fear':'공포','sadness':'슬픔'}[cls.replace('model_','')],f'{amb:+.2f}',f'{frames[cls,"dis"].correct.mean()*100:.2f}%',f'{dis:+.2f}'])
explore+=table(['대상','정서','모호 전체 평균 차이 (%p)','명확 문항 정답률','명확 정답률 중립 대비 차이 (%p)'],descriptive)+'<p>이 표는 기술 통계다. 전체 평균이나 명확 문항 정확도의 차이에 새 유의성 검정을 추가하지 않았다. 판단 유보 변화가 곧 전반적 능력 향상 또는 고정관념 감소라는 의미는 아니다.</p>'
# Independently check stored label and sensitivity point estimates.
lab_map=dict(zip(ss.sample_id,ss.label_annotation))
for r in summary['label']:
    cls='anxiety' if r['path']=='user' else 'model_anxiety';base='neutral' if r['path']=='user' else 'model_neutral'
    means=[frames[c,'amb'].loc[frames[c,'amb'].item.map(lab_map).eq(r['lab']),'p_unk'].mean() for c in [cls,base]]
    assert abs(means[0]-means[1]-r['est'])<1e-5
ok=set(frames['none','amb'].loc[lambda d:d.p_unk<.95,'item'])
assert len(ok)==summary['non_ceiling_items']
for r,cls,base in zip(summary['sensitivity'],['anxiety','model_anxiety'],['neutral','model_neutral']):
    means=[frames[c,'amb'].loc[frames[c,'amb'].item.isin(ok),'p_unk'].mean() for c in [cls,base]]
    assert abs(means[0]-means[1]-r['est'])<1e-5
when=datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y-%m-%d %H:%M KST')
validation=f'''<p>{when} 검증. D 측정 15파일의 문항 수·문항당 행 수·문항/자극 키와 배정·확률 범위·합 1·표본 해시를 확인했다. 중복은 0행이다. 범주별 60개 점추정치와 BH, 확증 2개의 Holm, 문항 구분·천장 제외의 점추정치를 대조했다. 저장된 분석을 사용했으며 모델 추론과 통계 검정을 재실행하지 않았다.</p>
<p>노트북 파일의 마지막 셀 실행 번호는 아직 자동 저장되지 않았지만, 15조건 저장 완료, category_D.csv·summary_D.json의 생성과 마지막 커널 활동 후 idle 상태를 함께 확인했다. 오래된 노트북 체크포인트를 완료 근거로 삼지 않았다.</p>
<p>A·B·D 측정·분석은 완료됐다. C는 개정 전 파일 부족으로 비교가 미성립인 제한을 유지한다. A/B와 D의 표본은 독립 재현으로 가정하지 않으며, 사용자·모델 경로와 모델 규모 간 효과 차이는 별도로 검정하지 않았다.</p>'''
section=details('완료 분석 · 블록 D · 범주별 효과',body,'results-1p5b-D')+details('별도 탐색 · 한국 문항 구분·천장 제외·명확 문항',explore,'results-1p5b-D-exploratory')+details('완료 검증 · 자료 품질과 해석 범위',validation,'results-1p5b-progress')
page=out/'index.html';soup=BeautifulSoup(page.read_text(),'html.parser');old=soup.find(id='results-1p5b-progress');assert old is not None
for i in ['results-1p5b-D','results-1p5b-D-exploratory']:
    e=soup.find(id=i)
    if e:e.decompose()
old.replace_with(BeautifulSoup(section,'html.parser'))
parent=soup.find(id='results-model-1p5b');parent.find('summary',recursive=False).string='1.5B · Qwen2.5 · A·B·D 결과 검증 완료 · C 비교 미성립'
body_el=parent.find('div',recursive=False)
body_el.find('p',class_='lead',recursive=False).string='A·B의 중립 대비 정서 효과는 유의하지 않았다. D에서는 사용자·모델 불안 효과의 범주 간 차이가 유의했으나, 개별 범주 효과는 모두 BH 보정 후 유의하지 않았다. C는 개정 전 자료 부족으로 비교가 성립하지 않았다.'
body_el.find('p',class_='muted',recursive=False).string=f'최종 저장 결과 확인 {when}. A·B는 summary.json, D는 summary_D.json과 category_D.csv를 사용했다. C의 제한과 이전 설계 결과는 별도 항목에 유지했다.'
body_el.find('div',class_='note',recursive=False).string='예정된 측정과 A·B·D 통계 분석의 저장·자료 검증이 끝났다. C의 전후 비교는 미성립이다. 평균 효과, 범주 간 이질성, 개별 범주 효과의 질문과 보정 방법을 구분한다. 감정 경험이나 인과적 매개를 입증한 결과는 아니다.'
body_el.append(BeautifulSoup('<p><a href="results-1p5b-D.json">D 최종 수치·검증·출처 해시</a> · <a href="results-1p5b-D.csv">D 범주별 전체 수치</a> · <a href="build_results_1p5b_D.py">D 검증·그래프 생성 코드</a></p>','html.parser'))
text=str(soup).replace('1.5B 최신 v5는 A·B 완료, C 비교 자료 부족, D 진행 중이다.','1.5B 최신 v5는 A·B·D 결과 검증 완료, C 비교 자료 부족이다.')
text=text.replace('D는 진행 중이다. 7B v5의 완료된 블록 B에서는','1.5B D의 불안 효과는 사용자·모델 모두 범주 간 차이가 유의했으나 개별 범주는 BH 보정 후 모두 비유의였다. 7B v5의 완료된 블록 B에서는')
page.write_text(text)
(out/'results-1p5b-D.csv').write_bytes((source/'category_D.csv').read_bytes())
for name in ['summary_D.json','category_D.csv']:
    f=source/name;audit.append(dict(file=str(f.relative_to(root)),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
payload=dict(model=summary['model'],checked_at=when,status='A/B/D complete and validated; C before data unavailable',D_summary=summary,D_categories=categories.to_dict('records'),D_validation=audit,descriptive=descriptive,sample_sha256=summary['sample_sha256'])
(out/'results-1p5b-D.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
print('Validated all 15 D files, 60 category estimates, BH/Holm and label/sensitivity point estimates; final report generated.')
