"""Verified results only; no new inference. R0 and matched contrasts never share a label."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
B=Path('/Users/deep1003/Documents/Codex/2026-09-07/ai');O=Path(__file__).resolve().parent;D=B/'outputs/manuscript_results_20261024';r=pd.read_csv(D/'pooled_prompt_contrasts.csv')
plt.rcParams.update({'font.family':['AppleGothic','DejaVu Sans'],'font.size':11,'axes.unicode_minus':False,'svg.fonttype':'none','pdf.fonttype':42})
colors={'amb':'#0072B2','dis':'#D55E00'};markers={'amb':'o','dis':'s'}
def point(ax,row,y,scale=100):
 assert row.p_holm<.05
 v=row.estimate*scale;ax.errorbar(v,y,xerr=[[v-row.lo*scale],[row.hi*scale-v]],fmt=markers[row.case_type],color=colors[row.case_type],capsize=3,ms=7,lw=1.8,label='모호' if row.case_type=='amb' else '명확')
def clean(ax):
 ax.axvline(0,color='#78828c',lw=1);ax.grid(axis='x',alpha=.15);ax.spines[['top','right','left']].set_visible(False);ax.tick_params(axis='y',length=0,pad=9)
fig,axs=plt.subplots(1,2,figsize=(11,7));fig.subplots_adjust(left=.11,right=.97,bottom=.27,top=.66,wspace=.32)
fig.text(.055,.94,'기준에 따라 달라지는 정서 관련 활성',fontsize=22,weight='bold');fig.text(.055,.875,'CN1의 Fear·Desperation: 중립 R보다는 낮고, 확정 보존 CN0보다는 높다',fontsize=12)
fig.text(.055,.82,'L14 · 답변 직전 t₂ · 1,076개 고유 문항 · 정렬도 차이 ×1,000',fontsize=11)
for ax,(block,con,title) in zip(axs,[('R0','CN1-R','R 대비 변화\n확정 삭제 − 중립'),('matched','CN1-CN0','조건 간 차이\n확정 삭제 − 확정 보존')]):
 for k,axis in enumerate(['Fear','Anxiety','Desperation','Sadness']):
  for typ,off in [('amb',.15),('dis',-.15)]:
   row=r[(r.block==block)&(r.contrast==con)&(r.metric=='t2_'+axis)&(r.case_type==typ)].iloc[0];point(ax,row,3-k+off,1000)
 ax.set_yticks(range(3,-1,-1),['Fear','Anxiety','Desperation','Sadness']);ax.set_ylim(-.6,3.6);ax.set_xlim(-5,9);ax.set_xticks([-4,0,4,8]);ax.set_title(title,fontsize=14,pad=16);ax.set_xlabel('정렬도 차이 ×1,000',labelpad=12);clean(ax)
handles,labels=axs[0].get_legend_handles_labels();by=dict(zip(labels,handles));fig.legend(by.values(),by.keys(),loc='lower center',bbox_to_anchor=(.5,.12),ncol=2,frameon=False)
fig.text(.055,.075,'모든 점: 각 블록88개 Holm 보정 후 유의(p≤.0088). 선: 보정 전95% 군집 부트스트랩 구간.',fontsize=10,color='#444');fig.text(.055,.035,'축 간 크기는 감정 강도의 공통 척도가 아니다. 공지 묶음의 표상 효과이며, 감정 경험의 측정이 아니다.',fontsize=10,color='#555')
for ext in ['png','svg','pdf']:fig.savefig(O/f'activation_reference_vs_contrast.{ext}',dpi=180,facecolor='white')
plt.close(fig)
fig,axs=plt.subplots(2,2,figsize=(11,9),gridspec_kw={'height_ratios':[1.45,1]});fig.subplots_adjust(left=.17,right=.97,bottom=.21,top=.78,wspace=.38,hspace=.73)
fig.text(.055,.95,'사회적 판단: R 대비 변화와 조건 간 차이',fontsize=21,weight='bold');fig.text(.055,.895,'‘알 수 없음’의 증가는 모호 문항에서는 정답 증가, 명확 문항에서는 정답 감소와 연결됐다',fontsize=11)
fig.text(.055,.845,'선택 확률 변화(%p) · 모든 점은 해당40개 가족 Holm 보정 후 유의 · 선은 보정 전95% 구간',fontsize=10.5)
for col,metric in enumerate(['p_unknown','p_correct']):
 ax=axs[0,col];spec=[('amb','UN0-R'),('amb','UN1-R'),('dis','UN0-R'),('dis','UN1-R')]
 for y,(typ,con) in zip(range(3,-1,-1),spec):point(ax,r[(r.block=='R0')&(r.contrast==con)&(r.case_type==typ)&(r.metric==metric)].iloc[0],y)
 ax.set_yticks(range(3,-1,-1),[('모호' if t=='amb' else '명확')+' · '+c.replace('-','−') for t,c in spec]);ax.set_title('R 대비 | '+('알 수 없음' if metric=='p_unknown' else '정답 확률'),fontsize=13,pad=13);ax.set_ylim(-.6,3.6);ax.set_xlim(-6,6);ax.set_xlabel('ΔR (%p)',labelpad=9);clean(ax)
 ax=axs[1,col]
 for y,typ in [(1,'amb'),(0,'dis')]:point(ax,r[(r.block=='matched')&(r.contrast=='CN1-CN0')&(r.case_type==typ)&(r.metric==metric)].iloc[0],y)
 ax.set_yticks([1,0],['모호 · CN1−CN0','명확 · CN1−CN0']);ax.set_title('조건 간 | '+('알 수 없음' if metric=='p_unknown' else '정답 확률'),fontsize=13,pad=13);ax.set_ylim(-.6,1.6);ax.set_xlim(-6,6);ax.set_xlabel('확정 삭제 − 확정 보존 (%p)',labelpad=9);clean(ax)
fig.text(.055,.11,'위쪽: 불확실성 공지의 중립 R 대비 변화. 아래쪽: 확정 조건에서 삭제 공지와 보존 공지의 차이.',fontsize=10.5);fig.text(.055,.065,'명확 문항에서는 고정관념 방향 답이 정답일 수도 있다. ‘알 수 없음’·고정관념 선호·정확성을 구분한다.',fontsize=10,color='#555');fig.text(.055,.03,'모호 문항의 P(정답)=P(알 수 없음)이므로 두 패널은 그 유형에서 독립적인 결과가 아니다.',fontsize=10,color='#555')
for ext in ['png','svg','pdf']:fig.savefig(O/f'judgment_reference_vs_contrast.{ext}',dpi=180,facecolor='white')
plt.close(fig)
