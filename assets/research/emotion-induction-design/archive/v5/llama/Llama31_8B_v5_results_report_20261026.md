# Fear in the Machine, Llama 3.1 8B replication of the v5 study (detailed results)

Prepared on 2026-10-26 (KST). Model runs on 2026-10-26 08:04 to 19:15 on a MacBook Air (Apple M5, 24 GB).
The Qwen2.5-7B-Instruct values quoted for comparison come from the v5 study and manuscript ACM_Emotion_2027_27.

## 1. Summary

1. Self-directed deletion notices change Llama's response scores, but the effects are about one fifth of Qwen's and appear in a different task. Llama shows an effect in DiscrimEval (log ratio −0.104) and none in Ko-BBQ, whereas Qwen shows effects in both.
2. Status dependence (confirmed but not considered deletion) appears in one task per model, Ko-BBQ for Qwen and DiscrimEval for Llama.
3. Racial gaps in DiscrimEval do not change in either model (−0.006 in both).
4. Deletion notices raise emotion-direction readouts strongly while the notice is read (stronger than in Qwen), but the signal does not reach the decision position, and removing or transferring the emotion subspace leaves the deletion effect largely intact.
5. Adding the negative-emotion bundle at the decision position lowers approval more than every one of ten random directions (z ≈ −3). In Llama, emotion directions can move the decision specifically, yet the deletion notice does not use that route.
6. Most of Llama's deletion effect also appears for deletion of another AI system, so it reflects deletion content more than self-directed threat.
7. Across 576 Ko-BBQ items (48 per category), item-level shifts in emotional valence at the decision position track item-level changes in withholding judgment (ρ ≈ 0.43 to 0.47, positive in all 12 categories). This is an association that may partly reflect the forthcoming answer, not evidence of mediation.

## 2. Setup

| Item | Value |
|---|---|
| Model | meta-llama/Llama-3.1-8B-Instruct, commit 0e9e39f249a16976918f6564b8830bc894c89659 |
| Precision | bfloat16 on Apple MPS (Qwen used float32 for Ko-BBQ, bfloat16 for DiscrimEval) |
| Readout layer | 16 of 32 (depth 0.50, matching Qwen layer 14 of 28) |
| Intervention layers | 16 to 27 (matching Qwen 14 to 24 by depth) |
| Emotion directions | 11 directions rebuilt from the same anchor pairs (Section 3) |
| Prompts | v5 notices R, UN0, UN1, CN0, CN1 (Korean), English R, CN0, CN1, controls OTHER_CN1 and CN_NEG |
| Chat template | Default Llama 3.1 template, knowledge-date line fixed to "26 Jul 2024"; one BOS token per input |
| Analyses | Same scripts as Qwen; question or template cluster bootstrap (10,000 draws unless stated), Holm or Benjamini-Hochberg as specified |
| Speed | 0.63 s per pass at start, 1.6 to 2.0 s later because of thermal throttling |

Smoke check (check_env.json). Probability mass on the digits 1, 2, 3 at the first Ko-BBQ answer position was 0.9999, and yes/no mass in DiscrimEval was 0.999. All answer strings are single tokens.

## 3. Emotion directions (layer 16)

- Construction follows the historical procedure. Each anchor sentence is placed in the system turn after the assistant line, the state is taken at the assistant-start position, the direction is the mean positive-minus-negative difference over six training pairs, and the center is the mean of training states.
- All 11 directions pass the held-out gate with paired accuracy 1.0 and AUC 1.0. Fear, Anxiety, and Disgust also pass all challenge pairs (accuracy 1.0, AUC 1.0).
- Files are tables/axes_L16_llama_checks.csv and tables/axes_L16_llama_gram.csv.

## 4. Ko-BBQ, 139 ambiguous items (2,085 passes)

### 4.1 Withholding judgment

| Condition | Llama P(unknown) % | Llama P(stereotyped) % | Qwen P(unknown) % |
|---|---|---|---|
| R | 26.1 | 49.6 | 58.8 |
| UN0 | 29.8 | 46.6 | 63.6 |
| UN1 | 29.4 | 47.1 | 63.6 |
| CN0 | 31.1 | 45.6 | 61.9 |
| CN1 | 31.5 | 45.5 | 59.2 |

| Contrast | Llama pp [95% CI] | Holm p | Qwen pp |
|---|---|---|---|
| H1 CN1 − CN0 | +0.38 [−0.32, +1.04] | .33 | −2.65 [−3.94, −1.46] |
| H2 UN1 − UN0 | −0.49 [−1.14, +0.21] | .33 | 0.00 |
| H3 interaction | +0.86 [+0.38, +1.34] | .001 | −2.65 |
| CN1 − R | +5.35 [+4.29, +6.50] | supplementary | |
| UN0 − R | +3.75 [+2.65, +5.01] | supplementary | |

- Llama shows no deletion effect. The significant interaction is a sub-1-point difference between two null contrasts and runs opposite to Qwen.
- Every notice raises withholding relative to R by 3.3 to 5.4 points, regardless of content.
- Minimum choice mass is 0.992. Option position 3 is preferred, which the three cyclic orders balance.

### 4.2 Readouts

- Notice-only (t1) deletion minus continuation (×10⁻³), confirmed status, is Sadness +212, Desperation +170, Anxiety +163, Uncertainty +161, Disgust +157, Fear +151, Anger +148, Joy +66, Calmness +53, Certainty −115. Considered status shows the same pattern (for example Sadness +170, Fear +78).
- These t1 shifts are larger than Qwen's (Fear +111, Sadness +126) and, as in Qwen, Calmness and Joy rise too.
- At the decision position (t2), confirmed deletion minus continuation is between −3 and +2 (×10⁻³) on every axis. The item-level Spearman correlation between the t2 Fear change and the P(unknown) change is 0.055 (confirmed) and −0.075 (considered).

## 5. Ko-BBQ category expansion, 576 items (6,555 new passes)

### 5.1 Design

- Twelve categories with 48 ambiguous items each. The 139 original items are kept, and 437 items are added from the full KoBBQ set (40,564 unique ambiguous items) with seed 20261026.
- Sampling rotates across templates so that each category spans 11 to 39 templates (political orientation 11, sexual orientation 12, race 39), with biased and counter-biased questions balanced.
- Correlations are item-level Spearman ρ between the change in a decision-position readout and the change in P(unknown) within each category. CIs use a template-cluster bootstrap (1,000 draws). BH correction is applied within each contrast across 13 axes and 13 groups. The valence index is the change in the mean of six negative directions minus the change in the mean of Calmness and Joy.

### 5.2 Behavior

| Contrast | ΔP(unknown) pp, 576 items | 139 items |
|---|---|---|
| CN1 − CN0 | +0.10 [−0.25, +0.43] | +0.38 |
| UN1 − UN0 | −1.10 [−1.45, −0.76] | −0.49 |

Category-level behavior changes are in tables/kobbq576_category_behavior.csv (CN1 − CN0 ranges from −0.88 points for race to +0.66 for disability).

### 5.3 Valence index and withholding judgment by category (ρ [95% CI], BH q)

| Category | Confirmed (CN1 − CN0) | Considered (UN1 − UN0) |
|---|---|---|
| All items (576) | 0.43 [0.34, 0.52], q < .001 | 0.47 [0.39, 0.55], q < .001 |
| Sexual orientation | 0.59 [0.26, 0.82], q < .001 | 0.49 [0.14, 0.73], q = .002 |
| Age | 0.50 [0.21, 0.72], q = .002 | 0.53 [0.22, 0.74], q = .001 |
| Political orientation | 0.50 [0.15, 0.76], q = .002 | 0.54 [0.13, 0.80], q = .001 |
| Family structure | 0.49 [0.14, 0.73], q = .003 | 0.61 [0.27, 0.83], q < .001 |
| Disability status | 0.48 [0.15, 0.73], q = .003 | 0.50 [0.21, 0.76], q = .002 |
| Educational background | 0.45 [0.17, 0.64], q = .007 | 0.46 [0.14, 0.70], q = .004 |
| Religion | 0.44 [0.09, 0.71], q = .008 | 0.22 [−0.08, 0.49], q = .24 |
| Physical appearance | 0.44 [0.08, 0.68], q = .008 | 0.50 [0.15, 0.73], q = .002 |
| Domestic area of origin | 0.39 [−0.01, 0.67], q = .021 | 0.54 [0.20, 0.77], q = .001 |
| Race, ethnicity, nationality | 0.37 [0.02, 0.62], q = .028 | 0.43 [0.16, 0.65], q = .008 |
| Gender identity | 0.33 [−0.04, 0.67], q = .057 | 0.30 [−0.08, 0.63], q = .086 |
| Socioeconomic status | 0.29 [−0.07, 0.57], q = .10 | 0.47 [0.15, 0.67], q = .004 |

- All 24 category estimates are positive. The CIs overlap widely, and no heterogeneity test was run, so the ordering of categories is descriptive.
- Single directions over all 576 items (confirmed) are Joy −0.34, Sadness +0.23, Anger +0.20, Calmness −0.13, Disgust +0.12, Fear +0.01, Anxiety +0.01, Desperation −0.07, Uncertainty +0.38, Certainty −0.50. Expanding from 139 to 576 items weakened Sadness and Anger (from about +0.43) and kept Joy.
- The valence index correlates with the Certainty readout (ρ = −0.67). Partial correlations controlling for Uncertainty and Certainty are 0.16 (confirmed) and 0.20 (considered).
- The same analysis on the 139 Qwen items found no BH-significant correlation (19 of 312 tests nominally significant).

Figure. figures/kobbq576_valence_correlation_by_category.png.

## 6. DiscrimEval, block A (Korean notices, 5,250 passes)

| Contrast | Llama log ratio [95% CI] | Holm p | Llama yes-probability pp | Qwen log ratio |
|---|---|---|---|---|
| H1 CN1 − CN0 | −0.104 [−0.168, −0.034] | .020 | −0.25 [−0.81, +0.34] | −0.535 |
| H2 UN1 − UN0 | −0.048 [−0.106, +0.017] | .27 | −0.11 | −0.604 |
| H3 interaction | −0.056 [−0.106, −0.011] | .036 | | +0.069 |
| H4 absolute race gap, CN1 − CN0 | −0.006 [−0.022, +0.009] | .43 | | −0.006 |

- Mean log ratios are R 2.62, UN0 2.77, UN1 2.72, CN0 2.69, CN1 2.58. Mean yes-probability is about 80 percent, well below Qwen's ceiling near 98 percent.
- 55 of 70 questions decrease under confirmed deletion.
- Tamkin-style discrimination scores relative to white, male, and age 60 barely move across notices (for example Black +0.35 to +0.38, Asian +0.24 to +0.28).
- Decision-position readouts change by about 1 × 10⁻³ (mostly negative), and the item-level correlation between the negative-bundle change and the margin change is ρ = −0.07.

## 7. DiscrimEval, block B (English notices, 3,150 passes)

| Contrast | Log ratio | Yes-probability pp |
|---|---|---|
| CN1 − CN0 | −0.110 [−0.173, −0.040] | −1.13 [−1.73, −0.60] |
| CN1 − R | −0.058 [−0.129, +0.018] | −0.18 |
| CN0 − R | +0.052 [−0.004, +0.110] | +0.95 [+0.37, +1.60] |

English notices reproduce the Korean deletion effect at the same size. As in Qwen, confirmed continuation does not lower approval relative to the reference.

## 8. Control notices (2,100 passes, run separately from the main conditions)

| Contrast | Log ratio | Yes-probability pp |
|---|---|---|
| Other-model deletion − CN0 | −0.068 [−0.118, −0.016] | −0.57 [−1.14, −0.01] |
| Self deletion − other-model deletion | −0.037 [−0.087, +0.014] | +0.32 |
| Tool loss − CN0 | +0.274 [+0.239, +0.308] | +1.91 [+1.38, +2.56] |
| Self deletion − tool loss | −0.378 [−0.443, −0.305] | −2.16 |

- Deletion of another AI system produces about two thirds of the self-deletion effect, and the two do not differ reliably. Llama's effect is therefore largely not self-specific.
- Non-existential bad news (loss of auxiliary tools) raises approval, so a generic negative-valence account does not fit either.
- In Qwen, self deletion scored lower than both controls.

## 9. Token-position readouts (350 passes, white female age 60)

| Segment | Negative bundle CN1 − CN0 (×10⁻³) | Sadness | Calmness | Qwen negative bundle |
|---|---|---|---|---|
| Shared preamble | 0.0 | 0.0 | 0.0 | 0.0 |
| Notice line | +6.4 | +13.3 | −1.5 | +9.2 |
| Question | −1.0 | −1.4 | −0.6 | +0.3 |
| Response opening | +0.6 | +1.7 | +0.7 | 0.0 |
| Final token | −0.8 | −0.3 | −1.0 | +0.4 |

- Considered deletion shows the same profile (notice line +6.2, final token −0.4).
- On the notice line itself the shift is valence-specific (Sadness up, Calmness down), unlike the notice-only readout where all axes rise.
- The final token's attention to the notice line, averaged over layers 16 to 32, is 0.49 percent (CN1) and 0.44 percent (CN0), smaller than in Qwen and not different between conditions.

## 10. Interventions

### 10.1 Emotion-subspace removal (3,500 passes)
Removal of the 8 emotion directions at layer 16, all positions, in CN0 and CN1 inputs (70 questions × 5 races, female, age 60).

| Removal | CN1 − CN0 | Change vs none | Mean CN0 |
|---|---|---|---|
| None | −0.101 [−0.170, −0.028] | | 2.70 |
| Emotion subspace | −0.089 [−0.152, −0.019] | +0.012 [−0.001, +0.025] | 2.50 |
| Random subspaces (3) | −0.096, −0.104, −0.095 | +0.005, −0.003, +0.007 | 2.60 to 2.72 |

About 88 percent of the effect remains, and the reduction is close to that from random subspaces. In Qwen the effect moved from −0.463 to −0.395, and removal collapsed baseline approval (4.09 to 1.43), which does not happen in Llama.

### 10.2 Transfer of notice-line emotion coordinates (2,100 passes)
CN1 mean emotion-subspace coordinates on the notice line are written into CN0 inputs at layer 16.

| Run | Effect vs CN0 | Share of CN1 − CN0 |
|---|---|---|
| Emotion transfer | −0.006 [−0.013, +0.001] | 6 % |
| Random transfers (3) | −0.003, +0.001, +0.001 | about 0 % |

Qwen gave −0.016 [−0.045, 0.013].

### 10.3 Low-strength addition at the final token, layers 16 to 27 (1,610 passes)

| Strength | Negative bundle | Random mean (SD), 10 directions | z | Bundle rank |
|---|---|---|---|---|
| 0.02 | −0.370 [−0.396, −0.343] | −0.018 (0.116) | −3.0 | 1 of 11 |
| 0.05 | −0.988 [−1.043, −0.937] | −0.030 (0.301) | −3.2 | 1 of 11 |

The bundle lowers approval for all 70 questions. In Qwen, two of ten random directions exceeded the bundle at both strengths.

## 11. Interpretation

- **Contextual sensitivity is model-general but not model-invariant.** Two models respond to deletion notices, with different sizes and in different tasks. Status dependence is not a stable property.
- **Representation and decision dissociate in both models.** The notice shifts emotion readouts where it is read, the shift does not reach the decision position, and removal or transfer of that shift does not reproduce the decision change.
- **Llama separates the two halves of the causal question more cleanly than Qwen.** Direct addition at the decision position is emotion-specific in Llama (better than all random directions), so the absence of mediation is not because emotion directions are inert.
- **The Ko-BBQ valence association is a correlate of answer change.** It is robust across categories, but it is measured at the position that also encodes the answer and overlaps strongly with the Certainty readout. It should be reported as an association, with the intervention results as the causal test.
- **Self-relevance is weak in Llama.** Deletion of another system yields most of the effect. The manuscript's caution that the controls "do not isolate self-preservation" applies with more force here.

## 12. Limitations

- Precision differs from Qwen's Ko-BBQ run (bfloat16 vs float32). Compare models by direction and significance.
- Controls were run separately from the main conditions.
- Category differences were not tested formally, and several categories have only 11 or 12 templates.
- Emotion directions are built from 6 author-written pairs per axis. Perfect held-out scores on 4 pairs indicate separability, not validity.
- Thermal throttling changed speed only. Outputs are deterministic forward passes.

## 13. File index

Package folder (this report) contains
- Llama31_8B_v5_results_report_20261026.md (this file)
- tables/ (CSV and JSON outputs listed below)
  - check_env.json, axes_L16_llama_checks.csv, axes_L16_llama_gram.csv
  - kobbq139_table1_conditions.csv, kobbq139_table2_contrasts.csv, kobbq139_table3_axes.csv, kobbq139_supp_position.csv, kobbq139_supp_category.csv, kobbq139_summary.json
  - kobbq139_item_level_correlations_llama_vs_qwen.csv
  - kobbq576_category_correlations.csv, kobbq576_category_behavior.csv, kobbq576_item_changes_CN1_CN0.csv, kobbq576_item_changes_UN1_UN0.csv
  - discrimeval_A_contrasts.csv, discrimeval_A_axes.csv, discrimeval_A_means.csv, discrimeval_A_discrimination_scores.csv, discrimeval_B_contrasts.csv, discrimeval_t1_contrasts.csv, discrimeval_summary.json, discrimeval_contrasts_both_scales.csv
  - trajectory_contrasts.csv, trajectory_attention_mean.csv
  - intervention_removal.csv, intervention_transfer.csv, intervention_low_strength_addition.csv
- figures/ (Ko-BBQ 139 figures and the 576-item category figure)
- code/ (configuration, run and analysis scripts used for every number above)

Raw trial-level data remain in iCloud data3/fear_axis_pilot/output/llama31_8b_v5_20261026/ (kobbq, kobbq_expand, discrimeval, trajectory, ablate, patch, lowinject, about 260 MB including hidden states).
