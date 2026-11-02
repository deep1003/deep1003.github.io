# Exploratory moderation model for Llama-3.1-8B-Instruct (v5 cohort, 576 ambiguous KoBBQ items, L16, 11-axis anchor directions)
# Same estimator as the audited v11 Qwen script: raw probabilities for pp, clipping only for logit; 2,000 cluster draws, seed 20261101.
import sys,json,numpy as np,pandas as pd
from scipy.stats import rankdata,spearmanr
T=pd.read_csv(sys.argv[1]); chk=pd.read_csv(sys.argv[2])
NEG=['t2_Fear','t2_Anxiety','t2_Sadness','t2_Anger','t2_Disgust','t2_Desperation']; POS=['t2_Calmness','t2_Joy']
T['V']=T[NEG].mean(axis=1)-T[POS].mean(axis=1)
T=T[T['item'].str.contains('-amb-')]
g=T.groupby(['item','condition']).agg(V=('V','mean'),p=('p_unknown','mean'),cl=('cluster','first'),cat=('category','first')).reset_index()
W=g.pivot(index='item',columns='condition',values=['V','p'])
meta=g.drop_duplicates('item').set_index('item')[['cl','cat']]
# reproduction check against report table (CN1-CN0 Valence and p_unknown)
d=(W['V']['CN1']-W['V']['CN0']).rename('dV'); m=chk.set_index('item')
print('repro dV corr',np.corrcoef(d.loc[m.index],m['Valence'])[0,1],'max abs diff',float((d.loc[m.index]-m['Valence']).abs().max()), 'dp maxdiff',float(((W['p']['CN1']-W['p']['CN0']).loc[m.index]-m['p_unknown']).abs().max()))
rng=np.random.default_rng(20261101)
zs=lambda v:(v-v.mean())/v.std()
def ols(idx,V,Y0,dY):
    v,y0=zs(V[idx]),zs(Y0[idx]); X=np.c_[np.ones(len(idx)),v,y0,v*y0]
    return np.linalg.lstsq(X,dY[idx]/dY[idx].std(),rcond=None)[0][1:]
def pcor(idx,a,b,c):
    ra,rb,rc=rankdata(a[idx]),rankdata(b[idx]),rankdata(c[idx]); X=np.c_[np.ones(len(idx)),rc]
    ea=ra-X@np.linalg.lstsq(X,ra,rcond=None)[0]; eb=rb-X@np.linalg.lstsq(X,rb,rcond=None)[0]
    return np.corrcoef(ea,eb)[0,1]
def sp(idx,a,b): return spearmanr(a[idx],b[idx])[0]
def boot(fn,c,B=2000):
    c=np.array(c); u=np.unique(c); ix={k:np.where(c==k)[0] for k in u}
    est=np.atleast_1d(fn(np.arange(len(c)))); bs=np.array([np.atleast_1d(fn(np.concatenate([ix[k] for k in rng.choice(u,len(u))]))) for _ in range(B)])
    lo,hi=np.percentile(bs,[2.5,97.5],axis=0); p=2*np.minimum((bs<=0).mean(0),(bs>=0).mean(0))
    return est,lo,hi,np.maximum(p,1/B),len(u)
out={}
for c1,c0,lab in [('CN1','CN0','d_TERM|CLOSED'),('UN1','UN0','d_TERM|OPEN')]:
    items=W.index[W['p'][[c1,c0]].notna().all(1)]
    c=meta.loc[items,'cl'].values
    V0=W['V'][c0].loc[items].values; V1=W['V'][c1].loc[items].values; dV=V1-V0
    P0=W['p'][c0].loc[items].values; P1=W['p'][c1].loc[items].values
    clip=lambda p:np.clip(p,1e-6,1-1e-6); lg=lambda p:np.log(clip(p)/(1-clip(p)))
    for yl,Y0,Y1 in [('pp',100*P0,100*P1),('logit',lg(P0),lg(P1))]:
        dY=Y1-Y0
        r=boot(lambda ix:sp(ix,dV,dY),c); b=boot(lambda ix:ols(ix,V0,Y0,dY),c); p1=boot(lambda ix:pcor(ix,dV,dY,Y0),c)
        name=f'kobbq {lab} {yl}'
        print('==',name,'n',len(items),'clusters',b[4],'mean dY %.4f'%dY.mean())
        print('   rho(dV,dY) %+.3f [%+.3f, %+.3f]'%(r[0][0],r[1][0],r[2][0]))
        print('   partial rho %+.3f [%+.3f, %+.3f]'%(p1[0][0],p1[1][0],p1[2][0]))
        for j,t in enumerate(['b1','b2','b3']): print('   %s %+.3f [%+.3f, %+.3f] p=%.4f'%(t,b[0][j],b[1][j],b[2][j],b[3][j]))
        out[name]=dict(n=len(items),clusters=int(b[4]),rho=[float(r[k][0]) for k in range(3)],partial=[float(p1[k][0]) for k in range(3)],coef=[list(map(float,x)) for x in b[:4]])
json.dump(out,open('moderation_llama_v5.json','w'),indent=1)
