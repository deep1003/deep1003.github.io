"""Companion to the internal-emotion atlas: each region uses its own emotion colour ramp,
dark -> emotion colour -> yellow peak. Same cells, same values and same scale as the original
(change in cosine vs UN0FA0, -0.007 to +0.016); only the colour mapping differs.

입력: data/atlas/atlas_source_data.csv, data/atlas/region_geometry.json (저장된 값, 모델 재실행 없음)
출력: Emotion_atlas_change_coloured_en.{svg,pdf,png}
"""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.patheffects
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize, to_rgb
from matplotlib.patches import Polygon, Rectangle

DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('.')
VMIN, VMAX = -0.007, 0.016                      # 원본 아틀라스와 같은 척도
YELLOW = '#FFE84A'                              # 정서 램프의 노란 구간
PEAK = '#FFFAA0'                                # 최상단의 밝은 노란색(원본 열지도의 정점과 같은 느낌)
EMO = {'UN': '#2166C4', 'FA': '#D9382C', 'calm': '#86C454', 'sadness': '#F28B7A',
       'anger': '#A82418', 'desperation': '#661226', 'joy': '#2E9A3C'}
NAME = {'UN': 'Uncertainty', 'FA': 'Fear /\nanxiety', 'calm': 'Calm', 'sadness': 'Sadness',
        'anger': 'Anger', 'desperation': 'Desperation', 'joy': 'Joy'}
LEG = {'UN': 'Uncertainty', 'FA': 'Fear/anxiety', 'calm': 'Calm', 'sadness': 'Sadness',
       'anger': 'Anger', 'desperation': 'Desperation', 'joy': 'Joy'}
CONDS = [('UN0FA0', 'a  UN0FA0 (reference)'), ('UN0FA1', 'b  UN0FA1'), ('UN1FA0', 'c  UN1FA0'), ('UN1FA1', 'd  UN1FA1')]
INK = '#1F1B16'


def shade(c, k):
    """k<1: 검정 쪽으로 어둡게."""
    return tuple(np.array(to_rgb(c)) * k)


def mid_tone(c, light=.42):
    """정서색의 색상·채도는 유지하고 명도만 맞춘다(영역 간 같은 값이 같은 밝기로 보이게)."""
    import colorsys
    h, l, s_ = colorsys.rgb_to_hls(*to_rgb(c)); return colorsys.hls_to_rgb(h, light, min(1, s_ * 1.05))


def ramp(c):
    """정서별 램프: 아주 어두운 정서색(음수) -> 어두운 정서색(0) -> 정서색 -> 노란 정점."""
    z = (0 - VMIN) / (VMAX - VMIN)              # 0의 위치(약 0.30)
    m = mid_tone(c)
    y = np.array(to_rgb(YELLOW)); mm = np.array(m)
    # 0 이상 구간의 위쪽 약 1/3을 노란색 쪽에 배정한다(밝은 끝은 가장 큰 변화에만)
    stops = [(0.0, shade(m, .18)), (z, shade(m, .45)), (.56, m),
             (.74, tuple(.55 * mm + .45 * y)), (.90, tuple(y)), (1.0, to_rgb(PEAK))]
    return LinearSegmentedColormap.from_list('ramp', stops)


def build():
    g = json.loads((DATA / 'region_geometry.json').read_text())
    d = pd.read_csv(DATA / 'atlas_source_data.csv')
    axes = g['axes']; tiles = g['tiles']; polys = g['polygons']
    norm = Normalize(VMIN, VMAX); cmaps = {a: ramp(EMO[a]) for a in axes}
    plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': ['Helvetica', 'Arial', 'Inter', 'DejaVu Sans'],
                         'svg.fonttype': 'none'})
    fig = plt.figure(figsize=(180 / 25.4, 200 / 25.4))
    fig.text(.03, .975, 'Change from the shared reference, coloured by internal emotion', fontsize=11, weight='bold', color=INK)
    fig.text(.03, .953, 'Same cells, values and scale as the original atlas; each region uses its own emotion ramp, all peaking at yellow.',
             fontsize=7, color='#55504A')
    boxes = [(.02, .52), (.46, .52), (.02, .135), (.46, .135)]
    for (cond, title), (x0, y0) in zip(CONDS, boxes):
        ax = fig.add_axes([x0, y0, .40, .38]); ax.set_aspect('equal'); ax.axis('off')
        verts, cols = list(tiles), []
        # 타일-축 대응과 값
        ref = d[d.condition == 'UN0FA1'][['tile_id', 'axis']].drop_duplicates().set_index('tile_id')['axis']
        vals = (d[d.condition == cond].set_index('tile_id')['delta_cosine'] if cond != 'UN0FA0'
                else pd.Series(0.0, index=ref.index))
        for tid in range(len(tiles)):
            a = ref.at[tid]; cols.append(cmaps[a](norm(vals.at[tid])))
        ax.add_collection(PolyCollection(verts, facecolors=cols, edgecolors='none', antialiased=False, rasterized=True))
        for a, poly in zip(axes, polys):
            ax.add_patch(Polygon(poly, closed=True, fill=False, edgecolor='white', lw=.8))
            cx, cy = np.array(poly).mean(axis=0)          # 영역 꼭짓점 평균 위치에 이름
            ax.text(cx, cy, NAME[a], ha='center', va='center', fontsize=7, weight='bold', color='white',
                    path_effects=[matplotlib.patheffects.withStroke(linewidth=1.6, foreground='#000000')])
        ax.set_xlim(-1.03, 1.03); ax.set_ylim(-1.03, 1.03)
        fig.text(x0 + .01, y0 + .385, title, fontsize=8.5, color=INK)
    # 범례: 정서별 램프 7개
    lx, ly, lw, lh = .06, .075, .125, .012
    fig.text(lx, ly + .028, 'Change vs. UN0FA0: low -> emotion colour -> bright yellow (high)', fontsize=7, color=INK)
    grad = np.linspace(0, 1, 256)[None, :]
    for k, a in enumerate(axes):
        x = lx + (k % 4) * (lw + .095); y = ly - (k // 4) * .045
        cax = fig.add_axes([x, y, lw, lh]); cax.imshow(grad, aspect='auto', cmap=cmaps[a]); cax.set_xticks([]); cax.set_yticks([])
        for s in cax.spines.values(): s.set_linewidth(.3)
        fig.text(x + lw + .006, y + .002, LEG[a], fontsize=6.5, color=INK, va='bottom')
    fig.text(.03, .012, 'Region geometry and cell values are identical to the original atlas; colour encodes the same within-item change, '
             'not emotion probability.', fontsize=6, color='#55504A')
    OUT.mkdir(parents=True, exist_ok=True)
    stem = OUT / 'Emotion_atlas_change_coloured_en'
    for ext, kw in [('svg', {}), ('pdf', {}), ('png', {'dpi': 600})]:
        fig.savefig(f'{stem}.{ext}', facecolor='white', **kw)
    plt.close(fig)
    return stem


if __name__ == '__main__':
    import matplotlib.patheffects
    print(build())
