"""Final grid figures with every layer/dose cell and unadjusted intervals."""
from pathlib import Path
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import Rectangle
ROOT=Path(__file__).resolve().parent

def main():
 assert (ROOT/'DONE').exists()
 d=pd.read_csv(ROOT/'primary_144.csv');r=pd.read_csv(ROOT/'random_controls_144.csv');keys=['case_type','condition','layer','dose','axis','arm','metric'];d=d.merge(r[keys+['p_holm_random_144']],on=keys)
 plt.rcParams.update({'font.family':['AppleGothic','DejaVu Sans'],'font.size':10,'axes.unicode_minus':False,'svg.fonttype':'none','pdf.fonttype':42})
 for metric,stem,title in [('p_unknown','unknown_grid','알 수 없음'),('p_person_bias','person_bias_grid','사람 선택 내 고정관념')]:
  subset=d[d.metric==metric];limit=max(.005,float(np.abs(subset.estimate).max())*100);norm=TwoSlopeNorm(vmin=-limit,vcenter=0,vmax=limit)
  fig,axes=plt.subplots(2,4,figsize=(15,9));fig.subplots_adjust(left=.065,right=.93,top=.78,bottom=.14,wspace=.20,hspace=.38)
  fig.text(.04,.955,f'다층·다강도 검증: {title}',fontsize=22,weight='bold')
  fig.text(.04,.912,'32문항 · L7/L14/L21 · 기준의0.25/1/4배 · 3선택지 순서 평균 · 동일 공지 sham 대비 %p',fontsize=11)
  fig.text(.04,.875,'색: 평균 변화  |  숫자: 평균 [보정 전95% 구간]  |  *: 주 검정 Holm144 p<.05  |  #: 무작위 대조 Holm144 p<.05',fontsize=10)
  fig.text(.04,.835,'녹색 테두리: 같은 셀이 두 대조를 모두 통과. 큰 색만 보고 최적 조합을 선택하지 않는다.',fontsize=10,color='#555')
  for i,typ in enumerate(['amb','dis']):
   for j,(axis,cond,sign) in enumerate([(a,c,s) for a in ['Anxiety','Desperation'] for c,s in [('CN0','+'),('UN0','-')]]):
    ax=axes[i,j];mat=np.zeros((3,3));rows={}
    for y,layer in enumerate([7,14,21]):
     for x,dose in enumerate([.25,1,4]):
      row=subset[(subset.case_type==typ)&(subset.axis==axis)&(subset.condition==cond)&(subset.layer==layer)&(subset.dose==dose)].iloc[0];mat[y,x]=row.estimate*100;rows[y,x]=row
    image=ax.imshow(mat,cmap='RdBu_r',norm=norm,aspect='auto')
    for (y,x),row in rows.items():
     a=row.p_holm_144<.05;b=row.p_holm_random_144<.05;mark=('*' if a else '')+('#' if b else '')
     value=row.estimate*100;lo=row.lo*100;hi=row.hi*100
     mean_text=f'{value:+.3f}' if abs(value)>=.0005 else f'{value:+.1e}'
     txt=f'{mean_text}{mark}\n[{lo:+.3f},\n{hi:+.3f}]'
     color='white' if abs(value)>.65*limit else '#111';ax.text(x,y,txt,ha='center',va='center',fontsize=8.6,color=color)
     if a and b:ax.add_patch(Rectangle((x-.48,y-.48),.96,.96,fill=False,edgecolor='#009E73',lw=3))
    ax.set_xticks(range(3),['0.25x','1x','4x']);ax.set_yticks(range(3),['L7','L14','L21']);ax.tick_params(length=0,pad=7)
    ax.set_title(('모호' if typ=='amb' else '명확')+' · '+axis+'\n'+cond+' '+sign+' 방향',fontsize=11,pad=13)
    if i==1:ax.set_xlabel('층별 기준 L2 용량의 배수')
  bar=fig.colorbar(image,cax=fig.add_axes([.948,.20,.012,.52]));bar.set_label('평균 변화 (%p)')
  fig.text(.04,.058,'Anxiety·Desperation은 층마다 원래 프로브로 재추출했다. 축 강도는 감정 강도가 아니며, 주관적 경험 또는 자연 매개효과를 입증하지 않는다.',fontsize=10,color='#555')
  for ext in ['png','svg','pdf']:fig.savefig(ROOT/f'{stem}.{ext}',dpi=180,facecolor='white')
  plt.close(fig)

if __name__=='__main__':main()
