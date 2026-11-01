import json, numpy as np
from collections import defaultdict
D='/Users/deep1003/Library/Mobile Documents/com~apple~CloudDocs/data3/fear_in_the_machine_v7_qwen_20261028/24_final_experiment_20261031/v11/round1_main_qwen'
z=np.load(D+'/02_vectors/fitted_v2/instrument_L19.npz', allow_pickle=True); AU=z['axes_unit'].astype(np.float64)
H=np.load(D+'/03_raw/behavior/L19.npy', mmap_mode='r')
A=defaultdict(lambda: defaultdict(list))
for l in open('/tmp/v11peek/round1_main_qwen_03_raw_behavior_trials.jsonl'):
    r=json.loads(l)
    if r['condition'] not in ('CN1','CN0'): continue
    m=r['metadata']
    if r['task']=='kobbq' and not m['ambiguous']: continue
    pe=AU@np.asarray(H[r['activation']['row']],dtype=np.float64); sc=r['scores']['conditional']
    y=100*sc[m['unknown_key']] if r['task']=='kobbq' else np.log(sc['yes'])-np.log(sc['no'])
    A[(r['task'],r['item_id'])][r['condition']].append((pe[:6].mean()-pe[6:].mean(),y))
out={}
for task in ['kobbq','discrimeval']:
    ks=[k for k in A if k[0]==task]
    dv=np.array([np.mean([t[0] for t in A[k]['CN1']])-np.mean([t[0] for t in A[k]['CN0']]) for k in ks])
    dy=np.array([np.mean([t[1] for t in A[k]['CN1']])-np.mean([t[1] for t in A[k]['CN0']]) for k in ks])
    q=np.quantile(dv,np.linspace(0,1,11)); b=np.clip(np.searchsorted(q,dv,side='right')-1,0,9)
    out[task]=[[float(dv[b==i].mean()),float(dy[b==i].mean()),float(dy[b==i].std(ddof=1)/np.sqrt((b==i).sum())),int((b==i).sum())] for i in range(10)]
print(json.dumps(out))
