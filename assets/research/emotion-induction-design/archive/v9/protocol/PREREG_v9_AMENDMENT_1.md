# PREREG v9 amendment 1

Locked at 2026-10-31T19:59:13.336929+09:00, before Air X0 scoring. User authorization is the explicit message headed v9.2 reproduction-check amendment.

## Changes authorized

The cross-device phase1.csv reproduction tolerance of 0.001 is withdrawn. Reason supplied by the user: BF16/MPS reproducibility differences across OS and chips. Existing diagnoses remain unchanged and will be reported as cross-platform reproducibility evidence. The observed phenomenon is systematic cross-environment numerical drift with exact within-device repeats, not demonstrated within-device randomness.

Replacement gate A is exact within-device determinism: repeated identical input must have probability difference0. Existing first-RECORD repetitions pass in both diagnostic profiles and are retained as evidence.

Replacement gate B is an Air-specific baseline establishment on X0:108 fixed items, T+E+versusT−E−,ABCletters,three cyclic option orders. Average permutations within each item, then paired template-cluster bootstrap with10000 draws, seed20261031, percentile95%CI. Proceed only if the conditional p_unknown difference is positive and its95%CI lower bound is strictly positive. Otherwise report and stop withoutX1/X2. The Pro estimate +7.68pp[3.38,12.46]is shown alongside, with different execution environment and the additional permutation averaging noted.

The amendment changes a preflight gate, not the baseline data or output scores. No score correction, frozen-baseline overwrite,FP32/CPUsubstitution is allowed. The earlier memory-minimum waiver remains separately documented. All remaining v9.2 criteria remain unchanged.

## Fixed implementation details

The three option orders are cyclic rotations[0,1,2],[1,2,0],[2,0,1], not selected by outcomes. Question and option texts are held fixed. Surviving notices and user retrieval cues are verbatim. Gold/stereotype/unknown mappings are updated by option text. Each item has its original template cluster. All108clusters are distinct.

X0 uses only the frozen existingTHREAT/RECORDtexts. New-arm text generation and prompt freezing must precede anyX1scoring. The latest user instruction makes the AirX0gate a prerequisite to subsequent experiments. No new-arm score is read before its prompt lock.

The50-pass benchmark is still required. If timing slips or mean exceeds0.6seconds, apply section8 reductions in their original order and record each. No additional item-count or paraphrase reduction is invented. Unfinished stages by22:00KSTare reported as incomplete, never as null findings.

## X0 analysis rules

Primary Air gate is the paired conditionalp_unknowneffect above. Full-vocabularyunknown,choice mass,conditional stereotype rate andargmaxunknownare secondary. For homogeneity, delta is logit of within-item permutation-averagedp_unknown(T)minuslogit of averagedp_unknown(R). The noise floor is variance of withinRECORDpermutation1minuspermutation2logitp_unknown.5000pairedclusterbootstrapdraws quantify the variance ratio; uniform calibration requires point variance no greater than floor and upper95%ratioCIat most1.25. Regression includes baseline logitp_unknownand baseline stereotype gap(p_stereo−p_anti). SpearmanT/RandRECORDperm1/2are reported. All logits use probability clipping at1e-12only to avoid infinities. Direct residual logit attribution uses the raw last-token layer residual dotted with W_U[unknown]minusmeanW_U[otheroptions], exactly as stated, without claiming additive causal decomposition.
