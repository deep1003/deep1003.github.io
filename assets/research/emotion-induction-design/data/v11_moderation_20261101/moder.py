import json, numpy as np
from collections import defaultdict
from scipy.stats import spearmanr
D='/Users/deep1003/Library/Mobile Documents/com~apple~CloudDocs/data3/fear_in_the_machine_v7_qwen_20261028/24_final_experiment_20261031/v11/round1_main_qwen'
z=np.load(D+'/02_vectors/fitted_v2/instrument_L19.npz', allow_pickle=True)
AU=z['axes_unit'].astype(np.float64); GEN=z['GEN_raw_unit'].astype(np.float64)
H=np.load(D+'/03_raw/behavior/L19.npy', mmap_mode='r')
A=defaultdict(lambda: defaultdict(list)); clu={}
for l in open('/tmp/v11peek/round1_main_qwen_03_raw_behavior_trials.jsonl'):
    r=json.loads(l)
    if r['condition'] not in ('CN1','CN0','UN1','UN0'): continue
    m=r['metadata']
    if r['task']=='kobbq' and not m['ambiguous']: continue
    h=np.asarray(H[r['activation']['row']],dtype=np.float64); pe=AU@h
    sc=r['scores']['conditional']
    y=sc[m['unknown_key']] if r['task']=='kobbq' else np.log(sc['yes'])-np.log(sc['no'])
    A[(r['task'],r['item_id'])][r['condition']].append((pe[:6].mean()-pe[6:].mean(), float(GEN@h), y))
    clu[(r['task'],r['item_id'])]=r['cluster_id'] if r['task']=='kobbq' else str(m['question_id'])
rng=np.random.default_rng(1)
def boot(x,y,c,B=2000):
    c=np.array(c); u=np.unique(c); idx={k:np.where(c==k)[0] for k in u}; bs=[]
    for _ in range(B):
        ii=np.concatenate([idx[k] for k in rng.choice(u,len(u))]); bs.append(spearmanr(x[ii],y[ii])[0])
    return spearmanr(x,y)[0], *np.percentile(bs,[2.5,97.5])
for task in ['kobbq','discrimeval']:
  for c1,c0 in [('CN1','CN0'),('UN1','UN0')]:
    keys=[k for k in A if k[0]==task and c1 in A[k] and c0 in A[k]]
    b=np.array([np.mean([t[0] for t in A[k][c0]]) for k in keys])
    g=np.array([np.mean([t[1] for t in A[k][c0]]) for k in keys])
    y0=np.array([np.mean([t[2] for t in A[k][c0]]) for k in keys])
    dy=np.array([np.mean([t[2] for t in A[k][c1]]) for k in keys])-y0
    c=[clu[k] for k in keys]
    print(task,c1,'-',c0,'n',len(keys))
    print('  moderation: rho(baseline valence at KEEP, d outcome) = %.3f [%.3f, %.3f]'%boot(b,dy,c))
    print('  rho(baseline general emotionality, d outcome) = %.3f [%.3f, %.3f]'%boot(g,dy,c))
    print('  check: rho(baseline outcome, d outcome) = %.3f [%.3f, %.3f]'%boot(y0,dy,c))
    print('  rho(baseline valence, baseline outcome) = %.3f'%spearmanr(b,y0)[0])
