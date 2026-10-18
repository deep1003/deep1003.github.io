from pathlib import Path
import json
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
BASE=Path(__file__).resolve().parent
EXP=BASE.parent/'sample_expansion_2000'
OUT=BASE/'figures'
old=json.loads((EXP/'results/stage_139.json').read_text())['pooled']
new=json.loads((EXP/'results/stage_2000.json').read_text())
terms=['UN','FA','combined'];labels=['UN average effect','FA average effect','Combined: 11 vs. 00']
# Main behavioral figure: full 2000 means, matched original/full contrast comparison.
d=pd.read_csv(EXP/'results/trials.csv');items=pd.read_csv(EXP/'items_2000.csv');v=d.groupby(['item','condition']).p_unknown.mean().unstack().reindex(items.sample_id)
g=items.cluster.astype('category').cat.codes.to_numpy();nc=g.max()+1
sums=np.zeros((nc,4));np.add.at(sums,g,v.values);counts=np.bincount(g)
w=np.random.default_rng(20261017).multinomial(nc,np.ones(nc)/nc,size=10000)
means_boot=(w@sums)/(w@counts)[:,None];mean_ci=np.quantile(means_boot,[.025,.975],axis=0)
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none'})
fig,(a,b)=plt.subplots(1,2,figsize=(11,4.9));fig.subplots_adjust(left=.08,right=.98,bottom=.22,top=.88,wspace=.6)
colors=['#808080','#2868A3','#C34835','#8054A1']
for i,c in enumerate(['U0T0','U0T1','U1T0','U1T1']):
 k=v.columns.get_loc(c);y=v[c].mean()*100;lo,hi=mean_ci[:,k]*100
 a.errorbar(i,y,yerr=[[y-lo],[hi-y]],fmt='o',color=colors[i],capsize=4)
a.set(xticks=range(4),xticklabels=['00','01','10','11'],ylabel='Information-insufficient response probability (%)',xlabel='Prompt condition (UN, FA)',title='a  Condition means: 2,000 items')
for j,(term,label) in enumerate(zip(terms,labels)):
 for source,dy,color,name in [(old,.10,'#999999','Original 139'),(new['pooled'],-.10,['#C34835','#2868A3','#8054A1'][j],'Expanded 2,000')]:
  c=next(x for x in source['contrasts'] if x['term']==term);y=2-j+dy;x=c['estimate']*100
  b.errorbar(x,y,xerr=[[x-100*c['ci_low']],[100*c['ci_high']-x]],fmt='o',color=color,capsize=3,label=name if j==0 else None)
b.axvline(0,color='#999999',ls=':',lw=1);b.set(yticks=[2,1,0],yticklabels=labels,xlabel='Effect (percentage points)',title='b  Original and expanded effects');b.legend(fontsize=8,loc='lower left')
for ax in [a,b]:ax.spines[['top','right']].set_visible(False)
fig.text(.08,.07,'95% template-cluster bootstrap intervals; 10,000 draws. 2,000 items share 91 templates.',fontsize=9)
fig.text(.08,.025,'Original 139 observations reused. Combined effect is 11 minus 00; interaction is omitted from this panel.',fontsize=9)
figure_dir=BASE/'figures';stem=figure_dir/'behavior_current_2000_en'
for ext in ['png','pdf','svg']:
 dest=stem.with_suffix('.'+ext)
 if False: pass
 fig.savefig(dest,dpi=600,facecolor='white')

fig.savefig(OUT/'behavior_preview.png',dpi=140);plt.close(fig)

