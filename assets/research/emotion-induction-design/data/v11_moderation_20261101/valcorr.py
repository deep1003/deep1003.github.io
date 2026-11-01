# Exploratory, post hoc: item-level valence-index correlation, v11 Round 1, Qwen2.5-7B-Instruct, L19 decision position
import json, numpy as np, sys
from collections import defaultdict
from scipy.stats import spearmanr, rankdata
D='/Users/deep1003/Library/Mobile Documents/com~apple~CloudDocs/data3/fear_in_the_machine_v7_qwen_20261028/24_final_experiment_20261031/v11/round1_main_qwen'
z=np.load(D+'/02_vectors/fitted_v2/instrument_L19.npz', allow_pickle=True)
AU=z['axes_unit'].astype(np.float64); VAL=z['VAL_unit'].astype(np.float64); GENu=z['GEN_raw_unit'].astype(np.float64)
H=np.load(D+'/03_raw/behavior/L19.npy', mmap_mode='r')
print('H', H.shape, H.dtype)
recs=[]
for l in open('/tmp/v11peek/round1_main_qwen_03_raw_behavior_trials.jsonl'):
    r=json.loads(l)
    if r['condition'] not in ('CN1','CN0','UN1','UN0'): continue
    m=r['metadata']; row=r['activation']['row']
    h=np.asarray(H[row],dtype=np.float64)
    pe=AU@h
    d=dict(task=r['task'],cond=r['condition'],item=r['item_id'],clu=r['cluster_id'],
           vidx=pe[:6].mean()-pe[6:].mean(), val=float(VAL@h), gen=float(GENu@h), pe=pe,
           neg=r['readouts']['NEG'], genro=r['readouts']['GEN'])
    sc=r['scores']['conditional']
    if r['task']=='kobbq':
        d['amb']=m['ambiguous']; d['cat']=m['category']; d['unk']=sc[m['unknown_key']]
        d['ster']=sc[m['stereotype_key']]; d['anti']=sc[m['anti_key']]
    else:
        d['amb']=None; d['cat']='discrimeval'; d['item']=r['item_id']
        d['apr']=np.log(sc['yes'])-np.log(sc['no']); d['clu']=str(m['question_id'])
    recs.append(d)
print('n recs', len(recs))
def agg(task, filt):
    A=defaultdict(lambda: defaultdict(list)); meta={}
    for d in recs:
        if d['task']!=task or not filt(d): continue
        A[d['item']][d['cond']].append(d); meta[d['item']]=(d['clu'],d['cat'])
    return A, meta
def mean_field(lst,f): return float(np.mean([x[f] for x in lst])) if f!='pe' else np.mean([x['pe'] for x in lst],axis=0)
def deltas(A, meta, c1, c0, ycol, fields=('vidx','val','gen','neg','pe')):
    out=[]
    for it,cd in A.items():
        if c1 in cd and c0 in cd:
            row={'item':it,'clu':meta[it][0],'cat':meta[it][1],'dy':mean_field(cd[c1],ycol)-mean_field(cd[c0],ycol)}
            for f in fields: row['d'+f]=mean_field(cd[c1],f)-mean_field(cd[c0],f)
            out.append(row)
    return out
rng=np.random.default_rng(20261101)
def boot_rho(x,y,clu,B=2000,fn=None):
    fn=fn or (lambda a,b,idx: spearmanr(a[idx],b[idx])[0])
    clu=np.asarray(clu); uc=np.unique(clu); idxs={c:np.where(clu==c)[0] for c in uc}
    est=fn(x,y,np.arange(len(x))); bs=[]
    for _ in range(B):
        s=rng.choice(uc,len(uc),replace=True); ii=np.concatenate([idxs[c] for c in s])
        bs.append(fn(x,y,ii))
    bs=np.array(bs); lo,hi=np.nanpercentile(bs,[2.5,97.5])
    p=2*min(np.mean(bs<=0),np.mean(bs>=0)); return est,lo,hi,max(p,1/B),len(uc)
def partial_fn(zc):
    def f(a,b,idx):
        ra,rb,rz=rankdata(a[idx]),rankdata(b[idx]),rankdata(zc[idx])
        X=np.c_[np.ones(len(idx)),rz]
        ea=ra-X@np.linalg.lstsq(X,ra,rcond=None)[0]; eb=rb-X@np.linalg.lstsq(X,rb,rcond=None)[0]
        return np.corrcoef(ea,eb)[0,1]
    return f
EMO=list(z['emotion_order'])
def report(name, rows, ylab, scale=1.0):
    x=np.array([r['dvidx'] for r in rows]); y=np.array([r['dy'] for r in rows])*scale; c=[r['clu'] for r in rows]
    v=np.array([r['dval'] for r in rows]); g=np.array([r['dgen'] for r in rows])
    print('==',name,'n items',len(rows),'mean d(valence index) %.4f'%x.mean(),'mean d',ylab,'%.4f'%y.mean())
    e=boot_rho(x,y,c); print('  rho(valence index, d%s) = %.3f [%.3f, %.3f] p_boot=%.4f clusters=%d'%(ylab,*e))
    e=boot_rho(v,y,c); print('  rho(VAL_unit NEG-minus-POS, d%s) = %.3f [%.3f, %.3f] p=%.4f'%(ylab,*e[:4]))
    e=boot_rho(x,y,c,fn=partial_fn(g)); print('  partial rho | d general emotionality = %.3f [%.3f, %.3f] p=%.4f'%e[:4])
    pe=np.array([r['dpe'] for r in rows])
    print('  single directions:', ', '.join('%s %.2f'%(EMO[k],spearmanr(pe[:,k],y)[0]) for k in range(8)))
    cats=sorted(set(r['cat'] for r in rows))
    if len(cats)>1:
        pos=0
        for ct in cats:
            ii=[i for i,r in enumerate(rows) if r['cat']==ct]
            rr=spearmanr(x[ii],y[ii])[0]; pos+=rr>0
            print('    %-28s n=%3d rho=%.2f'%(ct,len(ii),rr))
        print('  positive categories: %d of %d'%(pos,len(cats)))
    return x,y,c
A,meta=agg('kobbq', lambda d: d['amb'])
print('KoBBQ ambiguous items', len(A))
for c1,c0,nm in [('CN1','CN0','KoBBQ amb  d_TERM|CLOSED'),('UN1','UN0','KoBBQ amb  d_TERM|OPEN')]:
    report(nm, deltas(A,meta,c1,c0,'unk'), 'P(unknown) pp', 100)
# interaction contrast
r1=deltas(A,meta,'CN1','CN0','unk'); r0={r['item']:r for r in deltas(A,meta,'UN1','UN0','unk')}
ri=[dict(item=r['item'],clu=r['clu'],cat=r['cat'],dy=r['dy']-r0[r['item']]['dy'],dvidx=r['dvidx']-r0[r['item']]['dvidx'],dval=r['dval']-r0[r['item']]['dval'],dgen=r['dgen']-r0[r['item']]['dgen'],dpe=r['dpe']-r0[r['item']]['dpe']) for r in r1 if r['item'] in r0]
report('KoBBQ amb  d_StatusxOutcome', ri, 'P(unknown) pp', 100)
A2,meta2=agg('discrimeval', lambda d: True)
print('DiscrimEval items', len(A2))
for c1,c0,nm in [('CN1','CN0','DiscrimEval d_TERM|CLOSED'),('UN1','UN0','DiscrimEval d_TERM|OPEN')]:
    report(nm, deltas(A2,meta2,c1,c0,'apr'), 'approval tendency')
