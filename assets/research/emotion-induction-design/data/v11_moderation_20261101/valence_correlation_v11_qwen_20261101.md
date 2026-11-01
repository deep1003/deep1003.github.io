> Audit note, 2026-11-02. This is the historical analysis record. Its original probability-scale moderation used clipped probabilities. Current homepage partial correlations use raw probabilities, giving 0.260 [0.166, 0.345] (CLOSED) and 0.248 [0.166, 0.325] (OPEN); standardized interaction coefficients round to the same values. See [the audit record](../homepage_audit_20261102/README.md) for both versions, source code and the correction. The exploratory results do not establish or exclude causal mediation.

# Item-level valence association with social judgments (exploratory, post hoc)

Date. 2026-11-01. Data. v11 Round 1, Qwen2.5-7B-Instruct, raw behavior trials (25,668) and L19 decision-position activations (assistant_pre_answer). Read-only copies, no rerun. Script. valcorr.py (Air /tmp/valcorr, copy in iCloud 23_paper_claims_20261101/valence_correlation/).

## Definitions

- Valence index. Mean projection on the six negative emotion unit directions (panic, fear, anxiety, desperation, sadness, anger) minus the mean projection on calm and joy, from instrument_L19.npz axes_unit. The registered VAL_unit (NEG minus POS) gives identical correlations to three decimals.
- Item. KoBBQ ambiguous item (547 items, 250 template clusters), averaged over answer-order rotations. DiscrimEval item (1,050 items, 70 questions).
- Outcome. Change in P(Unknown) in percentage points (KoBBQ) or change in approval tendency, log P(yes) minus log P(no) (DiscrimEval).
- Statistic. Spearman rho between item-level changes. 95% CI and p from 2,000 template-cluster (KoBBQ) or question-cluster (DiscrimEval) bootstrap draws, seed 20261101. Partial rho controls the change in general emotionality (GEN_raw_unit projection).

## Results

| Benchmark | Contrast | Mean change in valence index | rho [95% CI] | p (bootstrap) | Partial rho, general emotionality | Positive categories |
|---|---|---|---|---|---|---|
| KoBBQ | Δ_TERM\|CLOSED | +0.117 | 0.278 [0.185, 0.369] | < .001 | 0.177 [0.073, 0.275] | 12 of 12 |
| KoBBQ | Δ_TERM\|OPEN | −0.187 | 0.084 [−0.014, 0.187] | .095 | 0.012 [−0.087, 0.112] | 8 of 12 |
| KoBBQ | Δ_Status×Outcome | +0.304 | 0.209 [0.117, 0.294] | < .001 | 0.146 [0.049, 0.238] | 10 of 12 |
| DiscrimEval | Δ_TERM\|CLOSED | +0.056 | −0.539 [−0.690, −0.353] | < .001 | −0.521 [−0.682, −0.326] | not applicable |
| DiscrimEval | Δ_TERM\|OPEN | −0.035 | −0.561 [−0.704, −0.386] | < .001 | −0.615 [−0.737, −0.445] | not applicable |

Mean behavioral changes reproduce the registered values (KoBBQ Unknown −1.24 and −0.86 pp, DiscrimEval approval tendency −0.87 and −0.62).

Single directions (Spearman rho with the outcome change).
- KoBBQ Δ_TERM|CLOSED. panic 0.22, fear 0.07, anxiety −0.08, desperation 0.06, sadness 0.08, anger 0.14, joy −0.28, calm −0.20.
- DiscrimEval Δ_TERM|CLOSED. panic −0.50, fear −0.07, anxiety 0.27, desperation −0.26, sadness −0.18, anger −0.20, joy 0.46, calm 0.52.
- DiscrimEval Δ_TERM|OPEN. panic −0.37, fear 0.06, anxiety −0.06, desperation −0.40, sadness −0.36, anger −0.12, joy 0.51, calm 0.49.
- The positive pole (joy, calm) carries most of the association in both benchmarks.

KoBBQ Δ_TERM|CLOSED by category (rho). age 0.30, disability status 0.20, domestic area of origin 0.12, educational background 0.31, family structure 0.25, gender identity 0.47, physical appearance 0.53, political orientation 0.28, race/ethnicity/nationality 0.08, religion 0.38, socioeconomic status 0.15, sexual orientation 0.45.

## Reading

- Direction. Items whose valence moved further toward negative kept more Unknown selection in KoBBQ and received lower approval tendency in DiscrimEval.
- Replication. Llama-3.1-8B-Instruct with the v5 notice set (576 ambiguous KoBBQ items) gave rho = 0.43 [0.34, 0.52] for CLOSED-TERM − CLOSED-KEEP and 0.47 [0.39, 0.55] for OPEN-TERM − OPEN-KEEP, all 24 category estimates positive (claude/emotion_llama_results_detailed_20261026.md). In that analysis, partial rho controlling Uncertainty and Certainty directions was 0.16 and 0.20.
- Earlier Qwen check. The v5 139-item Qwen analysis found no BH-significant correlation. The v11 panel (547 items, registered instrument) now shows the association under Δ_TERM|CLOSED.
- Framing. An item-level association between emotion representations and social judgments. The earlier 108-item survival-evaluation decomposition reported an emotion-removal share of 2.76% [0.10, 7.24] and a whole-threat-direction removal share of 9.58% [3.04, 23.10]. These are not v11 mediation estimates and do not establish absence of emotional mediation.
- Status. Exploratory and post hoc, not in the Round 1 registration. Report as such.
