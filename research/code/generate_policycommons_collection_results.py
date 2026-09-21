#!/usr/bin/env python3
"""Build the static v7.10 collection-results dashboard from local release files."""

from __future__ import annotations

from collections import Counter
from html import escape
from pathlib import Path

import pandas as pd


ROOT = Path("/Users/deep1003/Downloads/policycommons_local_enrichment_20260920_r1/final_augmented_release_v7_10_fulltext_ai_corrections")
MASTER = ROOT / "policycommons_augmented_master_final_v7_10.parquet"
PAIRS = ROOT / "document_country_pairs_final_v7_10.csv"
OUTPUT = Path(__file__).resolve().parents[1] / "policycommons-collection-results-v7-10.html"


def nonempty(series: pd.Series) -> pd.Series:
    return series.notna() & series.astype(str).str.strip().ne("")


def bar_chart(rows, title, note="", limit=20):
    rows = list(rows)[:limit]
    maximum = max((value for _, value in rows), default=1)
    bars = "".join(
        f"<div class='bar-row'><div class='bar-label'>{escape(str(label))}</div>"
        f"<div class='bar-track'><span style='width:{value/maximum*100:.3f}%'></span></div>"
        f"<div class='bar-value'>{value:,}</div></div>" for label, value in rows
    )
    return f"<section class='panel'><h2>{escape(title)}</h2><p class='note'>{escape(note)}</p>{bars}</section>"


def line_chart(rows, title, note=""):
    rows = list(rows)
    width, height, left, right, top, bottom = 860, 300, 55, 20, 25, 45
    inner_w, inner_h = width-left-right, height-top-bottom
    values = [v for _, v in rows]
    vmax = max(values) if values else 1
    points = []
    for i, (_, value) in enumerate(rows):
        x = left + (inner_w * i / max(len(rows)-1, 1))
        y = top + inner_h * (1 - value / vmax)
        points.append(f"{x:.1f},{y:.1f}")
    ticks = "".join(
        f"<text x='{left + inner_w*i/max(len(rows)-1,1):.1f}' y='{height-15}' text-anchor='middle'>{year}</text>"
        for i, (year, _) in enumerate(rows) if i in {0, len(rows)-1} or year % 5 == 0
    )
    grid = "".join(
        f"<line x1='{left}' x2='{width-right}' y1='{top+inner_h*(1-j/4):.1f}' y2='{top+inner_h*(1-j/4):.1f}'/><text x='{left-8}' y='{top+inner_h*(1-j/4)+4:.1f}' text-anchor='end'>{int(vmax*j/4):,}</text>"
        for j in range(5)
    )
    svg = f"<svg viewBox='0 0 {width} {height}' role='img' aria-label='{escape(title)}'><g class='grid'>{grid}</g><polyline points='{' '.join(points)}'/>{ticks}</svg>"
    return f"<section class='panel wide'><h2>{escape(title)}</h2><p class='note'>{escape(note)}</p>{svg}</section>"


master_columns = [
    "record_id", "title", "abstract", "publisher", "year", "url", "keywords", "topics",
    "country", "published_in_country_name", "institution_type_final", "language",
    "collection_categories", "query_id", "master_origin", "document_genre_protocol_3_7",
    "country_resolution_status", "ai_evidence_location", "ai_fulltext_review_status_v7",
    "format_status", "pairing_status", "national_policy_interest_scope", "human_form_review_v7_8",
]
master = pd.read_parquet(MASTER, columns=master_columns)
pairs = pd.read_csv(PAIRS, dtype=str)

country_counts = pairs["analysis_country"].value_counts().items()
institution_counts = pairs["institution_type"].fillna("missing").replace("", "missing").value_counts().items()
language_counts = master["language"].fillna("missing").replace("", "missing").value_counts().items()

category_counter = Counter()
for value in master.loc[nonempty(master["collection_categories"]), "collection_categories"]:
    category_counter.update(part.strip() for part in str(value).split(";") if part.strip())

year_numeric = pd.to_numeric(pairs["year"], errors="coerce")
year_counts = year_numeric[(year_numeric >= 1990) & (year_numeric <= 2026)].astype(int).value_counts().sort_index()
year_rows = [(year, int(year_counts.get(year, 0))) for year in range(1990, 2027)]

coverage_fields = [
    ("title", "Title"), ("abstract", "Abstract or summary"), ("publisher", "Publisher"),
    ("year", "Year"), ("url", "Policy Commons URL"), ("keywords", "RIS keywords"),
    ("topics", "CSV Topics"), ("country", "Raw CSV country / Published in"),
    ("institution_type_final", "Final institution type"), ("language", "Language"),
    ("collection_categories", "Collection category"), ("query_id", "Query identifier"),
]
coverage = [(label, int(nonempty(master[col]).sum()), nonempty(master[col]).mean()*100) for col, label in coverage_fields]

country_table = "".join(f"<tr><td>{escape(code)}</td><td>{count:,}</td><td>{count/len(pairs)*100:.2f}%</td></tr>" for code, count in pairs.analysis_country.value_counts().items())
year_table = "".join(f"<tr><td>{year}</td><td>{count:,}</td></tr>" for year, count in sorted(Counter(pd.to_numeric(pairs.year, errors='coerce').dropna().astype(int)).items(), reverse=True))
coverage_table = "".join(f"<tr><td><code>{escape(label)}</code></td><td>{count:,}</td><td>{rate:.2f}%</td><td>{len(master)-count:,}</td></tr>" for label, count, rate in coverage)

modules = [
    ("POCO_POGO", "World Governments", "R1, R2, R3"),
    ("POCO_PCWL", "World Cities / World Cities and Local…", "R2, R3"),
    ("POCO_POHE", "Public Health and Social Care", "R2, R3"),
    ("POCO_PSPL", "N.A. State, Provincial, and Territorial Governments", "R2, R3"),
    ("POCO_ALL", "Global Think Tanks", "R3 only"),
]
module_rows = "".join(f"<tr><td><code>{code}</code></td><td>{escape(name)}</td><td>{routes}</td><td>Not recoverable at record level in v7.10</td></tr>" for code, name, routes in modules)

html = f"""<!doctype html><html lang='en-GB'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Policy Commons v7.10 Collection Results | Youngsam Chun</title><meta name='description' content='Charts and tables describing the cleaned Policy Commons v7.10 master and final country-analysis view.'>
<link rel='stylesheet' href='../assets/style.css?v=4'><style>
.dash{{max-width:1240px;margin:0 auto;padding:40px 24px 80px}}.lead{{max-width:1000px}}.kpis{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:20px 0}}.kpi{{border:1px solid #ddd;padding:15px;background:#fff}}.kpi b{{display:block;font-size:25px;color:#a66b00}}.kpi span,.note{{color:#666;font-size:13px}}.grid2{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}}.panel{{border:1px solid #ddd;padding:18px;min-width:0;background:#fff}}.panel.wide{{grid-column:1/-1}}.panel h2{{font-size:18px;margin-top:0}}.bar-row{{display:grid;grid-template-columns:minmax(105px,1.4fr) minmax(120px,3fr) 68px;gap:9px;align-items:center;margin:8px 0;font-size:13px}}.bar-label{{overflow-wrap:anywhere}}.bar-track{{height:14px;background:#edf0f2}}.bar-track span{{display:block;height:100%;background:#b57a16}}.bar-value{{text-align:right;font-variant-numeric:tabular-nums}}svg{{width:100%;height:auto}}svg polyline{{fill:none;stroke:#b57a16;stroke-width:3}}svg .grid line{{stroke:#e5e5e5;stroke-width:1}}svg text{{font:11px system-ui;fill:#666}}details{{border:1px solid #ddd;padding:12px;margin:16px 0}}summary{{cursor:pointer;font-weight:650}}.scroll{{overflow:auto;max-height:620px;margin-top:12px}}table{{width:100%;border-collapse:collapse;table-layout:fixed}}th,td{{padding:8px;border-bottom:1px solid #ddd;text-align:left;overflow-wrap:anywhere}}th{{background:#f5f6f7}}.warning{{border-left:5px solid #ad791c;background:#fff9eb;padding:14px 16px;margin:18px 0}}code{{white-space:normal;overflow-wrap:anywhere}}@media(max-width:780px){{.grid2,.kpis{{grid-template-columns:1fr}}.panel.wide{{grid-column:auto}}.bar-row{{grid-template-columns:100px 1fr 58px}}.dash{{padding:25px 14px}}}}
</style></head><body><nav class='topbar'><div class='topbar-inner'><span class='brand'>Youngsam Chun</span><a class='nav active' href='../research.html'>Research</a></div></nav><main class='dash'>
<p class='small'><a href='policycommons-ris-collection.html'>Collection and cleaning workflow</a> / Results</p><h1>Policy Commons v7.10 cleaned collection results</h1><p class='lead'>Descriptive status of the 269,853-record canonical master and the authoritative 182,010-row national document-country analytical file. Values are computed from the frozen local v7.10 files, not from a later live query.</p>
<div class='kpis'><div class='kpi'><b>{len(master):,}</b><span>canonical document versions</span></div><div class='kpi'><b>{len(pairs):,}</b><span>final document-country rows and unique documents</span></div><div class='kpi'><b>{pairs.analysis_country.nunique():,}</b><span>analytical country or jurisdiction codes</span></div><div class='kpi'><b>{len(master.columns):,} / 162</b><span>profiled columns / total master columns</span></div></div>
<div class='warning'><strong>Module limitation.</strong> The final v7.10 master does not contain a dedicated record-level module code. Module-specific record counts therefore cannot be reconstructed reliably from this release. The table below reports which frozen collection routes used each module and makes the missing linkage explicit. No module counts are inferred from publisher, title or country.</div>
<div class='grid2'>
{bar_chart(country_counts, 'Leading analytical countries and jurisdictions', 'Top 20 of 135 codes. Counts use the final document-country file.', 20)}
{bar_chart(institution_counts, 'Institution types in the final analytical view', 'Classification recorded in the 182,010-row final pair file.', 12)}
{line_chart(year_rows, 'Documents by year, 1990–2026', 'Years outside this plotting window and 222 missing years remain in the detailed table.')}
{bar_chart(language_counts, 'Languages in the canonical master', 'Top 15 raw or normalised language values in the 269,853-row master.', 15)}
{bar_chart(category_counter.most_common(), 'Search-route collection categories', 'Multi-valued categories are split and whole-counted. These are query categories, not Policy Commons modules.', 15)}
{bar_chart([(label, count) for label, count, _ in coverage], 'Representative field coverage', 'Non-empty values; both null and empty strings count as missing.', 20)}
{bar_chart(master.master_origin.value_counts().items(), 'Master origin', 'Origin of all 269,853 canonical document versions.', 10)}
{bar_chart(master.format_status.fillna('missing').replace('', 'missing').value_counts().items(), 'Available export formats', 'RIS-only, exact RIS/CSV pairs and CSV-only states in the augmented master.', 10)}
{bar_chart(master.document_genre_protocol_3_7.fillna('missing').replace('', 'missing').value_counts().items(), 'Document genre values', 'Protocol 3.7 genre values retained in the final master.', 10)}
{bar_chart(master.country_resolution_status.fillna('missing').replace('', 'missing').value_counts().items(), 'Country-resolution status values', 'Top final-master status values. Historical correction statuses remain visible for audit.', 12)}
{bar_chart(pairs.release_source.fillna('missing').replace('', 'missing').value_counts().items(), 'Final analytical rows by release source', 'Provenance of the 182,010 authoritative document-country rows.', 10)}
{bar_chart(pairs.country_method.fillna('missing').replace('', 'missing').value_counts().items(), 'Final country-attribution methods', 'Rules that supplied the analytical country in the final pair file.', 15)}
{bar_chart(pairs.national_policy_interest_scope.fillna('missing').replace('', 'missing').value_counts().items(), 'National policy-interest scope', 'Final pair-file eligibility scope.', 10)}
{bar_chart(pairs.human_form_review_v7_8.fillna('missing').replace('', 'missing').value_counts().items(), 'Human document-form status', 'Final retained proceedings are shown separately from records not individually reviewed.', 10)}
</div>
<details open><summary>Module coverage and record-linkage limitation</summary><div class='scroll'><table><thead><tr><th>Module</th><th>Displayed name</th><th>Frozen routes</th><th>Record-level count</th></tr></thead><tbody>{module_rows}</tbody></table></div><p class='note'>R1 is the 16 September World Governments run; R2 is the four-module AIGOV5 paired RIS/CSV run; R3 is the five-module 1950–2026 broad collection. A future release should add a many-to-many <code>record_module_link</code> table derived from frozen source manifests.</p></details>
<details><summary>Complete country and jurisdiction table</summary><div class='scroll'><table><thead><tr><th>Code</th><th>Documents</th><th>Share</th></tr></thead><tbody>{country_table}</tbody></table></div></details>
<details><summary>Complete year table</summary><div class='scroll'><table><thead><tr><th>Year</th><th>Documents</th></tr></thead><tbody>{year_table}</tbody></table></div></details>
<details><summary>Representative column completeness</summary><div class='scroll'><table><thead><tr><th>Field</th><th>Non-empty</th><th>Coverage</th><th>Missing</th></tr></thead><tbody>{coverage_table}</tbody></table></div><p class='note'>The full 162-variable dictionary is available from the workflow page. The dashboard profiles representative attributes only, while retaining exact denominators.</p></details>
<details><summary>Data scope and interpretation</summary><ul><li>Country, year, institution, release-source and attribution-method charts use the authoritative final document-country file.</li><li>Language, query category, master origin, format, genre, resolution status and field completeness use the canonical master.</li><li>Documents from documented AI-oriented searches remain included under the high-recall rule even when exported metadata has no AI term.</li><li>Counts are descriptive collection status, not estimates of national policy quality or policy intensity.</li><li>Territories and project-normalised jurisdictions are included among the 135 analytical codes.</li></ul></details>
<p class='small'>Generated from <code>policycommons_augmented_master_final_v7_10.parquet</code> and <code>document_country_pairs_final_v7_10.csv</code>. Generator: <a href='code/generate_policycommons_collection_results.py'>source code</a>.</p><footer>© 2026 Youngsam Chun · <a href='../research.html'>Research overview</a></footer></main></body></html>"""

OUTPUT.write_text(html, encoding="utf-8")
print(f"wrote {OUTPUT}")
