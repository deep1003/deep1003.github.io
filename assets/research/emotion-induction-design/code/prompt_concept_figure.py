"""Unicode-aware text layout helpers for current master figures."""
import re
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextToPath
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


def mix(color, t):
    """흰색과 개념색 사이 보간(t=0 흰색, t=1 개념색)."""
    r = np.array(to_rgb(color)); return tuple(1 - t * (1 - r))


