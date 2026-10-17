"""One authoritative publication selection; display cached artwork without plotting."""
from pathlib import Path
import json
BASE = Path(__file__).resolve().parent

def entries(placement=None):
    figures = json.loads((BASE / 'figure_catalog.json').read_text())['figures']
    return [f for f in figures if placement is None or f['placement'] == placement]

def show(figure_id, width=1000):
    from IPython.display import Image, Markdown, HTML, display
    entry = next(f for f in entries() if f['id'] == figure_id)
    path = BASE / (entry['local_stem'] + '.png')
    if not path.exists():
        raise FileNotFoundError(f'Cached publication artwork is missing: {path}')
    display(Markdown(f"**{entry['id']}. {entry['title']}**"))
    if figure_id == 'M3':
        display(HTML((BASE / 'atlas_geometry_explainer.html').read_text()))
    display(Image(filename=str(path), width=width))
    if figure_id == 'S3':
        display(HTML((BASE / 'representation_analysis/three_axis_supplement/output/Interpretation.html').read_text()))
    return path

def show_supplement(enabled=False):
    if enabled:
        for entry in entries('supplement'):
            show(entry['id'])
    else:
        print('Supplementary figures are available. Set SHOW_SUPPLEMENT = True to display them once.')
