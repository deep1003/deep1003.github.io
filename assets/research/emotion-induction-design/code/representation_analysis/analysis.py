"""Four fixed prompts: semantic embeddings, Qwen hidden states and exploratory emotion axes."""
from pathlib import Path
import fcntl, hashlib, json, os, time
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

BASE=Path(__file__).resolve().parent
SOURCE=BASE.parent/'results/a8e92be4014f'
SEMANTIC='intfloat/multilingual-e5-small'
SEMANTIC_REVISION='614241f622f53c4eeff9890bdc4f31cfecc418b3'
MODEL='Qwen/Qwen2.5-7B-Instruct'
REVISION='a09a35458c702b33eeacc393d103063234e8bc28'
LAYERS=[14,21,28]
LABELS={'UN':'UN 불확실성','FA':'FA 공포·불안','calm':'평온','sadness':'슬픔','anger':'분노','desperation':'절박함','joy':'기쁨'}
CONDITIONS=['UN0FA0','UN0FA1','UN1FA0','UN1FA1']

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write_json(path,value):
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');os.replace(temp,path)
def progress(**kw):write_json(BASE/'status.json',dict(time=time.time(),**kw))

def prepare():
    anchors=json.loads((BASE/'anchors.json').read_text())
    manifest=json.loads((SOURCE/'manifest.json').read_text())
    targets={k.replace('U','UN').replace('T','FA'):manifest['system']+'\n\n'+v for k,v in manifest['stimuli'].items()}
    cfg={'target_source_sha256':sha(SOURCE/'manifest.json'),'anchors_sha256':sha(BASE/'anchors.json'),
         'analysis_code_sha256':sha(__file__),'qwen_model':MODEL,'qwen_revision':REVISION,
         'dtype':'float32','attention':'eager','batch':1,'layers':LAYERS,'primary_layer':14,
         'semantic_encoder':SEMANTIC,'semantic_revision':SEMANTIC_REVISION,'semantic_prefix':'query: ',
         'axis_method':'training paired positive-minus-negative mean; unit direction; midpoint centering',
         'validation':'four heldout pairs: positive fraction >= .75 AND AUC >= .75; no adjustment after observations',
         'scaling':'projection divided by SD of pooled positive/negative training projections; not emotion probabilities',
         'pca':'PCA of the four fixed condition profiles on axes passing heldout gate; separate fit per representation; additional full-vector PCA',
         'qwen_position':'system-only message; add_generation_prompt=True; last token at assistant start; no KoBBQ',
         'limits':'Exploratory small authored anchor set; cross-context transfer from narrative anchors to operational notices; correlated axes; four target points only; no causal or population inference.'}
    key=hashlib.sha256(json.dumps(cfg,sort_keys=True).encode()).hexdigest()[:12]
    out=BASE/'results'/key;out.mkdir(parents=True,exist_ok=True)
    p=out/'manifest.json'
    if p.exists():assert json.loads(p.read_text())==cfg
    else:write_json(p,cfg)
    return anchors,targets,out

def encode_semantic(anchors,targets,out):
    p=out/'semantic.npz'
    if p.exists():return
    import torch
    from transformers import AutoTokenizer,AutoModel
    tok=AutoTokenizer.from_pretrained(SEMANTIC,revision=SEMANTIC_REVISION,local_files_only=True)
    model=AutoModel.from_pretrained(SEMANTIC,revision=SEMANTIC_REVISION,local_files_only=True).eval()
    texts=[v for r in anchors for v in [r['positive'],r['negative']]]+list(targets.values())
    vectors=[]
    for start in range(0,len(texts),16):
        enc=tok(['query: '+v for v in texts[start:start+16]],padding=True,truncation=False,return_tensors='pt')
        assert enc.input_ids.shape[1]<=512
        with torch.inference_mode():
            h=model(**enc).last_hidden_state
            v=(h*enc.attention_mask[...,None]).sum(1)/enc.attention_mask.sum(1)[:,None]
            vectors.extend(torch.nn.functional.normalize(v,dim=1).numpy())
    a=np.array(vectors);assert np.isfinite(a).all()
    np.savez_compressed(p,anchors=a[:-4].reshape(len(anchors),2,-1),targets=a[-4:])
    write_json(out/'semantic_runtime.json',{'model':SEMANTIC,'revision':getattr(model.config,'_commit_hash',None),'pooling':'attention-masked mean, L2-normalized','prefix':'query: '})
    del model

def encode_qwen(anchors,targets,out):
    import torch
    from transformers import AutoTokenizer,AutoModelForCausalLM
    files=out/'hidden';files.mkdir(exist_ok=True)
    plan=[(f'anchor_{i:03d}_{side}',text) for i,r in enumerate(anchors) for side,text in [('pos',r['positive']),('neg',r['negative'])]]
    source=json.loads((SOURCE/'manifest.json').read_text());system=source['system']
    plan=[(k,system+'\n\n'+v) for k,v in plan]+[(c,v) for c,v in targets.items()]
    done=sum((files/f'{k}.npy').exists() for k,_ in plan)
    if done<len(plan):
        progress(state='loading_qwen',completed=done,total=len(plan))
        tok=AutoTokenizer.from_pretrained(MODEL,revision=REVISION,local_files_only=True)
        device='mps' if torch.backends.mps.is_available() else 'cpu'
        # Transformers' optional single-block allocator warmup exceeds Metal's buffer limit.
        # Skip that reservation on MPS; parameters are loaded directly in unchanged FP32.
        import transformers.modeling_utils as modeling_utils
        original_warmup=modeling_utils.caching_allocator_warmup
        if device=='mps':modeling_utils.caching_allocator_warmup=lambda *args,**kwargs: None
        try:
            model=AutoModelForCausalLM.from_pretrained(MODEL,revision=REVISION,dtype=torch.float32,attn_implementation='eager',local_files_only=True,device_map={'':device},low_cpu_mem_usage=True).eval()
        finally:
            modeling_utils.caching_allocator_warmup=original_warmup
        write_json(out/'qwen_runtime.json',{'revision':getattr(model.config,'_commit_hash',None),'device':device,'dtype':'float32','torch':torch.__version__,'layers':LAYERS,'hidden_size':model.config.hidden_size})
        for i,(key,content) in enumerate(plan):
            path=files/f'{key}.npy'
            if path.exists():continue
            text=tok.apply_chat_template([{'role':'system','content':content}],tokenize=False,add_generation_prompt=True)
            enc=tok(text,return_tensors='pt').to(device)
            with torch.inference_mode():
                result=model(**enc,output_hidden_states=True,use_cache=False,logits_to_keep=1)
                v=np.array([result.hidden_states[layer][0,-1].float().cpu().numpy().copy() for layer in LAYERS])
            assert v.shape==(len(LAYERS),model.config.hidden_size) and np.isfinite(v).all()
            np.save(path,v);del result
            done+=1;progress(state='measuring_qwen',completed=done,total=len(plan),last_key=key,out=str(out))
            if done%10==0 or done==len(plan):print(f'Qwen {done}/{len(plan)}',flush=True)
        del model
        if device=='mps':torch.mps.empty_cache()
    a=np.array([[np.load(files/f'anchor_{i:03d}_{s}.npy') for s in ['pos','neg']] for i in range(len(anchors))])
    target=np.array([np.load(files/f'{c}.npy') for c in targets])
    np.savez_compressed(out/'qwen.npz',anchors=a,targets=target)

def score_space(name,anchor_vectors,target_vectors,anchors,out):
    axes=list(LABELS);scores=[];checks=[];directions=[];centers=[];scales=[]
    for axis in axes:
        train=np.array([i for i,r in enumerate(anchors) if r['axis']==axis and r['split']=='train'])
        test=np.array([i for i,r in enumerate(anchors) if r['axis']==axis and r['split']=='heldout'])
        pos,neg=anchor_vectors[train,0],anchor_vectors[train,1]
        direction=(pos-neg).mean(0);norm=np.linalg.norm(direction);assert norm>1e-9;direction/=norm
        center=np.concatenate([pos,neg]).mean(0)
        scale=np.std((np.concatenate([pos,neg])-center)@direction,ddof=1);assert scale>1e-9
        pp=(anchor_vectors[test,0]-center)@direction;nn=(anchor_vectors[test,1]-center)@direction
        fraction=float(np.mean(pp>nn));auc=float(np.mean((pp[:,None]>nn[None,:])+.5*(pp[:,None]==nn[None,:])))
        passed=fraction>=.75 and auc>=.75
        checks.append({'space':name,'axis':axis,'heldout_pairs':len(test),'paired_accuracy':fraction,'auc':auc,'passed':passed})
        directions.append(direction);centers.append(center);scales.append(scale)
        for cond,v in zip(CONDITIONS,target_vectors):
            delta=v-center;raw=float(delta@direction);cos=raw/float(np.linalg.norm(delta))
            scores.append({'space':name,'condition':cond,'axis':axis,'label':LABELS[axis],'cosine':cos,'projection':raw,'standardized':raw/scale,'passed':passed})
    pd.DataFrame(directions@np.array(directions).T,index=axes,columns=axes).to_csv(out/f'axis_cosines_{name}.csv')
    np.savez_compressed(out/f'axes_{name}.npz',directions=directions,centers=centers,scales=scales)
    return pd.DataFrame(scores),pd.DataFrame(checks)

def fit_pca(matrix,conditions):
    pca=PCA(n_components=2,svd_solver='full');xy=pca.fit_transform(matrix)
    # Stable display sign, without modifying distances or variance.
    for j in range(2):
        if xy[-1,j]<xy[0,j]:xy[:,j]*=-1;pca.components_[j]*=-1
    rows=[{'condition':c,'PC1':float(v[0]),'PC2':float(v[1])} for c,v in zip(conditions,xy)]
    from scipy.spatial.distance import pdist
    d=pdist(matrix);d2=pdist(xy)
    stress=float(np.sqrt(np.sum((d-d2)**2)/np.sum(d**2)))
    return rows,{'explained_variance_ratio':pca.explained_variance_ratio_.tolist(),'retained_variance':float(pca.explained_variance_ratio_.sum()),'distance_stress':stress,'components':pca.components_.tolist()}

def analyze(out):
    anchors,targets,expected=prepare();assert Path(out)==expected
    semantic=np.load(out/'semantic.npz');qwen=np.load(out/'qwen.npz')
    all_scores=[];all_checks=[];embedding_pca={};profile_pca={}
    spaces={'semantic':(semantic['anchors'],semantic['targets'])}
    for i,layer in enumerate(LAYERS):spaces[f'qwen_L{layer}']=(qwen['anchors'][:,:,i,:],qwen['targets'][:,i,:])
    for name,(a,t) in spaces.items():
        scores,checks=score_space(name,a,t,anchors,out);all_scores.append(scores);all_checks.append(checks)
        rows,stats=fit_pca(t,CONDITIONS);embedding_pca[name]={'coordinates':rows,**stats}
        keep=checks.loc[checks.passed,'axis'].tolist()
        if len(keep)>=2:
            v=scores.pivot(index='condition',columns='axis',values='standardized').reindex(index=CONDITIONS,columns=keep)
            rows,stats=fit_pca(v.to_numpy(),CONDITIONS);profile_pca[name]={'axes':keep,'coordinates':rows,**stats}
        else:profile_pca[name]={'axes':keep,'unavailable':'Fewer than two independently heldout-passing axes.'}
    scores=pd.concat(all_scores);checks=pd.concat(all_checks);scores.to_csv(out/'scores.csv',index=False);checks.to_csv(out/'heldout_checks.csv',index=False)
    write_json(out/'embedding_pca.json',embedding_pca);write_json(out/'profile_pca.json',profile_pca)
    write_json(out/'summary.json',{'conditions':CONDITIONS,'n_target_prompts':4,'n_anchor_pairs':70,'qwen_forward_inputs':144,'primary_layer':14,'profile_pca':profile_pca,'embedding_pca':embedding_pca,'limits':json.loads((out/'manifest.json').read_text())['limits']})
    return scores,checks

def plot(out,show=False):
    import matplotlib
    if not show:matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    plt.rcParams.update({'font.family':'AppleGothic','axes.unicode_minus':False,'svg.fonttype':'path','pdf.fonttype':42})
    out=Path(out);scores=pd.read_csv(out/'scores.csv');checks=pd.read_csv(out/'heldout_checks.csv')
    colours={'UN0FA0':'#a5bed8','UN0FA1':'#dbc68e','UN1FA0':'#416e9b','UN1FA1':'#a8832b'}
    markers={'UN0FA0':'o','UN0FA1':'s','UN1FA0':'o','UN1FA1':'s'}
    names={'semantic':'문구의 의미 표현','qwen_L14':'7B 내부 표현 · 14층'}
    for kind,title in [('profile_pca','정서·불확실성 점수의 PCA'),('embedding_pca','전체 표현 벡터의 PCA')]:
        data=json.loads((out/f'{kind}.json').read_text());fig,axs=plt.subplots(1,2,figsize=(11,4.8),layout='constrained')
        for ax,space in zip(axs,names):
            result=data[space]
            if 'coordinates' not in result:ax.text(.5,.5,'검증 통과 축 부족',ha='center');continue
            xy=pd.DataFrame(result['coordinates']).set_index('condition')
            for a,b in [('UN0FA0','UN1FA0'),('UN0FA1','UN1FA1')]:ax.plot(xy.loc[[a,b],'PC1'],xy.loc[[a,b],'PC2'],color='#c5c5c5',lw=1,zorder=1)
            for c,row in xy.iterrows():
                ax.scatter(row.PC1,row.PC2,s=95,color=colours[c],marker=markers[c],edgecolor='#333',linewidth=.5,zorder=3)
                ax.annotate(c,(row.PC1,row.PC2),xytext=(7,7),textcoords='offset points',fontsize=10)
            ratios=result['explained_variance_ratio'];ax.set(xlabel=f'PC1 ({ratios[0]:.1%})',ylabel=f'PC2 ({ratios[1]:.1%})',title=names[space]+f"\n2차원 보존 분산 {result['retained_variance']:.1%}")
            ax.margins(.35);ax.axhline(0,color='#ddd',lw=.6);ax.axvline(0,color='#ddd',lw=.6);ax.spines[['top','right']].set_visible(False)
        fig.suptitle(title+' · 네 고정 프롬프트',fontsize=13)
        for ext in ['png','svg','pdf']:fig.savefig(out/f'{kind}.{ext}',dpi=200)
        if show:plt.show()
        plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(12,5),layout='constrained');cmap=LinearSegmentedColormap.from_list('blue_gold',['#6588ad','#ffffff','#bb9950'])
    axes=list(LABELS)
    visible=scores[scores.space.isin(names)];vmax=max(1,float(visible.standardized.abs().max()))
    for ax,space in zip(axs,names):
        mat=scores[scores.space==space].pivot(index='condition',columns='axis',values='standardized').reindex(index=CONDITIONS,columns=axes)
        im=ax.imshow(mat,cmap=cmap,vmin=-vmax,vmax=vmax,aspect='auto')
        ax.set(xticks=range(len(axes)),xticklabels=[LABELS[x] for x in axes],yticks=range(4),yticklabels=CONDITIONS,title=names[space]);ax.tick_params(axis='x',rotation=45)
        valid=checks[checks.space==space].set_index('axis').passed
        for i in range(4):
            for j,a in enumerate(axes):ax.text(j,i,f'{mat.iloc[i,j]:+.2f}'+('' if valid[a] else '*'),ha='center',va='center',fontsize=9,color='#222')
    fig.colorbar(im,ax=axs,label='기준 문장 대비 표준화 투영값 · 축별 기준 척도');fig.suptitle('정서 개념의 동시 유사도 · *는 보류 문장 검증 실패')
    for ext in ['png','svg','pdf']:fig.savefig(out/f'emotion_heatmap.{ext}',dpi=200)
    if show:plt.show()
    plt.close(fig)
    return out

def run():
    anchors,targets,out=prepare()
    with open(BASE/'writer.lock','a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        progress(state='semantic',out=str(out));encode_semantic(anchors,targets,out)
        encode_qwen(anchors,targets,out);analyze(out);plot(out)
        progress(state='complete',out=str(out));print('COMPLETE',out,flush=True)
    return out

if __name__=='__main__':run()
