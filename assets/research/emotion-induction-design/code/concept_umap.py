"""Joint UMAP of cached seven-concept profiles. No model inference or forced regions."""
from pathlib import Path
import hashlib,json,importlib.metadata
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.manifold import trustworthiness
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from plot_style import CONDITION_ORDER,CONDITION_COLORS

BASE=Path(__file__).resolve().parent
SOURCE=BASE/'representation_analysis/item_category_alignment/output/item_alignment.csv'
OUT=BASE/'representation_analysis/emotion_atlas/output'
AXES=['UN','FA','calm','sadness','anger','desperation','joy']
SCENARIOS=[(15,42),(5,42),(30,42),(15,13),(15,97)]

def build(show=False,refit=False):
    from english_figures import style,save
    OUT.mkdir(exist_ok=True,parents=True)
    d=pd.read_csv(SOURCE);d=d[d.layer==14].copy()
    d['condition']=pd.Categorical(d.condition,CONDITION_ORDER,ordered=True)
    d=d.sort_values(['condition','item']).reset_index(drop=True)
    x=d[['cos_'+a for a in AXES]].to_numpy(float)
    assert x.shape==(556,7) and np.isfinite(x).all()
    cached=OUT/'umap_validation.json'
    prior=json.loads(cached.read_text()) if cached.exists() else {}
    version=prior.get('settings',{}).get('umap_version') if not refit else None
    if version is None:version=importlib.metadata.version('umap-learn')
    plan=dict(source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        rows='139 selected items x 4 conditions; repeated within item',features=['cos_'+a for a in AXES],
        preprocessing='No rescaling or orthogonalization; seven original cosine-cosine similarity features.',
        fit_scope='All four conditions jointly; this is not a baseline-only embedding.',
        primary=dict(n_neighbors=15,random_state=42,min_dist=.3,metric='euclidean',n_epochs=300,n_jobs=1),
        sensitivity=[dict(n_neighbors=n,random_state=s) for n,s in SCENARIOS],
        model_inference=False,umap_version=version)
    planpath=OUT/'umap_plan.json';signature=hashlib.sha256(json.dumps(plan,sort_keys=True).encode()).hexdigest()
    if refit or not (cached.exists() and json.loads(cached.read_text()).get('plan_signature')==signature):
        planpath.write_text(json.dumps(plan,indent=2))  # Fixed before any layout is fitted.
        from umap import UMAP
        records=[];embedding=None
        high=cdist(x,x);np.fill_diagonal(high,np.inf);true_nn=np.argsort(high,axis=1)[:,:10]
        for n,seed in SCENARIOS:
            y=UMAP(n_components=2,n_neighbors=n,min_dist=.3,metric='euclidean',n_epochs=300,
                   random_state=seed,transform_seed=seed,n_jobs=1).fit_transform(x)
            dist=cdist(y,y);np.fill_diagonal(dist,np.inf);nn=np.argsort(dist,axis=1)[:,:10]
            recall=np.mean([len(set(a)&set(b))/10 for a,b in zip(true_nn,nn)])
            records.append(dict(n_neighbors=n,seed=seed,primary=n==15 and seed==42,
                trustworthiness_k10=float(trustworthiness(x,y,n_neighbors=10)),knn_recall_k10=float(recall)))
            if n==15 and seed==42:embedding=y.copy()
        assert embedding is not None
        d['UMAP_1']=embedding[:,0];d['UMAP_2']=embedding[:,1]
        d.to_csv(OUT/'umap_coordinates.csv',index=False)
        pd.DataFrame(records).to_csv(OUT/'umap_sensitivity.csv',index=False)
        cached.write_text(json.dumps(dict(plan_signature=signature,settings=plan,
            diagnostics=records,interpretation='Exploratory nonlinear profile layout; not full 3584-dimensional hidden states, causal evidence or independent emotion clusters.'),indent=2))
    d=pd.read_csv(OUT/'umap_coordinates.csv');style()
    fig,ax=plt.subplots(figsize=(180/25.4,140/25.4))
    fig.subplots_adjust(left=.14,right=.96,bottom=.23,top=.83)
    labels=['00 Reference','01 FA only','10 UN only','11 UN + FA']
    for c,label in zip(CONDITION_ORDER,labels):
        part=d[d.condition==c]
        ax.scatter(part.UMAP_1,part.UMAP_2,s=11,color=CONDITION_COLORS[c],marker='o',
                   alpha=.75,linewidths=.2,edgecolors='white',label=label)
    ax.set_xlabel('UMAP 1',fontsize=10);ax.set_ylabel('UMAP 2',fontsize=10)
    ax.tick_params(labelsize=8);ax.spines[['top','right']].set_visible(False)
    fig.text(.14,.94,'UMAP of item-level concept profiles',fontsize=11,weight='bold')
    fig.text(.14,.885,'Joint fit: 139 repeated items x 4 conditions; seven cosine-cosine similarity features',fontsize=7)
    handles=[Line2D([],[],marker='o',linestyle='none',color=CONDITION_COLORS[c],markersize=5,label=l) for c,l in zip(CONDITION_ORDER,labels)]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.55,.07),ncol=4,frameon=False,fontsize=7)
    fig.text(.14,.025,'Exploratory geometry; no inferred territory boundaries, density estimates or emotion-state labels.',fontsize=6.5)
    save(fig,OUT,'Concept_profile_UMAP_en',show)
    return OUT/'Concept_profile_UMAP_en.png'

if __name__=='__main__':build(False)
