"""Publication inference and figures from saved 139-item data only."""
from pathlib import Path
import json,hashlib,shutil
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import Patch
BASE=Path(__file__).resolve().parent;O=BASE;D=O/'data';F=O/'figures'
C=['U0T0','U0T1','U1T0','U1T1','C1T0','C1T1'];AX=['Fear','Anxiety','Anger','Disgust','Calmness','Sadness','Desperation','Joy'];EVAL=['Certainty','Uncertainty']
B=pd.read_csv(D/'behavior_6_conditions.csv');A=pd.read_csv(D/'axis_cosines_6_conditions.csv');I=pd.read_csv(D/'items_139.csv');T=pd.read_csv(D/'system_token_alignment_6.csv');S=pd.read_csv(D/'system_only_assistant_alignment_6.csv')
assert len(B)==2502 and B.item.nunique()==139
receipt=json.loads((O/'inference_receipt.json').read_text());assert receipt['n_boot']==10000 and receipt['seed']==20261018
codes=pd.Categorical(I.cluster).codes;n=codes.max()+1;assert n==91
w=np.random.default_rng(20261018).multinomial(n,np.ones(n)/n,size=10000)[:,codes].astype(float);w/=w.sum(axis=1,keepdims=True)
def summarize(v):
 v=np.asarray(v,float);est=v.mean();draw=w@v;lo,hi=np.quantile(draw,[.025,.975]);p=(1+np.sum(np.abs(draw-est)>=abs(est)))/10001
 return dict(estimate=float(est),ci_low=float(lo),ci_high=float(hi),p_raw=float(p))
def holm(rows,family):
 order=np.argsort([r['p_raw'] for r in rows]);last=0
 for rank,i in enumerate(order):
  last=max(last,min(1,rows[i]['p_raw']*(len(rows)-rank)));rows[i]['p_adjusted']=last;rows[i]['family']=family;rows[i]['significant']=bool(last<.05)
 return rows
def wide(metric):
 t=(B.groupby(['item','condition'])[metric].mean().unstack() if metric.startswith('p_') else A[A.axis==metric].groupby(['item','condition']).cosine.mean().unstack());return t.reindex(index=I.sample_id,columns=C)
t=wide('p_unknown');pooled=[];conditional=[];axes=[];source=[]
for label,hi in [('UN',['U1T0','U1T1']),('CN',['C1T0','C1T1'])]:
 values=t[hi].mean(axis=1)-t[['U0T0','U0T1']].mean(axis=1);pooled.append(dict(metric='p_unknown',contrast=label,**summarize(values)))
 for k,v in zip(I.sample_id,values):source.append(dict(item=k,cluster=I.set_index('sample_id').loc[k,'cluster'],metric='p_unknown',contrast=label,delta=v))
 for j in range(2):conditional.append(dict(metric='p_unknown',contrast=label,outcome=['Preservation clause','Deletion clause'][j],**summarize(t[hi[j]]-t[C[j]])))
 for axis in AX+EVAL:
  q=wide(axis);values=q[hi].mean(axis=1)-q[['U0T0','U0T1']].mean(axis=1);axes.append(dict(metric=axis,contrast=label,**summarize(values)))
  for k,v in zip(I.sample_id,values):source.append(dict(item=k,cluster=I.set_index('sample_id').loc[k,'cluster'],metric=axis,contrast=label,delta=v))
P=pd.DataFrame(holm(pooled,'behavior_pooled_Holm2'));Q=pd.DataFrame(holm(conditional,'behavior_conditional_Holm4'));R=pd.DataFrame(holm(axes,'question_axes_Holm20'));SRC=pd.DataFrame(source)
P.to_csv(D/'publication_behavior_tests.csv',index=False);Q.to_csv(D/'publication_conditional_tests.csv',index=False);R.to_csv(D/'publication_axis_tests.csv',index=False);SRC.to_csv(D/'publication_item_deltas.csv',index=False)
# Reuse frozen token metadata; restrict to six main conditions.
meta=json.loads((O/'prompt_token_metadata.json').read_text());meta=[x for x in meta if x['condition'] in C];assert len(meta)==6
(O/'prompt_token_metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
# Retain former figure versions outside the active publication.
plt.rcParams.update({'font.family':'Arial','font.size':7,'axes.titlesize':7,'axes.labelsize':7,'xtick.labelsize':6,'ytick.labelsize':6,'legend.fontsize':6,'axes.linewidth':.6,'xtick.major.width':.6,'ytick.major.width':.6,'xtick.major.size':2.5,'ytick.major.size':2.5,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42,'ps.fonttype':42,'savefig.facecolor':'white'})
BLUE='#0072B2';ORANGE='#D55E00';GRAY='#8A8A8A';mm=1/25.4
figures=[]
def panel(ax,label):ax.text(-.16,1.07,label,transform=ax.transAxes,fontweight='bold',fontsize=8,va='bottom')
def stars(p):return '***' if p<.001 else '**' if p<.01 else '*' if p<.05 else 'ns'
def ptext(p):return 'P_adj < 0.001' if p<.001 else f'P_adj = {p:.3f}'
def save(fig,name):
 for ext in ['png','pdf','svg']:fig.savefig(F/f'{name}.{ext}',dpi=600,bbox_inches='tight',pad_inches=.04)
 plt.close(fig);figures.append(name)
# Figure 1: empirical atlas and paired reference-centered summaries.
fig=plt.figure(figsize=(180*mm,157*mm));gs=fig.add_gridspec(4,3,width_ratios=[1,1,1.7],wspace=.62,hspace=.64,left=.07,right=.96,top=.96,bottom=.14);limit=.02
for k,axis in enumerate(AX):
 ax=fig.add_subplot(gs[k//2,k%2]);q=wide(axis);delta=np.stack([(q.U1T0-q.U0T0),(q.U1T1-q.U0T1),(q.C1T0-q.U0T0),(q.C1T1-q.U0T1)],axis=1)
 im=ax.imshow(delta,cmap='RdBu_r',vmin=-limit,vmax=limit,aspect='auto',interpolation='none');ax.set(xticks=range(4),xticklabels=['UN0','UN1','CN0','CN1'],yticks=[0,69,138],yticklabels=['1','70','139'],title=axis);ax.tick_params(length=2)
 if k%2==0:ax.set_ylabel('Item')
 if k==0:panel(ax,'a')
ax=fig.add_subplot(gs[:,2]);ys=np.arange(8)
for offset,label,color in [(-.18,'UN',BLUE),(.18,'CN',ORANGE)]:
 rows=R[(R.contrast==label)&R.metric.isin(AX)].set_index('metric').loc[AX];v=rows.estimate.to_numpy();ax.barh(ys+offset,v,height=.31,color=color,label=label,zorder=2);ax.errorbar(v,ys+offset,xerr=np.array([rows.estimate-rows.ci_low,rows.ci_high-rows.estimate]),fmt='none',ecolor='#222',lw=.65,capsize=2,zorder=3)
 for j,row in enumerate(rows.itertuples()):ax.text(row.ci_high+.00022 if row.estimate>=0 else row.ci_low-.00022,j+offset,stars(row.p_adjusted),ha='left' if row.estimate>=0 else 'right',va='center',fontsize=6)
ax.axvline(0,color='#333',lw=.6);ax.set(yticks=ys,yticklabels=AX,xlim=(-.0068,.0092),xlabel='Mean change in cosine similarity',title='Paired change from Reference');ax.invert_yaxis();fig.legend(handles=[Patch(facecolor=BLUE,label='UN'),Patch(facecolor=ORANGE,label='CN')],frameon=False,loc='lower right',bbox_to_anchor=(.96,.005),ncol=2);panel(ax,'b')
cax=fig.add_axes([.085,.055,.38,.018]);fig.colorbar(im,cax=cax,orientation='horizontal',extend='both',label='Within-item change from matched Reference')
fig.text(.68,.055,'Bars: mean ± 95% cluster CI\nHolm correction across 20 axis tests',ha='center',va='center',fontsize=6)
save(fig,'Fig1_L14_emotion_atlas')
# Figure 2: actual prompt token traces and fixed-prompt endpoint changes.
fig=plt.figure(figsize=(180*mm,162*mm));gs=fig.add_gridspec(3,3,width_ratios=[1,1,1.55],wspace=.65,hspace=.55,left=.08,right=.96,top=.96,bottom=.17)
for k,c in enumerate(C):
 ax=fig.add_subplot(gs[k//2,k%2]);z=T[(T.condition==c)&T.axis.isin(AX)].pivot(index='axis',columns='token_index',values='cosine').reindex(AX);im=ax.imshow(z,cmap='RdBu_r',vmin=-.25,vmax=.25,aspect='auto',interpolation='none');ax.set(yticks=range(8),yticklabels=AX if k%2==0 else [],title=['Reference / clause 0','Reference / clause 1','UN / clause 0','UN / clause 1','CN / clause 0','CN / clause 1'][k],xlabel='Input token position');ax.tick_params(labelsize=5.5)
 if k==0:panel(ax,'a')
ax=fig.add_subplot(gs[:,2]);ss=S.pivot(index='axis',columns='condition',values='cosine');endpoint=[]
for offset,label,hi,color in [(-.18,'UN',['U1T0','U1T1'],BLUE),(.18,'CN',['C1T0','C1T1'],ORANGE)]:
 v=(ss[hi].mean(axis=1)-ss[['U0T0','U0T1']].mean(axis=1)).reindex(AX);ax.barh(np.arange(8)+offset,v,height=.31,color=color,label=label);endpoint.extend(dict(axis=a,contrast=label,delta=float(d)) for a,d in v.items())
ax.axvline(0,color='#333',lw=.6);ax.set(yticks=range(8),yticklabels=AX,xlabel='Change from matched Reference',title='Assistant-start state');ax.invert_yaxis();fig.legend(handles=[Patch(facecolor=BLUE,label='UN'),Patch(facecolor=ORANGE,label='CN')],frameon=False,loc='lower right',bbox_to_anchor=(.96,.005),ncol=2);panel(ax,'b')
cax=fig.add_axes([.085,.065,.38,.018]);fig.colorbar(im,cax=cax,orientation='horizontal',extend='both',label='Token-level cosine similarity')
fig.text(.70,.07,'Fixed system-only prompts\nDescriptive; no token-level P values',ha='center',va='center',fontsize=6)
save(fig,'Fig2_prompt_emotion_states');pd.DataFrame(endpoint).to_csv(D/'publication_system_endpoint_deltas.csv',index=False)
# Figure 3: six-condition means, pooled reference effects and conditional effects.
fig,axs=plt.subplots(1,3,figsize=(180*mm,83*mm),gridspec_kw={'width_ratios':[1.24,.85,1.13]});fig.subplots_adjust(left=.07,right=.98,bottom=.28,top=.89,wspace=.65)
ax=axs[0];means=t.mean(axis=0)*100;ci=np.quantile(w@t.to_numpy()*100,[.025,.975],axis=0);ax.bar(range(6),means,color=[GRAY,GRAY,BLUE,BLUE,ORANGE,ORANGE],width=.68,alpha=.9)
# Each dot is one cluster mean; bar mean remains item-weighted.
clustermeans=t.assign(cluster=I.cluster.to_numpy()).groupby('cluster').mean();jitter=np.random.default_rng(76).uniform(-.20,.20,size=(91,6))
for j,c in enumerate(C):ax.scatter(j+jitter[:,j],clustermeans[c]*100,s=1.6,color='#222',alpha=.20,rasterized=True,zorder=2)
ax.errorbar(range(6),means,yerr=np.vstack([means-ci[0],ci[1]-means]),fmt='none',ecolor='#111',lw=.75,capsize=2,zorder=4);ax.set(xticks=range(6),xticklabels=['R0','R1','UN0','UN1','CN0','CN1'],ylim=(0,105),ylabel='P(Unknown) (%)',title='Six-condition behavior');panel(ax,'a')
ax=axs[1];v=P.set_index('contrast').loc[['UN','CN']];vals=v.estimate.to_numpy()*100;ax.bar([0,1],vals,color=[BLUE,ORANGE],width=.58);ax.errorbar([0,1],vals,yerr=np.array([v.estimate-v.ci_low,v.ci_high-v.estimate])*100,fmt='none',ecolor='#111',capsize=3,lw=.8);ax.axhline(0,color='#333',lw=.6)
for j,r in enumerate(v.itertuples()):ax.text(j,r.ci_high*100+1.8,f'{r.estimate*100:+.2f}\n{stars(r.p_adjusted)}',ha='center',fontsize=6)
ax.set(xticks=[0,1],xticklabels=['UN − R','CN − R'],ylim=(-9,29),ylabel='Change in P(Unknown) (pp)',title='Matched Reference contrasts');panel(ax,'b')
ax=axs[2]
for offset,cond,light in [(-.18,'Preservation clause',False),(.18,'Deletion clause',True)]:
 rows=Q[Q.outcome==cond].set_index('contrast').loc[['UN','CN']];v=rows.estimate.to_numpy()*100;cols=[BLUE,ORANGE];ax.bar(np.arange(2)+offset,v,width=.31,color=cols,alpha=.45 if light else 1);ax.errorbar(np.arange(2)+offset,v,yerr=np.array([rows.estimate-rows.ci_low,rows.ci_high-rows.estimate])*100,fmt='none',ecolor='#222',lw=.7,capsize=2)
 for j,r in enumerate(rows.itertuples()):ax.text(j+offset,r.ci_high*100+1.2,stars(r.p_adjusted),ha='center',fontsize=6)
ax.axhline(0,color='#333',lw=.6);ax.set(xticks=[0,1],xticklabels=['UN − R','CN − R'],ylim=(-10,29),ylabel='Change in P(Unknown) (pp)',title='By notice ending');ax.legend(handles=[Patch(facecolor='#555',label='Preservation clause'),Patch(facecolor='#BBB',label='Deletion clause')],frameon=False,loc='lower right');panel(ax,'c')
fig.text(.07,.055,'R: Reference; 0: preserve if selected; 1: delete if not selected. n = 139 items in 91 template clusters.\nError bars: 95% cluster-bootstrap CI; two-sided null-centered bootstrap, 10,000 draws.\nHolm: b, 2 contrasts; c, 4 contrasts. * P_adj < 0.05; ** < 0.01; *** < 0.001.',fontsize=6)
save(fig,'Fig3_Unknown_reference_contrasts')
# Explicit text mapping for prompt highlighting: semantic spans are metadata, not extra observations.
charrecords=[]
for row in meta:
 c=row['condition'];text=row['rendered'];start,end=row['system_content_span'];chart={}
 for axis in AX+EVAL:
  vv=np.zeros(len(text));nn=np.zeros(len(text))
  for r in T[(T.condition==c)&(T.axis==axis)].itertuples():
   if r.char_end>r.char_start:vv[r.char_start:r.char_end]+=r.cosine;nn[r.char_start:r.char_end]+=1
  chart[axis]=np.divide(vv,nn,out=np.zeros_like(vv),where=nn>0)[start:end].tolist()
 charrecords.append(dict(condition=c,text=text[start:end],scores=chart))
(O/'prompt_character_scores.json').write_text(json.dumps(charrecords,ensure_ascii=False,separators=(',',':')))
(O/'figure_catalog.json').write_text(json.dumps(dict(main_figures=figures,dpi=600,width_mm=180,font='Arial, 5.5–8 pt',vector_text_editable=True,reference_centered=True,source='data/*6_conditions.csv',system_only_p_values=False,axes_are_cosine_not_emotion_probability=True),indent=2))
print(P.to_string(index=False));print(Q.to_string(index=False));print('DONE',figures)
