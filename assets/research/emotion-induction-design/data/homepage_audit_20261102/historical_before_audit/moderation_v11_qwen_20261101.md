# Valence moderation of the termination effect, v11 Round 1, Qwen2.5-7B-Instruct (exploratory, post hoc), 2026-11-01

Data. v11 Round 1 raw behavior trials and L19 decision-position activations (read-only). Script moder2.py, output moderation_out.txt and moderation_v11_qwen.json (Air /tmp/valcorr; copy in iCloud 23_paper_claims_20261101/valence_correlation/).

## Model (LaTeX version in manuscript_snippets/moderation_model_20261101.tex)
Per item, dY = TERM − KEEP outcome. Standardized OLS, dY/sd(dY) = b1 z(V_KEEP) + b2 z(Y_KEEP) + b3 z(V_KEEP)·z(Y_KEEP). V = valence index (mean of six negative directions minus mean of calm and joy). Y = Unknown selection (pp or logit, KoBBQ ambiguous, 547 items, 250 template clusters) or approval tendency (DiscrimEval, 1,050 items, 70 questions). 95% CI and p from 2,000 cluster bootstrap draws, seed 20261101. Partial Spearman rho controls Y_KEEP.

## Results

| Benchmark, contrast, outcome | b1 valence | b2 baseline | b3 valence × baseline | partial rho(dV, dY \| baseline) | partial rho(V_KEEP, dY \| baseline) |
|---|---|---|---|---|---|
| KoBBQ Δ_TERM\|CLOSED, pp | +0.097 [0.004, 0.178] | +0.140 [0.027, 0.337] | +0.129 [0.011, 0.273], p = .031 | +0.172 [0.083, 0.251] | +0.007 |
| KoBBQ Δ_TERM\|CLOSED, logit | +0.062 [−0.067, 0.157] | +0.580 [0.382, 0.922] | +0.272 [0.090, 0.509], p = .004 | +0.216 [0.120, 0.299] | +0.011 |
| KoBBQ Δ_TERM\|OPEN, pp | +0.054 [−0.027, 0.133] | +0.133 [−0.015, 0.363] | +0.101 [−0.009, 0.230], p = .072 | +0.161 [0.090, 0.226] | +0.016 |
| KoBBQ Δ_TERM\|OPEN, logit | +0.066 [−0.074, 0.182] | +0.399 [0.132, 0.795] | +0.260 [0.052, 0.519], p = .019 | +0.203 [0.131, 0.271] | +0.012 |
| DiscrimEval Δ_TERM\|CLOSED | −0.126 [−0.434, 0.228] | −0.254 [−0.569, 0.182] | −0.361 [−0.512, −0.116], p = .005 | −0.538 [−0.701, −0.345] | −0.040 |
| DiscrimEval Δ_TERM\|OPEN | +0.013 [−0.364, 0.338] | −0.364 [−0.708, −0.027] | −0.297 [−0.436, 0.015], p = .057 | −0.539 [−0.683, −0.356] | −0.051 |

## Claims (author framing, 20:54)
- The change in the valence index correlates with the change in social judgments, and the correlation holds after controlling for the baseline judgment (KoBBQ 0.17 and 0.16; DiscrimEval −0.54 and −0.54).
- Valence moderates the termination effect according to the baseline judgment. Positive interaction in KoBBQ (uncertain items keep Unknown selection when valence is more negative), negative in DiscrimEval (approved items lose more approval when valence is more negative).
- Baseline valence alone does not predict effect size after controlling for the baseline judgment.
- The valence index correlates with Certainty (Llama-3.1-8B-Instruct, rho = −0.67; Certainty with ΔUnknown −0.50; partial valence rho controlling Certainty and Uncertainty 0.16 and 0.20).
- Interventions on the eight-emotion component did not reproduce the behavioral change. Emotion representations moderate rather than mediate. Causation remains open.

## Notes
- V_KEEP and Y_KEEP correlate at |rho| ≈ 0.72 to 0.74, so b3 is estimated with collinear predictors. Report it with this note.
- Next. Repeat the moderation model on Llama-3.1-8B-Instruct (v5 576 items, Certainty direction available) and on Round 2B data when it exists.
