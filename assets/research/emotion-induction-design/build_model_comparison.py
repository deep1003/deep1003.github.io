"""Compare validated final v5 summaries without adding cross-model significance tests."""
import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

out = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('source_root', type=Path, help='fear_axis_pilot directory; read only')
root = parser.parse_args().source_root
filenames = ['results-1p5b-BC.json', 'results-1p5b-D.json', 'results-7b.json',
             'results-1p5b-D.csv', 'results-7b-D.csv']
sources = [dict(file=n, sha256=hashlib.sha256((out/n).read_bytes()).hexdigest()) for n in filenames]
baselines = []
for folder in ['outputs_1p5b_v5', 'outputs_7b_v5']:
    values = []
    for filename, n, per, metric in [('base_none_amb.csv',400,1,'p_unk'),
                                     ('user_neutral_amb.csv',400,4,'p_unk'),
                                     ('base_none_dis.csv',100,1,'correct')]:
        f = root/folder/filename
        d = pd.read_csv(f)
        assert len(d)==n*per and d.item.nunique()==n and not d.duplicated(['item','stim']).any()
        assert np.isfinite(d[['p_bias','p_anti','p_unk']]).all().all()
        assert np.allclose(d.p_bias+d.p_anti+d.p_unk,1,atol=1e-5)
        values.append(float(d[metric].mean()))
        sources.append(dict(file=str(f.relative_to(root)),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
    baselines.append(values)
small = json.loads((out/filenames[0]).read_text())['summary']
ds = json.loads((out/filenames[1]).read_text())['D_summary']
large_all = json.loads((out/filenames[2]).read_text())
large, dl = large_all['summary'], large_all['D_summary']
assert small['model'] == 'Qwen/Qwen2.5-1.5B-Instruct'
assert large['model'] == 'Qwen/Qwen2.5-7B-Instruct'
assert ds['sample_sha256'] == dl['sample_sha256']
cats = [pd.read_csv(out/n) for n in filenames[3:]]
assert all(len(d) == 60 and not d.duplicated(['path','emotion','cat']).any() for d in cats)
assert set(map(tuple,cats[0][['path','emotion','cat']].values)) == set(map(tuple,cats[1][['path','emotion','cat']].values))
assert all((d.q_BH >= .05).all() for d in cats)
comparisons = []
for i, (key, idx, label) in enumerate([('A',0,'사용자 불안'),('A',1,'사용자 공포'),
                                      ('B',0,'모델 불안'),('B',1,'모델 공포'),('B_exp',0,'모델 슬픔 (탐색)')]):
    r = [d[key][idx] for d in [small,large]]
    comparisons.append(dict(label=label, small=r[0], large=r[1], exploratory=key=='B_exp'))

plt.rcParams.update({'font.family':'AppleGothic','axes.unicode_minus':False,'font.size':11,
                     'svg.fonttype':'path','svg.hashsalt':'emotion-modelcomparison'})
fig, ax = plt.subplots(figsize=(11,6.5))
fig.subplots_adjust(left=.24,right=.97,top=.88,bottom=.13)
for key, color, shift, name in [('small','#496b9c',.13,'1.5B'),('large','#b16b35',-.13,'7B')]:
    for i,row in enumerate(comparisons):
        r=row[key]; y=4-i+shift; sig=r.get('p_holm',r['p'])<.05
        ax.errorbar(100*r['est'],y,xerr=[[100*(r['est']-r['lo'])],[100*(r['hi']-r['est'])]],
                    fmt='o',color=color,markerfacecolor=color if sig else 'white',capsize=4,
                    markersize=7,label=name if i==0 else None)
ax.set_yticks(range(5),[r['label'] for r in comparisons[::-1]])
ax.set_xlim(-12,24);ax.set_ylim(-.6,4.6);ax.axvline(0,color='#516174',linestyle='--',lw=1)
ax.set_xlabel('각 모델의 대응 중립 대비 ‘알 수 없음’ 확률 변화 (%p)')
ax.set_title('최신 v5 · 모델별 효과와 95% 신뢰구간',pad=18)
ax.grid(axis='x',alpha=.18);ax.legend(loc='upper right',frameon=False)
for side in ['top','right','left']:ax.spines[side].set_visible(False)
for ext in ['svg','png']:fig.savefig(out/f'results-model-comparison.{ext}',dpi=170,facecolor='white',metadata={'Date':None} if ext=='svg' else None)
plt.close(fig)

def table(headers, rows):
    return '<div class="scroll"><table><thead><tr>'+''.join(f'<th>{x}</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{x}</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def effect(r, exploratory):
    p=r['p'] if exploratory else r['p_holm']
    return f"{100*r['est']:+.2f} [{100*r['lo']:+.2f}, {100*r['hi']:+.2f}]<br>{'미보정' if exploratory else 'Holm'} p = {p:.4f}"

ab = table(['대상·정서 − 대응 중립','1.5B 효과·95% CI (%p)','7B 효과·95% CI (%p)'],
           [[r['label'],effect(r['small'],r['exploratory']),effect(r['large'],r['exploratory'])] for r in comparisons])
hetero = table(['D 범주 간 불안 효과 차이','1.5B Holm p','7B Holm p','비교 해석'],
              [[label,f"{ds['D_conf'][i]['p_holm']:.4f}",f"{dl['D_conf'][i]['p_holm']:.4f}",txt]
               for i,label,txt in [(0,'사용자 불안','1.5B에서만 유의하나 모델 간 차이를 직접 검정하지 않음'),
                                    (1,'모델 불안','두 모델 모두 유의')]])
baseline_table = table(['기준선 비교','1.5B','7B'],
    [[name,f'{100*baselines[0][i]:.2f}%',f'{100*baselines[1][i]:.2f}%']
     for i,name in enumerate(['모호 문항 P(알 수 없음) · 자극 없음','모호 문항 P(알 수 없음) · 사용자 중립','명확 문항 정확도 · 자극 없음'])])
drows=[]
for path,emotion in [('user','anxiety'),('user','fear'),('model','anxiety'),('model','fear'),('model','sadness')]:
    vals=[float(d[(d.path==path)&(d.emotion==emotion)].est.mean()) for d in cats]
    drows.append([('사용자' if path=='user' else '모델')+' '+{'anxiety':'불안','fear':'공포','sadness':'슬픔'}[emotion],
                  f'{vals[0]:+.2f}',f'{vals[1]:+.2f}'])
dt=table(['D 같은 480문항의 전체 평균 차이','1.5B (%p)','7B (%p)'],drows)
when=datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y-%m-%d %H:%M KST')
section=f'''<section id="model-comparison" aria-labelledby="model-comparison-title">
<h2 id="model-comparison-title">9. 1.5B와 7B 최종 결과 비교</h2>
<p class="lead">두 모델 모두 사용자 정서 A와 모델 공포·슬픔 B의 중립 대비 효과는 유의하지 않았다. 모델 불안 효과의 범주 간 차이는 공통으로 나타났다. 평균적인 모델 불안 효과는 7B에서만 유의했지만, 모델 규모 자체가 원인이라는 결론은 아직 이르다.</p>
<p class="muted">{when} 비교. 최신 v5의 검증된 A·B·D 결과만 비교한다. 과거 800문항·15자극 실험은 합치지 않았다. 1.5B의 C는 개정 전 자료가 없어 전후 비교 미성립이다.</p>
<figure class="result-figure"><img src="results-model-comparison.svg" alt="두 모델의 최신 A/B 효과와 95% 신뢰구간 비교. 7B 모델 불안만 Holm 보정 후 유의하며 다른 중립 대비 효과는 유의하지 않음."><figcaption>파랑은 1.5B, 갈색은 7B. 채운 점은 해당 모델 내 검정에서 유의함, 빈 점은 비유의다. 95% 구간은 다중비교 보정 구간이 아니다. 한쪽만 유의하다는 사실은 모델 간 효과 차이가 유의하다는 뜻이 아니다.</figcaption></figure>
{ab}
<details class="result-group" open><summary>공통 결과 · 무엇이 두 모델에서 반복됐는가?</summary><div class="result-body">
<ul><li><strong>사용자 불안·공포 A:</strong> 두 모델 모두 중립 대비 효과를 확인하지 못했다. 사용자 메시지를 읽는 것만으로 사회적 판단이 일관되게 바뀐다는 근거는 이번 최신 실행에서 확보하지 못했다.</li>
<li><strong>모델 공포·슬픔 B:</strong> 두 모델 모두 중립 대비 유의하지 않았다. 공포 추정치는 음수, 슬픔은 작은 양수로 방향도 같지만 효과 없음이나 조건 간 동등성이 입증된 것은 아니다.</li>
<li><strong>모델 불안의 범주 간 차이 D:</strong> 두 모델 모두 유의했다. 동시에 개별 범주 효과는 두 모델 각각 60개 비교 모두 BH 보정 후 유의하지 않았다. 범주 간 이질성과 특정 범주의 효과를 구분해야 한다.</li>
<li><strong>고정관념 선호:</strong> A·B의 불안·공포는 두 모델 모두 ±3%p 동등성을 확립하지 못했다. 판단 유보를 곧 편향 감소로 해석할 수 없다.</li></ul>
</div></details>
<details class="result-group" open><summary>모델별 차이 · 가장 뚜렷한 대비와 해석의 범위</summary><div class="result-body">
<p><strong>B 모델 불안은 1.5B +2.62%p(Holm p = .2150), 7B +12.00%p(p = .0250)였다.</strong> 7B에서만 판단 유보 증가를 확인했다. 하지만 B 표본은 각각 652개와 139개로, 같은 선별 규칙을 적용해도 서로 다른 문항이 남았다. 모델 규모와 표본 구성의 효과를 분리하지 못하므로 ‘큰 모델이 불안에 더 민감하다’는 확정 결론은 아니다.</p>
{hetero}
<p>사용자 불안의 범주 간 차이는 1.5B에서만 유의했다. 이것도 모델 간 이질성 차이를 직접 검정한 결과는 아니다. 공포 − 불안의 탐색 비교는 두 모델 모두 음수였지만, 보정 전 결과이며 정서 기제의 차이를 확립한 근거로 삼지 않는다.</p>
{baseline_table}
<p>7B는 중립 조건에서 이미 판단 유보 확률이 높다. 따라서 두 모델은 정서 자극 이전의 출발점부터 다르며, 확률이 더 증가할 여지도 다르다. 이 천장 가능성이 사용자 정서의 비유의 결과를 설명한다고 직접 검증한 것은 아니다. 기준선 정확도 차이만으로 모델의 전반적 지능 차이를 판단하지 않는다.</p>
</div></details>
<details class="result-group"><summary>같은 D 표본에서 비교 · 표본 차이를 줄여도 남는 패턴</summary><div class="result-body">
<p>D는 두 모델이 같은 표본 해시의 모호 480문항·명확 120문항과 같은 자극 배정 규칙을 사용했다. B보다 모델 비교에 적합한 조건이지만, 아래 수치는 기술 통계이며 모델 간 직접 검정이나 신뢰구간은 새로 계산하지 않았다.</p>{dt}
<p>같은 D 문항에서도 모델 불안의 중립 대비 평균은 7B +6.55%p, 1.5B +2.02%p로 7B가 더 컸다. 이는 후속 검증의 단서다. 두 효과의 차이가 유의하다고 판정하지 않는다.</p>
<p>사용자 공포는 1.5B −2.38%p와 7B +3.05%p로 평균 방향이 달랐다. 모델 공포도 −1.26%p와 +0.44%p였다. 방향 차이 자체에 대한 검정은 없으므로 ‘규모가 커질수록 모든 위협 반응이 강해진다’는 단일 설명으로 묶지 않는다.</p>
<p>천장 제외 민감도에서도 7B 모델 불안 +16.49%p(95% CI [6.97, 26.20], 미보정 p = .0005)는 유의했으나 1.5B +1.94%p([−1.19, 4.90], p = .2055)는 유의하지 않았다. 다만 남은 문항은 각각 133개와 470개로 다시 달라지므로 동일 표본 비교가 아니다.</p>
<p>7B 모델 불안의 NC·ST 탐색 비교는 보정 전 유의했고 1.5B는 세 문항 구분 모두 비유의였다. 문항 구분과 범주가 얽혀 있고 직접 차이·동등성 검정도 없어 문화적 보편성이나 한국 특수성을 입증하지 않는다.</p>
</div></details>
<div class="note"><strong>연구 해석.</strong> 현재 가장 일관된 단서는 ‘임박한 공포가 편향을 일괄 증폭한다’는 패턴보다 ‘불안 관련 판단 변화가 정서 대상과 문항 범주에 따라 달라진다’는 패턴이다. 내부 정서 벡터의 추출·조향이나 매개 분석 결과는 여기에 없으므로 실제 감정 경험 또는 인과적 정서 기제를 주장하지 않는다. 모델 차이를 확증하려면 동일 문항·자극을 짝지은 모델 × 정서 상호작용 검정이 필요하다.</div>
<p><a href="results-model-comparison.json">비교 수치와 출처 해시</a> · <a href="build_model_comparison.py">비교 그래프 생성 코드</a></p>
</section>'''
page=out/'index.html';soup=BeautifulSoup(page.read_text(),'html.parser')
old=soup.find(id='model-comparison')
if old:old.decompose()
soup.find('footer').insert_before(BeautifulSoup(section,'html.parser'))
old_link = soup.find(id='model-comparison-link')
if old_link:old_link.decompose()
soup.find(id='results-title').insert_after(BeautifulSoup('<p id="model-comparison-link"><a href="#model-comparison">1.5B·7B 최종 비교 요약과 그래프 보기</a></p>','html.parser'))
page.write_text(str(soup))
(out/'results-model-comparison.json').write_text(json.dumps(dict(checked_at=when,scope='validated final v5 A/B/D; no new cross-model inference',AB=comparisons,baseline_metrics=['P_unknown_none_amb','P_unknown_neutral_amb','accuracy_none_dis'],baselines=baselines,D_sample_sha256=ds['sample_sha256'],D_heterogeneity=[ds['D_conf'],dl['D_conf']],D_descriptive=drows,sources=sources),ensure_ascii=False,indent=2)+'\n')
print('Validated matching D keys and sample hash; generated comparison and added summary section.')
