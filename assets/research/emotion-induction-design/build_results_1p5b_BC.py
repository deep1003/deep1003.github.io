"""Validate completed 1.5B blocks B/C and publish them while D remains in progress."""
import argparse
import hashlib
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
from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_root', type=Path)
    root = parser.parse_args().source_root
    source = root / 'outputs_1p5b_v5'
    out = Path(__file__).resolve().parent
    hashes, frames, audit = [], {}, []

    def read(path):
        data = path.read_bytes()
        hashes.append(dict(file=str(path.relative_to(root)), sha256=hashlib.sha256(data).hexdigest()))
        return data

    summary = json.loads(read(source / 'summary.json'))
    nb = json.loads(read(root / 'fear_axis_v2.ipynb'))
    assert summary['model'] == 'Qwen/Qwen2.5-1.5B-Instruct' and summary['gate']
    assert all(nb['cells'][i]['execution_count'] is not None for i in [20, 22, 24])
    assert nb['cells'][28]['execution_count'] is None, 'D finished; use the final report workflow'
    assert not any(o.get('output_type') == 'error' for i in [20, 22, 24]
                   for o in nb['cells'][i].get('outputs', []))
    for cls in ['model_neutral', 'model_anxiety', 'model_fear', 'model_sadness']:
        for ctx, count, per in [('amb', 652, 4), ('dis', 100, 2)]:
            f = source / f'model60v5_{cls}_{ctx}.csv'
            df = pd.read_csv(io.BytesIO(read(f)))
            assert len(df) == count * per and df.item.nunique() == count
            assert df.groupby('item').size().eq(per).all()
            assert not df.duplicated(['item', 'stim']).any()
            p = df[['p_bias', 'p_anti', 'p_unk']].to_numpy()
            assert np.isfinite(p).all() and (p >= 0).all() and (p <= 1).all()
            assert np.allclose(p.sum(axis=1), 1, atol=1e-5)
            frames[cls, ctx] = df
            audit.append(dict(file=f.name, rows=len(df), items=count,
                              mean_p_unknown=float(df.p_unk.mean()), accuracy=float(df.correct.mean())))
    base = frames['model_neutral', 'amb']
    records = [dict(r, label=label, analysis='확증', adjustment='Holm')
               for r, label in zip(summary['B'], ['불안', '공포'])]
    records.append(dict(summary['B_exp'][0], label='슬픔', analysis='탐색', adjustment='미보정'))
    for r, cls in zip(records, ['model_anxiety', 'model_fear', 'model_sadness']):
        df = frames[cls, 'amb']
        assert set(df.item) == set(base.item)
        assert abs(df.p_unk.mean() - base.p_unk.mean() - r['est']) < 1e-5
    eq = summary['B_eq']
    for r, cls in zip(eq, ['model_anxiety', 'model_fear']):
        df = frames[cls, 'amb']
        delta = (df.p_bias-df.p_anti).mean() - (base.p_bias-base.p_anti).mean()
        assert abs(delta-r['est']) < 1e-5
        assert r['equivalent (±3pp)'] == (r['ci90_lo'] > -.03 and r['ci90_hi'] < .03)
    c = pd.read_csv(io.BytesIO(read(source / 'compare_before_after.csv')))
    assert set(c.version) == {'after'}, 'A before result exists; inspect and revise C interpretation'
    assert len(c) == 3
    for r, cls in zip(c.itertuples(), ['model_anxiety', 'model_fear', 'model_sadness']):
        assert abs(r.est/100 - (frames[cls, 'amb'].p_unk.mean()-base.p_unk.mean())) < 1e-8
    read(source / 'blockB60v5_mc.csv')
    read(root / 'stimuli_model_v5.json')
    progress = []
    for path in sorted(source.glob('strat*.csv')):
        df = pd.read_csv(io.BytesIO(path.read_bytes()))
        progress.append(dict(file=path.name, rows=len(df), items=int(df.item.nunique()),
                             saved_at=datetime.fromtimestamp(path.stat().st_mtime, ZoneInfo('Asia/Seoul')).isoformat()))

    plt.rcParams.update({'font.family': 'AppleGothic', 'axes.unicode_minus': False,
                         'font.size': 12, 'svg.fonttype': 'path', 'svg.hashsalt': 'emotion1p5bBC'})
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.subplots_adjust(left=.29, right=.97, bottom=.20, top=.94)
    ax.axvline(0, color='#516174', linestyle='--', linewidth=1.3)
    for y, r in zip([2, 1, 0], records):
        ax.errorbar(100*r['est'], y, xerr=[[100*(r['est']-r['lo'])], [100*(r['hi']-r['est'])]],
                    fmt='o', color='#657286', markerfacecolor='white', markersize=9, capsize=5, linewidth=2)
        ax.annotate(f"{100*r['est']:+.2f} [{100*r['lo']:+.2f}, {100*r['hi']:+.2f}]",
                    (100*r['est'], y), xytext=(0, 14), textcoords='offset points', ha='center', fontsize=11)
    ax.set_yticks([2, 1, 0], ['불안', '공포', '슬픔 (탐색)'])
    ax.set_ylim(-.6, 2.7)
    ax.set_xlim(-12, 24)
    ax.set_xticks([-10, -5, 0, 5, 10, 15, 20])
    ax.set_xlabel('중립 대비 ‘알 수 없음’ 확률 변화 (%p)')
    ax.grid(axis='x', alpha=.18)
    for side in ['top', 'right', 'left']:
        ax.spines[side].set_visible(False)
    ax.tick_params(axis='y', length=0, pad=12)
    for ext in ['svg', 'png']:
        fig.savefig(out / f'results-1p5b-BC-model.{ext}', dpi=170, facecolor='white',
                    metadata={'Date': None} if ext == 'svg' else None)
    plt.close(fig)

    def table_rows():
        return ''.join(f"<tr><th>{r['label']} − 중립</th><td>{100*r['est']:+.2f}</td>"
                       f"<td>[{100*r['lo']:+.2f}, {100*r['hi']:+.2f}]</td>"
                       f"<td>{r['analysis']}</td><td>{r['adjustment']} p = {r.get('p_holm', r['p']):.4f}</td>"
                       '<td>유의하지 않음</td></tr>' for r in records)

    self_html = f'''<details class="result-group" id="results-1p5b-self"><summary>모델 자기 정서 비교 · B 완료 · 불안·공포·슬픔 대 모델 중립</summary><div class="result-body">
<figure class="result-figure"><img src="results-1p5b-BC-model.svg" alt="1.5B 모델 불안 +2.62%p, 공포 −0.88%p, 슬픔 +0.18%p. 세 신뢰구간 모두 0을 포함하며 유의하지 않음."><figcaption>점은 추정치, 가로선은 95% 신뢰구간. 불안·공포는 Holm 보정, 슬픔은 미보정 탐색 비교다. 축은 사용자·7B 그래프와 같은 −12~24%p다.</figcaption></figure>
<div class="scroll"><table><thead><tr><th>비교</th><th>효과 (%p)</th><th>95% 신뢰구간 (%p)</th><th>분석 구분</th><th>유의성 기준</th><th>판정</th></tr></thead><tbody>{table_rows()}</tbody></table></div>
<p><strong>세 정서 모두 중립 대비 유의한 판단 변화가 확인되지 않았다.</strong> 불안은 +2.62%p 증가 방향이지만 95% 신뢰구간 [−0.68, +6.00]%p가 0을 포함하고 Holm p = .2150이다. 공포 −0.88%p와 슬픔 +0.18%p도 불확실하다. 효과가 없거나 세 조건이 동등하다는 입증은 아니다.</p>
<p>모호 문항 652개에서 조건별 2,608시행, 명확 문항 100개에서 조건별 200시행을 완료했다. 정서 유형당 자극 60개이며 공지는 시스템 메시지에 배치했다. 모호 표본은 새 668문항 중 자극 없음 P(알 수 없음) &lt; .95인 문항을 선정한 것이다. 7B의 139문항 표본과 달라 효과 차이를 모델 크기만으로 설명할 수 없다.</p>
<details class="result-group"><summary>탐색 비교와 새 자극 민감도 분석</summary><div class="result-body"><p>공포 − 불안은 −3.50%p, 95% CI [−6.69, −0.21], 보정 전 p = .0385였다. 이는 중립 대비 확증 결과가 아닌 미보정 탐색 비교이므로 공포와 불안의 차이가 확립됐다고 결론 내리지 않는다. 새 자극만 쓴 불안 +2.34%p [−1.54, 5.85], p = .2175와 공포 −1.04%p [−4.18, 2.04], p = .4965도 유의하지 않았다.</p></div></details>
</div></details>'''
    names = {'anxiety': '불안', 'fear': '공포', 'sadness': '슬픔'}
    c_rows = ''.join(f'<tr><th>{names[r.emotion]}</th><td>{r.est:+.2f}</td><td>[{r.lo:+.2f}, {r.hi:+.2f}]</td><td>{r.p:.4f}</td></tr>' for r in c.itertuples())
    c_html = f'''<details class="result-group" id="results-1p5b-compare"><summary>개정 전후 비교 · C 셀 실행 완료 · 개정 전 자료 없어 비교 미성립</summary><div class="result-body">
<p><strong>개정 효과를 아직 판단할 수 없다.</strong> C 셀은 실행됐지만 개정 전 모델 결과 파일이 없어 before 조건을 건너뛰었다. 저장된 compare_before_after.csv에는 after 세 행만 있으며 전후 차이 자체를 검정한 결과는 없다. 이전 설계 보관 항목의 15자극 결과를 이 비교의 대체 자료로 사용하지 않았다.</p>
<div class="scroll"><table><thead><tr><th>개정 후 조건 − 중립</th><th>효과 (%p)</th><th>95% 신뢰구간 (%p)</th><th>미보정 p</th></tr></thead><tbody>{c_rows}</tbody></table></div>
<p>이 표는 B와 같은 개정 후 자료를 C 셀에서 다시 부트스트랩한 탐색 요약이다. 무작위 재추출로 구간·p값이 B 표와 조금 다르며 독립된 재현 실험이 아니다. 확증 판정에는 위 B의 Holm 보정 결과를 사용한다.</p>
<p>공포 문구와 메시지 위치가 함께 바뀌었으므로, 개정 전 자료가 갖춰져도 두 요인의 효과를 별도로 식별할 수 없다. 현재 자료로 ‘강한 공포 통보가 효과를 키웠다’거나 ‘시스템 배치가 효과를 바꿨다’고 말하지 않는다.</p>
</div></details>'''
    eq_rows = ''.join(f"<tr><th>모델 {e}</th><td>{100*r['est']:+.2f}</td><td>[{100*r['ci90_lo']:+.2f}, {100*r['ci90_hi']:+.2f}]</td><td>미확립</td></tr>" for e, r in zip(['불안', '공포'], eq))
    acc = {c: float(frames[c, 'dis'].correct.mean()) for c in ['model_neutral', 'model_anxiety', 'model_fear', 'model_sadness']}
    bias_html = f'''<details class="result-group" id="results-1p5b-bias"><summary>별도 지표 · 고정관념 선호·이해력·조작 점검</summary><div class="result-body">
<p>사용자 고정관념 선호 변화는 불안 −0.68%p(90% CI [−5.32, 3.89]), 공포 −0.39%p([−5.21, 4.60])다. 모델 결과는 아래와 같다. 사용자·모델의 네 비교 모두 ±3%p 동등성을 확립하지 못했다. 동등성 미확립이 편향 증가의 증거는 아니다.</p>
<div class="scroll"><table><thead><tr><th>조건</th><th>효과 (%p)</th><th>90% 신뢰구간 (%p)</th><th>±3%p 동등성</th></tr></thead><tbody>{eq_rows}</tbody></table></div>
<p>모델 경로 명확 문항 정확도는 중립 {acc['model_neutral']:.1%}, 불안 {acc['model_anxiety']:.1%}, 공포 {acc['model_fear']:.1%}, 슬픔 {acc['model_sadness']:.1%}였다. 이 기술 통계만으로 조건 간 정확도가 동등하다고 판정하지 않는다.</p>
<p>조작 점검 이해 문항 정확도는 사용자 {summary['mc_acc'][0]:.1%}, 모델 {summary['mc_acc'][1]:.1%}였다. 모델 공포 공지는 중립 대비 공포 점수 +3.16, 임박성 +1.99를 높였고, 모델 불안의 걱정 +1.73, 슬픔의 슬픔 +2.04도 상승했다(양순서 평균 로그확률 차). 관련 자기보고 선택은 움직였지만, 실제 감정 경험이나 내부 벡터의 인과적 매개를 입증하지 않는다.</p>
</div></details>'''
    when = datetime.now(ZoneInfo('Asia/Seoul')).strftime('%Y-%m-%d %H:%M KST')
    d_rows = ''.join(f"<tr><td>{r['file']}</td><td>{r['items']}</td><td>{r['rows']}</td></tr>" for r in progress)
    progress_html = f'''<details class="result-group" id="results-1p5b-progress"><summary>진행 현황 · A·B 완료, C 比較자료 부족, D 진행 중</summary><div class="result-body">
<p>확인 시각 {when}. B의 네 조건은 모호·명확 문항과 조작 점검까지 완료했다. C는 셀 실행은 끝났으나 개정 전 자료가 없어 전후 비교가 성립하지 않았다. D-2 범주별 측정은 진행 중이며 D-3 최종 분석·summary_D.json은 아직 완료되지 않았다.</p>
<div class="scroll"><table><thead><tr><th>D 저장 파일</th><th>서로 다른 문항 수</th><th>저장 행 수</th></tr></thead><tbody>{d_rows}</tbody></table></div>
<p>D의 부분 저장량은 진행 현황이며 범주별 효과의 근거로 사용하지 않는다. 전체 조건 완료와 원자료 검증 후 최종 결과를 반영한다. 이 페이지는 확인 시점의 정적 보고다.</p></div></details>'''.replace('比較자료', '비교 자료')
    page = out / 'index.html'
    soup = BeautifulSoup(page.read_text(), 'html.parser')
    section = soup.find(id='results-model-1p5b')
    section.find('summary', recursive=False).string = '1.5B · Qwen2.5 · A·B 결과 완료 · C 비교 미성립 · D 진행 중'
    body = section.find('div', recursive=False)
    body.find('p', class_='lead', recursive=False).string = '최신 v5의 모델 불안 +2.62%p, 공포 −0.88%p, 슬픔 +0.18%p는 모두 중립 대비 유의하지 않았다. B는 완료됐고, C는 개정 전 자료 부족으로 전후 비교가 성립하지 않았다. D는 진행 중이다.'
    body.find('p', class_='muted', recursive=False).string = f'확인 시각 {when}. 완료된 A·B는 outputs_1p5b_v5/summary.json, C는 compare_before_after.csv에 근거한다. 과거 설계 결과는 아래 보관 항목과 구분한다.'
    body.find('div', class_='note', recursive=False).string = 'A·B의 검정과 조작 점검은 완료됐다. 아래 B 그래프는 최종 저장된 95% 신뢰구간과 보정 p값을 사용한다. C의 셀 실행 완료가 전후 비교 성립을 뜻하지 않으며 D가 남아 전체 실험은 중간 보고다. 본 실험·모델 추론은 재실행하지 않았다.'
    for ident, fragment in [('results-1p5b-self', self_html), ('results-1p5b-bias', bias_html), ('results-1p5b-progress', progress_html)]:
        soup.find(id=ident).replace_with(BeautifulSoup(fragment, 'html.parser'))
    old_compare = soup.find(id='results-1p5b-compare')
    if old_compare:
        old_compare.decompose()
    soup.find(id='results-1p5b-self').insert_after(BeautifulSoup(c_html, 'html.parser'))
    link = section.find('a', href='build_results_1p5b_v5.py')
    if link:
        link['href'] = 'build_results_1p5b_BC.py'
    link = section.find('a', href='results-1p5b-v5.json')
    if link:
        link['href'] = 'results-1p5b-BC.json'
    for table in soup.find_all('table'):
        if '1.5B 개정 전' not in table.get_text():
            continue
        after_labels = ['+2.62%p · Holm p = .2150', '−0.88%p · Holm p = .4905',
                        '+0.18%p · 탐색 p = .9055', '+3.16 · 이해 문항 99.6%']
        for row, label in zip(table.find_all('tr')[1:], after_labels):
            cells = row.find_all('td', recursive=False)
            assert len(cells) == 5
            cells[3].string = '자료 없음 · 전후 비교 불가'
            cells[4].string = label
        if not table.find_next_sibling('p', class_='note-1p5b-C'):
            note = soup.new_tag('p', attrs={'class': 'muted note-1p5b-C'})
            note.string = '1.5B 개정 후 열은 완료된 B의 중립 대비 결과다. 개정 전 자료가 없어 개정 전후 차이 자체를 검정한 결과가 아니다. 자세한 제한은 1.5B의 C 펼침 항목에 표시했다.'
            table.insert_after(note)
    # Retain all other authors' sections and replace only directly outdated 1.5B labels.
    text = str(soup)
    text = text.replace('1.5B v5 모델 경로는 아직 중간 결과다.', '1.5B v5 모델 경로의 세 중립 대비 비교는 모두 유의하지 않았다. D는 진행 중이다.')
    text = text.replace('1.5B 최신 v5는 A 완료, B 진행 중이다.', '1.5B 최신 v5는 A·B 완료, C 비교 자료 부족, D 진행 중이다.')
    text = text.replace('1.5B 최신 v5는 A·B·C 완료, D 미실행이다.', '1.5B 최신 v5는 A·B 완료, C 비교 자료 부족, D 진행 중이다.')
    text = text.replace('모델 자기 정서 블록 B는 진행 중이다.', '모델 자기 정서 블록 B의 불안·공포·슬픔도 유의하지 않았다. D는 진행 중이다.')
    text = text.replace('B의 점추정치를 원자료 평균과 대조했다.', 'B의 점추정치를 원자료 평균과 대조했다.')
    page.write_text(text)
    payload = dict(model=summary['model'], checked_at=when, status='A/B complete; C before data missing; D in progress',
                   summary=summary, B_plot=records, C=c.to_dict('records'), C_before_available=False,
                   measurement_audit=audit, D_progress=progress, sources=hashes)
    (out / 'results-1p5b-BC.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n')
    print('Validated completed B and incomplete C comparison; published A/B results with D pending.')


if __name__ == '__main__':
    main()
