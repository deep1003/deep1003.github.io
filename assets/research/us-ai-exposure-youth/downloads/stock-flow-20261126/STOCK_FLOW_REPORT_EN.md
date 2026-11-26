# Locating relative employment weakness with linked CPS stock–flow accounting

## Main conclusion

The relative weakness of full-time employment among workers aged 22–25 in THAIE Q5 is reproduced in our CPS reconstruction. The available linked sample does not identify a single transition channel that reliably explains this weakness. After normalizing flows by group employment and balancing calendar months, additional entry weakness, increased nonemployment exit, full-time/part-time substitution, recorded occupation movement, and age-boundary movement all have conditional intervals spanning zero. A sizable survey/coverage reconciliation term prevents a clean behavioral attribution. These findings neither establish an AI effect nor establish that every mechanism is absent.

## Aligned samples and outcomes

We retain frozen THAIE assignments and use two prespecified calendar comparisons. The ACS-calendar comparison uses January 2017–December 2019 and January 2023–December 2024. The entry-DID-calendar comparison uses January 2019–October 2022 and January 2023–October 2026, retaining only genuinely observable post-period flow months. November–December 2022 remain connecting months for stock accounting, rather than target-period means. October 2025 has no observed stock; November 2025 has a stock but no adjacent-month flow. Both October and November 2025 are omitted from the latter target comparison.

Employment is CPS PEMLR 1 or 2. Full-time employment additionally requires PRFTLF 1, the current usual full-time classification. The same definition is used at both endpoints and for the repeated-cross-section stocks. These are employment headcounts, not employment-to-population rates. This CPS definition is not the ACS past-year hours proxy. Consequently, matching calendar periods does not make the two surveys' full-time measures identical.

The linkage domain is origin ages 21–26, allowing observed entry into age 22 and departure after age 25. Keys are household identifiers and person line number. Consecutive months must satisfy rotation progression, stable recorded sex, race and state, and age progression of zero or one year. Movers and unmatched respondents are not coded as economic exits. Pre-2020 occupational membership uses the audited fractional Census occupation bridge. Unmapped records are not assigned to the control group. January 2020 code-system changes are separated from ordinary recorded occupation flows.

## Stock comparison

Intervals below are conditional state-resampling diagnostics, not official CPS survey-design intervals or causal confidence intervals.

| period | measure | pre_months | post_months | Relative change |
| --- | --- | --- | --- | --- |
| ACS_calendar | E | 36 | 24 | -6.87% [-11.09, -2.47] |
| ACS_calendar | FT | 36 | 24 | -8.73% [-12.85, -4.74] |
| DID_calendar | E | 46 | 44 | -8.92% [-12.44, -5.31] |
| DID_calendar | FT | 46 | 44 | -9.31% [-13.33, -5.33] |

The relative change is `(Q5_post / Q5_pre) / (Q1–Q4_post / Q1–Q4_pre) − 1`. Under the entry-DID calendar, Q5 full-time employment averages 1,902,982 before and 1,884,576 after, whereas Q1–Q4 rises from 7,128,429 to 7,784,395. Thus relative weakness is much larger than Q5's own absolute headcount decline. A repeated age band is not a fixed cohort.

## Exact accounting

For every matched observation we partition the change in `age-in-range × employment × exposure membership`. The primary ordering allocates a simultaneous age-boundary and job change to aging first. A symmetric two-factor allocation is retained as a sensitivity check. Among workers remaining in the age band, nonemployment entry and exit are split into unemployment and nonparticipation. Full-time/part-time switches are distinguished from movements between exposure bands. Simultaneous schedule and occupation changes are allocated to schedule transitions first. Recorded occupational changes are not verified employer or job changes, and occupation movements within an exposure band have zero effect on that band's stock.

Matched flows use one common origin weight for both endpoints. The observed change in matched respondents' CPS weights is recorded separately. The difference between repeated-cross-section stock change and the estimated flows plus that weight change is retained as survey/coverage reconciliation. It can reflect rotation, nonresponse, movers, unmatched coverage, and estimation discrepancies. It is not an economic exit or migration estimate. The September–November 2025 stock change is an unresolved two-month flow gap; no person transition or imputed observation is constructed across it.

For each target comparison, post-minus-pre stock means telescope exactly into weighted monthly stock changes. Each component is accumulated with those same edge weights. An additive log-mean decomposition then satisfies `sum(component log points) = log(Q5_post/Q5_pre) − log(Q1–Q4_post/Q1–Q4_pre)`.

| component | Log-point contribution |
| --- | --- |
| Nonemployment entry | -28.705 |
| Nonemployment exit | +45.015 |
| Full-/part-time balance | +2.055 |
| Recorded occupation balance | +12.639 |
| Age-boundary balance | -20.209 |
| Mapping coverage | +2.106 |
| 2020 classification boundary | +0.840 |
| Survey/coverage reconciliation | -22.604 |
| Unobserved 2025 flow gap | -0.913 |

These are additive log points, not additive percentage changes or shares of an AI effect. Large positive and negative gross-flow contributions cancel. In particular, a negative entry contribution accumulated across connecting months does not demonstrate a post-2022 decline in the entry probability. Existing differences in replenishment rates can produce such contributions. The reconciliation contribution is −22.60 log points in the primary accounting and remains large under alternative response weights. The total is −9.775 log points, equivalent to the −9.31% relative stock change. This decomposition cannot credibly assign causal percentages to individual channels.

## Flow comparison with group-size and seasonal normalization

For each calendar month we divide weighted flow totals by the corresponding origin full-time stock. We then give the 12 calendar months equal weight within each window. These are signed monthly flow intensities per 100 origin full-time workers, not transition probabilities among the nonemployed. A positive entry value replenishes the stock; exit values are negative. The table reports post-minus-pre changes in Q5 minus the same changes in Q1–Q4. It is a descriptive contrast, not a controlled DID estimate.

| component | Q5 pre → post | Q1–Q4 pre → post | Relative change [95% interval] |
| --- | --- | --- | --- |
| Nonemployment entry | 4.262 → 3.321 | 4.849 → 3.811 | +0.097 [-0.339, +0.632] |
| Nonemployment exit | -3.722 → -3.063 | -4.961 → -3.923 | -0.379 [-0.983, +0.233] |
| Full-/part-time balance | 0.559 → 0.769 | 0.425 → 0.575 | +0.059 [-0.719, +0.856] |
| Recorded occupation balance | 0.305 → 0.237 | -0.080 → -0.056 | -0.092 [-1.072, +0.837] |
| Age-boundary balance | -1.270 → -1.226 | -0.929 → -0.711 | -0.175 [-0.713, +0.438] |

All five intervals cross zero. Entry intensity falls in both groups and does not fall more in Q5 after normalization. Exit intensity becomes less negative in both groups, with a smaller improvement in Q5. Full-time/part-time balance improves slightly more in Q5. Occupational and age-boundary balances have negative relative point estimates but are imprecise. The ACS-calendar sensitivity likewise does not isolate any of these five channels from zero. It uses 35 pre-period flow months rather than 36 stock months because December 2016 was not in the verified source cache; January 2017 remains in the stock comparison. This limitation does not break the exact period-mean stock identity.

## Attrition correction and robustness

The response model is estimated separately by destination year across all eligible origin workers aged 21–26, including nonemployed workers. Household cross-fitting uses two folds. Predictors include state, exact age, sex, race, Hispanic origin, education, labor-force status, usual full-time status, rotation month, calendar month, industry, and enrollment. The primary weight is origin CPS weight × inverse 0.75 planned rotation overlap × inverse predicted match probability. Probabilities are bounded at 0.05 and 0.995. We retain design-only weights, 99th-percentile inverse-response trimming, and entropy calibration to origin-only margins. Destination stocks are never forced to match.

Across all 115 observed adjacent pairs, there are 538,185 linked person-transition records in the origin-age domain. Repeated observations are not unique people. The smallest fitted probability is 0.365; calibration multipliers range approximately 0.546–3.913. Every origin calibration passed. Four weighting methods and two age allocations are saved. For the entry-DID calendar, the entry accounting contribution ranges from −23.01 to −30.71 log points; age-boundary balance ranges from −18.04 to −20.61. The survey/coverage term ranges from −16.41 to −22.68. Sign stability of these accounting terms does not convert them into post-treatment effects.

The 999 bootstrap draws resample 51 states including DC, jointly across windows, groups and components. They condition on fitted response models, calibrated weights, and the fixed occupation mapping. They do not incorporate first-stage estimation uncertainty, official CPS strata/PSUs, bridge uncertainty, or simultaneous-testing adjustment. Individual-channel intervals are diagnostic and should not be used to claim publication-grade causal significance. Response correction assumes matchability is conditionally ignorable; it cannot identify nonignorable attrition or recover unobserved movers.

## Interpretation and next verification

The defensible result remains relative weakness in the young high-exposure full-time employment stock. Neither a Q5-specific collapse of entry nor increased full-time-to-part-time displacement is established. The large residual and imprecise occupational/age flows prevent a clean attribution. This analysis does not replace the previous controlled entry DID, whose relative estimate was not statistically distinguishable from zero. Stock-flow accounting itself does not control differential pandemic recovery, industrial shocks, or age-specific cohort composition. Equal calendar-month weighting addresses seasonal composition only.

Before a mechanism claim, repeat fully controlled entry and exit models over exactly matched risk sets; compare multiple pre-period windows excluding pandemic months; audit occupational recoding and require persistent changes in a separately weighted three-interview sample; estimate nonresponse models with richer household history; and quantify mapping and official-design uncertainty. Contract permanence is not identified by usual full-time status. Remaining unexplained variation must not be labeled AI displacement.

## Reproducibility and sources

- `build.py` reconstructs linked records, response correction and state/month accounting from hashed source caches.
- `decompose.py` computes exact period-mean and log-mean decompositions with response-weight and age-allocation sensitivities.
- `flow_diagnostics.py` computes equal-calendar-month flow intensities and conditional uncertainty.
- Saved figures are generated without displaying images during smoke checks.

The BLS discusses the distinction between employment stocks and flows and their reconciliation in its [CPS flows overview](https://www.bls.gov/cps/cps_flows.htm). The historical methodology describes rotation overlap and classification/margin discrepancies in [Frazis et al. (2005)](https://www.bls.gov/opub/mlr/2005/09/art1full.pdf). Census documents dependent interviewing for industry and occupation in [CPS data collection](https://www.census.gov/programs-surveys/cps/technical-documentation/methodology/collecting-data.html). The [BLS recent flows documentation](https://www.bls.gov/web/empsit/cps_flows_recent.pdf) explains the missing October–November 2025 flows. Our accounting keeps unresolved coverage explicitly rather than forcing destination margins.
