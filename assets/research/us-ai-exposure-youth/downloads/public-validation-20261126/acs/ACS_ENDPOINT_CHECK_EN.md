> Archived initial two-endpoint check. The full 2017–2019 / 2023–2024 extension is now complete and documented in ACS_VALIDATION_REPORT_EN.md. Statements about uncollected years below describe the earlier stage.

# ACS independent occupation-based validation

Completed November 26, 2026. Exact ages 22–25, own frozen THAIE mapping, national and all 50 states plus DC. This is an annual repeated-cross-section descriptive validation. It is not a November 2022 DID and does not establish AI causation.

## Completed coverage

| Year | All person records | Eligible 22–25 records | Weighted 22–25 people | Employed THAIE coverage |
| --- | --- | --- | --- | --- |
| 2019 | 3239553 | 136743 | 16797608 | 98.09% |
| 2024 | 3422888 | 144239 | 17506783 | 97.84% |

The two official national person archives contain 6,662,441 person records. All 51 geographies are present in each year. In total, 2,496 employment/hours/contribution rows and 624 salary rows were computed. Both complete archives were newly acquired from Census, hashed, and parsed in chunks. Only necessary columns and ages 22–25 were retained locally.

The population universe is civilian noninstitutional ages 22–25. Institutional group quarters (RELSHIPP = 37) and active Armed Forces (ESR = 4 or 5) are excluded. Both 2019 and 2024 use Census 2018 occupation codes; they join directly to the unchanged 547-occupation THAIE score universe. No CPS historical bridge is applied to these ACS years. The frozen national quintile cutpoints are retained across states and years.

## Main descriptive cross-check

| outcome | Q5_pre_n | Q5_post_n | estimate_pct | 95% CI |
| --- | --- | --- | --- | --- |
| employed | 20168 | 19668 | -6.24% | [-8.80, -3.67] |
| FT_proxy | 15199 | 14933 | -5.25% | [-8.20, -2.31] |
| PT_proxy | 4969 | 4735 | -9.96% | [-15.16, -4.76] |

The relative endpoint statistic is 100 × [(Q5_2024/Q5_2019)/(Q1–Q4_2024/Q1–Q4_2019)−1]. The table supports relative weakness of high-exposure occupational employment across this five-year interval. It does not locate that divergence after ChatGPT. It also does not show a shift into part-time employment. In Q5 itself, the FT-hours proxy changed +0.58% and the PT-hours proxy −6.56%; relative comparisons incorporate growth in the lower-exposure group.

FT_proxy means current civilian employment and usual past-12-month weekly hours ≥35; PT_proxy means current employment and usual past-12-month hours 1–34. These differ from CPS current usual FT/PT recodes and do not identify contract permanence. Occupation refers to the current or latest job, while hours refer to the past year. Employment divided by the entire eligible age population is labeled an exposure-group contribution to the overall employment rate, not an occupation-specific employment probability or unemployment rate.

## Annual salary cross-check

| year | band | outcome | unweighted_n | Estimate | variance_status |
| --- | --- | --- | --- | --- | --- |
| 2019 | Q5 | annual_salary_mean_2024USD | 19702 | $37,661 | replicate_SDR |
| 2019 | Q5 | annual_salary_median_2024USD | 19702 | $32,225 | replicate_estimator_undefined_SE_withheld |
| 2019 | Q1–Q4 | annual_salary_mean_2024USD | 77987 | $33,858 | replicate_SDR |
| 2019 | Q1–Q4 | annual_salary_median_2024USD | 77987 | $28,507 | replicate_estimator_undefined_SE_withheld |
| 2024 | Q5 | annual_salary_mean_2024USD | 19080 | $41,478 | replicate_SDR |
| 2024 | Q5 | annual_salary_median_2024USD | 19080 | $35,534 | replicate_estimator_undefined_SE_withheld |
| 2024 | Q1–Q4 | annual_salary_mean_2024USD | 82646 | $35,804 | replicate_SDR |
| 2024 | Q1–Q4 | annual_salary_median_2024USD | 82646 | $30,458 | replicate_estimator_undefined_SE_withheld |

Salary estimates condition on current civilian employment, wage/salary class of worker 1–5, and positive past-year salary income. Income is adjusted by ADJINC/1,000,000 then by annual CPI-U to 2024 dollars. Official BLS CPI-U annual averages are 255.657 for 2019 and 313.689 for 2024. Annual salary includes differences in weeks/hours worked and composition. It is not an hourly wage or a longitudinal gain for the same individuals. Public income topcoding and allocation can affect distributions.

## Replicate inference and precision

Counts, rates, and means use all 80 provided person replicate weights. Standard errors are sqrt[(4/80)×sum_r(theta_r−theta)^2]. State and national calculations retain the supplied negative replicate weights for linear totals and means; they are valid variance inputs. The minimum raw replicate weight among retained-age records is −178 in 2019 and −1125 in 2024. They are not replaced by zero.

A two-year endpoint statistic uses separate 80-replicate perturbations of 2019 and 2024 and sums the year-block variance components under an explicit independent-year approximation. Intervals are pointwise normal 95% intervals, without multiplicity correction. They quantify sampling uncertainty in this descriptive statistic; they do not account for THAIE measurement error or identify causal effects.

Full-weight medians are reported. For this quantile estimator, negative replicate weights do not define a probability distribution, so affected median standard errors are withheld rather than clipping weights or silently dropping the full-weight point estimate. Zero SDR errors/uncontrolled zero estimates also have uncertainty withheld pending the Census generalized-variance fallback. 47 median cells have an explicit non-SDR variance status. Means provide the complete linear earnings cross-check in the meantime.

There are 40 state/year/Q5 FT-or-PT cells with fewer than 30 actual records. The detailed precision table reports actual n, weighted people, Kish weight-only diagnostic, replicate SE and relative SE. State estimates must not be read as uniformly precise. A threshold on n alone is not a precision guarantee. Negative normal lower bounds in sparse cells are a warning about the approximation, not negative population counts.

## What remains incomplete

2017–2018 and 2023 national files were not collected in this run, so the intended three-year baseline/two-year post pooling is not yet complete. The 2025 PUMS remains unverified/unreleased in the checked official endpoints, and the 2026 PUMS is unavailable. Only two annual endpoints were compared. No ACS monthly event study, individual transition, permanent-to-contract transition, or causal AI effect was estimated. Further work should complete pre/post annual profiles, harmonize missing historical code regimes, and prespecify pooling and precision rules.

## Reproduction and sources

Code and logs are in `work/us_public_validation_20261126/acs/`. Public outputs are in this directory. `acs_validation_checks.json` records passed data-I/O checks, source manifests record URLs/checksums, and `acs_employment_replicate_totals.parquet` preserves the 80 replicate totals.

- [2019 official national person ZIP](https://www2.census.gov/programs-surveys/acs/data/pums/2019/1-Year/csv_pus.zip)
- [2024 official national person ZIP](https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/csv_pus.zip)
- [2019 variable schema](https://api.census.gov/data/2019/acs/acs1/pums/variables.html)
- [2024 variable schema](https://api.census.gov/data/2024/acs/acs1/pums/variables.html)
- [ACS 2024 accuracy and replicate weights](https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/2024AccuracyPUMS.pdf)
- [Official BLS CPI-U API](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0?startyear=2019&endyear=2024&annualaverage=true)
