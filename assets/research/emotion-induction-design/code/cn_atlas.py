"""Eight-axis atlas from frozen directions and cached L14 states. No model inference."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.optimize import least_squares
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.collections import PolyCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize
from PIL import Image
from emotion_atlas import clip, area, center, partition

BASE = Path(__file__).resolve().parent
EXT = BASE/'representation_analysis/certainty_extension'
OUT = EXT/'atlas8'
OLD = BASE/'representation_analysis/emotion_atlas/output'
AXES = ['UN','CN','FA','calm','sadness','anger','desperation','joy']
NAMES = ['UN','CN','FA','Calm','Sadness','Anger','Desperation','Joy']
LABELS = ['Uncertainty','Certainty','Fear /\nanxiety','Calm','Sadness','Anger','Desperation','Joy']
COLORS = ['#2166C4','#5B9BD5','#D9382C','#86C454','#F28B7A','#A82418','#661226','#2E9A3C']
CONDITIONS = ['UN0FA0','UN0FA1','UN1FA0','UN1FA1']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    OUT.mkdir(exist_ok=True)
    old = pd.read_csv(OLD/'atlas_source_data.csv')
    cn = np.load(EXT/'certainty_axis_L14.npz')
    rows, inputs = [], {}
    chunks = BASE/'representation_analysis/item_category_alignment/output/chunks'
    for path in sorted(chunks.glob('batch_[0-9][0-9][0-9][0-9][0-9].npz')):
        inputs[path.name] = sha(path)
        with np.load(path) as data:
            hidden = data['hidden'][:,0,:].astype(float)
            diff = hidden-cn['center']
            scores = diff@cn['direction']/np.linalg.norm(diff,axis=1)
            for key, value in zip(data['keys'],scores):
                item,condition,rotation = key
                rows.append(dict(item=str(item),condition=str(condition).replace('U','UN').replace('T','FA'),
                                 rotation=int(rotation),axis='CN',cosine=float(value)))
    raw_cn = pd.DataFrame(rows)
    keys = ['item','condition','rotation']
    assert len(raw_cn)==1668 and not raw_cn.duplicated(keys).any()
    assert np.isfinite(raw_cn.cosine).all() and (raw_cn.cosine.abs()<=1).all()
    raw_old = old[['axis']+keys+['cosine']].copy()
    raw = pd.concat([raw_old,raw_cn],ignore_index=True)
    assert len(raw)==13344
    original = np.load(BASE/'representation_analysis/results/d335ad178e3c/axes_qwen_L14.npz')['directions'].astype(float)
    directions = np.insert(original,1,cn['direction'],axis=0)
    directions /= np.linalg.norm(directions,axis=1,keepdims=True)
    cosine = directions@directions.T
    published = pd.read_csv(EXT/'axis_cosines_qwen_L14_with_certainty.csv',index_col=0)
    assert np.allclose(cosine,published.values,atol=1e-12)
    u,s,_ = np.linalg.svd(directions-directions.mean(0),full_matrices=False)
    xy = u[:,:2]*s[:2]
    if xy[0,0]>xy[3,0]: xy[:,0]*=-1
    if xy[3,1]<xy[5,1]: xy[:,1]*=-1
    sites = xy/np.max(np.abs(xy))*.70
    theta = np.linspace(0,2*np.pi,512,endpoint=False)
    outer = np.column_stack([np.cos(theta),np.sin(theta)])
    target = area(outer)/8
    def cells(weights):
        result=[]
        for i in range(8):
            p=outer.copy()
            for j in range(8):
                if i!=j:
                    p=clip(p,2*(sites[j]-sites[i]),sites[j]@sites[j]-sites[i]@sites[i]+weights[i]-weights[j])
            result.append(p)
        return result
    fit=least_squares(lambda w:np.array([area(p)/target-1 for p in cells(np.r_[0.,w])])[1:],np.zeros(7),
                      xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=1000)
    weights=np.r_[0.,fit.x]
    polys=cells(weights)
    assert max(abs(area(p)/target-1) for p in polys)<1e-5
    adjacency=np.zeros((8,8),bool)
    for i in range(8):
        for j in range(i+1,8):
            n=2*(sites[j]-sites[i]);b=sites[j]@sites[j]-sites[i]@sites[i]+weights[i]-weights[j]
            edge=polys[i][abs(polys[i]@n-b)<1e-7]
            adjacency[i,j]=adjacency[j,i]=len(edge)>1 and max(pdist(edge))>1e-6
    items=old[['item','category','cluster']].drop_duplicates().sort_values(['category','cluster','item'])
    tiles,mapping=[],[]
    for axis,poly in zip(AXES,polys):
        for item,parent in zip(items.itertuples(index=False),partition(poly,139)):
            for rotation,p in enumerate(partition(parent,3)):
                mapping.append(dict(tile_id=len(tiles),axis=axis,item=item.item,rotation=rotation,category=item.category,
                                    cluster=item.cluster,area=area(p)))
                tiles.append(p)
    mapping=pd.DataFrame(mapping)
    values=mapping.merge(raw,on=['axis','item','rotation'],validate='one_to_many')
    ref=raw[raw.condition=='UN0FA0'].drop(columns='condition').rename(columns={'cosine':'baseline'})
    values=values.merge(ref,on=['axis','item','rotation'],validate='many_to_one')
    values['delta_cosine']=values.cosine-values.baseline
    assert len(mapping)==3336 and len(values)==13344
    assert not values.duplicated(['axis']+keys).any()
    assert (values.loc[values.condition=='UN0FA0','delta_cosine']==0).all()
    parity=values[values.axis!='CN'].merge(old,on=['axis']+keys,suffixes=('_new','_old'),validate='one_to_one')
    assert np.array_equal(parity.cosine_new,parity.cosine_old)
    assert np.allclose(parity.delta_cosine_new,parity.delta_cosine_old,atol=1e-16)
    values.to_csv(OUT/'atlas_source_data.csv',index=False)
    mapping.to_csv(OUT/'tile_layout.csv',index=False)
    pd.DataFrame(cosine,index=NAMES,columns=NAMES).to_csv(OUT/'concept_cosines.csv')
    pd.DataFrame(adjacency,index=NAMES,columns=NAMES).to_csv(OUT/'boundary_adjacency.csv')
    pd.DataFrame(linkage(pdist(directions,metric='cosine'),method='average',optimal_ordering=True),
                 columns=['child_1','child_2','distance','n_concepts']).to_csv(OUT/'hierarchical_linkage.csv',index=False)
    # Rigid display rotation only: preserve all distances, contacts and tile identities.
    pair_centers=np.array([center(p) for p in polys[:2]])
    heading=np.mean(pair_centers/np.linalg.norm(pair_centers,axis=1,keepdims=True),axis=0)
    angle=3*np.pi/4-np.arctan2(heading[1],heading[0])
    rotation=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
    polys=[p@rotation.T for p in polys]
    tiles=[p@rotation.T for p in tiles]
    sites=sites@rotation.T
    xy=xy@rotation.T
    geometry=dict(axes=AXES,polygons=[p.tolist() for p in polys],tiles=[p.tolist() for p in tiles],sites=sites.tolist(),weights=weights.tolist())
    (OUT/'region_geometry.json').write_text(json.dumps(geometry))
    # Shared numeric limits across all regions and conditions. No clipping of CN values.
    low=min(-.007,float(values.delta_cosine.min()))
    high=max(.016,float(values.delta_cosine.max()))
    low=np.floor(low*1000)/1000;high=np.ceil(high*1000)/1000
    norm=Normalize(low,high)
    from emotion_atlas_coloured import mid_tone,shade
    def ramp(color):
        m=np.array(mid_tone(color));yellow=np.array(matplotlib.colors.to_rgb('#FFE84A'))
        z=(0-low)/(high-low)
        return LinearSegmentedColormap.from_list('axis',[(0,shade(m,.18)),(z,shade(m,.45)),
            (z+.37*(1-z),m),(z+.63*(1-z),.55*m+.45*yellow),(z+.86*(1-z),yellow),(1,'#FFFAA0')])
    cmaps={a:ramp(c) for a,c in zip(AXES,COLORS)}
    plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','savefig.dpi':600})
    fig=plt.figure(figsize=(10,11.6))
    for condition,panel,(x,y) in zip(CONDITIONS,'abcd',[(.02,.55),(.51,.55),(.02,.115),(.51,.115)]):
        ax=fig.add_axes([x,y,.47,.405]);ax.set_aspect('equal');ax.axis('off')
        subset=values[values.condition==condition].set_index('tile_id').reindex(range(len(tiles)))
        colors=[cmaps[a](norm(v)) for a,v in zip(mapping.axis,subset.delta_cosine)]
        ax.add_collection(PolyCollection(tiles,facecolors=colors,edgecolors='none',antialiaseds=False,rasterized=True))
        for label,p in zip(LABELS,polys):
            closed=np.vstack([p,p[:1]])
            ax.plot(*closed.T,color='white',lw=1.0)
            cx,cy=center(p)
            ax.text(cx,cy,label,ha='center',va='center',fontsize=10,weight='bold',color='white',
                    path_effects=[pe.withStroke(linewidth=2.5,foreground='black')])
        ax.set(xlim=(-1.02,1.02),ylim=(-1.02,1.02))
        ax.set_title(f'{panel}  {condition}'+(' (reference)' if condition=='UN0FA0' else ''),loc='left',fontsize=12,pad=8)
    fig.text(.04,.085,f'Change in cosine vs. UN0FA0: shared scale {low:+.3f} to {high:+.3f}',fontsize=10)
    grad=np.linspace(low,high,256)[None,:]
    for k,(axis,label) in enumerate(zip(AXES,NAMES)):
        x=.04+(k%4)*.245;y=.055-(k//4)*.037
        ax=fig.add_axes([x,y,.155,.011]);ax.imshow(grad,cmap=cmaps[axis],norm=norm,aspect='auto',extent=[low,high,0,1])
        ax.set_xticks([low,0,high],labels=[f'{low:+.3f}','0',f'{high:+.3f}'],fontsize=6)
        ax.set_yticks([]);ax.tick_params(length=1,pad=1)
        fig.text(x+.161,y,'Certainty' if label=='CN' else label,fontsize=8)
    stem=OUT/'Emotion_atlas_CN_en'
    for ext in ['png','pdf','svg']:
        fig.savefig(stem.with_suffix('.'+ext),dpi=600,facecolor='white')
    fig.savefig(OUT/'preview.png',dpi=130,facecolor='white')
    plt.close(fig)
    validation=dict(no_model_inference=True,n_items=139,n_conditions=4,n_rotations=3,axis_count=8,
        n_tiles_per_region=417,n_tiles_per_panel=3336,n_value_rows=13344,old_seven_scores_preserved=True,
        two_dimensional_retained_variance=float(sum(s[:2]**2)/sum(s**2)),
        max_relative_area_error=float(max(abs(area(p)/target-1) for p in polys)),
        color_limits=[low,high],delta_range=[float(values.delta_cosine.min()),float(values.delta_cosine.max())],
        cn_condition_mean_delta=values[values.axis=='CN'].groupby('condition').delta_cosine.mean().to_dict(),
        chunks_sha256=inputs,axis_sha256=sha(EXT/'certainty_axis_L14.npz'),
        builder_sha256=sha(Path(__file__)),new_adjacency=True,display_rotation_degrees=float(np.degrees(angle)),rotation_preserves_geometry=True)
    (OUT/'validation.json').write_text(json.dumps(validation,indent=2))
    print(json.dumps({k:v for k,v in validation.items() if k!='chunks_sha256'},indent=2))
    return OUT

if __name__=='__main__':
    build()
