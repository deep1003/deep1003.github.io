# Following workers after the generative AI shock

How have employment opportunities and job quality changed for young people entering the labour market in highly AI-exposed fields, and how far up the age distribution do these changes extend?

This extension follows observed worker adaptation. It adds attrition-corrected linked CPS transitions and a newly acquired SIPP person-month panel. The estimates describe differential changes by baseline exposure. They do not identify individual AI adoption or establish that AI caused those changes.

## Findings

Custom response correction changes the linked CPS estimates little. For THAIE Q5 workers aged 22–25, the adjusted occupational full-time-to-part-time differential is approximately +0.21 percentage points after calibration, with a 95% interval of about −1.34 to +1.76. The corresponding economic-short-hours estimate is about +0.52 pp, with an interval of −0.42 to +1.45. Neither establishes increased downgrading. The intervals condition on the fitted correction weights.

The SIPP main cohort contains 2,850 baseline workers observed for 48 months in 2021–2024, or 136,800 person-months. Of these, 2,843 have the complete outcome periods required by the common-sample models. For all baseline workers, adjusted THAIE Q5 relative changes are +0.70 weekly hours [−0.94, +2.35], +1.72 pp in lower monthly hours intensity [−1.88, +5.32], and −$479 in monthly real earnings [−$1,145, +$187]. These intervals allow meaningful adverse and favourable changes.

The 22–25 THAIE group contains only 28 high-exposure people. Its lower-intensity estimate changes from +9.12 pp in the basic specification to +32.33 pp in the adjusted specification. The adjusted annual pre-period contrast is already −15.00 pp [−29.51, −0.49]. The post estimate does not survive the predeclared primary-family Holm correction. This combination is not convincing evidence of an AI-induced transition out of full-time work. Employment entry among this baseline-worker cohort can also increase the lower-intensity employment share.

Directly observed monthly transitions do not support a clear increase in movement from full-time intensity to lower intensity, or from employee work to other arrangements. No SIPP DID survives correction over the broad planned family. This does not demonstrate that effects are absent. Small high-exposure and subgroup samples leave wide uncertainty.

## Sources and observation windows

Basic CPS records cover January–September of 2010–2026, with adjacent-month links restricted to origin rotation groups eligible for the following month. Main corrected transition models use 2017–2026 and a 2023–2026 post period. The new SIPP analysis uses the 2022, 2023, 2024 and 2025 survey files, which refer to calendar years 2021, 2022, 2023 and 2024. The 2025 file being released in 2026 does not create 2026 outcomes. SIPP and CPS are analysed separately and are not linked to one another.

Official four-year SIPP longitudinal weights identify 6,122 people. The main analytical cohort restricts to adults with positive baseline job hours, a covered 2021 occupation, and continuous US survey-frame membership across all 48 months. Eleven otherwise eligible people are excluded by that final frame restriction. This defines a selected baseline-worker cohort. It does not represent all later labour-market entrants or all US residents. Never-employed baseline entrants cannot be assigned baseline occupational exposure in this design.

Age is frozen in October 2022. Baseline vulnerability characteristics are frozen in 2021. The analysis covers ages 16 and above, with separate 22–25, 26–29 and 30–34 bands, older groups, and comparisons within female, no-BA, Black, Hispanic, foreign-born, work-limiting disability and household-income-below-200%-of-poverty groups. These characteristics mark distinct dimensions of potential disadvantage, rather than a uniform vulnerable category. Many youth-by-vulnerability cells fail minimum support and remain explicitly unsupported.

## CPS response correction

Next-month linkage is modelled from origin state, age, sex, race, Hispanic origin, education, citizenship, marital status, labour-force status, major occupation and industry, rotation, calendar month and hours categories. A household-separated two-fold cross-fit logistic model produces inverse-response weights. We compare origin weights, inverse-probability weights, 99th-percentile-trimmed response factors, and calibrated weights. Calibration targets the eligible origin sample's weighted demographic, state, labour-status and month-by-rotation margins.

All yearly models converge. Maximum relative calibration error is below 0.000001, with no structural-zero target cells. Two fitted probabilities in 2021 require the predeclared probability safeguard; the remaining years require none. The safeguard, trimming and calibration are documented in the weight audit. The correction assumes response is ignorable conditional on observed origin variables. It cannot recover destinations of unobserved movers or solve nonignorable attrition. These custom weights are not official CPS gross-flow weights or IPUMS linkage weights.

Adjusted state-panel transition contrasts retain common support across the three exposure measures and the same fixed 2019 origin denominator weights across correction methods. They include baseline industry composition and pandemic-recovery controls. State-cluster uncertainty conditions on the estimated response and calibration weights and therefore omits weight-estimation uncertainty. Matched pairs are repeated observations, not unique independent workers.

## SIPP identification and estimation

Occupational exposure is assigned once using the 2021 occupation contributing the largest cumulative monthly-average hours. At least 90% of baseline job hours must map to the shared occupation universe. Baseline matched-hour coverage is 97.64%. Existing exposure, THAIE and simple time weighting use the same people, outcomes, cutoffs and periods. Q5 membership uses the existing frozen 2019 occupational quintile cutoffs. Exposure never updates in response to later job changes.

For each person, the pooled contrast is average January–September outcomes in 2023–2024 minus the corresponding average in 2021–2022. A weighted regression compares Q5 with Q1–Q4. It is a within-person change design, equivalent to the two-period person fixed-effect contrast. The adjusted specification adds baseline state effects on changes, age and age squared, and the baseline demographic flags. Annual event contrasts use 2022 as reference. There is only one annual pre-event contrast, so this panel cannot establish a long parallel trend.

Point estimates use FINYR4. All 240 official replicate weights refit each regression; Fay BRR with factor 0.5 supplies variance, using 4/240 times the sum of squared replicate deviations. Unsupported comparisons remain missing, rather than becoming zeros. The planned broad DID family has 1,440 comparisons, and the primary three-age family has 180. Holm-adjusted probabilities are retained alongside unadjusted values. The interpretation is exploratory and conditional on baseline exposure, not causal adoption DID.

Monthly observed transitions use the same people but changing origin risk sets. They compare February–September transitions in 2023–2024 against 2021–2022. These pooled flow contrasts are descriptive and do not use the adjusted change-regression covariates. They distinguish actual individual moves from a changing cross-sectional share.

## Outcome interpretation

SIPP hours sum monthly-average weekly hours over all jobs. Nonworking weeks within a month contribute zero. The 35-hour split measures monthly employment intensity; a partial job month can fall below 35 even when usual weekly work is full-time. It must not be labelled the CPS usual full-time/part-time classification. SIPP lower-intensity employment is not itself involuntary part-time work.

TPEARN measures earnings and business profits, including negative losses. TPTOTINC includes other personal income. Both are deflated with monthly CPI-U to September 2026 dollars. Missing earnings are set to zero only for recorded nonemployment months. Employed missing earnings remain missing. Later nonemployed people remain in the cohort, avoiding a comparison limited to employment survivors. Neither series is an hourly wage measure.

CPS economic short hours can occur among usually full-time workers and overlaps that usual-status category. It is not a subset of usual part-time work. Employee-to-self-employment is not permanent-to-contract employment.

## Can permanent-to-contract transitions be identified?

Not cleanly from these SIPP fields. JBORSE identifies employer, own-business/self-employment, or other arrangements. CONCHK asks only people reporting other arrangements whether an ongoing employer arrangement exists. CNTRC concerns union contract coverage. It does not identify fixed-term employment. RSEND can flag a temporary or seasonal job ending, but is observed only for ended spells. Job IDs allow tracking job changes but do not supply contract duration.

Accordingly, the outputs report employee-to-self-employment, employee-to-other-arrangement and a narrowly labelled no-ongoing-arrangement proxy. None is renamed permanent-to-contract. A validated contract-duration or contingent-work measure, with its restricted universe and timing, is needed for that stronger research claim. The separate variable audit records which fields are available and which have actually been used.

## Results tables

### Common-sample SIPP changes

| age       | measure   | outcome        |   estimate |   ci_low |   ci_high |   persons |   high_persons |
|:----------|:----------|:---------------|-----------:|---------:|----------:|----------:|---------------:|
| age22_25  | E         | hours          |       2.47 |    -5.02 |      9.95 |       153 |             34 |
| age22_25  | E         | part_intensity |       7.80 |    -9.96 |     25.57 |       153 |             34 |
| age22_25  | E         | real_earnings  |     118.97 |  -951.09 |   1189.04 |       153 |             34 |
| age22_25  | THAIE     | hours          |       1.81 |    -6.84 |     10.46 |       153 |             28 |
| age22_25  | THAIE     | part_intensity |      32.33 |    13.01 |     51.65 |       153 |             28 |
| age22_25  | THAIE     | real_earnings  |     -10.72 | -1260.50 |   1239.07 |       153 |             28 |
| age22_25  | TIME      | hours          |       0.37 |    -8.96 |      9.71 |       153 |             25 |
| age22_25  | TIME      | part_intensity |      15.99 |     0.97 |     31.00 |       153 |             25 |
| age22_25  | TIME      | real_earnings  |     239.67 | -1158.11 |   1637.45 |       153 |             25 |
| age26_29  | E         | hours          |       0.38 |    -5.68 |      6.45 |       198 |             45 |
| age26_29  | E         | part_intensity |       3.58 |    -7.71 |     14.87 |       198 |             45 |
| age26_29  | E         | real_earnings  |    -103.45 | -2133.13 |   1926.23 |       198 |             45 |
| age26_29  | THAIE     | hours          |       1.24 |    -5.27 |      7.76 |       198 |             33 |
| age26_29  | THAIE     | part_intensity |       2.07 |   -11.18 |     15.31 |       198 |             33 |
| age26_29  | THAIE     | real_earnings  |     313.14 | -1625.71 |   2251.99 |       198 |             33 |
| age26_29  | TIME      | hours          |       1.15 |    -5.28 |      7.58 |       198 |             35 |
| age26_29  | TIME      | part_intensity |       0.84 |   -11.25 |     12.93 |       198 |             35 |
| age26_29  | TIME      | real_earnings  |    -347.11 | -2769.12 |   2074.89 |       198 |             35 |
| age30_34  | E         | hours          |       0.15 |    -3.93 |      4.23 |       268 |             49 |
| age30_34  | E         | part_intensity |      -0.42 |    -8.76 |      7.91 |       268 |             49 |
| age30_34  | E         | real_earnings  |     721.73 | -1605.05 |   3048.51 |       268 |             49 |
| age30_34  | THAIE     | hours          |      -1.97 |    -6.72 |      2.78 |       268 |             47 |
| age30_34  | THAIE     | part_intensity |       5.43 |    -4.71 |     15.57 |       268 |             47 |
| age30_34  | THAIE     | real_earnings  |   -1647.33 | -4253.28 |    958.62 |       268 |             47 |
| age30_34  | TIME      | hours          |      -4.15 |    -8.49 |      0.18 |       268 |             51 |
| age30_34  | TIME      | part_intensity |       4.50 |    -4.67 |     13.68 |       268 |             51 |
| age30_34  | TIME      | real_earnings  |   -1921.72 | -4433.32 |    589.88 |       268 |             51 |
| all16plus | E         | hours          |       0.25 |    -1.33 |      1.83 |      2843 |            662 |
| all16plus | E         | part_intensity |       1.31 |    -1.94 |      4.55 |      2843 |            662 |
| all16plus | E         | real_earnings  |    -218.48 |  -864.38 |    427.42 |      2843 |            662 |
| all16plus | THAIE     | hours          |       0.70 |    -0.94 |      2.35 |      2843 |            604 |
| all16plus | THAIE     | part_intensity |       1.72 |    -1.88 |      5.32 |      2843 |            604 |
| all16plus | THAIE     | real_earnings  |    -478.71 | -1144.51 |    187.09 |      2843 |            604 |
| all16plus | TIME      | hours          |      -0.34 |    -1.91 |      1.22 |      2843 |            604 |
| all16plus | TIME      | part_intensity |       1.69 |    -1.73 |      5.10 |      2843 |            604 |
| all16plus | TIME      | real_earnings  |    -712.47 | -1412.43 |    -12.50 |      2843 |            604 |

### Observed THAIE monthly transition contrasts

| age       | transition                   |   estimate |   ci_low |   ci_high | status    |
|:----------|:-----------------------------|-----------:|---------:|----------:|:----------|
| all16plus | full_to_part                 |      -0.14 |    -0.57 |      0.29 | estimated |
| all16plus | full_to_nonemployment        |      -0.03 |    -0.26 |      0.21 | estimated |
| all16plus | employee_to_self             |       0.03 |    -0.05 |      0.11 | estimated |
| all16plus | employee_to_other            |      -0.02 |    -0.08 |      0.03 | estimated |
| all16plus | employee_to_no_ongoing_other |       0.01 |    -0.01 |      0.02 | estimated |
| all16plus | employee_to_nonemployment    |      -0.27 |    -0.60 |      0.06 | estimated |
| age22_34  | full_to_part                 |      -0.40 |    -1.54 |      0.73 | estimated |
| age22_34  | full_to_nonemployment        |      -0.02 |    -0.61 |      0.57 | estimated |
| age22_34  | employee_to_self             |       0.07 |    -0.12 |      0.25 | estimated |
| age22_34  | employee_to_other            |       0.03 |    -0.01 |      0.08 | estimated |
| age22_34  | employee_to_no_ongoing_other |       0.02 |    -0.02 |      0.06 | estimated |
| age22_34  | employee_to_nonemployment    |      -0.70 |    -1.61 |      0.20 | estimated |

## Reproducibility and verification

The scripts retain raw-source lineage and separate public aggregate outputs from internal person-level public-use records. No person or household identifiers are exported in the deliverables. Independent checks reproduce uncorrected CPS counts, verify transition accounting and panel keys, confirm longitudinal weight equality to replicate zero, and independently refit the all-adult THAIE hours regression and all 240 replicate regressions using statsmodels. Point and standard-error differences are below 0.0000001. Smoke checks emit no figures. Plot files are generated separately.

## Primary documentation

- [Census SIPP datasets](https://www.census.gov/programs-surveys/sipp/data/datasets.html)
- [2025 SIPP data and longitudinal files](https://www.census.gov/programs-surveys/sipp/data/datasets/2025-data/2025.html)
- [Census SIPP weighting](https://www.census.gov/programs-surveys/sipp/methodology/weighting.html)
- [2025 source and accuracy statement](https://www2.census.gov/programs-surveys/sipp/tech-documentation/source-accuracy-statements/2025/SIPP-2025-SA.pdf)
- [2025 SIPP dictionary](https://www2.census.gov/programs-surveys/sipp/tech-documentation/data-dictionaries/2025/2025_SIPP_Data_Dictionary.pdf)
- [2025 SIPP instrument](https://www2.census.gov/programs-surveys/sipp/tech-documentation/2025/2025_SIPP_PU_Instrument_Specifications.pdf)
- [IPUMS CPS linking documentation](https://cps.ipums.org/cps/cps_linking_documentation.shtml)

## Baseline vulnerability domains

These are within-domain exposure contrasts, not formal tests of differences between demographic groups. The foreign-born earnings interval excludes zero before multiplicity correction, but does not survive the planned correction. Small youth cells are marked unsupported; no zero effect is imputed.

| age       | subgroup   | outcome        |   persons |   high_persons | status                   |   estimate |   ci_low |   ci_high |   p_holm_all_DID |
|:----------|:-----------|:---------------|----------:|---------------:|:-------------------------|-----------:|---------:|----------:|-----------------:|
| all16plus | female     | hours          |      1346 |            332 | estimated                |       1.27 |    -0.90 |      3.44 |             1.00 |
| all16plus | female     | part_intensity |      1346 |            332 | estimated                |       1.58 |    -4.05 |      7.21 |             1.00 |
| all16plus | female     | real_earnings  |      1346 |            332 | estimated                |      18.98 |  -733.92 |    771.87 |             1.00 |
| all16plus | no_BA      | hours          |      1485 |            292 | estimated                |       1.32 |    -1.24 |      3.88 |             1.00 |
| all16plus | no_BA      | part_intensity |      1485 |            292 | estimated                |       1.40 |    -4.09 |      6.89 |             1.00 |
| all16plus | no_BA      | real_earnings  |      1485 |            292 | estimated                |     137.79 |  -441.83 |    717.40 |             1.00 |
| all16plus | black      | hours          |       201 |             32 | estimated                |       1.85 |    -1.66 |      5.37 |             1.00 |
| all16plus | black      | part_intensity |       201 |             32 | estimated                |       4.67 |    -5.33 |     14.67 |             1.00 |
| all16plus | black      | real_earnings  |       201 |             32 | estimated                |    -281.10 | -2130.29 |   1568.10 |             1.00 |
| all16plus | hispanic   | hours          |       421 |             70 | estimated                |      -1.10 |    -5.02 |      2.83 |             1.00 |
| all16plus | hispanic   | part_intensity |       421 |             70 | estimated                |       3.50 |    -5.61 |     12.62 |             1.00 |
| all16plus | hispanic   | real_earnings  |       421 |             70 | estimated                |   -1101.20 | -2771.94 |    569.55 |             1.00 |
| all16plus | foreign    | hours          |       529 |             93 | estimated                |      -0.86 |    -4.14 |      2.42 |             1.00 |
| all16plus | foreign    | part_intensity |       529 |             93 | estimated                |      -0.78 |    -7.98 |      6.41 |             1.00 |
| all16plus | foreign    | real_earnings  |       529 |             93 | estimated                |   -2425.19 | -4441.83 |   -408.54 |             1.00 |
| all16plus | disabled   | hours          |       185 |             35 | estimated                |       3.26 |    -3.47 |      9.98 |             1.00 |
| all16plus | disabled   | part_intensity |       185 |             35 | estimated                |      -1.91 |   -15.28 |     11.47 |             1.00 |
| all16plus | disabled   | real_earnings  |       185 |             35 | estimated                |    -428.42 | -1723.19 |    866.36 |             1.00 |
| all16plus | low_income | hours          |       354 |             51 | estimated                |       2.16 |    -2.78 |      7.10 |             1.00 |
| all16plus | low_income | part_intensity |       354 |             51 | estimated                |       9.51 |    -0.91 |     19.92 |             1.00 |
| all16plus | low_income | real_earnings  |       354 |             51 | estimated                |     396.42 |  -309.20 |   1102.04 |             1.00 |
| age22_34  | female     | hours          |       278 |             57 | estimated                |       2.13 |    -3.24 |      7.50 |             1.00 |
| age22_34  | female     | part_intensity |       278 |             57 | estimated                |       9.33 |    -2.60 |     21.26 |             1.00 |
| age22_34  | female     | real_earnings  |       278 |             57 | estimated                |     933.65 |  -325.32 |   2192.62 |             1.00 |
| age22_34  | no_BA      | hours          |       310 |             44 | estimated                |       4.16 |    -1.58 |      9.91 |             1.00 |
| age22_34  | no_BA      | part_intensity |       310 |             44 | estimated                |       0.08 |   -11.27 |     11.43 |             1.00 |
| age22_34  | no_BA      | real_earnings  |       310 |             44 | estimated                |      77.79 | -1320.29 |   1475.88 |             1.00 |
| age22_34  | black      | hours          |        40 |              7 | unsupported_small_domain |     nan    |   nan    |    nan    |             1.00 |
| age22_34  | black      | part_intensity |        40 |              7 | unsupported_small_domain |     nan    |   nan    |    nan    |             1.00 |
| age22_34  | black      | real_earnings  |        40 |              7 | unsupported_small_domain |     nan    |   nan    |    nan    |             1.00 |
| age22_34  | hispanic   | hours          |       120 |             16 | unsupported_small_domain |     nan    |   nan    |    nan    |             1.00 |
| age22_34  | hispanic   | part_intensity |       120 |             16 | unsupported_small_domain |     nan    |   nan    |    nan    |             1.00 |
| age22_34  | hispanic   | real_earnings  |       120 |             16 | unsupported_small_domain |     nan    |   nan    |    nan    |             1.00 |
| age22_34  | foreign    | hours          |        94 |             16 | unsupported_small_domain |     nan    |   nan    |    nan    |             1.00 |
| age22_34  | foreign    | part_intensity |        94 |             16 | unsupported_small_domain |     nan    |   nan    |    nan    |             1.00 |
| age22_34  | foreign    | real_earnings  |        94 |             16 | unsupported_small_domain |     nan    |   nan    |    nan    |             1.00 |
| age22_34  | disabled   | hours          |        33 |              8 | unsupported_small_domain |     nan    |   nan    |    nan    |             1.00 |
| age22_34  | disabled   | part_intensity |        33 |              8 | unsupported_small_domain |     nan    |   nan    |    nan    |             1.00 |
| age22_34  | disabled   | real_earnings  |        33 |              8 | unsupported_small_domain |     nan    |   nan    |    nan    |             1.00 |
| age22_34  | low_income | hours          |        94 |             17 | unsupported_small_domain |     nan    |   nan    |    nan    |             1.00 |
| age22_34  | low_income | part_intensity |        94 |             17 | unsupported_small_domain |     nan    |   nan    |    nan    |             1.00 |
| age22_34  | low_income | real_earnings  |        94 |             17 | unsupported_small_domain |     nan    |   nan    |    nan    |             1.00 |
