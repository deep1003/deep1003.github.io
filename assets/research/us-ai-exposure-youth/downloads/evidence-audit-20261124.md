# Productivity and the Age Composition of Employment in AI-Exposed U.S. Industries

## Evidence audit and revised interpretation

Research question. Have highly AI-exposed industries experienced productivity improvements alongside weaker employment opportunities for labor-market entrants? This retrospective audit evaluates two proposed results without requiring that either be statistically significant. Estimates and figures are reproducible from the accompanying code and tables. The evidence supports a qualified descriptive employment-composition finding, but does not establish the proposed productivity–employment tradeoff or an AI causal effect.

### Main results

| Outcome and window | Estimate | 95% confidence interval | Conventional p | Small-cluster wild-score p |
|---|---|---|---|---|
| Labor productivity growth, 2022–2025, per SD of THAIE | +0.89 percentage points/year | −0.95 to +2.72 | .303 | Not computed |
| Full-time young/older ratio, through 2025 | −7.73% | −13.79% to −1.24% | .024 | .062 |
| Full-time young/older ratio, through 2026 | −9.58% | −16.13% to −2.51% | .013 | .048 |
| Total young/older ratio, through 2025 | −7.03% | −11.82% to −1.98% | .011 | .063 |
| Total young/older ratio, through 2026 | −9.23% | −14.65% to −3.48% | .005 | .039 |

The full-time employment ratio is employment among ages 22–25 divided by employment among ages 40 and older. These are relative ratio changes, not percentage-point changes in employment rates. The 2025 common window aligns the employment analysis with the latest acquired productivity observations. Employment data extend through January–September 2026; productivity data end in 2025. All annual CPS comparisons use January–September. The 2026 extension is not a full-calendar-year estimate.

## Data and measurement

Industry exposure is frozen using 2019 national CPS employment and THAIE-linked employment, with employment-weighted quintile ranks among 13 broad CPS industries. Q5 comprises information, financial activities, and professional and business services. With only 13 broad industries, Q5 is a coarse employment-weighted exposure group, not exactly 20% of industries or workers. Other industries form the comparison group. Exposure is not reassigned after dropping an industry. These are industry groups, not the occupational Q5 groups used in earlier analyses.

The productivity analysis uses 33 official BLS KLEMS series across 11 matched industries, three measures, and 2010–2025, totaling 528 annual observations. Measures are labor productivity, total factor productivity, and real sectoral output. The main outcome is annualized labor productivity growth from 2022 to 2025, compared with 2017–2019 growth. Published indexes are normalized to 2017 = 100. Their absolute levels cannot establish that one industry has a higher productivity level than another. Transport/utilities and public administration are excluded from the productivity match rather than combined through arbitrary index averaging. BLS private-business coverage and CPS all-worker exposure/employment coverage differ, particularly in education and health. The 11-industry employment sensitivity partially aligns industry coverage, but does not eliminate the ownership mismatch.

BLS data were acquired through the free public API. Six 2025 industry productivity growth figures were independently checked against the official release. The source request bodies, responses, URLs, and hashes are retained. No paid data or services were used.

## Empirical design

The primary productivity model regresses annualized growth on one standard deviation of frozen 2019 THAIE across 11 industries. HC3 standard errors and t(9) confidence intervals are reported. Unweighted OLS is primary; 2019-employment-weighted WLS is a sensitivity. Growth panels additionally include industry and year fixed effects, a THAIE-by-post-2022 interaction, and THAIE interactions for 2020 and 2021. These panels test additional growth after 2022 rather than a cross-sectional level relationship.

The age-composition model estimates the conditional young-to-older employment ratio using a count quasi-likelihood. Its linear predictor includes industry effects, year effects, Q5-by-post-2022, and separate Q5 interactions with 2020 and 2021. Conditioning on the combined young and older counts is equivalent to a log young/older count-ratio specification and avoids arbitrary log-zero substitutions. Counts are survey-weighted aggregates; precision is based on industry-level score variation, not on treating weighted persons as independent observations. The reported effect is 100[exp(beta) − 1].

The main employment window is 2017–2025; the extension ends in 2026. State-industry models replace common year effects with state-by-year effects, absorbing common within-state population and macroeconomic shifts. National industry exposure supplies only 13 independent clusters, including three treated industries. Standard errors cluster by industry, not state. The t reference distribution has 12 degrees of freedom. A null-imposed, nuisance-profiled wild-score sensitivity enumerates all 8,192 industry-level Rademacher sign patterns. This is a small-cluster robustness check, not a randomized treatment test. Confidence intervals in the figures are conventional pointwise cluster intervals and are not inverted wild-score intervals.

Industry-specific linear trends, exclusion of 2020–2021, a pre-AI placebo, an 11-industry matched sample, continuous exposure, long-period event studies, and leave-one-industry-out estimates assess robustness. Full-time and total-employment outcomes are both reported. Holm corrections are provided for the two common-window employment outcomes and the two productivity measures. A separate retrospective audit covers the five focused prior model families; it is not a correction for every historical project test and is not preregistration.

## Findings

### Productivity

The estimated post-2022 productivity-growth slope is positive but imprecise. The 95% interval includes negative and substantial positive associations. The pre-AI growth slope is also positive and insignificant. The long growth panel estimates only +0.023 additional annual growth log points per SD after 2022, with p = .962. Total factor productivity likewise provides no significant post-2022 association. Thus, this sample does not substantiate either a productivity-growth advantage or a generative-AI productivity acceleration. A positive sign alone is insufficient evidence.

### Employment age composition

The young/older ratio declines more in the three high-exposure industries than in the comparison industries. Conventional estimates are negative in national models, state-by-year models, the pandemic-exclusion model, the matched 11-industry sample, and every leave-one-industry-out estimate. The common-window full-time effect is −7.73%. Its conventional two-outcome Holm-adjusted p is .024, but its small-cluster wild-score p is .062. The 2026 extension reaches p = .048 in that sensitivity, narrowly below .05. The total-employment counterpart is similar. This is not uniformly strong inference across time windows.

Short-window joint pretrend p-values are approximately .20 for full-time and .96 for total employment. Long-period binned tests yield .166 and .954. Failure to reject pretrends is not evidence that parallel trends hold, particularly with 13 clusters. Industry-specific linear trends change the common-window full-time estimate to +2.31%, with a 95% interval of −4.55% to +9.67% and p = .487. The total-employment estimate becomes −1.41%, with p = .715. This sensitivity materially limits causal interpretation. Trend specifications can also absorb genuine gradual treatment responses, so their null estimates do not prove that an effect is absent.

The ratio decomposition is essential. Between 2022 and 2026, young full-time employment in high-exposure industries increased by approximately 0.51%, while older full-time employment increased by 4.67%. In other industries, young full-time employment increased by 5.20%, while older full-time employment decreased by 0.65%. A relative weakening is visible, but an absolute collapse in young full-time employment is not. The ratio cannot identify hiring, separations, retirement, occupational switching, cohort composition, or individual transitions into part-time or contract work.

### Can the two proposed findings be joined?

No. An exploratory directed intersection–union test of a positive productivity slope and a negative full-time age-ratio contrast has p = .152, limited by the productivity result. This is not a mediation analysis. BLS and CPS coverage also differ. The present results cannot show that AI-generated productivity gains caused firms to replace young workers, that older workers captured those gains, or that aggregate welfare increased or decreased.

## Relationship to prior evidence

The Stanford Canaries study documents weaker employment among ages 22–25 in AI-exposed occupations using ADP payroll records. Its unit, coverage, and exposure grouping differ from this industry analysis. Its authors discuss descriptive interpretation, education sensitivity, and pre-existing trends. Our findings are directionally consistent with relative early-career weakness but do not reproduce its effect size or establish its hiring mechanism.

The published Generative AI at Work study provides firm-level evidence that an AI assistant improved worker productivity, with heterogeneous benefits across experience and skill. Such evidence establishes that productivity gains are possible in particular tasks and settings. It does not validate a national industry-level productivity effect in the present data. Studies of recession entry show why weak early-career opportunities may have lasting consequences, but those estimates cannot be imported as the monetary cost of AI exposure.

Pretrend tests and conventional significance should be interpreted in light of Roth's work on pretesting and Rambachan and Roth's work on deviations from parallel trends. The present trend sensitivities are not a formal HonestDiD analysis.

## Claims suitable for a manuscript

Supported as a qualified descriptive result. After 2022, the ratio of employment among ages 22–25 to employment among ages 40 and older weakened more in the highest-THAIE broad industries than in other industries. The result is directionally stable across several specifications, but is sensitive to industry trends and small-cluster inference.

Not established. A positive relationship between THAIE and productivity growth; AI-driven productivity acceleration; causal displacement of young workers; an increase in older employment caused by AI; reduced hiring as the specific mechanism; movement from full-time to part-time or permanent to contract employment; a quantified welfare tradeoff.

Earlier occupational-Q5 age-gap estimates are retained as a separate analysis. Occupational and industry quintiles must not be substituted for each other. Existing linked-CPS and SIPP transition results and selective archived job postings do not independently identify the hypothesized downgrading mechanism.

## Retrospective selection audit

The bounded audit contains 128 non-placebo estimates across five previously explored occupational-THAIE families. Fifty-six have conventional p < .05; 17 remain below .05 after Holm correction across these 128 estimates. These counts are not independent discoveries. Some surviving variants have substantive pretrend or specification concerns. The previously emphasized adjusted occupational-Q5 young-versus-older gaps have nominal p-values of .0021 and .0062 in the state and industry-control variants, but bounded-audit Holm p-values of .208 and .556. Those occupational results should not be presented as prospectively selected confirmatory evidence. The new industry analysis is distinct and likewise exploratory. Broad multiplicity adjustment is a transparency sensitivity, not a substitute for an independent confirmatory sample or a valid identification design.

## Academic and policy implications

The contribution is a transparent distinction between productivity performance, employment age composition, and worker adjustment. The labor-market finding can motivate a descriptive paper on uneven entry opportunities, with clearly bounded inference. It cannot yet anchor a causal productivity-versus-displacement paper.

National monitoring should report hiring and retention by age, exposure, hours, and contract status. Regional monitoring should track whether exposure-intensive employment growth reaches young residents, while recognizing that this national-industry treatment supplies no separate state-level causal effect. Firms can evaluate paid entry pathways, supervised training, and internal mobility rather than assuming that higher older-worker shares imply productivity gains. For individuals, weaker entry opportunities could delay experience accumulation, but this analysis does not establish lifetime earnings losses. These are policy evaluation priorities, not demonstrated intervention benefits.

Additional data priorities are actual firm AI adoption dates and intensity; a representative firm-by-month posting panel with complete denominators; linked employer–employee hires and separations; usual and actual hours, involuntary part-time status, temporary-help and independent-contract arrangements; wages, benefits, training, and job tenure; firm output and hours on matched coverage; and predetermined exposure at the worker's origin job. Longer post-treatment follow-up, direct population denominators, stronger adoption variation, and designs addressing industry-specific shocks are necessary before estimating causal welfare effects.

## Sources

- BLS KLEMS series dictionary. https://download.bls.gov/pub/time.series/mp/mp.txt
- BLS productivity data tables. https://www.bls.gov/productivity/tables/home.htm
- BLS 2025 industry productivity release, November 20, 2026. https://www.bls.gov/news.release/archives/prod5_11202026.htm
- BLS free public API. https://api.bls.gov/publicAPI/v2/timeseries/data/
- Brynjolfsson, Chandar, and Chen. Canaries in the Coal Mine, August 2026 revision. https://digitaleconomy.stanford.edu/app/uploads/2026/08/Canaries_August2026.pdf
- Brynjolfsson, Li, and Raymond. Generative AI at Work. Quarterly Journal of Economics. https://doi.org/10.1093/qje/qjae044
- Oreopoulos, von Wachter, and Heisz. The Short- and Long-Term Career Effects of Graduating in a Recession. https://www.aeaweb.org/articles?id=10.1257/app.4.1.1
- Roth. Pretest with Caution. https://www.aeaweb.org/articles?id=10.1257/aeri.20210236
- Rambachan and Roth. A More Credible Approach to Parallel Trends. https://doi.org/10.1093/restud/rdad018

## Reproducibility and scope

Scripts are in work/us_paper_evidence_audit_20261124. Tables retain all model variants and diagnostics. validation.json records an independent statsmodels implementation matching the main QMLE coefficient and cluster standard error. Source provenance remains in the raw directory. Figures are saved without interactive rendering. This audit creates new artifacts only; existing manuscripts, website pages, and prior result directories were not modified.
