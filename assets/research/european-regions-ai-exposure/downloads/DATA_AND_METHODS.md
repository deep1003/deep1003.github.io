# European Regions dashboard methods and data

Updated 25 November 2026. This is an exploratory working study, not a monthly European software-payroll database.

## Binding source rule


Our THAIE uses the GPT5 2025 task-capability benchmark and H50=203.012577 minutes, with official O*NET-SOC/ESCO/ISCO transfer. It is retrospective potential exposure, not actual adoption in 2022. ISCO3 scores are averaged to broader Eurostat occupation classes where detailed employment is unavailable. This aggregation is a proxy and does not recover unobserved within-class task weights.

## Official sources newly downloaded

- Eurostat lfsa_egai2d, ages15–64, three sex categories,2020–2025. National two-digit occupation counts, not regional software occupations.
- Eurostat lfsa_egais, broad age/sex and one-digit occupation,2020–2025. Ten scored major occupation groups are coarse; quintiles differ from the detailed table.
- UK ONS3713, published11November2026. SOC2010/SOC2020 software counts and NUTS2/ITL2 geography, annual windows ending June2020–2026. Published national totals are used rather than summing suppressed regions. No pre-2022 index is linked across the SOC transition. New2025-geography areas without a2022 baseline have no index. Same code is not proof of a harmonised historical boundary.
- Sweden SCB YREG57BAS / TAB4435, annual occupation3×age×sex×county2020–2024. Exact software developers SSYK2512 are instead taken from YREG60BAS, with sex but no age. Native SSYK251 age curves are broader and cannot be labelled exact software developers. Source2023 introduces model-imputed occupations and an expanded age population; common16–64 bands are maintained in the broader age profiles, but not in the exact all-source-age table.
- Sweden SCB ArbStatusM, actual monthly total employment by county, age and sex, January2020–August2026. This is all-occupation employment, never software headcounts. Regional THAIE uses deterministic four-digit occupation links and own scores in2022, covering about67–78% of published occupational employment mass. Unscored mass is not treated as zero exposure. The series are not seasonally adjusted.
- Finland StatFin115s, occupation×region of residence×sex2020–2024. ISCO251 is a broader software/application group, not an age-specific exact software-developer occupation.
- Previous Eurostat regional source supports a balanced2020–2025 cohort of237NUTS2 regions in27EU countries, with ages15–24 and55–64. Exposure is the prior fixed own-THAIE regional ranking; classification vintage and public-cell scope limits remain. UK is not inserted with incompatible age outcomes.

## Construction

Monthly index=100×count/mean of all12monthly counts in2022. Annual index=100×count/published2022count, except that the UK2022label denotes the annual window ending June2022. Aggregate group counts are summed first and then indexed. They are not unweighted averages of local indices.

A fixed2022region ranking groups Swedish counties. Occupational quintiles rank the scored occupations equally. These two exposure units are never pooled. One occupation carries one fixed score and cannot identify five exposure classes internally.

Occupation-based panels use complete occupation support over all displayed years and both source sexes, within geography and age. Missing and suppressed cells are not filled with zero. Genuine source zeros are retained. Excluding an incomplete occupation can make the retained population selective, especially in small areas and narrow ages. Crosswalk ambiguity is retained in the audit and not allocated mechanically.

Requested ages22–25,26–30,31–34,35–40,41–49,50+ are not jointly acquired with month, region, occupation and sex. The actual source bands are shown in all charts. Annual observations are not interpolated to months. Broad software groups, ICT professionals and exact software developers have separate labels.

## Interpretation

Curves are descriptive employment indices, not causal AI effects. The November2022marker is contextual. Samples, definitions and observation windows differ across countries. Source sex categories do not measure gender identity. Age-cohort employment changes do not identify the same worker's transitions, hiring or retirement flows. Provider sampling/model uncertainty is not removed by indexing.

Previous statistical evidence is separately labelled and available in the six-page PDF. It uses own THAIE, European official data and retrospective correction families. Productivity associations do not establish AI productivity gains; no additional duration-score validity beyond contentE is established. Null and timing-sensitive age results remain visible.

## Reproduce

The reproduction ZIP includes seven official raw source snapshots, our transferredISCO3score table, official crosswalk-derived mapping, the public regional aggregate input, scripts and source hashes. No personal records are included. Install numpy,pandas,openpyxl,matplotlib, then run `python scripts/build.py` from the extracted folder to rebuild source-grain indices offline into `site/data/` and `derived/`. Source endpoints are recorded in metadata. Collection scripts may use the original project layout; offline rebuilding uses bundled snapshots and inputs.

The HTML uses native SVG with no third-party chart library. Current chart values and SVG can be exported directly. Validation checks sources, raw-source reconciliation, baseline arithmetic, keys, cohort support, score lineage and index dimensions without displaying charts.


## 25 November 2026 all-age update

The NUTS-2 explorer now provides all 12 native age bands on the same 208-region balanced 2020–2025 cohort. Employment is summed within the original fixed 2022 regional THAIE quintiles and divided by the corresponding 2022 sum. No quintile ranks are re-estimated after cohort restriction. Q5 is dark red and thicker; Q1–Q4 remain visible in muted greys. Overlapping age totals are not additive. No manuscript changes.


## UK monthly follow-up, 25 November 2026

ONS/HMRC PAYE RTI November2026 workbook provides actual monthly, seasonally adjusted payrolled employees. We downloaded and extracted January2020–October2026 for41 source NUTS2 codes,179 NUTS3 codes and6 national age groups. All18,614 extracted counts are numeric, keys are unique, and every index denominator contains12 observed2022 months. Region tables and national age tables are separate margins. These payroll counts exclude self-employed workers and do not identify occupation or sex. No monthly software-occupation index or regional THAIE quintiles are inferred. The native geography vintage is retained and is not silently converted to ITL2025. The default Europe-wide monthly view reports non-availability; users may select the genuine annual208-region panel or the distinct UK monthly payroll source. ONS has received a request for free data feasibility, with no chargeable work authorised.

Source https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/realtimeinformationstatisticsreferencetableseasonallyadjusted


## European overview and drilldown

The initial panel now displays the observed annual European overview, ages15+, on the fixed208-region cohort. Geography selections include27 supported countries and208 individual NUTS2 regions. Women and men retain that same cohort. Any aggregate with a missing or suppressed contributing public cell is left unavailable; no smaller sex-specific cohort is silently substituted. The original regional exposure quintile remains fixed. Country views can have fewer than five quintiles; an individual region has one quintile and therefore one line. Sweden-specific monthly series are supplementary. The regional sex counts come from the already collected Eurostat lfst_r_lfe2emp source.


## Current display specification,25 November2026

This supersedes earlier display-baseline descriptions above. Every displayed employment index uses the single observed November2022 count as100 and begins in January2022. Monthly source counts are rebased on load; old annual indices are not reused. Sex-specific and all-displayed-sample totals use their own November counts. Without that observed month, the chart is unavailable rather than assigned a fictitious month. Existing Eurostat annual-average data therefore do not yield a November-based regional index. Historical downloadable annual tables retain their documented original baseline and are not the currently plotted index.


## Restored Europe-first evidence hierarchy

Annual European regional and occupational curves are restored using their original source-consistent2022 annual baseline. All displayed periods still start in2022; full source history remains retained for DID. Monthly curves retain November2022=100. Quarterly SSB11658 national software employment uses Q42022=100, labelled quarterly and never interpolated into months. The quarterly panel is Norway only, not European regional coverage. The separate monthly UK panel contains all-occupation payroll employment. Sweden is supplementary. This supersedes the prior temporary exclusion of annual charts under a universal November denominator.

Quarterly source https://www.ssb.no/en/statbank/table/11658/
