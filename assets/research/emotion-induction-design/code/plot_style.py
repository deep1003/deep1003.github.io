"""연구 그림의 공통 색상과 조건별 마커."""
PALETTE = {
    'neutral': '#858585', 'UN': '#c94b4b', 'FA': '#3979b8',
    'calm': '#269b88', 'sadness': '#8867ad', 'anger': '#db8738',
    'desperation': '#93654b', 'joy': '#d6b238',
}

def condition_marker(ax, x, y, condition, **kwargs):
    """UN+FA 조건은 빨강/파랑 반쪽 마커로 표시한다."""
    common = dict(markersize=9, markeredgecolor='#333333', markeredgewidth=.6, linestyle='None', zorder=4)
    common.update(kwargs)
    if condition == 'UN1FA1':
        return ax.plot(x, y, marker='o', fillstyle='left', markerfacecolor=PALETTE['UN'], markerfacecoloralt=PALETTE['FA'], **common)
    colour = PALETTE['UN'] if condition == 'UN1FA0' else PALETTE['FA'] if condition == 'UN0FA1' else PALETTE['neutral']
    return ax.plot(x, y, marker='o', markerfacecolor=colour, **common)
