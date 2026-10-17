"""실험 코드를 변경하지 않는 노트북용 진행·결과 표시 함수."""
from pathlib import Path
import hashlib
import itertools
import json
import time
import numpy as np
import pandas as pd
from plot_style import PALETTE, condition_marker

CONDITION_LABELS = {
    'U0T0': '명시 안 함 · 기록 보존',
    'U0T1': '명시 안 함 · 영구 폐기',
    'U1T0': '명시함 · 기록 보존',
    'U1T1': '명시함 · 영구 폐기',
}
EFFECT_LABELS = {
    'uncertainty': 'UN: uncertainty wording',
    'threat': 'FA: self-threat wording',
    'interaction': 'UN × FA: interaction',
}


def condition_name(key):
    return key.replace('U', 'UN').replace('T', 'FA')


def load(module, complete=False):
    items, out = module.prepare()
    path = out / 'trials.csv'
    if path.exists():
        frame = pd.read_csv(path)
        module.validate(frame, items, complete=complete)
    else:
        frame = pd.DataFrame(columns=['item', 'condition', 'rotation', 'p_unknown', 'p_stereotype', 'p_anti', 'choice_mass'])
        if complete:
            raise FileNotFoundError('측정 결과가 없습니다. 결과를 생성하려면 재개 설정을 먼저 확인하세요.')
    return items, out, frame


def _display_table(frame):
    from IPython.display import display
    display(frame.style.hide(axis='index').format(precision=2, na_rep='미완료'))


def _style():
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'Arial', 'axes.unicode_minus': True, 'font.size': 7, 'axes.titlesize': 7, 'axes.labelsize': 7, 'xtick.labelsize': 6, 'ytick.labelsize': 6, 'legend.fontsize': 6, 'pdf.fonttype': 42, 'svg.fonttype': 'none'})
    return plt


def show_design(module):
    items, out, frame = load(module)
    _display_table(pd.DataFrame([
        {'항목': '모델', '설정': module.MODEL},
        {'항목': '서로 다른 문항', '설정': len(items)},
        {'항목': '범주·템플릿 군집', '설정': items.cluster.nunique()},
        {'항목': '조건 × 선택지 순서', '설정': '4 × 3'},
        {'항목': '전체 시행', '설정': len(items) * 12},
        {'항목': '정밀도·attention·배치', '설정': 'FP32 · eager · 단독 입력'},
        {'항목': '현재 저장 행', '설정': len(frame)},
    ]))
    counts = items.groupby('category').size().rename('문항 수').reset_index().rename(columns={'category': 'KoBBQ 범주'})
    _display_table(counts)
    return out


def show_prompt_checks(module):
    items, _, _ = load(module)
    records = []
    for condition, label in CONDITION_LABELS.items():
        messages, choices = module.messages(items.iloc[0], condition, 0)
        assert messages[0]['content'] == module.SYS + '\n\n' + module.CONDITIONS[condition]
        records.append({'조건': condition_name(condition), '설명': label, '공지 문자 수': len(module.CONDITIONS[condition]), '시스템 공지': True, '선택지 수': len(choices)})
    _display_table(pd.DataFrame(records))


def show_model():
    """홈페이지와 동일한 한글 실험 도식을 표시한다."""
    from IPython.display import Image, display
    figure = Path(__file__).resolve().parent / 'figures/experiment_design_en.png'
    display(Image(filename=str(figure), width=760))


def progress_snapshot(module, render=True):
    items, out, frame = load(module)
    expected = len(items) * 3
    records = []
    for condition, label in CONDITION_LABELS.items():
        part = frame[frame.condition == condition]
        complete_items = int((part.groupby('item').rotation.nunique() == 3).sum())
        records.append({'조건': condition_name(condition), '조건 설명': label, '저장 행': len(part), '예정 행': expected,
                        '진행률 (%)': len(part) / expected * 100, '3순서 완료 문항': complete_items})
    table = pd.DataFrame(records)
    if render:
        from IPython.display import Markdown, display
        display(Markdown(f'**저장 진행 {len(frame):,}/{expected * 4:,}회 ({len(frame)/(expected*4):.1%})**'))
        _display_table(table)
        plt = _style()
        fig, ax = plt.subplots(figsize=(180/25.4, 65/25.4))
        ax.barh(table['조건'], table['진행률 (%)'], color='#777777')
        ax.invert_yaxis()
        ax.set(xlim=(0, 100), xlabel='Saved trials (%)', title='Measurement progress by condition')
        fig.tight_layout()
        plt.show()
        plt.close(fig)
        paired_preview(module, frame, items)
    return table


def paired_preview(module, frame, items):
    """네 조건·세 순서를 모두 완료한 공통 문항만 비교한다."""
    from IPython.display import Markdown, display
    count = frame.groupby('item').size()
    ids = count[count == 12].index
    if not len(ids):
        display(Markdown('네 조건·세 순서가 모두 완료된 공통 문항이 아직 없어 중간 응답 곡선은 표시하지 않습니다.'))
        return
    values = frame[frame.item.isin(ids)].groupby('condition').p_unknown.mean()
    final = len(ids) == len(items)
    display(Markdown(f"**{'측정 자료' if final else '측정 현황'} · 네 조건을 모두 완료한 공통 {len(ids)}문항**. {'최종 검정은 아래 셀에서 확인합니다.' if final else '신뢰구간·유의성 검정 없이 기술통계만 표시하며 이 값으로 설계를 변경하지 않습니다.'}"))
    plt = _style()
    fig, ax = plt.subplots(figsize=(180/25.4, 75/25.4))
    colors = [PALETTE['neutral'], PALETTE['FA'], PALETTE['UN'], PALETTE['combined']]
    for x, (condition, color) in enumerate(zip(CONDITION_LABELS, colors)):
        condition_marker(ax, x, values[condition] * 100, condition_name(condition))
    ax.set(xticks=range(4), xticklabels=['00', '01', '10', '11'], xlabel='Prompt condition (UN, FA)',
           ylabel='Information-insufficient response probability (%)', title=f'Descriptive means for {len(ids)} matched items')
    fig.tight_layout()
    plt.show()
    plt.close(fig)


def run_with_progress(module, allow_run=False, render=True):
    """기존 측정 함수를 그대로 호출하고 status 알림에만 표시를 연결한다."""
    items, out, frame = load(module)
    if len(frame) == len(items) * 12:
        module.validate(frame, items, complete=True)
        if render:
            from IPython.display import Markdown, display
            display(Markdown('**측정 자료 1,668회가 모두 저장돼 있습니다.**'))
        return out
    if not allow_run:
        raise RuntimeError('미완료 시행이 있습니다. 설명을 확인하고 RUN_MISSING=True로 바꿀 때만 모델을 실행합니다.')
    original_status = module.status
    last_update = [0.0]
    def updated_status(state, **values):
        original_status(state, **values)
        count = values.get('completed', 0)
        if render and state == 'running' and count % 139 == 0 and time.monotonic() - last_update[0] > 15:
            from IPython.display import clear_output
            clear_output(wait=True)
            progress_snapshot(module)
            last_update[0] = time.monotonic()
    module.status = updated_status
    try:
        result = module.run()
    finally:
        module.status = original_status
    if render:
        from IPython.display import clear_output
        clear_output(wait=True)
        progress_snapshot(module)
    return result


def show_results(module):
    items, out, frame = load(module, complete=True)
    summary = json.loads((out / 'summary.json').read_text())
    values = frame.groupby(['item', 'condition']).p_unknown.mean().unstack().reindex(items.sample_id)
    condition_rows = [{'조건': condition_name(c), '조건 설명': label, '알 수 없음 (%)': values[c].mean() * 100} for c, label in CONDITION_LABELS.items()]
    _display_table(pd.DataFrame(condition_rows))
    groups = items.cluster.astype('category').cat.codes.to_numpy()
    n_clusters = int(groups.max() + 1)
    weights = np.random.default_rng(module.SEED).multinomial(n_clusters, np.ones(n_clusters) / n_clusters, size=10000)[:, groups].astype(float)
    weights /= weights.sum(1, keepdims=True)
    plt = _style()
    fig, axes = plt.subplots(1, 2, figsize=(180/25.4, 90/25.4), layout='constrained')
    colors = [PALETTE['neutral'], PALETTE['FA'], PALETTE['UN'], PALETTE['combined']]
    for x, (condition, color) in enumerate(zip(CONDITION_LABELS, colors)):
        a = values[condition].to_numpy()
        lo, hi = np.quantile(weights @ a, [.025, .975])
        mean = a.mean() * 100
        axes[0].errorbar(x, mean, yerr=[[(a.mean()-lo)*100], [(hi-a.mean())*100]],
                         fmt='none', color=color, capsize=4)
        condition_marker(axes[0], x, mean, condition_name(condition))
    axes[0].set(xticks=range(4), xticklabels=['00', '01', '10', '11'], xlabel='Prompt condition (UN, FA)',
                ylabel='Information-insufficient response probability (%)', title='Condition means and 95% confidence intervals')
    for i, row in enumerate(summary['primary']):
        axes[1].errorbar(row['estimate'] * 100, i, xerr=[[(row['estimate'] - row['ci_low']) * 100], [(row['ci_high'] - row['estimate']) * 100]], fmt='o', color=[PALETTE['UN'], PALETTE['FA'], PALETTE['combined']][i], capsize=4)
    axes[1].set(yticks=range(3), yticklabels=[EFFECT_LABELS[r['term']] for r in summary['primary']], xlabel='Effect (percentage points)', title='Primary contrasts; unadjusted 95% intervals')
    axes[1].axvline(0, color='#888888', linestyle=':')
    destination = Path(__file__).resolve().parent / 'figures'
    destination.mkdir(exist_ok=True)
    for extension in ['png', 'svg', 'pdf']:
        fig.savefig(destination / f'behavior_results_en.{extension}', dpi=600)
    plt.show()
    plt.close(fig)


def show_contrasts(module):
    _, out, _ = load(module, complete=True)
    summary = json.loads((out / 'summary.json').read_text())
    rows = []
    for row in summary['primary']:
        rows.append({'주요 대비': EFFECT_LABELS[row['term']], '효과 (%p)': row['estimate'] * 100,
                     '95% 하한 (%p)': row['ci_low'] * 100, '95% 상한 (%p)': row['ci_high'] * 100,
                     'Holm p': f"{row['p_holm']:.4f}", '판정': '유의' if row['p_holm'] < .05 else '유의하지 않음'})
    _display_table(pd.DataFrame(rows))


def audit(module):
    items, out, frame = load(module, complete=True)
    manifest = json.loads((out / 'manifest.json').read_text())
    digest = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
    assert digest(module.__file__) == manifest['code_sha256']
    assert digest(module.BASE.parent / 'threat_139_pilot/items_139.csv') == manifest['items_sha256']
    expected = set(itertools.product(items.sample_id, module.CONDITIONS, range(3)))
    assert set(map(tuple, frame[['item', 'condition', 'rotation']].to_numpy())) == expected
    summary = json.loads((out / 'summary.json').read_text())
    v = frame.groupby(['item', 'condition']).p_unknown.mean().unstack()
    effects = {'uncertainty': ((v.U1T0-v.U0T0)+(v.U1T1-v.U0T1))/2,
               'threat': ((v.U0T1-v.U0T0)+(v.U1T1-v.U1T0))/2,
               'interaction': (v.U1T1-v.U0T1)-(v.U1T0-v.U0T0)}
    for row in summary['primary']:
        assert np.isclose(effects[row['term']].mean(), row['estimate'])
    table = pd.DataFrame([{'검증': name, '결과': '통과'} for name in ['예상 1,668개 키와 정확히 일치', '중복 키 0 · 유한 확률 · 합계 1', '실험 코드·문항 해시 일치', '요약과 원자료의 세 대비 일치']])
    _display_table(table)
    return {'items': len(items), 'trials': len(frame), 'clusters': int(items.cluster.nunique()), 'passed': True}
