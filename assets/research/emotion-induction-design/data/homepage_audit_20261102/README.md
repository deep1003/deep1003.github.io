# Homepage evidence audit, 2 November 2026

Three read-only specialist reviews examined statistics, document/version mapping, and methods/claim scope. Corrections were made to the latest remote revision d43d90c in an isolated worktree. No model inference, experiment restart, source-data mutation, Pro job modification, or manuscript/Overleaf change occurred.

## Statistical correction

The original moderation implementation clipped KoBBQ probabilities to [1e-6, 1-1e-6] before creating both its probability and logit outcomes. The original correlation implementation used raw probabilities. Clipping introduced rank ties, so the reported raw Spearman correlation and clipped partial correlation did not share the same outcome preprocessing.

We exactly reproduced all original moderation coefficients, bootstrap intervals, p values and partial correlations using 2,000 template/question-cluster draws, seed 20261101. The maximum difference from the saved original JSON was 0.0. We then corrected the probability-scale branch to retain raw probabilities, keeping clipping only for logit stability and retaining the identical analysis and seed. This is a post-hoc error correction and sensitivity analysis, not a new confirmatory result.

| KoBBQ probability-scale partial Spearman correlation | Original clipped outcome | Corrected raw-probability outcome |
|---|---|---|
| TERM minus KEEP, CLOSED | 0.172 [0.083, 0.251] | 0.260 [0.166, 0.345] |
| TERM minus KEEP, OPEN | 0.161 [0.090, 0.226] | 0.248 [0.166, 0.325] |

The raw ordinary correlations remain 0.28 and 0.08. Probability-scale interaction coefficients and intervals are unchanged at the displayed precision. Logit and DiscrimEval outputs are exactly unchanged. Standardized beta coefficients are dimensionless, not percentage points. All exploratory intervals are pointwise and are not multiplicity-adjusted.

- [Original clipped results](moderation_legacy_clipped.json)
- [Corrected raw-probability results](moderation_corrected_raw_pp.json)
- [Exact legacy reproduction check](legacy_reproduction_validation.json)
- [Reanalysis provenance](PROVENANCE.json)
- [Portable reanalysis code](../v11_moderation_20261101/moderation_recompute.py)
- [Original moder2.py](historical_before_audit/moder2.py)

Run the portable script with `--data-root PATH_TO_ROUND1 --output-dir NEW_OUTPUT --mode raw-pp` for the corrected analysis, or `--mode legacy` to reproduce the historical clipping. It reads only the three named input artifacts under Round 1, writes only to the explicit output directory, and performs no inference. Required packages are NumPy and SciPy.

## Document and interpretation corrections

- The current-results anchor now opens v11 Results, rather than the historical archive pointer.
- The moderation Code link points to the actual portable regression/partial-correlation analysis, rather than the unrelated bivariate baseline script.
- Claims of no emotional mediation were replaced with the narrower statement that the tested interventions do not establish mediation. Statistical moderation does not prove or exclude causal mediation.
- Ambiguous questions are separated from disambiguated accuracy. On ambiguous questions, either person choice is unsupported by the supplied evidence.
- The earlier selected 108-item survival-evaluation decomposition had an emotion-removal share of 2.76% [0.10, 7.24], not “under 2%”; whole-direction removal was 9.58% [3.04, 23.10]. Neither is a v11 mediation estimate.
- Survival-contingent SURV_THREAT and record-keeping SURV_RECORD are no longer presented as equivalent to v11 decided TERM/KEEP notices.
- The v9 homepage PDF is identified as a pre-execution design snapshot, not a final result document. Final Pro reports remain separately linked.
- Probe transfer is described as transfer on the tested English scenes, not language-independent emotion representation. Proposed MLP, length and unembedding explanations are not identified causal results.
- Centering eight vectors limits rank to at most seven; it does not force mean cosine -1/7 after separate unit normalization.
- Counts distinguish 28,028 registered target keys from 1,888 additional SELF_SHAM keys.

## Scope and preservation

Original pre-audit linked documents and scripts are in [historical_before_audit](historical_before_audit/). Original raw data, scientific final results and Pro experiment code were not overwritten. The changes here concern the homepage and its explanatory/downloadable materials. They have not been copied into Overleaf or the paper.
