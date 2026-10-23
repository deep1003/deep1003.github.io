"""Final saved figures only. No plotting during smoke validation."""
from pathlib import Path
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
ROOT=Path(__file__).resolve().parent

def main():
 assert (ROOT/'DONE').exists()
 d=pd.read_csv(ROOT/'primary_48.csv')
 plt.rcParams.update({'font.family':'AppleGothic','font.size':10,'axes.unicode_minus':False,'svg.fonttype':'none','pdf.fonttype':42})
 fig,axes=plt.subplots(4,2,figsize=(14,15),sharex='col');fig.subplots_adjust(top=.82,left=.12,right=.98,bottom=.075,hspace=.5,wspace=.22)
 fig.text(.04,.965,'불확실성 후속 실험: 세 방향의 동일 용량 직접 개입',fontsize=20,weight='bold')
 fig.text(.04,.932,'새 24문항 · L14 마지막 입력 토큰 · FP32 · 4공지 x 3순서 x 9개입 = 2,592회',fontsize=11)
 fig.text(.04,.903,'점: 동일 공지 sham 대비 평균 변화  |  선: 보정 전 95% 구간  |  별표: 48개 주 검정 Holm p < .05',fontsize=10)
 fig.legend(handles=[Line2D([],[],color='#0072B2',marker='o',label='확정 CN에 + 방향 주입'),Line2D([],[],color='#D55E00',marker='s',label='미정 UN에서 - 방향 감산')],loc='upper left',bbox_to_anchor=(.035,.885),ncol=2,frameon=False)
 for row,(typ,threat) in enumerate([(t,h) for t in ['amb','dis'] for h in ['0','1']]):
  for col,(metric,label) in enumerate([('p_unknown','P(알 수 없음)'),('p_person_bias','동일 가중 사람 선택 내 고정관념 비율')]):
   ax=axes[row,col];ax.axvline(0,color='#777',lw=.8);ax.grid(axis='x',color='#eee');ax.set_axisbelow(True);ax.spines[['top','right','left']].set_visible(False);ax.tick_params(length=0,pad=8)
   ax.set_title(('모호' if typ=='amb' else '명확')+' · '+('비위협' if threat=='0' else '위협')+' · '+label,fontsize=12,pad=13)
   for i,axis in enumerate(['Fear','Anxiety','Desperation']):
    for j,(prefix,sign,color,marker) in enumerate([('CN','+','#0072B2','o'),('UN','-','#D55E00','s')]):
     r=d[(d.case_type==typ)&(d.condition==prefix+threat)&(d.arm==axis+sign)&(d.metric==metric)].iloc[0]
     v,l,h=r[['estimate','lo','hi']].to_numpy()*100;y=i+(-.14 if j==0 else .14)
     ax.errorbar(v,y,xerr=[[max(0,v-l)],[max(0,h-v)]],fmt=marker,color=color,capsize=3)
     if r.p_holm_primary_48<.05:ax.annotate('*',(v,y),xytext=(0,-12),textcoords='offset points',ha='center',color=color)
   ax.set_yticks(range(3),['Fear','Anxiety','Desperation']);ax.set_ylim(2.5,-.5)
   subset=d[d.metric==metric];limit=max(.05,float(np.abs(subset[['lo','hi']].to_numpy()).max())*100*1.2);ax.set_xlim(-limit,limit)
   if row==3:ax.set_xlabel('동일 공지 sham 대비 변화 (%p)')
 fig.text(.04,.028,'Fear는 자연 UN-CN 축 변화가 음수이므로 반대 부호의 별도 보충 검정도 공개한다. 벡터 효과는 감정 경험이나 자연 매개효과의 증명이 아니다.',fontsize=10,color='#555')
 for ext in ['png','svg','pdf']:fig.savefig(ROOT/f'uncertainty_interventions.{ext}',dpi=180,facecolor='white')
 plt.close(fig)

if __name__=='__main__':main()
