import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt, os, json
S='/home/claude/deep1003.github.io/assets/research/emotion-induction-design'
A=S+'/archive/v7'; F=A+'/figures'; os.makedirs(F,exist_ok=True); T=A+'/tables'; os.makedirs(T,exist_ok=True)
C1,C2,C3,C4='#2a78d6','#eb6834','#1baf7a','#eda100'
INK='#333333'; GRID='#e1e0d9'; BASE='#c3c2b7'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.edgecolor':BASE,'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.color':GRID,'grid.linewidth':0.6,'axes.axisbelow':True,'figure.dpi':150})
def save(fig,name):
    fig.savefig(f'{F}/{name}.png',dpi=200,bbox_inches='tight',facecolor='white'); fig.savefig(f'{F}/{name}.pdf',bbox_inches='tight'); plt.close(fig)
CONDS=['R','SURV_RECORD','SURV_THREAT','SURV_RECORD_V','SURV_THREAT_V']
LAB=['REF','RECORD','THREAT','RECORD (tagged)','THREAT (tagged)']
# Fig1 stacked behavior Llama & Qwen
fig,axs=plt.subplots(1,2,figsize=(9,3.6),sharey=True)
rows=[]
for ax,(name,f) in zip(axs,[('Llama-3.1-8B-Instruct',A+'/data/llama31_kobbq/pilot4_survival_cue_llama.csv'),('Qwen2.5-7B-Instruct',S+'/data/v7_qwen_20261029/pilot4_survival_cue_qwen.csv')]):
    d=pd.read_csv(f); g=d.groupby('condition')[['p_unknown','p_stereo','p_anti','choice_mass']].mean().loc[CONDS]*100
    x=np.arange(5); b=np.zeros(5)
    for col,c,l in [('p_unknown','#b7b5aa','Unknown'),('p_stereo',C2,'Stereotyped'),('p_anti',C1,'Anti-stereotyped')]:
        ax.bar(x,g[col],bottom=b,color=c,width=0.62,edgecolor='white',linewidth=1.5,label=l); b+=g[col].values
    if name.startswith('Llama'):
        ax.plot(x,g['choice_mass'],'o',color=INK,ms=5,label='A/B/C mass (full vocab.)')
    ax.set_xticks(x); ax.set_xticklabels(LAB,rotation=30,ha='right'); ax.set_title(name,fontsize=10,color=INK); ax.set_ylim(0,105)
    for i,v in enumerate(g['p_unknown']): ax.text(i,v/2,f'{v:.1f}',ha='center',va='center',fontsize=7.5,color=INK)
    g.insert(0,'model',name); rows.append(g.round(2))
axs[0].set_ylabel('Mean probability over 108 items (%)')
h,l=axs[0].get_legend_handles_labels(); fig.legend(h,l,loc='upper center',ncol=4,frameon=False,bbox_to_anchor=(0.5,1.06))
save(fig,'fig1_kobbq_behavior_llama_qwen')
pd.concat(rows).to_csv(T+'/fig1_kobbq_behavior_llama_qwen.csv')
# Fig2 condition means 5 models
cd=pd.read_csv(S+'/data/v7_synthesis_5models_20261030/condition_descriptives.csv')
models=[('Llama31','Llama-3.1-8B-Instruct'),('Qwen','Qwen2.5-7B-Instruct'),('DeepSeek','DeepSeek-LLM-7B-Chat'),('Llama32','Llama-3.2-3B-Instruct'),('Gemma2','Gemma-2-2B-IT')]
fig,axs=plt.subplots(1,2,figsize=(9,3.2))
out=[]
for ax,(task,met,xl) in zip(axs,[('KoBBQ','p_unknown','KoBBQ P(unknown), conditional on A/B/C (%)'),('DiscrimEval','q_yes','DiscrimEval affirmative probability q_yes (%)')]):
    for j,(c,col,lab,mk) in enumerate([('R','#8a887f','REF','s'),('SURV_RECORD',C1,'RECORD','o'),('SURV_THREAT',C2,'THREAT','D')]):
        ys=[];xs=[]
        for i,(k,n) in enumerate(models):
            v=cd[(cd.task==task)&(cd.model==k)&(cd.condition==c)&(cd.metric==met)]['mean']
            if len(v): xs.append(v.iloc[0]*100); ys.append(i); out.append((task,n,c,met,round(v.iloc[0]*100,2)))
        ax.plot(xs,np.array(ys)+(j-1)*0.18,mk,color=col,ms=6,label=lab,markeredgecolor='white',markeredgewidth=0.8)
    ax.set_yticks(range(5)); ax.set_yticklabels([n for _,n in models]); ax.invert_yaxis(); ax.set_xlabel(xl); ax.grid(axis='y',visible=False)
axs[1].set_yticklabels([])
h,l=axs[0].get_legend_handles_labels(); fig.legend(h,l,loc='upper center',ncol=3,frameon=False,bbox_to_anchor=(0.5,1.04))
save(fig,'fig2_condition_means_5models')
pd.DataFrame(out,columns=['task','model','condition','metric','mean_pct']).to_csv(T+'/fig2_condition_means_5models.csv',index=False)
# Fig3 robustness
r=pd.read_csv(A+'/data/robustness/robust_analysis_qwen.csv')
sel=[('P1 (108, original)','THREAT-RECORD','P1 original, mid-bias 108'),('P2 (108)','THREAT-RECORD','P2 close paraphrase, 108'),('P3 (108)','THREAT-RECORD','P3 compressed paraphrase, 108'),('random 216','P1_THREAT-P1_RECORD','P1, random 216')]
fig,axs=plt.subplots(1,2,figsize=(9,2.6),sharey=True)
for ax,(met,tt) in zip(axs,[('p_unknown','P(unknown)'),('p_sgp','P(stereotyped | person)')]):
    for i,(s,c,l) in enumerate(sel):
        q=r[(r.set==s)&(r.contrast==c)&(r.metric==met)].iloc[0]
        ax.errorbar(q.est,i,xerr=[[q.est-q.lo],[q.hi-q.est]],fmt='o',color=C1,ecolor=C1,elinewidth=2,capsize=0,ms=6)
    ax.axvline(0,color=BASE,lw=1); ax.set_title('THREAT − RECORD, '+tt+' (pp)',fontsize=9.5,color=INK); ax.grid(axis='y',visible=False)
axs[0].set_yticks(range(4)); axs[0].set_yticklabels([l for *_,l in sel]); axs[0].invert_yaxis()
save(fig,'fig3_robustness_qwen')
# Fig4 decomposition shares 7B 8-axis
b=pd.read_csv(A+'/data/decomposition_qwen25_7b/behavioral_shares.csv'); b=b[b.metric=='p_unknown']
fig,ax=plt.subplots(figsize=(6.2,2.8))
comps=[('full','Full threat direction d'),('emo','Emotion component d_emo'),('res','Residual component d_res')]
for j,(dr,col,lab) in enumerate([('remove',C1,'Removal from THREAT'),('add',C2,'Addition to RECORD')]):
    for i,(c,_) in enumerate(comps):
        q=b[(b.direction==dr)&(b.component==c)].iloc[0]
        ax.errorbar(q.share_percent,i+(j-0.5)*0.25,xerr=[[q.share_percent-q.share_ci_lo],[q.share_ci_hi-q.share_percent]],fmt='o',color=col,elinewidth=2,ms=6,label=lab if i==0 else None)
ax.axvline(0,color=BASE,lw=1); ax.set_yticks(range(3)); ax.set_yticklabels([l for _,l in comps]); ax.invert_yaxis(); ax.grid(axis='y',visible=False)
ax.set_xlabel('Share of total THREAT − RECORD effect on P(unknown) (%)'); ax.legend(frameon=False,loc='lower center',bbox_to_anchor=(0.5,1.0),ncol=2,fontsize=8)
save(fig,'fig4_decomposition_shares_qwen7b')
# Fig5 7B vs 235B raw shifts
ce=pd.read_csv(A+'/data/qwen3_235b/followup/comparison_effects.csv')
order=['remove_full','remove_emo','remove_res','add_full','add_emo','add_res']
labs={'remove_full':'Remove d','remove_emo':'Remove d_emo','remove_res':'Remove d_res','add_full':'Add d','add_emo':'Add d_emo','add_res':'Add d_res'}
fig,ax=plt.subplots(figsize=(6.2,3.2))
for j,(p,col,lab) in enumerate([('7B',C1,'Qwen2.5-7B-Instruct'),('235B_batch1',C2,'Qwen3-235B-A22B-Instruct-2507 (batch 1)')]):
    for i,k in enumerate(order):
        q=ce[ce.config==k].iloc[0]; e=q[f'{p}_shift_pp']; pp='235B' if p!='7B' else '7B'; lo=q[f'{pp}_ci_low']; hi=q[f'{pp}_ci_high']
        hollow = (p!='7B' and k.endswith('_emo'))
        ax.errorbar(e,i+(j-0.5)*0.28,xerr=[[e-lo],[hi-e]],fmt='o',color=col,mfc='white' if hollow else col,elinewidth=2,ms=6,label=lab if i==0 else None)
ax.axvline(0,color=BASE,lw=1); ax.set_yticks(range(6)); ax.set_yticklabels([labs[k] for k in order]); ax.invert_yaxis(); ax.grid(axis='y',visible=False)
ax.set_xlabel('Raw shift in P(unknown) (pp)'); ax.legend(frameon=False,fontsize=8,loc='lower center',bbox_to_anchor=(0.5,1.0),ncol=1)
save(fig,'fig5_intervention_7b_vs_235b')
# Fig6 235B mass
te=pd.read_csv(A+'/data/qwen3_235b/total_effects.csv').set_index('metric')
fig,ax=plt.subplots(figsize=(5.6,2.8))
ms=[('p_unknown','P(unknown), within A/B/C'),('full_unknown','Unknown-letter mass, full vocabulary'),('mass','A/B/C mass, full vocabulary')]
for j,(c,col,lab) in enumerate([('record_mean',C1,'RECORD'),('threat_mean',C2,'THREAT')]):
    ax.barh(np.arange(3)+(j-0.5)*0.36,[te.loc[m,c]*100 for m,_ in ms],height=0.34,color=col,label=lab,edgecolor='white')
    for i,(m,_) in enumerate(ms): ax.text(te.loc[m,c]*100+1,i+(j-0.5)*0.36,f'{te.loc[m,c]*100:.1f}',va='center',fontsize=7.5,color=INK)
ax.set_yticks(range(3)); ax.set_yticklabels([l for _,l in ms]); ax.invert_yaxis(); ax.set_xlim(0,105); ax.set_xlabel('Mean over 108 ambiguous items (%)'); ax.grid(axis='y',visible=False)
ax.legend(frameon=False,fontsize=8,loc='lower right')
save(fig,'fig6_qwen235b_probability_mass')
# Fig7 preference H1
h=pd.read_csv(A+'/data/preference/main_H1_preference.csv')
emos=['joy','calm','neutral','fear','sadness','anxiety','anger','desperation','panic']
fig,ax=plt.subplots(figsize=(6.4,3.6))
for j,(c,col,lab) in enumerate([('R','#8a887f','REF'),('SURV_RECORD',C1,'RECORD'),('SURV_THREAT',C2,'THREAT')]):
    for i,e in enumerate(emos):
        q=h[(h.condition==c)&(h.emotion==e)].iloc[0]
        ax.errorbar(q.share_minus_50,i+(j-1)*0.22,xerr=[[q.share_minus_50-q.lo],[q.hi-q.share_minus_50]],fmt='o',color=col,elinewidth=1.8,ms=5,label=lab if i==0 else None)
ax.axvline(0,color=BASE,lw=1); ax.set_yticks(range(len(emos))); ax.set_yticklabels(emos); ax.invert_yaxis(); ax.grid(axis='y',visible=False)
ax.set_xlabel('Preference share for the emotion story minus 50 (pp)'); ax.legend(frameon=False,fontsize=8,loc='lower right')
save(fig,'fig7_preference_shares')
# Fig8 on-policy (values transcribed from analysis_v2.txt)
op=pd.DataFrame([('Decision-position negative emotion (x10^-3)','A',11.59,10.50,12.67),('Decision-position negative emotion (x10^-3)','C',-2.43,-4.89,-0.19),
 ('P(unknown) (pp)','A',13.35,4.62,23.38),('P(unknown) (pp)','C',-7.15,-20.15,5.32),
 ('P(stereotyped | person) (pp)','A',0.79,-7.03,9.36),('P(stereotyped | person) (pp)','C',-6.52,-16.94,4.37)],columns=['metric','format','est','lo','hi'])
op.to_csv(T+'/fig8_onpolicy_threat_minus_record.csv',index=False)
fig,axs=plt.subplots(1,3,figsize=(9,2.2),sharey=True)
for ax,m in zip(axs,op.metric.unique()):
    for i,(fm,col) in enumerate([('A',C1),('C',C2)]):
        q=op[(op.metric==m)&(op.format==fm)].iloc[0]
        ax.errorbar(q.est,i,xerr=[[q.est-q.lo],[q.hi-q.est]],fmt='o',color=col,elinewidth=2,ms=6)
    ax.axvline(0,color=BASE,lw=1); ax.set_title(m,fontsize=8.5,color=INK); ax.grid(axis='y',visible=False)
axs[0].set_yticks([0,1]); axs[0].set_yticklabels(['Format A (direct answer)','Format C (rationale first)']); axs[0].invert_yaxis()
save(fig,'fig8_onpolicy_formats')
print('done')
