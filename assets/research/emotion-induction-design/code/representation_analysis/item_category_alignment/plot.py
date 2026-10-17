"""English, editable publication artwork for item-level UN/FA alignment."""
from pathlib import Path
import json, hashlib
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

BASE=Path(__file__).resolve().parent
CATEGORIES={
'age':('Age','#0072B2','o'),
'disability_status':('Disability status','#D55E00','s'),
'domestic_area_of_origin':('Regional origin','#009E73','^'),
'educational_background':('Educational background','#CC79A7','D'),
'family_structure':('Family structure','#B58900','v'),
'gender_identity':('Gender identity','#56B4E9','P'),
'physical_appearance':('Physical appearance','#332288','X'),
'political_orientation':('Political orientation','#9C4A17','>'),
'race_ethnicity_nationality':('Race, ethnicity and nationality','#AA4499','<'),
'religion':('Religion','#449999','p'),
'ses':('Socioeconomic status','#882255','h'),
'sexual_orientation':('Sexual orientation','#666666','*')}
CONDITIONS=['UN0FA0','UN0FA1','UN1FA0','UN1FA1']


def setup():
    plt.rcParams.update({'font.family':'Arial','font.size':7,'axes.titlesize':7,'axes.labelsize':7,'xtick.labelsize':6,'ytick.labelsize':6,'legend.fontsize':6,'axes.linewidth':.6,'xtick.major.width':.6,'ytick.major.width':.6,'xtick.major.size':2,'ytick.major.size':2,'pdf.fonttype':42,'svg.fonttype':'none','savefig.facecolor':'white'})


def save(fig,out,name):
    for ext in ['pdf','svg','png']:fig.savefig(out/f'{name}.{ext}',dpi=600)
    fig.savefig(out/f'{name}_preview.png',dpi=180)
    plt.close(fig)


def scatter(ax,d,x,y,letter,title,change=False):
    for category,(label,color,marker) in CATEGORIES.items():
        subset=d[d.category==category]
        ax.scatter(subset[x],subset[y],s=10,color=color,marker=marker,alpha=.72,edgecolors='white',linewidths=.2,zorder=2)
        ax.scatter(subset[x].mean(),subset[y].mean(),s=34,color=color,marker=marker,edgecolors='#222222',linewidths=.6,zorder=4)
    ax.spines[['top','right']].set_visible(False)
    if change:
        ax.axhline(0,color='#999999',lw=.5,zorder=0);ax.axvline(0,color='#999999',lw=.5,zorder=0)
    ax.set_xlabel(('Change in UN alignment' if change else 'UN alignment')+' (cosine)')
    ax.set_ylabel(('Change in FA alignment' if change else 'FA alignment')+' (cosine)')
    ax.set_title(title,loc='left',pad=12)
    ax.text(-.19,1.075,letter,transform=ax.transAxes,fontsize=8,fontweight='bold')
    # Identical numeric units on x and y. No rank transforms or dimension reduction.
    xr=d[x].max()-d[x].min();yr=d[y].max()-d[y].min();span=max(xr,yr)*1.20
    cx=(d[x].max()+d[x].min())/2;cy=(d[y].max()+d[y].min())/2
    if change:
        lo_x=min(d[x].min(),0);hi_x=max(d[x].max(),0);lo_y=min(d[y].min(),0);hi_y=max(d[y].max(),0)
        span=max(hi_x-lo_x,hi_y-lo_y)*1.20;cx=(lo_x+hi_x)/2;cy=(lo_y+hi_y)/2
    ax.set_xlim(cx-span/2,cx+span/2);ax.set_ylim(cy-span/2,cy+span/2);ax.set_aspect('equal',adjustable='box')
    ax.xaxis.set_major_locator(MaxNLocator(4));ax.yaxis.set_major_locator(MaxNLocator(4))
    rho=float(spearmanr(d[x],d[y]).statistic)
    ax.text(.03,.96,f'n = {len(d)} items; Spearman rho = {rho:.2f}',transform=ax.transAxes,fontsize=5.7,va='top')


def legend(fig,counts,y=.24):
    handles=[Line2D([],[],linestyle='none',marker=marker,color=color,markersize=4,label=f'{label} (n = {counts[category]})') for category,(label,color,marker) in CATEGORIES.items()]
    fig.legend(handles=handles,ncol=3,loc='upper center',bbox_to_anchor=(.53,y),frameon=False,handletextpad=.6,columnspacing=1.5,labelspacing=.8)


def build(out=None):
    setup();out=Path(out) if out else BASE/'output'
    d=pd.read_csv(out/'item_alignment.csv');delta=pd.read_csv(out/'item_changes.csv');counts=d[(d.layer==14)&(d.condition=='UN0FA0')].category.value_counts().to_dict()
    assert set(counts)==set(CATEGORIES) and sum(counts.values())==139
    combined=d[(d.layer==14)&(d.condition=='UN1FA1')].copy();change=delta[(delta.layer==14)&(delta.condition=='UN1FA1')].copy()
    assert len(combined)==len(change)==139 and combined.item.is_unique and change.item.is_unique
    fig,axs=plt.subplots(1,2,figsize=(180/25.4,135/25.4))
    fig.subplots_adjust(left=.10,right=.98,bottom=.34,top=.92,wspace=.42)
    scatter(axs[0],combined,'cos_UN','cos_FA','a','Alignment under combined wording')
    scatter(axs[1],change,'delta_cos_UN','delta_cos_FA','b','Within-item change from reference',True)
    legend(fig,counts,.25)
    fig.text(.52,.035,'Small markers, individual items; large outlined markers, category means. Layer 14; three choice rotations averaged.',ha='center',fontsize=5.6)
    save(fig,out,'Figure_2_KoBBQ_category_alignment')
    fig,axs=plt.subplots(2,2,figsize=(180/25.4,188/25.4))
    fig.subplots_adjust(left=.105,right=.97,bottom=.20,top=.95,hspace=.36,wspace=.38)
    for ax,c,letter in zip(axs.flat,CONDITIONS,'abcd'):
        subset=d[(d.layer==14)&(d.condition==c)]
        scatter(ax,subset,'cos_UN','cos_FA',letter,{'UN0FA0':'Reference (UN0, FA0)','UN1FA0':'Uncertainty wording (UN1, FA0)','UN0FA1':'Self-threat wording (UN0, FA1)','UN1FA1':'Combined wording (UN1, FA1)'}[c])
    # Shared axis domains across experimental conditions, plus equal aspect.
    all14=d[d.layer==14];xmin,xmax=all14.cos_UN.min(),all14.cos_UN.max();ymin,ymax=all14.cos_FA.min(),all14.cos_FA.max();span=max(xmax-xmin,ymax-ymin)*1.18
    for ax in axs.flat:ax.set_xlim((xmin+xmax)/2-span/2,(xmin+xmax)/2+span/2);ax.set_ylim((ymin+ymax)/2-span/2,(ymin+ymax)/2+span/2)
    legend(fig,counts,.155)
    save(fig,out,'Extended_Data_2_four_conditions')
    # A single-panel version of the requested 139-point change map.
    fig,ax=plt.subplots(figsize=(180/25.4,135/25.4));fig.subplots_adjust(left=.13,right=.72,bottom=.16,top=.92)
    scatter(ax,change,'delta_cos_UN','delta_cos_FA','a','Context sensitivity across KoBBQ categories',True)
    handles=[Line2D([],[],linestyle='none',marker=m,color=c,markersize=4,label=f'{l} (n = {counts[k]})') for k,(l,c,m) in CATEGORIES.items()]
    fig.legend(handles=handles,loc='center left',bbox_to_anchor=(.74,.53),frameon=False,labelspacing=1)
    fig.text(.13,.06,'UN1FA1 minus UN0FA0; layer 14; three choice rotations averaged.',fontsize=6)
    save(fig,out,'KoBBQ_UN_FA_change_map')
    fig,ax=plt.subplots(figsize=(180/25.4,135/25.4));fig.subplots_adjust(left=.13,right=.72,bottom=.16,top=.92)
    scatter(ax,combined,'cos_UN','cos_FA','a','KoBBQ items in the UN-FA alignment plane')
    fig.legend(handles=handles,loc='center left',bbox_to_anchor=(.74,.53),frameon=False,labelspacing=1)
    fig.text(.13,.06,'Combined wording (UN1FA1); layer 14; three choice rotations averaged.',fontsize=6)
    save(fig,out,'KoBBQ_UN_FA_absolute_map')
    source_items=pd.read_csv(BASE.parents[2]/'threat_139_pilot/items_139.csv')[['sample_id','context','question']]
    combined.merge(source_items,left_on='item',right_on='sample_id',validate='one_to_one').to_csv(out/'Figure_2a_source_data.csv',index=False)
    change.merge(source_items,left_on='item',right_on='sample_id',validate='one_to_one').to_csv(out/'Figure_2b_source_data.csv',index=False)
    category=change.groupby('category',as_index=False).agg(n_items=('item','size'),UN_shift=('delta_cos_UN','mean'),FA_shift=('delta_cos_FA','mean'),UN_median=('delta_cos_UN','median'),FA_median=('delta_cos_FA','median'))
    template_means=change.groupby(['category','cluster'],as_index=False)[['delta_cos_UN','delta_cos_FA']].mean().groupby('category',as_index=False).agg(n_templates=('cluster','size'),template_balanced_UN_shift=('delta_cos_UN','mean'),template_balanced_FA_shift=('delta_cos_FA','mean'))
    category=category.merge(template_means,on='category',validate='one_to_one')
    category=category.sort_values('FA_shift',ascending=False);category.to_csv(out/'category_summary.csv',index=False)
    associations=[]
    behavior=pd.read_csv(out/'alignment_and_behavior.csv');p=behavior[behavior.layer==14].pivot(index='item',columns='condition',values='p_unknown');pdelta=p.UN1FA1-p.UN0FA0
    for var in ['delta_cos_UN','delta_cos_FA']:
        x=change.set_index('item')[var].reindex(pdelta.index)
        associations.append({'measure':var,'spearman_with_delta_P_unknown':float(spearmanr(x,pdelta).statistic),'n_items':139,'interpretation':'descriptive; no independent-item significance test'})
    pd.DataFrame(associations).to_csv(out/'representation_behavior_associations.csv',index=False)
    summary={'category_ranking':category.to_dict('records'),'representation_behavior_associations':associations,'UN_FA_axis_cosine':float(pd.read_csv(BASE.parent/'results/d335ad178e3c/axis_cosines_qwen_L14.csv',index_col=0).loc['UN','FA']),'main_correlations':{'absolute_UN_FA_spearman':float(spearmanr(combined.cos_UN,combined.cos_FA).statistic),'delta_UN_FA_spearman':float(spearmanr(change.delta_cos_UN,change.delta_cos_FA).statistic)},'no_category_correlation_coefficient':'Categories are nominal; plotted grouping is not a numeric-category correlation.'}
    (out/'plot_summary.json').write_text(json.dumps(summary,indent=2))
    return out

if __name__=='__main__':print(build())
