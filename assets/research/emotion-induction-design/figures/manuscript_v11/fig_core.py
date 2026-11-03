# Figure 1: emotion representation and judgment coupling
import json, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7.5,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':0.6,'xtick.major.width':0.6,'ytick.major.width':0.6})
INK='#1f2933'; MUTED='#5f6b7a'; GRID='#e3e7ec'; QWEN='#2b6cb0'; LLAMA='#c05621'
S='/tmp/claude-0/-home-claude/7fc580cb-60a4-5295-be7b-4ce446a2c023/scratchpad/figs/'
B=json.load(open('/home/claude/deep1003.github.io/assets/research/emotion-induction-design/figures/manuscript_v11/valence_bins_v11_qwen.json'))
fig=plt.figure(figsize=(7.0,4.9))
gs=fig.add_gridspec(2,2,height_ratios=[1,1.05],hspace=0.62,wspace=0.32)
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
# panels c,d: caution-aligned estimates across models, benchmarks and contrasts
rows=[('Qwen2.5-7B-Instruct','KoBBQ','CLOSED',(0.28,0.19,0.37),(0.26,0.17,0.35),(0.13,0.01,0.27)),
      ('Qwen2.5-7B-Instruct','KoBBQ','OPEN',(0.08,-0.01,0.19),(0.25,0.17,0.33),(0.10,-0.01,0.23)),
      ('Qwen2.5-7B-Instruct','DiscrimEval','CLOSED',(-0.54,-0.69,-0.35),(-0.54,-0.70,-0.35),(-0.36,-0.51,-0.12)),
      ('Qwen2.5-7B-Instruct','DiscrimEval','OPEN',(-0.56,-0.70,-0.39),(-0.54,-0.68,-0.36),(-0.30,-0.44,0.02)),
      ('Llama-3.1-8B-Instruct*','KoBBQ','CLOSED',(0.43,0.34,0.52),(0.40,0.30,0.49),(-0.05,-0.14,0.02)),
      ('Llama-3.1-8B-Instruct*','KoBBQ','OPEN',(0.47,0.39,0.55),(0.48,0.40,0.56),(0.10,0.01,0.19))]
def align(t,bench):
    if bench=='DiscrimEval': return (-t[0],-t[2],-t[1])
    return t
labels=[f'{m}, {b}, {c}' for m,b,c,*_ in rows]
ys=list(range(len(rows)))[::-1]
for k,(lab,title,idx,xl) in enumerate([('c','Correlation with the change in judgment',(3,4),r'$\rho$ aligned to the cautious response'),
                                     ('d','Moderation by the baseline judgment',(5,),r'$\beta_3$ aligned to the cautious response')]):
    a=fig.add_subplot(gs[1,k])
    a.axvline(0,color=MUTED,lw=0.6,ls=(0,(2,2)))
    for y,r in zip(ys,rows):
        col=QWEN if r[0].startswith('Qwen') else LLAMA
        for j,i in enumerate(idx):
            est,lo,hi=align(r[i],r[1]); off=(0.17 if j==0 else -0.17) if len(idx)==2 else 0
            mk='o' if j==0 else 'D'
            fc=col if j==0 else 'white'
            a.plot([lo,hi],[y+off,y+off],color=col,lw=1.1,solid_capstyle='round')
            a.plot(est,y+off,marker=mk,ms=4.0 if mk=='o' else 3.4,mfc=fc,mec=col,mew=1.0,ls='none')
    a.set_yticks(ys); a.set_yticklabels(labels if k==0 else ['']*len(rows),fontsize=6.4,color=INK)
    a.set_xlabel(xl,color=INK); a.set_title(title,loc='left',fontsize=8,color=INK,pad=4)
    a.text(-0.06 if k==1 else -0.9,1.06,lab,transform=a.transAxes,fontsize=9,fontweight='bold',color=INK)
    a.grid(axis='x',color=GRID,lw=0.5); a.set_axisbelow(True)
    a.set_ylim(-0.7,len(rows)-0.3)
    if k==0:
        a.plot([],[],marker='o',color=MUTED,mfc=MUTED,ls='none',ms=4,label='correlation')
        a.plot([],[],marker='D',color=MUTED,mfc='white',ls='none',ms=3.4,label='baseline-controlled')
        a.legend(loc='upper right',fontsize=6.3,frameon=False,handletextpad=0.3,borderaxespad=0.1)
        a.set_xlim(-0.1,1.0); a.set_xticks([0,0.2,0.4,0.6])
    else:
        a.set_xlim(-0.3,0.6)
fig.savefig(S+'Fig_v11_core.pdf',bbox_inches='tight'); fig.savefig(S+'Fig_v11_core.png',dpi=200,bbox_inches='tight')
