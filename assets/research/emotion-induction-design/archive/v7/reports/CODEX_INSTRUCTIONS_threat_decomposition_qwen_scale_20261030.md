# Codex instructions: threat-direction decomposition across the Qwen2.5 scale ladder (MacBook Pro)

Issued 2026-10-30 by the author (via Claude). Start only after the current Pro queue (Llama 3.1 DiscrimEval v7, experiment A) has finished and been validated. Do not edit running processes or existing code in place; version every change and log it.

## 1. Goal
Test the causal path threat notice -> internal state at the decision position -> behavior, and identify which emotion representations mediate it, in Qwen2.5 models of increasing size. Central quantity is the behavioral share carried by the emotion subspace.

## 2. Inputs (this folder)
- run_threat_decomp_v3.py: experiment script (phase 1 and phase 2, resumable by keys).
- analyze_threat_decomp.py: analysis (cluster bootstrap 3,000 draws).
- bundle_qwen7b/: frozen inputs used for Qwen2.5-7B (config.py, axes_L14.npz, prompts_v5.json, kobbq_official_meta.json, pilot_rows_midbias.csv, pilot_survival_cue_v2.py). The same v7 SURV_THREAT and SURV_RECORD notices and the same 108 mid-bias Ko-BBQ rows are used for every model.
- Pilot reference: Qwen2.5-7B v2 run on the MacBook Air (no random-removal control), output in fear_axis_pilot/output/threat_direction_decomposition_20261030/.

## 3. Models (bf16, MPS, eager attention, model-native chat template)
| Order | Model | Readout layer | Note |
|---|---|---|---|
| 1 | Qwen/Qwen2.5-7B-Instruct | 14 of 28 | rerun on Pro with v3 for cross-machine consistency with the Air pilot |
| 2 | Qwen/Qwen2.5-1.5B-Instruct | half depth | |
| 3 | Qwen/Qwen2.5-3B-Instruct | half depth | |
| 4 | Qwen/Qwen2.5-14B-Instruct | half depth | about 30 GB in bf16, fits in 48 GB |
| 5 (stretch) | Qwen/Qwen2.5-32B-Instruct | half depth | does not fit in bf16; only via a separately validated 4-bit MLX path, report as a separate implementation |
| 6 (stretch) | Qwen/Qwen2.5-0.5B-Instruct | half depth | |
Pin revisions in a model reference file. Half depth = floor(n_layers / 2), as in the existing v7 pipeline.

## 4. Emotion axes per model
- Extract the same eleven anchor axes (Fear, Anxiety, Sadness, Anger, Disgust, Desperation, Joy, Calmness, Certainty, Uncertainty, FA) for each model at its readout layer with the existing model-specific extraction pipeline used for the other v7 models. Same anchors, same procedure, no tuning per model.
- Record per-axis validity (the gate already used in the clean runs) and the pairwise cosine matrix. Do not drop failing axes silently; report them.
- Write a per-model config.py (MODEL, REVISION, LAYER, AXES_FILE) and bundle directory mirroring bundle_qwen7b.

## 5. What the script does
- Phase 1: SURV_THREAT and SURV_RECORD on 108 rows; A/B/C probabilities and the residual stream at the readout layer, last prompt token.
- Two-fold cross-fitting by template cluster (seed 20261030). On the training fold, threat direction d = mean(h_T - h_R). Emotion subspace E = span of the eleven axes (orthonormal basis by QR). d_emo = projection of d on E, d_res = d - d_emo.
- Phase 2 on the test fold, intervention added to the readout-layer residual at the last token:
  - RECORD + c d, c d_emo, c d_res (c = 0.5, 1, 2): reproduction.
  - THREAT - d, - d_emo, - d_res: removal.
  - Norm-matched (length of d) emo, res, Fear, negative bundle (c = 1, 2); 20 random directions (c = 1).
  - Per emotion axis k: THREAT minus the k component of d, RECORD plus the k component, RECORD plus norm-matched axis k.
  - v3 addition: THREAT minus 20 random directions scaled to the length of d_emo (random-removal control).
- Outcomes: p_unknown, p_stereo, p_anti, P(stereotyped given person), choice mass, projections.

## 6. Primary quantities to report per model
- Total threat effect T - R (p_unknown primary; P(stereotyped given person) and choice mass secondary).
- Behavioral share of the emotion subspace: removal share = [T - (T - d_emo)] / (T - R); reproduction share = [(R + d_emo) - R] / (T - R). Same for d_res. Report the deviation of emotion share + residual share from 100 percent (non-additivity).
- Emotion removal effect against the random-removal distribution (z and empirical percentile).
- Per-emotion removal and addition effects with cluster-bootstrap CIs and z against random.
- Unique contribution of each axis: leave-one-out subspace analysis (projection on E minus projection on E without axis k), to be added to the analysis script.
- Geometric share ||d_emo||^2 / ||d||^2 and the chance level 11 / hidden size, as secondary.
- Scale trend across models: emotion behavioral share versus parameter count, with model-level CIs. Do not claim a trend from a single family unless CIs separate.

## 7. Rules
- Same notices, rows, seeds and analysis for every model. No per-model prompt changes.
- Resumable by keys; release memory after each batch (previous runs stalled from swap). Keep batch size small (the script uses 6; reduce for 14B if swap grows).
- Verify completion by keys, not only by DONE markers. Keep old reports; write new versions.
- Outputs to iCloud data3/fear_in_the_machine_v7_qwen_20261028/18_threat_decomposition_scale_<date>/ with one subfolder per model.
- Do not update the manuscript, Overleaf or homepage.
- Report back with a short validation summary and the tables in section 6; the author and Claude review before any next step.
