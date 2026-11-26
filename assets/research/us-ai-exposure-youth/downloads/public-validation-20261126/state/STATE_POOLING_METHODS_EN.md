# Three-year state CPS estimates

Built November 26, 2026. All estimates use our frozen occupational THAIE assignment and observed Basic Monthly CPS records. Ages are 22–25 at each interview. This is a repeated cross-sectional period analysis, not a cohort of the same young people followed for three years.

## Construction and checks

The four periods are January 2017–December 2019, November 2019–October 2022, December 2022–November 2025, and November 2023–October 2026. The central comparison uses 36 calendar months before and after the excluded November 2022 transition month. Each post period has 35 observed months because October 2025 was not collected. No missing month or person is imputed. Average monthly population and employment divide the summed weights by observed months. Rates use the ratio of weighted sums, rather than an unweighted average of monthly rates.

The numerator is full-time or part-time employment in occupational Q5 or Q1–Q4. The main denominator is every civilian noninstitutional resident aged 22–25 in the state, including unemployed and nonparticipants. A second denominator is employment within the same exposure band; that quantity is an FT/PT composition share and must not be called a population employment rate. Unmapped occupations remain outside the two mapped numerators, while all eligible people remain in the population denominator.

The underlying parser was extended locally to retain HRHHID, HRHHID2 and PULINENO. These keys are used for dependence diagnostics and do not establish validated longitudinal person matches. Private working files remain under work/us_public_validation_20261126/state; output tables contain aggregates only.

Pre-2020 occupation codes use the existing audited 2010-to-2018 probabilistic bridge. Mapping probabilities are summed within each THAIE band before multiplying person contributions. This preserves the population denominator and avoids duplicating respondents. Historical band counts are expected allocations, not individually observed detailed occupations. Crosswalk uncertainty and THAIE measurement uncertainty are not propagated.

All 117 available months passed independent comparisons against the existing audited state Q5 FT/PT numerators and national age-group population. Each date–person-key pair is unique. FT and PT sum to employment within each mapped band. All 51 state/DC estimates are finite in every period. Exact checks appear in FRESH_SMOKE_CHECKS.json. No plots were rendered by these checks.

## Uncertainty

For a weighted ratio r = sum(x)/sum(w), the household score is the within-household sum of x − r*w. The working variance is K/(K−1) times the sum of squared household scores divided by sum(w)^2. Household keys combine state, HRHHID and HRHHID2 across observed months. This accounts for dependence within repeated household IDs under a working independent-household model.

It does not reconstruct confidential survey strata or primary sampling units, public-file perturbation uncertainty, occupation-level common shocks, historical crosswalk uncertainty, or exposure-score uncertainty. The intervals are therefore labelled working household-cluster intervals, not official design-based CPS confidence intervals. Intervals are withheld for fewer than five positive numerator records or degenerate variance; zero observed events do not establish a zero population rate. Person-key counts are ID counts, not validated counts of distinct people. Displaying every finite point estimate is not a claim that every state estimate is precise.

## Support and national levels

For November 2023–October 2026, 15,447 observed Q5 full-time person-month records contribute nationally. The smallest state cell contains 89 records and the median contains 228. Under the working household model, the largest state relative standard error is approximately 19.1%. These values describe the pooled period and cannot be compared with a single-year map as though the underlying time period were unchanged.

National Q5 full-time employment divided by the entire same-age population is 11.217% in the symmetric pre-period, 10.910% in the symmetric post-period, and 10.609% in the latest 36-calendar-month period. In the latest period, Q5 full-time employment averages approximately 1.866 million per observed month. Full-time workers constitute 81.692% of Q5 employed youth. The 10.609% and 81.692% quantities have different denominators.

## Relative changes

The unadjusted relative change is 100 × [(Q5_post/Q1–Q4_post)/(Q5_pre/Q1–Q4_pre) − 1], using weighted employment sums within each period. Observed-month normalization cancels within each ratio. Joint household scores retain covariance when IDs appear on both sides. National and state descriptive contrasts have separate Holm correction families of nine and 459 planned contrasts; intervals are marginal working intervals, not simultaneous intervals. Unestimable zero-count log contrasts remain unreported and do not reduce the multiplicity family size. Sparse or degenerate contrast intervals are withheld.

For the symmetric periods, the national Q5/Q1–Q4 FT contrast is −7.37%, with a working interval of approximately −11.79% to −2.72%. This is an unadjusted descriptive contrast, not the previous controlled occupation-panel DID. It does not control industry shocks, occupational common shocks, population composition, or differential recovery. Its working p-value must not be used to replace the more conservative uncertainty in the controlled research model. The main research conclusion about causality remains unchanged.

The cached PT_econ variable means PRWKSTAT categories 3/6. It measures economic short actual hours and can include people whose usual schedule remains full-time. It must not be labelled usual involuntary part-time employment. The separately rebuilt linked-CPS module imposes destination usual PT when estimating FT-to-economic-PT transitions.

## Reproduction

Run work/us_public_validation_20261126/state/build_pooled.py and then validate_and_compare.py in the project Python environment. The first script rebuilds provenance-checked youth caches; the second verifies original aggregates and calculates descriptive relative contrasts. Read the uncertainty labels before interpreting any interval or p-value.
