"""Keep one curated publication set across the website and cached notebook bundle."""
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
        'M2': '빈 마름모는 결합 효과 11−00, 채운 원은 기존 세 주요 대비다. 결합 효과 +22.72%p는 상호작용 −1.94%p와 다르다. 모든 구간은 보정 전 95% 구간이며 Holm 보정은 기존 세 검정에만 적용한다.',
        'M3': '같은 문항·선택지 순서의 00 대비 내부 유사도 변화. 앞의 표는 고정 방향의 코사인 유사도와 실제 경계 접촉 여부다. 영역당 417칸은 139문항×3선택지 순서이며, 화면 픽셀이나 독립적인 417개 문항을 뜻하지 않는다.',
        'M4': '실제 한국어 입력의 토큰별 내부 유사도. 글자 배경은 FA 유사도가며 단어의 인과 기여도가 아니다.',
        'S1': '축 간 유사도와 보류 문장 진단. 축의 겹침과 제한된 구분 타당성을 공개한다.',
        'S3': '세 방향의 평균 유사도 변화와 문항별 응답 변화의 연관성을 구분한다. 91개 군집·10,000회 부트스트랩의 보정 전 95% 구간을 표시했다. 약한 상관은 인과적 무효를 뜻하지 않으며, 기존 지표를 변경하지 않았다.',
        'S2': '139문항의 절대 UN·FA 정렬과 00 대비 변화. 범주는 색으로만 구분하며 각 패널의 선은 전체 문항 OLS 적합선이다.'}
    def artwork(entry):
        stem = entry['website_stem']
        version = sha(SITE / (stem + '.png'))[:10]
        title = entry['id'] + '. ' + entry['title']
        preface = (BASE / 'atlas_geometry_explainer.html').read_text() if entry['id'] == 'M3' else ''
        return preface + (f'<figure data-publication-id="{entry["id"]}"><a href="{stem}.svg"><img '
                f'src="{stem}.png?v={version}" loading="lazy" alt="{title}"/></a>'
                f'<figcaption><strong>{title}</strong> · {captions[entry["id"]]}</figcaption>'
                f'<p class="links"><a href="{stem}.pdf">PDF</a><a href="{stem}.svg">SVG</a>'
                f'<a href="{stem}.png">600 dpi PNG</a></p></figure>')
    model = soup.find(id='model')
    model.find('h2').insert_after(fragment(artwork(figures[0])))
    results = soup.find(id='results')
    results.find('h2').insert_after(fragment('<details id="behavior-figure"><summary>본문 M2 · 행동 결과</summary>' + artwork(figures[1]) + '</details>'))
    main = '<section id="publication-main"><h2>감정 축 유사도 · 본문 그림</h2><p>행동 효과와 내부 유사도는 별도로 해석한다. 유사도는 작성한 개념 방향과의 코사인이며 실제 감정 경험이나 행동의 원인을 입증하지 않는다.</p>'
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
    supplementary = '<section id="publication-supplement"><h2>별첨 그림</h2><p>축 검증, 범주별 유사도, 세 개념 방향의 동반 변화를 별첨으로 제공한다.</p>'
    for entry in figures[4:]:
        supplementary += f'<details><summary>{entry["id"]} · {entry["title"]}</summary>' + artwork(entry) + '</details>'
    supplementary += '<div id="s3-interpretation">' + (BASE / 'representation_analysis/three_axis_supplement/output/Interpretation.html').read_text() + '</div><p id="s3-source-links" class="links"><a href="data/three-axis/source_data.csv">문항별 측정값</a><a href="data/three-axis/behavior_associations.csv">평균 변화와 상관·신뢰구간</a><a href="data/three-axis/contrast_sensitivity.csv">세 대비 전체 민감도 분석</a><a href="data/three-axis/alignment_change_intervals.csv">유사도 간 상관·구간</a><a href="data/three-axis/bootstrap_plan.json">사후 분석 설정</a><a href="data/three-axis/Expert_review.md">세 전문 역할의 AI 검토</a><a href="data/three-axis/Captions_and_methods.md">영문 캡션과 방법</a></p>'
    supplementary += '<p class="links"><a href="data/category/category_summary.csv">범주별 수치</a><a href="data/category/representation_behavior_associations.csv">행동 변화와의 관계</a><a href="data/category/fitted_lines.csv">적합선 계수</a></p></section>'
    rep.insert_after(fragment(supplementary))
    selection = '<details id="publication-selection"><summary>그림 구성과 공통 표기</summary><p>본문 4개, 별첨 3개를 사용한다. 조건은 00·01·10·11 순서이며 회색·파랑·빨강·보라색으로 표시한다. 활성·유사도는 짙은 적색에서 밝은 노란색이고, 단위와 범위는 각각의 범례를 따른다. KoBBQ 범주 산점도는 범주별 색을 사용한다. 모든 PNG는 600 dpi이며 PDF·SVG를 함께 제공한다.</p><a href="data/figure_catalog.json">그림 목록</a></details>'
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
    for section_id, title in [('publication-main', '7. 감정 축 유사도 · 본문 그림'), ('representations', '8. 측정 방법'), ('publication-supplement', '9. 별첨 그림'), ('implications', '10. 학술적 함의'), ('limitations', '11. 한계와 후속 검증'), ('references', '12. 참고문헌')]:
        soup.find(id=section_id).find('h2').string = title
    s3 = soup.find('figure', attrs={'data-publication-id': 'S3'})
    if s3:
        for identity in ('s3-interpretation', 's3-source-links'):
            node = soup.find(id=identity)
            if node:
                s3.find_parent('details').append(node.extract())
    combined_data = json.loads((BASE / 'figures/behavior_contrasts_display.json').read_text())['combined']
    for identity in ('combined-effect-summary', 'combined-effect-explanation', 'combined-effect-formula'):
        node = soup.find(id=identity)
        if node:
            node.decompose()
    abstract = soup.find(id='results-current')
    abstract.find(class_='brief-i').find('em').string = 'UN이 없을 때 FA의 추가 효과는 +4.92%p, 있을 때는 +2.98%p다. 그 차이가 −1.94%p다.'
    for paragraph in abstract.find_all('p', recursive=False):
        if paragraph.get_text().startswith(('두 문구 요소 모두', '11 결합 조건은')):
            paragraph.string = '11 결합 조건은 00 대비 정보 부족 응답 확률을 +22.72%p 높였다. 음의 상호작용은 전체 효과가 감소했다는 뜻이 아니라, 두 단독 효과를 중립 기준에서 더한 값보다 결합 효과가 작다는 뜻이다. 고정 문구와 선별 문항의 결과이며 실제 정서나 자기보존 동기를 입증하지 않는다.'
    abstract.find(class_='result-brief').insert_after(fragment(
        '<p id="combined-effect-summary"><strong>UN + FA 결합 효과 · 11−00 = +22.72%p</strong> '
        '(95% 구간 +19.13~+26.34%p). 결합 조건의 확률은 61.39%, 기준은 38.67%다. '
        '추가 기술적 대비이며 기존 세 주요 검정에 포함되지 않는다.</p>'))
    explanation = '<div id="combined-effect-explanation"><p><strong>결합 효과와 상호작용을 구분한다.</strong> 결합 효과는 두 문구를 함께 넣은 11과 기준 00의 차이이며, 상호작용은 FA의 추가 효과가 UN 유무에 따라 달라지는 정도다.</p><div class="equation">결합 효과 = Y<sub>11</sub> − Y<sub>00</sub> = +22.72%p<br/>상호작용 = (Y<sub>11</sub> − Y<sub>10</sub>) − (Y<sub>01</sub> − Y<sub>00</sub>) = 2.98 − 4.92 = −1.94%p</div><p>두 단독 효과를 기준 00에서 더하면 11의 가산적 예상치는 63.32%이고 실제 값은 61.39%다. 결합 조건은 네 조건 중 가장 높지만 가산적 예상치보다 1.94%p 낮다. UN·FA의 평균 효과 +18.76%p와 +3.95%p의 합은 결합 효과 +22.72%p와 같으므로, 여기에 상호작용을 다시 더하지 않는다.</p><p>결합 효과는 같은 139문항·91개 군집·10,000회 대응 군집 부트스트랩으로 구간을 계산한 추가 요약이다. 기존 세 주요 대비의 p값과 Holm 보정 범위는 바꾸지 않았다.</p><a href="data/behavior/contrasts_display.json">결합 효과와 주요 대비의 수치·출처</a></div>'
    soup.find(id='behavior-figure').append(fragment(explanation))
    soup.find(id='model').append(fragment('<p id="combined-effect-formula">별도의 결합 효과는 Δ<sub>combined</sub> = Y<sub>11</sub> − Y<sub>00</sub>이다. 위의 상호작용 대비와 구분한다.</p>'))
    for tag in soup.find_all('a', href=True):
        relative = tag['href'].split('?')[0]
        if relative.startswith('figures/') and (SITE / relative).is_file():
            tag['href'] = relative + '?v=' + sha(SITE / relative)[:10]
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

The study uses four main-text figures (M1–M4) and three supplementary figures (S1–S3), listed in figure_catalog.json. Figure display reads existing artwork and never calls a plotting builder. Set SHOW_SUPPLEMENT=True to display the three supplements. Progress is shown as tables. Explicit measurement flags default to False; no model inference or background jobs start automatically.

Before M3, the notebook and website show a cosine-similarity/contact table and an audited explanation of geometry and observed cells. Geometry is PCA plus an equal-area power diagram, not correlation thresholding; each cell is one item–choice-rotation–axis value.

Supplement S3 relates FA, desperation, and anger changes in cosine similarity to behavioral changes using existing observations only. It is a post hoc descriptive analysis with 10,000 paired template-cluster bootstrap replicates and pointwise unadjusted 95% intervals, not a test of independent or combined causal emotion effects. The existing outcome and three primary hypothesis tests are unchanged.

The combined effect (11 minus 00) is an additional descriptive contrast, distinct from the interaction difference in differences. Its unadjusted 95% interval uses the same paired cluster bootstrap. The three primary tests and their Holm adjustment are unchanged.

All charts use American English, consistent 00/01/10/11 colors, 600 dpi PNG and vector PDF/SVG exports. The original Korean stimuli remain Korean. Internal cosine similarity is not evidence of experienced emotion or emotion-specific causal mediation.

The ZIP contains the same notebook source without embedded output images, with each of the seven PNGs stored once, code and cached measurements. Execute display cells to view them. The separately downloadable notebook retains four main-text figures as saved outputs. Unzip beside uncertainty_self_threat_139/ and threat_139_pilot/. Models and model weights are not included. PDF/SVG files are downloaded individually from the website.

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
                     'l14_methods.html', 'emotion_atlas_section.html', 'atlas_geometry_explainer.html', 'fear_anxiety_review.html',
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
            if file.suffix not in ('.py', '.csv', '.json', '.md', '.npz') and file.name != 'Interpretation.html':
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
