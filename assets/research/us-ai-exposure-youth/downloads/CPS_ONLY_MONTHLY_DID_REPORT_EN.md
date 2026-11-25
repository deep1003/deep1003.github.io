# Occupational THAIE and Age-Specific Full-Time and Part-Time Employment After Generative AI

## Independent monthly CPS analysis

### Abstract

We compare employment in the highest occupational THAIE quintile with the lower four quintiles across six age groups using independently aggregated Basic Monthly CPS microdata. The analysis covers January 2017–October 2026, with October 2025 unavailable. Occupation–industry, occupation–month-of-year, and industry–calendar-date fixed effects control stable allocation, occupation-specific seasonality, and industry-wide monthly shocks. Exposure-specific pandemic-quarter terms address differential 2020–2021 changes. Among 12 primary contrasts, full-time employment among ages 22–25 and part-time employment among ages 31–34 are nominally negative. None survives Holm correction. The young full-time result is sensitive to a linear exposure trend and exhibits nominal pre-period divergence. No age group shows a significant relative part-time increase. These estimates do not establish AI-caused displacement, a full-time-to-part-time transition, or a particular age boundary.

## Introduction

The research question is whether weaker full-time employment among young workers in highly AI-exposed fields reflects fewer hiring opportunities, poorer offered job quality, or both, and who experiences these changes. The present analysis tests age-specific employment stocks. Hiring, offered-job characteristics, and individual transitions require separate data and are not inferred from these stocks.

All empirical inputs are official CPS microdata and our THAIE occupational assignments.

## Methods

### Data construction and exposure

The six exact groups are ages 22–25, 26–30, 31–34, 35–40, 41–49, and 50+. We include employed civilian noninstitutional people in all 50 states and DC, including employed people temporarily absent from work. Composite final CPS weights yield monthly population employment counts. Full-time and part-time follow PRFTLF classifications among people with PEMLR in 1 or 2. They describe employment-hours status, not permanent versus contractual employment.

The monthly inventory contains 118 calendar months, of which 117 are available. October 2025 is missing, not zero, and is not interpolated. We extend the newly constructed 2020–2026 monthly data back to 2017 to examine a pre-pandemic period. Independently rebuilt 2020–2026 Q5 counts match the previous CPS-only reconstruction. Occupational E and TIME are not substituted for THAIE. The existing 2019 employment-based THAIE classification is frozen throughout, including across age and employment-status groups. Scores are retrospective task measures, not observed adoption. Unmapped occupations remain unassigned.

CPS occupation codes before 2020 are probabilistically bridged to the common 2018 Census occupation universe using the existing verified crosswalk. These are expected allocations, not individually observed historical detailed occupations. Crosswalk uncertainty is not fully propagated into the standard errors. The 2020-start sensitivity avoids that historical bridge, at the cost of a short, pandemic-dominated pre-period. Software developers, Census 1021, remain THAIE Q4 and must not be relabeled as Q5 to reproduce a different framework's result.

### Model and estimand

For each age a and employment type h, the Poisson quasi-mean is

E[Y(occupation, industry, month)] = exp[occupation×industry FE + occupation×month-of-year FE + industry×calendar-date FE + beta×Q5×Post + Q5×pandemic-quarter terms].

Y is a survey-weighted aggregate employment count, not a binary employment probability. Post begins in December 2022, the first CPS reference month after November 30. This is an availability-date comparison, not observed firm adoption. The reported effect is 100[exp(beta)−1], a relative employment-growth contrast in Q5 versus Q1–Q4. It is not a percentage-point employment-rate effect and not the October 2026 endpoint alone.

The occupation-by-month-of-year effects permit each occupation to have its own recurring seasonal pattern. Industry-by-calendar-date effects absorb common industry-specific monthly shocks, including industry-wide pandemic recovery and composition changes. Occupation-by-industry effects absorb stable allocation differences. Eight Q5-specific quarter terms cover 2020–2021. This does not control every occupation-specific recovery, telework, monetary, cohort, or adoption shock.

### Support and inference

The primary full-time and part-time fits use identical rows within each age group. Fixed-effect categories with zero employment in either outcome throughout the estimation window are iteratively excluded to avoid separated nuisance effects. Zero counts within otherwise supported cells remain in the model. No monthly n≥30 display threshold is imposed on regressions. Thus, small and zero survey-count cells enter a working quasi-mean model; they should not be interpreted as literal administrative zero employment.

The common support retains 89.6%–98.8% of full-time counts and 99.7%–99.9% of part-time counts among exposure-covered workers in industries 1–13. This outcome-based support restriction can affect generalizability. An additional full-time-only-support analysis retains all full-time counts in that covered industry sample. The support file gives exact age-specific retention.

Primary score-sandwich standard errors cluster by detailed occupation, the exposure-assignment unit, allowing serial dependence within occupations. There are 478–522 occupation clusters. A two-way occupation-and-calendar-date sensitivity additionally permits contemporaneous cross-occupation dependence. Working t intervals use cluster degrees of freedom. These are not official CPS design-based intervals; household rotation, cross-occupation movement, survey design, and crosswalk estimation can introduce additional uncertainty. The absorbed fixed-effect rank convention is conservative in the independently checked reduced panel. Explicit-dummy statsmodels Poisson estimates and cluster standard errors match after aligning that finite-sample convention.

Holm correction covers the 12 primary age-by-outcome DID contrasts. A separate 60-test sensitivity-grid correction and fully reported secondary age and full-time/part-time contrasts prevent significance-driven selection. These analyses are exploratory, not preregistered. Marginal confidence intervals in tables and plots remain 95% pointwise intervals, not simultaneous family-wise bands.

### Event studies and robustness

Event studies use the monthly observations with three-month interaction bins, referenced to September–November 2022. The 2020–2021 quarters enter as separate pandemic nuisance controls rather than ordinary pretrend leads. The initial, final, and boundary bins can contain fewer than three observations; actual month coverage is provided. Joint pretrend tests examine all non-pandemic pre-event interactions. Neither a large pretrend p-value nor non-rejection proves parallel trends.

Predefined sensitivities add a Q5-specific linear trend, exclude 2020–2021, restrict the start to 2020, or place a January 2019 placebo within 2017–2019. The full-time-only-support sensitivity checks whether part-time support restrictions drive the full-time contrast. A fitted linear trend can absorb genuine gradual responses; its result is a sensitivity, not a definitive adjustment for all pre-existing trends.

## Results

### Primary DID estimates

| Age | Outcome | DID % | CI low | CI high | Raw p | Holm p, 12 tests | Joint pretrend p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 22–25 | FT | -9.026 | -16.255 | -1.172 | 0.025 | 0.279 | 0.037 |
| 22–25 | PT | -4.098 | -15.893 | 9.352 | 0.531 | 1.000 | 0.028 |
| 26–30 | FT | -3.881 | -12.281 | 5.323 | 0.395 | 1.000 | 0.105 |
| 26–30 | PT | -5.288 | -15.524 | 6.187 | 0.351 | 1.000 | 0.440 |
| 31–34 | FT | -2.332 | -10.433 | 6.502 | 0.593 | 1.000 | 0.181 |
| 31–34 | PT | -14.040 | -24.564 | -2.049 | 0.023 | 0.279 | 0.001 |
| 35–40 | FT | 0.109 | -7.859 | 8.766 | 0.979 | 1.000 | 0.034 |
| 35–40 | PT | -1.702 | -12.286 | 10.158 | 0.767 | 1.000 | 0.073 |
| 41–49 | FT | -3.799 | -11.929 | 5.082 | 0.389 | 1.000 | 0.096 |
| 41–49 | PT | -7.095 | -18.392 | 5.765 | 0.265 | 1.000 | 0.151 |
| 50+ | FT | -2.980 | -10.399 | 5.053 | 0.455 | 1.000 | 0.039 |
| 50+ | PT | -5.589 | -12.684 | 2.081 | 0.149 | 1.000 | 0.151 |

None of the 12 primary contrasts survives Holm correction. The ages 22–25 full-time estimate is -9.03% with a 95% interval of [-16.26, -1.17], nominal p=0.025, and Holm p=0.279. The ages 31–34 part-time contrast is nominally negative, not an increase. There is no statistically supported relative expansion in part-time employment in any of the six age groups.

### The original 2020-start monthly window

| Age | Outcome | 2020-start DID % | CI low | CI high | Raw p |
| --- | --- | --- | --- | --- | --- |
| 22–25 | FT | -2.385 | -10.247 | 6.166 | 0.572 |
| 22–25 | PT | -3.014 | -18.100 | 14.851 | 0.722 |
| 26–30 | FT | -1.721 | -7.475 | 4.391 | 0.572 |
| 26–30 | PT | -4.654 | -17.300 | 9.925 | 0.511 |
| 31–34 | FT | -4.377 | -10.765 | 2.469 | 0.204 |
| 31–34 | PT | -4.637 | -18.743 | 11.917 | 0.560 |
| 35–40 | FT | 6.481 | -0.536 | 13.994 | 0.071 |
| 35–40 | PT | 2.719 | -9.297 | 16.327 | 0.672 |
| 41–49 | FT | -0.017 | -5.484 | 5.767 | 0.995 |
| 41–49 | PT | 0.297 | -13.755 | 16.639 | 0.969 |
| 50+ | FT | -0.705 | -5.170 | 3.970 | 0.763 |
| 50+ | PT | 2.287 | -4.095 | 9.095 | 0.491 |

No contrast in the 2020-start window is nominally significant at .05. For ages 22–25 full-time employment, the estimate is −2.38% with a 95% interval of −10.25% to +6.17%, p=.572. The difference from the longer-window estimate demonstrates sensitivity to the pre-period and historical coding bridge. The short-window model also has little non-pandemic pre-treatment information. Neither window establishes AI causality.

### Pretrends and sensitivity

| age | outcome | pretrend_terms | pretrend_p | p_holm_pretrend12 |
| --- | --- | --- | --- | --- |
| 22–25 | FT | 16 | 0.037 | 0.343 |
| 22–25 | PT | 16 | 0.028 | 0.305 |
| 26–30 | FT | 16 | 0.105 | 0.576 |
| 26–30 | PT | 16 | 0.440 | 0.603 |
| 31–34 | FT | 16 | 0.181 | 0.603 |
| 31–34 | PT | 16 | 0.001 | 0.015 |
| 35–40 | FT | 16 | 0.034 | 0.343 |
| 35–40 | PT | 16 | 0.073 | 0.514 |
| 41–49 | FT | 16 | 0.096 | 0.576 |
| 41–49 | PT | 16 | 0.151 | 0.603 |
| 50+ | FT | 16 | 0.039 | 0.343 |
| 50+ | PT | 16 | 0.151 | 0.603 |

For ages 22–25 full-time employment, the joint pretrend p-value is approximately .037 before multiplicity correction. Its linear-trend-adjusted DID becomes -0.44%, p=0.924. Thus, the nominal baseline finding is insufficient for causal attribution. The full sensitivity matrix, two-way clustering, and full-time-only-support estimates are reported alongside these results rather than selected by significance.

### Absolute changes do not identify a relative part-time shift

Using identical January–September windows, ages 22–25 Q5 full-time employment decreased 3.34% between 2022 and 2026, while Q1–Q4 full-time employment increased 6.91%. Q5 part-time employment increased 6.53%, but Q1–Q4 part-time employment increased 20.11%. An absolute increase in Q5 part-time headcount can therefore coexist with a negative relative DID. Neither number shows that the same individuals moved from full-time to part-time work. These raw endpoint changes and the pooled adjusted DID are different estimands.

### Age and employment-type heterogeneity

Shared occupation-score covariance is retained when comparing models. The global equal-age-effects test gives p=.159 for full-time and p=.588 for part-time employment, with two-test Holm p=.317 and .588. None of the ten direct youngest-versus-older contrasts survives its own family correction. No full-time-versus-part-time contrast survives its six-test correction. A significant coefficient in one age group and an insignificant coefficient in another do not establish a difference between those groups.

## Discussion

The maintainable result is a qualified descriptive pattern of early-career full-time weakness, not a robust causal estimate. The monthly CPS construction independently reproduces the earlier raw young-worker pattern while showing why an absolute part-time increase cannot establish a relative shift toward part-time work. The more demanding occupation-clustered, industry-month-adjusted design yields nominal signals that do not survive the primary family correction and are sensitive to trend assumptions.

The data do not establish that AI caused job destruction, that effects end at a particular age, that older workers benefited causally, that hiring rather than separations is the mechanism, or that workers moved from permanent jobs into contracts. The 50+ group also combines aging and retirement-related composition changes. Employment stocks cannot distinguish these channels, and FT/PT classifications do not measure contract security or offered-job benefits.

Policy implications concern monitoring and evaluation. Track entry hiring, retention, hours, involuntary part-time status, training, and benefits together; evaluate paid entry pathways and adoption-related adaptation using observed employer adoption and linked worker histories. The current estimates do not support a quantified aggregate welfare loss, a demonstrated benefit of an intervention, or a claim that young workers alone experience AI displacement.

## Sources and reproducibility

- Official Basic Monthly CPS files and record layouts. https://www.census.gov/data/datasets/time-series/demo/cps/cps-basic.html
- Official Census data directory. https://www2.census.gov/programs-surveys/cps/datasets/
- Census occupation code lists and crosswalks. https://www.census.gov/topics/employment/industry-occupation/guidance/code-lists.html
- BLS occupational comparability guidance. https://www.bls.gov/cps/cpsoccind.htm
- Source URL and SHA256 inventory, frozen THAIE assignments, model grid, support diagnostics, and independent validation accompany this report.

The analysis is implemented in work/us_cps_only_monthly_did_20261125. Data-and-I/O smoke checks emit no images. Scientific figures are saved as separate PNG/SVG artifacts and displayed only in the requested research deliverables. Existing manuscripts remain unchanged.
