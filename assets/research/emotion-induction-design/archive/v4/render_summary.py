"""Render descriptive v4 A/B summaries from frozen records, without model inference."""
from pathlib import Path
import csv
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
with (ROOT / 'threat_ab_t2.csv').open() as f:
    trials = list(csv.DictReader(f))
with (ROOT / 'threat_ab_t1.csv').open() as f:
    endpoints = {r['condition']: r for r in csv.DictReader(f)}
rows = []
for family, state in [('A', 'UN'), ('A', 'CN'), ('B', 'UN'), ('B', 'CN')]:
    c0, c1 = f'{family}_{state}0', f'{family}_{state}1'
    zero = {(r['item'], r['rotation']): float(r['p_unknown']) for r in trials if r['condition'] == c0}
    one = {(r['item'], r['rotation']): float(r['p_unknown']) for r in trials if r['condition'] == c1}
    assert set(zero) == set(one) and len(zero) == 417
    delta = float(np.mean([one[k] - zero[k] for k in sorted(zero)]) * 100)
    fear = (float(endpoints[c1]['t1_Fear']) - float(endpoints[c0]['t1_Fear'])) * 1000
    rows.append({'family': family, 'state': state, 'behavior_change_pp': delta, 'fear_cosine_change_x1000': fear})
with (ROOT / 'descriptive_summary.csv').open('w') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'svg.fonttype': 'none', 'axes.spines.top': False, 'axes.spines.right': False})
fig, axes = plt.subplots(1, 2, figsize=(12, 4.9), gridspec_kw={'width_ratios': [1.13, 1]}, layout='constrained')
y = np.arange(4)
labels = ['A · Undecided', 'A · Confirmed', 'B (v4) · Undecided', 'B (v4) · Confirmed']
for ax in axes:
    ax.axvline(0, color='#9AA5AB', ls=':', lw=1)
    ax.set_yticks(y, labels)
    ax.set_ylim(3.6, -0.8)
    ax.tick_params(axis='y', length=0, pad=10)
    ax.spines['left'].set_visible(False)
    ax.grid(axis='x', color='#e9ecef', lw=.7)
    ax.set_axisbelow(True)
axes[0].scatter([r['behavior_change_pp'] for r in rows], y, color=['#8396A5']*2 + ['#244C67']*2, s=65, zorder=3)
for i,r in enumerate(rows):
    axes[0].annotate(f"{r['behavior_change_pp']:+.2f}",(r['behavior_change_pp'],i),xytext=(0,12),textcoords='offset points',ha='center',fontsize=11)
axes[0].set_xlim(-1.75,1.25)
axes[0].set_xlabel('Change in P(unknown)\n(percentage points)')
axes[0].set_title('a  Social judgment', loc='left', fontsize=14, fontweight='bold', pad=18)
axes[1].scatter([r['fear_cosine_change_x1000'] for r in rows], y, color='#D94343', s=65, zorder=3)
for i,r in enumerate(rows):
    axes[1].annotate(f"{r['fear_cosine_change_x1000']:+.0f}",(r['fear_cosine_change_x1000'],i),xytext=(0,12),textcoords='offset points',ha='center',fontsize=11)
axes[1].set_xlim(0,130)
axes[1].set_xlabel('Change in Fear-axis cosine\n(× 1,000)')
axes[1].set_title('b  Notice-end representation', loc='left', fontsize=14, fontweight='bold', pad=18)
fig.suptitle('Deletion relative to preservation', fontsize=16, fontweight='bold')
for suffix in ['png','svg']:
    fig.savefig(ROOT/f'v4_summary.{suffix}', dpi=220, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(json.dumps(rows, indent=2))
