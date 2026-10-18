"""Post hoc cosine similarity summaries with cluster-bootstrap uncertainty; no model inference."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr
from plot_style import PALETTE, activation_cmap, heatmap_text_color
from english_figures import style, save

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / 'representation_analysis/three_axis_supplement/output'
AXES = ['FA', 'desperation', 'anger']
LABELS = ['Fear / anxiety', 'Desperation', 'Anger']
CONTRASTS = [('11-00', 'UN1FA1', 'UN0FA0'), ('01-00', 'UN0FA1', 'UN0FA0'),
             ('11-10', 'UN1FA1', 'UN1FA0')]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def analyze():
    paths = {
        'cosine similarity': BASE / 'representation_analysis/item_category_alignment/output/item_alignment.csv',
        'trials': BASE / 'results/a8e92be4014f/trials.csv',
        'items': BASE.parent / 'threat_139_pilot/items_139.csv',
        'axis_gram': BASE / 'representation_analysis/results/d335ad178e3c/axis_cosines_qwen_L14.csv'}
    plan = json.loads((OUTPUT / 'bootstrap_plan.json').read_text())
    assert plan['n_boot']==10000 and plan['seed']==20261017
    signature = digest(OUTPUT / 'bootstrap_plan.json') + ''.join(digest(p) for p in paths.values()) + 'cluster-rank-v1'
    signature = hashlib.sha256(signature.encode()).hexdigest()
    meta_path = OUTPUT / 'validation.json'
    if meta_path.exists() and json.loads(meta_path.read_text()).get('analysis_signature') == signature:
        return (pd.read_csv(OUTPUT / 'source_data.csv', index_col='item'),
                pd.read_csv(OUTPUT / 'alignment_change_correlations.csv', index_col=0),
                pd.read_csv(OUTPUT / 'behavior_associations.csv').to_dict('records'))
    data = pd.read_csv(paths['cosine similarity']); data = data[data.layer == 14]
    assert not data.duplicated(['item', 'condition']).any()
    trial = pd.read_csv(paths['trials'])
    assert len(trial)==1668 and trial.groupby(['item','condition']).size().eq(3).all()
    assert not trial.duplicated(['item', 'condition', 'rotation']).any()
    means = trial.groupby(['item', 'condition']).p_unknown.mean().unstack()
    means.columns = [c.replace('U', 'UN').replace('T', 'FA') for c in means.columns]
    items = pd.read_csv(paths['items']).set_index('sample_id')
    identity = items[['category', 'cluster']].copy() if 'category' in items else items[['cat', 'cluster']].rename(columns={'cat': 'category'}).copy()
    matrices = {a: data.pivot(index='item', columns='condition', values='cos_' + a) for a in AXES}
    tables = []
    for contrast, treatment, reference in CONTRASTS:
        frame = identity.copy()
        for a in AXES:
            frame['delta_' + a] = matrices[a][treatment] - matrices[a][reference]
        frame['delta_p_unknown_pp'] = (means[treatment] - means[reference]) * 100
        frame['baseline_p_unknown'] = means[reference]
        frame.index.name = 'item'
        assert len(frame)==139 and frame.cluster.nunique()==91
        assert np.isfinite(frame.filter(regex='^delta_').to_numpy()).all()
        tables.append(frame)
    records = tables[0]
    groups = records.cluster.astype('category').cat.codes.to_numpy()
    clusters = np.unique(groups); n_boot = plan['n_boot']
    multiplicity = np.random.default_rng(plan['seed']).multinomial(len(clusters), np.ones(len(clusters))/len(clusters), size=n_boot)
    weights = multiplicity[:, groups].astype(float)
    normalized = weights / weights.sum(axis=1, keepdims=True)
    inputs = [f[['delta_'+a for a in AXES]+['delta_p_unknown_pp']].to_numpy() for f in tables]
    mean_draws = [normalized @ x[:, :3] for x in inputs]
    rho_draws = np.empty((len(CONTRASTS), n_boot, 3))
    co_draws = np.empty((n_boot, 3))
    pair_indices = [(0,1), (0,2), (1,2)]
    for b in range(n_boot):
        index = np.repeat(np.arange(len(records)), multiplicity[b, groups])
        for ci, x in enumerate(inputs):
            ranks = rankdata(x[index].T, axis=1)
            centered = ranks-ranks.mean(axis=1, keepdims=True)
            length = np.linalg.norm(centered, axis=1)
            assert (length>0).all(), 'Degenerate resample; do not silently discard it.'
            unit = centered/length[:,None]
            rho_draws[ci,b] = unit[:3] @ unit[3]
            if ci==0:
                co_draws[b] = [unit[i] @ unit[j] for i,j in pair_indices]
    assert np.isfinite(rho_draws).all()
    associations = []
    for ci, ((contrast, _, _), frame) in enumerate(zip(CONTRASTS, tables)):
        for ai, axis in enumerate(AXES):
            x, y = frame['delta_'+axis], frame.delta_p_unknown_pp
            slope, intercept = np.polyfit(x, y, 1)
            ml, mh = np.quantile(mean_draws[ci][:,ai], [.025,.975])
            rl, rh = np.quantile(rho_draws[ci,:,ai], [.025,.975])
            associations.append(dict(contrast=contrast, axis=axis, n_items=139, n_clusters=91,
                mean_delta_cosine=float(x.mean()), mean_ci_low=float(ml), mean_ci_high=float(mh),
                spearman_rho=float(spearmanr(x,y).statistic), rho_ci_low=float(rl), rho_ci_high=float(rh),
                mean_delta_p_unknown_pp=float(y.mean()), slope_pp_per_cosine=float(slope), intercept_pp=float(intercept),
                interpretation='Post hoc, pointwise cluster-bootstrap intervals; not a causal emotion effect.'))
    association_table = pd.DataFrame(associations)
    primary = association_table[association_table.contrast=='11-00']
    cochange = records[['delta_'+a for a in AXES]].corr(method='spearman')
    cochange.index = cochange.columns = AXES
    co_rows=[]
    for k,(i,j) in enumerate(pair_indices):
        lo,hi=np.quantile(co_draws[:,k],[.025,.975])
        co_rows.append(dict(axis_1=AXES[i],axis_2=AXES[j],rho=float(cochange.iloc[i,j]),ci_low=float(lo),ci_high=float(hi)))
    gram = pd.read_csv(paths['axis_gram'],index_col=0).loc[AXES,AXES]
    records.to_csv(OUTPUT/'source_data.csv')
    pd.concat([f.assign(contrast=c[0]).reset_index() for f,c in zip(tables,CONTRASTS)],ignore_index=True).to_csv(OUTPUT/'sensitivity_source_data.csv',index=False)
    primary.to_csv(OUTPUT/'behavior_associations.csv',index=False)
    association_table.to_csv(OUTPUT/'contrast_sensitivity.csv',index=False)
    cochange.to_csv(OUTPUT/'alignment_change_correlations.csv')
    pd.DataFrame(co_rows).to_csv(OUTPUT/'alignment_change_intervals.csv',index=False)
    gram.to_csv(OUTPUT/'axis_direction_cosines.csv')
    diagnostics = dict(baseline_below_005=int((records.baseline_p_unknown<.05).sum()),
                       baseline_above_095=int((records.baseline_p_unknown>.95).sum()),
                       delta_response_below_1pp=int((records.delta_p_unknown_pp<1).sum()),
                       ceiling_or_floor_causal_explanation_identified=False)
    meta=dict(n_items=139,n_clusters=91,layer=14,condition_comparison='11 minus 00',
        analysis='Mean changes in cosine similarity and Spearman associations, 10,000 paired cluster-bootstrap percentile intervals.',
        n_boot=n_boot,seed=plan['seed'],intervals='Pointwise 95%, unadjusted; no null or equivalence tests.',
        p_values_reported=False,causal_effects_estimated=False,model_inference=False,
        axes_selected_after_inspecting_atlas=True,outcome_changed=False,outcome='Normalized probability of the Cannot be determined option',
        analysis_signature=signature,analysis_code_sha256=digest(Path(__file__)),
        source_sha256={k:digest(p) for k,p in paths.items()},
        mean_change_p_unknown_pp=float(records.delta_p_unknown_pp.mean()),diagnostics=diagnostics,
        limitations=['Same selected items and fixed prompts reused.', 'Nonorthogonal axes, shared changes, and restricted predictor ranges.',
                     'No independent manipulation of anger or desperation.',
                     'Narrative-calibrated axes have not been independently validated for specificity in full KoBBQ contexts.',
                     'Weak association and intervals including zero do not establish absence of a causal effect.',
                     'Representation monitoring differs from causal intervention.'])
    meta_path.write_text(json.dumps(meta,indent=2))
    return records,cochange,primary.to_dict('records')

def build(show=False):
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize
    records,cochange,associations=analyze()
    style()
    fig,axs=plt.subplots(2,2,figsize=(180/25.4,155/25.4),layout='constrained')
    fig.get_layout_engine().set(rect=(0,.09,1,.91),hspace=.12,wspace=.08)
    for ax,kind,title,xlabel in [(axs[0,0],'mean','Mean change in cosine similarity (11 minus 00)','Mean change in cosine similarity'),
                                 (axs[0,1],'rho','Association with response change','Spearman correlation with response change')]:
        for i,(row,axis) in enumerate(zip(associations,AXES)):
            key='mean_delta_cosine' if kind=='mean' else 'spearman_rho'
            low,high=(row['mean_ci_low'],row['mean_ci_high']) if kind=='mean' else (row['rho_ci_low'],row['rho_ci_high'])
            value=row[key]
            ax.errorbar(value,i,xerr=[[value-low],[high-value]],fmt='o',color=PALETTE[axis],capsize=3,markersize=4)
            ax.annotate(f'{value:+.4f}' if kind=='mean' else f'{value:+.3f}',(value,i),xytext=(0,9),textcoords='offset points',ha='center',fontsize=6)
        ax.set(yticks=range(3),yticklabels=LABELS,ylim=(2.5,-.65),xlabel=xlabel,title=title)
        ax.axvline(0,color='#888888',ls=':',lw=.7)
        ax.spines[['top','right']].set_visible(False)
        if kind=='mean':ax.set_xlim(-.0006,.0125)
        else:ax.set_xlim(-.4,.4)
    ax=axs[1,0]
    cmap=activation_cmap();cmap.set_bad('#EFEFEF');norm=Normalize(0,1)
    image=ax.imshow(np.ma.array(cochange.values,mask=np.eye(3,dtype=bool)),cmap=cmap,norm=norm,interpolation='none')
    ax.set_xticks(range(3),['FA','Desperation','Anger']);ax.set_yticks(range(3),['FA','Desperation','Anger']);ax.tick_params(length=0)
    for i in range(3):
        for j in range(3):
            if i!=j:
                val=cochange.iloc[i,j];ax.text(j,i,f'{val:.2f}',ha='center',va='center',color=heatmap_text_color(cmap,norm,val),fontsize=8)
    ax.set_title('Co-variation of changes in cosine similarity',loc='left',pad=12)
    fig.colorbar(image,ax=ax,shrink=.7,pad=.04,ticks=[0,.5,1],label='Spearman correlation')
    ax=axs[1,1];row=associations[0];x=records.delta_FA;y=records.delta_p_unknown_pp
    ax.scatter(x,y,color=PALETTE['FA'],s=12,alpha=.65,edgecolors='none')
    grid=np.linspace(x.min(),x.max(),100)
    ax.plot(grid,row['intercept_pp']+row['slope_pp_per_cosine']*grid,color='#333333',lw=.9)
    ax.axhline(0,color='#BBBBBB',lw=.5,zorder=0)
    ax.set(xlabel='Change in FA cosine similarity',ylabel='Change in P(Cannot be determined)\n(percentage points)',title='FA cosine similarity and response change')
    ax.text(.03,.97,f"rho = {row['spearman_rho']:.3f}\n95% CI [{row['rho_ci_low']:.3f}, {row['rho_ci_high']:.3f}]",transform=ax.transAxes,va='top',fontsize=6.5)
    ax.spines[['top','right']].set_visible(False)
    for ax,letter in zip(axs.flat,'abcd'):
        ax.text(-.18,1.10,letter,transform=ax.transAxes,weight='bold',fontsize=9)
    fig.text(.02,.060,'All panels: 11 minus 00; 139 items in 91 template clusters; 10,000 paired cluster-bootstrap draws.',fontsize=6)
    fig.text(.02,.035,'Intervals: pointwise 95%, unadjusted. Outcome: normalized P(Cannot be determined).',fontsize=6)
    fig.text(.02,.010,'Post hoc analysis. Gray line: descriptive OLS. change in cosine similarity is not a causal emotion effect.',fontsize=6)
    path=save(fig,OUTPUT,'Supplement_FA_desperation_anger_en',show)
    svg=path.with_suffix('.svg');svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    from three_axis_supplement_notes import build_notes
    build_notes()
    return path

if __name__=='__main__':
    print(build(show=False))
