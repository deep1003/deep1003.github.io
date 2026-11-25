# European regional analysis critical audit, 25 November 2026

Three specialist reviews independently examined measurement and inference, source processing, and visualization/reproducibility. The manuscript was not edited. Raw inputs and prior results were preserved.

## Findings and corrections

| Priority | Finding | Action and remaining limit |
|---|---|---|
| High | Some regional scores use one published occupation; disclosed-cell mapping fraction was liable to be read as workforce coverage | Preserve provisional 208-region cohort, disclose per-region support and add 135-region descriptive sensitivity. Frozen original quintile cutoffs retained. No certified population coverage inferred. |
| High | Statistical claims depend on sample support and inference choice | Add support and weight-year sensitivities. Primary youth +2.689%, wild p=.0746; support >=50 occupations +1.876%, p=.2783. Ratio +1.556%, p=.5498 in screened sample. No robust causal displacement finding. |
| High | Joint pretrend output mixed one lead coefficient with a four-lead joint p-value | Blank effect/CI fields for joint rows, explicitly type inference and retain separate event-study coefficients. Correct generating script. |
| Medium | Annual chart displayed exact November intervention marker despite no monthly observation | Exact-month marker only on monthly series. Annual 2022 value and quarterly Q4 baselines remain explicitly distinct from November monthly baseline. |
| Medium | Main chart did not always respond to selected age; some software sex charts used quintile colors | Bind selected age to main plot. Men/women use consistent red/blue. Grey inter-sex shading is a gap, not a confidence interval. |
| Medium | CSV exports omitted source/frequency/baseline and quality flags | Add export provenance and original regional Eurostat u/b/d flags. Preserve missingness and suppression. |
| High | Existing reproduction archive regenerated an older, materially smaller dashboard | Replace with complete current offline site/data snapshot, portable validator and checksums. This reproduces rendering and validates indices, not the entire upstream collection/crosswalk pipeline. |
| Medium | Swedish monthly county counts linked to workplace employee occupation weights with different population | Explicitly qualify as partial composition proxy. Download free residence SSYK3 source and publish comparison. Same-resolution geography change alters 2/21 counties; versus current workplace SSYK4 alters 10/21 but confounds resolution. Exact monthly table geography wording remains unconfirmed. |

## Independent checks that passed

All 19,265 task probabilities reproduced E times horizon probability with maximum absolute error 2.22e-16. Native time conversion, log-normal horizon calibration, p(H50)=0.5 and p(H80)=0.8 were checked. Full dummy weighted least squares reproduced absorbed fixed-effects coefficients and country-clustered standard errors within 1e-9. An independent exhaustive 64-sign restricted bootstrap reproduced p=.125 on a six-country check. Existing displayed annual count/index arithmetic, strict region aggregation and fixed age cohorts passed. Crosswalk aggregation sensitivity changed 28/241 quintile labels but zero Q5 memberships, with region score Spearman .99545.

## Interpretation limits

Exposure is a fixed 2022 task-based proxy, not observed adoption. Annual post-2023 comparisons do not identify a November 2022 discontinuity. Nonrejection of pretrends does not establish parallel trends. Country clusters carry uneven identifying information. COVID, industrial shocks, migration and boundary vintage remain unresolved. Conditional statistical association can be reported with caveats; a causal AI effect is not established. Threshold sensitivities are diagnostic, not selected for statistical significance. Screened samples change the target population.

The primary youth CR1 t confidence interval is +0.170% to +5.272%, whereas its restricted wild p is .0746. They must not be described as one matched bootstrap confidence procedure. All outcomes and diagnostic families remain visible, including multiplicity adjustments. Findings selected only for nominal significance would be inappropriate.

## Reproduction scope

The downloadable snapshot includes current chart runtime, source-backed aggregate data, quality/support files and a numerical validator. It is a reproducible rendering snapshot, not a claim that all national collection and harmonization stages are fully automated. Old acquisition scripts and original sources are retained locally for subsequent provenance reconstruction.
