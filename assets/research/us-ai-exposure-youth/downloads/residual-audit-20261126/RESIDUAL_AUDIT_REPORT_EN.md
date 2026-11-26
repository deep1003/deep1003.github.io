# Auditing the CPS survey reconciliation and the robustness of relative employment weakness

## Main findings

The large survey reconciliation is a difference between sizable endpoint-coverage and weighting terms, not a measured economic outflow. Scheduled rotation replacement supplies the largest negative accounting contribution, while eligible-but-unlinked endpoints supply a large positive offset. Reweighting corrections and observed CPS weight changes add further offsets. Occupational code-system changes were already excluded from the residual and remain a separate behavioral-classification bookkeeping term.

Long-window Q5/Q1–Q4 full-time employment weakness remains about 9% after rotation standardization, restriction to unambiguous historical occupational-code components, and a single-code-era reference period. However, a shorter, genuinely matched 22-month comparison yields −4.23% with an interval spanning zero. Thus the direction is consistent but statistical resolution is not robust to every period choice.

No individual flow pathway is statistically resolved by these conditional diagnostics, including after an endpoint-calibration diagnostic almost eliminates the national residual. Eliminating a residual by forcing endpoint margins to match does not identify missing transitions or validate an AI mechanism.

## Data and scope

We reuse the verified, hashed monthly CPS caches and frozen THAIE mapping. The target is civilian noninstitutional adults aged 22–25. Full-time employment is PEMLR 1/2 and PRFTLF 1 at each endpoint and in the stocks. Linkage uses an origin-age-21–26 domain to capture aging boundaries, unique household/person keys, rotation progression, stable recorded sex/race/state, and age progression of zero or one year. There are 115 actual adjacent-month pairs and 538,185 linked person-transition observations; repeated observations are not distinct people. The missing October 2025 is not imputed, and September–November 2025 is not linked as an individual transition.

The primary stock comparison is January 2019–October 2022 versus January 2023–October 2026, excluding October and November 2025 from the latter because adjacent flows are unavailable. The first window has 46 and the latter 44 observed target months. All changes below concern headcounts or flow intensities, not employment-to-population rates or causal AI effects. The ACS-calendar sensitivity is retained in the downloadable residual-attribution table.

## Exact residual identity

Let `B` denote target-age, full-time, exposure-group membership. Let `M` be valid matched persons and `U0,U1` unmatched endpoint records. Let `P0,P1` be the original CPS weights and `w` a common adjusted origin-based weight. Then the repeated-cross-section stock change satisfies

`ΔS = ΣM w(B1−B0) + ΣM(P1−P0)B1 + Rrotation + Runlinked + ΣM(P0−w)(B1−B0)`.

`Rrotation` is destination MIS 1/5 stock minus origin MIS 4/8 stock. `Runlinked` is the remaining unmatched destination stock minus unmatched origin stock among the scheduled overlap. These categories are exclusive. The last term is split into the planned six-of-eight rotation expansion and the additional response adjustment. The original matched weight-change term is a raw accounting convention, not the causal effect of changing survey weights. The combined reconciliation equals all terms after the weighted behavioral flow. This identity is checked by state, month, exposure group and weight method against the prior output.

The terms are integrated with the exact same period-mean telescoping coefficients and log-mean denominators as the previous decomposition.

| Accounting component | Additive log points |
| --- | --- |
| Scheduled rotation replacement | -34.369 |
| Eligible but unlinked endpoints | +19.693 |
| Planned rotation expansion correction | -2.512 |
| Additional inverse-response correction | -3.693 |
| Observed matched-weight change | -1.722 |
| Combined reconciliation | -22.604 |

These additive log-point contributions sum to the previously reported combined survey reconciliation. They are not percentages of a causal effect or additive employment-change percentages. Scheduled rotation is random by design, but realized weighted group stocks differ between outgoing and incoming panels. Large signed terms can accumulate across many months and offset. Treating the −34.37 rotation contribution alone as the share of employment weakness explained by rotation would be misleading. The separately recorded January 2020 occupation-classification boundary contributes +0.840 log points to the primary overall employment accounting; it is not included in this residual total.

## Why coverage terms are large

The planned nonoverlap changes roughly one quarter of the interview sample each month. Across these pairs, Q5 origin scheduled-rotation full-time stock averages approximately 482,500 and incoming stock 472,319. Eligible-but-unlinked origin and destination Q5 stocks average approximately 178,915 and 198,868. These are repeated monthly weighted stocks, not unique workers, observed hiring, or job separations. The corresponding control-group stocks are much larger. Taking differences between such quantities creates sizable noise relative to the net stock change.

The linkage audit identifies 616,549 eligible origin records. Of these, 538,185 validate, 72,118 have no destination key, 4,780 fail the age-progression rule, 840 fail stable recorded race, and 626 fail stable recorded sex, under an ordered rejection hierarchy. A missing key does not tell us whether the cause is nonresponse, moving, household replacement, or another coverage issue. Invalid matches are not accepted merely to reduce the residual, and unmatched respondents are not coded as nonemployment. These records cannot reveal their unobserved job transitions without assumptions.

## Non-tautological stock sensitivities

| Sensitivity | Pre/post months | Relative change | Conditional 95% interval |
| --- | --- | --- | --- |
| Original full CPS stock | 46/44 | -9.31% | [-13.88, -5.34] |
| Equal rotation-group mix | 46/44 | -9.31% | [-13.69, -5.43] |
| Unambiguous code components | 46/44 | -9.02% | [-13.61, -4.77] |
| Single code era, 2020 start | 34/44 | -9.15% | [-13.33, -5.15] |
| Single code era, matched 22 months | 22/22 | -4.23% | [-10.91, +1.53] |

Equal rotation mix standardizes each month's eight MIS-specific weighted occupational full-time shares to equal rotation-group weights, preserving the same-age population total. It directly checks whether changing rotation composition drives the long-window stock contrast; its result is virtually identical to the original estimate. It cannot remove all rotation-group response or classification errors.

The unambiguous-code restriction builds connected components of the 2010→2018 occupation crosswalk. A component is retained only when every linked new-code occupation has the same mapped Q5-versus-Q1–Q4 status and none is unmapped. This avoids fabricated individual old-code assignments or selectively treating fractional records as known identities. It changes the supported occupation universe, so its estimate is a robustness contrast rather than the identical population estimand. The negative result persists. The single-code-era comparisons additionally avoid the historical bridge altogether. The shorter 22-month comparison is substantially weaker and imprecise; pandemic recovery, endpoint selection and sampling precision remain material limitations.

## Reducing the residual without claiming to observe missing behavior

Origin-only entropy calibration reduces Q5's national mean absolute monthly combined reconciliation from 60,914 to 57,990 persons, about 4.8%. For Q1–Q4 it falls from 122,763 to 118,540. Thus observed-response adjustment improves reconciliation only modestly; it does not repair all missing outcomes or panel coverage.

We also construct an explicitly constrained diagnostic. Starting with origin-calibrated weights, positive entropy calibration matches the original origin state/population/status margins and national destination Q5/Q1–Q4 FT/PT margins. The new relative calibration multipliers range from 0.506 to 1.886. The maximum normalized margin discrepancy is 1.55e-10. National combined full-time reconciliation then falls below 0.0014 persons per pair/group.

This near-zero residual is guaranteed by matching both endpoint stock margins. It is not an independent successful recovery of missing transitions. It does not prove ignorability, identify movers, validate occupation histories, or create new observations. Raw cross-sectional stocks remain unchanged by this flow-weight diagnostic, so their unchanged relative change is also guaranteed. We use it only to ask whether an allocation consistent with both sets of observed margins leads to a newly resolved mechanism.

## Do pathway conclusions change?

Flow intensities use signed weighted transitions per 100 origin full-time workers, with equal weight for each calendar month. They are replenishment/depletion intensities, not probabilities among the nonemployed or verified first-job hiring rates. Positive entries add to the stock; exits are signed negatively. The reported contrast is the Q5 post-minus-pre change minus the Q1–Q4 post-minus-pre change.

| Pathway | IPW contrast, pp | Dual-endpoint contrast, pp | Dual conditional 95% interval |
| --- | --- | --- | --- |
| Nonemployment entry | +0.097 | +0.125 | [-0.361, +0.713] |
| Nonemployment exit | -0.379 | -0.314 | [-0.881, +0.308] |
| Full-/part-time balance | +0.059 | +0.284 | [-0.544, +1.127] |
| Recorded occupation balance | -0.092 | -0.050 | [-1.004, +0.901] |
| Age-boundary balance | -0.175 | -0.170 | [-0.759, +0.503] |

Every pathway interval spans zero under primary IPW, origin-only calibration, the dual-endpoint diagnostic, and symmetric common weights based on the average endpoint CPS weights. This also holds for the tested single-code-era and matched-22-month flow comparisons. The large residual therefore does not conceal a mechanism that becomes statistically resolved by these tested adjustments. This is not proof that all mechanisms are zero or absent. Wide intervals allow substantively important effects, and the constrained calibration cannot establish the true distribution of unobserved transitions.

## Statistical and causal limits

Intervals use 999 common state-resampling draws, with 51 states including DC. They condition on fitted propensity weights, fixed mapping, and the fitted calibration, rather than refitting those stages in each draw. They do not recover official CPS survey strata/PSUs, all occupation-level common shocks, bridge uncertainty, or nonignorable selection. They are working diagnostics, not publication-grade causal inference or a multiplicity-adjusted set of confirmatory tests. The stock and flow tests use independent fixed bootstrap seeds, so working interval endpoints may differ slightly from the prior report.

These diagnostics do not replace the previously estimated controlled entry DID. Equal calendar-month weighting addresses seasonal composition, not differential COVID recovery or industry-specific demand shocks. A shorter comparison changes both the period and precision. The occupation-code audit addresses known crosswalk ambiguity and the January 2020 boundary, not every occupation misreporting or dependent-interviewing error. Geographic mobility is incompletely observed because valid links require stable state. Forced margin agreement should never be presented as evidence of AI-caused displacement.

## Defensible conclusion

Within the long-window comparisons, young Q5 full-time employment remains weaker relative to Q1–Q4 after rotation and occupation-code checks. The finding is sensitive in magnitude and statistical resolution to the comparison period. No specific entry, exit, schedule-switch, occupational-movement, or aging pathway is established by the available linked CPS, even under tested residual-reduction adjustments. The evidence supports relative employment weakness with an unresolved mechanism; it does not establish AI causation or a contract-quality deterioration.

## Reproduction

- `audit.py` verifies hashed caches, constructs the exact coverage/weight residual identity, audits link rejection, and fits the constrained dual-margin diagnostic.
- `summarize.py` integrates the residual terms and estimates rotation/code/period stock sensitivities.
- `flows.py` compares flow pathways across weighting and reference-period alternatives.
- `report.py` checks agreement with the prior accounting and writes saved figures without image emission during smoke checks.

Only aggregate outputs should be shared. The private matched-record cache is excluded from the materials bundle. Existing website and manuscript files are not modified by this audit.
