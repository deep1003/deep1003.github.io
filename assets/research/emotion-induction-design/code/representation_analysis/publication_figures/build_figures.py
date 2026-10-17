"""Publication figures from immutable cached representations. No model inference."""
from pathlib import Path
import hashlib
import json
import shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

HERE = Path(__file__).resolve().parent
DEFAULT_DATA = HERE.parent / 'results' / 'd335ad178e3c'
CONDITIONS = ['UN0FA0', 'UN1FA0', 'UN0FA1', 'UN1FA1']
CODES = ['00', '10', '01', '11']
CONCEPTS = ['UN', 'FA', 'calm', 'sadness', 'anger', 'desperation', 'joy']
LABELS = ['Uncertainty (UN)', 'Fear / anxiety (FA)', 'Calm', 'Sadness', 'Anger', 'Desperation', 'Joy']
COLORS = ['#777777', '#C34835', '#2868A3', '#8054A1']
MARKERS = ['o', '^', 's', 'D']
SPACES = ['semantic', 'qwen_L14']
TITLES = ['Semantic concept profiles', 'Internal concept profiles, layer 14']
CMAP = LinearSegmentedColormap.from_list('purple_white_teal', ['#7853A2', '#FFFFFF', '#167D8D'])


def setup():
    plt.rcParams.update({'font.family': 'Arial', 'font.size': 7, 'axes.titlesize': 7,
        'axes.labelsize': 7, 'xtick.labelsize': 6, 'ytick.labelsize': 6,
        'legend.fontsize': 6, 'axes.linewidth': .6, 'lines.linewidth': .7,
        'xtick.major.width': .6, 'ytick.major.width': .6, 'xtick.major.size': 2,
        'ytick.major.size': 2, 'pdf.fonttype': 42, 'ps.fonttype': 42,
        'svg.fonttype': 'none', 'axes.unicode_minus': True, 'savefig.facecolor': 'white'})


def panel(ax, letter, title):
    ax.text(-.20, 1.09, letter, transform=ax.transAxes, weight='bold', fontsize=8, va='bottom')
    ax.set_title(title, loc='left', pad=12, weight='normal')


def save(fig, name, out):
    for ext in ['pdf', 'svg', 'png']:
        fig.savefig(out / f'{name}.{ext}', dpi=600)
    fig.savefig(out / f'{name}_preview.png', dpi=180)
    plt.close(fig)


def build(data=DEFAULT_DATA, output=None):
    setup()
    data = Path(data)
    out = Path(output) if output else HERE / 'output'
    out.mkdir(parents=True, exist_ok=True)
    source = out / 'source_data'
    source.mkdir(exist_ok=True)
    scores = pd.read_csv(data / 'scores.csv')
    pca = json.loads((data / 'profile_pca.json').read_text())
    matrices = {}
    for space in SPACES:
        m = scores[scores.space == space].pivot(index='condition', columns='axis', values='standardized').reindex(index=CONDITIONS, columns=CONCEPTS)
        matrices[space] = m.subtract(m.loc['UN0FA0'])
        matrices[space].to_csv(source / f'fig1_delta_{space}.csv')
        pd.DataFrame(pca[space]['coordinates']).to_csv(source / f'fig1_pca_{space}.csv', index=False)
        pd.DataFrame(pca[space]['components'], columns=CONCEPTS, index=['PC1', 'PC2']).to_csv(source / f'fig1_loadings_{space}.csv')
    # Explicit physical dimensions. PCA distance is not distorted by display aspect.
    fig = plt.figure(figsize=(180 / 25.4, 143 / 25.4))
    grid = fig.add_gridspec(2, 2, left=.135, right=.90, bottom=.105, top=.86, hspace=.64, wspace=.53, height_ratios=[1, 1.12])
    for col, space in enumerate(SPACES):
        ax = fig.add_subplot(grid[0, col])
        xy = pd.DataFrame(pca[space]['coordinates']).set_index('condition').loc[CONDITIONS]
        for c, code, color, marker in zip(CONDITIONS, CODES, COLORS, MARKERS):
            x, y = xy.loc[c, ['PC1', 'PC2']]
            ax.scatter(x, y, s=30, marker=marker, color=color, edgecolors='white', linewidths=.4, zorder=3)
            ax.annotate(code, (x, y), xytext=(5, 6), textcoords='offset points', fontsize=6)
        xmin, xmax = xy.PC1.min(), xy.PC1.max()
        width = (xmax - xmin) * 1.34
        cx = (xmin + xmax) / 2
        cy = (xy.PC2.min() + xy.PC2.max()) / 2
        ax.set_xlim(cx - width / 2, cx + width / 2)
        ax.set_ylim(cy - width * .31, cy + width * .31)
        ax.set_aspect('equal', adjustable='box')
        ax.spines[['top', 'right']].set_visible(False)
        ax.xaxis.set_major_locator(MaxNLocator(4))
        ax.yaxis.set_major_locator(MaxNLocator(3))
        ratios = pca[space]['explained_variance_ratio']
        ax.set_xlabel(f'PC1 ({ratios[0] * 100:.1f}%; a.u.)')
        ax.set_ylabel(f'PC2 ({ratios[1] * 100:.1f}%; a.u.)')
        panel(ax, 'ab'[col], TITLES[col])
        hm = fig.add_subplot(grid[1, col])
        values = matrices[space].T.values
        img = hm.imshow(values, cmap=CMAP, norm=TwoSlopeNorm(vmin=-.65, vcenter=0, vmax=.65), aspect='auto', interpolation='none')
        for i in range(7):
            for j in range(4):
                v = values[i, j]
                hm.text(j, i, f'{v:+.2f}' if j else '0.00', ha='center', va='center', fontsize=6, color='white' if abs(v) > .44 else '#161616')
        hm.set_xticks(range(4), CODES)
        hm.set_yticks(range(7), LABELS)
        hm.set_xlabel('Prompt condition (UN, FA)')
        hm.tick_params(length=0, pad=4)
        hm.set_xticks(np.arange(-.5, 4, 1), minor=True)
        hm.set_yticks(np.arange(-.5, 7, 1), minor=True)
        hm.grid(which='minor', color='#e6e6e6', linewidth=.35)
        hm.tick_params(which='minor', length=0)
        for spine in hm.spines.values(): spine.set_visible(False)
        panel(hm, 'cd'[col], 'Change from reference prompt (00)')
    cbax = fig.add_axes([.925, .142, .012, .245])
    cb = fig.colorbar(img, cax=cbax, ticks=[-.6, -.3, 0, .3, .6])
    cb.set_label('Change in anchor-standardized projection (a.u.)', fontsize=6, labelpad=5)
    cb.ax.tick_params(labelsize=5.5)
    handles = [Line2D([], [], marker=m, color=c, linestyle='none', markersize=4, label=l) for m,c,l in zip(MARKERS,COLORS,['00  Reference','10  UN only','01  FA only','11  UN + FA'])]
    fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(.52, .99), ncol=4, frameon=False, handletextpad=.4, columnspacing=1.8)
    fig.text(.52, .035, 'Separate PCA fits and calibrations; four fixed prompts; alignment does not establish emotion.', ha='center', fontsize=6)
    save(fig, 'Figure_1_concept_alignment', out)

    # Convergent-looking target scores require a separate discriminant-validity check.
    fig = plt.figure(figsize=(180 / 25.4, 150 / 25.4))
    grid = fig.add_gridspec(2, 2, left=.15, right=.90, bottom=.13, top=.94, hspace=.72, wspace=.65, height_ratios=[1, 1])
    for col, space in enumerate(SPACES):
        ax = fig.add_subplot(grid[0,col])
        cosine = pd.read_csv(data / f'axis_cosines_{space}.csv', index_col=0).loc[CONCEPTS,CONCEPTS]
        cosine.to_csv(source / f'extended1_axis_cosines_{space}.csv')
        masked = np.ma.array(cosine.values, mask=np.eye(7,dtype=bool))
        cmap = plt.get_cmap('cividis').copy();cmap.set_bad('#f1f1f1')
        img = ax.imshow(masked, vmin=0, vmax=1, cmap=cmap, interpolation='none')
        for i in range(7):
            for j in range(7):
                if i != j:ax.text(j,i,f'{cosine.iloc[i,j]:.2f}', ha='center',va='center',fontsize=5,color='white' if cosine.iloc[i,j]<.45 else 'black')
        short=['UN','FA','Calm','Sad.','Anger','Desp.','Joy']
        ax.set_xticks(range(7),short,rotation=45,ha='right');ax.set_yticks(range(7),short)
        ax.tick_params(length=0)
        for spine in ax.spines.values():spine.set_visible(False)
        panel(ax,'ab'[col],TITLES[col])
    cb=fig.colorbar(img,cax=fig.add_axes([.925,.62,.012,.29]),ticks=[0,.5,1]);cb.set_label('Axis cosine similarity',fontsize=6)
    checks=pd.read_csv(data/'axis_audit'/'heldout_axis_identification.csv')
    checks.to_csv(source/'extended1_heldout_identification.csv',index=False)
    ax=fig.add_subplot(grid[1,0])
    for space,color,offset,label,marker in [('semantic','#777777',-.12,'Semantic','o'),('qwen_L14','#2868A3',.12,'Internal, L14','s')]:
        part=checks[checks.space==space].set_index('axis').loc[CONCEPTS]
        ax.scatter(part.correct_of_4,np.arange(7)+offset,color=color,s=18,label=label,marker=marker,zorder=3)
    ax.set_yticks(range(7),LABELS);ax.invert_yaxis();ax.set_xlim(-.25,4.25);ax.set_xticks(range(5));ax.set_xlabel('Correctly identified held-out pairs (of 4)')
    ax.spines[['top','right']].set_visible(False);ax.legend(frameon=False,loc='upper left',bbox_to_anchor=(-.02,-.25),ncol=2)
    panel(ax,'c','Between-concept specificity')
    ax=fig.add_subplot(grid[1,1])
    pc=np.array(pca['qwen_L14']['components'][0]);y=np.arange(7)
    ax.barh(y,pc,color='#989898',height=.65);ax.set_yticks(y,LABELS);ax.invert_yaxis();ax.set_xlim(0,.65);ax.set_xticks([0,.2,.4,.6]);ax.set_xlabel('PC1 loading (a.u.)')
    ax.spines[['top','right']].set_visible(False);panel(ax,'d','Internal PC1 loads on all concepts')
    save(fig,'Extended_Data_1_axis_specificity',out)
    files=[data/'scores.csv',data/'profile_pca.json',data/'axis_audit'/'heldout_axis_identification.csv']+[data/f'axis_cosines_{s}.csv' for s in SPACES]
    provenance={'data_directory':str(data),'input_sha256':{str(p.relative_to(data)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'figure_width_mm':180,'font':'Arial','font_pt':{'body':7,'minimum':5,'panel':8},'pca_observations':4,'pca_features':7,'inference_performed':False,'heatmap_center':0,'heatmap_limits':[-.65,.65],'pca_equal_aspect':True,'comparison_caution':'Separate representation spaces and anchor calibrations. Not comparable emotion intensities.'}
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2))
    caption = HERE / 'Captions_and_methods.md'
    if caption.exists():
        shutil.copy2(caption, out / caption.name)
    return out

if __name__ == '__main__':
    print(build())
