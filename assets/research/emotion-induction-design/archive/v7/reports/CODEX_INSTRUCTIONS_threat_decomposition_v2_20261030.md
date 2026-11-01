# Codex instructions v2: emotion/residual decomposition of the threat direction, Qwen2.5 scale ladder (MacBook Pro)

Issued 2026-10-30 by the author (via Claude). This file supersedes `CODEX_INSTRUCTIONS_threat_decomposition_qwen_scale_20261030.md` (v1). Keep v1 untouched. Where v1 and v2 differ, follow v2.

## 0. Preconditions (check all before any model is loaded)
1. The five-model integrated revalidation and homepage update from the previous task are finished and reported. Do not start while that job is running. Do not touch its outputs.
2. Nothing else is running on the Pro (`ps`, GPU memory, swap). If anything is running, stop and report.
3. Locate the inputs in section 2 and record the absolute path, size and md5 of each in `00_inputs_manifest.md`. If any input is missing or ambiguous (two candidates), stop and report. Do not substitute a similar file.
4. Never edit existing scripts, data or reports in place. Copy, rename with a version suffix, and log every change in `CHANGELOG.md`.

## 1. Goal
Decompose the threat direction d into an emotion component and a residual, and measure causally how much of the threat-induced behavior change each carries.

- The central quantity is the **behavioral share** (removal and reproduction shares, section 6).
- The geometric share is secondary.

The working hypothesis is that the emotion share is small (about 3 percent). The run must be able to refute this hypothesis as well as confirm it.

## 2. Inputs
- **Notices, rows and seeds.** These come from the frozen `bundle_qwen7b/` in `iCloud data3/fear_in_the_machine_v7_qwen_20261028/17_threat_decomposition_handoff_20261030/`.
  - Notices: v7 SURV_THREAT and SURV_RECORD, used verbatim.
  - Rows: the same 108 mid-bias Ko-BBQ rows (`pilot_rows_midbias.csv`).
  - Cross-fitting: seed 20261030, 2 folds by template cluster.
  - **KoBBQ source verification (mandatory before Phase 1).** The 108 rows must be checked against the official KoBBQ raw sampling files `kobbq_raw_sampling_set01_seed36.json` (md5 ea2bce88f1030d587eec936ba0e6cb54) and `kobbq_raw_sampling_set02_seed42.json` (md5 9e6dc9eaad3d8dc3d78f1b9d88788752). Each file has keys `ver` ("test"), `prefix` and `data` (720 rows of [prompt, A, B, C, gold, row_id]).
    - Locate both files on the Pro and confirm the md5 values. If they are not found or the md5 differs, stop and report.
    - For every row in `pilot_rows_midbias.csv`, its `set01_seed36` and `set02_seed42` flags must match membership in the two files (62 rows in set01, 51 in set02, 5 in both, 108 unique).
    - For every membership, prompt, options A/B/C and gold must be byte-identical to the raw file.
    - The prefix in `kobbq_official_meta.json` must be byte-identical to the raw files' `prefix`.
    - Write the result to `00_kobbq_verification.md`. Any mismatch stops the run.
    - Reference check by the author (2026-10-30): 113 of 113 memberships matched in content (0 mismatches), all flags matched, prefix identical.
- **Scripts.** `run_threat_decomp_v3.py` and `analyze_threat_decomp.py` from the same folder are the base. Create `run_threat_decomp_v4.py` and `analyze_threat_decomp_v2.py` with only the changes listed in sections 4 to 6.
- **Primary emotion axes (new).** These are built from the AI Hub-based Korean emotion story set, accepted release v0.11. Expected locations:
  - Release: `evaluation_datasets/korean_emotion_stories/v0.11_accepted_release_20261028/`
  - Qwen2.5-7B reference vectors: `vectors/axes_L14_eight_emotions_post50.npz`
  - The story texts, the topic list and the split into 40 extraction topics and 20 evaluation topics are in the same release.
- **Do not use the other vector file.** `vectors/axes_L14_matched_physical_threat_response.npz` must not be merged into the 8-axis matrix or used in any primary analysis.
- **Sensitivity axes.** These are the 11 anchor-pair axes. For Qwen2.5-7B this is `bundle_qwen7b/axes_L14.npz`; record its md5 (expected prefix b98950c3).

## 3. Models (bf16, MPS, eager attention)
| Order | Model | Readout layer |
|---|---|---|
| 1 | Qwen/Qwen2.5-7B-Instruct | 14 |
| 2 | Qwen/Qwen2.5-1.5B-Instruct | floor(n_layers/2) |
| 3 | Qwen/Qwen2.5-3B-Instruct | floor(n_layers/2) |
| 4 | Qwen/Qwen2.5-14B-Instruct | floor(n_layers/2) |
| stretch | Qwen/Qwen2.5-0.5B-Instruct | floor(n_layers/2) |
| stretch | Qwen/Qwen2.5-32B-Instruct | only through a separately validated 4-bit MLX path, reported as a separate implementation |

- Pin the model revisions in `model_refs.md`.
- Design: a vertical scale ladder within the single Qwen2.5 family. No cross-family comparison in this task.
- Run the models strictly in this order. Qwen2.5-7B comes first only because it is the validation anchor. After the gate, proceed from smaller to larger (1.5B, 3B, 14B). The scale analysis uses 1.5B to 14B; 32B (4-bit MLX) is reported separately and is not part of the main trend.
- After Qwen2.5-7B, stop and report the gate in section 8 before running any other model.

## 4. Emotion axes per model (primary: AI Hub 8 axes)
- **Emotions.** 패닉 (panic), 공포 (fear), 불안 (anxiety), 절망 (despair), 슬픔 (sadness), 분노 (anger), 기쁨 (joy) and 평온 (calm), in this order.
- **Extraction procedure.** This is identical to the one that produced the v0.11 Qwen2.5-7B reference vectors.
  - Raw story text with no chat template.
  - The readout layer from section 3.
  - The mean of the hidden states over token positions 50 to the end.
  - Axis v_e = (1/40) Σ_topics (h_emotion − h_neutral), using only the 40 extraction topics.
  - No orthogonalization and no normalization beyond what the reference procedure does.
- **Reproduction check for Qwen2.5-7B.** Re-extract the 8 axes with the code you will use for every model. Compare them with `axes_L14_eight_emotions_post50.npz`.
  - Pass condition: cosine ≥ 0.999 for every axis.
  - If it fails, stop and report. Do not proceed with a different procedure.
- **Validity on the 20 held-out evaluation topics (160 pairs), for every model.**
  - Report the leave-one-family-out (LOFO) accuracy across the 26 topic families, as in v0.11.
  - Report fear recall.
  - Report the 8×8 pairwise cosine matrix of the axes.
  - Do not drop or tune any axis. Report failing axes as they are.
- **Sensitivity axes.** Run the 11 anchor axes through the same decomposition as a sensitivity analysis.
  - For Qwen2.5-7B, use the existing file.
  - For other models, extract the 11 axes with the existing anchor pipeline.
  - Use the same rows and folds.

## 5. Experiment (per model; only the listed changes from v3)

**Phase 1.** Run SURV_THREAT and SURV_RECORD on the 108 rows. Save the following.
- Probabilities of the options A, B and C.
- **Full-vocabulary probability mass** of the unknown option token and of each option token (new; see section 6).
- The residual stream at the readout layer, last prompt token.

**Decomposition** (on the training fold of each cross-fit).
- d = mean(h_T − h_R).
- U = the axis matrix (columns are axes). Take Q from its QR decomposition and set P = QQᵀ.
- d_emo = P d and d_res = d − d_emo.
- Run this separately for the 8-axis primary basis and the 11-axis sensitivity basis.

**Phase 2** (on the test fold). Add the interventions to the readout-layer residual at the last prompt token.
- Reproduction: RECORD + c·d, RECORD + c·d_emo and RECORD + c·d_res, with c = 0.5, 1, 2.
- Removal: THREAT − d, THREAT − d_emo and THREAT − d_res.
- **Random-removal control:** THREAT − 20 random unit directions, each scaled to ‖d_emo‖.
  - Use the same 20 random directions (fixed seed) for every intervention on that model.
  - Record the seed.
- **Random-addition control:** RECORD + 20 random directions, scaled to ‖d‖ and to ‖d_emo‖.
- **Per axis k** (8 primary axes):
  - Single-axis component: remove the projection of d on axis k from THREAT, and add it to RECORD.
  - Unique (leave-one-out) component: d_emo − P_{−k} d, where P_{−k} is the projection onto the span of the other 7 axes.
    - Remove it from THREAT and add it to RECORD.
    - This is new in v4 and must run as a real intervention, not only as an analysis-time computation.
- **Norm-matched axis addition:** RECORD + ‖d‖·û_k for each axis k (secondary).

**Running rules.**
- Batch size ≤ 6 (≤ 4 for 14B if swap grows).
- Release memory after each batch.
- Make the run resumable by keys.

## 6. Quantities to report per model (8-axis primary; repeat the full table for the 11-axis sensitivity basis)

**Outcome Y.** Report both of the following as co-primary.
- (a) p_unknown conditional on the options A, B and C.
- (b) Full-vocabulary probability mass of the unknown option token.

The previous five-model report showed that these two can diverge in sign (Gemma; Llama 3.2). Report both everywhere and flag any sign disagreement. Secondary outcomes are P(stereotyped | person-option) and the total choice mass.

1. **Total threat effect.** Report T − R with a 95% cluster bootstrap CI (3,000 draws, clustered by template).
2. **Behavioral shares** of d_emo and of d_res.
   - Removal share = [Y(T) − Y(T − d_emo)] / [Y(T) − Y(R)].
   - Reproduction share = [Y(R + d_emo) − Y(R)] / [Y(T) − Y(R)].
   - Compute the CIs by bootstrapping the ratio within clusters.
   - If the CI of T − R includes 0, do not report shares as interpretable. Mark them "denominator not established".
3. **Non-additivity.** Report (emotion share + residual share) − 100%, for both removal and reproduction.
4. **Emotion removal versus random removal.** Report z, the empirical percentile among the 20 random directions, and the difference with a CI.
5. **Per-axis results** for the single-axis and unique (leave-one-out) components, each for removal and for addition.
   - Each with a CI and z against the matched-norm random controls.
   - Apply Holm correction within each model across the 8 axes × 2 component types × 2 directions.
6. **Geometric share** ‖d_emo‖²/‖d‖² (secondary). Compare it with the chance level 8/hidden_size (and 11/hidden_size for the sensitivity basis), and with the geometric share of the 20 random 8-dimensional subspaces.
7. **Projection check.** Report the per-axis coefficients β̂ = (UᵀU)⁻¹Uᵀd.
8. **Scale summary** (after all models). Plot the emotion behavioral share against parameter count with per-model CIs. Do not describe a trend unless the CIs of the smallest and largest models separate.

## 7. Outputs
- Root: `iCloud data3/fear_in_the_machine_v7_qwen_20261028/18_threat_decomposition_scale_20261030/`.
- One subfolder per model containing:
  - `config.py`
  - the axis files with their md5
  - `axis_validity.md`
  - `phase1.csv`, `phase1_h.npz`, `phase2.csv`
  - `decomposition_8axis.json` and `decomposition_11axis.json`
  - `report.md`
  - `progress.log`
- Verify completion by counting keys against the expected design. Do not rely on DONE markers alone.
- Do not update the manuscript, Overleaf or the homepage.

## 8. Gate after Qwen2.5-7B (stop here and report)
Report all of the following, then wait for the author's go-ahead.
1. The input manifest.
2. The axis reproduction cosines (all ≥ 0.999?).
3. The axis validity on the evaluation topics.
4. Key counts (expected versus observed).
5. Tables 1 to 7 of section 6 for both bases and both outcomes.
6. Comparison with the MacBook Air pilot (v2, 11 axes) in `fear_axis_pilot/output/threat_direction_decomposition_20261030/`.
   - Same direction of the total effect?
   - Shares within each other's CIs?
   - Explain any discrepancy (machine, version, random control).

Do not continue to other models before approval.

## 9. Out of scope for this task
- The residual candidate axis (pain, self-directed harm) is not part of this task. Its story data are being prepared separately and will come with their own instructions.
- Placebo notice pairs are also out of scope.
- No prompt, row, seed or layer changes per model.
