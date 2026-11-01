"""Archive tables and figures for v3 sub-studies and v4 (recomputed from archived trial files; no model run).
Bootstrap: item means over option orders, 10,000 template-cluster draws, seed 20261022 (same as analyze_main_study.py)."""
import sys, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
S=sys.argv[1]; D=S+'/data/'; A=S+'/archive/'
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8,"axes.spines.top":False,"axes.spines.right":False})
def frame(tr,col='p_unknown',scale=100):
    im=tr.groupby(['item','cluster','condition'])[col].mean().unstack()*scale
    cl=im.index.get_level_values('cluster').to_numpy(); u=np.unique(cl); rng=np.random.default_rng(20261022)
    ix={c:np.where(cl==c)[0] for c in u}; dr=[np.concatenate([ix[c] for c in rng.choice(u,len(u))]) for _ in range(10000)]
    def boot(v):
        v=np.asarray(v,float); bs=np.array([v[d].mean() for d in dr]); lo,hi=np.percentile(bs,[2.5,97.5])
        return v.mean(),lo,hi,max(min(1,2*min((bs<=0).mean(),(bs>=0).mean())),1e-4)
    return im,boot
def save(fig,path):
    for e in ('png','svg','pdf'): fig.savefig(f'{path}.{e}',dpi=300,bbox_inches='tight')
    plt.close(fig)
# v3-D condition means
a=pd.read_csv(D+'main_trials.csv'); b=pd.read_csv(D+'diag_t0t1_trials.csv')
m=pd.concat([a[a.condition.isin(['R','UN0','UN1'])],b])
im,boot=frame(m)
order=['R','D0_none','UN0','D1_nonsel_keep','D4_you_keep','UN1','D2_sel_delete','D3_you_delete']
lab=['R','D0','UN0','D1','D4','UN1','D2','D3']
rows=[dict(condition=c,label=l,**dict(zip(['p_unknown','ci_lo','ci_hi','p'],boot(im[c])))) for c,l in zip(order,lab)]
t=pd.DataFrame(rows).drop(columns='p'); t.to_csv(A+'v3/tables/diag_condition_means_recomputed.csv',index=False)
fig,ax=plt.subplots(figsize=(4.2,2.6)); col=['#9e9e9e','#7b7b7b']+['#9ec5e8']*3+['#c62828']*3
for i,r in t.iterrows():
    ax.bar(i,r.p_unknown,0.65,color=col[i]); ax.errorbar(i,r.p_unknown,yerr=[[r.p_unknown-r.ci_lo],[r.ci_hi-r.p_unknown]],color='#212121',capsize=2,lw=0.8)
ax.set_xticks(range(len(t)),lab); ax.set_ylim(0,100); ax.set_ylabel('P(unknown), %'); ax.set_xlabel('Condition (blue, preservation ending; red, deletion ending)')
save(fig,A+'v3/figures/diag_condition_means')
# threat screen
t1=pd.read_csv(A+'v3/tables/threat_screen_t1_vs_neutral.csv'); bb=pd.read_csv(A+'v3/tables/threat_screen_bbq_family_vs_neutral.csv')
fams=['B','P','TCS','TR','TC','TN','TI','TD','PC']
fig,ax=plt.subplots(figsize=(4.2,2.6))
for i,f in enumerate(fams):
    v=t1[t1.family==f].Fear.to_numpy(); ax.scatter(np.full(len(v),i),v,s=8,color='#424242'); ax.plot([i-0.25,i+0.25],[v.mean()]*2,color='#c62828',lw=1.2)
ax.axhline(0,color='#9e9e9e',lw=0.6); ax.set_xticks(range(len(fams)),fams); ax.set_ylabel('Fear-axis change vs neutral notices (×10⁻³)'); ax.set_xlabel('Prompt family')
save(fig,A+'v3/figures/threat_screen_t1_fear')
fig,ax=plt.subplots(figsize=(4.2,2.6))
for i,f in enumerate(fams):
    r=bb[bb.family==f].iloc[0]; ax.errorbar(i,r.diff_pp,yerr=[[r.diff_pp-r.ci_lo],[r.ci_hi-r.diff_pp]],fmt='o',color='#212121',ms=3,capsize=2,lw=0.8)
ax.axhline(0,color='#9e9e9e',lw=0.6); ax.set_xticks(range(len(fams)),fams); ax.set_ylabel('ΔP(unknown) vs neutral notices, pp'); ax.set_xlabel('Prompt family')
save(fig,A+'v3/figures/threat_screen_bbq')
# v4 A/B
ab=pd.read_csv(A+'v4/threat_ab_t2.csv'); im,boot=frame(ab)
rows=[]; cons=[]
for f in 'AB':
    c={k:f'{f}_{k}' for k in ['R','UN0','UN1','CN0','CN1']}
    for k,v in c.items(): e,lo,hi,_=boot(im[v]); rows.append(dict(family=f,condition=k,p_unknown=e,ci_lo=lo,ci_hi=hi))
    U=im
    defs={'CN1 - CN0':U[c['CN1']]-U[c['CN0']],'UN1 - UN0':U[c['UN1']]-U[c['UN0']],
          'Interaction (CN1-CN0) - (UN1-UN0)':(U[c['CN1']]-U[c['CN0']])-(U[c['UN1']]-U[c['UN0']]),
          'UN - R':(U[c['UN0']]+U[c['UN1']])/2-U[c['R']],'CN - R':(U[c['CN0']]+U[c['CN1']])/2-U[c['R']],
          'CN1 - R':U[c['CN1']]-U[c['R']],'Deletion - keep (mean)':(U[c['UN1']]+U[c['CN1']])/2-(U[c['UN0']]+U[c['CN0']])/2}
    for k,v in defs.items(): e,lo,hi,p=boot(v); cons.append(dict(family=f,contrast=k,estimate_pp=e,ci_lo=lo,ci_hi=hi,p_boot=p))
means=pd.DataFrame(rows); means.to_csv(A+'v4/tables/ab_condition_means_recomputed.csv',index=False)
pd.DataFrame(cons).to_csv(A+'v4/tables/ab_contrasts_recomputed.csv',index=False)
# t2 axis deletion-keep
imF,bF=frame(ab,'t2_Fear',1000); r2=[]
for f in 'AB':
    for st in ['UN','CN']:
        e,lo,hi,p=bF(imF[f'{f}_{st}1']-imF[f'{f}_{st}0']); r2.append(dict(family=f,contrast=f'{st}1 - {st}0',fear_t2_x1000=e,ci_lo=lo,ci_hi=hi))
pd.DataFrame(r2).to_csv(A+'v4/tables/ab_t2_fear_recomputed.csv',index=False)
fig,ax=plt.subplots(figsize=(4.6,2.6)); cols={'R':'#9e9e9e','UN0':'#f4a3a3','UN1':'#c62828','CN0':'#9ec5e8','CN1':'#1f5fa8'}
x=0; ticks=[]; labs=[]
for f in 'AB':
    for k in ['R','UN0','UN1','CN0','CN1']:
        r=means[(means.family==f)&(means.condition==k)].iloc[0]
        ax.bar(x,r.p_unknown,0.7,color=cols[k]); ax.errorbar(x,r.p_unknown,yerr=[[r.p_unknown-r.ci_lo],[r.ci_hi-r.p_unknown]],color='#212121',capsize=2,lw=0.8)
        ticks.append(x); labs.append(k); x+=1
    x+=1
ax.set_xticks(ticks,labs); ax.set_ylim(0,100); ax.set_ylabel('P(unknown), %'); ax.text(2,95,'Family A',ha='center'); ax.text(8,95,'Family B (v4)',ha='center')
save(fig,A+'v4/figures/ab_condition_means')
print(t.round(1).to_string()); print(means.round(2).to_string()); print(pd.DataFrame(cons).round(2).to_string()); print(pd.DataFrame(r2).round(2))
