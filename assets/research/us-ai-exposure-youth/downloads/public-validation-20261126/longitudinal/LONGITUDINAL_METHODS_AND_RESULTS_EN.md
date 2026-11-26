# Corrected longitudinal analysis of worker adaptation

Built November 26, 2026 from official CPS and SIPP public-use records and free official longitudinal weights. Outputs are descriptive risk-set estimates. No plots were displayed, and no website or manuscript was changed.

## CPS linkage

Fresh parsing of the available January 2020–October 2026 files yields 79 genuine adjacent-calendar-month pairs. Cross-year pairs are retained. October 2025 was not collected, so no transition into or out of that month is imputed. The earlier attrition script used only February–September within each year and therefore omitted many available pairs.

Origin eligibility requires MIS 1, 2, 3, 5, 6, or 7. Links require unique household/person identifiers, the expected next MIS, stable recorded sex, race and state, and age progression of zero or one year. Unemployed and NILF respondents remain in linkage and response estimation rather than being removed before matching. Exposure is assigned using the origin occupation and frozen THAIE membership. Destination occupation is never used to classify origin exposure. Age is fixed at each transition's origin, not over the entire six-year span.

Response probabilities use two household-disjoint folds within each destination year. Predictors include state, requested age band, sex, education, race, Hispanic origin, initial labor-force status, rotation group, calendar month, broad industry and origin exposure. All 14 logistic fits converged in five Newton iterations. Probabilities are clipped to .05–.995. Output tables compare original weights, response IPW, and a sensitivity trimming inverse-probability factors at their 99th percentile. Monthly weighted retention ranges from 86.34% to 93.00%. The 2025 range is 87.11%–90.34%, and the January–October 2026 observed-pair range is 87.61%–90.54%. For ages 22–25 in Q5, the original-weight FT→PT rate is 3.644% before and 3.625% after the transition, compared with IPW rates of 3.669% and 3.645%. Trimming gives 3.66865% and 3.64446%; the trimming sensitivity is below .001 percentage point. Stability to this trimming choice does not validate the response model. Calibration to initial margins was not implemented in this rebuild; IPW is not an official longitudinal CPS weight. Response-on-observables, correct predictor specification and adequate overlap remain assumptions. These adjustments cannot automatically recover movers or selection on unobserved variables.

FT and PT require employment and PRFTLF 1 or 2. The economic-PT transition additionally requires destination usual PT. A separate economic-short-hours outcome uses PRWKSTAT 3/6 and includes people who remain usual FT. These outcomes must not be treated as interchangeable. Employee-to-self-employment is a class-of-worker change, not a permanent-to-contract transition.

Pre-transition pairs end by October 2022. Post-transition pairs begin in December 2022. Pairs involving November 2022 are excluded from the pre/post readout. The pre-period includes the pandemic, and these pooled periods have different durations and composition. Their differences are not controlled DID estimates or evidence of an AI effect. Monthly retention and annual transition tables permit later calendar and composition adjustments.

Risk counts are person-transition opportunities, not independent people or national employment counts. A respondent may contribute several opportunities. Annual unique-person counts must not be added and called unique people across all years. No confidence intervals or significance tests are claimed for these new descriptive tables. Repeated respondents, sample design, occupational dependence and uncertainty from estimating response propensities require further variance estimation. Entry-flow exposure is not fabricated for respondents without a valid prior occupation.

## SIPP shorter cohorts

The 2025 release provides official longitudinal weights for two-, three- and four-year groups. These correspond to reference years 2023–2024, 2022–2024 and 2021–2024. Joining SSUID, PNUM and SPANEL matches 18,207, 10,717 and 6,122 people, respectively. Exposure uses each person's hours-dominant positive-hours occupation during January–October of the first reference year. Transition risk sets begin after that October, and age and vulnerability are fixed in that month. Baseline October must be in universe with valid monthly employment status. The no-BA subgroup requires valid education codes 31–42, excluding negative or missing codes.

Mapped baseline workers number 8,594, 5,024 and 2,847. The respective 22–25 counts are 534, 304 and 164. These counts use different baseline years and cannot be interpreted as a direct attrition comparison. The two-year cohort begins after ChatGPT and cannot identify a pre-AI effect. Small age-by-exposure-by-vulnerability groups are explicitly flagged when fewer than five events are observed.

Monthly employment uses RMESR 1–5. Hours sum valid TJB job-specific average weekly hours for the reference month. Employed records with every job-hours field missing remain unknown, not zero. Outcome-specific risk sets exclude unknown destination hours or arrangements rather than counting them as no event. Nonemployment remains a valid competing outcome. The main arrangement requires a positive-hours job, preventing inactive historical job slots from being classified as current contracts.

A full-to-part intensity transition means at least 35 monthly-average weekly hours followed by 0–<35 while employed. This is not identical to usual FT/PT. A stricter sensitivity requires RMESR 1 at both endpoints, meaning work in all weeks, and the same persistent JOBID. This reduces partial-month and unpaid-absence confounding. Exact alignment of hours stages and intra-month change dates was not completed, so no usual-hours transition is claimed from the staged JOBHRS variables. General contract-duration transitions are not estimated because JBORSE, CONCHK and CNTRC do not identify permanent versus fixed-term employment.

Person-year outcome means include hours, employment, real monthly earnings and total personal income, weighted by the relevant official cohort weight. Dollar amounts use December 2024 CPI-U. Variable-specific missing codes are removed. TPEARN uses −100000998 and TPTOTINC uses −10000000999. Legitimate business losses remain. Earnings and total income are not pure hourly wages. Annual outcomes include observed nonemployment, while missing monetary values remain missing. Baseline-year outcome averages include the exposure-construction months and are descriptive levels.

No replicate-weight variance or causal DID was computed for the new two- or three-year cohort tables. A separate four-year-only file reports marginal rates for all ages and ages 22–25 using the matching 240 official Fay BRR replicates and variance factor 4/240. Its full-sample replicate differs from FINYR4 by at most 0.00001 because of released-file numeric precision. Inference uses REPWGT0 as the full-sample weight and matches its 240 replicates. These intervals condition on fixed baseline exposure, suppress intervals for domains with fewer than 20 origin people or five events, and are not AI-effect estimates. Zero observed events do not imply zero population risk; degenerate zero-variance replicate results are retained only as raw diagnostics, not presented as precise zero confidence intervals. The factor follows the 2025 SIPP Source and Accuracy Statement, variance-estimation section, using 240 replicates and Fay rho=.5. Four-year replicate inference is never attached to two- or three-year cohorts. Complete 2026 SIPP worker histories are unavailable in these files.

## Output scope

`cps_pair_audit.csv` and yearly retention tables document matching and response. `cps_transition_rates_by_year.csv` and `cps_transition_rates_pooled.csv` include all ages and women, no-BA, Black and Hispanic domains. `sipp_cohort_transition_rates.csv` separates general monthly intensity from the same-job, full-month sensitivity. `sipp_person_year_outcomes.csv` contains within-cohort outcome levels. `sipp_4yr_transition_replicate_intervals.csv` contains the separate four-year marginal-rate intervals. Source manifests and validation JSON files document weights and consistency checks. Individual records remain in the local work directory; deliverable tables contain aggregates only.

## Youth CPS descriptive readout

The following rates use cross-fitted response IPW. Exposure bands have different risk populations. Neither levels nor their pre/post differences establish an AI effect.

```csv
band,period,transition,risk_pairs,event_pairs,rate_pct
Q1–Q4,post,FT_to_NILF,54548,1431,2.894374903971426
Q1–Q4,post,FT_to_PT,54548,3017,5.813563583634267
Q1–Q4,post,FT_to_U,54548,609,1.1204228462478518
Q1–Q4,post,FT_to_economic_PT,54548,623,1.248308242730567
Q1–Q4,post,FT_to_economic_short_hours,54548,1213,2.403934431343582
Q1–Q4,pre,FT_to_NILF,41630,1242,3.247872120629685
Q1–Q4,pre,FT_to_PT,41630,2298,5.735533227440344
Q1–Q4,pre,FT_to_U,41630,826,2.202670823105186
Q1–Q4,pre,FT_to_economic_PT,41630,516,1.4361923808666224
Q1–Q4,pre,FT_to_economic_short_hours,41630,1146,3.0619375882940645
Q5,post,FT_to_NILF,12995,278,2.312059055460256
Q5,post,FT_to_PT,12995,455,3.644532200534124
Q5,post,FT_to_U,12995,113,0.7925854959010143
Q5,post,FT_to_economic_PT,12995,82,0.7018777713306411
Q5,post,FT_to_economic_short_hours,12995,142,1.182703774614572
Q5,pre,FT_to_NILF,10840,256,2.4995443656633536
Q5,pre,FT_to_PT,10840,386,3.6690484070368417
Q5,pre,FT_to_U,10840,152,1.5113875338779956
Q5,pre,FT_to_economic_PT,10840,69,0.7051604459519176
Q5,pre,FT_to_economic_short_hours,10840,152,1.574247917678724
```

# Entry opportunities as destination outcomes

This extension separates labor-market entry from changes among incumbent workers. It uses the same observed linked CPS respondents and identical response weights as the adaptation analysis. Individual response probabilities were not retained by the first run; they were recovered by replaying the identical deterministic cross-fitting specification and saved locally. An unchanged SHA-256 hash of the original pooled transition table verifies that the replay did not change those results. Destination occupation was not added to the response model.

The risk set contains respondents who were unemployed or outside the labor force in the origin month. Outcomes are entry into Q5 full-time, Q1–Q4 full-time, Q5 part-time, Q1–Q4 part-time, or unmapped employment in the destination month. All five outcomes share the same origin-jobless denominator within each reported age, origin status, period and weighting method. Their sum equals entry into any employment. Destination THAIE therefore classifies the outcome; it is not assigned treatment status for nonworkers. This avoids treating an unobserved prior occupation as low exposure.

The primary age groups are all ages 16+ and ages 22–25 at the origin. Respondents who turn 26 before the destination interview are retained. Tables also distinguish unemployed and NILF origins, and provide separate strata for assigned versus unassigned origin occupation. The latter is a data-availability distinction, not evidence of first-job status. The available records do not establish that a particular transition is a person's first-ever job or a post-graduation entry.

True adjacent months and the same transition exclusion around November 2022 are maintained. The output includes destination-year and pooled pre/post rates, with original weights, response IPW and inverse-factor trimming. Simple post-minus-pre differences and differences between the Q5 and Q1–Q4 changes are labelled unadjusted descriptive contrasts. They are not controlled DID estimates. The exposure bands differ in their size and occupational composition; a smaller entry rate into Q5 cannot by itself establish restricted opportunity. COVID recovery, student enrollment, demand composition, demographic changes and destination occupation coding remain possible explanations. No p-values or causal conclusions are attached to this extension.

Files are `cps_entry_rates_by_year.csv`, `cps_entry_rates_pooled.csv`, `cps_entry_unadjusted_changes.csv` and `cps_entry_validation.json`. Risk counts are repeated transition opportunities, not independent people. Missing October 2025 remains unobserved, with no individual imputation. Individual identifiers and response weights remain in the work directory only.

```csv
period,outcome,risk_pairs,event_pairs,rate_pct
post,Q1–Q4_FT,31167,1990,6.200793434174648
post,Q1–Q4_PT,31167,1602,5.18665518114633
post,Q5_FT,31167,409,1.3140645824757355
post,Q5_PT,31167,265,0.8706906561616339
post,any_employment,31167,4348,13.829805476732195
post,unmapped_employment,31167,82,0.2576016227738511
pre,Q1–Q4_FT,27503,2039,7.3342183224543
pre,Q1–Q4_PT,27503,1405,5.202857223820939
pre,Q5_FT,27503,451,1.7264053349667832
pre,Q5_PT,27503,248,0.8873691406877523
pre,any_employment,27503,4219,15.436171645147985
pre,unmapped_employment,27503,76,0.2853216232182098
```
