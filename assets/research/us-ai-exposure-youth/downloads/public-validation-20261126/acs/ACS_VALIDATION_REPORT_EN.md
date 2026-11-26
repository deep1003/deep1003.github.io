# ACS annual and pooled independent validation

Completed November 26, 2026. We acquired five official national ACS 1-year person samples, linked our frozen THAIE occupational classification, and calculated national and state estimates for ages 22–25. The preferred descriptive comparison pools 2017–2019 against 2023–2024. Three pre-years and two post-years are available in this analysis; no third clean post-year is invented. This is an independent annual cross-check of occupational employment allocation, not a causal AI DID.

## Data actually processed

| Year | All person records | Eligible youth records | Weighted youth population | Mapped employment |
| --- | --- | --- | --- | --- |
| 2017 | 3,190,040 | 139,808 | 17,274,917 | 98.36% |
| 2018 | 3,214,539 | 139,311 | 17,057,865 | 98.20% |
| 2019 | 3,239,553 | 136,743 | 16,797,608 | 98.09% |
| 2023 | 3,405,809 | 142,045 | 16,967,412 | 98.28% |
| 2024 | 3,422,888 | 144,239 | 17,506,783 | 97.84% |

The five complete person archives contain **16,472,829 records**, of which **702,146 civilian noninstitutional youth records** enter these age-specific analyses. These are person records across separate annual samples, not necessarily unique people across years. Every year contains all 50 states and DC. Public outputs include 6,240 annual employment/hours/rate rows, 2,496 pooled employment/rate rows, 468 pooled change rows, and 312 pooled salary-mean rows.

The age-population denominator retains all eligible civilian noninstitutional people before occupation linkage. Armed Forces ESR codes 4/5 and institutional group quarters are excluded. Institutional status uses RELP=16 in 2017/2018 and RELSHIPP=37 thereafter, verified against year-specific official schemas. State codes are harmonized from ST or STATE. Years 2018 onward use Census 2018 occupation recodes and join directly to our frozen score table.

The 2017 sample uses Census 2010 occupation codes. We apply the verified 2010–2018 crosswalk to calculate **expected Q5, Q1–Q4 and unmapped contributions**. We preserve each original person record and multiply its survey weight by the corresponding band probability. We do not assign an unobserved detailed 2018 occupation to a worker. The three band probabilities sum to one, including unmapped contributions. Contributing record counts may overlap across bands in 2017; fractional record equivalents are reported separately. The frozen THAIE cutpoints are not recalculated by year, age or state.

## Pooled descriptive result

| Outcome | Relative change | 95% CI |
| --- | --- | --- |
| Employment | -7.92% | [-9.51, -6.33] |
| Usual past-year FT-hours proxy | -7.41% | [-9.26, -5.55] |
| Usual past-year PT-hours proxy | -11.26% | [-14.58, -7.94] |

Each pre-period count is the average of its three annual weighted totals; each post-period count is the average of its two annual totals. Relative change is 100×[(post_Q5/pre_Q5)/(post_Q1–Q4/pre_Q1–Q4)−1]. The contrast compares annual-average counts after normalizing each period by its number of years. Population-contribution rates use the ratio of annual-average group employment to annual-average eligible population, preserving within-year covariance through the replicate weights.

These results describe relative high-exposure occupational employment allocation across the specified periods. They do not prove AI caused any change, identify the exact timing after November 2022, demonstrate permanent-to-contract transitions, or follow the same workers. Comparing the pooled result with the explicitly labeled exploratory 2019-to-2024 endpoint check helps reveal sensitivity to period selection. The older endpoint tables and intervals are preserved in `acs_endpoint_changes_2019_2024.csv`.

## Annual profile

| year | band | outcome | People |
| --- | --- | --- | --- |
| 2017 | Q5 | employed | 2,542,858 |
| 2017 | Q5 | FT_proxy | 1,914,146 |
| 2017 | Q5 | PT_proxy | 628,711 |
| 2017 | Q1–Q4 | employed | 10,048,237 |
| 2017 | Q1–Q4 | FT_proxy | 6,935,837 |
| 2017 | Q1–Q4 | PT_proxy | 3,112,399 |
| 2018 | Q5 | employed | 2,521,090 |
| 2018 | Q5 | FT_proxy | 1,909,772 |
| 2018 | Q5 | PT_proxy | 611,318 |
| 2018 | Q1–Q4 | employed | 10,052,454 |
| 2018 | Q1–Q4 | FT_proxy | 7,024,573 |
| 2018 | Q1–Q4 | PT_proxy | 3,027,881 |
| 2019 | Q5 | employed | 2,425,454 |
| 2019 | Q5 | FT_proxy | 1,846,682 |
| 2019 | Q5 | PT_proxy | 578,772 |
| 2019 | Q1–Q4 | employed | 10,101,965 |
| 2019 | Q1–Q4 | FT_proxy | 7,119,526 |
| 2019 | Q1–Q4 | PT_proxy | 2,982,439 |
| 2023 | Q5 | employed | 2,405,559 |
| 2023 | Q5 | FT_proxy | 1,876,326 |
| 2023 | Q5 | PT_proxy | 529,233 |
| 2023 | Q1–Q4 | employed | 10,385,494 |
| 2023 | Q1–Q4 | FT_proxy | 7,432,318 |
| 2023 | Q1–Q4 | PT_proxy | 2,953,176 |
| 2024 | Q5 | employed | 2,398,141 |
| 2024 | Q5 | FT_proxy | 1,857,315 |
| 2024 | Q5 | PT_proxy | 540,826 |
| 2024 | Q1–Q4 | employed | 10,652,541 |
| 2024 | Q1–Q4 | FT_proxy | 7,557,467 |
| 2024 | Q1–Q4 | PT_proxy | 3,095,074 |

Employment is current civilian employment. The FT-hours proxy additionally requires usual weekly hours over the past 12 months of at least 35; the PT-hours proxy requires 1–34. These are not the CPS current usual FT/PT recodes and do not classify permanent or fixed-term contracts. Current occupational assignment and past-year hours do not share an identical reference period. The annual profile therefore supplements rather than replaces monthly CPS results.

## Annual salary means in pooled samples

| period | band | Mean annual salary | 95% CI |
| --- | --- | --- | --- |
| pre2017_2019 | Q5 | $37,111 | [$36,805, $37,417] |
| post2023_2024 | Q5 | $41,001 | [$40,556, $41,446] |
| pre2017_2019 | Q1–Q4 | $32,703 | [$32,560, $32,846] |
| post2023_2024 | Q1–Q4 | $35,737 | [$35,544, $35,930] |

These are ratios of average annual salary numerators to average annual salary-worker counts, not averages of medians. Salary observations require current civilian employment, COW 1–5 and positive WAGP. Amounts are adjusted by ADJINC/1,000,000 and official annual CPI-U to 2024 dollars. In 2017, fractional exposure probabilities enter these linear numerators and denominators; no supposedly observed within-band 2017 median is imputed. Annual earnings reflect weeks, hours, occupation composition, income allocation and topcoding. They are not hourly pay or within-person wage growth. National CPI-U adjustment does not remove regional cost-of-living differences.

## Sampling uncertainty and state precision

We retain all 80 supplied person replicate weights, including legitimate negative replicate weights for counts and means. For an annual statistic, the variance is (4/80) times the sum of squared replicate deviations. In a pooled statistic, each year's replicate perturbations vary that year's numerator and denominator jointly, divided by the number of years in its period. The variance sums the year-block components under an explicit independent-year approximation. The supplied person weights determine point estimates. Weighted people and weighted totals are not treated as independent sample sizes.

All intervals are pointwise normal 95% intervals, without multiple-testing adjustment. They quantify sampling uncertainty conditional on the fixed THAIE score and fixed crosswalk, excluding score-estimation and bridge uncertainty. Cross-year covariance is not estimated. The 2017 mapping adds a modeling assumption even though exposure-group contributions are computed transparently.

The state precision file reports contributing person records, fractional record equivalents, annual-average weighted counts, replicate standard errors and relative standard errors. Thresholds on record count do not guarantee precision. Pooling may make state cells more stable but reduces timing resolution. Uncontrolled zero SDR errors have uncertainty withheld pending the Census generalized-variance fallback. Full-weight annual medians are preserved for directly mapped years, but quantile SEs are withheld where this estimator is undefined for signed replicate weights; no replicate weights are clipped to fabricate a median interval.

## Scope and remaining limits

The planned three-year pre/two-year post pooling is now complete for all states. A third clean post-year, 2025, is unavailable in the verified PUMS endpoints; 2026 PUMS is also unavailable. The ACS person samples do not expose the monthly timing needed to center a monthly event study at November 2022. The 2020 experimental sample and 2021/2022 are not substituted into the clean post pool. A five-year ACS release crossing the treatment date would not fix that timing problem.

The ACS check can support or challenge the descriptive occupational pattern with a different survey and larger annual sample. It cannot by itself establish AI adoption, permanent-contract displacement, individual adaptation, or causal hiring effects. Further causal work still requires appropriate comparison trends, measured adoption or plausibly exogenous exposure variation and attention to pandemic and industry shocks.

## Reproduction and provenance

Scripts, per-file source records, logs and locally retained age-subset caches are in `work/us_public_validation_20261126/acs/`. Source archives were downloaded free from the official Census FTP site and verified by SHA-256. `acs_pooled_validation_checks.json` records year/geography coverage, unique annual cells and national-to-state reconciliation. `acs_processing_lineage.json` hashes the processing code, THAIE scores, crosswalk and CPI inputs. The annual employment, population and salary replicate-component files preserve the inputs needed to recompute pooled uncertainty.

- [Official ACS PUMS access](https://www.census.gov/programs-surveys/acs/microdata/access.html)
- [2017 ACS variables](https://api.census.gov/data/2017/acs/acs1/pums/variables.html)
- [2018 ACS variables](https://api.census.gov/data/2018/acs/acs1/pums/variables.html)
- [2024 ACS variables](https://api.census.gov/data/2024/acs/acs1/pums/variables.html)
- [ACS accuracy and replicate inference](https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/2024AccuracyPUMS.pdf)
- [Official CPI-U annual inputs](https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0?startyear=2017&endyear=2024&annualaverage=true)
