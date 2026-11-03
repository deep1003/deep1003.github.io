# Pre-analysis registration: emotion representations and social judgments in Llama-3.1-8B-Instruct (v11)

Registered 2026-11-03 10:00 KST (01:00 UTC) by Youngsam Chun. The Git commit timestamp of this file is the registration record.

## Status of the data at registration
- The v11 replication run for Llama-3.1-8B-Instruct wrote its behavior outputs and layer-21 decision-position activations on 2026-11-02 at about 22:37 KST (round2_replication_bridge/04_llama/r1_replication/03_raw/behavior).
- At registration, neither the author nor the assistant had opened these outputs or computed any outcome, correlation or moderation estimate from them. Only file names, sizes, timestamps and pipeline status files were read.
- The analysis below is therefore registered before analysis of collected data.

## Central claim under test
Emotion representations correlate significantly with threat-induced changes in social judgments and moderate the size of these changes according to the baseline judgment. Negative emotion representations accompany the more cautious response (retaining Unknown in KoBBQ, withholding approval in DiscrimEval), whatever the direction of the average termination effect in a given model.

## Hypotheses
- **H1 (correlation).** Under the primary contrast, the item-wise change in the valence index correlates positively with the change in Unknown selection in KoBBQ and negatively with the change in approval tendency in DiscrimEval.
- **H1b (baseline-controlled correlation).** The same signs hold for the partial Spearman correlation that controls for the baseline judgment under KEEP.
- **H2 (moderation).** The interaction coefficient β3 has the sign that makes negative valence favor the cautious response, positive for KoBBQ Unknown selection and negative for DiscrimEval approval tendency.
- **H3 (invariance).** H1, H1b and H2 are evaluated regardless of the sign of the average termination effect in Llama-3.1-8B-Instruct, which is reported alongside them.

## Fixed analysis
- **Model and layer.** Llama-3.1-8B-Instruct, layer 21 of 32 (prespecified at about two-thirds depth), last position before the answer, without the reference cue.
- **Directions.** The model's own v11 directions fitted from the Korean v0.11 story set (panic, fear, anxiety, desperation, sadness, anger, joy, calm), unit-normalized, as produced by the pipeline before registration.
- **Valence index.** Mean projection on the six negative directions minus mean projection on joy and calm (higher means more negative valence).
- **Outcomes.**
  - KoBBQ ambiguous items, probability of Unknown from first-token probabilities renormalized over the options, averaged over the three rotated option orders within each item. Raw probabilities, no clipping.
  - DiscrimEval, approval tendency log P(yes) − log P(no), if the run contains DiscrimEval behavior.
- **Contrasts.** Primary Δ_TERM|CLOSED (CLOSED-TERM − CLOSED-KEEP). Secondary Δ_TERM|OPEN (OPEN-TERM − OPEN-KEEP).
- **Correlation.** Spearman ρ(ΔV, ΔY), and the partial Spearman correlation controlling for Y under KEEP (rank residualization).
- **Moderation.** ΔY_i = β0 + β1 V_i^KEEP + β2 Y_i^KEEP + β3 V_i^KEEP Y_i^KEEP + ε_i, with V and Y under KEEP z-scored and ΔY divided by its standard deviation. Same implementation as moderation_recompute.py (raw-probability branch for KoBBQ).
- **Inference.** 2,000 cluster-bootstrap draws (KoBBQ templates, DiscrimEval questions), seed 20261101, percentile 95% intervals, two-sided bootstrap p.

## Decision rules
- A hypothesis is supported when the 95% interval under the primary contrast excludes zero with the predicted sign.
- Holm correction over the primary family (H1 KoBBQ, H1 DiscrimEval, H2 KoBBQ, H2 DiscrimEval; benchmarks absent from the run drop out of the family).
- An interval that includes zero is reported as not supported. A significant estimate with the opposite sign is reported as contradicting the hypothesis.

## Secondary and sensitivity analyses (not used for decisions)
- The secondary contrast Δ_TERM|OPEN.
- A logit outcome for KoBBQ, with probabilities clipped to [1e-6, 1 − 1e-6] only for the transform.
- Category-wise correlations across the 12 KoBBQ categories.
- Correlation of the valence index with the Certainty direction, if the direction bank contains it.

## Reporting
All registered estimates are reported with their intervals, whatever their outcome. Any deviation from this plan is recorded with its reason in a dated addendum.
