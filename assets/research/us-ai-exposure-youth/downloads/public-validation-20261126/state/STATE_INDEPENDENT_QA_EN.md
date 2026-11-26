# Independent critical QA of the pooled-state CPS module

Reviewed November 26, 2026. This was a read-only review of build_pooled.py, validate_and_compare.py and STATE_POOLING_METHODS_EN.md. A limited additional review covered ACS process.py, summarize.py and salary-mean pooling. No plots were rendered and no production code was changed by this reviewer.

## Overall judgment

No substantive arithmetic error was found in the fractional exposure allocation, population denominator, ratio linearization, relative-change gradient or Holm calculation. Their interpretation is appropriate only as repeated-cross-sectional, unadjusted descriptive estimates with working household-cluster uncertainty. They do not supply official CPS design inference, an AI causal estimate or validated longitudinal worker histories.

## Verified calculations

1. Pre-2020 bridge probabilities are summed by THAIE band before multiplying individual employment contributions. This retains one person row and leaves the population denominator intact. Unmapped probability contributes to neither mapped employment numerator. The bridge row-sum assertion is appropriate. Expected band allocations are not observed detailed occupations, and their uncertainty is not included.
2. The parser restricts records to civilian noninstitutional people and the state module then restricts age to 22–25. Population P includes unemployed and nonparticipants. Q5 FT/P is therefore the share of all same-age residents employed full-time in Q5 occupations. It is not employment conditional on belonging to a population of Q5 workers. The same-band employed denominator yields an employment-composition share, as the report correctly states.
3. Pooling sum(numerator)/sum(population) estimates a population-weighted period ratio. It is not the arithmetic mean of monthly rates. Dividing both totals by the same observed-month count leaves that ratio unchanged. Missing October 2025 is omitted, not treated as zero.
4. The ratio influence contribution x−r*w, summed within household and divided by the total denominator, is the correct first-order gradient for the stated working independent-household model. The K/(K−1) factor is a conventional working cluster adjustment.
5. For L=log(Q5 post/Q1–4 post)−log(Q5 pre/Q1–4 pre), the code's signed household scores are correct. Shared IDs on both sides retain working covariance. On actual pooled national FT totals, an independent finite-difference check gave log-total elasticities [−1.00000000003,+1.00000000004,+1.00000000003,−1.00000000003], agreeing with [−1,+1,+1,−1].
6. The revised manual step-down Holm adjustment agrees with statsmodels multipletests after padding unestimable comparisons with p=1 in the planned nine national and 459 state tests. Separate national and state descriptive families are disclosed; this is not a claim of a preregistered confirmatory family.

Numerical evidence is stored in STATE_QA_NUMERICAL_CHECKS.json.

## Confirmed issue addressed during review

The initial ratio implementation could produce a zero-width uncertainty interval for a zero observed numerator, creating false precision in rare economic-short-hours cells. The revised source now retains the point estimate but withholds SEs and intervals when fewer than five contributing records, nonfinite SE, or zero SE occurs, with an explicit status. Output regeneration is the responsibility of the root workflow. Five records are an engineering minimum screen, not evidence that a cell has adequate precision or a Census-endorsed sufficiency threshold.

## Remaining limitations and safeguards

- Household IDs are working dependence groups. Combining state, HRHHID and HRHHID2 does not validate person matches, prevent every long-horizon ID-reuse issue or reconstruct household strata/PSUs. Person-key counts must remain labeled IDs, not distinct workers.
- The working intervals omit occupation-level common shocks. The relatively small national household-based p-value must not replace occupation-clustered uncertainty in the controlled research models. Administrative measurement uncertainty, crosswalk uncertainty and exposure-score uncertainty are also not represented.
- The 36-calendar-month postperiod contains 35 observed months. Normalization cancels in Q5/Q1–4 ratios, but the missing seasonal composition does not cancel mechanically if groups have different seasonality. These descriptive contrasts do not control that issue. They should retain the explicit observed-month warning.
- Historical contributing-record counts can include fractional allocations to more than one band. They are not mutually exclusive observed occupation classifications or effective sample sizes. Do not compare such counts to direct post-2020 classifications without the bridge caveat.
- The table field all_age_population refers to all eligible 22–25-year-olds, not all ages in the U.S. The report currently explains this correctly. Public-facing labels should say all residents aged 22–25.
- Intervals are marginal, not simultaneous. Many state comparisons share overlapping periods and households. Holm controls its declared families under arbitrary dependence, but it does not remove exploratory specification search or establish cross-state heterogeneity.
- PT_econ uses PRWKSTAT 3/6 and can include usual full-time workers with short actual hours. The methods document correctly disclaims usual involuntary part-time employment. FT/PT does not identify permanent versus temporary contracts.

## Engineering finding

The previously identified cache-integrity gap has been repaired. The revised source now verifies pipeline, dictionary and cached parquet hashes before reuse. This reviewer independently hashed all 117 cached parquet files and matched their provenance. The downstream validator also compares Q1–Q4 FT/PT to the previous aggregates, retains raw PRFTLF/PRWKSTAT and checks record-level FT and economic-short-hours definitions. Its updated 117-month fresh smoke check passed. No residual cache-byte integrity gap was found. Cached reuse and fresh raw parsing should still be described distinctly when documenting a particular execution.

## Limited ACS cross-check

The ACS annual mean is computed as a weighted salary numerator divided by the corresponding weighted denominator, and replicate versions recompute that ratio. The SDR factor 4/80 is correctly applied around the full-sample estimate. The two-endpoint comparison perturbs coordinated Q5/Q1–4 replicates within each year and combines year blocks under an explicitly independent-year approximation. The pooled salary mean correctly uses the ratio of annual-average numerators and denominators rather than averaging medians or unweighted annual means.

The income universe remains current employed wage/salary workers with positive past-year salary. Annual earnings need not have been earned in the currently reported occupation, and differences reflect hours, weeks, selection and composition as well as pay. ADJINC and annual CPI scaling do not convert this into an hourly wage or the pay of every worker. These limits must accompany interpretation. Signed-replicate quantiles and zero-SDR cases are withheld rather than represented as spuriously exact estimates, which is a conservative guardrail.

## Publication recommendation

The state descriptive estimates can be shown with their population denominator, observed-month coverage and working-uncertainty labels. Preserve the distinction between these descriptive contrasts and controlled occupational DID. Do not use the pooled-state significance to restore a causal youth-displacement claim or to assert individual full-time-to-part-time transitions.

## Final repair verification

Rare relative contrasts now also withhold uncertainty when any contributing numerator has fewer than five records. Comparisons with an observed zero denominator/numerator needed for a log ratio are not emitted as finite log effects. Unestimable tests remain counted in the planned Holm families through virtual p=1 values. The revised numerical QA JSON records the estimable and virtual-test counts. This prevents reduced multiplicity correction from silently benefiting sparse or unestimable comparisons. No production code was edited by this reviewer.
