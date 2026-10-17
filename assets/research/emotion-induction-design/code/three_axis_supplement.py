"""Post hoc descriptive FA/desperation/anger alignment-behavior analysis. No inference."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from plot_style import PALETTE, activation_cmap, heatmap_text_color
from english_figures import style, save

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / 'representation_analysis/three_axis_supplement/output'
AXES = ['FA', 'desperation', 'anger']
LABELS = ['Fear / anxiety', 'Desperation', 'Anger']

def analyze():
    paths = {
        'alignment': BASE / 'representation_analysis/item_category_alignment/output/item_alignment.csv',
        'trials': BASE / 'results/a8e92be4014f/trials.csv',
        'items': BASE.parent / 'threat_139_pilot/items_139.csv',
        'axis_gram': BASE / 'representation_analysis/results/d335ad178e3c/axis_cosines_qwen_L14.csv'}
    data = pd.read_csv(paths['alignment'])
    data = data[data.layer == 14]
    assert not data.duplicated(['item', 'condition']).any()
    trial = pd.read_csv(paths['trials'])
    assert not trial.duplicated(['item', 'condition', 'rotation']).any()
    means = trial.groupby(['item', 'condition']).p_unknown.mean().unstack()
    items = pd.read_csv(paths['items']).set_index('sample_id')
    records = items[['category', 'cluster']].copy() if 'category' in items else items[['cat', 'cluster']].rename(columns={'cat': 'category'}).copy()
    for axis in AXES:
        matrix = data.pivot(index='item', columns='condition', values='cos_' + axis)
        records['delta_' + axis] = matrix.UN1FA1 - matrix.UN0FA0
    records['delta_p_unknown_pp'] = (means.U1T1 - means.U0T0) * 100
    records.index.name = 'item'
    assert len(records) == 139 and records.cluster.nunique() == 91
    assert np.isfinite(records.filter(regex='^delta_').to_numpy()).all()
    cochange = records[['delta_' + a for a in AXES]].corr(method='spearman')
    cochange.index = cochange.columns = AXES
    gram = pd.read_csv(paths['axis_gram'], index_col=0).loc[AXES, AXES]
    associations = []
    for axis in AXES:
        x, y = records['delta_' + axis], records.delta_p_unknown_pp
        slope, intercept = np.polyfit(x, y, 1)
        associations.append(dict(axis=axis, n_items=len(records),
            spearman_rho=float(spearmanr(x, y).statistic),
            mean_delta_cosine=float(x.mean()), slope_pp_per_cosine=float(slope),
            intercept_pp=float(intercept), interpretation='Post hoc descriptive association; not a causal emotion effect.'))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    records.to_csv(OUTPUT / 'source_data.csv')
    pd.DataFrame(associations).to_csv(OUTPUT / 'behavior_associations.csv', index=False)
    cochange.to_csv(OUTPUT / 'alignment_change_correlations.csv')
    gram.to_csv(OUTPUT / 'axis_direction_cosines.csv')
    meta = dict(n_items=139, n_clusters=91, layer=14, condition_comparison='11 minus 00',
        analysis='Post hoc descriptive Spearman associations and pooled OLS display lines.',
        p_values_reported=False, causal_effects_estimated=False, model_inference=False,
        axes_selected_after_inspecting_atlas=True,
        analysis_code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        source_sha256={k: hashlib.sha256(p.read_bytes()).hexdigest() for k, p in paths.items()},
        mean_change_p_unknown_pp=float(records.delta_p_unknown_pp.mean()),
        limitations=['Same selected items and prompts reused.',
                     'Nonorthogonal axes and strongly correlated alignment changes.',
                     'No independent manipulation of anger or desperation.',
                     'Input-evoked hidden alignment is not experienced emotion or causal mediation.'])
    (OUTPUT / 'validation.json').write_text(json.dumps(meta, indent=2))
    return records, cochange, associations

def build(show=False):
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize
    records, cochange, associations = analyze()
    style()
    fig, axs = plt.subplots(2, 2, figsize=(180/25.4, 150/25.4), layout='constrained')
    fig.get_layout_engine().set(rect=(0, .07, 1, .93), hspace=.10, wspace=.09)
    ax = axs[0, 0]
    mask = np.ma.array(cochange.values, mask=np.eye(3, dtype=bool))
    cmap = activation_cmap(); cmap.set_bad('#EFEFEF')
    norm = Normalize(0, 1)
    image = ax.imshow(mask, cmap=cmap, norm=norm, interpolation='none')
    ticks = ['FA', 'Desperation', 'Anger']
    ax.set_xticks(range(3), ticks); ax.set_yticks(range(3), ticks)
    ax.tick_params(length=0)
    for i in range(3):
        for j in range(3):
            if i != j:
                val = cochange.iloc[i, j]
                ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                        color=heatmap_text_color(cmap, norm, val), fontsize=8)
    ax.set_title('Co-variation of alignment changes', loc='left', pad=12)
    bar = fig.colorbar(image, ax=ax, shrink=.7, pad=.04, ticks=[0, .5, 1])
    bar.set_label('Spearman correlation', fontsize=7)
    y = records.delta_p_unknown_pp
    lower, upper = float(y.min()), float(y.max())
    pad = (upper-lower)*.10
    for ax, axis, label, row in zip([axs[0, 1], axs[1, 0], axs[1, 1]], AXES, LABELS, associations):
        x = records['delta_' + axis]
        ax.scatter(x, y, color=PALETTE[axis], s=12, alpha=.65, edgecolors='none')
        grid = np.linspace(x.min(), x.max(), 100)
        ax.plot(grid, row['intercept_pp'] + row['slope_pp_per_cosine']*grid, color='#333333', lw=.9)
        ax.axhline(0, color='#BBBBBB', lw=.5, zorder=0)
        ax.set(ylim=(lower-pad, upper+pad), xlabel=f'Change in {label.lower()} alignment (cosine)',
               ylabel='Change in information-insufficient\nresponse probability (percentage points)')
        ax.set_title(f'{label}: alignment and response change', loc='left', pad=12)
        ax.text(.03, .96, f"Spearman rho = {row['spearman_rho']:.3f}",
                transform=ax.transAxes, va='top', fontsize=7)
        ax.spines[['top', 'right']].set_visible(False)
    for ax, letter in zip(axs.flat, 'abcd'):
        ax.text(-.17, 1.08, letter, transform=ax.transAxes, weight='bold', fontsize=9)
    fig.text(.02, .040, '11-minus-00 changes; 139 selected items in 91 template clusters. Lines: pooled OLS fits.', fontsize=6)
    fig.text(.02, .012, 'Post hoc descriptive associations. Co-alignment does not establish independent or joint causal emotion effects.', fontsize=6)
    path = save(fig, OUTPUT, 'Supplement_FA_desperation_anger_en', show)
    svg = path.with_suffix('.svg')
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    return path

if __name__ == '__main__':
    print(build(show=False))
