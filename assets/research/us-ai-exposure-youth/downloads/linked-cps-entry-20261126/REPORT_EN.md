# Does entry into high-exposure full-time work decline more for young adults?

## Finding

The linked CPS does not establish a significantly larger decline in Q5 full-time entry than in Q1–Q4. The proportional industry-controlled DID is +6.94%, with a 95% interval from −14.53% to +33.80% (p=.546). A materially negative effect remains compatible with this interval. The additive DID is +0.962 percentage points, opposite to the proposed greater-Q5-decline hypothesis; its nominal significance does not survive all specification checks and must not be interpreted as an AI benefit.

## Data and risk set

We rebuilt 115 genuine adjacent-calendar-month CPS pairs spanning February 2017–October 2026. The full linked risk file contains 95,862 origin-jobless transition opportunities at ages 22–25, not independent people. Rotation eligibility, unique identifiers, next-month MIS, sex/race consistency, state continuity and age progression are verified. People aged 25 at origin who turn 26 remain eligible. October 2025 is unobserved; neither September-to-November nor October-to-November transitions are invented.

The primary window has destination months January 2019–October 2022 and January 2023–October 2026. Each side spans 46 calendar months. There are 46 observed pre-months and 44 observed post-months because the missing October 2025 survey removes two adjacent pairs. November and December 2022 are excluded to avoid mixing the launch transition with fully post-launch intervals. A sensitivity includes December 2022 as the first post month. Extended-preperiod analysis starts in February 2017; the no-bridge sensitivity starts in 2020.

Origin nonemployment includes unemployment and nonparticipation. All these respondents form a common denominator. Destination THAIE classifies entry outcomes; it is not a treatment assigned to a nonworker. Unmapped destinations remain outside the two target entry outcomes, not recoded as low exposure. Approximately 98% of weighted FT entries are mapped. The 2017–2019 occupation bridge contributes fractional expected group membership rather than fabricated detailed occupations. Score and bridge uncertainty are not included in the intervals.

FT entry requires destination PEMLR 1/2 and PRFTLF 1, the usual full-time labor-force classification. It includes wage/salary and self-employed work, rather than employer payroll hiring alone, and does not identify permanent contracts. CPS linkage is address/rotation based and cannot automatically recover movers; selection related to unobserved mobility can remain after IPW.

Same-window unadjusted rates are retained separately.

| period   |   risk_pairs |   months |   Q5_entry_rate_pct |   Q14_entry_rate_pct |
|:---------|-------------:|---------:|--------------------:|---------------------:|
| post     |        31167 |       44 |              1.3164 |               6.2103 |
| pre      |        39062 |       46 |              1.7004 |               7.2415 |

## Two distinct DID estimands

**Proportional entry contrast.** We aggregate weighted new FT entries by state, destination broad industry, exposure group and observed month. A PPML mean includes state×exposure-group, industry×exposure-group, state×calendar-month, industry×calendar-month, and exposure-group×month-of-year fixed effects. The coefficient is on Q5×post. Eight Q5×pandemic-quarter interactions cover 2020–2021. Because the jobless denominator is shared within state-month, its log is absorbed by the state-month effects. State and industry month effects control local conditions, common entry volumes, and industry-wide demand/recovery; the group-season terms permit differential seasonality.

The reported percentage is 100×(exp(beta)−1), a change in the Q5/Q1–Q4 entry-rate ratio. Conditioning on industry-month means this is a within-industry composition contrast; it is not the total effect of industry-wide hiring changes. Full zero-entry cells are retained wherever a risk set is observed. All-zero FE margins are removed for finite PPML estimation without losing any positive mapped entry weight. Missing risk cells are not filled with zero.

**Absolute entry-gap contrast.** For every jobless risk opportunity we form 100×(entry into Q5 FT − entry into Q1–Q4 FT) and regress this paired outcome on post, state, differential month-of-year seasonality, prior-industry history, origin labor-force status and pandemic-quarter indicators. Survey/response weights enter WLS. This is an additive paired-outcome DID in percentage points. Prior industry is a work-history covariate and its unavailable category is explicit; nonworkers are not assumed currently employed in that industry. A demographic sensitivity adds exact age, sex, education, race, Hispanic origin and enrollment. Its controls and estimand differ from the destination-industry-conditioned proportional model.

The broader Q1–Q4 group has a larger baseline entry rate. A larger absolute Q1–Q4 decline and a larger proportional Q5 decline can coexist. Therefore the two measures are reported separately rather than chosen after seeing their significance.

## Primary estimates

| metric       |   estimate |   CI_low |   CI_high |   p_value |   p_Holm_two_coprimary |
|:-------------|-----------:|---------:|----------:|----------:|-----------------------:|
| relative_pct |     6.9399 | -14.5284 |   33.8005 |    0.5459 |                 0.5459 |
| absolute_pp  |     0.9620 |   0.2587 |    1.6652 |    0.0089 |                 0.0179 |

Working covariance clusters scores by state and calendar quarter with their intersection removed, using finite-sample corrections and t critical values. The two co-primary DID tests receive Holm correction. State-only and state-plus-year alternatives are retained in DID_RESULTS.csv. These are not full CPS design-based variances, and they do not propagate estimated response probabilities, unknown attrition mechanisms, exposure measurement, or occupation-bridge uncertainty. Global occupation shocks persisting beyond these cluster structures remain a limitation.

The additive +0.962 pp estimate says that the Q5-minus-Q1–Q4 gap increases, not that Q5 entry itself necessarily increases. Adding a differential trend gives +0.794 pp (p=.209); adding 2022 recovery interactions gives +0.457 pp (p=.281). State-plus-year clustering also widens its interval to approximately −0.052 to +1.976 pp (p=.060). It is not a robust causal improvement. The proportional primary estimate is statistically inconclusive under every weight variant.

## Attrition adjustment

For comparability across occupation-code regimes, a common set of origin covariates is used in year-specific household-fold response models among rotation-eligible jobless adults. Covariates are state, age group, sex, race, Hispanic origin, education, labor-force status, MIS, interview month, prior industry and enrollment. No destination information enters the response model. Original respondent weights, cross-fitted response IPW, 99th-percentile inverse-factor trimming, and calibration to eligible youth jobless state-month margins are compared on identical matched risk sets.

| metric       | method     |   estimate |   CI_low |   CI_high |   p_value |
|:-------------|:-----------|-----------:|---------:|----------:|----------:|
| relative_pct | origin     |     6.5105 | -14.9331 |   33.3595 |    0.5713 |
| relative_pct | ipw        |     6.9399 | -14.5284 |   33.8005 |    0.5459 |
| relative_pct | trim99     |     6.8772 | -14.5664 |   33.7032 |    0.5491 |
| relative_pct | calibrated |     6.4608 | -14.0928 |   31.9321 |    0.5560 |
| absolute_pp  | origin     |     0.9427 |   0.2453 |    1.6401 |    0.0097 |
| absolute_pp  | ipw        |     0.9620 |   0.2587 |    1.6652 |    0.0089 |
| absolute_pp  | trim99     |     0.9634 |   0.2647 |    1.6620 |    0.0085 |
| absolute_pp  | calibrated |     0.9283 |   0.2633 |    1.5933 |    0.0078 |

Correction changes the proportional primary estimate from +6.51% to +6.94%, and the additive estimate from +0.943 to +0.962 pp. These differences are small relative to their uncertainty. Four state-month cells in the full 2017–2026 inventory have eligible young nonworkers but no successful match. Their missing outcomes cannot be recovered by calibration; targets are restored only in cells with observed respondents. The largest calibration multiplier is about 9.96 in a sparse 2018 cell, so calibrated estimates are sensitivity checks rather than an automatic solution to attrition. IPW assumes response on observables and is not an official longitudinal weight.

The four unrecoverable cells contain nine eligible person-month records and approximately 0.0037% of eligible population weight across the full inventory. Their state-month support is explicitly retained in UNRECOVERABLE_RESPONSE_CELLS.csv rather than silently imputed.

## Event study and pretrends

Monthly observations are grouped into calendar-quarter coefficients. Group-specific month-of-year effects and a complete set of quarter indicators are collinear unless four seasonal references are supplied. We therefore omit the four 2022 quarters and interpret each event coefficient relative to its season-matched 2022 reference. Q4 2022 contains October only; Q4 2026 also contains October only. The 2020–2021 quarter terms are pandemic nuisance effects, not plotted AI-event coefficients.

The state-plus-quarter covariance is indefinite for all full pretrend blocks and several marginal event terms. Invalid intervals and joint tests are withheld, not made positive by clipping eigenvalues. The saved event graphs use explicitly labeled state-cluster diagnostic intervals, whose coefficients exactly reproduce the primary event model. This alternative conditions on the observed common time path and does not solve global-shock or survey-design uncertainty.

| metric       | spec         |   terms |   p_value |   p_Holm_four_diagnostics |
|:-------------|:-------------|--------:|----------:|--------------------------:|
| relative_pct | main         |       4 |    0.3858 |                    0.7715 |
| relative_pct | extended_pre |      12 |    0.4578 |                    0.7715 |
| absolute_pp  | main         |       4 |    0.1154 |                    0.3462 |
| absolute_pp  | extended_pre |      12 |    0.0110 |                    0.0438 |

The extended-preperiod additive pretrend test rejects flat leads (p=.011; Holm across four diagnostics approximately .044). This undermines a causal interpretation of its positive DID contrast. The proportional diagnostic does not reject, but that is not proof of parallel trends or enough power to rule out relevant divergence. Event coefficients have pointwise intervals; a separate column applies Holm correction over the displayed coefficient family. Individual positive or negative quarters are not selected as confirmatory results.

## Specification checks

| metric       | spec              |   estimate |   CI_low |   CI_high |   p_value |
|:-------------|:------------------|-----------:|---------:|----------:|----------:|
| relative_pct | main              |     6.9399 | -14.5284 |   33.8005 |    0.5459 |
| relative_pct | no_industry       |     1.0383 | -24.8175 |   35.7860 |    0.9436 |
| relative_pct | no_covid_controls |    -9.8130 | -25.9524 |    9.8443 |    0.2936 |
| relative_pct | trend             |    24.0419 |   0.6675 |   52.8438 |    0.0435 |
| relative_pct | exclude_covid     |     7.0828 | -14.5735 |   34.2293 |    0.5371 |
| relative_pct | recovery_2022     |    -2.2620 | -26.1192 |   29.2990 |    0.8686 |
| relative_pct | extended_pre      |     1.9078 | -15.6744 |   23.1558 |    0.8411 |
| relative_pct | no_bridge         |    16.6123 | -10.9137 |   52.6433 |    0.2518 |
| relative_pct | matched_missing   |     6.9063 | -14.6061 |   33.8382 |    0.5488 |
| relative_pct | first_post_Dec22  |     7.1062 | -14.1550 |   33.6331 |    0.5315 |
| absolute_pp  | main              |     0.9620 |   0.2587 |    1.6652 |    0.0089 |
| absolute_pp  | no_industry       |     0.9665 |   0.2310 |    1.7019 |    0.0117 |
| absolute_pp  | no_covid_controls |     0.2172 |  -0.3690 |    0.8034 |    0.4555 |
| absolute_pp  | trend             |     0.7942 |  -0.4670 |    2.0554 |    0.2086 |
| absolute_pp  | exclude_covid     |     0.9743 |   0.2573 |    1.6913 |    0.0099 |
| absolute_pp  | recovery_2022     |     0.4566 |  -0.3915 |    1.3048 |    0.2806 |
| absolute_pp  | extended_pre      |     0.7042 |   0.1422 |    1.2662 |    0.0154 |
| absolute_pp  | no_bridge         |     1.4850 |   0.3936 |    2.5765 |    0.0095 |
| absolute_pp  | matched_missing   |     0.9572 |   0.2532 |    1.6612 |    0.0093 |
| absolute_pp  | first_post_Dec22  |     0.9489 |   0.2472 |    1.6506 |    0.0097 |
| absolute_pp  | demographics      |     1.0780 |   0.3954 |    1.7606 |    0.0030 |

Removing pandemic interactions yields a proportional estimate of −9.81% (p=.294), while the primary adjustment gives +6.94% (p=.546). Extending the preperiod to 2017 gives +1.91% (p=.841). Adding 2022 recovery interactions gives −2.26% (p=.869). Thus the apparent direction is substantially more sensitive to pandemic/reference-period assumptions than to response-weight correction. A nominally positive proportional trend specification is not evidence of an AI benefit and changes under alternative covariance.

## Numerical verification and interpretation

The absorbed PPML was checked against an independent explicit-dummy statsmodels fit on 782 real cells. The maximum coefficient difference is approximately 2.6e−12 and the two-way covariance difference approximately 5.2e−10 after aligning finite-sample conventions. The paired-outcome WLS agrees with explicit weighted dummy regression within 9.4e−14. All 117 source-cache hashes, adjacent-month dates, age/risk eligibility, outcome-weight accounting and missing-month rules passed. Smoke checks emitted no graphs.

This analysis supports neither a statistically established extra Q5 entry decline nor AI causal attribution. Its intervals still allow economically important harm. Entry includes return to employment and is not verified first-job hiring; recorded age is not experience. Origin selection into nonemployment, differential recovery, schooling, public-file age perturbation, imperfect occupation mapping, and unobserved actual AI adoption remain alternatives. Repeated monthly employment-stock weakness cannot be equated with this entry-flow estimand.

## Files

- PRIMARY_RESULTS.csv and DID_RESULTS.csv contain main and sensitivity estimates.
- EVENT_STUDY.csv preserves two-way intervals, including withheld cases; EVENT_STUDY_STATE_INTERVALS_WITH_MULTIPLICITY.csv contains the plotted diagnostic intervals.
- PRETREND_TESTS_WITH_MULTIPLICITY.csv records valid diagnostics and invalid-covariance flags.
- SAME_WINDOW_UNADJUSTED_RATES.csv separates raw flow descriptions from controlled estimates.
- response_audit.csv and linkage_audit.csv document response and matching support.
- INDEPENDENT_NUMERICAL_CHECKS.json and PREPARATION_CHECKS.json contain validation evidence.
- ENTRY_EVENT_STUDY and ENTRY_SPECIFICATION_SENSITIVITY are saved as PNG and SVG. No individual data are published.

Reproduction scripts are under work/us_entry_did_20261126. Official source URLs and original hashes are in the pre-existing CPS source manifest referenced by PREPARATION_CHECKS.json. No paid data or new outside employment/exposure series enter this analysis.
