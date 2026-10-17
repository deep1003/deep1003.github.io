"""Prompt text coloured by the dominant internal emotion (three colour families).

입력: representation_analysis/token_highlights/output/highlights.json (저장된 측정값, 모델 재실행 없음)
출력: figures/Prompt_text_concepts_en.{svg,pdf,png} + Prompt_text_concepts_source.csv

표준화: 각 개념 축을 네 프롬프트의 모든 글자(14층)에 대해 z-점수화한다.
  원 코사인은 축마다 기준 수준이 달라(분노·절박함이 전반적으로 높음) 그대로 비교하면 한 축이 전부를 덮는다.
  z는 "그 축 안에서 상대적으로 높은 위치"를 뜻하며, 정서 확률이나 원인 기여도가 아니다.
오른쪽 텍스트: 글자마다 z가 가장 큰 개념의 색, 그 z가 클수록 진하게(z < Z_MIN이면 칠하지 않음).
"""
from pathlib import Path
import json, csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from matplotlib.font_manager import FontProperties, findSystemFonts
from matplotlib.textpath import TextToPath
from matplotlib.patches import Rectangle, ConnectionPatch
import re

BASE = Path(__file__).resolve().parent
DATA = BASE / 'representation_analysis/token_highlights/output'
OUT = BASE / 'figures'
LAYER = '14'
CONDITIONS = ['UN0FA0', 'UN0FA1', 'UN1FA0', 'UN1FA1']
LABELS = {'UN0FA0': '00  Reference', 'UN0FA1': '01  FA only', 'UN1FA0': '10  UN only', 'UN1FA1': '11  UN + FA'}
COND_COL = {'UN0FA0': '#8E897F', 'UN0FA1': '#D9382C', 'UN1FA0': '#2166C4', 'UN1FA1': '#8E45A8'}
CONCEPTS = ['UN', 'FA', 'Calm', 'Sadness', 'Anger', 'Desperation', 'Joy']
SHORT = ['UN', 'FA', 'Calm', 'Sad.', 'Ang.', 'Desp.', 'Joy']
# 7개념 색: 페이지 팔레트(UN 청록, FA 적갈)와 같은 계열의 안료 톤
# 세 색상 계열: 불확실성(청색) · 부정 정서(적색, 명도로 구분) · 긍정 정서(녹색, 명도로 구분)
CCOL = {'UN': '#2166C4',
        'FA': '#D9382C', 'Sadness': '#F28B7A', 'Anger': '#A82418', 'Desperation': '#661226',
        'Calm': '#86C454', 'Joy': '#2E9A3C'}
GROUPS = [('Uncertainty', ['UN']), ('Negative', ['FA', 'Sadness', 'Anger', 'Desperation']), ('Positive', ['Calm', 'Joy'])]
ORDER = [c for _, cs in GROUPS for c in cs]                 # 열 순서: 계열별로 묶는다
SHORT_OF = {'UN': 'UN', 'FA': 'FA', 'Calm': 'Calm', 'Sadness': 'Sad.', 'Anger': 'Ang.', 'Desperation': 'Desp.', 'Joy': 'Joy'}
Z_MIN, Z_MAX = 0.5, 2.5       # 칠하기 시작하는 z, 최대 진하기 z
INK = '#1F1B16'


def korean_font():
    """맥에서는 AppleGothic, 그 외에는 설치된 한글 글꼴을 쓴다."""
    from matplotlib import font_manager as fm
    for name in ['AppleGothic', 'Apple SD Gothic Neo', 'Noto Sans CJK KR', 'Noto Sans CJK JP', 'NanumGothic', 'Noto Serif CJK KR']:
        try:
            fm.findfont(FontProperties(family=name), fallback_to_default=False)
            return FontProperties(family=name)
        except Exception:
            continue
    return FontProperties()


FONT = korean_font()
MEASURE = TextToPath()


def segments(text):
    """문장 단위 구간(원문 공백 포함)."""
    starts = [0] + [m.end() for m in re.finditer(r'\n\n|(?<=\.)\s+(?=[가-힣])', text)]
    starts = sorted(set(starts + [len(text)]))
    return [(a, z) for a, z in zip(starts, starts[1:]) if text[a:z].strip()]


def wrap_span(text, a, z, width, size):
    prop = FONT.copy(); prop.set_size(size)
    widths = {c: MEASURE.get_text_width_height_descent(c, prop, False)[0] for c in set(text[a:z]) if c not in '\r\n'}
    lines, line, used = [], [], 0.
    for word in re.finditer(r'[^\S\r\n]+|\S+|[\r\n]+', text[a:z]):
        token = word.group(); start = a + word.start()
        if '\n' in token or '\r' in token:
            if line: lines.append(line); line, used = [], 0.
            continue
        total = sum(widths[c] for c in token)
        if not token.isspace() and line and used + total > width:
            lines.append(line); line, used = [], 0.
        if token.isspace() and not line: continue
        for j, c in enumerate(token):
            w = widths[c]
            if line and used + w > width:
                lines.append(line); line, used = [], 0.
            line.append((start + j, c, used, w)); used += w
    if line: lines.append(line)
    return lines


YELLOW = '#FFE84A'


def mid_tone(c, light=.42):
    import colorsys
    h, l, s_ = colorsys.rgb_to_hls(*to_rgb(c)); return colorsys.hls_to_rgb(h, light, min(1, s_ * 1.05))


def emo_ramp(c):
    """M3b와 같은 정서 램프(정점은 노란색). 입력 0~1."""
    m = np.array(mid_tone(c)); y = np.array(to_rgb(YELLOW))
    pk = np.array(to_rgb('#FFFAA0'))
    # M3와 같은 형태: 위쪽 절반을 노란색 쪽에 배정해 밝은 끝을 넓게 보이게 한다
    stops = [(0.0, m * .18), (.25, m * .45), (.56, m), (.74, .55 * m + .45 * y), (.90, y), (1.0, pk)]
    return LinearSegmentedColormap.from_list('emo', [(p, tuple(v)) for p, v in stops])


def mix(color, t):
    """흰색과 개념색 사이 보간(t=0 흰색, t=1 개념색)."""
    r = np.array(to_rgb(color)); return tuple(1 - t * (1 - r))


def load():
    payload = json.loads((DATA / 'highlights.json').read_text(encoding='utf-8'))
    prompts = {p['condition']: p for p in payload['prompts']}
    raw = {c: np.array([r['cosine'] for r in prompts[c]['layers'][LAYER]], float) for c in CONDITIONS}
    allv = np.vstack([raw[c] for c in CONDITIONS])
    mu, sd = allv.mean(0), allv.std(0, ddof=1)
    z = {c: (raw[c] - mu) / sd for c in CONDITIONS}
    return prompts, raw, z


def row(fig, p, Z, bottom, height, letter, size=7.4):
    text = p['text']; n = len(text)
    assert Z.shape == (n, 7)
    fw, fh = fig.get_size_inches() * 72
    left, heat_w, right, right_w = .095, .19, .40, .56
    ax = fig.add_axes([left, bottom, heat_w, height])
    # 왼쪽: 계열별로 묶은 열(흰색 → 개념색), 계열 사이에 흰 간격을 둔다
    cols, xpos, x = [], [], 0.
    for gi, (_, cs) in enumerate(GROUPS):
        for cname in cs:
            cols.append(cname); xpos.append(x); x += 1
        x += .45
    for cname, x0 in zip(cols, xpos):
        k = CONCEPTS.index(cname)
        t = np.clip((Z[:, k] + 1.5) / (Z_MAX + 1.5), 0, 1)      # z -1.5~2.5를 램프 전체에 대응
        img = emo_ramp(CCOL[cname])(t)[:, None, :3]
        ax.imshow(img, aspect='auto', origin='upper', interpolation='none', rasterized=True,
                  extent=(x0 - .5, x0 + .5, n - .5, -.5))
    ax.set_xlim(-.5, xpos[-1] + .5); ax.set_ylim(n - .5, -.5)
    ax.set_xticks(xpos); ax.set_xticklabels([SHORT_OF[c] for c in cols], rotation=90, fontsize=5.6)
    for lab, cname in zip(ax.get_xticklabels(), cols):
        lab.set_color(CCOL[cname]); lab.set_fontweight('bold')
    ex = xpos[-1] + .65
    ax.set_yticks([0, n - 1]); ax.set_yticklabels(['1', str(n)], fontsize=6)
    ax.set_ylabel('Character position', fontsize=6.5, labelpad=3)
    ax.tick_params(length=0, pad=2)
    for s in ax.spines.values(): s.set_visible(False)
    fig.text(.04, bottom + height + .010, letter, weight='bold', fontsize=8)
    fig.text(left, bottom + height + .010, LABELS[p['condition']], color=COND_COL[p['condition']], fontsize=8, weight='bold')
    # 오른쪽: 원문, 글자마다 우세 개념 색
    tx = fig.add_axes([right, bottom, right_w, height]); width = right_w * fw; h = height * fh
    tx.set_xlim(0, width); tx.set_ylim(0, h); tx.axis('off')
    spans = segments(text); line_h, gap, pad = size + 3.2, 5.5, 3.
    for _ in range(12):
        wrapped = [wrap_span(text, a, z, width - 2 * pad, size) for a, z in spans]
        used = sum(len(l) * line_h + 2 * pad + gap for l in wrapped) - gap
        if used <= h: break
        size -= .2; line_h -= .2; gap -= .2
    top = h
    dom = Z.argmax(1); dz = Z.max(1)
    for (a, z), lines in zip(spans, wrapped):
        box_h = len(lines) * line_h + 2 * pad
        tx.add_patch(Rectangle((0, top - box_h), width, box_h, facecolor='white', edgecolor='#B9B2A5', lw=.4))
        for r, line in enumerate(lines):
            y = top - pad - r * line_h
            for i, c, x, w in line:
                if c.isspace(): continue
                t = np.clip((dz[i] - Z_MIN) / (Z_MAX - Z_MIN), 0, 1) if dz[i] >= Z_MIN else 0.
                col = CCOL[CONCEPTS[dom[i]]]
                if t > 0:
                    tx.add_patch(Rectangle((pad + x, y - line_h + .6), max(w, .5), line_h - .4,
                                           facecolor=tuple(.7 * np.array(mix(col, .18 + .82 * t)) + .3 * np.array(to_rgb(YELLOW))) if t > .85 else mix(col, .18 + .82 * t), edgecolor='none'))
                fg = '#FFFFFF' if t > .62 and np.mean(to_rgb(col)) < .55 else INK
                tx.text(pad + x, y - .4, c, fontproperties=FONT, fontsize=size, va='top', color=fg)
        fig.add_artist(ConnectionPatch(xyA=(ex, (a + z - 1) / 2), coordsA=ax.transData, xyB=(0, top - box_h / 2),
                                       coordsB=tx.transData, color='#9A9285', lw=.45, clip_on=False, zorder=1))
        ax.plot([ex, ex], [a - .5, z - .5], color='#6B635A', lw=.6, clip_on=False)
        top -= box_h + gap


def legend(fig, x0, y0):
    fig.text(x0, y0 + .018, 'Dominant internal emotion (character background)', fontsize=7, color=INK)
    x = x0
    for gname, cs in GROUPS:
        fig.text(x, y0 - .001, gname + ':', fontsize=6.3, color=INK, fontweight='bold')
        x += .0075 * len(gname) + .016
        for cname in cs:
            fig.add_artist(Rectangle((x, y0 - .002), .016, .010, transform=fig.transFigure, facecolor=CCOL[cname], edgecolor='none'))
            fig.text(x + .019, y0, cname, fontsize=6.3, color=INK)
            x += .019 + .0068 * len(cname) + .012
        x += .018
    fig.text(x0, y0 - .020, f'Left: within-emotion z-score, dark -> emotion colour -> yellow peak. Text: dominant emotion, shaded from z = {Z_MIN} to {Z_MAX} (yellow tint at the top).',
             fontsize=6, color='#6B635A')


def build(show=False):
    plt.rcParams.update({'font.family': 'sans-serif', 'svg.fonttype': 'path'})
    prompts, raw, z = load()
    fig = plt.figure(figsize=(180 / 25.4, 270 / 25.4))
    fig.text(.04, .979, 'Where each internal emotion is most aligned in the prompt', fontsize=10, weight='bold', color=INK)
    fig.text(.095, .955, 'Emotions by family (ramps peak at yellow)', fontsize=7, color=INK)
    fig.text(.40, .955, 'Original Korean prompt; background = dominant internal emotion', fontsize=7, color=INK)
    for i, c in enumerate(CONDITIONS):
        row(fig, prompts[c], z[c], .762 - i * .212, .156, 'abcd'[i])
    legend(fig, .095, .045)
    fig.text(.04, .006, 'Contextual hidden-state alignment, standardized within each internal emotion; not token attribution or experienced emotion.',
             fontsize=6, color='#6B635A')
    OUT.mkdir(exist_ok=True)
    stem = OUT / 'Prompt_text_concepts_en'
    for ext, kw in [('svg', {}), ('pdf', {}), ('png', {'dpi': 600})]:
        fig.savefig(f'{stem}.{ext}', facecolor='white', **kw)
    with open(OUT / 'Prompt_text_concepts_source.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['condition', 'char_index', 'char'] + [f'cos_{c}' for c in CONCEPTS] + [f'z_{c}' for c in CONCEPTS] + ['dominant'])
        for c in CONDITIONS:
            for i, rec in enumerate(prompts[c]['layers'][LAYER]):
                w.writerow([c, i, rec['char']] + [f'{v:.6f}' for v in raw[c][i]] + [f'{v:.4f}' for v in z[c][i]] + [CONCEPTS[int(z[c][i].argmax())]])
    if show: plt.show()
    else: plt.close(fig)
    return stem


if __name__ == '__main__':
    print(build())
