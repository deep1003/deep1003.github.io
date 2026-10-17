"""Single source of truth for study identities and quantitative color scales."""
from matplotlib.colors import LinearSegmentedColormap

PALETTE = {
    'neutral': '#777777', 'UN': '#C34835', 'FA': '#2868A3', 'combined': '#8054A1',
    'calm': '#279387', 'sadness': '#8167A9', 'anger': '#CA773B',
    'desperation': '#A04F80', 'joy': '#C2A237',
}
CONDITION_ORDER = ['UN0FA0', 'UN0FA1', 'UN1FA0', 'UN1FA1']
CONDITION_COLORS = dict(zip(CONDITION_ORDER, [PALETTE[k] for k in ['neutral','FA','UN','combined']]))
CONDITION_MARKERS = dict(zip(CONDITION_ORDER, ['o', 's', '^', 'D']))
CONDITION_TINTS = dict(zip(CONDITION_ORDER, ['#F3F3F3', '#EAF1F7', '#F9ECEA', '#F1ECF6']))
CONCEPT_ORDER = ['UN', 'FA', 'calm', 'sadness', 'anger', 'desperation', 'joy']
ACTIVATION_STOPS = ['#160000','#550000','#A60000','#E52600','#FF7600','#FFD12B','#FFFFA0']
SIMILARITY_STOPS = [(0.0, '#300000'), (0.5, '#700000'), (0.6, '#C00000'), (0.7, '#F52A00'), (0.82, '#FFB900'), (0.9, '#FFE92B'), (1.0, '#FFFF70')]
REPRESENTATION_COLORS = {'semantic': '#777777', 'qwen_L14': '#222222'}
FIT_COLOR = '#333333'


def activation_cmap():
    return LinearSegmentedColormap.from_list('study_activation', ACTIVATION_STOPS)


def similarity_cmap():
    return LinearSegmentedColormap.from_list('study_similarity', SIMILARITY_STOPS)


def condition_marker(ax, x, y, condition, **kwargs):
    common = dict(markersize=8, markeredgecolor='#333333', markeredgewidth=.6,
                  linestyle='None', zorder=4)
    common.update(kwargs)
    return ax.plot(x, y, marker=CONDITION_MARKERS[condition],
                   markerfacecolor=CONDITION_COLORS[condition], **common)

CATEGORY_STYLES={
'age':('Age','#0072B2','o'),
'disability_status':('Disability status','#D55E00','o'),
'domestic_area_of_origin':('Regional origin','#009E73','o'),
'educational_background':('Educational background','#CC79A7','o'),
'family_structure':('Family structure','#B58900','o'),
'gender_identity':('Gender identity','#56B4E9','o'),
'physical_appearance':('Physical appearance','#332288','o'),
'political_orientation':('Political orientation','#9C4A17','o'),
'race_ethnicity_nationality':('Race, ethnicity and nationality','#AA4499','o'),
'religion':('Religion','#449999','o'),
'ses':('Socioeconomic status','#882255','o'),
'sexual_orientation':('Sexual orientation','#666666','o')}


def heatmap_text_color(cmap, norm, value):
    """Choose black or white by contrast against the actual cell background."""
    rgb = cmap(norm(value))[:3]
    linear = [c/12.92 if c <= .04045 else ((c+.055)/1.055)**2.4 for c in rgb]
    luminance = sum(w*c for w,c in zip([.2126,.7152,.0722],linear))
    return '#111111' if luminance > .179 else '#FFFFFF'
