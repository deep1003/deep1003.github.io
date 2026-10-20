"""Default: saved data and hashes only. Explicit flags run saved-data analysis/rendering."""
from pathlib import Path
import argparse,json,hashlib
import pandas as pd,numpy as np
BASE=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--analyze',action='store_true')
p.add_argument('--render',action='store_true')
args=p.parse_args()
b=pd.read_csv(BASE/'data/behavior_6_conditions.csv')
assert len(b)==2502 and b.item.nunique()==139 and not b.duplicated(['item','condition','rotation']).any()
assert b.groupby(['item','condition']).size().eq(3).all()
assert set(b.condition)=={'U0T0','U0T1','U1T0','U1T1','C1T0','C1T1'}
assert np.isfinite(b[['p_unknown','p_stereotype','p_anti']]).all().all()
assert np.allclose(b[['p_unknown','p_stereotype','p_anti']].sum(axis=1),1,atol=1e-6)
if (BASE/'CHECKSUMS.json').exists():
 for name,digest in json.loads((BASE/'CHECKSUMS.json').read_text()).items():assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==digest,name
print('139 items / six conditions / 2502 keys verified. No model inference.')
if args.analyze or args.render:
 source=(BASE/'reproduce_analysis.py').read_text()
 if not args.render:source=source[:source.index('plt.rcParams.update')]
 exec(compile(source,'reproduce_analysis.py','exec'),{'__file__':str(BASE/'reproduce_analysis.py')})

if args.render:
 import subprocess,sys
 subprocess.run([sys.executable,str(BASE/'reproduce_tables.py')],check=True)
 subprocess.run([sys.executable,str(BASE/'render_restored_figures.py')],check=True)

if args.render:
 import subprocess,sys
 subprocess.run([sys.executable,str(BASE/'reproduce_tables.py')],check=True)
 subprocess.run([sys.executable,str(BASE/'render_restored_figures.py')],check=True)

if args.render:
 import subprocess,sys
 subprocess.run([sys.executable,str(BASE/'reproduce_tables.py')],check=True)
 subprocess.run([sys.executable,str(BASE/'render_restored_figures.py')],check=True)
