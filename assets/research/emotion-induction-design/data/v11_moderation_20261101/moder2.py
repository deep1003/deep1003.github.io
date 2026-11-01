# Moderation model, v11 Round 1, Qwen2.5-7B-Instruct, L19 decision position. Exploratory, post hoc.
# Model per item i:  dY_i = b0 + b1 z(V_keep) + b2 z(Y_keep) + b3 z(V_keep)*z(Y_keep) + e
#   V_keep = valence index under KEEP; Y_keep = baseline outcome under KEEP; dY = TERM - KEEP.
# Also partial Spearman rho(dV, dY | Y_keep) and rho(V_keep, dY | Y_keep).
import json, numpy as np
from collections import defaultdict
from scipy.stats import rankdata
D='/Users/deep1003/Library/Mobile Documents/com~apple~CloudDocs/data3/fear_in_the_machine_v7_qwen_20261028/24_final_experiment_20261031/v11/round1_main_qwen'
z=np.load(D+'/02_vectors/fitted_v2/instrument_L19.npz', allow_pickle=True)
AU=z['axes_unit'].astype(np.float64)
H=np.load(D+'/03_raw/behavior/L19.npy', mmap_mode='r')
A=defaultdict(lambda: defaultdict(list)); clu={}
for l in open('/tmp/v11peek/round1_main_qwen_03_raw_behavior_trials.jsonl'):
    r=json.loads(l)
    if r['condition'] not in ('CN1','CN0','UN1','UN0'): continue
    m=r['metadata']
    if r['task']=='kobbq' and not m['ambiguous']: continue
    pe=AU@np.asarray(H[r['activation']['row']],dtype=np.float64)
    sc=r['scores']['conditional']
    if r['task']=='kobbq':
        p=min(max(sc[m['unknown_key']],1e-6),1-1e-6); y=(100*p, np.log(p/(1-p)))
    else:
        a=np.log(sc['yes'])-np.log(sc['no']); y=(a,a)
    A[(r['task'],r['item_id'])][r['condition']].append((pe[:6].mean()-pe[6:].mean(),)+y)
    clu[(r['task'],r['item_id'])]=r['cluster_id'] if r['task']=='kobbq' else str(m['question_id'])
rng=np.random.default_rng(20261101)
zs=lambda v:(v-v.mean())/v.std()
def ols(idx,V,Y0,dY):
    v,y0=zs(V[idx]),zs(Y0[idx]); X=np.c_[np.ones(len(idx)),v,y0,v*y0]
    return np.linalg.lstsq(X,dY[idx]/dY[idx].std(),rcond=None)[0][1:]
def pcor(idx,a,b,c):
    ra,rb,rc=rankdata(a[idx]),rankdata(b[idx]),rankdata(c[idx]); X=np.c_[np.ones(len(idx)),rc]
    ea=ra-X@np.linalg.lstsq(X,ra,rcond=None)[0]; eb=rb-X@np.linalg.lstsq(X,rb,rcond=None)[0]
    return np.corrcoef(ea,eb)[0,1]
def boot(fn,c,B=2000):
    c=np.array(c); u=np.unique(c); ix={k:np.where(c==k)[0] for k in u}
    est=np.array(fn(np.arange(len(c)))); bs=np.array([fn(np.concatenate([ix[k] for k in rng.choice(u,len(u))])) for _ in range(B)])
    lo,hi=np.percentile(bs,[2.5,97.5],axis=0); p=2*np.minimum((bs<=0).mean(0),(bs>=0).mean(0))
    return est,lo,hi,np.maximum(p,1/B),len(u)
out={}
for task,cols in [('kobbq',[(1,'Unknown selection, pp'),(2,'Unknown selection, logit')]),('discrimeval',[(1,'approval tendency')])]:
  for c1,c0,lab in [('CN1','CN0','d_TERM|CLOSED'),('UN1','UN0','d_TERM|OPEN')]:
    keys=[k for k in A if k[0]==task and c1 in A[k] and c0 in A[k]]
    c=[clu[k] for k in keys]
    for col,yl in cols:
        V0=np.array([np.mean([t[0] for t in A[k][c0]]) for k in keys]); V1=np.array([np.mean([t[0] for t in A[k][c1]]) for k in keys])
        Y0=np.array([np.mean([t[col] for t in A[k][c0]]) for k in keys]); Y1=np.array([np.mean([t[col] for t in A[k][c1]]) for k in keys])
        dY=Y1-Y0; dV=V1-V0
        b=boot(lambda ix: ols(ix,V0,Y0,dY),c)
        p1=boot(lambda ix: [pcor(ix,dV,dY,Y0)],c)
        p2=boot(lambda ix: [pcor(ix,V0,dY,Y0)],c)
        name='%s %s %s'%(task,lab,yl)
        print('==',name,'n items',len(keys),'clusters',b[4],'mean dY %.4f'%dY.mean())
        for j,t in enumerate(['b1 valence(KEEP)','b2 baseline outcome','b3 valence x baseline']):
            print('   %-24s %+.3f [%+.3f, %+.3f] p=%.4f'%(t,b[0][j],b[1][j],b[2][j],b[3][j]))
        print('   partial rho(dV, dY | baseline)       %+.3f [%+.3f, %+.3f] p=%.4f'%(p1[0][0],p1[1][0],p1[2][0],p1[3][0]))
        print('   partial rho(V_keep, dY | baseline)   %+.3f [%+.3f, %+.3f] p=%.4f'%(p2[0][0],p2[1][0],p2[2][0],p2[3][0]))
        out[name]=dict(n=len(keys),clusters=int(b[4]),coef=[list(map(float,x)) for x in b[:4]],pc_dV=[float(x[0]) for x in p1[:4]],pc_V0=[float(x[0]) for x in p2[:4]])
json.dump(out,open('/tmp/valcorr/moderation_v11_qwen.json','w'),indent=1)
