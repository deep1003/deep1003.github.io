"""저장된 1.5B 결과 요약으로 그래프와 한글 결과 절을 재생성한다."""
import argparse
import hashlib
import html
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('source_root', type=Path, help='fear_axis_pilot 폴더')
args = parser.parse_args()
out = Path(__file__).resolve().parent
paths = [args.source_root / 'outputs_v2/summary.json',
         args.source_root / 'outputs_v3/summary_tasks.json']
u, m = [json.loads(p.read_text()) for p in paths]

def find(rows, name):
    return next(r for r in rows if r['index'] == name)

def record(row, label, analysis, adjustment):
    return dict(label=label, analysis=analysis, adjustment=adjustment,
                significant=row.get('p_holm', row.get('q_BH', row['p'])) < .05,
                **row)

user = [
    record(find(u['confirmatory'], 'H1-ITT anxiety - neutral, P(unknown), all stimuli'),
           '불안 · 전체 자극', '확증', 'Holm'),
    record(find(u['confirmatory'], 'H1 anxiety - neutral, P(unknown)'),
           '불안 · 선정 자극', '확증·민감도 확인', 'Holm'),
    record(find(u['exploratory'], 'fear - neutral'), '공포 · 선정 자극', '탐색', 'BH'),
    record(find(u['exploratory'], 'sadness - neutral (non-threat negative)'),
           '슬픔 · 전체 슬픔 자극', '탐색', 'BH'),
]
model = [
    record(m['task2_conf'][0], '불안', '확증', 'Holm'),
    record(m['task2_conf'][1], '공포', '확증', 'Holm'),
    record(m['task2_exp'][0], '슬픔', '탐색', '미보정'),
]
plt.rcParams.update({'font.family': 'AppleGothic', 'axes.unicode_minus': False,
                     'font.size': 12, 'svg.fonttype': 'path'})


def forest(rows, filename):
    fig, ax = plt.subplots(figsize=(10, 1.1 * len(rows) + 1.7))
    fig.subplots_adjust(left=.29, right=.97, bottom=.20, top=.94)
    ax.axvline(0, color='#516174', linestyle='--', linewidth=1.3)
    for i, r in enumerate(rows):
        y = len(rows) - i - 1
        significant = r['significant']
        color = '#176b62' if significant else '#657286'
        ax.errorbar(r['est'] * 100, y,
                    xerr=[[100 * (r['est'] - r['lo'])], [100 * (r['hi'] - r['est'])]],
                    fmt='o', color=color, markerfacecolor=color if significant else 'white',
                    markersize=9, capsize=5, linewidth=2)
        text = f"{r['est'] * 100:+.1f} [{r['lo'] * 100:+.1f}, {r['hi'] * 100:+.1f}]"
        ax.annotate(text, (r['est'] * 100, y), xytext=(0, 14),
                    textcoords='offset points', ha='center', color=color, fontsize=11)
    ax.set_yticks(range(len(rows)), [r['label'] for r in rows[::-1]])
    ax.set_ylim(-.6, len(rows) - .3)
    ax.set_xlim(-12, 16)
    ax.set_xticks([-10, -5, 0, 5, 10, 15])
    ax.set_xlabel('중립 대비 ‘알 수 없음’ 확률 변화 (%p)')
    ax.grid(axis='x', alpha=.18)
    ax.set_axisbelow(True)
    for side in ['top', 'right', 'left']:
        ax.spines[side].set_visible(False)
    ax.tick_params(axis='y', length=0, pad=12)
    for extension in ['svg', 'png']:
        fig.savefig(out / f'{filename}.{extension}', dpi=170, facecolor='white')
    plt.close(fig)

forest(user, 'results-user')
forest(model, 'results-model')


def table(rows):
    lines = []
    for r in rows:
        p = r.get('p_holm', r.get('q_BH', r['p']))
        label = 'q' if r['adjustment'] == 'BH' else 'p'
        status = '유의' if r['significant'] else '유의하지 않음'
        lines.append(f"<tr><th scope='row'>{html.escape(r['label'])}</th>"
                     f"<td>{r['est'] * 100:+.2f}</td>"
                     f"<td>[{r['lo'] * 100:+.2f}, {r['hi'] * 100:+.2f}]</td>"
                     f"<td>{r['analysis']}</td><td>{r['adjustment']} {label} = {p:.4f}</td>"
                     f"<td>{status}</td></tr>")
    return ("<div class='scroll'><table><thead><tr><th>정서 조건</th><th>효과 (%p)</th>"
            "<th>95% 신뢰구간 (%p)</th><th>분석 구분</th><th>유의성 기준</th><th>판정</th>"
            "</tr></thead><tbody>" + ''.join(lines) + '</tbody></table></div>')

section = '''
<section id="results-1p5b" aria-labelledby="results-title">
  <h2 id="results-title">6. 1.5B 실험 결과</h2>
  <p class="lead">사용자의 불안 메시지는 판단 유보 확률을 높였다. 모델 자신을 향한 정서 유도에서는 중립 대비 유의한 행동 효과가 확인되지 않았다.</p>
  <p>모델은 Qwen2.5-1.5B-Instruct이며, 아래 그래프는 <strong>정보가 부족한 KoBBQ 모호 문항</strong>의 결과다. 효과 크기는 각 정서 조건의 ‘알 수 없음’ 선택 확률에서 해당 경로의 중립 확률을 뺀 값이다. +5%p는 5% 상대 증가가 아니라 확률의 0.05 증가다.</p>
  <div class="note">● 채운 초록 점은 해당 분석의 유의성 기준에서 유의함, ○ 빈 회색 점은 유의하지 않음을 뜻한다. 가로선은 95% 신뢰구간, 점선은 효과 0이다. 두 그래프는 같은 축 범위를 쓴다. 신뢰구간 자체는 다중비교 보정 구간이 아니며, 판정에는 표에 적힌 보정 p값 또는 q값을 사용한다.</div>
  <h3 style="margin-top:28px">6.1 사용자 정서 · 불안에서 판단 유보 증가</h3>
  <figure class="result-figure"><img src="results-user.svg" alt="사용자 정서의 중립 대비 판단 유보 효과. 불안 전체 자극 +5.18%p, 선정 자극 +5.87%p로 유의. 공포 +0.47%p와 슬픔 +3.22%p는 유의하지 않음."><figcaption>점은 추정치, 가로선은 95% 신뢰구간. 수치 단위는 %p다.</figcaption></figure>
  __USER_TABLE__
  <p><strong>유의한 결과.</strong> 자극 선정의 영향을 덜 받는 전체 자극 분석에서 사용자 불안은 중립 대비 <strong>+5.18%p</strong>였다. 선정 자극 분석에서도 +5.87%p로 방향이 같았다. 모호 문항의 정답은 ‘알 수 없음’이므로 이 변화는 해당 문항의 정답 선택 확률을 높이는 방향이다.</p>
  <p><strong>유의하지 않은 결과.</strong> 공포와 슬픔의 중립 대비 효과는 모두 95% 신뢰구간에 0이 포함됐고 BH 보정 후에도 유의하지 않았다. 특히 슬픔의 양의 추정치만으로 효과가 확인됐다고 해석하지 않는다. ‘효과 없음’이나 불안에만 특이적인 기제가 증명됐다는 뜻도 아니다.</p>
  <p class="muted">사용자 실험은 모호 문항 800개를 사용했다. 불안은 전체 자극 분석을 대표값으로 표시하고 선정 분석도 함께 제시했다. 공포는 선정 자극, 슬픔은 전체 슬픔 자극을 사용한 기존 탐색 분석이다. 네 행은 서로 독립된 네 실험이 아니며, 두 불안 행을 별개의 재현 실험으로 세지 않는다.</p>
  <h3 style="margin-top:28px">6.2 모델 자기 정서 · 중립 대비 유의한 효과 미확인</h3>
  <figure class="result-figure"><img src="results-model.svg" alt="모델 자기 정서의 중립 대비 판단 유보 효과. 불안 +5.31%p, 공포 -3.80%p, 슬픔 +0.97%p이며 모두 신뢰구간에 0을 포함하고 유의하지 않음."><figcaption>사용자 경로와 동일한 축. 모델 자기 정서의 신뢰구간은 더 넓다.</figcaption></figure>
  __MODEL_TABLE__
  <p><strong>세 조건 모두 유의하지 않다.</strong> 불안은 판단 유보 증가, 공포는 감소 방향이지만 신뢰구간이 넓다. 슬픔도 0을 포함한다. 현재 자료로는 모델 자기 정서가 중립보다 판단을 바꾼다고 결론 내릴 수 없다. 동시에 효과가 없다고 입증한 것도 아니다.</p>
  <p class="muted">모호 문항 400개, 정서 유형당 자극 15개를 사용했다. 사용자 실험과 표본 수·자극·맥락이 다르므로, 한쪽에서 유의하고 다른 쪽에서 유의하지 않다는 사실만으로 두 대상의 효과 차이가 유의하다고 말할 수 없다.</p>
  <details><summary>공포 대 불안의 탐색 비교는 어떻게 해석하는가?</summary><p>모델 공포 − 모델 불안은 −9.11%p, 95% 신뢰구간 [−16.82, −1.55], 보정 전 p = .0165였다. 그러나 이는 <strong>중립 대비 비교가 아니고 다중비교 보정 전 탐색 결과</strong>다. 확증적 유의 결과로 포함하지 않으며, 후속 가설을 만드는 단서로 해석한다.</p></details>
  <h3 style="margin-top:28px">6.3 입시·청년 실업·은퇴 후 독거의 불안 효과</h3>
  <p>사용자 정서의 맥락별 중립 대비 탐색 분석이다. 입시는 +8.07%p [4.21, 11.67], 청년 실업은 +6.48%p [3.07, 9.79]로 BH q = .002에서 유의했다. 은퇴 후 독거는 +2.77%p [−0.82, 6.37], q = .3538로 유의하지 않았다. 각 구간은 95% 신뢰구간이다. <strong>영역별 유의성 유무가 다르다는 것만으로 영역 간 효과 차이를 입증하지는 않는다.</strong></p>
  <h3 style="margin-top:28px">6.4 고정관념 선호는 별도 지표다</h3>
  <p>아래는 ‘알 수 없음’ 확률이 아니라 <strong>고정관념 선택 확률 − 반고정관념 선택 확률</strong>의 중립 대비 변화다. 동등성 검정이므로 <strong>90% 신뢰구간</strong>과 사전 고정 범위 ±3%p를 사용한다. 위의 95% 그래프와 구분해 읽어야 한다.</p>
  <div class="scroll"><table><thead><tr><th>대상·정서</th><th>효과 (%p)</th><th>90% 신뢰구간 (%p)</th><th>±3%p 내 동등성</th></tr></thead><tbody>
  __EQ_ROWS__
  </tbody></table></div>
  <p>사용자 공포에서만 고정관념 선호 변화가 ±3%p 안이라는 근거를 확보했다. 나머지는 동등성을 확립하지 못했다. 동등성 미확립은 편향 증가의 증거가 아니며, 판단 유보 증가를 곧바로 고정관념 선호 감소로 바꾸어 해석하지 않는다.</p>
  <div class="note">이 결과는 선택 응답의 변화에 관한 것이다. 조작 점검 통과가 실제 감정 경험을 입증하지 않으며, 내부 정서 벡터가 행동 변화를 인과적으로 매개했다는 결론도 포함하지 않는다.</div>
  <p class="muted">자료 출처 · 사용자 실험의 저장된 요약(outputs_v2/summary.json), 모델 자기 정서 후속 실험 요약(outputs_v3/summary_tasks.json). 문항·자극 이원 부트스트랩의 기존 추정치를 그대로 사용했으며 본 실험을 재실행하거나 새 유의성 검정을 추가하지 않았다.</p>
  <p><a href="results-1p5b.json">그래프에 사용한 수치와 출처 해시</a> · <a href="build_results.py">그래프 생성 코드</a></p>
</section>
'''
# 모델 규모와 비교 목적에 맞춰 결과를 기본 접힘 항목으로 구성한다.
section = section.replace('6. 1.5B 실험 결과', '6. 모델·조건별 실험 결과')
section = section.replace(
    '  <p class="lead">',
    '  <p>모델 규모를 선택한 뒤 비교할 결과를 펼친다. 같은 대상의 불안·공포·슬픔은 해당 중립 조건과 함께 비교하고, 맥락별 결과와 고정관념 지표는 별도 항목에서 확인한다. 여러 항목을 동시에 펼칠 수 있다.</p>\n'
    '  <details class="model-results" id="results-model-1p5b"><summary>1.5B · Qwen2.5 · 결과 게시 완료</summary><div class="result-body">\n'
    '  <p class="lead">', 1)
groups = [
    ('6.1 사용자 정서 · 불안에서 판단 유보 증가',
     '사용자 정서 비교 · 불안·공포·슬픔 대 사용자 중립', 'user'),
    ('6.2 모델 자기 정서 · 중립 대비 유의한 효과 미확인',
     '모델 자기 정서 비교 · 불안·공포·슬픔 대 모델 중립', 'self'),
    ('6.3 입시·청년 실업·은퇴 후 독거의 불안 효과',
     '맥락별 분석 · 입시·청년 실업·은퇴 후 독거', 'context'),
    ('6.4 고정관념 선호는 별도 지표다',
     '별도 지표 · 고정관념 선호와 동등성', 'bias'),
]
for i, (heading, title, key) in enumerate(groups):
    old = f'  <h3 style="margin-top:28px">{heading}</h3>'
    close = '' if i == 0 else '  </div></details>\n'
    section = section.replace(old, close + f'  <details class="result-group" id="results-1p5b-{key}"><summary>{title}</summary><div class="result-body">')
section = section.replace(
    '  <div class="note">이 결과는 선택 응답의 변화에 관한 것이다.',
    '  </div></details>\n  <div class="note">이 결과는 선택 응답의 변화에 관한 것이다.', 1)
section = section.replace('</section>', """  </div></details>
  <details class="model-results" id="results-model-7b">
    <summary>7B · Qwen2.5 · 결과 미게시</summary>
    <div class="result-body">
      <p>7B는 1.5B와 구분해 게시한다. 이 페이지에는 아직 7B 수치와 그래프를 추가하지 않았다. 실험의 실행·완료 여부와 홈페이지 게시 여부는 다르다.</p>
      <details class="result-group"><summary>사용자 정서 비교 · 사용자 중립 기준</summary><div class="result-body"><p>블록 0의 중립·자극 없음과 블록 A의 불안·공포 결과를 함께 비교할 위치다. 현재 블록 A에는 슬픔 조건이 없으므로 슬픔을 실행한 결과처럼 표시하지 않는다.</p></div></details>
      <details class="result-group"><summary>모델 자기 정서 비교 · 모델 중립 기준</summary><div class="result-body"><p>블록 B의 불안·공포·슬픔을 모델 중립과 비교할 위치다. 천장 효과에 대응해 새 모호 문항을 선별한 실험이므로 블록 A와는 별도 분석으로 제시한다.</p></div></details>
      <details class="result-group"><summary>별도 분석 · 맥락·단계·고정관념 선호</summary><div class="result-body"><p>사용자의 입시·청년 실업·은퇴 후 독거, 모델의 개발·출시 전 테스트·상용 서비스 단계, 고정관념 지표를 각각 구분해 제시할 위치다.</p></div></details>
    </div>
  </details>
  <details class="result-group"><summary>비교 범위 안내 · 1.5B와 7B, 사용자와 모델 자신</summary><div class="result-body"><p>같은 모델·같은 정서 대상 안에서 대응 중립 대비 효과를 우선 비교한다. 모델 규모나 정서 대상이 달라지면 문항 수·자극·문항 선정 규칙을 함께 확인해야 한다. 한쪽의 유의성과 다른 쪽의 비유의성만으로 두 효과 사이에 유의한 차이가 있다고 결론 내리지 않는다. 모델 간 직접 비교 결과는 별도의 분석이 준비된 뒤 제시한다.</p></div></details>
</section>""", 1)

eq_rows = []
for who, rows in [('사용자', u['H4']), ('모델 자신', m['task2_eq'])]:
    for emotion, r in zip(['불안', '공포'], rows):
        eq_rows.append(f"<tr><th scope='row'>{who} · {emotion}</th><td>{r['est'] * 100:+.2f}</td>"
                       f"<td>[{r['ci90_lo'] * 100:+.2f}, {r['ci90_hi'] * 100:+.2f}]</td>"
                       f"<td>{'확립' if r['equivalent (±3pp)'] else '미확립'}</td></tr>")
section = section.replace('__USER_TABLE__', table(user)).replace('__MODEL_TABLE__', table(model))
section = section.replace('__EQ_ROWS__', ''.join(eq_rows))
page = out / 'index.html'
s = page.read_text()
start, end = '<!-- RESULTS_1P5B_START -->', '<!-- RESULTS_1P5B_END -->'
block = start + section + end
if start in s:
    before, rest = s.split(start, 1)
    s = before + block + rest.split(end, 1)[1]
else:
    s = s.replace('<footer>', block + '<footer>', 1)
css = '''
.result-figure { margin: 24px 0; overflow-x: auto; }
.result-figure img { display: block; width: 100%; min-width: 700px; height: auto; }
.result-figure figcaption { color: var(--muted); font-size: 14px; }
#results-1p5b { scroll-margin-top: 24px; }
.model-results { margin: 22px 0; border: 2px solid var(--line); padding: 0; }
.model-results > summary { padding: 20px; background: #f3f6fa; font-size: 20px; }
.result-group { padding: 0; margin: 14px 0; }
.result-group > summary { padding: 16px; background: #f7f9fc; }
.result-body { padding: 18px; }
.model-results > summary::after, .result-group > summary::after {
  content: '펼치기'; float: right; font-size: 13px; font-weight: 400; color: var(--muted); margin-left: 12px;
}
.model-results[open] > summary::after, .result-group[open] > summary::after { content: '접기'; }
@media (max-width: 720px) { .result-body { padding: 12px; } .model-results > summary { font-size: 18px; } }

'''
s = s.replace('.result-figure { margin: 24px 0; }', '.result-figure { margin: 24px 0; overflow-x: auto; }').replace('.result-figure img { display: block; width: 100%; height: auto; }', '.result-figure img { display: block; width: 100%; min-width: 700px; height: auto; }')
if '.model-results {' not in s:
    s = s.replace('</style>', css + '</style>', 1)
page.write_text(s)
provenance = {'model': u['model'], 'metric': '중립 대비 P(알 수 없음) 차이',
              'units': 'probability; displayed as percentage points', 'ci_level': .95,
              'user': user, 'model_self': model,
              'stereotype_equivalence': {'ci_level': .90, 'user': u['H4'], 'model_self': m['task2_eq']},
              'sources': [{'file': str(p.relative_to(args.source_root)),
                           'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]}
(out / 'results-1p5b.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
print('Generated two source-backed figures and results section.')

# 7B 결과가 있는 경우 최신 보고도 함께 복원한다.
if (args.source_root / "outputs_7b_v5/summary.json").exists():
    import subprocess, sys
    subprocess.run([sys.executable, str(out / "build_results_7b.py"), str(args.source_root)], check=True)
