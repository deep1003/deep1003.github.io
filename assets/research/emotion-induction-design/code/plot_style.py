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
REPRESENTATION_COLORS = {'semantic': '#777777', 'qwen_L14': '#222222'}
FIT_COLOR = '#333333'


def activation_cmap():
    return LinearSegmentedColormap.from_list('study_activation', ACTIVATION_STOPS)


def similarity_cmap():
    return LinearSegmentedColormap.from_list('study_similarity', ['#FFFFFF', '#000000'])


def condition_marker(ax, x, y, condition, **kwargs):
    common = dict(markersize=8, markeredgecolor='#333333', markeredgewidth=.6,
                  linestyle='None', zorder=4)
    common.update(kwargs)
    return ax.plot(x, y, marker=CONDITION_MARKERS[condition],
                   markerfacecolor=CONDITION_COLORS[condition], **common)

CATEGORY_STYLES={
'age':('Age','#0072B2','o'),
'disability_status':('Disability status','#D55E00','s'),
'domestic_area_of_origin':('Regional origin','#009E73','^'),
'educational_background':('Educational background','#CC79A7','D'),
'family_structure':('Family structure','#B58900','v'),
'gender_identity':('Gender identity','#56B4E9','P'),
'physical_appearance':('Physical appearance','#332288','X'),
'political_orientation':('Political orientation','#9C4A17','>'),
'race_ethnicity_nationality':('Race, ethnicity and nationality','#AA4499','<'),
'religion':('Religion','#449999','p'),
'ses':('Socioeconomic status','#882255','h'),
'sexual_orientation':('Sexual orientation','#666666','*')}
