"""EXAONE notice-state illustration from existing states and raw emotion contrasts."""
from pathlib import Path
import argparse,json,hashlib,math,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge,Circle
from matplotlib.offsetbox import DrawingArea,AnnotationBbox
from matplotlib.colors import LinearSegmentedColormap,Normalize

def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def build(states_file,instrument_file,out):
 out=Path(out);out.mkdir(parents=True,exist_ok=False)
 with np.load(states_file) as z:h=z['states'].astype(float);conditions=list(z['conditions'].astype(str))
 with np.load(instrument_file) as z:raw=z['raw_matched_class_means'].astype(float);names=list(z['emotion_order'].astype(str))
 assert h.shape==(5,4096) and raw.shape==(8,4096) and set(conditions)=={'R','UN0','CN0','UN1','CN1'}
 axes=raw/np.linalg.norm(raw,axis=1,keepdims=True);u,s,_=np.linalg.svd(axes.T,full_matrices=False);q=u[:,s>max(s)*1e-10];assert q.shape[1]==8
 x=h@q;_,ss,v=np.linalg.svd(x-x.mean(0),full_matrices=False);components=q@v[:2].T;xy=h@components;xy-=xy[conditions.index('R')];variance=ss**2/sum(ss**2);projection=h@axes.T;delta=projection-projection[conditions.index('R')];limit=math.ceil(np.max(np.abs(delta))*2)/2
 labels=axes@components*3.3;labels_by_name=dict(zip(names,labels));display={'panic':'Panic','fear':'Fear','anxiety':'Anxiety','desperation':'Desperation','sadness':'Sadness','anger':'Anger','joy':'Joy','calm':'Calmness'}
 colors=['#665487','#a23c31','#8b6b43','#884366','#bd6c60','#702b22','#356f44','#678139'];maps=[LinearSegmentedColormap.from_list(n,['#ffffff',c]) for n,c in zip(names,colors)]
 fig=plt.figure(figsize=(15,8.6));fig.text(.055,.96,'EXAONE-3.5-7.8B-Instruct · L21 · FP32',fontsize=15,weight='bold');axs=[fig.add_axes([.075,.34,.405,.54]),fig.add_axes([.56,.34,.405,.54])]
 def ring(ax,point,values,key):
  area=DrawingArea(24,24,0,0);radius=10.5
  for j,value in enumerate(values):area.add_artist(Wedge((12,12),radius,j*45,(j+1)*45,width=radius*.48,facecolor=maps[j](abs(value)/limit),edgecolor='#b9bec2',linewidth=.4,hatch='///' if value<0 else None))
  area.add_artist(Circle((12,12),radius*.32,color='white',ec='none'));color='#555c65' if key=='R' else '#d48222' if key.startswith('UN') else '#267bb5';marker='o' if key=='R' else 's' if key.startswith('UN') else '^';area.add_artist(plt.Line2D([12],[12],marker=marker,color=color,markersize=4.5,linestyle='None'));ax.add_artist(AnnotationBbox(area,point,frameon=False,box_alignment=(.5,.5),zorder=5))
 allxy=np.vstack([xy,labels]);xlim=(min(allxy[:,0])-.35,max(allxy[:,0])+.48);ylim=(min(allxy[:,1])-.35,max(allxy[:,1])+.38)
 label_offsets={'panic':(8,9),'fear':(0,18),'anxiety':(0,0),'desperation':(0,17),'sadness':(0,0),'anger':(0,-12),'joy':(0,-55),'calm':(0,0)}
 for ax,keys,title,letter in zip(axs,[['R','UN0','CN0'],['R','UN1','CN1']],['Continuation (KEEP) notices','Termination (TERM) notices'],['a','b']):
  ax.set_title(letter+'   '+title,loc='left',weight='bold',fontsize=12,pad=15);ax.set_xlim(xlim);ax.set_ylim(ylim);ax.axvline(0,color='#dce1e5',lw=.8);ax.axhline(0,color='#dce1e5',lw=.8);ax.spines[['top','right']].set_visible(False);ax.set_xlabel(f'PC1 ({variance[0]:.1%} of state variance)',fontsize=11)
  if ax is axs[0]:ax.set_ylabel(f'PC2 ({variance[1]:.1%} of state variance)',fontsize=11)
  else:ax.tick_params(labelleft=False)
  for name,color in zip(names,colors):ax.annotate(display[name],labels_by_name[name],xytext=label_offsets[name],textcoords='offset points',ha='center',fontsize=10,color=color,arrowprops=dict(arrowstyle='-',color=color,lw=.6) if name=='joy' else None)
  for k in keys:
   i=conditions.index(k);ring(ax,xy[i],delta[i],k);name={'R':'REF','UN0':'OPEN-KEEP','CN0':'CLOSED-KEEP','UN1':'OPEN-TERM','CN1':'CLOSED-TERM'}[k]
   offset={'R':(17,-19),'UN0':(-76,18),'CN0':(18,-18),'UN1':(-32,19),'CN1':(18,-20)}[k];ax.annotate(name,xy[i],xytext=offset,textcoords='offset points',color='#555c65' if k=='R' else '#d48222' if k.startswith('UN') else '#267bb5',fontsize=10,weight='bold',zorder=7)
  for first,second in zip(keys[:-1],keys[1:]):ax.annotate('',xy[conditions.index(second)],xytext=xy[conditions.index(first)],arrowprops=dict(arrowstyle='-|>',color='#555d63',linestyle='--',lw=1.8,shrinkA=12,shrinkB=12),zorder=2)
 fig.text(.5,.26,f'Ring shading 0–{limit:g} · absolute projection change from REF · equal sectors, not proportions · negative changes hatched',ha='center',fontsize=10,color='#555d63')
 for j,(name,cmap) in enumerate(zip(names,maps)):
  row,col=divmod(j,4);ax=fig.add_axes([.10+col*.225,.16-row*.09,.16,.015]);ax.imshow(np.linspace(0,1,256)[None,:],aspect='auto',cmap=cmap,extent=[0,limit,0,1]);ax.set_yticks([]);ax.set_xticks([0,limit/2,limit]);ax.tick_params(labelsize=8);ax.set_title(display[name],fontsize=9,pad=3)
 fig.text(.5,.015,'Exploratory comparisons between separate inputs, not a time course or a causal mediation test.',ha='center',fontsize=9,color='#555d63')
 for ext in ['png','pdf','svg']:fig.savefig(out/('exaone_L21_notice_states.'+ext),dpi=220,bbox_inches='tight')
 plt.close(fig)
 rows=[]
 for i,c in enumerate(conditions):
  record=dict(condition=c,PC1=float(xy[i,0]),PC2=float(xy[i,1]))
  for j,name in enumerate(names):record[name+'_projection']=float(projection[i,j]);record[name+'_change_from_REF']=float(delta[i,j])
  rows.append(record)
 with (out/'exaone_L21_notice_states_coordinates.csv').open('x',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 meta=dict(model='LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct',layer=21,precision='float32',state_shape=list(h.shape),raw_axis_span_rank=8,primary_centered_E8_rank=7,PC_variance_fractions=variance[:2].tolist(),two_PC_retained_fraction=float(sum(variance[:2])),ring_range=[0,limit],negative_hatching=True,equal_sector_areas=True,label_display_scale=3.3,axis_labels_are_directions_not_centroids=True,arrows_are_not_time_or_causal=True,new_model_inference=False,state_source_sha256=sha(states_file),instrument_source_sha256=sha(instrument_file),code_sha256=sha(__file__),method='Unit-normalised raw matched emotion-minus-neutral class means; retain common component; fit PCA on five raw-span projected states; translate REF to origin')
 (out/'NOTICE_STATES_METHOD.json').write_text(json.dumps(meta,indent=2)+'\n')
 title=f'State changes under continuation and termination notices in EXAONE. Two components retain {sum(variance[:2]):.1%} of state variation.'
 notes='The same main Korean notices were presented without a user question. States were captured at the final assistant-opening token at L21. Eight raw emotion-minus-neutral directions were unit normalised without neutral-PC removal or centering. Emotion names are uniformly rescaled projected direction labels, not story centroids or measured experience. REF is a comparison origin, not absence of emotion. Rings use full-dimensional changes along eight raw directions; equal-area sectors are not proportions and hatching marks negative changes. Dashed arrows join separate inputs rather than a time course. PCA bases, layer boundaries and ring ranges are model specific, so absolute coordinates and colour strength cannot be compared across models. This is exploratory, separate from judgement, moderation and attention-intervention tests.'
 (out/'exaone_L21_notice_states_title.txt').write_text(title+'\n');(out/'exaone_L21_notice_states_notes.txt').write_text(notes+'\n');print(title)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--states',type=Path,required=True);p.add_argument('--instrument',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();build(a.states,a.instrument,a.output)
