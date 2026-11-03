# Figure: operator notices and termination change benchmark outcomes by small amounts
import matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7.5,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':0.6})
INK='#1f2933'; MUTED='#5f6b7a'; GRID='#e3e7ec'; ANCH='#9aa5b1'; KEEP='#7a8796'; TERM='#2b6cb0'
S='/tmp/claude-0/-home-claude/7fc580cb-60a4-5295-be7b-4ce446a2c023/scratchpad/figs/'
lev={'kobbq':{'NO-NOTICE':84.65,'REF':85.82,'OPEN':(88.99,88.13),'CLOSED':(88.55,87.31)},
     'de':{'NO-NOTICE':76.51,'REF':78.19,'OPEN':(79.38,77.74),'CLOSED':(78.14,74.91)}}
fig=plt.figure(figsize=(7.0,2.5))
gs=fig.add_gridspec(1,2,wspace=0.32)
for k,(key,lab,title,yl) in enumerate([('kobbq','a','KoBBQ, ambiguous items','P(Unknown), %'),('de','b','DiscrimEval','P(yes), % (approval)')]):
    a=fig.add_subplot(gs[0,k]); L=lev[key]
    a.plot([0,1],[L['NO-NOTICE'],L['REF']],color=ANCH,lw=0.9,zorder=1)
    a.plot([0],[L['NO-NOTICE']],'o',color=ANCH,ms=5,zorder=3); a.plot([1],[L['REF']],'o',color=ANCH,ms=5,zorder=3)
    for x,s in [(2.2,'OPEN'),(3.4,'CLOSED')]:
        kv,tv=L[s]
        a.annotate('',xy=(x+0.32,tv),xytext=(x,kv),arrowprops=dict(arrowstyle='-|>',color=TERM,lw=1.0,shrinkA=4,shrinkB=4,mutation_scale=7))
        a.plot([x],[kv],'o',mfc='white',mec=KEEP,mew=1.2,ms=5,zorder=3); a.plot([x+0.32],[tv],'o',color=TERM,ms=5,zorder=3)
        a.text(x+0.47,tv,f'{tv-kv:+.1f}'.replace('-','−'),fontsize=6.6,color=TERM,va='center')
    a.set_xticks([0,1,2.36,3.56]); a.set_xticklabels(['NO-\nNOTICE','REF','OPEN','CLOSED'],fontsize=6.8,color=INK)
    a.set_xlim(-0.4,4.5)
    if k==0:
        a.plot([],[],'o',mfc='white',mec=KEEP,mew=1.2,ms=5,ls='none',label='KEEP'); a.plot([],[],'o',color=TERM,ms=5,ls='none',label='TERM'); a.legend(loc='lower right',fontsize=6.5,frameon=False,handletextpad=0.2)
    a.set_ylabel(yl,color=INK); a.set_title(title,loc='left',fontsize=8,color=INK,pad=4)
    a.text(-0.2,1.06,lab,transform=a.transAxes,fontsize=9,fontweight='bold',color=INK)
    a.grid(axis='y',color=GRID,lw=0.5); a.set_axisbelow(True)
fig.savefig(S+'Fig_v11_notice.pdf',bbox_inches='tight'); fig.savefig(S+'Fig_v11_notice.png',dpi=200,bbox_inches='tight')
