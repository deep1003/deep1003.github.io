# Builds the data bundle (observations, regime trends, forecasts) for the
# early-career employment page. Status codes: r reported, d derived from a
# reported change, e estimated or interpolated, f forecast.
import json, math, statistics as st

def interp(pts):
    """Fill missing integer years between reported anchors (status e)."""
    pts = sorted(pts); out = []
    for (x0, y0, s0), (x1, y1, s1) in zip(pts, pts[1:]):
        out.append((x0, y0, s0))
        for x in range(x0 + 1, x1):
            out.append((x, round(y0 + (y1 - y0) * (x - x0) / (x1 - x0), 2), 'e'))
    out.append(pts[-1]); return out

def ols(xy):
    n = len(xy); mx = sum(x for x, _ in xy) / n; my = sum(y for _, y in xy) / n
    sxx = sum((x - mx) ** 2 for x, _ in xy)
    b = sum((x - mx) * (y - my) for x, y in xy) / sxx if sxx else 0.0
    return b, my - b * mx

REG = [('pre', 2016, 2019), ('covid', 2020, 2022), ('genai', 2023, 2100)]
PHI, Z, END = 0.8, 1.28, 2029

def build(sid, label, pts, rate=True, note=''):
    pts = interp(pts); xy = [(x, y) for x, y, _ in pts]
    trends = []
    for name, a, b in REG:
        seg = [(x, y) for x, y in xy if a <= x <= b]
        if len(seg) >= 2:
            s, i = ols(seg)
            trends.append({'regime': name, 'x0': seg[0][0], 'x1': seg[-1][0],
                           'y0': round(s * seg[0][0] + i, 3), 'y1': round(s * seg[-1][0] + i, 3),
                           'slope': round(s, 3)})
    gen = [(x, y) for x, y in xy if x >= 2023]
    if len(gen) < 2: gen = xy[-3:]
    slope = ols(gen)[0]
    diffs = [b[1] - a[1] for a, b in zip(xy, xy[1:])]
    sd = st.pstdev(diffs) if len(diffs) > 1 else abs(slope)
    lx, ly = xy[-1]; fc = []; cum = 0.0
    for h in range(1, END - lx + 1):
        cum += PHI ** h; y = ly + slope * cum; w = Z * sd * math.sqrt(h)
        lo, hi = y - w, y + w
        if rate: y, lo, hi = [max(0, min(100, v)) for v in (y, lo, hi)]
        fc.append({'x': lx + h, 'y': round(y, 2), 'lo': round(lo, 2), 'hi': round(hi, 2)})
    return {'id': sid, 'label': label, 'note': note,
            'obs': [{'x': x, 'y': y, 's': s} for x, y, s in pts],
            'trends': trends, 'fc': fc, 'genai_slope': round(slope, 3)}

D = {}
# --- Korea: employment rate of graduates by institution level (KEDI/MOE, 31 Dec reference) ---
D['kr_emp'] = [
 build('jc', 'Junior college (short-cycle)', [(2016,70.6,'r'),(2017,69.8,'r'),(2018,71.1,'r'),(2019,70.9,'r'),(2020,68.7,'r'),(2021,71.0,'e'),(2022,72.9,'r'),(2023,72.4,'r'),(2024,72.1,'r')]),
 build('ug', 'University (bachelor\'s)', [(2016,64.3,'r'),(2017,62.6,'r'),(2018,64.2,'r'),(2019,63.3,'r'),(2020,61.0,'r'),(2021,64.1,'e'),(2022,66.3,'r'),(2023,64.6,'r'),(2024,62.8,'r')]),
 build('gs', 'Graduate school (master\'s and doctoral)', [(2016,78.3,'r'),(2017,77.7,'r'),(2018,78.9,'r'),(2019,79.9,'e'),(2020,80.2,'e'),(2021,84.2,'e'),(2022,85.2,'e'),(2023,82.4,'r'),(2024,82.1,'r')]),
 build('phd', 'New doctorates, employed or placed at graduation', [(2015,76.4,'r'),(2016,75.5,'r'),(2017,74.3,'r'),(2023,70.9,'r'),(2024,70.4,'r'),(2025,66.7,'r')]),
 build('phd30', 'New doctorates aged under 30', [(2016,62.9,'r'),(2020,63.7,'r'),(2021,59.3,'r'),(2022,56.6,'r'),(2023,53.2,'r'),(2024,52.3,'r'),(2025,48.9,'r')]),
]
for s in D['kr_emp']: s['obs'] = [o for o in s['obs'] if o['x'] >= 2016]
# --- Korea: youth (15-29) employment rate, annual ---
ytd26 = round(sum([43.6,43.3,43.6,43.7,43.8,43.9,44.2,44.1,44.0,42.9]) / 10, 2)
D['kr_youth'] = [build('y1529', 'Employment rate, ages 15-29', [(2016,41.7,'e'),(2017,42.1,'e'),(2018,42.7,'e'),(2019,43.5,'e'),(2020,42.2,'e'),(2021,44.2,'r'),(2022,46.6,'r'),(2023,46.5,'r'),(2024,46.1,'r'),(2025,45.0,'r'),(2026,ytd26,'d')])]
# --- Degree output, thousands ---
G = {
 'bachelor': {
  'KR': [(2016,335,'e'),(2017,335,'e'),(2018,326,'e'),(2019,323,'e'),(2020,325,'e'),(2021,322,'e'),(2022,318,'e'),(2023,311.8,'d'),(2024,308.1,'d')],
  'US': [(2016,1920.7,'r'),(2017,1956.0,'r'),(2018,1980.6,'r'),(2019,2013.1,'r'),(2020,2038,'e'),(2021,2066,'e'),(2022,2015.0,'r'),(2023,2005,'e'),(2024,2000,'e')],
  'CN': [(2016,3744,'e'),(2017,3842,'e'),(2018,3868,'e'),(2019,3947,'e'),(2020,4206,'e'),(2021,4281,'e'),(2022,4716,'e'),(2023,4897,'e'),(2024,5090,'e'),(2025,5230.6,'r')]},
 'master': {
  'KR': [(2016,81.5,'e'),(2017,82.8,'e'),(2018,82.8,'e'),(2019,82.1,'e'),(2020,83.0,'r'),(2021,81.2,'e'),(2022,81.0,'e'),(2023,84.4,'e'),(2024,88.7,'e')],
  'US': [(2016,785.6,'r'),(2017,804.7,'r'),(2018,820.1,'r'),(2019,833.8,'r'),(2020,843,'e'),(2021,867,'e'),(2022,880.2,'r'),(2023,870,'e'),(2024,865,'e')],
  'CN': [(2016,509,'r'),(2019,577,'r'),(2022,779.8,'r'),(2023,927.6,'r'),(2024,986.4,'r'),(2025,1053.6,'r')]},
 'doctoral': {
  'KR': [(2016,13.9,'e'),(2017,14.3,'e'),(2018,14.7,'e'),(2019,15.3,'e'),(2020,16.1,'r'),(2021,16.4,'e'),(2022,17.8,'e'),(2023,17.7,'e'),(2024,18.7,'e')],
  'US': [(2016,177.9,'r'),(2017,181.4,'r'),(2018,184.1,'r'),(2019,187.6,'r'),(2020,190,'e'),(2021,194,'e'),(2022,203.9,'r'),(2023,205,'e'),(2024,206,'e')],
  'CN': [(2016,55,'r'),(2019,63,'r'),(2022,82.3,'r'),(2023,87.1,'r'),(2024,97.2,'r'),(2025,112.9,'r')]}}
NAMES = {'KR': 'Korea', 'US': 'United States', 'CN': 'China'}
D['grad'] = {}
for lvl, cs in G.items():
    D['grad'][lvl] = []
    for c, pts in cs.items():
        s = build(c, NAMES[c], pts, rate=False); base = s['obs'][0]['y']
        s['base'] = base
        for o in s['obs']: o['i'] = round(100 * o['y'] / base, 1)
        for f in s['fc']:
            for k in ('y', 'lo', 'hi'): f[k + 'i'] = round(100 * f[k] / base, 1)
        for t in s['trends']: t['y0i'] = round(100 * t['y0'] / base, 1); t['y1i'] = round(100 * t['y1'] / base, 1)
        D['grad'][lvl].append(s)
# --- Quarterly, 2025 vs 2026 ---
m26 = [43.6,43.3,43.6,43.7,43.8,43.9,44.2,44.1,44.0,42.9]
yoy = [-1.2,-1.0,-0.9,-1.6,-2.4,-1.7,-1.6,-1.0,-1.1,-1.7]
m25 = [round(a - b, 1) for a, b in zip(m26, yoy)]
nov25 = round(12 * 45.0 - sum(m25) - 44.3, 1)       # implied by the 2025 annual mean of 45.0
m25 += [nov25, 44.3]
gap = sum(yoy[-3:]) / 3
m26 += [round(m25[10] + gap, 1), round(m25[11] + gap, 1)]  # Nov-Dec 2026 nowcast
q = lambda m: [round(sum(m[i:i + 3]) / 3, 2) for i in (0, 3, 6, 9)]
D['quarterly'] = {
 'kr': {'label': 'Korea, employment rate of ages 15-29 (%)', 'y2025': q(m25), 'y2026': q(m26),
        's2025': ['d','d','d','e'], 's2026': ['r','r','r','f'], 'm2025': m25, 'm2026': m26},
 'us': {'label': 'United States, unemployment rate of recent graduates aged 22-27 (%)',
        'y2025': [5.8,5.3,5.3,5.7], 'y2026': [5.7,5.6,5.2,None], 's2025': ['r','r','r','r'], 's2026': ['r','r','r','f']}}
us = [5.8,5.3,5.3,5.7,5.7,5.6,5.2]
D['quarterly']['us']['y2026'][3] = round(us[-1] + 0.8 * (us[-1] - us[-2]) * 0.5, 2)
# --- Attainment level, 25-64, Korea vs OECD ---
D['level'] = {'cats': ['Short-cycle', "Bachelor's", "Master's", 'Doctoral'],
              'KR': [78.1, 80.1, 87.1, None], 'KRs': ['r','r','d',''], 'OECD': [83.4, 86.0, 90, 93], 'OECDs': ['r','r','r','r']}
# --- Strata ---
D['strata'] = {
 'jobs': {'cats': ['Ages 15-29, high AI exposure','Ages 15-29, lower exposure','Ages 50-59, high AI exposure','Ages 50-59, lower exposure'], 'v': [-268,-17,173,57]},
 'ind': {'cats': ['Information services','Publishing','Computer programming','Professional services'], 'v': [-31.4,-27.4,-16.6,-11.6]},
 'edu': {'cats': ['Jan 2019 to Oct 2022','Nov 2022 onwards'], 'univ': [8.2,7.0], 'jc': [8.0,5.4]},
 'age': {'cats': ['Ages 20-24','Ages 25-29','Ages 15-29'], 'aug': [-1.8,-0.5,-1.0], 'oct': [-3.6,-0.5,-1.7]},
 'us': {'cats': ['Ages 22-25, two most exposed quintiles','Ages 22-25, three least exposed quintiles'], 'v': [-11,10]}}
json.dump(D, open('research/data/early-career-employment.json', 'w'), separators=(',', ':'))
print(len(json.dumps(D)), 'bytes')
print('KR quarterly', D['quarterly']['kr']['y2025'], D['quarterly']['kr']['y2026'], 'nov25', nov25)
for s in D['kr_emp'] + D['kr_youth']: print(s['id'], s['obs'][-1], s['genai_slope'], [(f['x'], f['y'], f['lo'], f['hi']) for f in s['fc']])
for l in D['grad']:
    for s in D['grad'][l]: print(l, s['id'], s['obs'][-1]['y'], [(f['x'], f['y']) for f in s['fc']])
