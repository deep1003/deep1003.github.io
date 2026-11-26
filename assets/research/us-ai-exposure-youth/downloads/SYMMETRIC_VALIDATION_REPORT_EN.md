# Symmetric-window validation of the occupational THAIE employment study

## Design and verification

The primary analysis uses 47 pre-event calendar months from December 2018 through October 2022 and 47 post-event calendar months from December 2022 through October 2026. November 2022 is excluded as the transition month. October 2025 was not observed, giving 47 pre-event and 46 post-event observations. The robustness window uses November 2019–October 2022 and December 2022–November 2025, with 36 pre-event and 35 observed post-event months. No display interpolation enters estimation.

The outcomes are weighted full-time and part-time employment counts. Frozen 2019 occupational THAIE Q5 is compared with Q1–Q4. Full-time and part-time models use identical rows within each age/window. Occupation–industry, occupation–month-of-year, and industry–calendar-month fixed effects absorb stable allocation, occupation-specific seasonality, and industry-wide monthly shocks. Q5-by-pandemic-quarter interactions are retained. Zero survey-count cells are supported model cells, not administrative proof of zero jobs. Requiring shared FT/PT support retains 91.75% of weighted youth FT employment and 99.48% of PT employment in the long window. An FT-only-support sensitivity restores all weighted FT employment and gives −6.02% (p=.090) in the long window and −1.88% (p=.584) in the short window. Thus, common support restrictions do not account for the loss of conventional FT significance.

The model is Poisson QMLE with occupation-clustered working uncertainty; it does not implement the full CPS survey-design variance. The 2019 baseline freezes employment composition and quintile cutpoints, not score vintage. Task scores and capability weights are retrospective, not observed pre-event adoption. Pre-2020 workers are fractionally allocated through a national occupation-code bridge. Exposure linkage and bridge uncertainty are not propagated into the intervals. Full-time and part-time status refer to usual hours across jobs, whereas exposure is assigned from the primary occupation; this does not identify permanent or contract status.

All 94 available raw CPS files covering the longest window, including the transition month, matched their recorded hashes. Fresh same-parser regeneration of five selected months across all six ages exactly reproduced stored weighted occupational counts. A separate PRWKSTAT recode agreed with PRFTLF in those records. Reconstructing 2019 composition weights and all four cutpoints reproduced the stored THAIE quintiles. These checks establish internal reproducibility, not independent retrieval or validation of every original record. An explicit-dummy Poisson GLM reproduced coefficients on 2,139 real CPS cells from six occupations. Its exact fixed-effect rank was 446 versus the absorbed routine's conservative degrees convention of 449. Standard errors agree after explicitly harmonizing that finite-sample convention; the harmonization factor is 1.000892. This does not independently validate the degrees convention or the full survey variance.

## Primary results

| age | outcome | estimate_pct | ci_low_pct | ci_high_pct | p_value | p_Holm_primary12 |
| --- | --- | --- | --- | --- | --- | --- |
| 50+ | PT | -2.4926 | -9.8054 | 5.4131 | 0.5250 | 1.0000 |
| 35–40 | FT | 0.6651 | -6.8134 | 8.7438 | 0.8661 | 1.0000 |
| 41–49 | PT | -2.9447 | -14.2763 | 9.8849 | 0.6364 | 1.0000 |
| 31–34 | PT | -15.9808 | -27.1107 | -3.1513 | 0.0164 | 0.1972 |
| 26–30 | PT | -2.9349 | -14.5240 | 10.2254 | 0.6455 | 1.0000 |
| 22–25 | PT | -1.7798 | -14.0015 | 12.1788 | 0.7907 | 1.0000 |
| 50+ | FT | -1.2581 | -7.6695 | 5.5986 | 0.7112 | 1.0000 |
| 35–40 | PT | -0.7065 | -10.2563 | 9.8594 | 0.8905 | 1.0000 |
| 31–34 | FT | -1.6587 | -9.2644 | 6.5846 | 0.6832 | 1.0000 |
| 26–30 | FT | -3.3651 | -10.4452 | 4.2748 | 0.3771 | 1.0000 |
| 41–49 | FT | -2.4422 | -9.5402 | 5.2127 | 0.5205 | 1.0000 |
| 22–25 | FT | -6.5987 | -13.2203 | 0.5281 | 0.0687 | 0.7562 |

The youth full-time estimate is -6.60% with a marginal 95% interval [-13.22, 0.53], raw p=0.069, and Holm p=0.756. The part-time estimate is -1.78%, p=0.791. None of the 12 primary tests survives Holm correction. The ages 31–34 part-time estimate is nominally negative but does not survive correction. No age group exhibits a significant relative part-time increase.

The direct 12-coefficient all-zero Wald test gives p=0.324; an occupation-score Rademacher multiplier diagnostic with 4,999 draws gives p=0.318. Direct tests do not establish equal-versus-different age effects, and a difference in separate significance labels cannot establish an age boundary. See the direct age and FT/PT contrast tables.

## Window, support and trend sensitivities

| label | estimate_pct | ci_low_pct | ci_high_pct | p_value |
| --- | --- | --- | --- | --- |
| 36-month main | -1.8223 | -8.6856 | 5.5568 | 0.6182 |
| 47-month trend | -1.2548 | -11.5318 | 10.2161 | 0.8215 |
| 47-month main | -6.5987 | -13.2203 | 0.5281 | 0.0687 |
| 47-month no_covid | -6.7301 | -13.3783 | 0.4285 | 0.0647 |
| 47-month frozen 36-window units | -6.4632 | -13.1408 | 0.7278 | 0.0769 |

The 47-month negative contrast weakens materially in the 36-month window and with a Q5-specific linear trend. Freezing the units retained in the shorter window has a much smaller effect than changing the calendar span. Omitting 2020–2021 leaves the 47-month coefficient close to its baseline, but does not resolve pre-existing divergence or identify an AI shock. The shorter window has only 12 non-pandemic pre-event months, so its three-year post-period cannot be causally justified by invoking the 36-month calendar count alone. The 47-month window has 23 non-pandemic pre-event months. The 2018–2019 observations also rely on the historical occupation crosswalk. The pooled Q5 linear trend is estimated using both pre- and post-event observations and may absorb a genuine gradual effect; it is a sensitivity specification, not a definitive causal correction.

## Event studies and uncertainty

| age | outcome | pretrend_p | p_Holm12 |
| --- | --- | --- | --- |
| 35–40 | PT | 0.1142 | 1.0000 |
| 50+ | PT | 0.1450 | 1.0000 |
| 41–49 | FT | 0.3190 | 1.0000 |
| 26–30 | FT | 0.8770 | 1.0000 |
| 31–34 | FT | 0.0390 | 0.4293 |
| 22–25 | FT | 0.0294 | 0.3527 |
| 50+ | FT | 0.4270 | 1.0000 |
| 35–40 | FT | 0.0702 | 0.7024 |
| 26–30 | PT | 0.6222 | 1.0000 |
| 31–34 | PT | 0.2073 | 1.0000 |
| 41–49 | PT | 0.5601 | 1.0000 |
| 22–25 | PT | 0.3351 | 1.0000 |

The event studies use monthly counts and three-month relative-time bins, with August–October 2022 as the omitted reference. Pandemic quarters have separate nuisance coefficients and are excluded from the flat-lead joint test. Boundary bins can have fewer months; November 2022 and October 2025 remain absent. For youth full-time employment the raw joint lead p-value is 0.029; its twelve-test Holm p-value is 0.353. Non-rejection after correction does not validate parallel trends. Event intervals are pointwise, not simultaneous.

## Interpretation

A negative early-career full-time contrast remains a descriptive research signal. Its conventional significance does not survive the requested balanced-window validation, and its magnitude is sensitive to the pre-period and trend. The evidence does not establish a causal AI-induced decline, a full-time-to-part-time transition, a sex-specific disadvantage, or a protective age boundary. Non-significance does not establish zero effects; the primary interval still admits an economically substantial decline. Occupational exposure is not employer adoption, and working cluster covariance does not fully capture the CPS sampling design.

An additional matched-observation sensitivity removes December 2019, the pre-event month mirroring missing October 2025. This gives 46 observed months on each side in the long window and a youth full-time estimate of −6.62% (p=.071). Thus, the missing month alone does not explain the loss of conventional significance. In the shorter window, 35 observed months on each side give −1.30% (p=.739).

The earlier 2017-start estimate of −9.03% (raw p=.025) and annual legacy estimate of −8.76% should remain labeled as prior specifications, rather than pooled with the current validation. Index graphs normalized to November 2022 describe endpoint paths and are not DID estimates. Existing manuscripts were not edited.
