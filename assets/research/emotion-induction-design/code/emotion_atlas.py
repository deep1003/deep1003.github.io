"""Power-cell concept atlas with real rotation-level observations and cluster diagnostics."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
from scipy.optimize import least_squares
from scipy.spatial.distance import pdist,squareform
from scipy.cluster.hierarchy import linkage,dendrogram,cophenet
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.collections import PolyCollection
import matplotlib.patheffects as pe
from plot_style import activation_cmap,similarity_cmap,PALETTE,CONDITION_ORDER,heatmap_text_color

BASE=Path(__file__).resolve().parent
AXIS_DATA=BASE/'representation_analysis/results/d335ad178e3c'
ITEM_DATA=BASE/'representation_analysis/item_category_alignment/output/item_alignment.csv'
TRIAL_DATA=ITEM_DATA.with_name('trial_alignment.csv')
OUT=BASE/'representation_analysis/emotion_atlas/output'
AXES=['UN','FA','calm','sadness','anger','desperation','joy']
LABELS=['Uncertainty','Fear /\nanxiety','Calm','Sadness','Anger','Desperation','Joy']
CONDITIONS=CONDITION_ORDER

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def clip(poly,n,b):
    if len(poly)==0:return np.empty((0,2))
    result=[]
    for a,z in zip(poly,np.roll(poly,-1,axis=0)):
        da, dz=np.dot(a,n)-b,np.dot(z,n)-b
        ina,inz=da<=1e-12,dz<=1e-12
        if ina:result.append(a)
        if ina!=inz:result.append(a+(z-a)*da/(da-dz))
    return np.array(result).reshape(-1,2)

def area(poly):
    if len(poly)<3:return 0.
    return abs(np.sum(poly[:,0]*np.roll(poly[:,1],-1)-poly[:,1]*np.roll(poly[:,0],-1)))/2

def center(poly):
    cross=poly[:,0]*np.roll(poly[:,1],-1)-np.roll(poly[:,0],-1)*poly[:,1]
    return np.sum((poly+np.roll(poly,-1,axis=0))*cross[:,None],axis=0)/(3*cross.sum())

def partition(poly,n):
    """Equal-area recursive cuts. Geometry never uses measured activation values."""
    if n==1:return [poly]
    axis=int(np.argmax(np.ptp(poly,axis=0)));normal=np.eye(2)[axis]
    a,z=poly[:,axis].min(),poly[:,axis].max();left=n//2;target=area(poly)*left/n
    for _ in range(40):
        mid=(a+z)/2
        if area(clip(poly,normal,mid))<target:a=mid
        else:z=mid
    mid=(a+z)/2
    return partition(clip(poly,normal,mid),left)+partition(clip(poly,-normal,-mid),n-left)

def layout():
    directions=np.load(AXIS_DATA/'axes_qwen_L14.npz')['directions'].astype(float)
    directions/=np.linalg.norm(directions,axis=1,keepdims=True)
    u,s,_=np.linalg.svd(directions-directions.mean(0),full_matrices=False)
    xy=u[:,:2]*s[:2]
    if xy[0,0]>xy[2,0]:xy[:,0]*=-1
    if xy[2,1]<xy[4,1]:xy[:,1]*=-1
    sites=xy/np.max(np.abs(xy))*.70
    t=np.linspace(0,2*np.pi,256,endpoint=False);outer=np.column_stack([np.cos(t),np.sin(t)])
    total=area(outer);target=total/7
    def cells(w):
        polys=[]
        for i in range(7):
            p=outer.copy()
            for j in range(7):
                if i!=j:p=clip(p,2*(sites[j]-sites[i]),np.dot(sites[j],sites[j])-np.dot(sites[i],sites[i])+w[i]-w[j])
            polys.append(p)
        return polys
    def residual(w):return np.array([area(p)/target-1 for p in cells(np.r_[0.,w])])[1:]
    fit=least_squares(residual,np.zeros(6),xtol=1e-12,ftol=1e-12,gtol=1e-12,max_nfev=500)
    weights=np.r_[0.,fit.x];polys=cells(weights)
    errors=np.array([area(p)/target-1 for p in polys]);assert np.max(abs(errors))<1e-5
    cosine=directions@directions.T;distance=pdist(directions,metric='cosine')
    tree=linkage(distance,method='average',optimal_ordering=True)
    coph=float(cophenet(tree,distance)[0]);adjacency=np.zeros((7,7),bool)
    for i in range(7):
        for j in range(i+1,7):
            n=2*(sites[j]-sites[i]);b=np.dot(sites[j],sites[j])-np.dot(sites[i],sites[i])+weights[i]-weights[j]
            edge=polys[i][abs(polys[i]@n-b)<1e-7]
            adjacency[i,j]=adjacency[j,i]=len(edge)>1 and np.max(pdist(edge))>1e-6
    high=pdist(directions);low=pdist(xy)
    diagnostics=dict(two_dimensional_retained_variance=float((s[:2]**2).sum()/(s**2).sum()),
        distance_stress=float(np.sqrt(np.sum((high-low)**2)/np.sum(high**2))),
        distance_rank_spearman=float(spearmanr(high,low).statistic),
        cophenetic_correlation=coph,max_relative_region_area_error=float(np.max(abs(errors))),
        geometry='Equal-area power diagram of original PCA sites; not a neural or geographic map.',
        clustering='Average linkage on original 1-cosine distances; optimal leaf order.',
        area_has_no_emotional_meaning=True)
    return polys,xy,sites,weights,cosine,tree,adjacency,diagnostics

def hierarchy_figure(cosine,tree,adjacency):
    from english_figures import save
    fig,(ax,hm)=plt.subplots(1,2,figsize=(180/25.4,110/25.4))
    fig.subplots_adjust(left=.20,right=.91,bottom=.22,top=.84,wspace=.75)
    d=dendrogram(tree,labels=[x.replace('\n',' ') for x in LABELS],orientation='left',
        color_threshold=0,above_threshold_color='#444444',ax=ax)
    ax.set_xlabel('Average-linkage distance (1 - cosine)',fontsize=7)
    ax.set_title('a  Hierarchy in original axis space',loc='left',fontsize=8,pad=16)
    ax.tick_params(axis='y',labelsize=7)
    ax.spines[['top','right']].set_visible(False)
    order=d['leaves'][::-1];v=cosine[np.ix_(order,order)];contact=adjacency[np.ix_(order,order)]
    cmap=similarity_cmap();cmap.set_bad('#EEEEEE');norm=Normalize(-1,1)
    im=hm.imshow(np.ma.array(v,mask=~contact),cmap=cmap,norm=norm,interpolation='none')
    for i in range(7):
        for j in range(7):
            if contact[i,j]:hm.text(j,i,f'{v[i,j]:.2f}',ha='center',va='center',fontsize=6,color=heatmap_text_color(cmap,norm,v[i,j]))
    labels=[AXES[i].capitalize() if AXES[i] not in ['UN','FA'] else AXES[i] for i in order]
    hm.set_xticks(range(7),labels,rotation=45,ha='right',fontsize=6)
    hm.set_yticks(range(7),labels,fontsize=6);hm.tick_params(length=0)
    hm.set_title('b  Cosines of boundary-sharing pairs',loc='left',fontsize=8,pad=16)
    fig.colorbar(im,cax=fig.add_axes([.94,.31,.015,.38]),ticks=[-1,0,1],label='Axis cosine')
    fig.text(.04,.04,'Gray: no inter-region boundary; diagonal omitted. Boundary contact is geometric, not a similarity estimate.',fontsize=6)
    save(fig,OUT,'Emotion_atlas_hierarchy_en',False)

def build(show=True):
    from english_figures import style,save
    style();OUT.mkdir(parents=True,exist_ok=True)
    data=pd.read_csv(TRIAL_DATA);data=data[data.layer==14].copy()
    assert len(data)==1668 and not data.duplicated(['item','rotation','condition']).any()
    pooled=pd.read_csv(ITEM_DATA);pooled=pooled[pooled.layer==14]
    avg=data.groupby(['item','condition'])[['cos_'+a for a in AXES]].mean()
    target=pooled.set_index(['item','condition'])[['cos_'+a for a in AXES]].sort_index()
    assert np.allclose(avg.sort_index(),target,atol=1e-12)
    items=data[['item','category','cluster']].drop_duplicates().sort_values(['category','cluster','item'])
    polys,xy,sites,weights,cosine,tree,adj,diagnostics=layout()
    tiles=[];rows=[];parent_areas=[]
    for k,axis in enumerate(AXES):
        parent_cells=partition(polys[k],139)
        for item,parent in zip(items.itertuples(index=False),parent_cells):
            parts=partition(parent,3)
            parent_areas.append(area(parent))
            for rotation,poly in enumerate(parts):
                tile_id=len(tiles);tiles.append(poly)
                rows.append(dict(tile_id=tile_id,axis=axis,item=item.item,rotation=rotation,
                    category=item.category,cluster=item.cluster,area=area(poly),x=center(poly)[0],y=center(poly)[1]))
    mapping=pd.DataFrame(rows);assert len(mapping)==2919
    raw=data.melt(id_vars=['item','rotation','condition'],value_vars=['cos_'+a for a in AXES],var_name='axis',value_name='cosine')
    raw.axis=raw.axis.str.removeprefix('cos_')
    values=mapping.merge(raw,on=['axis','item','rotation'],validate='one_to_many')
    baseline=raw[raw.condition=='UN0FA0'][['axis','item','rotation','cosine']].rename(columns={'cosine':'baseline'})
    values=values.merge(baseline,on=['axis','item','rotation'],validate='many_to_one')
    values['delta_cosine']=values.cosine-values.baseline
    assert len(values)==11676 and not values.duplicated(['axis','item','rotation','condition']).any()
    assert (values[values.condition=='UN0FA0'].delta_cosine==0).all()
    mapping.to_csv(OUT/'tile_layout.csv',index=False);values.to_csv(OUT/'atlas_source_data.csv',index=False)
    pd.DataFrame(xy,index=AXES,columns=['Dimension_1','Dimension_2']).to_csv(OUT/'concept_coordinates.csv')
    pd.DataFrame(cosine,index=AXES,columns=AXES).to_csv(OUT/'concept_cosines.csv')
    pd.DataFrame(adj,index=AXES,columns=AXES).to_csv(OUT/'boundary_adjacency.csv')
    pd.DataFrame(tree,columns=['child_1','child_2','distance','n_concepts']).to_csv(OUT/'hierarchical_linkage.csv',index=False)
    (OUT/'region_geometry.json').write_text(json.dumps(dict(axes=AXES,polygons=[p.tolist() for p in polys],weights=weights.tolist(),sites=sites.tolist(),tiles=[p.tolist() for p in tiles])))
    hierarchy_figure(cosine,tree,adj)
    cmap=activation_cmap();outputs=[]
    for metric,name,title,label in [('cosine','Emotion_atlas_absolute_en','Concept-cosine similarity atlas','L14 centered cosine similarity'),('delta_cosine','Emotion_atlas_change_en','Change from the shared reference','Change in cosine vs. UN0FA0')]:
        low,high=float(values[metric].min()),float(values[metric].max());norm=Normalize(low,high)
        fig,axs=plt.subplots(2,2,figsize=(180/25.4,190/25.4))
        fig.subplots_adjust(left=.025,right=.88,top=.88,bottom=.14,wspace=.08,hspace=.16)
        fig.text(.025,.97,title,fontsize=10,weight='bold')
        fig.text(.025,.935,'Qwen2.5-7B-Instruct, L14; 139 items x 3 observed choice rotations per region',fontsize=6.5)
        def draw(ax,condition,panel):
            v=values[values.condition==condition].set_index('tile_id').reindex(range(len(tiles)))
            collection=PolyCollection(tiles,array=v[metric].to_numpy(),cmap=cmap,norm=norm,edgecolors='none',antialiaseds=False,rasterized=True)
            ax.add_collection(collection)
            for k,p in enumerate(polys):
                closed=np.vstack([p,p[:1]])
                ax.plot(closed[:,0],closed[:,1],color='#FFF5EA',lw=.65,zorder=3)
                cx,cy=center(p)
                text=ax.text(cx,cy,LABELS[k],color='white',fontsize=6,weight='bold',ha='center',va='center',zorder=4)
                text.set_path_effects([pe.withStroke(linewidth=1.8,foreground='#300000')])
            ax.set(xlim=(-1.03,1.03),ylim=(-1.03,1.03),aspect='equal');ax.axis('off')
            ax.set_title(f'{panel}  {condition}'+(' (reference)' if condition=='UN0FA0' else ''),loc='left',fontsize=7)
            return collection
        for ax,c,p in zip(axs.flat,CONDITIONS,'abcd'):im=draw(ax,c,p)
        cb=fig.colorbar(im,cax=fig.add_axes([.91,.24,.018,.50]))
        cb.set_label(label,fontsize=7);ticks=sorted(set([low,0.,high])) if low<=0<=high else [low,high]
        cb.set_ticks(ticks);cb.ax.set_yticklabels([f'{v:+.3f}' for v in ticks],fontsize=6)
        fig.text(.025,.095,'Power-cell regions: schematic similarity-based geometry; see the accompanying hierarchy.',fontsize=6)
        fig.text(.025,.065,'Each small cell is an observed item-rotation value. Three rotations remain repeated measures of 139 items.',fontsize=6)
        fig.text(.025,.035,'No interpolation, extra observations or spatial interpretation of within-region cell positions.',fontsize=6)
        path=save(fig,OUT,name,show);outputs.append(path)
        # Backward-compatible display copies are true 600 dpi exports.
        import shutil
        shutil.copy2(path,OUT/f'{name}_preview.png')
        if metric=='delta_cosine':
            single,ax=plt.subplots(figsize=(180/25.4,175/25.4));single.subplots_adjust(left=.03,right=.85,top=.91,bottom=.13)
            im=draw(ax,'UN1FA1','');single.colorbar(im,cax=single.add_axes([.90,.25,.018,.49]),label=label)
            single.text(.03,.055,'139 items x 3 choice rotations per region; repeated measures, not 417 independent items.',fontsize=7)
            save(single,OUT,'Emotion_atlas_combined_detail_en',False)
    validation=dict(n_concepts=7,n_items=139,n_rotations=3,n_conditions=4,n_cells_per_region=417,n_cells_per_panel=2919,
        n_measured_values=11676,baseline='same item, rotation and concept in UN0FA0',model_inference=False,
        interpolated_values=False,duplicated_keys=0,rotation_mean_matches_original_item_data=True,rotation_mean_tolerance=1e-12,
        max_rotation_mean_abs_error=float(np.max(np.abs(avg.sort_index().to_numpy()-target.to_numpy()))),
        max_relative_tile_area_error=float(np.max(np.abs(mapping.area.to_numpy()/(sum(area(p) for p in polys)/2919)-1))),
        diagnostics=diagnostics,source_sha256=sha(TRIAL_DATA),pooled_source_sha256=sha(ITEM_DATA),
        axes_sha256=sha(AXIS_DATA/'axes_qwen_L14.npz'),code_sha256=sha(__file__))
    (OUT/'validation.json').write_text(json.dumps(validation,indent=2))
    return outputs

if __name__=='__main__':build(False)
