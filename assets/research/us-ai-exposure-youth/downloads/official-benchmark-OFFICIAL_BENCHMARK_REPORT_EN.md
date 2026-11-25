# Official-data benchmark and sample-to-population reconciliation

## Finding

The small numbers previously discussed were unweighted survey person-month records, not estimated workers. For Alabama, 49 observed Q5 full-time records across nine months imply approximately 19,942 employed people in an average month after survey weighting. Maine's 9 records imply about 2,077 people; California's 273 imply about 178,622. These are model-free survey-weighted population estimates, not a count of unique respondents. Repeated respondents can appear across months.

All 50 states and DC have finite observed-data estimates. All are now colored by default. The former display cutoff is retained as a caution flag, with a dagger and dashed border, and an optional higher-support filter. Showing an estimate does not make it precise. No interpolation or small-area model was used to create additional workers or states.

## Survey records versus estimated workers

| state | nQ5_FT | Q5_FT_average | population_average | rate_pct |
| --- | --- | --- | --- | --- |
| Alaska | 45.000 | 4,271.274 | 37,468.049 | 11.400 |
| Alabama | 49.000 | 19,941.895 | 276,831.423 | 7.204 |
| California | 273.000 | 178,622.052 | 2,011,377.556 | 8.881 |
| Delaware | 14.000 | 2,204.468 | 37,697.152 | 5.848 |
| Maine | 9.000 | 2,077.173 | 51,793.747 | 4.010 |

nQ5_FT is the unweighted number of person-month records across January–September. Q5_FT_average is the estimated population of Q5 full-time workers in an average month. The estimate equals the sum of composite survey weights divided by nine, not the unweighted count. Neither measure is the number of distinct people who held such jobs at any time during nine months.

The raw composite weight has four implied decimal places. The parser divides PWCMPWGT by 10,000. This is a decimal-place conversion, not a division of the estimated population by 10,000 after weighting. The resulting weight indicates the population represented by an observed record. Averaging nine monthly stocks prevents counting nine months of the same population as nine times as many people.

## National filtering funnel, January–September 2026

| stage | survey_person_months | monthly_average_survey_records | monthly_average_estimated_people |
| --- | --- | --- | --- |
| Civilian population 16+ | 681,009.000 | 75,667.667 | 275,080,631.551 |
| Employed 22–25 | 25,064.000 | 2,784.889 | 12,848,181.672 |
| Mapped occupation, employed 22–25 | 24,668.000 | 2,740.889 | 12,643,603.891 |
| Population 22–25 | 34,393.000 | 3,821.444 | 17,836,118.420 |
| Q5 employed 22–25 | 4,252.000 | 472.444 | 2,207,252.378 |
| Q5 full-time 22–25 | 3,492.000 | 388.000 | 1,799,279.979 |

The age group contains an estimated 17,836,118 residents, of whom 12,848,182 are employed. Q5 employed workers number 2,207,252; Q5 full-time workers number 1,799,280. Their rate among the whole age-group population is 10.09%. Equivalently, the employment–population ratio (72.03%) multiplied by the Q5 share among employed workers (17.18%) and the full-time share within Q5 employment (81.52%) gives that same rate. Thus, 10.09% is not the full-time share among Q5 workers, which is approximately 81.52%.

The national Q5 full-time sample averages only 388 records per month, spread across 51 state/DC areas. That explains why narrow state cells can contain only a few records each month while representing thousands of workers. Frozen occupational Q5 membership does not require exactly 20% of each state's young population to belong to Q5.

## Independent national BLS comparison

The independently published [BLS October 2026 Table A-1](https://www.bls.gov/news.release/empsit.t01.htm) reports counts in thousands and separates seasonally adjusted from unadjusted estimates. We compare the unadjusted September and October 2026 columns to fresh raw-file calculations, with the same population universe and six age/sex groups. All 84 count/rate checks are within publication rounding. The largest count gap is 490.35 people against numbers rounded to the nearest thousand; all rate gaps are within 0.05 percentage points.

| metric | BLS | ours | gap |
| --- | --- | --- | --- |
| P | 275,682,000.000 | 275,681,852.005 | -147.995 |
| LF | 170,906,000.000 | 170,906,369.890 | 369.890 |
| E | 164,183,000.000 | 164,182,561.507 | -438.493 |
| EPR | 59.600 | 59.555 | -0.045 |
| U | 6,724,000.000 | 6,723,808.383 | -191.617 |
| UR | 3.900 | 3.934 | 0.034 |
| N | 104,775,000.000 | 104,775,482.115 | 482.115 |

This establishes that the raw-file weight scale, broad population filters, age/sex grouping and employment-status recodes reproduce those official monthly quantities. It does not validate THAIE scores or the precision of each Q5 state estimate.

## Actual gaps in state publications

We also rebuilt all 12 months of 2024 and compared [BLS expanded state demographic data](https://www.bls.gov/lau/table14full24.htm), covering all 51 areas at ages 16+, 50 available age-20–24 rows and 51 age-25–34 rows. These are 152 available state-by-age comparisons. They are not compared to the map's nine-month or age-22–25 values, because that would mix periods and age definitions.

For ages 16+, the largest employment-level gap is 2.200%. The [2024 Geographic Profile](https://www.bls.gov/opub/geographic-profile/2024/) explicitly incorporates updated population controls. The original monthly public-use files retain their release-vintage weights. This difference matters. For California, the official state population is 31.618 million versus 31.205 million from the original files, and employment is 18.596 million versus 18.353 million. This is a population-control-vintage discrepancy, not hundreds of thousands of missing survey respondents.

As a diagnostic only, scaling each state's age-16+ estimate by the ratio of the official to reconstructed population reduces the largest employment discrepancy to 0.250% and the median to 0.010%. This documents that population-level alignment explains most of the broad state level gaps. It is not a valid calibration of age-22–25 occupational cells and was not applied to the map or regressions. Remaining discrepancies can include rounding, monthly versus annual control alignment and revised weighting.

Detailed-age gaps are larger. The maximum employment-level discrepancy is 4.588% for ages 20–24 and 2.429% for ages 25–34. The age-20–24 employment–population ratio differs by as much as 1.475 percentage points. Those residuals have not been fully reconciled to revised individual weights. We do not claim they are all rounding or that a broad state rescaling solves them. Published age groups also do not isolate age 22–25 or our THAIE Q5, so no identical official Q5 benchmark is available.

There is a further documented source of subgroup differences. [BLS public-use-file guidance](https://www.bls.gov/cps/data/public-use-file.htm) explains that age perturbation and associated public-file weight changes began in 2011, so fine age cells may not exactly match internal files used for official releases. This is a documented mechanism, not a measured decomposition of our residuals; quantifying its contribution requires internal comparison data. The [Census 2023 disclosure note](https://www.census.gov/programs-surveys/cps/technical-documentation/user-notes/cps_2023_01.html) also lists substate geography synthesis and earnings changes. Its geographic synthesis operates separately within states and does not justify assuming the state code itself was changed. We do not invent a 2023 state-boundary break to explain the results.

## Interpretation and correction

The confirmed presentation problem was emphasizing sample counts and suppressing finite state estimates in a way that looked like missing population data. The map now prioritizes estimated people and rates, labels survey records separately, and shows all available states. The original sample rule remains a visible warning rather than an automatic exclusion.

The statistical limitation remains real. A weighted estimate of thousands can be supported by few sampled records and have large uncertainty. The [BLS CPS reliability documentation](https://www.bls.gov/cps/methods/reliability-of-cps-estimates.htm) describes a sample survey rather than a census of all workers. The [LAUS FAQ](https://www.bls.gov/lau/laufaq.htm) explains population controls and identifies the Geographic Profile as CPS-based. LAUS modeled totals, payroll jobs, ACS respondents, and CPS employed residents are different estimands and cannot be substituted without aligning definitions.

Cross-year original-vintage map changes can reflect population-control updates, demographic shifts, occupation changes and sampling variation. They are descriptive differences, not an AI treatment effect. A defensible future revision should harmonize control vintages at the appropriate demographic level, assess design-based uncertainty or larger-sample compatible sources, and preserve the original-vintage results as a documented sensitivity. We did not fabricate official THAIE counts or mechanically rescale narrow cells to unrelated totals.

## Reproduction and scope

National benchmarks were parsed from the official web table's unadjusted columns. The state table was captured in complete numbered-line segments through the web reader because direct command-line BLS HTML/XLSX requests returned HTTP 403. Segments were merged by line number; overlapping lines were required to agree; all lines covering the state table were present. Official source URLs, parsed rows, gaps and scripts are supplied. This is external published-table comparison, beyond same-parser internal regeneration, but not a complete survey-design validation.

Existing CPS raw files, score definitions, main DID coefficients and sample-size flags were not modified. Map visibility changed. No images or graphs were emitted by numerical checks. Updated November 26, 2026.
