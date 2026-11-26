# Why did the youth full-time employment finding become less significant?

## CPS-only controlled specification audit

### Main finding

The approximately −9% coefficient does not disappear simply because the data become monthly or because more seasonal and industry controls are added. Statistical confidence changes substantially with the working covariance assumption and testing family. The coefficient itself becomes much smaller when the pre-period begins in2020 or an exposure-specific linear trend is added.

All empirical inputs are our official CPS reconstruction, our frozen THAIE classification, and the existing official occupation-code bridge. Ages remain exactly22–25; the outcome remains full-time employment; Q5 membership remains unchanged.

## 1. Reproduce the earlier result

The published legacy state-level annual January–September specification for2017–2026 is reproduced exactly. It excludes Alaska and Michigan, uses49 state clusters, and includes baseline state industry composition and adult pandemic/recovery context interacted with year. The estimate is −8.7636%, with a95% interval of −13.1082% to −4.2017% and p=.000434. The earlier industry-cell variant is also reproduced.

Reaggregating the official CPS records while retaining state and detailed occupation jointly reproduces the legacy count totals and the newer national monthly totals. No change in the frozen THAIE exposure definition is needed to explain the difference.

## 2. Change clustering while holding the fitted model fixed

| cluster | estimate_pct | se_log | ci_low_pct | ci_high_pct | p_value |
| --- | --- | --- | --- | --- | --- |
| state | -8.7636 | 0.0243 | -13.1082 | -4.2017 | 0.0004 |
| occupation | -8.7636 | 0.0554 | -18.1696 | 1.7236 | 0.0983 |
| state_and_occupation | -8.7636 | 0.0504 | -17.5581 | 0.9691 | 0.0751 |

The same legacy coefficient has a working occupation-score standard error 2.28 times the state-clustered standard error. Its p-value becomes .098. Two-way state-and-occupation score aggregation gives p=.075. The coefficient, sample, outcome, controls, and residual-row finite-sample scaling are held fixed; only the score grouping and associated cluster correction/degrees of freedom change.

The occupation grouping allows contributions from the same detailed occupation across states and years to move together. State-only grouping does not represent that particular dependence. This is a sensitivity of the same estimating equations, not proof that one grouping supplies the exact CPS survey variance. Both are working sandwich calculations. Complex household sampling, cross-occupation movement, code-bridge uncertainty, and remaining cross-cluster dependence are not fully modeled.

For a conditional count model, the contribution from a detailed-occupation employment cell is x(state,time) × [Q5(occupation) − fitted_Q5_share(state,time)] × weighted_FT_count. Contributions are summed by the requested cluster, and the same model Hessian is used. Recombining by state reproduces the original state covariance. An independent weighted binary GLM on real disaggregated CPS cells reproduces the occupation covariance after aligning the finite-sample convention.

## 3. Frequency alone is not new identifying information

The annual and monthly January–September legacy specifications have the same coefficient and the same cluster score sums when their predictors are held constant within state–year. Changing the number of grouped rows changes the software-style (N−1)/(N−K) correction, even though it has not added independent variation in the design. Removing that row-count correction makes the corresponding cluster standard errors invariant to annual versus monthly representation. The frequency audit reports both conventions rather than attributing this bookkeeping difference to new evidence.

Adding the actual October–December observations is different from relabeling frequency. The audit separately adds those observations, seasonal terms, flexible pandemic quarters, and the December2022 rather than January2023 cutoff. The complete legacy table reports every step.

## 4. Change one component around the current monthly model

| label | estimate_pct | se_log | p_value | N |
| --- | --- | --- | --- | --- |
| Current monthly reference | -9.0258 | 0.0421 | 0.0252 | 236585 |
| Occupation–industry + date FE | -9.8948 | 0.0453 | 0.0219 | 236585 |
| Add occupation-specific seasonality | -9.9019 | 0.0457 | 0.0229 | 236585 |
| Reference without occupation-season FE | -9.0758 | 0.0420 | 0.0239 | 236585 |
| Reference without Q5 pandemic-quarter terms | -8.6368 | 0.0364 | 0.0133 | 236585 |
| Exclude Alaska and Michigan | -9.3450 | 0.0427 | 0.0219 | 232687 |
| Use January–September only | -9.4493 | 0.0459 | 0.0310 | 179390 |
| Move post start to January2023 | -8.9814 | 0.0423 | 0.0265 | 236585 |
| End in December2025 | -8.0153 | 0.0417 | 0.0458 | 214614 |
| Long window on short-window support | -8.7028 | 0.0437 | 0.0379 | 162479 |
| Start in January2020, same retained units | -2.3848 | 0.0427 | 0.5724 | 112476 |
| Add Q5-specific linear trend | -0.4376 | 0.0459 | 0.9240 | 236585 |
| Require full-time support only | -8.1244 | 0.0412 | 0.0403 | 460811 |
| One-to-one occupation links, long window | -5.9745 | 0.0436 | 0.1586 | 116313 |
| Same one-to-one occupations, start2020 | -2.7074 | 0.0527 | 0.6028 | 80523 |

The monthly reference is the occupation–industry Poisson quasi-mean model with occupation–industry, occupation–month-of-year and industry–calendar-date fixed effects, Q5-specific pandemic-quarter terms, and occupation-clustered inference. Its estimate is −9.0258%, p=.02524. The new implementation reproduces its coefficient and standard error.

### Fixed effects and pandemic controls

On identical retained observations, adding occupation-specific seasonality changes the simpler fixed-effects estimate from −9.8948% to −9.9019%. Replacing common date effects with industry-specific date effects yields −9.0258%. Omitting occupation seasonality from the reference yields −9.0758%; omitting Q5 pandemic-quarter controls yields −8.6368%. Thus, these controls do not account for a disappearance of the negative point estimate.

### Geography, month coverage, cutoff, and endpoint

Excluding Alaska and Michigan gives −9.3450%. Keeping January–September only gives −9.4493%. Moving the post start from December2022 to January2023 gives −8.9814%. Ending in2025 gives −8.0153%. These changes are materially smaller than the change associated with the pre-period or linear trend. They concern distinct controlled comparisons and should not be added together as causal shares.

### Separate support changes from the pre-period

The full monthly reference is −9.0258%. Restricting the long window to the occupation–industry and occupation-season support retained in the short window gives −8.7028%. On those retained units, removing2017–2019 yields −2.3848%, p=.5724. Thus the support adjustment accounts for about +0.32 percentage points in this sequence, while the period change accounts for +6.32 percentage points. The2020-onward rows and employment counts are verified identical after freezing support.

A full-time-only-support check gives −8.1244%, retaining all covered full-time employment rather than requiring part-time support as well. This does not restore a multiplicity-robust or trend-robust finding.

### Historical occupation-code links

On the short-window support further restricted to one-to-one historical occupation links, the long-window estimate is −5.9745%, p=.1586, and the2020-start estimate is −2.7074%, p=.6028. The restriction changes the occupational sample as well as removing split links. It therefore cannot uniquely identify a code-bridge error. Removing2017–2019 simultaneously removes an earlier economic period and historical bridged observations; those explanations are not fully separated here.

### Differential linear trend

Adding a Q5-specific linear trend to the long-window reference produces −0.4376%, p=.924. This is strong sensitivity to the trend assumption. It does not prove the AI effect is zero, because a fitted trend can absorb a gradual response as well as pre-existing divergence. The previous joint pretrend p-value for young full-time employment was approximately .037 before correction across pretrend tests.

## 5. Multiple testing changes the decision, not the coefficient

| model | family | tests | adjusted_p | rule |
| --- | --- | --- | --- | --- |
| Current reference | Current raw | 1 | 0.0252 | Unadjusted |
| Current reference | Current two-outcome family | 2 | 0.0505 | Holm |
| Current reference | Current six-age primary family | 12 | 0.2792 | Holm |
| Current reference | Current full sensitivity family | 60 | 1.0000 | Holm |
| Legacy state-clustered | Legacy raw | 1 | 0.0004 | Unadjusted |
| Legacy state-clustered | Legacy actual two-outcome family | 2 | 0.0009 | Holm |
| Legacy state-clustered | Legacy actual 36-specification family | 36 | 0.0139 | Holm |
| Legacy state-clustered | Legacy 12-test upper bound | 12 | 0.0052 | Bonferroni bound; not a fabricated Holm family |

For the current reference, the raw p-value is .02524. It becomes .05048 in the two-outcome family, .27916 in the six-age12-test primary family, and1.000 in the60-test sensitivity family. The −9.0258% coefficient does not change. Bonferroni simultaneous intervals are reported separately and are not mislabeled as Holm-inverted intervals.

Multiplicity alone cannot explain away the earlier very small state-clustered p-value. Even its conservative12-test Bonferroni bound is about .00521. The change in the underlying inference, particularly score grouping, precedes the additional effect of the larger testing family.

## Interpretation

The earlier descriptive Q5 full-time weakness remains visible. The stronger claim of a robust AI-induced youth full-time decline is not sustained across the working covariance, pre-period, trend, and testing-family choices. The audit distinguishes a coefficient that stays near−9% but has wider uncertainty from specifications in which the estimated magnitude itself approaches zero.

The legacy state-ratio model and the detailed-occupation Poisson model are different mean models and aggregation units. The audit provides controlled comparisons within each framework; it does not pretend that their entire difference is a uniquely additive decomposition. Results depend on the chosen path and anchor. No variant is selected as a causal estimate because its p-value is smaller.

The data are repeated cross-sectional employment stocks. They do not identify hiring, layoffs, individual full-time-to-part-time movement, or permanent-to-contract transitions. THAIE measures potential exposure, not observed adoption. Working cluster intervals are not official CPS survey-design intervals.

## Visual and reproduction notes

Figures use a white publication background and editable SVG/PDF text. Q5 is a moderately saturated warm red, #C64F5A, and a thicker line with a thin white halo. Q1–Q4 use muted sage, slate, lavender and sand tones with white halos. Color identifies age rather than exposure in fixed-occupation age charts; software developers remain THAIE Q4 under our method. No numerical data are changed by styling.

The accompanying files contain all controlled contrasts, exact legacy reproductions, frequency-invariance checks, clustering validation, and figure data. Scientific figures are generated with a noninteractive backend and closed after saving. Data-and-I/O smoke checks emit no images.
