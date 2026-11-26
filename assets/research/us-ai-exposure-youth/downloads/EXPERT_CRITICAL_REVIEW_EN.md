# Critical specialist audit of the CPS–THAIE employment analysis

## Overall assessment

Share with explicit methodological caveats. Three separate AI specialist agents reviewed statistical design and implementation, data processing, and presentation. The coordinating agent checked evidence, repaired confirmed defects, and commissioned additional refits. This is an internal computational audit, not external peer review. The scope is the current national monthly CPS occupational THAIE analysis and its active web presentation. Earlier SIPP, linked-CPS transitions, state-level panels, productivity and job-posting projects have not been revalidated by this audit.

No demonstrated arithmetic error changed the current primary coefficient. The prior claim of a robust AI-caused youth full-time employment decline is not supported. Pipeline reproducibility and presentation required repairs. Additional robustness tests strengthen the uncertainty rather than rescue significance.

## Confirmed defects and repairs

| Component | Finding | Repair and validation |
|---|---|---|
| Model caches | Reuse depended on filename existence | Require input, prepared sample, design, backend, code and environment fingerprints. Forty historical models were retrospectively attested against the preserved original archive. An intentionally changed signature fails. |
| Preparation caches | Raw or mapping changes could leave stale intermediates | Bind raw files, dictionaries, parser, preparation code, scores, crosswalk and product hashes. Legacy caches rebuild on future preparation. Temporary-file invalidation tests passed. |
| Input audit | Missing-month flag was hardcoded; frozen labels were not reconstructed | Explicit absence/nonnegative/mapping checks, five-month all-age regeneration and reconstructed 2019 weights and cutpoints. |
| Numerical validation | Only harmonized standard errors were disclosed | Publish raw and harmonized errors, exact FE rank 446 versus absorbed degrees 449. The adjustment factor is 1.000892; coefficient agreement is 4.72e−15. |
| Detailed Methods | Stale annual normalization, old analysis span and event reference | Align with November 2022 baseline, current symmetric windows, support and August–October 2022 reference. |
| Chart exports | Missing/suppressed measurements labeled observed | Export unavailable status; interpolation remains separately marked. |
| Accessible graph text | Sex panels described an occupation-fixed comparison | Use a correct sex-within-age/exposure description. |
| Report wording | A 36-month post-period called nearly four years | Correct to three years. |

## Source and transformation checks

All 94 available raw hashes match the local recorded manifest. Two archives, November 2022 and October 2026, were retrieved again from official Census URLs and match the stored bytes exactly. This independently checks those two retrievals, not all 94 sources. Five selected months, December 2018, October 2019, January 2020, November 2022 and October 2026, were regenerated for all six ages with the existing parser. Weighted occupational total, full-time and part-time cell differences were exactly zero. An alternative PRWKSTAT recode had zero discrepancies with PRFTLF in inspected employed records. The same-parser exercise does not independently validate every parser field.

The2019 composition weights and four quintile thresholds were rebuilt and reproduced every stored label. Exposure mapping coverage across age/month cells is approximately 97.25–98.87%, before additional regression support restrictions. Unmapped workers are excluded, not silently placed in Q1–Q4. Supported chart series/outcome combinations numbered 821 and all rebase to 100 in November 2022. Another 439 combinations lack an eligible baseline and are suppressed.

## THAIE formula and score reconstruction

The specialist rebuilt content and log-duration predictions from original embeddings and rating inputs, then checked the actual submitted TeX equation. For task j, the implementation is

$$p_j=\operatorname{logit}^{-1}\{\kappa\log_2(h_{50}/d_j)\}, \qquad \mathrm{THAIE}_j=e_jp_j, \qquad \mathrm{TIME}_j=e_j\min(1, h_{50}/d_j).$$

The slope is κ=ln(4)/log₂(h₅₀/h₈₀). The selected curve has h₅₀=203.012577 minutes, h₈₀=38.312431 minutes and κ=0.5762577283. Completion probabilities at those anchors are exactly 0.5 and 0.8 within floating-point tolerance. Reconstructed probabilities differ by at most 2.78e−16. Scores for 19,265 tasks through 923 O*NET, 798 SOC and 547 retained Census occupations reproduce stored E, THAIE, TIME and duration quantities within 8.89e−16. Effective hierarchical task weights sum to one. Positive durations, bounded content predictions, 0≤THAIE≤E and monotonic duration/fixed-slope horizon relationships passed. Content clipping affected 2,131 predictions and is an explicit modeling choice, not a newly discovered numerical failure.

The hierarchy gives equal weight to tasks within O*NET suboccupations, suboccupations within SOC, and matched SOC links within Census occupations. These are not measured workplace time shares. Of 867 Census–SOC links, 69 lack scores. Twenty-one Census occupations are entirely unmatched and excluded;31 retained occupations are only partially covered, including 22 below 80% link coverage. Means renormalize over matched links. This was previously insufficiently disclosed and is a measurement/selection risk, not an established arithmetic error. Curve calibration transfer to workplaces, prediction validity and uncertainty propagation remain unverified.

## Statistical estimand and formulas

For age-specific occupational–industry cells, the fitted conditional mean is

$$\mathbb{E}[Y_{oit}\mid X]=\exp\{\alpha_{oi}+\gamma_{o, m(t)}+\delta_{it}+\beta Q5_o Post_t+\sum_q\theta_q Q5_o PandemicQuarter_{qt}\}.$$

Y is a survey-weighted count of usual full-time or part-time employed people, not a job count, employment probability, observed hire, or individual transition. The percentage contrast is 100[exp(β)−1]. Transforming both ends of the log-coefficient interval is correct. The result is a conditional multiplicative DID contrast rather than the unadjusted ratio of two aggregate endpoints.

A common monthly age-population exposure offset is algebraically absorbed by industry×date fixed effects, so adding it does not change β. This does not adjust occupation-specific demographics or justify labeling the occupational charts employment rates. Current fixed effects are occupation×industry, occupation×season and industry×date. They are not state×industry×year fixed effects.

Standard errors are occupation-score working sandwich errors, not complete CPS survey-design errors. Repeated households, rotation overlap, occupation-code allocation and exposure measurement uncertainty are not fully propagated. Nominal 463 clusters do not ensure diffuse information. The variance-concentration inverse-Herfindahl count is 27.93, the largest occupation supplies 8.80% of variance and the top ten supply 52.42%. These are diagnostics, not substituted degrees of freedom.

## New robustness results

| Youth full-time, 47-month window | Relative contrast | Raw p |
|---|---:|---:|
| Current primary | −6.60% | .069 |
| Unchanged, bijective occupation-code links | −4.28% | .292 |
| Exclude influential occupation 735 | −7.64% | .030 |
| Exclude influential occupation 5000 | −5.71% | .111 |
| Exclude influential occupation 4850 | −7.46% | .039 |

The stable-code result has 95% CI[−11.77%, +3.85%] and retains 74.85% of primary-support weighted FT employment, with 329 supported occupations. It changes both mapping exposure and sample composition, so attenuation cannot be attributed uniquely to crosswalk bias. Leave-one-occupation-out exclusions were selected after inspecting influence and are post hoc, uncorrected diagnostics. Their nominally significant estimates must not be promoted as confirmatory evidence. The direction remains negative while nominal significance changes.

A minimum 80% matched-SOC coverage restriction, preserving original quintile assignments, gives −6.05% (95% CI[−12.70%, +1.11%], p=.096), retaining 94.63% of primary-support FT employment. This arbitrary-threshold eligibility sensitivity does not establish unbiased scores.

## Assumptions and unresolved limitations

1. 2019 freezes composition and cutpoints, not the date when the score was measured. THAIE uses retrospective task and capability information. It is neither observed pre-event adoption nor a randomized treatment.
2. Pre-2020 national fractional code allocations and directly reported 2020+ codes differ in measurement. Fifty-six old codes split. Current intervals do not capture allocation uncertainty.
3. Pandemic-quarter interactions absorb Q5 gaps in 2020–2021. Nominal symmetric windows leave only 23 or 12 nonpandemic premonths. The raw youth FT lead test p=.029 remains a concern. Holm nonrejection is not proof of parallel trends.
4. The pooled pre/post Q5 linear trend can absorb a genuine gradual response as well as pre-existing divergence. It is a sensitivity analysis rather than a definitive correction.
5. Common positive FT/PT support depends on observed outcomes. The FT-only sensitivity is useful but does not eliminate survey sparsity or selection.
6. PRFTLF refers to usual hours across jobs while occupational exposure follows the primary job. Full-time does not mean permanent employment; part-time does not mean temporary, contract or involuntary work. Repeated cross-sections do not trace workers.
7. The 12-test Holm family does not adjust for the full historical sequence of investigated outcomes, age boundaries and specifications. This is exploratory work. Joint-zero tests assess fitted coefficients, not AI causality; nonsignificance establishes neither zero effects nor age equivalence.

## Revised interpretation and research priorities

Retain a cautious descriptive signal of relatively weaker youth full-time employment in high-exposure occupations. Do not claim a robust causal AI effect, a demonstrated full-time-to-part-time move, an affected-age boundary, or permanent-to-contract displacement. First harmonize occupation groups over time and assess benchmark-vintage sensitivity. Then obtain suitable survey-design information and longitudinal hours, involuntary part-time, earnings, employer adoption and contract measures. New data access is not a prerequisite for correcting the current analysis.

Official definitions and coding documentation are available from [BLS CPS concepts](https://www.bls.gov/cps/definitions.htm), [BLS CPS technical documentation](https://www.bls.gov/cps/documentation.htm) and [Census occupation classification](https://www.census.gov/programs-surveys/cps/technical-documentation/methodology/industry-and-occupation-classification.html). October2025 CPS data were not collected, as noted in the [BLS full-/part-time table](https://www.bls.gov/cps/cpsaat08.htm). Display interpolation does not create an observed survey month.
