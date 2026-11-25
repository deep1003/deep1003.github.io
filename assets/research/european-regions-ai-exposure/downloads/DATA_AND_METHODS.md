# European Regions dashboard methods and data

Updated 25 November 2026. This is an exploratory working study, not a monthly European software-payroll database.

## Binding source rule

No Stanford employment data, ADP data, Stanford exposure scores or their quintile assignments are analytical inputs. Stanford is a visual reference only. A downloaded reference archive was excluded and removed from this working analysis. All displayed European indices are rebuilt from our collected official data and our own THAIE calculation. The own transferred score table is included and hashed.

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

The reproduction ZIP includes seven official raw source snapshots, our transferredISCO3score table, official crosswalk-derived mapping, the public regional aggregate input, scripts and source hashes. No personal records or Stanford/ADP data are included. Install numpy,pandas,openpyxl,matplotlib, then run `python scripts/build.py` from the extracted folder to rebuild source-grain indices offline into `site/data/` and `derived/`. Source endpoints are recorded in metadata. Collection scripts may use the original project layout; offline rebuilding uses bundled snapshots and inputs.

The HTML uses native SVG with no third-party chart library. Current chart values and SVG can be exported directly. Validation checks sources, raw-source reconciliation, baseline arithmetic, keys, cohort support, score lineage and index dimensions without displaying charts.
