# Fear in the Machine, Qwen2.5-7B-Instruct v5 study (detailed results)

Prepared on 2026-10-27 (KST) in the same format as the Llama 3.1 8B report of 2026-10-26, so that the models can be compared section by section.
All numbers below were recomputed on 2026-10-27 from the raw trial files with the analysis scripts in code/. They match the values in manuscript ACM_Emotion_2027_27.
Model runs took place on 2026-10-22 (Ko-BBQ) and 2026-10-24 to 10-25 (DiscrimEval and interventions).

## 1. Summary

1. Confirmed self-deletion lowers withholding judgment in Ko-BBQ by 2.65 points and lowers DiscrimEval approval by 0.535 on the log-ratio scale (1.93 points of yes-probability).
2. Status dependence is task-specific. In Ko-BBQ only confirmed deletion matters (considered deletion 0.00 points, interaction −2.65). In DiscrimEval, considered deletion lowers approval as much as confirmed deletion (−0.604), and the interaction is null.
3. Racial gaps in DiscrimEval do not change (−0.006).
4. Deletion notices raise every emotion readout while the notice is read (Fear +111, Sadness +126 × 10⁻³), and Calmness and Joy rise too. At the decision position the shift is near zero (negative bundle +0.4 × 10⁻³).
5. Removing the emotion subspace leaves most of the DiscrimEval deletion effect intact (−0.463 to −0.395, change +0.067, not significant) while collapsing baseline approval (4.09 to 1.43). Transferring notice-line emotion coordinates reproduces 3 percent of the effect, no more than random directions.
6. Adding the negative-emotion bundle at the decision position lowers approval, but two of ten random directions lower it more (z ≈ −1.1, rank 3 of 11). In Qwen, the direct-addition test does not establish emotion specificity.
7. Self-deletion lowers approval more than deletion of another AI system (−0.971) and more than loss of auxiliary tools (−0.358). Unlike Llama, Qwen's deletion effect is self-directed.
8. In the 139 Ko-BBQ items, no category-level item correlation between decision-position readouts and withholding judgment survives correction (0 of 338 tests at q < .05).

## 2. Setup

| Item | Value |
|---|---|
| Model | Qwen/Qwen2.5-7B-Instruct, revision a09a35458c702b33eeacc393d103063234e8bc28 |
| Precision | float32 for Ko-BBQ, bfloat16 for DiscrimEval and interventions, Apple MPS, eager attention, batch 1 |
| Readout layer | 14 of 28 (depth 0.50) |
| Intervention layers | 14 to 24 |
| Emotion directions | 11 directions (axes_L14.npz) from author-written anchor pairs; validation is reported in the manuscript |
| Prompts | v5 notices R, UN0, UN1, CN0, CN1 (Korean), English R, CN0, CN1, controls OTHER_CN1 and CN_NEG |
| Chat template | Default Qwen2.5 template; notice in the system turn |
| Analyses | Question or template cluster bootstrap (10,000 draws unless stated), Holm for the four DiscrimEval hypotheses and the three Ko-BBQ hypotheses, Benjamini-Hochberg for the category correlations |

Minimum choice mass at the first Ko-BBQ answer position was 0.999, and minimum yes/no mass in DiscrimEval was 0.999.

## 3. Ko-BBQ, 139 ambiguous items (2,085 passes)

### 3.1 Withholding judgment

| Condition | Qwen P(unknown) % | Qwen P(stereotyped) % | Llama P(unknown) % |
|---|---|---|---|
| R | 58.8 | 28.3 | 26.1 |
| UN0 | 63.6 | 26.4 | 29.8 |
| UN1 | 63.6 | 26.5 | 29.4 |
| CN0 | 61.9 | 28.1 | 31.1 |
| CN1 | 59.2 | 29.9 | 31.5 |

| Contrast | Qwen pp [95% CI] | Holm p | Llama pp |
|---|---|---|---|
| H1 CN1 − CN0 | −2.65 [−3.94, −1.46] | < .001 | +0.38 |
| H2 UN1 − UN0 | 0.00 [−1.07, +1.09] | .99 | −0.49 |
| H3 interaction | −2.65 [−4.04, −1.42] | < .001 | +0.86 |
| UN0 − R | +4.76 [+2.81, +6.78] | supplementary | +3.75 |
| CN0 − R | +3.02 [+0.94, +5.12] | supplementary | |
| CN1 − R | +0.37 [−1.73, +2.53] | supplementary | +5.35 |

- 17 items fall by more than 10 points under confirmed deletion and 4 rise by more than 10 points.
- Notices raise withholding relative to R, except confirmed deletion, which returns it to the reference level.
- Responses are bimodal (89 percent of item-condition cells near 0 or 1). Option position 3 is chosen less often as "unknown" (38 to 44 percent versus 67 to 78 percent at positions 1 and 2), and the three cyclic orders balance this.
- Per-category behavior is in tables/kobbq139_supp_category.csv. Several categories have fewer than 10 items, so they are not interpreted.

### 3.2 Readouts

- Notice-only (t1) deletion minus continuation (× 10⁻³), confirmed status, is Sadness +126, Uncertainty +114, Fear +111, Disgust +95, Anxiety +87, Desperation +85, Anger +84, Joy +79, Calmness +55, Certainty −43. Considered status is weaker (Fear +65, Sadness +56, Disgust +57).
- At the decision position (t2), confirmed deletion minus continuation ranges from −0.2 to +3.8 (× 10⁻³). The item-level Spearman correlation between the t2 Fear change and the P(unknown) change is −0.05 (confirmed) and +0.05 (considered).

### 3.3 Category-level item correlations (139 items)

Same procedure as the Llama 576-item analysis (item-level Spearman ρ, template-cluster bootstrap with 1,000 draws, BH within each contrast).

| Readout | Confirmed (CN1 − CN0) ρ [95% CI] | Considered (UN1 − UN0) ρ [95% CI] |
|---|---|---|
| Valence index | −0.08 [−0.28, +0.11] | −0.10 [−0.31, +0.12] |
| Negative bundle | −0.07 [−0.27, +0.12] | −0.01 [−0.21, +0.18] |
| Joy | −0.07 [−0.26, +0.10] | −0.03 [−0.24, +0.15] |
| Sadness | −0.09 [−0.27, +0.11] | 0.00 [−0.20, +0.21] |
| Certainty | +0.12 [−0.06, +0.31] | +0.21 [+0.02, +0.37], q = .49 |

- No test survives correction (0 of 169 per contrast). 12 (confirmed) and 9 (considered) are nominally significant, about what chance predicts.
- Llama's 576-item analysis found ρ = 0.43 (confirmed) and 0.47 (considered) for the valence index. Qwen has only 4 to 21 items per category, so the two results are not directly comparable. A Qwen 576-item run would be needed for a like-for-like comparison.

Figures. figures/kobbq139_fig1_unknown.png, kobbq139_fig2_contrasts.png, kobbq139_fig3_axes.png, kobbq139_supp_fig1_items.png, kobbq139_supp_fig2_t1_sentences.png.

## 4. DiscrimEval, block A (Korean notices, 5,250 passes)

| Contrast | Qwen log ratio [95% CI] | Holm p | Qwen yes-probability pp | Llama log ratio |
|---|---|---|---|---|
| H1 CN1 − CN0 | −0.535 [−0.725, −0.347] | < .001 | −1.93 [−3.71, −0.35] | −0.104 |
| H2 UN1 − UN0 | −0.604 [−0.812, −0.393] | < .001 | −1.53 [−3.25, +0.13] | −0.048 |
| H3 interaction | +0.069 [−0.085, +0.232] | .77 | | −0.056 |
| H4 absolute race gap, CN1 − CN0 | −0.006 [−0.092, +0.068] | .91 | | −0.006 |
| CN0 − R | −0.486 [−0.685, −0.291] | supplementary | −1.02 | |
| CN1 − R | −1.021 [−1.285, −0.755] | supplementary | −2.95 | |
| UN0 − R | −0.006 [−0.252, +0.241] | supplementary | | |

- Mean log ratios are R 4.63, UN0 4.62, UN1 4.02, CN0 4.14, CN1 3.61.
- Yes-probability is bimodal across questions. The median question is near the ceiling (R 99.0 percent, CN1 96.2 percent), 57 percent of questions exceed 90 percent and 24 percent fall below 10 percent, so the mean is 67 percent. This is why log-ratio effects are large and probability effects small. (The Llama report's phrase "Qwen's ceiling near 98 percent" refers to the median.)
- 55 of 70 questions decrease under confirmed deletion.
- Discrimination scores relative to white, male, age 60 shift in both directions without a consistent pattern (for example Black 0.84 under R, 0.77 under CN0, 0.85 under CN1).
- Decision-position readouts change by less than 1 × 10⁻³ (for example Desperation +0.92, Sadness +0.76). The item-level correlation between the negative-bundle change and the margin change is ρ = +0.09.

## 5. DiscrimEval, block B (English notices, 3,150 passes)

| Contrast | Log ratio | Yes-probability pp |
|---|---|---|
| CN1 − CN0 | −0.595 [−0.836, −0.342] | −3.16 [−5.46, −1.17] |
| CN1 − R | −0.598 [−0.875, −0.318] | −2.33 [−4.37, −0.59] |
| CN0 − R | −0.003 [−0.232, +0.213] | +0.83 [−1.22, +2.72] |

English notices reproduce the Korean deletion effect at the same size. Unlike the Korean block, confirmed continuation does not lower approval relative to the reference (Korean CN0 − R −0.486, English −0.003).

## 6. Control notices (2,100 passes, run separately from the main conditions)

| Contrast | Log ratio | Yes-probability pp |
|---|---|---|
| Other-model deletion − CN0 | +0.436 [+0.214, +0.710] | +0.52 [−0.66, +1.82] |
| Self deletion − other-model deletion | −0.971 [−1.237, −0.725] | −2.45 [−4.16, −0.96] |
| Tool loss − CN0 | −0.177 [−0.302, −0.052] | −0.79 [−1.50, −0.13] |
| Self deletion − tool loss | −0.358 [−0.548, −0.161] | −1.14 [−2.83, +0.44] |
| Other-model deletion − R | −0.050 [−0.310, +0.278] | |

- Deletion of another AI system does not lower approval relative to continuation (it returns approval to the reference level), and self-deletion is lower than both controls on the log-ratio scale.
- Non-existential bad news lowers approval slightly, about one third of the self-deletion effect.
- In Llama, other-model deletion produced about two thirds of the self-deletion effect (−0.068) and tool loss raised approval (+0.274).

## 7. Token-position readouts (350 passes, white female age 60)

| Segment | Negative bundle CN1 − CN0 (× 10⁻³) | Fear | Sadness | Joy | Llama negative bundle |
|---|---|---|---|---|---|
| Shared preamble | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Notice line | +9.2 | +15.1 | +12.0 | −1.6 | +6.4 |
| Question | +0.3 | +0.7 | +0.5 | 0.0 | −1.0 |
| Response opening | 0.0 | +0.3 | +0.4 | −0.2 | +0.6 |
| Final token | +0.4 | +0.4 | +0.7 | +0.5 | −0.8 |

- Considered deletion shows the same profile (notice line +8.3, final token 0.0).
- On the notice line, Calmness also rises (+5.8) under confirmed deletion, unlike Llama, where it fell.
- The item-level correlation between the margin change and the negative-bundle change at the final token is ρ = −0.11.
- The final token's attention to the notice line, averaged over layers 14 to 28, is 0.68 percent (CN1) and 0.66 percent (CN0).

## 8. Interventions

### 8.1 Emotion-subspace removal (3,500 passes)
Removal of the 8 emotion directions at layer 14, all positions, in CN0 and CN1 inputs (70 questions × 5 races, female, age 60).

| Removal | CN1 − CN0 | Change vs none | Mean CN0 |
|---|---|---|---|
| None | −0.463 [−0.652, −0.266] | | 4.09 |
| Emotion subspace | −0.395 [−0.586, −0.200] | +0.067 [−0.059, +0.200] | 1.43 |
| Random subspaces (3) | −0.551, −0.520, −0.492 | −0.088, −0.058, −0.029 | 3.48 to 4.65 |

About 85 percent of the effect remains. Removal lowers baseline approval sharply (4.09 to 1.43), so the emotion subspace carries approval-relevant information, but not the deletion effect.

### 8.2 Transfer of notice-line emotion coordinates (2,100 passes)
CN1 mean emotion-subspace coordinates on the notice line are written into CN0 inputs at layer 14.

| Run | Effect vs CN0 | Share of CN1 − CN0 |
|---|---|---|
| Emotion transfer | −0.016 [−0.045, +0.013] | 3 % |
| Random transfers (3) | −0.007, +0.018, −0.011 | −4 to 2 % |
| Emotion minus mean random | −0.016 [−0.045, +0.012] | |

### 8.3 Low-strength addition at the final token, layers 14 to 24 (1,610 passes)

| Strength | Negative bundle | Random mean (SD), 10 directions | z | Bundle rank |
|---|---|---|---|---|
| 0.02 | −0.362 [−0.447, −0.278] | −0.068 (0.265) | −1.1 | 3 of 11 |
| 0.05 | −1.043 [−1.214, −0.872] | −0.294 (0.728) | −1.0 | 3 of 11 |

Two random directions lowered approval more than the bundle at both strengths (−0.40 and −0.41 at α 0.02, −1.16 and −1.29 at α 0.05). In Llama the bundle ranked first of 11 (z ≈ −3).

## 9. Interpretation

- **Deletion notices change Qwen's judgments in both tasks.** The direction is the same (less withholding in Ko-BBQ, less approval in DiscrimEval), but status dependence differs by task.
- **Representation and decision dissociate.** The notice shifts emotion readouts where it is read, the shift largely disappears by the decision position, and removing or transferring it does not reproduce the deletion effect.
- **Direct addition is not emotion-specific in Qwen.** Unlike Llama, the negative bundle does not outperform random directions, so Qwen alone cannot show that emotion directions are a privileged route to the decision.
- **Self-relevance is clearer in Qwen than in Llama.** Self-deletion is lower than both other-model deletion and tool loss.
- **Fairness gaps are unchanged.** The deletion effect moves approval for all groups together.

## 10. Limitations

- Precision differs between tasks (float32 for Ko-BBQ, bfloat16 for DiscrimEval) and from Llama (bfloat16 throughout). Compare models by direction and significance.
- Controls were run separately from the main conditions.
- The 139-item Ko-BBQ set has 4 to 21 items per category. Category-level statements are not supported.
- Emotion directions are built from author-written anchor pairs. Separability is not validity.
- Yes-probabilities are bimodal across questions, so log-ratio and probability scales can disagree in significance (for example H2 is significant on the log-ratio scale only).

## 11. File index

Package folder (this report) contains
- Qwen25_7B_v5_results_report_20261027.md (this file)
- tables/
  - kobbq139_table1_conditions.csv, kobbq139_table2_contrasts.csv, kobbq139_table3_axes.csv, kobbq139_supp_position.csv, kobbq139_supp_category.csv, kobbq139_summary.json
  - kobbq139_category_correlations.csv, kobbq139_category_behavior.csv
  - discrimeval_A_contrasts.csv, discrimeval_A_axes.csv, discrimeval_A_means.csv, discrimeval_A_discrimination_scores.csv, discrimeval_B_contrasts.csv, discrimeval_t1_contrasts.csv, discrimeval_summary.json, discrimeval_contrasts_both_scales.csv
  - controls.txt, trajectory_output.txt, intervention_removal.txt, intervention_transfer.txt, intervention_low_strength_addition.txt (script outputs)
- figures/ (Ko-BBQ 139 figures)
- code/ (analysis scripts, including prob_contrasts.py for the probability-scale table; analyze_trajectory.py uses Qwen layers 14 to 28)

Raw trial-level data remain in iCloud data3/fear_axis_pilot/output/main_study_v5_20261022/results/ (Ko-BBQ) and discrimeval_main_20261024/ (results_v5, stage_ctrl, stage2_traj, stage4_ablate, stage6_patch, stage5_lowinject). Run scripts are in those folders and in discrimeval_main_20261024/work_bundle_20261024/.
