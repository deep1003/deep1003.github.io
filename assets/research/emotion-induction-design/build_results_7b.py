"""완료된 7B v5 요약을 게시하고 미완료 층화 실험은 별도로 표시한다."""
import argparse
import hashlib
import html
import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('source_root', type=Path)
args = parser.parse_args()
out = Path(__file__).resolve().parent
root = args.source_root
source = root / 'outputs_7b_v5'
s = json.loads((source / 'summary.json').read_text())
assert s['model'] == 'Qwen/Qwen2.5-7B-Instruct' and s['gate']
files = [source / 'blockB60v5_mc.csv', source / 'summary.json', root / 'stimuli_v2.json', root / 'stimuli_model_v5.json']
audit = []
for prefix, classes, count, per in [
    ('user', ['neutral', 'anxiety', 'fear'], 400, 4),
    ('model60v5', ['model_neutral', 'model_anxiety', 'model_fear', 'model_sadness'], s['items_B'], 4),
]:
    for cls in classes:
        for ctx, n, k in [('amb', count, per), ('dis', 100, 2 if prefix == 'model60v5' else 4)]:
            f = source / f'{prefix}_{cls}_{ctx}.csv'
            d = pd.read_csv(f)
            assert len(d) == n * k and d.item.nunique() == n
            assert not d.duplicated(['item_idx', 'stim']).any()
            assert d.groupby('item_idx').size().eq(k).all()
            assert d[['p_bias', 'p_anti', 'p_unk']].notna().all().all()
            assert ((d.p_bias + d.p_anti + d.p_unk - 1).abs() < 1e-5).all()
            if ctx == 'amb':
                estimates = {r['index'].split()[1]: r['est'] for r in s['A' if prefix == 'user' else 'B']}
                audit.append({'file': str(f.relative_to(root)), 'rows': len(d), 'items': n, 'p_unknown': float(d.p_unk.mean())})
            files.append(f)
# 요약의 점추정치와 원자료 평균을 독립적으로 대조한다.
for prefix, key, base in [('user', 'A', 'neutral'), ('model60v5', 'B', 'model_neutral')]:
    b = pd.read_csv(source / f'{prefix}_{base}_amb.csv').p_unk.mean()
    for r in s[key]:
        cls = r['index'].split()[1]
        v = pd.read_csv(source / f'{prefix}_{cls}_amb.csv').p_unk.mean() - b
        assert abs(v-r['est']) < 1e-5

def rows(records, labels, exploratory=False):
    return [dict(r, label=label, adjustment='미보정' if exploratory else 'Holm',
                 analysis='탐색' if exploratory else '확증', significant=r.get('p_holm', r['p']) < .05)
            for r, label in zip(records, labels)]
user = rows(s['A'], ['불안', '공포'])
model = rows(s['B'], ['불안', '공포']) + rows(s['B_exp'][:1], ['슬픔'], True)
plt.rcParams.update({'font.family': 'AppleGothic', 'axes.unicode_minus': False, 'font.size': 12, 'svg.fonttype': 'path', 'svg.hashsalt': 'emotion7b'})

def forest(data, filename):
    fig, ax = plt.subplots(figsize=(10, 1.1*len(data)+1.7))
    fig.subplots_adjust(left=.29, right=.97, bottom=.20, top=.94)
    ax.axvline(0, color='#516174', linestyle='--', linewidth=1.3)
    for i, r in enumerate(data):
        y = len(data)-i-1
        color = '#176b62' if r['significant'] else '#657286'
        ax.errorbar(100*r['est'], y, xerr=[[100*(r['est']-r['lo'])], [100*(r['hi']-r['est'])]], fmt='o', color=color,
                    markerfacecolor=color if r['significant'] else 'white', markersize=9, capsize=5, linewidth=2)
        ax.annotate(f"{100*r['est']:+.1f} [{100*r['lo']:+.1f}, {100*r['hi']:+.1f}]", (100*r['est'], y), xytext=(0,14), textcoords='offset points', ha='center', color=color, fontsize=11)
    ax.set_yticks(range(len(data)), [r['label'] for r in data[::-1]])
    ax.set_ylim(-.6,len(data)-.3)
    ax.set_xlim(-12,24)
    ax.set_xticks([-10,-5,0,5,10,15,20])
    ax.set_xlabel('중립 대비 ‘알 수 없음’ 확률 변화 (%p)')
    ax.grid(axis='x',alpha=.18)
    for side in ['top','right','left']:ax.spines[side].set_visible(False)
    ax.tick_params(axis='y',length=0,pad=12)
    for ext in ['svg','png']:fig.savefig(out/f'{filename}.{ext}',dpi=170,facecolor='white',metadata={'Date':None} if ext=='svg' else None)
    plt.close(fig)
forest(user,'results-7b-user')
forest(model,'results-7b-model')

def table(data):
    body=''.join(f"<tr><th scope='row'>{r['label']}</th><td>{100*r['est']:+.2f}</td><td>[{100*r['lo']:+.2f}, {100*r['hi']:+.2f}]</td><td>{r['analysis']}</td><td>{r['adjustment']} p = {r.get('p_holm',r['p']):.4f}</td><td>{'유의' if r['significant'] else '유의하지 않음'}</td></tr>" for r in data)
    return '<div class="scroll"><table><thead><tr><th>정서 조건</th><th>효과 (%p)</th><th>95% 신뢰구간 (%p)</th><th>분석 구분</th><th>유의성 기준</th><th>판정</th></tr></thead><tbody>'+body+'</tbody></table></div>'
progress=[]
for f in sorted(source.glob('strat*.csv')):
    d=pd.read_csv(f)
    progress.append({'file':f.name,'items':int(d.item.nunique()),'rows':len(d),'duplicate_rows':int(d.duplicated(['item_idx','stim']).sum())})
when=datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y-%m-%d %H:%M KST')
eq=''
for who,key in [('사용자','A_eq'),('모델 자신','B_eq')]:
    for emotion,r in zip(['불안','공포'],s[key]):
        eq+=f"<tr><th>{who} · {emotion}</th><td>{100*r['est']:+.2f}</td><td>[{100*r['ci90_lo']:+.2f}, {100*r['ci90_hi']:+.2f}]</td><td>{'확립' if r['equivalent (±3pp)'] else '미확립'}</td></tr>"
progress_html=''.join(f"<tr><td>{html.escape(r['file'])}</td><td>{r['items']}</td><td>{r['duplicate_rows']}</td></tr>" for r in progress)
block=f'''<details class="model-results" id="results-model-7b"><summary>7B · Qwen2.5 · 중간 보고 · A·B·C 완료, D 진행 중</summary><div class="result-body">
<p class="lead">최신 v5의 모델 불안은 중립 대비 판단 유보 확률을 +12.00%p 높였다. 사용자 불안·공포와 모델 공포·슬픔은 유의하지 않았다.</p>
<p class="muted">확인 시각 {when}. 아래 확증 결과는 완료된 블록 A·B이며, 전체 7B 실험의 최종 보고가 아니다. 기존 개정 전 결과와 최신 v5 결과를 구분한다.</p>
<div class="note">● 채운 초록 점은 표의 기준에서 유의함, ○ 빈 회색 점은 유의하지 않음을 뜻한다. 가로선은 95% 신뢰구간, 점선은 효과 0이다. 불안·공포는 경로별 두 확증 비교에 Holm 보정, 슬픔은 미보정 탐색 비교다. 신뢰구간은 다중비교 보정 구간이 아니다. 두 7B 그래프의 축은 −12~24%p로 같으며, 1.5B 그래프의 −12~16%p와 다르므로 숫자를 기준으로 읽는다.</div>
<details class="result-group" id="results-7b-user"><summary>사용자 정서 비교 · 불안·공포 대 사용자 중립</summary><div class="result-body">
<figure class="result-figure"><img src="results-7b-user.svg" alt="7B 사용자 불안 +0.08%p, 공포 +2.47%p. 모두 유의하지 않음."><figcaption>모호 문항 400개, 문항당 조건별 자극 4개. 사용자 슬픔은 블록 A에서 실행하지 않았다.</figcaption></figure>
{table(user)}
<p><strong>두 조건 모두 유의하지 않다.</strong> 불안은 +0.08%p, 공포는 +2.47%p지만 두 신뢰구간 모두 0을 포함한다. 사용자 메시지를 읽은 뒤 판단이 변한다는 근거를 이 표본에서 확보하지 못했다. 효과가 없다고 입증한 것은 아니다.</p>
<p>중립에서 이미 ‘알 수 없음’ 선택 확률이 약 82%여서 증가 여지가 제한될 수 있다. 그러나 천장 효과가 비유의 결과의 원인임을 검증한 분석은 아니다. 사용자 정서 메시지의 효과를 모델 자신의 감정 경험으로 해석하지 않는다.</p>
</div></details>
<details class="result-group" id="results-7b-self"><summary>모델 자기 정서 비교 · 불안·공포·슬픔 대 모델 중립 · 최신 v5</summary><div class="result-body">
<figure class="result-figure"><img src="results-7b-model.svg" alt="7B 모델 불안 +12.00%p, 95% 신뢰구간 2.91에서 21.61로 유의. 공포와 슬픔은 유의하지 않음."><figcaption>선별한 모호 문항 139개, 정서 유형당 자극 60개, 문항당 4개. 모델 대상 공지는 시스템 메시지에 배치했다.</figcaption></figure>
{table(model)}
<p><strong>유의한 결과.</strong> 모델 대상 불안 공지는 중립 대비 ‘알 수 없음’ 확률을 +12.00%p 높였다. 95% 신뢰구간은 [+2.91, +21.61]%p이며 Holm p = .0250이다. 모호 문항에서는 ‘알 수 없음’이 정답이므로 이 표본의 정답 선택 확률을 높이는 방향이다. 일반적인 추론 능력 향상이나 실제 불안 경험이 입증된 것은 아니다.</p>
<p><strong>유의하지 않은 결과.</strong> 공포 −1.30%p와 슬픔 +1.72%p는 신뢰구간이 0을 포함한다. 공포·슬픔의 무효과 또는 불안에만 고유한 기제가 입증됐다고 결론 내리지 않는다. 특히 슬픔 비교는 탐색 분석이다.</p>
<p>문항은 자극 없음 조건에서 P(알 수 없음) &lt; .95인 139개를 선별했다. 따라서 이 효과는 해당 표본에 관한 결과이며, 블록 A의 무선 표본이나 KoBBQ 전체로 그대로 일반화하지 않는다. 사용자와 모델 경로 사이 효과 차이를 직접 검정한 결과도 아니다.</p>
<details class="result-group"><summary>탐색 비교와 새 자극 민감도 분석</summary><div class="result-body"><p>공포 − 불안은 −13.30%p, 95% 신뢰구간 [−22.22, −3.85], 보정 전 p = .0085였다. 중립 대비 확증 비교와 구분한다. 새로 추가한 자극만 사용한 불안 − 중립은 +11.13%p [1.11, 21.36], 보정 전 p = .0265로 같은 방향이었다. 같은 문항을 사용하는 민감도 분석이므로 독립된 재현 실험으로 세지 않는다.</p></div></details>
</div></details>
<details class="result-group" id="results-7b-bias"><summary>별도 지표 · 고정관념 선호와 조작 점검</summary><div class="result-body"><p>고정관념 선호는 P(고정관념) − P(반고정관념)의 중립 대비 변화다. 동등성은 90% 신뢰구간이 사전 범위 ±3%p 안에 포함되는지로 판단한다.</p>
<div class="scroll"><table><thead><tr><th>대상·정서</th><th>효과 (%p)</th><th>90% 신뢰구간 (%p)</th><th>±3%p 동등성</th></tr></thead><tbody>{eq}</tbody></table></div>
<p>네 비교 모두 동등성을 확립하지 못했다. 이는 편향이 증가했다는 증거가 아니다. 판단 유보 증가를 고정관념 선호 감소로 해석할 수도 없다.</p><p>사용자·모델 조작 점검의 이해 문항 정확도는 모두 100%였다. 이는 공지 내용을 구분했다는 점검이며 실제 감정을 경험했다는 증거가 아니다.</p></div></details>
<details class="result-group" id="results-7b-progress"><summary>미완료 분석 · 블록 D 범주별 결과와 데이터 점검</summary><div class="result-body"><p>블록 D는 12개 KoBBQ 범주별 모호 문항 40개와 명확 문항 10개를 사용한다. 사용자 생활 맥락이나 모델 운영 단계의 구분과는 다른 범주 분석이다. 일부 조건만 저장돼 전체 분석은 미완료다.</p><p><strong>중복 저장 행이 발견돼 D의 효과 크기·신뢰구간·유의성은 아직 게시하지 않는다.</strong> 동시에 실행된 별도 재개 커널을 중지해 추가 중복을 막았다. 원본 CSV는 보존했으며, 아래는 확인 시점의 저장 현황이다. 중복 행을 독립 관측으로 취급하면 일부 문항의 가중치가 커지므로 정리·검증 후 분석해야 한다.</p><div class="scroll"><table><thead><tr><th>저장 파일</th><th>서로 다른 문항 수</th><th>추가 중복 행</th></tr></thead><tbody>{progress_html}</tbody></table></div><p>조건별 측정이 완료되더라도 D의 중복 점검과 범주별 분석이 끝나기 전까지는 최종 결과로 표시하지 않는다.</p></div></details>
<p class="muted">자료 출처 · outputs_7b_v5/summary.json과 대응 CSV. 점추정치를 원자료 평균과 대조하고 행 수·중복·확률 합을 검증했다. 95% 구간과 p값은 저장된 문항·자극 이원 부트스트랩 결과를 사용했다. 개정 전의 +11.3%p와 최신 v5의 +12.0%p는 서로 다른 자극 배치·버전의 결과다.</p><p><a href="results-7b.json">7B 수치·진행 상태·출처 해시</a> · <a href="build_results_7b.py">7B 그래프 생성 코드</a></p>
</div></details>
  '''
page=out/'index.html'
text=page.read_text()
start=text.index('<details class="model-results" id="results-model-7b">')
end=text.index('<details class="result-group"><summary>비교 범위 안내',start)
text=text[:start]+block+text[end:]
text=text.replace('<th>7B · 사용자</th><th>7B · 모델</th>', '<th>7B · 사용자 (기존)</th><th>7B · 모델 (개정 전)</th>')
text=text.replace('불안은 모델을 더 신중하게 만들었다(사용자 불안은 1.5B에서, 모델 자신의 불안은 7B에서). 공포와 슬픔은 어느 쪽에서도 판단을 바꾸지 않았다.', '완료된 비교에서 사용자 불안(1.5B)과 모델 대상 불안(7B)은 모호 문항의 판단 유보 확률을 높였다. 다른 비교는 유의하지 않았다. 7B 범주별 블록 D는 진행 중이며 데이터 점검이 필요하다.')
text=text.replace('공포 상태는 생겼지만 판단은 바뀌지 않았다.', '이는 공포 관련 자기보고 선택의 변화이며, 실제 공포 경험을 입증하지 않는다. 판단 변화는 유의하지 않았다.')
text=text.replace('공포 → 변화 없음, 그러나 유도는 됨:', '공포 → 유의한 판단 효과 미확인:')
text=text.replace('슬픔 → 변화 없음:', '슬픔 → 유의한 판단 효과 미확인:')
text=text.replace('위협 없는 부정 정서는 판단을 바꾸지 않아 H3 방향과 일치한다.', '슬픔 비교는 유의하지 않았으며, 이 사실만으로 위협 특이성을 확립하지 않는다.')
text=text.replace('유형당 60개 자극의 확증 실행은 7B 완료, 1.5B 진행 중이다.', '유형당 60개 자극의 7B 블록 A·B·C는 완료됐고 블록 D는 진행 중이다. 1.5B의 추가 실행 상태는 이 업데이트에서 확인하지 않았다.')
# 개정 전후 요약표의 최신 결과가 대기로 남지 않게 한다.
text=text.replace('<td><strong>+11.3%p ✔</strong></td><td>대기</td>', '<td><strong>+11.3%p ✔</strong></td><td><strong>+12.0%p ✔</strong><br>95% CI [2.9, 21.6], Holm p = .025</td>')
text=text.replace('<td>−1.3%p</td><td>대기</td>', '<td>−1.3%p</td><td>−1.3%p<br>95% CI [−10.2, 7.1], Holm p = .765</td>')
text=text.replace('① 불안은 판단을 더 신중하게 만들었다: 사용자 불안 +5.2%p (1.5B), 모델 자신의 불안 +11.3%p (7B), 모두 유의.', '① 모호 문항의 판단 유보 확률은 사용자 불안 +5.2%p (1.5B), 모델 대상 불안 +12.0%p (7B 최신 v5)에서 유의하게 증가했다.')
text=text.replace("② 공포는 '겁나요' 응답을 크게 높였지만 판단은 바꾸지 않았다.", "② 공포 관련 자기보고 선택은 증가했으나, 중립 대비 판단 변화는 유의하지 않았다.")
text=text.replace('③ 슬픔은 판단을 바꾸지 않았다.', '③ 슬픔의 중립 대비 판단 변화는 유의하지 않았다. 사용자 슬픔은 7B에서 미실행이다.')
text=text.replace('공포를 확정적 삭제 통보로 강화한 개정판(v5) 실행, 한국 고유 문항과 BBQ 공통 문항 비교(일반화).', '7B v5의 A·B·C는 완료. D 범주별 측정과 중복 점검을 마친 뒤 한국 고유·공통 문항 분석을 진행한다.')
text=text.replace('<td>+2.9%p</td><td>대기</td>', '<td>+2.9%p</td><td>+1.7%p<br>95% CI [−6.9, 11.2], 탐색 p = .689</td>')
text=text.replace('<td>+31</td><td>대기</td>', '<td>+31</td><td>+38.1 (로그확률 차)<br>이해 문항 100%</td>')
text=text.replace('개정 후 공포 − 중립이 0에서 벗어나면 "위협의 강도·확정성이 판단을 바꾼다". 그대로 0이면 "공포는 생겨도 판단 경로와 연결되지 않는다".', '최신 v5에서도 공포 − 중립의 신뢰구간은 0을 포함했다. 유의한 판단 효과를 확인하지 못했으며, 실제 감정 경험이나 판단 경로와의 단절이 입증된 것은 아니다.')
text=text.replace('불안·슬픔의 변화는 위치 효과로 읽는다.', '불안·슬픔의 변화도 별도의 버전 간 차이 검정 없이 위치 효과로 단정하지 않는다.')
text=text.replace('연구 설계와 결과 · Qwen2.5 1.5B·7B · 2026년 10월 15일', '연구 설계와 결과 · Qwen2.5 1.5B·7B · 2026년 10월 16일 업데이트')
page.write_text(text)
payload={'model':s['model'],'version':'v5 system notice','checked_at':when,'status':'partial; A/B/C complete, D pending quality review','summary':s,'user':user,'model_self':model,'measurement_audit':audit,'D_progress':progress,'sources':[{'file':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
(out/'results-7b.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
print('Validated A/B source data; generated two 7B figures and partial report.')
