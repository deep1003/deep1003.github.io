# Figure 1: emotion representation and judgment coupling
import json, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7.5,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':0.6,'xtick.major.width':0.6,'ytick.major.width':0.6})
INK='#1f2933'; MUTED='#5f6b7a'; GRID='#e3e7ec'; QWEN='#2b6cb0'; LLAMA='#c05621'
S='/tmp/claude-0/-home-claude/7fc580cb-60a4-5295-be7b-4ce446a2c023/scratchpad/figs/'
B=json.load(open('/home/claude/deep1003.github.io/assets/research/emotion-induction-design/figures/manuscript_v11/valence_bins_v11_qwen.json'))
fig=plt.figure(figsize=(7.0,4.9))
gs=fig.add_gridspec(2,2,wspace=0.32,hspace=0.55)
# panels a,b: binned item-wise changes (Qwen, CLOSED)
spec=[('kobbq','a','KoBBQ, Unknown selection',r'$\Delta$ P(Unknown), pp',r'$\rho=0.28$ [0.19, 0.37]'),
      ('discrimeval','b','DiscrimEval, approval tendency',r'$\Delta$ approval tendency, log-odds',r'$\rho=-0.54$ [$-0.69$, $-0.35$]')]
for k,(task,lab,title,yl,ann) in enumerate(spec):
    a=fig.add_subplot(gs[0,k])
    x=[r[0] for r in B[task]]; y=[r[1] for r in B[task]]; e=[1.96*r[2] for r in B[task]]
    a.axhline(0,color=MUTED,lw=0.6,ls=(0,(2,2)),zorder=1)
    a.errorbar(x,y,yerr=e,fmt='o',color=QWEN,ms=4.2,mec='white',mew=0.8,elinewidth=1.0,capsize=0,zorder=3)
    a.set_xlabel(r'$\Delta$ valence index (TERM $-$ KEEP)',color=INK); a.set_ylabel(yl,color=INK)
    a.set_title(title,loc='left',fontsize=8,color=INK,pad=4)
    a.text(-0.17,1.06,lab,transform=a.transAxes,fontsize=9,fontweight='bold',color=INK)
    a.grid(color=GRID,lw=0.5); a.set_axisbelow(True)
    a.text(0.03,0.9 if task=='kobbq' else 0.05,ann,transform=a.transAxes,fontsize=7,color=INK)

SL=json.load(open(S+'simple_slopes_v11_qwen.json'))
for k,(key,lab,title,xl) in enumerate([('kobbq|CLOSED','c','KoBBQ, moderation by baseline Unknown','Baseline P(Unknown) under KEEP'),('discrimeval|CLOSED','d','DiscrimEval, moderation by baseline approval','Baseline approval tendency under KEEP')]):
    a=fig.add_subplot(gs[1,k]); r=SL[key]; x=[0,1,2]
    a.axhline(0,color=MUTED,lw=0.6,ls=(0,(2,2)),zorder=1)
    a.plot(x,r['slope'],color=QWEN,lw=1.0,zorder=2)
    for xi,e,lo,hi in zip(x,r['slope'],r['lo'],r['hi']):
        a.plot([xi,xi],[lo,hi],color=QWEN,lw=1.1,zorder=2); a.plot(xi,e,'o',color=QWEN,ms=4.6,mec='white',mew=0.8,zorder=3)
    a.set_xticks(x); a.set_xticklabels(['Low\n(\u22121 SD)','Mean','High\n(+1 SD)'],fontsize=6.8,color=INK)
    a.set_xlim(-0.4,2.4); a.set_xlabel(xl,color=INK)
    a.set_ylabel('Slope of baseline valence\n(SD of \u0394 judgment per SD)',color=INK,fontsize=7)
    a.set_title(title,loc='left',fontsize=8,color=INK,pad=4)
    a.text(-0.17,1.06,lab,transform=a.transAxes,fontsize=9,fontweight='bold',color=INK)
    a.grid(axis='y',color=GRID,lw=0.5); a.set_axisbelow(True)
fig.savefig(S+'Fig_v11_core.pdf',bbox_inches='tight'); fig.savefig(S+'Fig_v11_core.png',dpi=200,bbox_inches='tight')
