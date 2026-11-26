# Independent public-data validation of high-exposure youth employment

Completed November 26, 2026. Free official public data and our frozen THAIE mapping were used. This package adds state pooling, independent ACS validation, linked-worker risk sets, and administrative hiring/mobility checks. The findings below distinguish observed employment patterns from causal attribution.

## Research question

Does weaker full-time employment among young people in high-exposure fields reflect fewer opportunities to enter employment, deterioration in jobs held by incumbent workers, or both? Which workers experience these changes?

## Principal findings

1. High-exposure youth employment displays relative weakness in independent survey comparisons. Relative weakness is not the same as an absolute employment loss, and annual comparisons do not establish when the divergence began.
2. The newly linked CPS does not show a descriptive increase in Q5 youth FT-to-PT transitions across the pooled periods. Directly observed movements must be distinguished from changes in repeated cross-sectional employment stocks.
3. Entry into full-time employment weakened in both Q5 and Q1–Q4. Administrative hiring results are sensitive to the preperiod and trend specification. Evidence does not establish that a Q5-specific AI shock caused the broad entry slowdown.

## State estimates and denominator reconciliation

The latest 36-calendar-month CPS period, November 2023–October 2026, contains 35 observed months. It supplies 15,447 Q5 full-time youth person-month records; every state and DC has at least 89 records. The national Q5 FT contribution to all same-age population is 10.609%, while the FT share among Q5 employed youth is 81.692%. These quantities have different denominators. Working household-cluster intervals are supplied, with sparse or degenerate intervals withheld. They are not full CPS survey-design intervals or causal occupational-shock intervals.

The state module independently checks 117 monthly source reconstructions against the prior audited aggregates, including both Q5 and Q1–Q4 FT/PT numerators. It verifies raw-file provenance, dictionary and parquet hashes, record uniqueness and outcome definitions. Independent numerical QA confirms the ratio/log-contrast gradients and multiplicity adjustment.

[State methods](state/STATE_POOLING_METHODS_EN.md), [pooled estimates](state/pooled_state_rates_working_uncertainty.csv), [saved map](state/Q5_youth_fulltime_three_year_map.svg), and [independent QA](state/STATE_INDEPENDENT_QA_EN.md).

## ACS annual and pooled validation

The ACS module acquires national person microdata, applies exact ages 22–25, excludes institutional residents and active Armed Forces, preserves frozen THAIE thresholds, and estimates uncertainty using the 80 official person replicate weights. The 2017 occupational bridge is fractional; it does not create individually observed historical occupations. The pooled comparison uses a three-year 2017–2019 baseline and a two-year 2023–2024 post period, normalizing weights separately by period length. Annual blocks are treated as independent for the reported variance approximation; exposure and crosswalk uncertainty are not propagated.

Five national archives contain 16,472,829 person records, including 702,146 eligible youth records. All 50 states and DC are present in every year. Pooling improves support but not uniformly precise estimates; the largest post-period state Q5 PT relative standard error is approximately 48.8%. A third clean ACS post year is not available in the verified microdata release.

The national relative changes below compare Q5 with Q1–Q4 and are percentages, not percentage-point employment-rate changes. Intervals are pointwise 95% replicate-based approximations for the descriptive annual comparison.

| outcome | estimate | CI95_low | CI95_high |
| --- | --- | --- | --- |
| employed | -7.919 | -9.511 | -6.327 |
| FT_proxy | -7.407 | -9.261 | -5.553 |
| PT_proxy | -11.260 | -14.581 | -7.940 |

The Q5 FT-hours-proxy count itself changed approximately −1.24%, with an interval spanning −3.01% to +0.53%. Its relative weakness therefore must not be presented as a statistically demonstrated absolute FT loss. The Q5 PT-hours-proxy count fell approximately 11.75%, rather than increasing. Neither annual result establishes that a change began after November 2022.

Hours are usual past-12-month hours, not current CPS FT/PT status. Annual salary relates to past-year income of currently employed wage/salary workers and cannot be interpreted as an hourly wage or a within-person wage gain. Newer aggregate ACS publication years are not assumed to establish available newer microdata.

[ACS report and pooled results](acs/ACS_VALIDATION_REPORT_EN.md).

## Incumbent-worker adaptation

The CPS module reconstructs 79 genuine adjacent-calendar-month links, validates rotation eligibility and demographic consistency, and estimates response probabilities using household-fold cross-fitting. Original, inverse-probability and trimmed weights are compared. IPW assumes response depends on observed covariates; calibration to all original margins and uncertainty from estimated propensities are not implemented. These rates carry no causal or statistical-significance claim.

The following are weighted monthly transition percentages among origin FT workers aged 22–25.

| band | transition | pre | post |
| --- | --- | --- | --- |
| Q1–Q4 | FT_to_PT | 5.736 | 5.814 |
| Q1–Q4 | FT_to_economic_PT | 1.436 | 1.248 |
| Q5 | FT_to_PT | 3.669 | 3.645 |
| Q5 | FT_to_economic_PT | 0.705 | 0.702 |

Economic PT requires destination usual PT; the separate economic-short-hours outcome can include people who remain usual FT. Neither outcome measures general permanent-to-contract conversion. These pre/post periods are unequal and the preperiod contains the pandemic; the table is not a controlled DID.

Official SIPP two-, three- and four-year cohorts yield 8,594, 5,024 and 2,847 baseline mapped workers, including 534, 304 and 164 aged 22–25. Baseline years differ, so these counts are not a single cohort's attrition sequence. The four-year youth Q5 cohort has only 23 people. Outcomes distinguish monthly hours intensity from usual schedule, align persistent job IDs in a strict same-job/full-month sensitivity, and retain nonemployment in personal outcome histories. Official 240-replicate Fay uncertainty is computed only for the four-year marginal transition rates, with sparse intervals withheld; it is not transferred to shorter panels. The latest SIPP reference year is 2024.

[Longitudinal report](longitudinal/LONGITUDINAL_METHODS_AND_RESULTS_EN.md).

## Opportunities to enter employment

All origin-jobless respondents form a common denominator. Destination THAIE classifies entry outcomes; nonworkers are not assigned a fictitious occupational treatment. Turning 26 between interviews does not exclude someone who was 25 at origin. These transitions do not identify first-ever jobs or graduation dates.

| outcome | pre | post |
| --- | --- | --- |
| Q1–Q4_FT | 7.334 | 6.201 |
| Q1–Q4_PT | 5.203 | 5.187 |
| Q5_FT | 1.726 | 1.314 |
| Q5_PT | 0.887 | 0.871 |
| any_employment | 15.436 | 13.830 |
| unmapped_employment | 0.285 | 0.258 |

The bands differ in size and composition. A smaller entry rate into Q5 is not by itself a disadvantage. Their pre/post changes are descriptive; demographic, schooling, industry, seasonality and pandemic composition still require controlled analyses. The simultaneous weakening of entry in both bands does not establish a uniquely AI-related mechanism.

[Entry methods](longitudinal/ENTRY_METHODS_EN.md) and [entry tables](longitudinal/cps_entry_rates_pooled.csv).

## Administrative hiring and mobility validation

The administrative module verifies 102 official QWI/J2J state/DC files. Outcomes use their actual public ages 22–24 and 35–64 and their quarterly industry grain. Industry THAIE is independently constructed from frozen 2019 occupational composition. This is a separate industry-exposure estimand, not occupational Q5. QWI and J2J share LEHD infrastructure and are not independent replications of each other.

Selected primary balanced-window youth results are shown below. Percentages describe multiplicative changes in flow-to-employment ratios, not individual hiring probabilities.

| product | outcome | estimate_pct | ci_low_pct | ci_high_pct | p_value | p_Holm24_primary |
| --- | --- | --- | --- | --- | --- | --- |
| qwi | log_HirN_rate | -4.706 | -13.636 | 5.147 | 0.304 | 1.000 |
| j2j | log_NEHire_rate | -4.798 | -12.778 | 3.912 | 0.242 | 1.000 |
| j2j | log_J2JHire_rate | -9.131 | -17.668 | 0.290 | 0.056 | 1.000 |

No primary youth result survives the 24-test correction. In the extended 2017 preperiod, the youth new-hire estimate is about −0.70% (p=.899) and nonemployment-entry estimate +0.83% (p=.858). The nominally stronger young-relative-to-older J2J contrast in the short specification fails linear-trend and longer-preperiod checks. Twelve industry clusters, including three treated groups, limit inference. Pretrend tests are reported with rank limitations and annual-average alternatives; nonrejection is not proof of parallel trends.

[Administrative main report](admin/ADMIN_VALIDATION_REPORT_EN.md) and [extended-preperiod report](admin/ADMIN_EXTENDED_PRE_REPORT_EN.md).

## What the package supports

The defensible finding is relative weakness of high-exposure youth employment accompanied by broadly weaker entry into full-time work. The linked descriptive results do not establish an increased Q5 FT-to-PT transition. No result establishes AI causality, a nationwide permanent-to-fixed-term shift, or a general welfare loss for every exposed worker. Conditional earnings of employed workers may rise while access to employment weakens; selection, hours and composition prevent treating that as a net benefit estimate.

The strongest next inferential step is to prespecify controlled entry and incumbent-transition models separately, address occupational/time common shocks and survey dependence, and report subgroup support before testing heterogeneity. Administrative industry flows remain triangulation. A contract-duration result requires a valid direct measure at both endpoints.

## Reproducibility and scope

Scripts and working caches are under work/us_public_validation_20261126. Public outputs here contain aggregates. Private respondent IDs remain in work caches. Each module supplies methods, source inventories and data-I/O checks. BUNDLE_FRESH_SMOKE_CHECKS.json records the final validation. Smoke checks emitted no images or graphs. The saved map is an export artifact; the homepage and manuscript were not changed during this validation build.
