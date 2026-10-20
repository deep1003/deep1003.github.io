"""Restore equal-area emotion atlas and overlapping token profiles from frozen caches."""
from pathlib import Path
import json, hashlib, shutil, colorsys, importlib.util
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import LinearSegmentedColormap, to_rgb, Normalize
from matplotlib.patches import Polygon, Rectangle, Patch
import matplotlib.patheffects as pe
from scipy.optimize import least_squares
BASE=Path(__file__).resolve().parent
P=BASE
D=P/'data'; F=P/'figures'; OUT=D/'atlas6'; OUT.mkdir(exist_ok=True)
AX=['Fear','Anxiety','Anger','Disgust','Calmness','Sadness','Desperation','Joy']
C=['U0T0','U0T1','U1T0','U1T1','C1T0','C1T1']
LABEL=['R0 · Reference / clause 0','R1 · Reference / clause 1','UN0 · Uncertainty / clause 0','UN1 · Uncertainty / clause 1','CN0 · Certainty / clause 0','CN1 · Certainty / clause 1']
COL=dict(zip(AX,['#D9382C','#B66B2F','#A82418','#79529B','#86B654','#F28B7A','#661226','#2E9A3C']))
plt.rcParams.update({'font.family':'Arial','font.size':7,'axes.titlesize':7,'axes.labelsize':6,'xtick.labelsize':5.5,'ytick.labelsize':5.5,'svg.fonttype':'none','pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})

A=pd.read_csv(D/'axis_cosines_6_conditions.csv'); I=pd.read_csv(D/'items_139.csv').sort_values(['category','cluster','sample_id'])
assert len(A)==27522 and I.sample_id.nunique()==139
# Original equal-area power-diagram algorithms, adapted to eight current emotion axes.
old=P/'code/original_atlas_geometry.py'
s=old.read_text(); functions=s[s.index('def clip('):]
ns={'np':np};exec(functions,ns);clip,area,center,partition=[ns[k] for k in ['clip','area','center','partition']]
pack=np.load(D/'axes_L14.npz'); names=pack['names'].tolist(); V=pack['directions'][[names.index(a) for a in AX]].astype(float);V/=np.linalg.norm(V,axis=1,keepdims=True)
u,sig,_=np.linalg.svd(V-V.mean(0),full_matrices=False);xy=u[:,:2]*sig[:2];sites=xy/np.abs(xy).max()*.7
theta=np.linspace(0,2*np.pi,256,endpoint=False);outer=np.c_[np.cos(theta),np.sin(theta)];target=area(outer)/8

def cells(weights):
 result=[]
 for i in range(8):
  p=outer.copy()
  for j in range(8):
   if i!=j:p=clip(p,2*(sites[j]-sites[i]),sites[j]@sites[j]-sites[i]@sites[i]+weights[i]-weights[j])
  result.append(p)
 return result
fit=least_squares(lambda w:np.array([area(p)/target-1 for p in cells(np.r_[0,w])])[1:],np.zeros(7),xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=1000)
polys=cells(np.r_[0,fit.x]);assert max(abs(area(p)/target-1) for p in polys)<1e-5
tiles=[];rows=[]
for ai,a in enumerate(AX):
 for item,parent in zip(I.itertuples(),partition(polys[ai],139)):
  for rot,p in enumerate(partition(parent,3)):
   rows.append(dict(tile_id=len(tiles),axis=a,item=item.sample_id,rotation=rot,category=item.category,cluster=item.cluster,area=area(p)));tiles.append(p)
M=pd.DataFrame(rows); assert len(M)==3336
values=M.merge(A,on=['axis','item','rotation'],validate='one_to_many')
ref=A[A.condition=='U0T0'][['axis','item','rotation','cosine']].rename(columns={'cosine':'reference'})
values=values.merge(ref,on=['axis','item','rotation'],validate='many_to_one');values['delta']=values.cosine-values.reference
assert len(values)==20016 and not values.duplicated(['tile_id','condition']).any()
assert values[values.condition=='U0T0'].delta.eq(0).all()
M.to_csv(OUT/'tile_layout.csv',index=False);values.to_csv(OUT/'atlas_source_data.csv',index=False)
(OUT/'region_geometry.json').write_text(json.dumps(dict(axes=AX,sites=sites.tolist(),polygons=[p.tolist() for p in polys],tiles=[p.tolist() for p in tiles])))
lo=min(float(values.delta.min()),-.00001);hi=max(float(values.delta.max()),.00001);norm=Normalize(lo,hi);zero=-lo/(hi-lo)
def ramp(color):
 h,l,s=colorsys.rgb_to_hls(*to_rgb(color));m=np.array(colorsys.hls_to_rgb(h,.42,s))
 stops=[(0,m*.18),(zero,m*.45),(zero+(1-zero)*.36,m),(zero+(1-zero)*.68,.55*m+.45*np.array(to_rgb('#FFE84A'))),(1,to_rgb('#FFFAA0'))]
 return LinearSegmentedColormap.from_list('emotion',stops)
cmaps={a:ramp(COL[a]) for a in AX}
fig=plt.figure(figsize=(180/25.4,245/25.4))
for k,c in enumerate(C):
 x=.025+(k%2)*.48;y=.68-(k//2)*.267;ax=fig.add_axes([x,y,.43,.255]);ax.set_aspect('equal');ax.axis('off')
 v=values[values.condition==c].set_index('tile_id').reindex(range(3336))
 colors=[cmaps[a](norm(d)) for a,d in zip(v.axis,v.delta)]
 ax.add_collection(PolyCollection(tiles,facecolors=colors,edgecolors='none',rasterized=True,antialiaseds=False))
 for a,p in zip(AX,polys):
  ax.add_patch(Polygon(p,fill=False,edgecolor='white',linewidth=.6));cx,cy=center(p)
  ax.text(cx,cy,a,ha='center',va='center',fontsize=6.2,fontweight='bold',color='white',path_effects=[pe.withStroke(linewidth=1.4,foreground='#222')])
 ax.set(xlim=(-1.03,1.03),ylim=(-1.03,1.03));ax.set_title(chr(97+k)+'  '+LABEL[k],loc='left',pad=5)
fig.text(.03,.985,'L14 emotion atlas | Master system notices',weight='bold',fontsize=9)
fig.text(.03,.966,'Change from R0 in the same item and choice rotation; 139 items × 3 repeated rotations per region',fontsize=6)
for k,a in enumerate(AX):
 x=.035+(k%4)*.24;y=.09-(k//4)*.039;ax=fig.add_axes([x,y,.17,.009]);ax.imshow(np.linspace(0,1,256)[None,:],cmap=cmaps[a],aspect='auto',extent=(lo,hi,0,1));ax.set_yticks([]);ax.set_xticks([lo,0,hi]);ax.set_xticklabels([f'{lo:+.3f}','0',f'{hi:+.3f}'],fontsize=4.6);ax.tick_params(length=1,pad=1);ax.set_title(a,fontsize=5.6,pad=2)
fig.text(.03,.013,'Schematic equal-area regions, not neural locations. Dark → emotion hue → yellow: increasing cosine change.\nCell positions carry no spatial meaning; rotations are repeated measures. Evaluation axes are reported separately.',fontsize=5.6)
def save(fig,name):
 for ext in ['png','pdf','svg']:fig.savefig(F/f'{name}.{ext}',dpi=600,bbox_inches='tight',pad_inches=.04)
 plt.close(fig)
save(fig,'Fig1_emotion_atlas_honeycomb6')
# Map actual tokenizer offsets to original system-content characters, then standardise each axis jointly across six prompts.
T=pd.read_csv(D/'system_token_alignment_6.csv');meta=json.loads((P/'prompt_token_metadata.json').read_text());prompts=json.loads((P/'prompts.json').read_text());texts={x['condition']:x['system_content'] for x in prompts['conditions']}
raw={};tokens={};char_token={}
for m in meta:
 c=m['condition'];start,end=m['system_content_span'];text=m['rendered'][start:end];assert text==texts[c]
 arr=np.zeros((len(text),8));cnt=np.zeros(len(text));ti=np.zeros(len(text));sub=T[T.condition==c].pivot(index='token_index',columns='axis',values='cosine')[AX]
 for j,(a,b) in enumerate(m['offsets']):
  aa=max(a,start)-start;bb=min(b,end)-start
  if bb>aa:arr[aa:bb]+=sub.loc[j].to_numpy();cnt[aa:bb]+=1;ti[aa:bb]+=j
 assert np.all(cnt>0);raw[c]=arr/cnt[:,None];char_token[c]=ti/cnt
 idx=[j for j,(a,b) in enumerate(m['offsets']) if b>start and a<end];tokens[c]=sub.loc[idx]
allv=np.vstack([raw[c] for c in C]);mu=allv.mean(0);sd=allv.std(0,ddof=1);assert (sd>0).all();Z={c:(raw[c]-mu)/sd for c in C}
# Reuse original Unicode-aware text layout; no tokenizer/model is loaded.
oldprompt=P/'code/prompt_concept_figure.py';sp=importlib.util.spec_from_file_location('original_prompt_layout',oldprompt);mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)
fig=plt.figure(figsize=(180/25.4,305/25.4));records=[];highlights=[]
for k,c in enumerate(C):
 bottom=.825-k*.15;ax=fig.add_axes([.075,bottom,.31,.115]);z=(tokens[c]-mu)/sd
 for a in AX:ax.plot(z.index,z[a],color=COL[a],lw=.65,alpha=.9)
 ax.axhline(.5,color='#888',lw=.4,ls=':');ax.set_xlabel('Actual token position',labelpad=1);ax.set_ylabel('Within-axis z',labelpad=1);ax.set_ylim(-5,5)
 fig.text(.025,bottom+.12,chr(97+k),weight='bold',fontsize=8);fig.text(.075,bottom+.12,LABEL[k],fontsize=7,weight='bold')
 text=texts[c];zv=Z[c];dom=zv.argmax(1);peak=zv.max(1);tx=fig.add_axes([.44,bottom,.535,.115]);fw,fh=fig.get_size_inches()*72;width=.535*fw;height=.115*fh;tx.set(xlim=(0,width),ylim=(0,height));tx.axis('off');size=6.5
 lines=mod.wrap_span(text,0,len(text),width-4,size);lh=8.7;assert len(lines)*lh<=height
 for row,line in enumerate(lines):
  for i,ch,x,w in line:
   y=height-row*lh
   strength=float(np.clip((peak[i]-.5)/2,0,1));color=COL[AX[dom[i]]]
   if strength>0:tx.add_patch(Rectangle((x,y-lh),w,lh,facecolor=mod.mix(color,.18+.65*strength),edgecolor='none'))
   tx.text(x,y-.5,ch,fontproperties=mod.FONT,fontsize=size,va='top',color='#171717')
 for i,ch in enumerate(text):records.append(dict(condition=c,char_index=i,char=ch,token_position=char_token[c][i],dominant=AX[dom[i]],peak_z=peak[i],highlighted=bool(peak[i]>.5),**{f'cos_{a}':raw[c][i,j] for j,a in enumerate(AX)},**{f'z_{a}':zv[i,j] for j,a in enumerate(AX)}))
 highlights.append(dict(condition=c,text=text,z=zv.tolist(),dominant=[AX[i] for i in dom],peak=peak.tolist(),token_position=char_token[c].tolist()))
fig.text(.075,.98,'Prompt emotion profiles and dominant-axis text highlights',fontsize=9,fontweight='bold');fig.text(.075,.961,'System-only L14 · overlapping eight emotion axes at actual token positions · original Korean prompts',fontsize=6)
fig.legend(handles=[Patch(color=COL[a],label=a) for a in AX],loc='lower center',bbox_to_anchor=(.52,.025),ncol=4,frameon=False,fontsize=6)
fig.text(.075,.012,'Right: largest within-axis z at each character, highlighted only above z = 0.5; darker = larger z (saturates at 2.5).\nAcross-six-prompt character calibration; overlapping byte-token fragments averaged. Descriptive, not emotion probability or causal activation.',fontsize=5.6)
save(fig,'Fig2_prompt_overlap_highlights6')
pd.DataFrame(records).to_csv(D/'prompt_dominant_emotion_source.csv',index=False)
(P/'prompt_dominant_emotions.json').write_text(json.dumps(dict(axes=AX,colors=COL,mean=mu.tolist(),sd=sd.tolist(),threshold=.5,saturation=2.5,prompts=highlights),ensure_ascii=False,separators=(',',':')))
validation=dict(items=139,clusters=91,conditions=6,rotations=3,emotions=AX,atlas_cells_per_panel=3336,atlas_values=20016,atlas_reference='U0T0, same item and rotation',atlas_scale=[lo,hi],equal_area_max_error=max(abs(area(p)/target-1) for p in polys),two_dimensional_variance=float((sig[:2]**2).sum()/(sig**2).sum()),prompt_highlight='argmax within-axis z over 8 emotions; threshold 0.5; six-prompt common calibration',evaluation_axes_excluded_from_emotion_winner=True,model_inference=False,behavior_figure_unchanged=True)
(P/'ATLAS_RESTORE_VALIDATION.json').write_text(json.dumps(validation,indent=2));print(json.dumps(validation,indent=2))
