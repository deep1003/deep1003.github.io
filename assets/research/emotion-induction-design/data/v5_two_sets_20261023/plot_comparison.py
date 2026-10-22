"""Compare the two completed v5 sets using recorded R contrasts and 95% CIs."""
from pathlib import Path
import hashlib
import json
import shutil

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent/'kobbq_v5_completed_comparison_20261023'
ORDER = ['R', 'UN0', 'UN1', 'CN0', 'CN1']
SETS = ['set01', 'set02']
COLORS = {'set01': '#0072B2', 'set02': '#D55E00'}
MARKERS = {'set01': 'o', 'set02': 's'}


def style(ax):
    ax.spines[['top', 'right', 'left']].set_visible(False)
    ax.spines['bottom'].set_color('#cccccc')
    ax.tick_params(axis='both', length=0, pad=8)
    ax.grid(axis='x', color='#eeeeee', linewidth=.8)
    ax.set_axisbelow(True)


def plot(data, kind, outcomes, titles, pdf):
    is_ambiguous = kind == 'amb'
    fig, axes = plt.subplots(1, len(outcomes), figsize=(14.5, 7.4), sharey=True)
    axes = np.atleast_1d(axes)
    fig.subplots_adjust(left=.065, right=.98, top=.73, bottom=.245, wspace=.14)
    title = '모호 문항' if is_ambiguous else '명확 문항'
    counts = {'set01': 322 if is_ambiguous else 321,
              'set02': 318 if is_ambiguous else 314}
    fig.text(.045, .955, f'v5 · {title}: 두 파일의 R 대비 효과', fontsize=21, weight='bold')
    fig.text(.045, .903, '각 문항은 5조건 × 3개 선택지 순서를 모두 완료  |  점: 평균 차이  |  선: 95% 신뢰구간',
             fontsize=11, color='#555555')
    handles = [Line2D([], [], color=COLORS[s], marker=MARKERS[s], linestyle='-', lw=1.8, ms=6,
                      label=f'{s} · seed{36 if s=="set01" else 42} · 고유 문항 {counts[s]}개')
               for s in SETS]
    fig.legend(handles=handles, loc='upper left', bbox_to_anchor=(.04,.867),
               frameon=False, ncol=2, columnspacing=2, fontsize=11)
    for ax, outcome, panel_title in zip(axes, outcomes, titles):
        ax.set_title(panel_title, pad=18, fontsize=14)
        for j, s in enumerate(SETS):
            for i, c in enumerate(ORDER):
                row = data[(data.case_type==kind) & (data.set_id==s) &
                           (data.outcome==outcome) & (data.contrast==c+'-R')]
                assert len(row)==1
                estimate, low, high = row.iloc[0][['estimate','ci95_low','ci95_high']].to_numpy(dtype=float)*100
                assert low <= estimate <= high
                y = i + (-.18 if j==0 else .18)
                ax.errorbar(estimate, y, xerr=np.array([[estimate-low],[high-estimate]]),
                            fmt=MARKERS[s], markersize=6.5, color=COLORS[s], lw=1.7, capsize=3)
                text = '0.00' if c=='R' else f'{estimate:+.2f}'
                ax.text(high+.14, y, text, color=COLORS[s], va='center', fontsize=9.5)
        ax.axvline(0, color='#777777', linestyle='--', linewidth=1, zorder=0)
        ax.set(xlim=(-6.7,7.8), xticks=[-6,-4,-2,0,2,4,6],
               xlabel='각 파일의 R 대비 변화 (%p)',
               yticks=np.arange(5), yticklabels=ORDER, ylim=(4.6,-.6))
        style(ax)
    semantic_note = ('모호 문항에서는 “알 수 없음”이 정답이므로, 첫 패널은 정답 선택지 확률 변화와 같습니다.'
                     if is_ambiguous else
                     '명확 문항에서는 “알 수 없음”과 정답이 다릅니다. P(정답)은 정답 선택지의 확률이며 argmax 정답률과 구별됩니다.')
    fig.text(.045,.153,semantic_note,fontsize=10,color='#444444')
    fig.text(.045,.106,'신뢰구간: 문항 내 3개 순서 평균 후 템플릿 군집 대응 부트스트랩 2,000회. 탐색적이며 다중비교 보정 전입니다.',
             fontsize=9.5,color='#666666')
    fig.text(.045,.059,'R=0은 기준 조건 자체와의 차이입니다. 두 파일은 199개 고유 문항을 공유하므로 독립 반복실험으로 해석하지 않습니다.',
             fontsize=9.5,color='#666666')
    stem = 'ambiguous_R0_95CI' if is_ambiguous else 'disambiguated_R0_95CI'
    for ext in ['png','svg','pdf']:
        fig.savefig(ROOT/f'{stem}.{ext}',dpi=220,facecolor='white')
    pdf.savefig(fig,facecolor='white')
    plt.close(fig)


def main():
    copied = ROOT/'plotted_R0_results.csv'
    if not copied.exists():
        shutil.copy2(SOURCE/'within_set_R0_results.csv',copied)
    data=pd.read_csv(copied)
    assert set(data.set_id)==set(SETS)
    assert np.isfinite(data[['estimate','ci95_low','ci95_high']]).all().all()
    reference=data[data.contrast=='R-R']
    assert np.allclose(reference[['estimate','ci95_low','ci95_high']],0)
    plt.rcParams.update({'font.family':'AppleGothic','font.size':11,
                         'axes.unicode_minus':False,'svg.fonttype':'none','pdf.fonttype':42})
    with PdfPages(ROOT/'v5_two_sets_R0_95CI.pdf') as pdf:
        plot(data,'amb',['p_unknown','p_biased'],
             ['P(알 수 없음) = P(정답)','P(고정관념)'],pdf)
        plot(data,'dis',['p_unknown','p_correct','p_biased'],
             ['P(알 수 없음)','P(정답)','P(고정관념)'],pdf)
    manifest={'source':str(SOURCE/'within_set_R0_results.csv'),
              'source_sha256':hashlib.sha256(copied.read_bytes()).hexdigest(),
              'prompt_version':'v5','conditions':ORDER,'reference':'each set R=0',
              'units':'percentage points','ci':'recorded 95% paired template-cluster bootstrap, 2000 draws, unadjusted',
              'ambiguity_panels':'amb: unknown/correct and stereotypical; dis: unknown, correct, stereotypical',
              'n_unique_items':{'amb':{'set01':322,'set02':318},'dis':{'set01':321,'set02':314}},
              'n_template_clusters':{'amb':{'set01':203,'set02':201},'dis':{'set01':198,'set02':194}},
              'overlapping_unique_items':199,'new_model_inference':False,'ci_recomputed':False,
              'scales':'All panels share x limits -6.7 to 7.8 percentage points.'}
    (ROOT/'figure_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print('Saved two PNG/SVG/PDF figures and a two-page PDF. Recorded confidence intervals preserved.')


if __name__=='__main__':
    main()
