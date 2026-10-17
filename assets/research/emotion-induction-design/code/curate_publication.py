"""Keep one six-figure publication set across the website and cached notebook bundle."""
from pathlib import Path
import hashlib
import json
import zipfile
import nbformat
from bs4 import BeautifulSoup
BASE = Path(__file__).resolve().parent
SITE = Path('/Users/deep1003/data3/deep1003.github.io/assets/research/emotion-induction-design')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def curate(records):
    catalog = json.loads((BASE / 'figure_catalog.json').read_text())
    figures = catalog['figures']
    allowed = {f['website_stem'] + '.' + ext for f in figures for ext in ('png', 'pdf', 'svg')}
    soup = BeautifulSoup((SITE / 'index.html').read_text(), 'html.parser')
    # Remove all old artwork once, including duplicate download paragraphs.
    for figure in list(soup.find_all('figure')):
        figure.decompose()
    for paragraph in list(soup.select('p.links')):
        for link in list(paragraph.find_all('a')):
            if link.get('href', '').startswith('figures/'):
                link.decompose()
        if not paragraph.get_text(strip=True):
            paragraph.decompose()
    for identity in ('publication-main', 'publication-supplement', 'publication-selection',
                     'standalone-panels', 'concept-figure', 'axis-validity', 'token-figure',
                     'prompt-text-plate', 'l14-axis-heatmap', 'category-map', 'study-color-guide',
                     'behavior-figure', 'seven-axis-intervention'):
        node = soup.find(id=identity)
        if node:
            node.decompose()
    def fragment(text):
        return BeautifulSoup(text, 'html.parser')
    captions = {
        'M1': '同一139문항과 세 선택지 순서를 사용한 대응 2×2 설계.'.replace('同一', '동일한 '),
        'M2': '조건 평균과 주요 대비. 95% 구간은 보정 전, 세 주요 대비의 p값은 Holm 보정이다.',
        'M3': '같은 문항·선택지 순서의 00 대비 내부 개념 정렬 변화. 경계는 시각화용 근사이며 정서의 생물학적 경계가 아니다.',
        'M4': '실제 한국어 입력의 토큰별 내부 정렬. 글자 배경은 FA 정렬이며 단어의 인과 기여도가 아니다.',
        'S1': '축 간 유사도와 보류 문장 진단. 축의 겹침과 제한된 구분 타당성을 공개한다.',
        'S2': '139문항의 절대 UN·FA 정렬과 00 대비 변화. 범주는 색으로만 구분하며 각 패널의 선은 전체 문항 OLS 적합선이다.'}
    def artwork(entry):
        stem = entry['website_stem']
        version = sha(SITE / (stem + '.png'))[:10]
        title = entry['id'] + '. ' + entry['title']
        return (f'<figure data-publication-id="{entry["id"]}"><a href="{stem}.svg"><img '
                f'src="{stem}.png?v={version}" loading="lazy" alt="{title}"/></a>'
                f'<figcaption><strong>{title}</strong> · {captions[entry["id"]]}</figcaption>'
                f'<p class="links"><a href="{stem}.pdf">PDF</a><a href="{stem}.svg">SVG</a>'
                f'<a href="{stem}.png">600 dpi PNG</a></p></figure>')
    model = soup.find(id='model')
    model.find('h2').insert_after(fragment(artwork(figures[0])))
    results = soup.find(id='results')
    results.find('h2').insert_after(fragment('<details id="behavior-figure"><summary>본문 M2 · 행동 결과</summary>' + artwork(figures[1]) + '</details>'))
    main = '<section id="publication-main"><h2>내부 개념 정렬 · 본문 그림</h2><p>행동 효과와 내부 정렬은 별도로 해석한다. 정렬은 작성한 개념 방향과의 코사인이며 실제 감정 경험이나 행동의 원인을 입증하지 않는다.</p>'
    for entry in figures[2:4]:
        main += f'<details><summary>본문 {entry["id"]} · {entry["title"]}</summary>' + artwork(entry) + '</details>'
    main += '</section>'
    results.insert_after(fragment(main))
    rep = soup.find(id='representations')
    intro = rep.find('p', recursive=False)
    if intro:
        intro.string = '측정 수식과 검증 조건은 아래에 접어 제시한다. 동일 자료의 PCA·UMAP·확대판은 중복 표시하지 않는다. 원자료와 좌표, 검증 수치는 내려받기 자료에 보존했다.'
    atlas = soup.find(id='emotion-atlas')
    if atlas:
        atlas.find('summary').string = '아틀라스 경계·계층군집·차원 축소의 방법과 한계'
    supplementary = '<section id="publication-supplement"><h2>별첨 그림</h2><p>본문 해석을 검증하는 두 그림만 제공한다.</p>'
    for entry in figures[4:]:
        supplementary += f'<details><summary>{entry["id"]} · {entry["title"]}</summary>' + artwork(entry) + '</details>'
    supplementary += '<p class="links"><a href="data/category/category_summary.csv">범주별 수치</a><a href="data/category/representation_behavior_associations.csv">행동 변화와의 관계</a><a href="data/category/fitted_lines.csv">적합선 계수</a></p></section>'
    rep.insert_after(fragment(supplementary))
    selection = '<details id="publication-selection"><summary>그림 구성과 공통 표기</summary><p>본문 4개, 별첨 2개를 사용한다. 조건은 00·01·10·11 순서이며 회색·파랑·빨강·보라색으로 표시한다. 활성·유사도는 짙은 적색에서 밝은 노란색이고, 단위와 범위는 각각의 범례를 따른다. KoBBQ 범주 산점도는 범주별 색을 사용한다. 모든 PNG는 600 dpi이며 PDF·SVG를 함께 제공한다.</p><a href="data/figure_catalog.json">그림 목록</a></details>'
    soup.find('nav').insert_after(fragment(selection))
    for link in list(soup.select('nav a')):
        if link.get('href') == '#category-map':
            link['href'] = '#publication-supplement'
            link.string = '별첨'
    # No stale duplicate figure links survive the active page.
    for link in list(soup.find_all('a')):
        href = link.get('href', '').split('?')[0]
        if href.startswith('figures/') and href not in allowed:
            link.decompose()
    for node in soup.find_all('details'):
        node.attrs.pop('open', None)
    for section_id, title in [('publication-main', '7. 내부 개념 정렬 · 본문 그림'), ('representations', '8. 측정 방법'), ('publication-supplement', '9. 별첨 그림'), ('implications', '10. 학술적 함의'), ('limitations', '11. 한계와 후속 검증'), ('references', '12. 참고문헌')]:
        soup.find(id=section_id).find('h2').string = title
    (SITE / 'index.html').write_text(str(soup))
    # Copies are backed up before this first curation. The original local outputs remain intact.
    for file in (SITE / 'figures').rglob('*'):
        if file.is_file() and str(file.relative_to(SITE)) not in allowed:
            file.unlink()
    records = [r for r in records if not r['website'].startswith('figures/') or r['website'] in allowed]
    for source, relative in [('figure_catalog.json', 'data/figure_catalog.json'),
                             ('publication_catalog.py', 'code/publication_catalog.py'),
                             ('curate_publication.py', 'code/curate_publication.py'),
                             ('sync_publication_assets.py', 'code/sync_publication_assets.py')]:
        import shutil
        path = SITE / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(BASE / source, path)
        records.append({'source': str(BASE / source), 'website': relative, 'sha256': sha(path)})
    readme = '''# Manual notebook workflow

The study uses four main-text figures (M1–M4) and two supplementary figures (S1–S2), listed in figure_catalog.json. Figure display reads existing artwork and never calls a plotting builder. Set SHOW_SUPPLEMENT=True to display the two supplements. Progress is shown as tables. Explicit measurement flags default to False; no model inference or background jobs start automatically.

All charts use American English, consistent 00/01/10/11 colors, 600 dpi PNG and vector PDF/SVG exports. The original Korean stimuli remain Korean. Internal alignment is not evidence of experienced emotion or emotion-specific causal mediation.

The ZIP contains the same notebook source without embedded output images, with each of the six PNGs stored once, code and cached measurements. Execute display cells to view them. The separately downloadable notebook retains four main-text figures as saved outputs. Unzip beside uncertainty_self_threat_139/ and threat_139_pilot/. Models and model weights are not included. PDF/SVG files are downloaded individually from the website.

Raw measurements, frozen collectors, hashes, and numerical checks are preserved. Older figure variants are retained in the local timestamped recovery backup and original analysis folders, outside the active figure set. Optional historic renderers remain available as implementation records and are not called by the default notebook.
'''
    (BASE / 'MANUAL_WORKFLOW.md').write_text(readme)
    (SITE / 'downloads/MANUAL_WORKFLOW.md').write_text(readme)
    notebook = BASE.parent / 'uncertainty_self_threat_139.ipynb'
    clean = nbformat.read(notebook, 4)
    for cell in clean.cells:
        if cell.cell_type == 'code':
            cell.outputs = []
            cell.execution_count = None
    bundle = SITE / 'downloads/notebook_cached_analysis.zip'
    with zipfile.ZipFile(bundle, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.writestr(notebook.name, nbformat.writes(clean))
        archive.write(BASE.parent / 'threat_139_pilot/items_139.csv', 'threat_139_pilot/items_139.csv')
        for file in BASE.glob('*.py'):
            if file.name != 'run_notebook.py':
                archive.write(file, Path(BASE.name) / file.name)
        for name in ['figure_catalog.json', 'color-specification.json', 'MANUAL_WORKFLOW.md',
                     'l14_methods.html', 'emotion_atlas_section.html', 'fear_anxiety_review.html',
                     'fear_anxiety_expert_review.md', 'axis_intervention/protocol.json']:
            archive.write(BASE / name, Path(BASE.name) / name)
        for entry in figures:
            relative = entry['local_stem'] + '.png'
            archive.write(BASE / relative, Path(BASE.name) / relative)
        for file in (BASE / 'results/a8e92be4014f').iterdir():
            if file.suffix in ('.csv', '.json', '.md'):
                archive.write(file, Path(BASE.name) / file.relative_to(BASE))
        for file in (BASE / 'representation_analysis').rglob('*'):
            if not file.is_file() or any(p in file.parts for p in ('references', 'hidden', 'chunks', '__pycache__', 'loading_recovery')):
                continue
            if file.suffix not in ('.py', '.csv', '.json', '.md', '.npz'):
                continue
            if file.suffix == '.npz' and file.parent.name == 'output':
                continue
            if file.parent.name in ('cb967efdc2e8', '93cf36e80cd1'):
                continue
            archive.write(file, Path(BASE.name) / file.relative_to(BASE))
    for relative in ['downloads/MANUAL_WORKFLOW.md']:
        records.append({'source': str(BASE / 'MANUAL_WORKFLOW.md'), 'website': relative, 'sha256': sha(SITE / relative)})
    for record in records:
        path = SITE / record['website']
        record['sha256'] = sha(path)
    return records
