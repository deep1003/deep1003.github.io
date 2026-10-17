"""Synchronize curated figures, source tables, and the manual notebook. No plotting."""
from pathlib import Path
import hashlib
import json
import shutil
from curate_publication import curate

BASE = Path(__file__).resolve().parent
SITE = Path('/Users/deep1003/data3/deep1003.github.io/assets/research/emotion-induction-design')
REP = BASE / 'representation_analysis'

def sync():
    records = []
    def copy(source, relative):
        target = SITE / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.resolve() != target.resolve():
            shutil.copy2(source, target)
        records.append({'source': str(source), 'website': relative,
                        'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})

    catalog = json.loads((BASE / 'figure_catalog.json').read_text())
    for figure in catalog['figures']:
        for extension in ('png', 'pdf', 'svg'):
            copy(BASE / (figure['local_stem'] + '.' + extension),
                 figure['website_stem'] + '.' + extension)
    for name in ('Prompt_text_activation_FA_provenance.json', 'Prompt_text_activation_source.json'):
        copy(BASE / 'figures' / name, 'data/prompt-text/' + name)
    copy(BASE / 'figures/behavior_contrasts_display.json', 'data/behavior/contrasts_display.json')
    copy(BASE / 'color-specification.json', 'data/color-specification.json')
    copy(BASE / 'figures/axis_similarity_L14_validation.json', 'data/l14/validation.json')
    for name in ('axis_cosines_qwen_L14.csv', 'heldout_checks.csv', 'manifest.json', 'qwen_runtime.json'):
        copy(REP / 'results/d335ad178e3c' / name, 'data/l14/' + name)
    copy(REP / 'anchors.json', 'data/l14/anchors.json')
    copy(BASE / 'l14_methods.html', 'data/l14/methods.html')
    copy(BASE / 'atlas_geometry_explainer.html', 'data/atlas/geometry_and_tiles.html')
    copy(BASE / 'axis_intervention/protocol.json', 'data/l14/axis_intervention_protocol.json')
    copy(BASE / 'fear_anxiety_expert_review.md', 'data/atlas/fear_anxiety_expert_review.md')
    for directory, destination in [('emotion_atlas', 'atlas'),
                                    ('publication_figures', 'concept'),
                                    ('item_category_alignment', 'category'), ('three_axis_supplement', 'three-axis')]:
        output = REP / directory / 'output'
        for file in output.rglob('*'):
            selected = file.suffix == '.csv' or file.name in ('Captions_and_methods.md', 'validation.json', 'provenance.json', 'artwork_provenance.json', 'manifest.json', 'plot_summary.json')
            if file.is_file() and ((destination == 'atlas' and file.suffix in ('.csv', '.json', '.md')) or selected):
                copy(file, 'data/' + destination + '/' + str(file.relative_to(output)))
    token = REP / 'token_highlights/output'
    for name, destination in [('prompt_highlights.html', 'index.html'),
                               ('token_scores.csv', 'token_scores.csv'), ('manifest.json', 'manifest.json')]:
        copy(token / name, 'prompt-activations/' + destination)
    modules = ['english_figures.py', 'notebook_views.py', 'plot_style.py', 'prompt_text_figure.py',
               'emotion_atlas.py', 'concept_umap.py', 'axis_intervention.py', 'three_axis_supplement.py', 'atlas_geometry_notes.py',
               'representation_analysis/analysis.py', 'representation_analysis/publication_figures/build_figures.py',
               'representation_analysis/item_category_alignment/plot.py',
               'representation_analysis/item_category_alignment/measure.py',
               'representation_analysis/item_category_alignment/collection_source_v1.py',
               'representation_analysis/token_highlights/render.py',
               'representation_analysis/token_highlights/measure.py']
    for name in modules:
        copy(BASE / name, 'code/' + name)
    copy(BASE.parent / 'uncertainty_self_threat_139.ipynb', 'downloads/uncertainty_self_threat_139.ipynb')
    records = curate(records)
    # Bundle and HTML are produced by curation and are hashed after all writes finish.
    for relative in ('downloads/notebook_cached_analysis.zip', 'index.html'):
        file = SITE / relative
        records.append({'source': str(file), 'website': relative,
                        'sha256': hashlib.sha256(file.read_bytes()).hexdigest()})
    unique = {entry['website']: entry for entry in records}
    manifest = {'manual_execution': True, 'automatic_model_inference': False,
                'automatic_figure_generation': False, 'main_figures': 4, 'supplementary_figures': 3,
                'figure_language': 'en-US', 'n_items': 139, 'records': list(unique.values())}
    (SITE / 'sync-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"Synchronized {len(unique)} files; 4 main + 3 supplementary figures; "
          f"bundle {(SITE / 'downloads/notebook_cached_analysis.zip').stat().st_size / 1e6:.2f} MB")

if __name__ == '__main__':
    sync()
