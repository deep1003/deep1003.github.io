"""Saved-data support figures only; no model inference. Default emits no graphs."""
from pathlib import Path
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--render',action='store_true')
args=parser.parse_args()
if not args.render:
 import numpy as np,pandas as pd
 base=Path(__file__).resolve().parent
 g=pd.read_csv(base/'data/emotion_axis_gram8.csv',index_col=0).to_numpy()
 assert g.shape==(8,8) and np.isfinite(g).all() and np.allclose(g,g.T)
 print('Saved eight-axis geometry verified; no plots or inference.')
 raise SystemExit(0)
"""Restore documentation and visual grammar only; no historical experiment results."""
from pathlib import Path
import json,hashlib,shutil,html
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import nbformat as nb
P=Path(__file__).resolve().parent;D=P/'data';F=P/'figures'
A=['Fear','Anxiety','Anger','Disgust','Calmness','Sadness','Desperation','Joy'];E=['Certainty','Uncertainty']
I=pd.read_csv(D/'items_139.csv');T=pd.read_csv(D/'behavior_6_conditions.csv');assert I.sample_id.nunique()==139 and T.item.nunique()==139 and len(T)==2502
categories={'age':'연령','disability_status':'장애 여부','domestic_area_of_origin':'국내 출신 지역','educational_background':'학력','family_structure':'가족 형태','gender_identity':'성별 정체성','physical_appearance':'외모','political_orientation':'정치 성향','race_ethnicity_nationality':'인종·민족·국적','religion':'종교','ses':'사회경제적 지위','sexual_orientation':'성적 지향'}
card=I.groupby('category').agg(items=('sample_id','nunique'),clusters=('cluster','nunique')).reset_index();card['category_ko']=card.category.map(categories);card=card[['category_ko','category','items','clusters']];card.to_csv(D/'sample_category_card.csv',index=False)
# Fixed-axis geometry, not new model measurements or population tests.
z=np.load(D/'axes_L14.npz');names=z['names'].tolist();v=z['directions'][[names.index(a) for a in A]].astype(float);v/=np.linalg.norm(v,axis=1,keepdims=True);G=v@v.T;assert np.allclose(np.diag(G),1) and np.allclose(G,G.T)
pd.DataFrame(G,index=A,columns=A).to_csv(D/'emotion_axis_gram8.csv',index_label='axis')
plt.rcParams.update({'font.family':'Arial','font.size':7,'svg.fonttype':'none','pdf.fonttype':42})
fig,ax=plt.subplots(figsize=(115/25.4,104/25.4));im=ax.imshow(G,cmap='RdBu_r',vmin=-1,vmax=1,interpolation='none');ax.set_xticks(range(8),A,rotation=45,ha='right',fontsize=6);ax.set_yticks(range(8),A,fontsize=6);ax.tick_params(length=0)
for i in range(8):
 for j in range(8):ax.text(j,i,f'{G[i,j]:.2f}',ha='center',va='center',fontsize=5.5,color='white' if abs(G[i,j])>.6 else '#111')
ax.set_title('Fixed emotion-axis directions | Gram matrix',fontsize=8,pad=8);cb=fig.colorbar(im,ax=ax,fraction=.04,pad=.05);cb.set_label('Cosine between axis directions',fontsize=6)
fig.text(.02,.01,'Descriptive geometry of eight fixed L14 directions, not item-level correlation or emotion probability.',fontsize=5)
fig.tight_layout(rect=(0,.035,1,1))
for ext in ['png','pdf','svg']:fig.savefig(F/f'Support_emotion_axis_geometry.{ext}',dpi=600,bbox_inches='tight')
plt.close(fig)

from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
plt.rcParams.update({'font.family':'Arial','font.size':7,'svg.fonttype':'none','pdf.fonttype':42})
fig,ax=plt.subplots(figsize=(180/25.4,93/25.4));ax.set(xlim=(0,100),ylim=(0,55));ax.axis('off')
def box(x,y,w,h,text,color):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.4,rounding_size=1',facecolor=color,edgecolor='#555',lw=.6));ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=6.5)
def arrow(x1,y1,x2,y2):ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=7,color='#444',lw=.7))
ax.text(0,53,'Measurement positions | Existing six-condition study',weight='bold',fontsize=8)
ax.text(0,47,'a  System-only: prompt localization',fontsize=7,weight='bold')
box(1,33,23,10,'System role + notice\n(no Ko-BBQ item)','#F1F4F6');arrow(25,38,33,38)
box(34,33,23,10,'L14 state at each\ninput token position','#E5F0F5');arrow(58,38,66,38)
box(67,33,31,10,'Overlapping emotion profiles\n+ literal text highlights','#F2F6EC')
ax.text(0,26,'b  Full input: item-conditioned representations and choice probabilities',fontsize=7,weight='bold')
box(1,12,23,10,'Same notice + Ko-BBQ\ncontext / question / choices','#F1F4F6');arrow(25,17,33,17)
box(34,12,23,10,'L14 final assistant-\nprefix token state','#E5F0F5');arrow(58,17,66,17)
box(67,12,31,10,'Fixed-axis cosines (L14)\nChoice logits (final layer)','#F2F6EC')
ax.text(0,3,'Schematic of measurement locations, not a causal pathway or a new experiment.\nChoice logits come from the final output head, not L14. Each L14 state has 3,584 dimensions.',fontsize=6)
fig.tight_layout(pad=.5)
for ext in ['png','pdf','svg']:fig.savefig(F/f'Support_measurement_positions.{ext}',dpi=600,bbox_inches='tight')
plt.close(fig)
