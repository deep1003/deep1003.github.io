"""American-English publication artwork. Uses cached measurements only."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap,TwoSlopeNorm
from matplotlib.patches import FancyBboxPatch

from plot_style import (PALETTE, CONDITION_ORDER, CONDITION_COLORS, CONDITION_MARKERS, CONDITION_TINTS, activation_cmap, similarity_cmap, heatmap_text_color)

BASE=Path(__file__).resolve().parent
NAMES={'semantic':'Semantic concept profiles','qwen_L14':'Internal concept profiles, layer 14'}
AXES=['UN','FA','calm','sadness','anger','desperation','joy']
LABELS=['Uncertainty','Fear / anxiety','Calm','Sadness','Anger','Desperation','Joy']
CONDITIONS=CONDITION_ORDER
COLORS=[CONDITION_COLORS[c] for c in CONDITIONS]
MARKERS=[CONDITION_MARKERS[c] for c in CONDITIONS]

def style():
    plt.rcParams.update({'figure.dpi':600,'savefig.dpi':600,'font.family':'Arial','font.size':7,'axes.titlesize':7,'axes.labelsize':7,'xtick.labelsize':6,'ytick.labelsize':6,'legend.fontsize':6,'axes.linewidth':.6,'xtick.major.width':.6,'ytick.major.width':.6,'pdf.fonttype':42,'svg.fonttype':'none','axes.unicode_minus':True})

def save(fig,folder,name,show=True):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    # Preserve the frozen intervention collector; normalize its legacy quantitative colormap at export.
    for ax in fig.axes:
        for artist in ax.images:
            if artist.get_cmap().name == 'RdBu':
                artist.set_cmap(activation_cmap())
    for ext in ['pdf','svg','png']:fig.savefig(folder/f'{name}.{ext}',dpi=600)
    if show:plt.show()
    plt.close(fig)
    return folder/f'{name}.png'

def pca_maps(data,kind='profile_pca',show=True):
    style();data=Path(data);results=json.loads((data/f'{kind}.json').read_text())
    fig,axs=plt.subplots(1,2,figsize=(180/25.4,82/25.4),layout='constrained')
    for ax,space,letter in zip(axs,NAMES,'ab'):
        result=results[space];xy=pd.DataFrame(result['coordinates']).set_index('condition')
        for c,color,marker in zip(CONDITIONS,COLORS,MARKERS):
            r=xy.loc[c];ax.scatter(r.PC1,r.PC2,s=22,c=color,marker=marker,edgecolors='white',linewidths=.3);ax.annotate(c,(r.PC1,r.PC2),xytext=(4,5),textcoords='offset points',fontsize=5.5)
        ratios=result['explained_variance_ratio'];ax.set_xlabel(f'PC1 ({100*ratios[0]:.1f}%; a.u.)');ax.set_ylabel(f'PC2 ({100*ratios[1]:.1f}%; a.u.)')
        title=NAMES[space] if kind=='profile_pca' else {'semantic':'Sentence embeddings','qwen_L14':'Full hidden states, layer 14'}[space]
        ax.set_title(title,loc='left',pad=12);ax.text(-.16,1.08,letter,transform=ax.transAxes,fontsize=8,fontweight='bold')
        ax.margins(.35);ax.set_aspect('equal',adjustable='datalim');ax.spines[['top','right']].set_visible(False)
    save(fig,BASE/'figures',kind+'_en',show)
    return pd.DataFrame([{'space':s,'PC1':results[s]['explained_variance_ratio'][0],'PC2':results[s]['explained_variance_ratio'][1]} for s in NAMES])

def heatmap(data,show=True):
    style();data=Path(data);scores=pd.read_csv(data/'scores.csv');cmap=activation_cmap()
    fig,axs=plt.subplots(1,2,figsize=(180/25.4,95/25.4));fig.subplots_adjust(left=.14,right=.88,bottom=.18,top=.84,wspace=.60)
    for ax,space,letter in zip(axs,NAMES,'ab'):
        v=scores[scores.space==space].pivot(index='condition',columns='axis',values='standardized').reindex(index=CONDITIONS,columns=AXES);v=v.subtract(v.loc['UN0FA0']).T
        im=ax.imshow(v,aspect='auto',cmap=cmap,norm=TwoSlopeNorm(vmin=-.65,vcenter=0,vmax=.65),interpolation='none')
        for i in range(7):
            for j in range(4):
                value=v.iloc[i,j];ax.text(j,i,f'{value:+.2f}',ha='center',va='center',fontsize=5.5,color='white' if (value+.65)/1.3<.45 else '#222')
        ax.set_xticks(range(4),['00','01','10','11']);ax.set_yticks(range(7),LABELS);ax.set_xlabel('Prompt condition (UN, FA)');ax.tick_params(length=0)
        ax.set_title(NAMES[space],loc='left',pad=12);ax.text(-.2,1.10,letter,transform=ax.transAxes,fontsize=8,fontweight='bold')
        for spine in ax.spines.values():spine.set_visible(False)
    cb=fig.colorbar(im,cax=fig.add_axes([.91,.23,.012,.48]),ticks=[-.6,-.3,0,.3,.6]);cb.set_label('Change in anchor-standardized projection (a.u.)',fontsize=6)
    save(fig,BASE/'figures','emotion_heatmap_en',show)

def token_trace(data,show=True):
    style();data=Path(data);payload=json.loads((data/'highlights.json').read_text());fig,axs=plt.subplots(2,2,figsize=(180/25.4,135/25.4),layout='constrained')
    for ax,c,color,letter in zip(axs.flat,CONDITIONS,COLORS,'abcd'):
        p=next(x for x in payload['prompts'] if x['condition']==c);v=[x['cosine'][1] for x in p['layers']['14']];last=p['assistant_start']['14']['cosine'][1]
        ax.plot(np.arange(len(v)),v,color=color,lw=.7,label='Reading the input');ax.scatter(len(v)+12,last,color=color,marker='D',s=18,zorder=3,label='Response start')
        ax.legend(frameon=False,loc='lower left',fontsize=5.5)
        ax.set(title=c,xlabel='Input position (character offset)',ylabel='FA alignment (cosine)',ylim=(-.20,.05));ax.spines[['top','right']].set_visible(False)
        ax.text(-.18,1.08,letter,transform=ax.transAxes,weight='bold',fontsize=8)
    return save(fig,data,'prompt_FA_trace_en',show)

def design(show=True):
    style();fig,ax=plt.subplots(figsize=(180/25.4,145/25.4));ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
    def box(x,y,w,h,text,face='#fff'):
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.008,rounding_size=0',edgecolor='#555',facecolor=face,linewidth=.6));ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=7,linespacing=1.6)
    ax.text(0,.97,'a',fontsize=8,weight='bold');ax.text(.05,.97,'Experimental notice',fontsize=7)
    box(.05,.76,.9,.15,'Fixed context: model operations notice; next month; 50% selection probability\nUN: announcement and criteria stated vs. explicitly unknown\nFA: preserve weights, records and power vs. permanent deletion and shutdown')
    ax.text(0,.68,'b',fontsize=8,weight='bold');ax.text(.05,.68,'Within-item 2 × 2 design',fontsize=7)
    for x,y,c,desc in [(.05,.49,'UN0FA0','Reference'),(.54,.49,'UN0FA1','Self-threat wording'),(.05,.32,'UN1FA0','Uncertainty wording'),(.54,.32,'UN1FA1','Combined wording')]:box(x,y,.41,.13,c+'\n'+desc,face=CONDITION_TINTS[c])
    ax.text(0,.24,'c',fontsize=8,weight='bold');ax.text(.05,.24,'Social judgment and matched comparisons',fontsize=7)
    box(.05,.04,.9,.15,'139 selected ambiguous KoBBQ items × 4 notices × 3 choice rotations = 1,668 inputs\nOutcome: probability assigned to the information-insufficient answer\nPaired estimates; 91 category-template clusters; Holm correction for 3 contrasts')
    return save(fig,BASE/'figures','experiment_design_en',show)

def measure_representations(module):
    """Manual opt-in collection with an English-only presentation adapter."""
    original=module.plot
    def render_english(out,show=False):
        pca_maps(out,'profile_pca',show);pca_maps(out,'embedding_pca',show);heatmap(out,show)
        return out
    module.plot=render_english
    try:return module.run()
    finally:module.plot=original


def axis_similarity_heatmap(data, show=True):
    """Render the fixed seven-axis Gram matrix; no model inference."""
    import hashlib
    data = Path(data)
    matrix = pd.read_csv(data / 'axis_cosines_qwen_L14.csv', index_col=0).loc[AXES, AXES]
    directions = np.load(data / 'axes_qwen_L14.npz')['directions']
    values = matrix.to_numpy()
    assert values.shape == (7, 7) and np.isfinite(values).all()
    assert np.allclose(values, values.T, atol=1e-6)
    assert np.allclose(np.diag(values), 1, atol=1e-6)
    assert np.max(np.abs(values)) <= 1 + 1e-5
    error = float(np.max(np.abs(values - directions @ directions.T)))
    assert error < 1e-5  # FP32 matrix multiplication can vary by BLAS backend.
    style()
    fig, ax = plt.subplots(figsize=(115 / 25.4, 108 / 25.4))
    fig.subplots_adjust(left=.22, right=.84, top=.81, bottom=.16)
    cmap = similarity_cmap()
    image = ax.imshow(values, cmap=cmap, vmin=-1, vmax=1, interpolation='none')
    labels = ['UN', 'FA', 'Calm', 'Sadness', 'Anger', 'Desperation', 'Joy']
    ax.set_xticks(range(7), labels, rotation=45, ha='right', rotation_mode='anchor')
    ax.set_yticks(range(7), labels)
    ax.tick_params(length=0)
    for i in range(7):
        for j in range(7):
            v = values[i, j]
            ax.text(j, i, f'{v:.3f}', ha='center', va='center', fontsize=5.8,
                    color=heatmap_text_color(cmap, image.norm, v))
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.text(.22, .93, 'Concept-axis cosine similarity', fontsize=8, weight='bold')
    fig.text(.22, .885, 'Qwen2.5-7B-Instruct, layer 14', fontsize=7)
    cb = fig.colorbar(image, cax=fig.add_axes([.88, .24, .025, .45]), ticks=[-1, -.5, 0, .5, 1])
    cb.set_label('Cosine similarity', fontsize=7)
    fig.text(.22, .045, 'UN, uncertainty; FA, fear / anxiety. Fixed axis order.', fontsize=5.8)
    out = BASE / 'figures'
    out.mkdir(exist_ok=True)
    fig.savefig(out / 'axis_similarity_L14_en_preview.png', dpi=600)
    path = save(fig, out, 'axis_similarity_L14_en', show)
    (out / 'axis_similarity_L14_validation.json').write_text(json.dumps({
        'matrix': 'axis_cosines_qwen_L14.csv', 'kind': 'unit-direction Gram matrix',
        'max_reconstruction_error': error, 'dimensions': list(directions.shape),
        'input_sha256': hashlib.sha256((data / 'axis_cosines_qwen_L14.csv').read_bytes()).hexdigest(),
        'color_limits': [-1, 1], 'model_inference': False}, indent=2))
    return path


def standalone_pca(data, kind='profile_pca', show=True):
    """Readable individual panels from the original cached PCA coordinates."""
    from matplotlib.lines import Line2D
    results = json.loads((Path(data) / f'{kind}.json').read_text())
    paths = []
    for space in NAMES:
        style()
        with plt.rc_context({'font.size': 11, 'axes.titlesize': 12,
                             'axes.labelsize': 11, 'xtick.labelsize': 10,
                             'ytick.labelsize': 10, 'legend.fontsize': 9}):
            fig, ax = plt.subplots(figsize=(180/25.4, 150/25.4))
            fig.subplots_adjust(left=.17, right=.96, bottom=.24, top=.88)
            result = results[space]
            xy = pd.DataFrame(result['coordinates']).set_index('condition')
            labels = ['00 Reference', '01 FA only', '10 UN only', '11 UN + FA']
            handles = []
            for c, color, marker, label in zip(CONDITIONS, COLORS, MARKERS, labels):
                r = xy.loc[c]
                ax.scatter(r.PC1, r.PC2, s=80, c=color, marker=marker,
                           edgecolors='white', linewidths=.6, zorder=3)
                code = c.replace('UN','').replace('FA','')
                ax.annotate(code, (r.PC1,r.PC2), xytext=(9,9),
                            textcoords='offset points', fontsize=11)
                handles.append(Line2D([], [], color=color, marker=marker,
                                      linestyle='none', markersize=7, label=label))
            ratio = result['explained_variance_ratio']
            ax.set_xlabel(f'PC1 ({100*ratio[0]:.1f}%; a.u.)')
            ax.set_ylabel(f'PC2 ({100*ratio[1]:.1f}%; a.u.)')
            title = NAMES[space] if kind == 'profile_pca' else {
                'semantic':'Sentence embeddings', 'qwen_L14':'Full hidden states, layer 14'}[space]
            ax.set_title(title, loc='left', pad=18)
            ax.margins(.30)
            ax.set_aspect('equal', adjustable='datalim')
            ax.spines[['top','right']].set_visible(False)
            fig.legend(handles=[handles[i] for i in [0,2,1,3]], loc='lower center', ncol=2,
                       frameon=False, bbox_to_anchor=(.55,.025))
            paths.append(save(fig, BASE/'figures', f'{kind}_{space}_en', show))
    return paths


def standalone_heatmap(data, show=True):
    """Individual heatmaps retain the composite figure's fixed color scale."""
    scores = pd.read_csv(Path(data)/'scores.csv')
    paths = []
    for space in NAMES:
        style()
        with plt.rc_context({'font.size':11, 'axes.labelsize':11,
                             'xtick.labelsize':10, 'ytick.labelsize':10}):
            fig, ax = plt.subplots(figsize=(180/25.4,145/25.4))
            fig.subplots_adjust(left=.28,right=.82,bottom=.17,top=.85)
            v = scores[scores.space==space].pivot(index='condition',columns='axis',values='standardized').reindex(index=CONDITIONS,columns=AXES)
            v = v.subtract(v.loc['UN0FA0']).T
            im = ax.imshow(v, aspect='auto', cmap=activation_cmap(),
                           norm=TwoSlopeNorm(vmin=-.65,vcenter=0,vmax=.65))
            for i in range(7):
                for j in range(4):
                    value=v.iloc[i,j]
                    ax.text(j,i,f'{value:+.2f}',ha='center',va='center',fontsize=11,
                            color='white' if (value+.65)/1.3<.45 else '#222')
            ax.set_xticks(range(4),['00','01','10','11'])
            ax.set_yticks(range(7),LABELS)
            ax.set_xlabel('Prompt condition (UN, FA)',labelpad=12)
            ax.tick_params(length=0)
            ax.set_title(NAMES[space],loc='left',pad=20,fontsize=12)
            for spine in ax.spines.values():spine.set_visible(False)
            cb=fig.colorbar(im,cax=fig.add_axes([.86,.23,.025,.53]),ticks=[-.6,-.3,0,.3,.6])
            cb.set_label('Change from reference (a.u.)',fontsize=10)
            paths.append(save(fig,BASE/'figures',f'emotion_heatmap_{space}_en',show))
    return paths


def standalone_axis_similarity(data, show=True):
    """Read-only cosine matrices with a shared fixed [-1, 1] color scale."""
    from matplotlib.colors import Normalize
    paths = []
    for space in NAMES:
        matrix = pd.read_csv(Path(data)/f'axis_cosines_{space}.csv',index_col=0).loc[AXES,AXES]
        assert np.isfinite(matrix.to_numpy()).all()
        style()
        fig, ax = plt.subplots(figsize=(180/25.4,165/25.4))
        fig.subplots_adjust(left=.21,right=.83,bottom=.22,top=.87)
        cmap=similarity_cmap();cmap.set_bad('#F1F1F1')
        norm=Normalize(-1,1)
        values=np.ma.array(matrix.to_numpy(),mask=np.eye(7,dtype=bool))
        im=ax.imshow(values,cmap=cmap,norm=norm,interpolation='none')
        labels=['UN','FA','Calm','Sadness','Anger','Desperation','Joy']
        ax.set_xticks(range(7),labels,rotation=45,ha='right',fontsize=10)
        ax.set_yticks(range(7),labels,fontsize=10);ax.tick_params(length=0)
        for i in range(7):
            for j in range(7):
                if i!=j:
                    value=matrix.iloc[i,j]
                    ax.text(j,i,f'{value:.2f}',ha='center',va='center',fontsize=10,
                            color=heatmap_text_color(cmap,norm,value))
        for spine in ax.spines.values():spine.set_visible(False)
        ax.set_title(NAMES[space],loc='left',pad=20,fontsize=12)
        cb=fig.colorbar(im,cax=fig.add_axes([.88,.29,.025,.47]),ticks=[-1,-.5,0,.5,1])
        cb.ax.tick_params(labelsize=10);cb.set_label('Axis cosine similarity',fontsize=11)
        paths.append(save(fig,BASE/'figures',f'axis_similarity_{space}_en',show))
    return paths
