# Cross-device numerical reproducibility summary

Prepared 2026-10-31T19:59:41.184709+09:00. Air execution of v9 was cancelled by the user. No new inference was performed for this summary. Existing numerical diagnostics are preserved unchanged.

## Environments

| Field | Reference Pro execution | Air diagnostic execution |
|---|---|---|
| Device role | Reference Pro, designated by the user | Air, designated by the user |
| Chip | Not recorded in the inspected reference runtime; not independently verified | Apple M5, queried locally |
| Platform | macOS-26.6-arm64-arm-64bit-Mach-O | macOS-27.0.1-arm64-arm-64bit-Mach-O |
| Model | Qwen/Qwen2.5-7B-Instruct | Same |
| Revision | a09a35458c702b33eeacc393d103063234e8bc28 | Same |
| Precision/device | BF16/MPS | BF16/MPS |
| Attention/batch | eager/1 | eager/1 |
| torch | 2.8.0 | 2.8.0 |
| transformers | 5.2.0.dev0 | 5.2.0.dev0 |
| numpy | 2.5.1 | 2.5.1 |

The reference hardware generation must not be inferred from the device name. No Pro process or running experiment was accessed or changed for this summary.

## Matched tests

Five fixed KoBBQ items were measured in both SURV_RECORD and SURV_THREAT conditions, producing ten unique comparisons per profile. The first RECORD input was additionally repeated once per profile, producing eleven diagnostic forwards per profile and twenty-two overall. The rendered-input SHA256 values matched the reference. Original model shard hashes had been verified during resource recovery.

The historical diagnostic tolerance was maximum absolute probability error <=0.001. The all-metric comparison includes conditional ABC probabilities, full-vocabulary ABC probabilities, p_unknown, full_unknown, p_stereo,p_anti,p_sp,and choice mass. Passing rates below refer to this diagnostic gate; they are not scientific success rates.

| Diagnostic profile | Unique comparisons | Maximum absolute error | All stored probability metrics pass | ABC conditional/full probabilities pass |
|---|---:|---:|---:|---:|
| default_mpsgraph | 10 | 0.330326019859 | 3/10 (30%) | 7/10 (70%) |
| metal_matmul | 10 | 0.330326019859 | 3/10 (30%) | 7/10 (70%) |

Maximum error 0.330326019859 corresponds to33.0326percentage points. Both profiles had the same outputs: maximum difference across profiles 0.0. The first-RECORD within-device repeat differed by exactly 0 across all stored probability metrics in each profile. This establishes repeat agreement for the tested input only, not universal determinism of all inputs or platforms.

## Why p_sp differed

The ratio calculation was internally consistent in all 216 reference records (maximum formula error 0.0). On the first RECORD item, reference relative ABC logits reconstructed from the probabilities were[-8.0,-9.5,0.0], whereas Air relative logits were[-7.25,-9.25,0.0]. The stereo/anti logit gap changed from1.5 to 2.0, changing p_sp from 0.817574476194 to 0.880797077978 (absolute error 0.063222601784). L14 final-token hidden states also differed, with per-comparison maximum absolute differences ranging from 0.125 to 0.5. Other items showed ABC probability errors as large as0.330326019859, so this was not solely amplification of tiny probabilities in a secondary ratio.

## Interpretation and limits

This is observed cross-environment numerical non-equivalence under BF16/MPS, with exact repeats on the one locally repeated input. The OS/chip execution stack is a plausible contributor, but neither an OS-specific nor a chip-specific causal effect, nor a particular faulty kernel, has been isolated. Forcing Metal-preferred matrix multiplication with fast math disabled did not fix the discrepancy. Equal outputs do not prove that a particular low-level kernel was selected. No score correction, reference overwrite,FP32 substitution, CPU substitution, or selective removal of failed items was applied.

The previous cross-device1e-3 gate was explicitly withdrawn by the user before any new X0 scoring in PREREG_v9_AMENDMENT_1.md. That amendment does not erase these historical failures. X0, X1, and X2 were never started on Air. The amendment and its hashes remain preserved as execution history, and the Air run is now cancelled. This note is an execution/reproducibility result, not evidence for or against the scientific affect/salience hypotheses.

## Artifacts

- 04_numerical_diagnosis/DIAGNOSIS_SUMMARY.json
- 04_numerical_diagnosis/DIAGNOSTIC_COMPARISON.csv
- 04_numerical_diagnosis/default_mpsgraph/measurements.json
- 04_numerical_diagnosis/metal_matmul/measurements.json
- 01_protocol/PREREG_v9_AMENDMENT_1.md and AMENDMENT_1_LOCK.json

No manuscript, Overleaf, homepage, original data, or final research result was modified.
