"""Render significant-only summaries; preserve nonsignificant cells as unestimated blanks."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
B=Path('/Users/deep1003/Documents/Codex/2026-09-07/ai');O=Path(__file__).resolve().parent;D=B/'outputs/multilayer_uncertainty_20261023'
plt.rcParams.update({'font.family':['AppleGothic','DejaVu Sans'],'axes.unicode_minus':False,'font.size':11,'svg.fonttype':'none','pdf.fonttype':42})
p=pd.read_csv(D/'primary_144.csv');s=p[p.p_holm_144<.05].copy();assert len(s)==6 and set(s.case_type)=={'amb'} and set(s.condition)=={'UN0'}
s.to_csv(O/'significant_primary.csv',index=False)
fig,axs=plt.subplots(1,2,figsize=(11,6));fig.subplots_adjust(left=.09,right=.96,bottom=.23,top=.71,wspace=.28)
fig.text(.06,.94,'유의한 개입 효과: 층 × 강도',fontsize=23,weight='bold')
fig.text(.06,.875,'모호16문항 · UN0(미정·비위협) · 각 축의 − 방향 개입 · 동일 공지 무개입 대비',fontsize=11)
fig.text(.06,.815,'숫자: 알 수 없음 확률 변화(%p)와95% 신뢰구간 · 유의성: 주144개 Holm p<.05',fontsize=11)
norm=TwoSlopeNorm(vmin=-.28,vcenter=0,vmax=.28)
for ax,axis in zip(axs,['Anxiety','Desperation']):
 z=s[s.axis==axis];mat=np.full((3,3),np.nan)
 for r in z.itertuples():mat[[7,14,21].index(r.layer),[.25,1,4].index(r.dose)]=r.estimate*100
 cmap=plt.get_cmap('RdBu_r').copy();cmap.set_bad('#eef0f3');ax.imshow(np.ma.masked_invalid(mat),cmap=cmap,norm=norm,aspect='auto')
 for i,l in enumerate([7,14,21]):
  for j,d in enumerate([.25,1,4]):
   r=z[(z.layer==l)&(z.dose==d)]
   if r.empty:ax.text(j,i,'비유의',ha='center',va='center',color='#818894',fontsize=10)
   else:
    r=r.iloc[0];ax.text(j,i,f'{r.estimate*100:+.3f}\n[{r.lo*100:+.3f},\n{r.hi*100:+.3f}]',ha='center',va='center',fontsize=11,color='white' if abs(r.estimate*100)>.18 else '#172331')
 ax.set_title(axis+' 감산',fontsize=16,pad=15);ax.set_yticks(range(3),['L7','L14','L21']);ax.set_xticks(range(3),['0.25배','1배','4배']);ax.tick_params(length=0,pad=9);ax.set_xlabel('층별 기준 L2 개입 용량의 배수',labelpad=10)
fig.text(.06,.12,'빨강: 증가   파랑: 감소   회색: 보정 후 비유의(효과0을 뜻하지 않음)',fontsize=11)
fig.text(.06,.065,'신뢰구간은 보정 전. 층 간 차이는 아래 직접 비교로 판단한다. 정서 특이성·정서 경험의 증거는 아니다.',fontsize=10,color='#555')
for ext in ['png','svg','pdf']:fig.savefig(O/f'significant_layer_dose.{ext}',dpi=180,facecolor='white')
plt.close(fig)
l=pd.read_csv(D/'direct_layer_96.csv');l=l[l.p_holm_layer_96<.05].copy();assert len(l)==9;l.to_csv(O/'significant_layer_contrasts.csv',index=False)
fig,ax=plt.subplots(figsize=(11,7));fig.subplots_adjust(left=.31,right=.87,bottom=.21,top=.76)
fig.text(.06,.945,'층이 달라지면 개입 효과도 달라졌다',fontsize=23,weight='bold');fig.text(.06,.885,'같은 축·같은 강도에서 효과를 직접 뺀 값 · 모호16문항 · UN0 · − 방향 개입',fontsize=11);fig.text(.06,.83,'유의한9개 층 차이만 표시 · 보충96개 Holm p<.05 · 점과95% 신뢰구간',fontsize=11)
colors={.25:'#627d98',1:'#227f9f',4:'#b34544'};labels=[]
for k,(axis,layer) in enumerate([('Anxiety','7-14'),('Anxiety','21-14'),('Desperation','21-14')]):
 for j,d in enumerate([.25,1,4]):
  r=l[(l.axis==axis)&(l.layer==layer)&(l.dose==d)].iloc[0];y=8-(k*3+j);v=r.estimate*100
  ax.errorbar(v,y,xerr=[[v-r.lo*100],[r.hi*100-v]],fmt='o',color=colors[d],capsize=4,ms=7,lw=2)
  labels.append(f'{axis} · L{layer.replace("-"," − L")} · {d:g}배')
  ax.text(1.025,y,f'{v:+.3f}',transform=ax.get_yaxis_transform(),ha='left',va='center',fontsize=10,color=colors[d],bbox={'facecolor':'white','edgecolor':'none','pad':2})
ax.set_yticks(range(8,-1,-1),labels);ax.axvline(0,color='#8a929a',lw=1);ax.set_xlim(-1.08,.09);ax.set_ylim(-.7,8.7);ax.set_xlabel('「알 수 없음」효과의 층 간 차이(%p)',labelpad=12);ax.grid(axis='x',alpha=.15);ax.spines[['top','right','left']].set_visible(False);ax.tick_params(axis='y',length=0,pad=10)
fig.text(.06,.11,'음수: 앞에 적힌 층의 개입 효과가 L14보다 작음. 각 층의 효과가0인지 검사한 그림과는 다르다.',fontsize=11)
fig.text(.06,.055,'신뢰구간은 보정 전. 무작위 방향 대비 정서 특이성은 확인되지 않았다. 전체 비유의 결과는 보존 자료에서 제공.',fontsize=10,color='#555')
for ext in ['png','svg','pdf']:fig.savefig(O/f'significant_layer_contrasts.{ext}',dpi=180,facecolor='white')
plt.close(fig)
(O/'validation.json').write_text(json.dumps({'primary_significant':6,'layer_contrasts_significant':9,'primary_family':144,'layer_family':96,'nonsignificant_not_zero':True,'reference':'same-condition sham, not R','no_new_inference':True},indent=2))
