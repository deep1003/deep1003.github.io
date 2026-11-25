# Independent statistical-methods audit

## Confirmed defects repaired

1. Cached models were accepted solely because a filename existed in `run_validation.py`. Model reuse now requires matching hashes of the complete aggregate input, prepared sample, design matrix and terms, preparation/design AST, backend bytes and numerical package versions. A retrospective attestation checked the 40 historical caches against the previously archived reproduction bundle. This is transparently labeled retrospective, not contemporaneous provenance. A deliberately altered signature was rejected without modifying the real cache.
2. `independent_check.py` previously reported only a harmonized standard-error difference. It now reports the exact dummy FE rank (446), absorbed degrees convention (449), raw reference SEs, absorbed SEs, adjustment factor (1.000891928), and harmonized SEs. The raw maximum SE difference is 0.000246343; coefficient maximum difference is 4.72e-15; harmonized maximum SE difference is 1.13e-13. The check validates the score-sandwich implementation after harmonizing the finite-sample convention. It does not independently validate that convention or the CPS survey-design variance.

## Model formulas and implementation

The model is E[Y_oit | X, FE] = exp(alpha_oi + gamma_o,month(t) + delta_it + beta Q5_o Post_t + sum_q theta_q Q5_o PandemicQuarter_qt). Y is a weighted employment count, not an employment probability. The reported relative contrast 100[exp(beta)-1] and its transformed t interval are correctly computed. Occupation-assignment clustering is a defensible working model but does not capture the full CPS design, household overlap or correlated movements across occupations. The independent explicit-dummy fit is a genuine check of the coefficient and covariance arithmetic on the reduced panel.

A common monthly age-population offset is absorbed exactly by industry-by-calendar-date effects. Its absence is not a coefficient error. This does not adjust occupation-specific demographic composition, convert the occupational descriptive indices into employment rates, or identify individual transitions.

The three-way fixed-effect structure is identified through exposure differences among occupations within industry-month cells, conditional on recurring occupational seasonality and occupation-industry intercepts. It is not the previously requested state-by-industry-by-year regional panel. Public labels must preserve this distinction.

## Limitations affecting interpretation

- November 2022 is a common event date, not randomized adoption. Retrospective exposure, occupation-specific recovery, interest-rate sensitivity, work-from-home exposure, education and hiring-cycle differences can remain confounders.
- Pandemic-quarter Q5 interactions absorb the Q5 gaps during 2020–2021, leaving only 23 or 12 non-pandemic pre-months in the long and short models. A nominal symmetric calendar window does not guarantee comparable identifying information.
- The youth FT lead test has raw p=.029. Holm non-rejection is not evidence that parallel trends holds. Omitting pandemic leads further narrows the tested assumption.
- The Q5 linear-trend sensitivity fits its slope over pre and post together. It can absorb a gradual genuine response as well as pre-existing divergence. It should not be characterized as definitive removal of bias.
- Common FT/PT positive FE support selects on outcome realizations. The existing FT-only sensitivity restores all weighted FT counts and is an appropriate disclosure; it does not solve all survey-sparsity or selection concerns.
- Age-specific models compare changing age cells, not fixed cohorts or individuals. FT/PT status cannot identify permanent-to-contract work or involuntary downgrading.
- The 12-test Holm family is exploratory and does not account for the full sequence of historical outcomes, age boundaries and specifications examined. Avoid a confirmatory framing.
- An all-zero joint test is a test of model coefficients, not a test of AI causality. Nonsignificance does not establish zero effects, equal age effects, or equivalence.

## Influence concentration diagnostic

For the 22–25 FT primary model, 463 nominal occupation clusters yield an inverse-Herfindahl variance-concentration count of 27.93. The largest occupation accounts for 8.80% of score-sandwich variance, and the top ten account for 52.42%. These are descriptive influence diagnostics, not formal degrees of freedom. Leave-one-influential-occupation refits would strengthen robustness. A large nominal cluster count alone should not be presented as sufficient assurance.

## Residual engineering risks

The strict cache check operates at `run()` model-reuse time. Standalone downstream report scripts consume tables and should additionally verify a run-level provenance manifest before publication. Retrospective attestation depends on the archived bundle used for comparison and must remain preserved if future bundles are regenerated. Supplemental sensitivity scripts have their own output behavior; they should receive the same provenance conventions before reuse as a general pipeline.

No plots were displayed in this audit. No backend numerical equations, original observations or estimates were changed.

## Completed influential-occupation sensitivity

Removing each of the three largest variance-contributing occupations from the youth FT model gives −7.64% (p=.0300; occupation735), −5.71% (p=.1110; occupation5000), and −7.46% (p=.0388; occupation4850). All are Q5 occupations. The baseline is −6.60% (p=.0687). The negative direction persists, but the nominal significance label changes under single-occupation exclusions. These three exclusions were selected after inspecting influence, are exploratory and have not been corrected for selection or multiple testing; they cannot rescue a confirmatory finding. Newly all-zero FE groups were pruned after each exclusion, and the remaining original common-support panel was retained.

## Publication gate

`validate_cache_provenance.py` reconstructs all40 current samples/designs and rejects mismatched signatures without automatic refitting. `summarize()` also verifies every available cache before regenerating tables. The original pre-audit bundle and its digest are preserved in this audit folder. The independent check does not require plots.
