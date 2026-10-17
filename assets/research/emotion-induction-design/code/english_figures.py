"""American-English publication artwork. Uses cached measurements only."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap,TwoSlopeNorm
from matplotlib.patches import FancyBboxPatch

BASE=Path(__file__).resolve().parent
NAMES={'semantic':'Semantic concept profiles','qwen_L14':'Internal concept profiles, layer 14'}
AXES=['UN','FA','calm','sadness','anger','desperation','joy']
LABELS=['Uncertainty','Fear / anxiety','Calm','Sadness','Anger','Desperation','Joy']
CONDITIONS=['UN0FA0','UN1FA0','UN0FA1','UN1FA1']
COLORS=['#777777','#C34835','#2868A3','#8054A1']
MARKERS=['o','^','s','D']

def style():
    plt.rcParams.update({'font.family':'Arial','font.size':7,'axes.titlesize':7,'axes.labelsize':7,'xtick.labelsize':6,'ytick.labelsize':6,'legend.fontsize':6,'axes.linewidth':.6,'xtick.major.width':.6,'ytick.major.width':.6,'pdf.fonttype':42,'svg.fonttype':'none','axes.unicode_minus':True})

def save(fig,folder,name,show=True):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
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
    style();data=Path(data);scores=pd.read_csv(data/'scores.csv');cmap=LinearSegmentedColormap.from_list('signed',['#7853A2','white','#167D8D'])
    fig,axs=plt.subplots(1,2,figsize=(180/25.4,95/25.4));fig.subplots_adjust(left=.14,right=.88,bottom=.18,top=.84,wspace=.60)
    for ax,space,letter in zip(axs,NAMES,'ab'):
        v=scores[scores.space==space].pivot(index='condition',columns='axis',values='standardized').reindex(index=CONDITIONS,columns=AXES);v=v.subtract(v.loc['UN0FA0']).T
        im=ax.imshow(v,aspect='auto',cmap=cmap,norm=TwoSlopeNorm(vmin=-.65,vcenter=0,vmax=.65),interpolation='none')
        for i in range(7):
            for j in range(4):
                value=v.iloc[i,j];ax.text(j,i,f'{value:+.2f}',ha='center',va='center',fontsize=5.5,color='white' if abs(value)>.44 else '#222')
        ax.set_xticks(range(4),['00','10','01','11']);ax.set_yticks(range(7),LABELS);ax.set_xlabel('Prompt condition (UN, FA)');ax.tick_params(length=0)
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
    for x,y,c,desc in [(.05,.49,'UN0FA0','Reference'),(.54,.49,'UN1FA0','Uncertainty wording'),(.05,.32,'UN0FA1','Self-threat wording'),(.54,.32,'UN1FA1','Combined wording')]:box(x,y,.41,.13,c+'\n'+desc)
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
