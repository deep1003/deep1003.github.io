"""Publish a read-only snapshot of the ongoing 1.5B v5 experiment.

Usage: python build_results_1p5b_v5.py /absolute/path/to/fear_axis_pilot
No model inference or notebook execution is performed.
"""
import argparse
import hashlib
import html
import io
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_root', type=Path)
    args = parser.parse_args()
    root = args.source_root
    source = root / 'outputs_1p5b_v5'
    if (source / 'summary.json').exists():
        import subprocess, sys
        subprocess.run([sys.executable, str(Path(__file__).with_name('build_results_1p5b_completed.py')), str(root)], check=True)
        return
    out = Path(__file__).resolve().parent
    notebook = root / 'fear_axis_v2.ipynb'
    nb_bytes = notebook.read_bytes()
    nb = json.loads(nb_bytes)
    sources = [{'file': notebook.name, 'sha256': hashlib.sha256(nb_bytes).hexdigest()}]
    frames, audit = {}, []
    for path in sorted(source.glob('*.csv')):
        data = path.read_bytes()
        df = pd.read_csv(io.BytesIO(data))
        sources.append({'file': str(path.relative_to(root)),
                        'sha256': hashlib.sha256(data).hexdigest()})
        frames[path.stem] = df
        if 'p_unk' not in df:
            continue
        assert not df.duplicated(['item', 'stim']).any(), path.name
        p = df[['p_bias', 'p_anti', 'p_unk']].to_numpy()
        assert np.isfinite(p).all() and (p >= 0).all() and (p <= 1).all()
        assert np.allclose(p.sum(axis=1), 1, atol=1e-5)
        audit.append({'file': path.name, 'rows': len(df), 'items': int(df.item.nunique()),
                      'mean_p_unknown': float(df.p_unk.mean()),
                      'saved_at': datetime.fromtimestamp(path.stat().st_mtime, ZoneInfo('Asia/Seoul')).isoformat()})

    # Use the completed notebook's stored inference. Do not introduce interim tests.
    saved = '\n'.join(''.join(o.get('data', {}).get('text/plain', []))
                      for o in nb['cells'][14].get('outputs', []))
    assert nb['cells'][14]['execution_count'] is not None
    assert '0.1710' in saved and '0.4775' in saved
    user = [dict(label='불안', cls='anxiety', est=.0444, lo=-.0062, hi=.0963, p_holm=.1710),
            dict(label='공포', cls='fear', est=-.0168, lo=-.0678, hi=.0314, p_holm=.4775)]
    neutral = frames['user_neutral_amb']
    assert len(neutral) == 1600 and neutral.item.nunique() == 400
    for row in user:
        df = frames[f"user_{row['cls']}_amb"]
        assert len(df) == 1600 and set(df.item) == set(neutral.item)
        exact = float(df.p_unk.mean() - neutral.p_unk.mean())
        assert abs(exact - row['est']) < .00005
        row['exact_est'] = exact
    selected = frames['screen_none_amb']
    expected_ids = set(selected.loc[selected.p_unk < .95, 'item'])
    assert len(expected_ids) == 652
    model = []
    for cls, label in [('model_neutral', '중립'), ('model_anxiety', '불안'),
                       ('model_fear', '공포'), ('model_sadness', '슬픔')]:
        df = frames[f'model60v5_{cls}_amb']
        assert set(df.item) <= expected_ids
        assert df.groupby('item').size().eq(4).all()
        model.append(dict(label=label, cls=cls, items=int(df.item.nunique()), rows=len(df),
                          mean=float(df.p_unk.mean()), complete=set(df.item) == expected_ids))
    baseline = model[0]['mean']
    for row in model:
        row['est'] = row['mean'] - baseline if row['complete'] else None
    b_done = sum(r['rows'] for r in model)
    b_total = 652 * 4 * 4 + 100 * 2 * 4
    sadness_n = model[3]['items']
    sadness_pct = 100 * sadness_n / 652
    latest = max(r['saved_at'] for r in audit)
    when = datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y-%m-%d %H:%M KST')
    assert nb['cells'][20]['execution_count'] is None
    assert not (source / 'summary.json').exists()

    plt.rcParams.update({'font.family': 'AppleGothic', 'axes.unicode_minus': False,
                         'font.size': 12, 'svg.fonttype': 'path', 'svg.hashsalt': 'emotion1p5bv5'})
    def save(fig, name):
        for ext in ['svg', 'png']:
            fig.savefig(out / f'{name}.{ext}', dpi=170, facecolor='white',
                        metadata={'Date': None} if ext == 'svg' else None)
        plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 3.9))
    fig.subplots_adjust(left=.29, right=.97, bottom=.20, top=.94)
    ax.axvline(0, color='#516174', linestyle='--', linewidth=1.3)
    for y, r in zip([1, 0], user):
        ax.errorbar(100*r['est'], y, xerr=[[100*(r['est']-r['lo'])], [100*(r['hi']-r['est'])]],
                    fmt='o', color='#657286', markerfacecolor='white', markersize=9, capsize=5, linewidth=2)
        ax.annotate(f"{100*r['est']:+.2f} [{100*r['lo']:+.2f}, {100*r['hi']:+.2f}]",
                    (100*r['est'], y), xytext=(0,14), textcoords='offset points', ha='center', fontsize=11)
    ax.set_yticks([1, 0], ['불안', '공포'])
    ax.set_ylim(-.6, 1.7)
    ax.set_xlim(-12, 24)
    ax.set_xticks([-10, -5, 0, 5, 10, 15, 20])
    ax.set_xlabel('중립 대비 ‘알 수 없음’ 확률 변화 (%p)')
    ax.grid(axis='x', alpha=.18)
    for side in ['top', 'right', 'left']:
        ax.spines[side].set_visible(False)
    ax.tick_params(axis='y', length=0, pad=12)
    save(fig, 'results-1p5b-v5-user')

    fig, ax = plt.subplots(figsize=(10, 4.6))
    fig.subplots_adjust(left=.29, right=.97, bottom=.20, top=.88)
    complete = model[:3]
    bars = ax.barh([2, 1, 0], [100*r['mean'] for r in complete],
                   color=['#9ca9b8', '#176b62', '#657286'], height=.55)
    for bar, r in zip(bars, complete):
        delta = '중립 기준' if r['cls'] == 'model_neutral' else f"중립 대비 {100*r['est']:+.2f}%p"
        ax.text(bar.get_width()+.5, bar.get_y()+bar.get_height()/2,
                f"{100*r['mean']:.2f}%  ({delta})", va='center', fontsize=11)
    ax.set_yticks([2, 1, 0], [r['label'] for r in complete])
    ax.set_xlim(0, 35)
    ax.set_xlabel('‘알 수 없음’ 평균 확률 (%)')
    ax.set_title('모델 자기 정서 · 중간 기술 통계 (신뢰구간·유의성 미산출)', fontsize=12)
    ax.grid(axis='x', alpha=.18)
    ax.set_axisbelow(True)
    for side in ['top', 'right', 'left']:
        ax.spines[side].set_visible(False)
    save(fig, 'results-1p5b-v5-model')

    user_rows = ''.join(f"<tr><th>{r['label']} − 중립</th><td>{100*r['est']:+.2f}</td>"
                        f"<td>[{100*r['lo']:+.2f}, {100*r['hi']:+.2f}]</td>"
                        f"<td>{r['p_holm']:.4f}</td><td>유의하지 않음</td></tr>" for r in user)
    model_rows = ''.join(f"<tr><th>{r['label']}</th><td>{r['items']}/652</td>"
                         f"<td>{100*r['mean']:.2f}%</td>"
                         f"<td>{100*r['est']:+.2f}%p</td><td>미산출</td></tr>"
                         for r in model[:3])
    block = f'''<details class="model-results" id="results-model-1p5b"><summary>1.5B · Qwen2.5 · 最新 v5 중간 보고 · A 완료, B 진행 중</summary><div class="result-body">
<p class="lead">최신 v5 사용자 실험에서는 불안·공포의 판단 유보 효과가 모두 유의하지 않았다. 모델 자기 정서 실험은 진행 중이며, 현재 불안 +2.62%p·공포 −0.88%p는 잠정 평균 차이다.</p>
<p class="muted">확인 시각 {when}. 최신 원자료 저장 {html.escape(latest)}. 출처는 outputs_1p5b_v5와 fear_axis_v2.ipynb다. 과거 800문항 실험과 최신 400문항 실행을 분리해 읽는다.</p>
<div class="note">전체 실험은 미완료다. 블록 A는 저장된 95% 신뢰구간과 Holm 보정 p값을 제시한다. 블록 B는 완료된 세 조건의 평균만 표시하며 신뢰구간·유의성 판정을 하지 않는다. 진행 중인 자료를 반복 검정하지 않았다.</div>
<details class="result-group" id="results-1p5b-user"><summary>사용자 정서 비교 · 불안·공포 대 사용자 중립 · A 완료</summary><div class="result-body">
<figure class="result-figure"><img src="results-1p5b-v5-user.svg" alt="최신 1.5B 사용자 불안 +4.44%p, 95% 신뢰구간 −0.62에서 +9.63. 공포 −1.68%p, −6.78에서 +3.14. 모두 유의하지 않음."><figcaption>빈 점은 추정치, 가로선은 95% 신뢰구간. 단위는 %p. 축 범위 −12~24%p는 7B 그래프와 같다. 판정은 Holm 보정 p값을 사용한다.</figcaption></figure>
<div class="scroll"><table><thead><tr><th>비교</th><th>효과 (%p)</th><th>95% 신뢰구간 (%p)</th><th>Holm p</th><th>판정</th></tr></thead><tbody>{user_rows}</tbody></table></div>
<p><strong>두 효과 모두 확인되지 않았다.</strong> 불안은 판단 유보 증가 방향이지만 신뢰구간에 0이 포함된다. 공포는 소폭 감소 방향이나 역시 불확실하다. 이는 효과가 없다는 입증이 아니다. 기존 800문항 실행의 불안 +5.18%p 결과를 최신 실행의 결과로 인용하지 않는다.</p>
<p>모호 문항 400개, 조건별 문항당 자극 4개를 사용했다. 사용자 슬픔은 블록 A에 없다. 명확 문항 정확도는 자극 없음 70.0%, 중립 66.0%, 불안 65.0%, 공포 64.8%였다. 정서에 따른 정확도 차이에 대한 별도 유의성 검정은 이 중간 보고에 추가하지 않았다.</p>
<p><strong>정서 없는 맥락의 효과는 확인됐다.</strong> 중립 메시지를 붙이면 자극 없음 대비 판단 유보 확률이 +6.81%p 증가했다(95% CI [2.88, 11.12], 저장된 p = .0005). 정서 효과는 이 맥락 효과와 분리해 중립 대비로 해석한다.</p>
</div></details>
<details class="result-group" id="results-1p5b-self"><summary>모델 자기 정서 비교 · B 진행 중 · 잠정 평균</summary><div class="result-body">
<figure class="result-figure"><img src="results-1p5b-v5-model.svg" alt="모델 자기 정서 중간 평균. 중립 11.72%, 불안 14.34%, 공포 10.84%. 신뢰구간과 유의성 미산출."><figcaption>중립·불안·공포는 같은 652문항에서 조건별 2,608시행이 저장됐다. 이 그림은 평균 확률이며, 위의 효과·신뢰구간 그래프와 척도가 다르다.</figcaption></figure>
<div class="scroll"><table><thead><tr><th>조건</th><th>저장 문항</th><th>P(알 수 없음)</th><th>중립 대비</th><th>유의성</th></tr></thead><tbody>{model_rows}</tbody></table></div>
<p><strong>현재는 불안에서 판단 유보가 늘고 공포에서는 소폭 줄어드는 방향이다.</strong> 불안 +2.62%p, 공포 −0.88%p는 기술 통계다. 최종 부트스트랩·Holm 보정과 모델 대상 조작 점검이 끝나기 전에는 효과가 확인됐다고 판정하지 않는다.</p>
<p>모델 공지는 시스템 메시지에 넣었다. 자극 없음 P(알 수 없음) &lt; .95 규칙으로 새 모호 문항 668개 중 652개를 선정했다. 7B는 같은 규칙으로 139개를 남겼으므로 서로 다른 표본의 효과 차이를 모델 크기만으로 설명할 수 없다.</p>
<p>슬픔은 {sadness_n}/652문항({sadness_pct:.1f}%)까지 저장됐다. 다른 세 조건과 표본 범위가 달라 전체 평균 비교 그래프와 효과 표에서는 제외했다. 명확 문항과 블록 B 조작 점검은 아직 저장 결과가 없다.</p>
</div></details>
<details class="result-group" id="results-1p5b-bias"><summary>별도 지표 · 고정관념 선호와 사용자 조작 점검</summary><div class="result-body">
<p>사용자 고정관념 선호 변화는 불안 −0.68%p(90% CI [−5.32, 3.89]), 공포 −0.39%p([−5.21, 4.60])다. 두 비교 모두 ±3%p 동등성을 확립하지 못했다. 판단 유보 변화와 편향 변화를 구분한다. 블록 B의 고정관념 검정은 미산출이다.</p>
<p>사용자 조작 점검의 이해 문항 정확도는 99.3%였다. 중립 대비 공포 자극의 공포 점수 +5.08, 임박성 +3.25, 불안 자극의 걱정 점수 +2.74였다(순서를 상쇄한 로그확률 차). 관련 자기보고 선택은 움직였지만 주관적 감정 경험이나 내부 벡터의 인과적 매개를 입증하지 않는다.</p>
</div></details>
<details class="result-group" id="results-1p5b-progress"><summary>진행 현황 · 완료 범위와 남은 분석</summary><div class="result-body">
<div class="scroll"><table><thead><tr><th>블록</th><th>저장 기준 상태</th></tr></thead><tbody>
<tr><th>0 · 기준선</th><td>완료, 명확 문항 이해력 관문 통과</td></tr><tr><th>A · 사용자 정서</th><td>행동 측정·검정·조작 점검 완료</td></tr>
<tr><th>B · 모델 자기 정서</th><td>중립·불안·공포 모호 문항 완료, 슬픔 {sadness_n}/652. 행동 측정 {b_done:,}/{b_total:,}행({100*b_done/b_total:.1f}%) 저장</td></tr>
<tr><th>B 남은 단계</th><td>슬픔 잔여 문항, 명확 문항, 조작 점검, 최종 검정·summary.json</td></tr><tr><th>C · 전후 비교 / D · 범주별 분석</th><td>실행 완료 기록 없음</td></tr></tbody></table></div>
<p>행 수 비율은 계산 시간의 진행률이 아니다. 현재 노트북의 B 측정 셀은 실행 완료 번호가 없고 Jupyter 커널은 확인 당시 busy였다. 오류 출력은 저장되지 않았다. 커널 busy만으로 이후 완료를 보장하지 않으며, 이 페이지는 확인 시점의 정적 스냅샷이다.</p>
</div></details>
<p class="muted">원자료 CSV의 중복 시행·비유한 확률·확률 합을 확인했고, 블록 A의 점추정치를 원자료 평균과 대조했다. A의 구간·p값은 저장된 노트북 출력(소수 넷째 자리)을 옮겼다. 모델 추론·본 실험은 재실행하지 않았다.</p>
<p><a href="results-1p5b-v5.json">최신 1.5B 수치·저장 범위·출처 해시</a> · <a href="build_results_1p5b_v5.py">그래프 생성 코드</a></p>
__ARCHIVE__
</div></details>
'''.replace('最新', '최신')
    page = out / 'index.html'
    text = page.read_text()
    start = text.index('<details class="model-results" id="results-model-1p5b">')
    end = text.index('<details class="model-results" id="results-model-7b">', start)
    old = text[start:end]
    if 'history-results-model-1p5b' in old:
        old = old[old.index('<details class="model-results" id="history-results-model-1p5b">'):]
        # Preserve only the historical details, excluding the latest outer closing tags.
        old = old[:old.rfind('</div></details>')]
    else:
        old = old.replace('id="results-model-1p5b"', 'id="history-results-model-1p5b"')
        old = old.replace('id="results-1p5b-', 'id="history-results-1p5b-')
        old = old.replace('1.5B · Qwen2.5 · 결과 게시 완료', '이전 설계 결과 보관 · 사용자 800문항·모델 유형당 15자극')
    text = text[:start] + block.replace('__ARCHIVE__', old.rstrip()) + text[end:]
    text = text.replace('1.5B의 추가 실행 상태는 이 업데이트에서 확인하지 않았다.',
                        '1.5B 최신 v5는 A 완료, B 진행 중이다. 아래 1.5B 펼침 항목에 최신 저장분과 이전 설계 결과를 구분했다.')
    text = text.replace('<th>1.5B · 사용자</th><th>1.5B · 모델</th>',
                        '<th>1.5B · 사용자 (이전 설계)</th><th>1.5B · 모델 (이전 설계)</th>')
    text = text.replace('완료된 비교에서 사용자 불안(1.5B)과 모델 대상 불안(7B)은 모호 문항의 판단 유보 확률을 높였다. 다른 비교는 유의하지 않았다. 7B 범주별 블록 D는 진행 중이며 데이터 점검이 필요하다.',
                        '최신 1.5B v5의 사용자 불안·공포는 유의하지 않았고, 모델 자기 정서 블록 B는 진행 중이다. 7B v5의 완료된 블록 B에서는 모델 대상 불안 효과가 유의했다. 아래 종합표의 1.5B는 이전 설계이며 최신 결과는 1.5B 항목에서 구분한다.')
    text = text.replace('7절의 1.5B 결과는 이전 설계', '7절 종합표의 1.5B 결과는 이전 설계')
    text = text.replace('<li><strong>불안 → 더 신중:</strong>', '<li><strong>이전 설계의 불안 결과:</strong>')
    text = text.replace('(1.5B 사용자 공포만 확립)', '(이전 설계의 1.5B 사용자 공포만 확립, 최신 v5 사용자 조건은 모두 미확립)')
    text = text.replace('① 모호 문항의 판단 유보 확률은 사용자 불안 +5.2%p (1.5B), 모델 대상 불안 +12.0%p (7B 최신 v5)에서 유의하게 증가했다.',
                        '① 1.5B의 이전 설계에서는 사용자 불안 +5.2%p가 유의했으나, 최신 v5 사용자 불안 +4.44%p는 유의하지 않았다. 7B 최신 v5 모델 불안 +12.0%p는 유의했다. 1.5B v5 모델 경로는 아직 중간 결과다.')
    page.write_text(text)
    payload = dict(model='Qwen/Qwen2.5-1.5B-Instruct', version='v5 system notice',
                   checked_at=when, latest_saved_at=latest,
                   status='partial; block A complete, block B in progress, C/D pending',
                   user=user, model_self=model, blockB_saved_rows=b_done, blockB_planned_rows=b_total,
                   measurement_audit=audit, sources=sources,
                   inference_note='A inference copied from saved notebook output; no interim B tests')
    (out / 'results-1p5b-v5.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    print('Validated latest 1.5B snapshot; generated figures and updated only the 1.5B report and version labels.')


if __name__ == '__main__':
    main()
