# Independent public-administrative validation of entry and mobility mechanisms

Verified November26,2026. Free official QWI and J2J extracts were analyzed; no paid access or individual records were required. No figures were emitted.

## Data and exposure

The source manifest records102 official state/DC files and verified SHA256 hashes. Both products contain mutually exclusive NAICS sectors; all-industry rows, sex subtotals and age totals were excluded. Nineteen NAICS sectors were mapped to12 mutually exclusive CPS broad industry groups. Private-sector QWI ownershipA05 was used; public administration92 was excluded. J2J ownershipA00 represents its all-covered-ownership universe and differs from QWI private ownership. Agricultural and other UI coverage limits remain. Public LEHD estimates are modeled/noise-protected administrative aggregates, not error-free job counts.

Own frozen2019 industry THAIE was reaggregated and matched its original numerator/coverage inputs. High exposure comprises information, financial activities, and professional/business services. This INDUSTRY treatment is not occupational THAIEQ5 and must not be described as an exact replication of the CPS occupational result. The2019component is employment composition applied to retrospective task-based THAIE scores, not proof that those scores were observed in2019. Broad-industry bins do not guarantee exactly20% of jobs per bin. Frozen national occupational composition provides exposure, not observed adoption.

Public age categories permit22–24 and35–64, not the requested exact22–25 and40+ groups. Allstates/DC were inventoried, including missing coverage; outcome-specific balanced panels retain48–49 states/DC. Census age bins do not identify recent graduates or first jobs.

## Design

QWI compares12prequarters2019Q4–2022Q3 with12postquarters2023Q1–2025Q4. J2J has11postquarters through2025Q3. Transition2022Q4 is excluded. Data collected more recently are not silently treated as available for all indicators. Regressions require complete state–industry–age support for the outcome. Suppressed/unavailable cells remain missing, never zero. Strict released flags1,6,10 are primary; adding distorted released flags7,9,12 is sensitivity. Broad-industry totals require every NAICS×age component. Earnings averages use their appropriate employment weights.

Outcomes are log quarterly hires or separations divided by beginning-quarter employment, and log average earnings. The ratios are flows per beginning job, not individual hiring probabilities. QWI HirN excludes recalls but does not establish first-career entry. J2J nonemployment-to-employment is not the CPS unemployment category. QWI earnings are monthly averages and J2J earnings are quarterly averages. Earnings refer to stable/full-quarter jobs and are not hourly wages, FT status, contract permanence or total welfare. Common inflation is absorbed by state×date effects; reported raw earnings levels are nominal.

OLS uses state×industry, state×calendar-quarter and industry×quarter-of-year fixed effects, plus high-industry interactions with2020–2021 pandemic quarters. State–industry cells have equal regression weight; the coefficient is not a population-weighted national average. The young/older log-ratio model is a descriptive triple-difference analogue. Standard errors cluster by12broadindustries, with only3treatedindustries, using t11 working inference. Two-way state/industry SEs accompany outputs. They are not official administrative measurement-error uncertainty. All24primary contrasts receive Holm correction; per-product12test corrections are also retained.

Event studies retain the industry-specific seasonal FE and therefore omit four seasonal reference quarters2021Q4–2022Q3. A single reference quarter with saturated quarter effects is collinear with that seasonal structure. Four-reference normalization was checked for full rank/conditioning and positive variances. It leaves only one non-pandemic pre-event coefficient in this short window. Non-rejection is weak evidence and cannot validate parallel trends. Trend and no-pandemic sensitivities are exploratory.

## Primary results

| product | age | outcome | estimate_pct | ci_low_pct | ci_high_pct | p_value | p_Holm24_primary | states | industries |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| qwi | 22–24 | log_HirN_rate | -4.7061 | -13.6357 | 5.1469 | 0.3040 | 1.0000 | 49.0000 | 12.0000 |
| qwi | 22–24 | log_HirA_rate | -3.8301 | -12.3364 | 5.5014 | 0.3732 | 1.0000 | 49.0000 | 12.0000 |
| qwi | 22–24 | log_Sep_rate | -1.9814 | -7.3536 | 3.7023 | 0.4510 | 1.0000 | 48.0000 | 12.0000 |
| qwi | 22–24 | log_earnings | -0.5510 | -2.0314 | 0.9518 | 0.4346 | 1.0000 | 48.0000 | 12.0000 |
| qwi | 35–64 | log_HirN_rate | -9.0674 | -17.7474 | 0.5287 | 0.0611 | 1.0000 | 49.0000 | 12.0000 |
| qwi | 35–64 | log_HirA_rate | -7.0153 | -13.5630 | 0.0285 | 0.0508 | 1.0000 | 49.0000 | 12.0000 |
| qwi | 35–64 | log_Sep_rate | -2.9233 | -6.5494 | 0.8434 | 0.1143 | 1.0000 | 48.0000 | 12.0000 |
| qwi | 35–64 | log_earnings | 1.8780 | -3.0513 | 7.0580 | 0.4265 | 1.0000 | 48.0000 | 12.0000 |
| qwi | 22–24 relative to35–64 | log_HirN_rate | 4.7857 | 1.1738 | 8.5266 | 0.0136 | 0.2859 | 49.0000 | 12.0000 |
| qwi | 22–24 relative to35–64 | log_HirA_rate | 3.3704 | -0.1782 | 7.0451 | 0.0608 | 1.0000 | 49.0000 | 12.0000 |
| qwi | 22–24 relative to35–64 | log_Sep_rate | 0.9687 | -2.7709 | 4.8521 | 0.5853 | 1.0000 | 48.0000 | 12.0000 |
| qwi | 22–24 relative to35–64 | log_earnings | -2.4079 | -8.0463 | 3.5763 | 0.3867 | 1.0000 | 48.0000 | 12.0000 |
| j2j | 22–24 | log_NEHire_rate | -4.7978 | -12.7780 | 3.9125 | 0.2422 | 1.0000 | 49.0000 | 12.0000 |
| j2j | 22–24 | log_ENSep_rate | -0.8264 | -3.4213 | 1.8381 | 0.5051 | 1.0000 | 49.0000 | 12.0000 |
| j2j | 22–24 | log_J2JHire_rate | -9.1315 | -17.6682 | 0.2905 | 0.0560 | 1.0000 | 49.0000 | 12.0000 |
| j2j | 22–24 | log_earnings | 0.0189 | -1.2730 | 1.3277 | 0.9751 | 1.0000 | 49.0000 | 12.0000 |
| j2j | 35–64 | log_NEHire_rate | -6.7859 | -10.6676 | -2.7356 | 0.0039 | 0.0900 | 49.0000 | 12.0000 |
| j2j | 35–64 | log_ENSep_rate | 1.1372 | -7.1670 | 10.1842 | 0.7768 | 1.0000 | 49.0000 | 12.0000 |
| j2j | 35–64 | log_J2JHire_rate | -13.6416 | -21.0950 | -5.4842 | 0.0043 | 0.0956 | 49.0000 | 12.0000 |
| j2j | 35–64 | log_earnings | 1.4004 | -3.5209 | 6.5728 | 0.5509 | 1.0000 | 49.0000 | 12.0000 |
| j2j | 22–24 relative to35–64 | log_NEHire_rate | 1.9817 | -3.2008 | 7.4416 | 0.4252 | 1.0000 | 49.0000 | 12.0000 |
| j2j | 22–24 relative to35–64 | log_ENSep_rate | -1.4315 | -8.4325 | 6.1048 | 0.6750 | 1.0000 | 49.0000 | 12.0000 |
| j2j | 22–24 relative to35–64 | log_J2JHire_rate | 5.1328 | 2.6517 | 7.6739 | 0.0007 | 0.0180 | 49.0000 | 12.0000 |
| j2j | 22–24 relative to35–64 | log_earnings | -1.3811 | -6.9183 | 4.4855 | 0.6068 | 1.0000 | 49.0000 | 12.0000 |

## Interpretation

No youth22–24 primary hiring, separation or earnings result survives the24test correction. The point estimates are consistent with weaker hiring in high-exposure industries, but their intervals do not establish a youth-specific AI effect. In the primary J2J model, older workers' nonemployment-entry and job-to-job hiring rates decline more than youth rates. The young-relative-to-older job-to-job hiring contrast is positive, not negative. That J2J relative contrast is +5.13% (raw p=.000749, Holm24 p=.0180), but becomes +0.64% (p=.703) after adding a high-industry linear trend; omitting2020–2021 gives +5.06% (p=.00112). Thus even the corrected primary contrast is not robust to the trend specification. This remains a descriptive industry-level mechanism result, with very few independent exposure clusters and incomplete pretrend information. It cannot be substituted for the original occupational CPS full-time outcome or interpreted as proof that older workers are harmed by AI.

A hiring-rate reduction may reflect ordinary churn, demand, industry-specific cycles or the denominator as well as entry opportunity. A separation ratio does not distinguish quits from layoffs here. Neither product observes full-time-to-part-time or permanent-to-contract transitions, AI adoption, training or benefits. Both products arise from overlapping LEHD infrastructure, so they are not independent replications of one another even though they are independent of CPS survey outcomes.

## Pretrend diagnostics

| product | age | outcome | pretrend_p | pretrend_terms |
| --- | --- | --- | --- | --- |
| j2j | 22–24 | log_ENSep_rate | 0.2943 | 1.0000 |
| j2j | 22–24 | log_J2JHire_rate | 0.4737 | 1.0000 |
| j2j | 22–24 | log_NEHire_rate | 0.3629 | 1.0000 |
| j2j | 22–24 | log_earnings | 0.4299 | 1.0000 |
| j2j | 22–24 relative to35–64 | log_ENSep_rate | 0.5480 | 1.0000 |
| j2j | 22–24 relative to35–64 | log_J2JHire_rate | 0.1896 | 1.0000 |
| j2j | 22–24 relative to35–64 | log_NEHire_rate | 0.1424 | 1.0000 |
| j2j | 22–24 relative to35–64 | log_earnings | 0.0544 | 1.0000 |
| j2j | 35–64 | log_ENSep_rate | 0.3631 | 1.0000 |
| j2j | 35–64 | log_J2JHire_rate | 0.1512 | 1.0000 |
| j2j | 35–64 | log_NEHire_rate | 0.9772 | 1.0000 |
| j2j | 35–64 | log_earnings | 0.0229 | 1.0000 |
| qwi | 22–24 | log_HirA_rate | 0.7017 | 1.0000 |
| qwi | 22–24 | log_HirN_rate | 0.5582 | 1.0000 |
| qwi | 22–24 | log_Sep_rate | 0.8533 | 1.0000 |
| qwi | 22–24 | log_earnings | 0.4251 | 1.0000 |
| qwi | 22–24 relative to35–64 | log_HirA_rate | 0.4434 | 1.0000 |
| qwi | 22–24 relative to35–64 | log_HirN_rate | 0.6078 | 1.0000 |
| qwi | 22–24 relative to35–64 | log_Sep_rate | 0.8285 | 1.0000 |
| qwi | 22–24 relative to35–64 | log_earnings | 0.0707 | 1.0000 |
| qwi | 35–64 | log_HirA_rate | 0.9294 | 1.0000 |
| qwi | 35–64 | log_HirN_rate | 0.7008 | 1.0000 |
| qwi | 35–64 | log_Sep_rate | 0.8844 | 1.0000 |
| qwi | 35–64 | log_earnings | 0.0322 | 1.0000 |

## Sources and reproduction

- [Official LEHD public data and nonsampling-error statement](https://lehd.ces.census.gov/data/)
- [QWI definitions and aggregation guidance](https://lehd.ces.census.gov/doc/QWI_101.pdf)
- [J2J technical documentation](https://lehd.ces.census.gov/doc/jobtojob_documentation_long.pdf)
- Exact downloaded URLs, hashes and local source paths appear in source_manifest.csv.
- Run run_admin_validation.py and then report_admin.py using the project environment. Original official files are preserved under work/us_robustness_data_20261124/raw. No account or purchase is needed. The per-state release text files remain available alongside those sources.

No manuscript or homepage was changed by this module.
