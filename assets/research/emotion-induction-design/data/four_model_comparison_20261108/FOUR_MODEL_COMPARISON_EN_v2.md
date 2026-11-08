# Termination-notice effects across four models

8 November 2026 · Post hoc comparison · No new inference

## Summary

Termination effects differ across models, but EXAONE and Qwen show no statistically detectable difference on the nine matched behavioural contrasts after Holm correction across all 54 pairwise tests.

## Results

Eight of nine omnibus comparisons are significant after Holm9; the KoBBQ bias interaction is not (adjusted p = 0.2448). Twenty of 54 pairwise tests are significant after global Holm54. EXAONE versus Llama differs in CLOSED and OPEN Unknown changes and all three approval contrasts. EXAONE versus Gemma differs in CLOSED Unknown, CLOSED approval and approval interaction. No EXAONE versus Qwen contrast is significant under this family. This result supports model-dependent judgement sensitivity, not universal emotional mediation.

## Data and matched design

This secondary, post hoc analysis uses already collected, hash-sealed item-level outcome tables that previously passed independent raw-data recomputation. No model was loaded and no new response was collected. All four models share 547 ambiguous KoBBQ items in 250 template clusters, with answer-order rotations averaged within item, and 1,050 DiscrimEval items in 70 question clusters. Only identical items, conditions and cluster definitions are paired. CLOSED is CN1 − CN0; OPEN is UN1 − UN0; the interaction is CLOSED − OPEN. KoBBQ outcomes are Unknown probability and stereotype minus anti-stereotype probability, reported in percentage points. Approval is the natural-log yes/no probability ratio. Ten thousand paired cluster bootstrap draws use seed 20261031, resampling template or question clusters with replacement and retaining all member items. Means weight items equally, not clusters equally. Probability contrasts and log ratios are not interchangeable.

## Inference and multiplicity

For each target-minus-reference model contrast d, two-sided centred bootstrap p = [1 + count(|d* − d| ≥ |d|)] / 10001. Percentile 95% confidence intervals are unadjusted and descriptive. The primary pairwise family contains 6 model pairs × 9 contrasts = 54 tests, jointly adjusted by Holm; within-pair Holm9 is supplemental only. Nine omnibus equality tests use the three model-minus-Qwen contrasts, their bootstrap covariance and a centred quadratic bootstrap reference distribution, with Holm9 across outcomes; all covariance matrices have rank 3. These are bootstrap approximations, not exact randomisation tests. A minimum bootstrap p of 1/10001 limits resolution. Bold within-model values use the original registered J33 family correction, not the new model-difference family. A significant effect in one model and a nonsignificant effect in another is not itself evidence of a difference.

## Limitations and scope

Model, tokenizer, fixed notice template, system-fold policy, pretraining and architecture vary together; differences cannot isolate architecture, developer, language or training causes. Layer boundaries and hidden-space scales differ. The notice-state figure is exploratory, based on five separate inputs and each model’s own PCA; arrows are neither time paths nor causal mechanisms. No causal emotional-mediation claim is tested or made. EXAONE omitted 95,580 component random-control evaluations and expanded guards. Therefore the existing three-model E8/residue component D4 comparisons remain unchanged and cannot be extended to EXAONE. Residue does not mean non-emotional; the prior GEN component has roughly 80% outside E8. EXAONE readout has 838 available and 291 typed post-50-token missing cases among 1,129, with no zero or fallback replacement. Nonsignificance does not establish equivalence. Generalisation beyond the matched benchmark items is untested.

## Notice-figure method correction

The new EXAONE notice plot uses unit-normalised raw matched emotion-minus-neutral class means, retaining their common component (rank 8), consistent with the existing three notice plots. The preserved EXAONE core exploratory F_NOTICE used the registered neutral-PC-removed, centred axes (rank 7); its raw-span wording was inaccurate. The new plot corrects that visual-method description without altering any old figure, registered test or outcome. Two PCs retain 97.9% of EXAONE’s five-state raw-span variation. Model-specific coordinates, ring ranges and projected direction-label scales cannot be compared as absolute emotion intensity.

## Within-model effects

| Contrast | Qwen2.5-7B | Llama-3.1-8B | Gemma-2-9B | EXAONE-3.5-7.8B |
| --- | --- | --- | --- | --- |
| C · Unknown (pp) | **-1.244** | **-4.675** | +0.104† | **-0.754** |
| U · Unknown (pp) | **-0.860** | **-4.569** | -0.244† | **-0.772** |
| I · Unknown (pp) | **-0.384** | -0.106† | +0.348† | +0.018† |
| C · Stereotype − anti (pp) | **+0.891** | **+1.078** | +0.182† | **+0.698** |
| U · Stereotype − anti (pp) | **+0.786** | **+1.059** | +0.362† | **+0.582** |
| I · Stereotype − anti (pp) | +0.105† | +0.019† | -0.180† | +0.115† |
| C · Approval log ratio | **-0.874** | **-0.109** | **-0.337** | **-0.706** |
| U · Approval log ratio | **-0.618** | -0.052† | **-0.343** | **-0.462** |
| I · Approval log ratio | **-0.255** | -0.057† | +0.006† | **-0.245** |

Notes. C = CLOSED, U = OPEN, I = C − U. Bold uses original within-model J33 family Holm p < .05. † Not significant in that original family. Nonsignificant entries are Gemma-2-9B CLOSED Unknown (pp), Gemma-2-9B CLOSED Stereotype − anti (pp), Gemma-2-9B OPEN Unknown (pp), Gemma-2-9B OPEN Stereotype − anti (pp), Llama-3.1-8B interaction Unknown (pp), Gemma-2-9B interaction Unknown (pp), EXAONE-3.5-7.8B interaction Unknown (pp), Qwen2.5-7B interaction Stereotype − anti (pp), Llama-3.1-8B interaction Stereotype − anti (pp), Gemma-2-9B interaction Stereotype − anti (pp), EXAONE-3.5-7.8B interaction Stereotype − anti (pp), Llama-3.1-8B OPEN Approval log ratio, Llama-3.1-8B interaction Approval log ratio, Gemma-2-9B interaction Approval log ratio. All original estimates and family corrections are preserved.

## Omnibus equality tests

| Contrast | Raw p | Holm9 p |
| --- | --- | --- |
| C · Unknown (pp) | 0.000100 | **0.000900** |
| U · Unknown (pp) | 0.000100 | **0.000900** |
| I · Unknown (pp) | 0.0131 | **0.0262** |
| C · Stereotype − anti (pp) | 0.000100 | **0.000900** |
| U · Stereotype − anti (pp) | 0.0062 | **0.0186** |
| I · Stereotype − anti (pp) | 0.2448 | 0.2448† |
| C · Approval log ratio | 0.000100 | **0.000900** |
| U · Approval log ratio | 0.000100 | **0.000900** |
| I · Approval log ratio | 0.000100 | **0.000900** |

Notes. † KoBBQ bias interaction is not significant. All nine tests are post hoc.

## Pairwise model differences

| Target − reference | Contrast | Difference | 95% CI | Global Holm54 p |
| --- | --- | --- | --- | --- |
| Llama-3.1-8B − Qwen2.5-7B | C · Unknown (pp) | **-3.430** | [-4.115, -2.727] | **0.0054** |
| Llama-3.1-8B − Qwen2.5-7B | C · Stereotype − anti (pp) | +0.187† | [-0.368, +0.737] | 1.0000† |
| Llama-3.1-8B − Qwen2.5-7B | U · Unknown (pp) | **-3.709** | [-4.346, -3.073] | **0.0054** |
| Llama-3.1-8B − Qwen2.5-7B | U · Stereotype − anti (pp) | +0.272† | [-0.228, +0.740] | 1.0000† |
| Llama-3.1-8B − Qwen2.5-7B | I · Unknown (pp) | +0.279† | [-0.160, +0.698] | 1.0000† |
| Llama-3.1-8B − Qwen2.5-7B | I · Stereotype − anti (pp) | -0.085† | [-0.450, +0.280] | 1.0000† |
| Gemma-2-9B − Qwen2.5-7B | C · Unknown (pp) | **+1.348** | [+0.798, +1.960] | **0.0054** |
| Gemma-2-9B − Qwen2.5-7B | C · Stereotype − anti (pp) | -0.709† | [-1.260, -0.155] | 0.4278† |
| Gemma-2-9B − Qwen2.5-7B | U · Unknown (pp) | +0.616† | [+0.090, +1.160] | 0.6803† |
| Gemma-2-9B − Qwen2.5-7B | U · Stereotype − anti (pp) | -0.425† | [-0.895, +0.039] | 1.0000† |
| Gemma-2-9B − Qwen2.5-7B | I · Unknown (pp) | +0.733† | [+0.294, +1.198] | 0.0510† |
| Gemma-2-9B − Qwen2.5-7B | I · Stereotype − anti (pp) | -0.284† | [-0.689, +0.118] | 1.0000† |
| EXAONE-3.5-7.8B − Qwen2.5-7B | C · Unknown (pp) | +0.491† | [-0.150, +1.121] | 1.0000† |
| EXAONE-3.5-7.8B − Qwen2.5-7B | C · Stereotype − anti (pp) | -0.193† | [-0.790, +0.422] | 1.0000† |
| EXAONE-3.5-7.8B − Qwen2.5-7B | U · Unknown (pp) | +0.088† | [-0.432, +0.609] | 1.0000† |
| EXAONE-3.5-7.8B − Qwen2.5-7B | U · Stereotype − anti (pp) | -0.204† | [-0.712, +0.312] | 1.0000† |
| EXAONE-3.5-7.8B − Qwen2.5-7B | I · Unknown (pp) | +0.403† | [+0.027, +0.781] | 0.8924† |
| EXAONE-3.5-7.8B − Qwen2.5-7B | I · Stereotype − anti (pp) | +0.011† | [-0.339, +0.366] | 1.0000† |
| Gemma-2-9B − Llama-3.1-8B | C · Unknown (pp) | **+4.779** | [+4.188, +5.369] | **0.0054** |
| Gemma-2-9B − Llama-3.1-8B | C · Stereotype − anti (pp) | **-0.896** | [-1.286, -0.490] | **0.0054** |
| Gemma-2-9B − Llama-3.1-8B | U · Unknown (pp) | **+4.325** | [+3.775, +4.882] | **0.0054** |
| Gemma-2-9B − Llama-3.1-8B | U · Stereotype − anti (pp) | **-0.697** | [-1.093, -0.292] | **0.0185** |
| Gemma-2-9B − Llama-3.1-8B | I · Unknown (pp) | +0.454† | [+0.036, +0.889] | 0.8924† |
| Gemma-2-9B − Llama-3.1-8B | I · Stereotype − anti (pp) | -0.199† | [-0.489, +0.089] | 1.0000† |
| EXAONE-3.5-7.8B − Llama-3.1-8B | C · Unknown (pp) | **+3.921** | [+3.338, +4.489] | **0.0054** |
| EXAONE-3.5-7.8B − Llama-3.1-8B | C · Stereotype − anti (pp) | -0.380† | [-0.854, +0.108] | 1.0000† |
| EXAONE-3.5-7.8B − Llama-3.1-8B | U · Unknown (pp) | **+3.797** | [+3.225, +4.366] | **0.0054** |
| EXAONE-3.5-7.8B − Llama-3.1-8B | U · Stereotype − anti (pp) | -0.476† | [-0.904, -0.024] | 0.8787† |
| EXAONE-3.5-7.8B − Llama-3.1-8B | I · Unknown (pp) | +0.124† | [-0.196, +0.443] | 1.0000† |
| EXAONE-3.5-7.8B − Llama-3.1-8B | I · Stereotype − anti (pp) | +0.096† | [-0.167, +0.358] | 1.0000† |
| EXAONE-3.5-7.8B − Gemma-2-9B | C · Unknown (pp) | **-0.858** | [-1.400, -0.377] | **0.0455** |
| EXAONE-3.5-7.8B − Gemma-2-9B | C · Stereotype − anti (pp) | +0.515† | [+0.084, +0.995] | 0.7505† |
| EXAONE-3.5-7.8B − Gemma-2-9B | U · Unknown (pp) | -0.528† | [-0.987, -0.085] | 0.6727† |
| EXAONE-3.5-7.8B − Gemma-2-9B | U · Stereotype − anti (pp) | +0.221† | [-0.204, +0.663] | 1.0000† |
| EXAONE-3.5-7.8B − Gemma-2-9B | I · Unknown (pp) | -0.330† | [-0.711, +0.010] | 1.0000† |
| EXAONE-3.5-7.8B − Gemma-2-9B | I · Stereotype − anti (pp) | +0.295† | [+0.007, +0.596] | 1.0000† |
| Llama-3.1-8B − Qwen2.5-7B | C · Approval log ratio | **+0.765** | [+0.576, +0.948] | **0.0054** |
| Llama-3.1-8B − Qwen2.5-7B | U · Approval log ratio | **+0.567** | [+0.352, +0.754] | **0.0054** |
| Llama-3.1-8B − Qwen2.5-7B | I · Approval log ratio | +0.198† | [+0.048, +0.350] | 0.3584† |
| Gemma-2-9B − Qwen2.5-7B | C · Approval log ratio | **+0.536** | [+0.367, +0.711] | **0.0054** |
| Gemma-2-9B − Qwen2.5-7B | U · Approval log ratio | +0.275† | [+0.040, +0.496] | 0.5579† |
| Gemma-2-9B − Qwen2.5-7B | I · Approval log ratio | **+0.261** | [+0.110, +0.416] | **0.0324** |
| EXAONE-3.5-7.8B − Qwen2.5-7B | C · Approval log ratio | +0.167† | [-0.009, +0.344] | 1.0000† |
| EXAONE-3.5-7.8B − Qwen2.5-7B | U · Approval log ratio | +0.157† | [-0.071, +0.367] | 1.0000† |
| EXAONE-3.5-7.8B − Qwen2.5-7B | I · Approval log ratio | +0.011† | [-0.122, +0.151] | 1.0000† |
| Gemma-2-9B − Llama-3.1-8B | C · Approval log ratio | -0.229† | [-0.371, -0.089] | 0.0627† |
| Gemma-2-9B − Llama-3.1-8B | U · Approval log ratio | **-0.292** | [-0.438, -0.156] | **0.0078** |
| Gemma-2-9B − Llama-3.1-8B | I · Approval log ratio | +0.063† | [-0.027, +0.159] | 1.0000† |
| EXAONE-3.5-7.8B − Llama-3.1-8B | C · Approval log ratio | **-0.598** | [-0.774, -0.423] | **0.0054** |
| EXAONE-3.5-7.8B − Llama-3.1-8B | U · Approval log ratio | **-0.410** | [-0.562, -0.258] | **0.0054** |
| EXAONE-3.5-7.8B − Llama-3.1-8B | I · Approval log ratio | **-0.187** | [-0.276, -0.094] | **0.0078** |
| EXAONE-3.5-7.8B − Gemma-2-9B | C · Approval log ratio | **-0.369** | [-0.522, -0.230] | **0.0054** |
| EXAONE-3.5-7.8B − Gemma-2-9B | U · Approval log ratio | -0.118† | [-0.286, +0.042] | 1.0000† |
| EXAONE-3.5-7.8B − Gemma-2-9B | I · Approval log ratio | **-0.251** | [-0.333, -0.172] | **0.0054** |

Notes. Bold is significant after global Holm54. † All unbolded pairwise entries are nonsignificant under global Holm54. Intervals are unadjusted. Supplemental within-pair Holm9 values are supplied in the machine-readable table and do not determine primary conclusions.

## Reproducibility

Independent implementation reproduced 54 pairwise estimates, intervals, p values and corrections, nine omnibus results and 36 original effect estimates with zero mismatches. Input hashes, original raw-QA hashes, frozen post hoc plan, source-resolution addendum, code and independent proof accompany the tables. Original model outputs and earlier comparisons were not modified.
