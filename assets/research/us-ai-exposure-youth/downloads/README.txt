AI exposure and early-career work in the United States
Exploratory follow-up research release
22 November 2026

Research page
https://deep1003.github.io/assets/research/us-ai-exposure-youth/

Analytical scope
153 Basic Monthly CPS observations, January–September of each year 2010–2026. Regional results cover 50 states and DC. Annual values are matched nine-month observations, not full-calendar-year estimates. No monthly interpolation or projection is used. Rates are not seasonally adjusted. Exposure composition and quintile membership are fixed using 2019 employment.

Exposure indices
E is the shared BGE-M3 prediction of an Eloundou beta-style content rating. THAIE is E multiplied by a retained duration-completion curve. TIME is E × min(1, h50/d). The GPT-5 curve is held fixed with h50 = 203.012577 minutes and h80 = 38.312431 minutes. These are potential-exposure comparisons, not observed adoption or worker-level automation.

Denominators
P = population, E = employment, U = unemployment, N = non-participation.
EPOP = E/P; UR = U/(E+U). National rates divide summed weighted numerators by summed denominators. FTPOP and PTPOP divide full-time and part-time employment by population. Counts in annual tables are sums of nine monthly survey-weighted totals; divide by nine for average monthly levels. Ratios and relative changes use matched months.

Occupational curves divide employment in a quintile by the entire selected age-group population. They are contributions, not employment rates for an occupation-specific population. Conditional occupational unemployment uses only people linked to a previous occupation and excludes new entrants and other unmatched people. Q0 retains unmatched records in underlying payloads; five-quintile charts display Q1–Q5 only.

Earnings
Ages 22–25, wage and salary workers in outgoing rotation groups. Weighted median weekly earnings use ORG weights and CPI-U, CUUR0000SA0, in September 2026 dollars. Values below 30 ORG person-months are suppressed. Person-months are not independent people. Medians reflect composition and selection among employed workers. No causal wage DID is provided. Full-time/part-time do not distinguish permanent from temporary contracts.

DID outputs
regional_did_primary.csv contains 12 primary comparisons, including p_holm_primary12. Regional estimates are percentage points, with fixed 2019 population or labour-force weights and state/year fixed effects. The adjusted model controls for industry composition and COVID recovery. The event is ChatGPT's public release on 30 November 2022, with 2023–2026 as post-period. Long-window and other robustness outputs are separate.

occupational_did.csv contains 18 supplementary contrasts with p_holm_secondary18. Percent effects are 100 × (exp(change in average log Q5/other employment ratio) − 1). Pre-period years are 2017–2019 and 2022; post-period years are 2023–2026. The model conditions on state–industry–year totals. It does not estimate the same outcome as the regional employment-rate DID.

occupational_sensitivity_posthoc.csv contains checks added after seeing the occupational pre-trend diagnostic. These do not replace the main contrast. Event-study intervals are pointwise 95% state-cluster intervals, not simultaneous confidence bands. State-cluster CR1 inference is not the full CPS survey-design variance.

Reproduction
aggregate-did-reproduction.zip contains portable Python code, saved aggregate inputs, exact reference tables, a data dictionary, dependency information and a successful numerical reproduction check. It reproduces primary and supplementary DID from aggregates, not upstream predictor fitting or raw CPS parsing. Read its README.md before running. Smoke checks display no plots.

Audit and source files
cps_source_manifest.json records the 153 source-file URLs, dictionary filenames and SHA-256 hashes. validation.json records analytical checks. release_manifest.json records the public release's files and SHA-256 values, excluding the manifest itself. Third-party source rights remain with their owners; no new blanket licence is assigned to source materials.

Interpretation
This is an exploratory follow-up, separate from the submitted THAIE manuscript. Negative occupational contrasts coexist with pre-trend concerns and baseline sensitivity. The regional evidence is imprecise. Neither a clear causal AI effect nor proof of zero effect follows from these results.
