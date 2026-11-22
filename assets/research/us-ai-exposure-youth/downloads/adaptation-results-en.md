# Worker adaptation, age and job quality after public generative AI

Updated 22 November 2026. This is an exploratory extension of the US regional AI-exposure study, not a revision of the submitted THAIE manuscript.

## Core research question

How have employment opportunities and job quality changed for labour-market entrants in highly AI-exposed fields, and how far across the age distribution do these changes extend?

The distinctive focus is workers' adaptation after potential AI shocks. The wider study covers all workers, with particular attention to young workers and dimensions of economic vulnerability. Possible paths include fewer entry opportunities, reduced hours, involuntary part-time work, unemployment, occupational reallocation, retraining and changes in contract security. Exposure does not itself establish an experienced AI shock.

## Hours-status definitions

Full-time/part-time status uses the CPS usual full-time labour-force recode PRFTLF. Economic-reason part-time uses PRWKSTAT codes 3 and 6, which include usual full-time workers temporarily working short hours for economic reasons. It can therefore overlap usual full-time status and is not a subset of the usual part-time group. An FT-to-economic-PT observation can be a temporary hours cut rather than a move into a usually part-time job.

## Main finding

The extension does not establish that AI has pushed young or disadvantaged workers from full-time into part-time work. The 22–25 occupational full-time count contrast is negative, but is sensitive to long pre-trends and multiplicity. Regional quality DID estimates are imprecise. Directly observed short-run transitions also do not show a consistent increase in movement from exposed full-time work into part-time or economic-reason part-time work. These are uncertain associations rather than evidence that harmful adjustment is absent.

## Population, exposure and design

Outcomes use the same January–September window in every year from 2010 through 2026. The main event window is 2017–2026; 2023–2026 is post and 2022 is the reference year. Ages 22–25, 26–29 and 30–34 are separate. Exploratory age groups cover 16–21, 35–44, 45–54, 55–64 and 65+, alongside all adults and ages 22–34. Non-overlapping bands partition the adult population; overlapping summary groups are never stacked as independent respondents.

Regional Q5 is the highest fixed-2019 state/DC quintile. Occupational Q5 uses fixed 2019 all-age employment-weighted cut-offs; Q1–Q4 is the comparison group. E, THAIE and TIME share common task/occupation inputs and common supported observations within each outcome and model window. Regional THAIE and TIME Q5 membership is identical, so their regional binary estimates are not independent evidence. Retrospective exposure does not measure historical adoption.

Regional DID includes state and year FE, fixed-2019 age-specific population weights, baseline industry shares interacted with year, adult COVID loss/recovery interacted with year and separate exposure departures in 2020 and 2021. Basic models are also supplied. Occupational quality-share and transition models include state×exposure-group FE and state×year FE, with group-specific industry-mix/COVID controls interacted with year. These are not the earlier industry-panel continuous-exposure regressions.

The occupational count model fits the high-versus-other count ratio within states using a conditional Binomial quasi-likelihood. Zero high or other counts can remain where the total is positive; survey-weighted counts are not assumed to be independent trials for inference. Unrestricted annual relative-count coefficients are estimated, and DID compares the average 2023–2026 log ratio with the average 2017–2019 and 2022 ratio. Group×2020/2021 departures do not identify that contrast. State-year common employment shocks cancel in the ratio, but group-specific shocks remain. Industry-share and adult-COVID controls allow differential trends associated with those baseline characteristics.

All intervals below are individual 95% state-clustered CR1 intervals. They are not full CPS survey-design intervals. Family-wise Holm corrections retain unsupported planned specifications as p=1. The two primary quality families each contain 72 comparisons; 36 direct age comparisons are separately corrected. Count comparisons use a separate 72-test family; long-count sensitivities use 54. The regional and occupational transition families have 636 and 516 planned exploratory comparisons. Pointwise event-study bands are not simultaneous bands.

## Regional quality DID

THAIE, adjusted model. Each employment measure uses the whole relevant age/subgroup state population, including non-employed people. Wage coefficients exponentiate differences in mean log real weekly wages among employed ORG wage/salary respondents.

| Age | FT / population, pp | PT / population, pp | Economic PT / population, pp | Real weekly log wages, % |
|---|---|---|---|---|
| 22–25 | -1.81 [-4.35, +0.72] | +1.14 [-1.12, +3.39] | -0.34 [-1.29, +0.60] | -0.57 [-6.30, +5.51] |
| 26–29 | -1.89 [-4.48, +0.69] | -0.51 [-1.69, +0.68] | +0.06 [-0.70, +0.82] | +2.62 [-1.71, +7.14] |
| 30–34 | -1.07 [-2.86, +0.73] | -0.06 [-1.43, +1.31] | -0.10 [-0.58, +0.38] | -2.65 [-7.68, +2.66] |

None of the 72 primary regional comparisons survives Holm correction. All adjusted THAIE intervals above include zero. There is no supported age threshold at 25, 29 or 34. Direct common-support between-age comparisons account for cross-equation state-cluster covariance; none survives the separate 36-test Holm family. Comparing significant and insignificant age-specific p-values would not be a valid age-difference test.

## Occupational full-time and part-time employment counts

THAIE, adjusted state-conditional relative count comparisons. These percentages are distinct from population-rate percentage points.

| Age | FT count gap, % | PT count gap, % | Economic PT count gap, % |
|---|---|---|---|
| 22–25 | -8.21 [-12.87, -3.30] | -2.45 [-14.59, +11.41] | -7.53 [-34.00, +29.56] |
| 26–29 | -2.79 [-7.45, +2.11] | -1.26 [-12.42, +11.33] | -7.70 [-30.07, +21.81] |
| 30–34 | -0.62 [-5.16, +4.13] | -20.89 [-30.44, -10.03] | -11.91 [-29.60, +10.22] |

For ages 22–25, the −8.21% full-time count contrast has an individual interval excluding zero but Holm p=0.101 across the 72 count comparisons. Its short 2017–2019 pre-test gives p=0.848, while the long 2010–2019 pre-test gives p=0.000726. Thus a short apparently stable baseline does not resolve the timing problem. Ages 30–34 show a sizeable negative part-time count contrast; its short pre-test also rejects at p=0.042. This is not the pattern of a universal shift into part-time work. Count comparisons and within-employment shares can move differently.

Within-employment quality shares are supplied separately. Occupational wages have much smaller support than regional wages after requiring all three exposure measures and both high/other groups. Six primary adjusted occupational wage specifications for ages 22–25 and 26–29 are not estimable because the fully controlled models saturate the supported cells. They are marked as unsupported rather than zero effects. The basic models and the age 30–34 estimate remain in the output, with their coverage. No simplified alternative was substituted silently.

## Observed worker transitions

We additionally matched adjacent CPS observations, using January–February through August–September pairs each year. This is a post-plan exploratory addition made after examining the cross-sectional quality estimates. Original household/person identifiers remain in memory only and are not exported. Links must satisfy identifier uniqueness, month-in-sample progression, stable sex/race/state and age progression of zero or one year. Origin ages define cohorts; a worker does not change age band halfway through a transition. Occupational exposure is assigned at origin; the destination can be any occupation.

The following THAIE estimates compare observed transition rates for workers originating in occupational Q5 versus Q1–Q4. They condition on matched full-time origins, not all young people or all job seekers.

| Age | FT → PT, pp | FT → economic PT, pp | FT → unemployment, pp |
|---|---|---|---|
| 22–25 | +0.20 [-1.35, +1.75] | +0.44 [-0.45, +1.34] | +0.33 [-0.70, +1.35] |
| 26–29 | -0.29 [-1.16, +0.58] | -0.01 [-0.58, +0.55] | +0.08 [-0.47, +0.63] |
| 30–34 | -0.26 [-0.81, +0.28] | +0.15 [-0.14, +0.44] | +0.18 [-0.11, +0.48] |

All listed intervals include zero. THAIE occupational transition support covers 32, 44 and 50 states for the three respective age groups under the main FT-origin specification. Common-support requirements are shared by all three metrics. Smaller subgroups and PT-origin cells are often unsupported; 150 of 516 planned occupational transition models are not estimable. Of 636 regional transition models, 15 are unsupported. Unsupported models remain visible in the tables and multiplicity denominators.

Regional transition estimates and long-window checks are also saved. The national unweighted validation rate among rotation-eligible person-pairs falls from about 94.8% in 2010 to 90.0% in 2026. Origin cross-sectional weights are used without a validated attrition adjustment. This is not the full IPUMS holistic CPSIDV algorithm or an official stock-reconciled gross-flow estimator. Age masking, migration, nonresponse, sample redesign and disclosure revisions can affect linkage. The results cannot establish whether a move was forced or caused by AI.

## All ages and unequal adaptation

The analysis separately covers all adults and each age band. Five overlapping dimensions are explored for both all adults and ages 22–34, no bachelor's degree, female, Black alone, Hispanic and foreign-born. They are not equivalent categories of disadvantage or treatments. Current low wages are not used to select a post-shock low-income group. Disability, caregiving, pre-shock wealth and employer benefits need a richer longitudinal baseline and are not claimed to be measured here.

The young subgroup regional estimates do not show a uniform increase in part-time or involuntary part-time work. Black 22–34-year-olds have a relatively negative THAIE full-time point estimate, but its interval includes zero. A negative or positive estimate for one subgroup does not demonstrate a difference from another subgroup without a direct contrast. Some long-window occupational involuntary-part-time share specifications survive the broad exploratory correction; they remain timing-sensitive, conditional-on-employment findings rather than proof of forced individual downgrading. All 960 exploratory quality comparisons, including unsupported ones, are retained.

## Earnings and contract-security qualifications

Real weekly earnings use CPI-U and a September 2026 reference. ORG wage cells below 30 valid person-months are withheld; historical occupational conversions can contribute fractional mapped person-month support. These are repeated employed samples, not the same workers' wage changes. Hours, occupation and worker selection can alter weekly earnings. Public-file rounding/topcoding changes phased in during 2023–2024 are not fully harmonised in this extension, so the wage estimates require additional sensitivity before strong interpretation. [Census disclosure note](https://www.census.gov/programs-surveys/cps/technical-documentation/user-notes/cps_2023_01.html).

Full-time/part-time is independent of permanent/contingent classification. Basic monthly CPS does not provide the complete contract-security axis. The project therefore does not claim to have estimated permanent-to-contract transitions. The separate source assessment identifies linked CPS, SIPP, intermittent contingent-work supplements, public and restricted LEHD, state records and training histories as complementary routes. In SIPP, EJB*_CNTRC labels refer to union coverage, not fixed-term contracts; that variable must not be repurposed.

## Verification and remaining identification limits

All new age-22–25 aggregate population, employment, unemployment, full-time, part-time and involuntary-part-time totals reconcile to the previous independent aggregates within 1.2×10⁻⁸. The adult age partition and linked transition accounting identities pass. Independent explicit-dummy WLS checks cover regional full-time, regional unbalanced wages and occupational quality shares; explicit Binomial GLM independently checks the count model, including state-cluster covariance. Known CPS identifier corrections, sample redesign and earnings disclosure changes are documented in the source assessment. Observed-link sample losses are outcomes worth monitoring, not negligible by assumption.

The analyses do not observe actual firm adoption, do not directly control teleworkability, and do not remove all occupation-specific demand, education or demographic shocks. Post-event changes are not automatically AI effects. Neither a statistical null nor an unsupported small-cell model rules out economically meaningful harm. The contribution is a transparent comparison of quantities, quality and observed short-run adjustment under the same exposure definitions, with explicit measurement and identification boundaries.

## Materials

- [Six-page English figure collection](worker-adaptation-results-en.pdf)
- [All planned quality DID results](adaptation-did-results.csv)
- [Quality event studies](adaptation-event-studies.csv) and [pretrend tests](adaptation-pretrend-tests.csv)
- [Occupational count DID](adaptation-occupation-count-did.csv), [count events](adaptation-occupation-count-events.csv) and [long count events](adaptation-occupation-count-long-events.csv)
- [Direct between-age comparisons](adaptation-direct-age-contrasts.csv)
- [Observed occupational transition DID](adaptation-occupation-transition-did.csv), [events](adaptation-occupation-transition-events.csv) and [pretrends](adaptation-occupation-transition-pretrends.csv)
- [Observed regional transition DID](adaptation-transition-did.csv) and [linkage support](adaptation-national-linkage-support.csv)
- [All-age results](adaptation-all-age-results.csv) and [demographic results](adaptation-demographic-results.csv)
- [Worker-transition data feasibility assessment](adaptation-transition-data-en.md) and [source matrix](adaptation-transition-data-sources.csv)
- [Numerical validation](adaptation-validation.json)


The 18 January–September files from 2024–2025 and January 2026 were re-downloaded for hash verification against the current official release. All 19 match the cached analytical inputs. This checks the relevant identifier and weight revision vintages without claiming that attrition or disclosure effects have been eliminated. [Census revision notes](https://www.census.gov/programs-surveys/cps/data/datasets/cps-basic-footnotes.html).
