"""Similarity-based emotion territories with measured, unsmoothed KoBBQ tiles."""
from pathlib import Path
import hashlib
import json

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from scipy.ndimage import label as connected_components
from scipy.spatial.distance import pdist
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.collections import LineCollection
import matplotlib.patheffects as path_effects

from plot_style import activation_cmap

BASE = Path(__file__).resolve().parent
AXIS_DATA = BASE / 'representation_analysis/results/d335ad178e3c'
ITEM_DATA = BASE / 'representation_analysis/item_category_alignment/output/item_alignment.csv'
OUT = BASE / 'representation_analysis/emotion_atlas/output'
AXES = ['UN', 'FA', 'calm', 'sadness', 'anger', 'desperation', 'joy']
CONDITIONS = ['UN0FA0', 'UN0FA1', 'UN1FA0', 'UN1FA1']
LABELS = ['Uncertainty', 'Fear /\nanxiety', 'Calm', 'Sadness', 'Anger', 'Desperation', 'Joy']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def layout():
    """Fit geometry from frozen concept directions, never from activation values."""
    directions = np.load(AXIS_DATA / 'axes_qwen_L14.npz')['directions'].astype(np.float64)
    directions /= np.linalg.norm(directions, axis=1, keepdims=True)
    centered = directions - directions.mean(axis=0)
    u, singular, _ = np.linalg.svd(centered, full_matrices=False)
    coordinates = u[:, :2] * singular[:2]
    # Fix only display orientation: UN left; calm above anger.
    if coordinates[0, 0] > coordinates[2, 0]:
        coordinates[:, 0] *= -1
    if coordinates[2, 1] < coordinates[4, 1]:
        coordinates[:, 1] *= -1
    explained = float(np.sum(singular[:2]**2) / np.sum(singular**2))
    full_dist = pdist(directions)
    short_dist = pdist(coordinates)
    stress = float(np.sqrt(np.sum((full_dist-short_dist)**2) / np.sum(full_dist**2)))
    # 31 x 32 grid, with 19 outermost cells omitted, gives 7 x 139 real tiles.
    yy, xx = np.mgrid[0:31, 0:32]
    all_grid = np.column_stack([xx.ravel(), yy.ravel()])
    distance = ((all_grid - [15.5, 15])**2).sum(axis=1)
    keep = np.argsort(distance, kind='stable')[:973]
    grid = all_grid[np.sort(keep)]
    grid_coordinates = (grid - [15.5, 15]) / 16
    # One global scale preserves distances and angles between concept centers.
    centers = coordinates / np.max(np.abs(coordinates)) * .85
    costs = ((grid_coordinates[:, None, :] - centers[None, :, :])**2).sum(axis=2)
    # Capacity-constrained Voronoi-type allocation: equal cell counts per concept.
    rows, columns = linear_sum_assignment(np.repeat(costs, 139, axis=1))
    territory = columns // 139
    assert np.array_equal(rows, np.arange(973))
    raster = np.full((31, 32), -1, dtype=int)
    raster[grid[:, 1], grid[:, 0]] = territory
    components = {axis: int(connected_components(raster == k)[1]) for k, axis in enumerate(AXES)}
    assert all(v == 1 for v in components.values()), 'A concept region is disconnected.'
    boundaries = []
    for x, y in grid:
        owner = raster[y, x]
        for dx, dy, start, end in [(1, 0, (x+.5, y-.5), (x+.5, y+.5)),
                                    (0, 1, (x-.5, y+.5), (x+.5, y+.5))]:
            nx, ny = x+dx, y+dy
            if nx >= 32 or ny >= 31 or raster[ny, nx] != owner:
                boundaries.append([start, end])
        if x == 0 or raster[y, x-1] == -1:
            boundaries.append([(x-.5, y-.5), (x-.5, y+.5)])
        if y == 0 or raster[y-1, x] == -1:
            boundaries.append([(x-.5, y-.5), (x+.5, y-.5)])
    # Verify the assignment's coarse spatial distances as an additional layout diagnostic.
    region_centers = np.array([grid_coordinates[territory == k].mean(axis=0) for k in range(7)])
    layout_distance_r = float(np.corrcoef(pdist(centers), pdist(region_centers))[0, 1])
    return grid, territory, raster, np.array(boundaries), coordinates, {
        'two_dimensional_retained_variance': explained, 'distance_stress': stress,
        'capacity': 139, 'components_per_region': components,
        'centroid_distance_correlation': layout_distance_r}


def build(show=True):
    """Use cached measurements only. No inference, invented tiles or smoothing."""
    from english_figures import style
    style()
    OUT.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(ITEM_DATA)
    data = data[data.layer == 14].copy()
    assert len(data) == 556 and not data.duplicated(['item', 'condition']).any()
    assert set(data.condition) == set(CONDITIONS)
    items = data[['item', 'category', 'cluster']].drop_duplicates().sort_values(['category', 'cluster', 'item'])
    assert len(items) == 139
    grid, owners, raster, boundaries, coordinates, diagnostics = layout()
    tile_rows = []
    for k, axis in enumerate(AXES):
        indices = np.where(owners == k)[0]
        indices = sorted(indices, key=lambda i: (-grid[i, 1], grid[i, 0]))
        assert len(indices) == 139
        for i, item in zip(indices, items.itertuples(index=False)):
            tile_rows.append(dict(axis=axis, item=item.item, category=item.category,
                                  cluster=item.cluster, x=int(grid[i, 0]), y=int(grid[i, 1])))
    tiles = pd.DataFrame(tile_rows)
    raw = data.melt(id_vars=['item', 'condition'], value_vars=['cos_'+a for a in AXES],
                    var_name='axis', value_name='cosine')
    raw.axis = raw.axis.str.removeprefix('cos_')
    values = tiles.merge(raw, on=['item', 'axis'], validate='one_to_many')
    baseline = raw[raw.condition == 'UN0FA0'][['item', 'axis', 'cosine']].rename(columns={'cosine': 'baseline'})
    values = values.merge(baseline, on=['item', 'axis'], validate='many_to_one')
    values['delta_cosine'] = values.cosine - values.baseline
    assert len(values) == 3892 and not values.duplicated(['item','axis','condition']).any()
    assert np.isfinite(values[['cosine', 'delta_cosine']]).all().all()
    assert (values.loc[values.condition == 'UN0FA0', 'delta_cosine'] == 0).all()
    tiles.to_csv(OUT / 'tile_layout.csv', index=False)
    values.to_csv(OUT / 'atlas_source_data.csv', index=False)
    pd.DataFrame(coordinates, index=AXES, columns=['Dimension_1','Dimension_2']).to_csv(OUT/'concept_coordinates.csv')
    cmap = activation_cmap()
    outputs = []
    for metric, name, title, color_label in [
        ('cosine', 'Emotion_atlas_absolute_en', 'Emotion-concept activation atlas', 'L14 centered cosine alignment'),
        ('delta_cosine', 'Emotion_atlas_change_en', 'Change from the shared reference', 'Change in cosine vs. UN0FA0')]:
        low, high = float(values[metric].min()), float(values[metric].max())
        norm = Normalize(low, high)
        fig, axs = plt.subplots(2, 2, figsize=(180/25.4, 176/25.4))
        fig.subplots_adjust(left=.025, right=.88, top=.88, bottom=.09, wspace=.10, hspace=.14)
        fig.text(.025, .97, title, fontsize=9, weight='bold')
        fig.text(.025, .935, 'Qwen2.5-7B-Instruct, layer 14; 139 selected KoBBQ items per region', fontsize=6.5)
        for ax, condition, panel in zip(axs.flat, CONDITIONS, 'abcd'):
            v = values[values.condition == condition]
            image = np.full((31, 32), np.nan)
            image[v.y.to_numpy(), v.x.to_numpy()] = v[metric].to_numpy()
            im = ax.imshow(image, origin='lower', interpolation='none', cmap=cmap, norm=norm,
                           extent=[-.5,31.5,-.5,30.5], rasterized=True)
            ax.add_collection(LineCollection(boundaries, colors='#F9EEEE', linewidths=.6))
            for k, label in enumerate(LABELS):
                points = grid[owners == k]
                center = points.mean(axis=0)
                point = points[np.argmin(((points-center)**2).sum(axis=1))]
                text = ax.text(point[0], point[1], label, color='white', ha='center', va='center',
                               fontsize=6, weight='bold', linespacing=1.1)
                text.set_path_effects([path_effects.withStroke(linewidth=1.8, foreground='#240000')])
            ax.set_xticks([]); ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)
            suffix = ' (reference)' if condition == 'UN0FA0' else ''
            ax.set_title(f'{panel}  {condition}{suffix}', loc='left', fontsize=7, pad=4)
        cb = fig.colorbar(im, cax=fig.add_axes([.91,.21,.018,.53]))
        cb.set_label(color_label, fontsize=6.5)
        # A visible zero tick retains the sign of low/negative alignments.
        ticks = sorted(set([low, 0., high])) if low <= 0 <= high else [low, high]
        cb.set_ticks(ticks)
        cb.ax.set_yticklabels([f'{v:+.3f}' for v in ticks], fontsize=6)
        fig.text(.025,.045,'Regions: fixed similarity-based layout. Tiles: individual items, not spatial measurements.',fontsize=6)
        fig.text(.025,.020,'Dark red = lower value; light yellow = higher value. No smoothing; identical scales across conditions.',fontsize=6)
        fig.savefig(OUT/f'{name}_preview.png',dpi=600)
        for ext in ['pdf','svg','png']:
            fig.savefig(OUT/f'{name}.{ext}',dpi=600)
        if show:
            plt.show()
        plt.close(fig)
        outputs.append(OUT/f'{name}.png')
    validation = dict(n_concepts=7, n_items=139, n_conditions=4, n_cells_per_panel=973,
                      n_measured_values=3892, baseline='UN0FA0 within item and concept',
                      model_inference=False, interpolated_values=False,
                      duplicated_keys=0, diagnostics=diagnostics,
                      source_sha256=sha(ITEM_DATA), axes_sha256=sha(AXIS_DATA/'axes_qwen_L14.npz'),
                      code_sha256=sha(__file__))
    (OUT/'validation.json').write_text(json.dumps(validation, indent=2))
    return outputs


if __name__ == '__main__':
    build(show=False)
