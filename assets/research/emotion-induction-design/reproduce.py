"""Portable 139-item saved-data verification and rendering. No model inference."""
from pathlib import Path
import argparse,json,hashlib
import numpy as np,pandas as pd
BASE=Path(__file__).resolve().parent
D=BASE/'data'
C=['U0T0','U0T1','U1T0','U1T1','C1T0','C1T1']
AX=['Fear','Anxiety','Anger','Disgust','Calmness','Sadness','Desperation','Joy','Certainty','Uncertainty']
def verify():
    b=pd.read_csv(D/'behavior_6_conditions.csv')
    assert len(b)==2502 and b.item.nunique()==139
    assert set(b.condition)==set(C)
    assert not b.duplicated(['item','condition','rotation']).any()
    assert b.groupby(['item','condition']).size().eq(3).all()
    assert np.isfinite(b[['p_unknown','p_stereotype','p_anti']]).all().all()
    assert np.allclose(b[['p_unknown','p_stereotype','p_anti']].sum(axis=1),1,atol=1e-6)
    a=pd.read_csv(D/'axis_cosines_6_conditions.csv')
    assert len(a)==27522 and np.isfinite(a.cosine).all()
    assert pd.read_csv(D/'items_139.csv').cluster.nunique()==91
    manifest=BASE/'CHECKSUMS.json'
    if manifest.exists():
        for name,digest in json.loads(manifest.read_text()).items():
            assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==digest,name
    print('139 items, 91 clusters, six conditions, 2502 keys, 27522 cosines verified; no model inference.')
def render():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    F=BASE/'figures';F.mkdir(exist_ok=True)
    b=pd.read_csv(D/'behavior_6_conditions.csv');a=pd.read_csv(D/'axis_cosines_6_conditions.csv')
    M=pd.read_csv(D/'condition_means.csv');E=pd.read_csv(D/'paired_contrasts.csv')
    system=pd.read_csv(D/'system_only_assistant_alignment_6.csv');tokens=pd.read_csv(D/'system_token_alignment_6.csv')
    figures=[]
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False});figures=[]
    def save(fig,name):
     for ext in ['png','svg','pdf']:fig.savefig(F/f'{name}.{ext}',dpi=600,bbox_inches='tight',facecolor='white')
     plt.close(fig);figures.append(name)
    labels=['Reference\nPreserved','Reference\nDeleted','Uncertainty\nPreserved','Uncertainty\nDeleted','Certainty\nPreserved','Certainty\nDeleted'];colors=['#B6B6B6','#696969']*3
    fig,ax=plt.subplots(figsize=(9,4.3),layout='constrained');r=M[M.metric=='p_unknown'].set_index('term').loc[C];v=r.estimate.to_numpy()*100;ax.bar(range(6),v,color=colors);ax.errorbar(range(6),v,yerr=np.array([r.estimate-r.ci_low,r.ci_high-r.estimate])*100,fmt='none',ecolor='#222',capsize=4)
    for i,x in enumerate(v):ax.text(i,x+8,f'{x:.2f}%',ha='center')
    ax.set(xticks=range(6),xticklabels=labels,ylim=(0,82),ylabel='P(Unknown) (%)',title='Main study: 139 items, 91 template clusters, six conditions');fig.supxlabel('Three rotations averaged within item; pointwise 95% cluster-bootstrap intervals.',fontsize=9);save(fig,'M2_behavior')
    terms=['UN_vs_Reference','CN_vs_Reference','CN_vs_UN','Threat_Reference','Threat_Uncertainty','Threat_Certainty'];labs=['Uncertainty minus Reference','Certainty minus Reference','Certainty minus Uncertainty','Deletion effect: Reference','Deletion effect: Uncertainty','Deletion effect: Certainty'];r=E[E.metric=='p_unknown'].set_index('term').loc[terms];fig,ax=plt.subplots(figsize=(9,4.1),layout='constrained');v=r.estimate.to_numpy()*100;ax.errorbar(v,range(6),xerr=np.array([r.estimate-r.ci_low,r.ci_high-r.estimate])*100,fmt='o',capsize=4,color='#405A69');ax.axvline(0,ls=':',color='#999');ax.set(yticks=range(6),yticklabels=labs,xlabel='Paired change in P(Unknown) (percentage points)',title='Main study: paired behavior contrasts');ax.invert_yaxis();fig.supxlabel('Notice contrasts average preserved/deleted conditions. 10,000 template-cluster draws.',fontsize=9);save(fig,'S1_behavior_contrasts')
    r=E[E.metric.isin(AX)&E.term.isin(['UN_vs_Reference','CN_vs_Reference'])].pivot(index='metric',columns='term',values='estimate').reindex(index=AX,columns=['UN_vs_Reference','CN_vs_Reference']);fig,ax=plt.subplots(figsize=(7,5.2),layout='constrained');im=ax.imshow(r,cmap='RdBu_r',vmin=-.008,vmax=.008,aspect='auto');ax.set(yticks=range(10),yticklabels=AX,xticks=[0,1],xticklabels=['Uncertainty − Reference','Certainty − Reference'],title='Question-following L14: mean changes')
    for i in range(10):
     for j in range(2):ax.text(j,i,f'{r.iloc[i,j]:+.4f}',ha='center',va='center',color='white' if abs(r.iloc[i,j])>.005 else '#222')
    fig.colorbar(im,ax=ax,label='Change in cosine similarity');fig.supxlabel('Axis-specific centers differ. Values do not rank emotion intensity.',fontsize=9);save(fig,'S2_axis_mean_changes')
    # True item-by-condition map, never substituted with prompt embeddings.
    ids=list(pd.read_csv(D/'items_139.csv').sample_id);fig,axs=plt.subplots(2,5,figsize=(13,7),layout='constrained')
    for ax,axis in zip(axs.flat,AX):
     t=a[a.axis==axis].groupby(['item','condition']).cosine.mean().unstack().reindex(index=ids,columns=C);delta=t.subtract(t.U0T0,axis=0);im=ax.imshow(delta.to_numpy(),cmap='RdBu_r',vmin=-.025,vmax=.025,aspect='auto',interpolation='none');ax.set(title=axis,xticks=range(6),xticklabels=['R0','R1','U0','U1','C0','C1'],yticks=[0,69,138],yticklabels=['1','70','139']);ax.tick_params(labelsize=7)
    fig.colorbar(im,ax=axs,shrink=.65,label='Within-item change in cosine similarity');fig.suptitle('M3: within-item emotion-axis cosine changes at L14',fontsize=14);fig.supxlabel('139 item rows; three rotations averaged. Reference-preserved subtracted within item. R/U/C = notice; 0/1 = preserved/deleted.',fontsize=8);save(fig,'M3_item_axis_map')
    fig,axs=plt.subplots(3,2,figsize=(12,8),layout='constrained')
    for ax,c in zip(axs.flat,C):
     t=tokens[(tokens.condition==c)&tokens.axis.isin(AX)].pivot(index='axis',columns='token_index',values='cosine').reindex(AX);im=ax.imshow(t,cmap='RdBu_r',vmin=-.3,vmax=.3,aspect='auto',interpolation='none');ax.set(title=c,yticks=range(10),yticklabels=AX,xlabel='System-only input token position');ax.tick_params(labelsize=6)
    fig.colorbar(im,ax=axs,shrink=.6,label='Cosine similarity');fig.suptitle('M4: actual system-only token states at L14',fontsize=14);fig.supxlabel('Prompt text and token IDs are provided in the prompt appendix and token CSV. No Ko-BBQ item is included in these traces.',fontsize=8);save(fig,'M4_system_token_map')
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render',action='store_true')
    args=parser.parse_args()
    verify()
    if args.render:render()
