"""Publish the authoritative study palette and an English figure legend."""
from pathlib import Path
import json
import matplotlib.pyplot as plt
import numpy as np
from plot_style import (PALETTE, CONDITION_ORDER, CONDITION_COLORS, CONDITION_MARKERS,
                        CONCEPT_ORDER, CATEGORY_STYLES, ACTIVATION_STOPS, activation_cmap,
                        similarity_cmap, SIMILARITY_STOPS, REPRESENTATION_COLORS, FIT_COLOR)
BASE=Path(__file__).resolve().parent

def build(show=False):
    from english_figures import style, save
    style()
    spec=dict(condition_order=CONDITION_ORDER,concept_order=CONCEPT_ORDER,
              identities=PALETTE,condition_colors=CONDITION_COLORS,condition_markers=CONDITION_MARKERS,
              category_styles={k:dict(label=v[0],color=v[1],marker=v[2]) for k,v in CATEGORY_STYLES.items()},
              representations=REPRESENTATION_COLORS,fit_color=FIT_COLOR,
              quantitative_scales=dict(activation=ACTIVATION_STOPS,similarity=SIMILARITY_STOPS),
              rules=['Identity colors are fixed across graphs, text highlights and legends.',
                     'Condition 11 is purple; condition identity colors are independent of quantitative value colors.',
                     'Continuous colors encode values, not emotion identities; color bars state units and sign.',
                     'All activation heatmaps use dark red through light yellow; negative values are retained.',
                     'Similarity matrices use the same dark-red-to-bright-yellow scale and the range [-1, 1].',
                     'Condition panels retain 00, 01, 10, 11; category colors are a separate fixed encoding.',
                     'Token backgrounds use the shared red-yellow value scale; concept selectors use fixed identity colors.'])
    (BASE/'color-specification.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2))
    fig=plt.figure(figsize=(180/25.4,148/25.4))
    def heading(y,text):fig.text(.04,y,text,fontsize=8,weight='bold')
    heading(.94,'a  Experimental conditions')
    ax=fig.add_axes([.04,.81,.92,.09]);ax.set_xlim(-.4,3.4);ax.set_ylim(-.5,.5);ax.axis('off')
    labels=['00  Reference','01  FA only','10  UN only','11  UN + FA']
    for i,(c,l) in enumerate(zip(CONDITION_ORDER,labels)):
        ax.scatter(i,0,s=45,color=CONDITION_COLORS[c],marker=CONDITION_MARKERS[c]);ax.text(i+.10,0,l,ha='left',va='center',fontsize=7)
    heading(.74,'b  Concept identities')
    labels=['Uncertainty','Fear / anxiety','Calm','Sadness','Anger','Desperation','Joy']
    for i,(key,label) in enumerate(zip(CONCEPT_ORDER,labels)):
        col=i%4;row=i//4
        fig.text(.05+col*.235,.66-row*.08,'●',color=PALETTE[key],fontsize=14,va='center')
        fig.text(.08+col*.235,.66-row*.08,label,fontsize=7,va='center')
    heading(.47,'c  Quantitative scales (not identity colors)')
    for y,cmap,label in [(.35,activation_cmap(),'Activation / cosine similarity: lower to higher values'),(.21,similarity_cmap(),'Concept similarity: cosine -1 to +1')]:
        ax=fig.add_axes([.05,y,.9,.035]);ax.imshow(np.linspace(0,1,256)[None,:],cmap=cmap,aspect='auto',vmin=0,vmax=1);ax.axis('off');fig.text(.05,y+.055,label,fontsize=7)
    fig.text(.05,.11,'Dark red to bright yellow encodes magnitude; read the labeled scale for each measure.',fontsize=6.5)
    fig.text(.05,.065,'KoBBQ category colors are fixed separately. Dark-gray solid lines denote pooled OLS fits.',fontsize=6.5)
    return save(fig,BASE/'figures','Study_color_guide_en',show)

if __name__=='__main__':build()
