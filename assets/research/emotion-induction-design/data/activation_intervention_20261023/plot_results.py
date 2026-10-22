"""Save final analytical figures only, never plt.show()."""
from pathlib import Path
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
ROOT=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'AppleGothic','font.size':10,'axes.unicode_minus':False,'svg.fonttype':'none','pdf.fonttype':42})

def style(ax):
 ax.axvline(0,c='#777',lw=.8);ax.grid(axis='x',c='#eee');ax.set_axisbelow(True);ax.spines[['top','right','left']].set_visible(False);ax.tick_params(length=0,pad=7)

def save(fig,name):
 for ext in ['png','svg','pdf']:fig.savefig(ROOT/f'{name}.{ext}',dpi=180,facecolor='white')
 plt.close(fig)

def main():
 a=pd.read_csv(ROOT/'observational_conditional_bias.csv');b=pd.read_csv(ROOT/'person_mass_weighted_sensitivity.csv')
 fig,axes=plt.subplots(2,2,figsize=(13,9),sharex=True,sharey=True);fig.subplots_adjust(top=.79,bottom=.13,left=.09,right=.98,hspace=.28,wspace=.16)
 fig.text(.04,.96,'사람 선택에 한정한 고정관념 비율: 추정 방식 민감도',size=19,weight='bold');fig.text(.04,.915,'기존 v5 전체 자료 · R 대비 %p · 선: 보정 전 95% 템플릿 군집 부트스트랩 구간',size=11)
 fig.legend(handles=[Line2D([],[],c='#0072B2',marker='o',label='문항·순서별 비율을 동일 가중 평균'),Line2D([],[],c='#D55E00',marker='s',label='사람 선택 확률로 가중한 비율')],loc='upper left',bbox_to_anchor=(.035,.875),ncol=2,frameon=False)
 for i,t in enumerate(['amb','dis']):
  for j,s in enumerate(['set01','set02']):
   ax=axes[i,j];style(ax);ax.set_title(f'{s} · '+('모호 문항' if t=='amb' else '명확 문항'))
   for k,(data,color,marker) in enumerate([(a[a.metric=='p_person_bias'],'#0072B2','o'),(b,'#D55E00','s')]):
    for y,c in enumerate(['R','UN0','UN1','CN0','CN1']):
     if c=='R':v=l=h=0
     else:
      row=data[(data['set']==s)&(data.case_type==t)&(data.contrast==c+'-R')].iloc[0];v,l,h=row[['estimate','lo','hi']].to_numpy()*100
     ax.errorbar(v,y+(-.13 if k==0 else .13),xerr=[[max(0,v-l)],[max(0,h-v)]],fmt=marker,c=color,capsize=2)
   ax.set_yticks(range(5),['R','UN0','UN1','CN0','CN1']);ax.set_ylim(4.6,-.6);ax.set_xlim(-5,5)
   if i==1:ax.set_xlabel('R 대비 변화 (%p)')
 fig.text(.04,.035,'두 추정량은 서로 다른 질문에 답한다. 전체 사람 선택을 조건으로 한 확률질량 가중 추정에서는 모든 구간이 0을 포함한다.',size=10,color='#555')
 save(fig,'conditional_bias_sensitivity')
 d=pd.read_csv(ROOT/'intervention_contrasts.csv');d=d[d.primary==True]
 fig,axes=plt.subplots(2,2,figsize=(13,9),sharex=True);fig.subplots_adjust(top=.80,bottom=.14,left=.18,right=.97,hspace=.3,wspace=.24)
 fig.text(.04,.96,'Fear·Anxiety 방향 직접 개입: 행동 효과',size=19,weight='bold');fig.text(.04,.915,'24문항 · 유형당 12개 독립 템플릿 · 3선택지 순서 평균 · 동일 공지의 sham 대비 %p',size=11)
 fig.text(.04,.87,'R에서 + 주입 / CN1에서 - 방향 감산  |  선: 보정 전 95% 구간  |  별표: 16개 주 검정 Holm p < .05',size=10)
 labels=[('R','Fear+'),('R','Anxiety+'),('CN1','Fear-'),('CN1','Anxiety-')]
 extent=0
 for i,t in enumerate(['amb','dis']):
  for j,(metric,title) in enumerate([('p_unknown','P(알 수 없음)'),('p_person_bias','사람 선택 내 고정관념 비율')]):
   ax=axes[i,j];style(ax);ax.set_title(('모호' if t=='amb' else '명확')+' · '+title)
   for y,(c,arm) in enumerate(labels):
    row=d[(d.case_type==t)&(d.condition==c)&(d.arm==arm)&(d.metric==metric)].iloc[0];v,l,h=row[['estimate','lo','hi']].to_numpy()*100;extent=max(extent,abs(l),abs(h))
    color='#0072B2' if arm.startswith('Fear') else '#D55E00';ax.errorbar(v,y,xerr=[[max(0,v-l)],[max(0,h-v)]],fmt='o',c=color,capsize=3)
    if row.p_holm_primary<.05:ax.annotate('*',(v,y),xytext=(0,-13),textcoords='offset points',ha='center')
   ax.set_yticks(range(4),[f'{c} · {arm}' for c,arm in labels]);ax.set_ylim(3.5,-.5)
   if i==1:ax.set_xlabel('동일 공지 sham 대비 변화 (%p)')
 for ax in axes.flat:ax.set_xlim(-max(.1,extent*1.2),max(.1,extent*1.2))
 fig.text(.04,.035,'유의한 모호 문항 효과는 0.000003~0.000046%p에 그쳤다. 1,296쌍 모두 최고 확률 답은 동일했다. 정서 경험·자연 매개효과의 입증이 아니다.',size=10,color='#555')
 save(fig,'intervention_behavior')

if __name__=='__main__':main()
