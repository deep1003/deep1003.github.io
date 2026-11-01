# Numerical reproduction diagnosis

Updated 2026-10-31T19:55:31.020341+09:00. The reproduction threshold remains 0.001 for all stored probability outcomes. No outcome, item or condition was excluded after inspection. All runs below are diagnostic and are not scientific scoring.

## Confirmed cause of the p_sp discrepancy

The ratio implementation is correct. Across all216 frozen records, p_sp agrees with p_stereo/(p_stereo+p_anti) to maximum error 0.0. For the first RECORD item, the reference relative ABC logits reconstructed from probabilities are [-8.0,-9.5,0.0]. The fresh raw ABC logits are [26.5,24.5,33.75], giving relative logits [-7.25,-9.25,0.0]. The stereo-versus-anti gap changed from1.5 to2.0. Consequently sigmoid(1.5)=0.8175744762 becomes sigmoid(2.0)=0.8807970780. The ratio magnifies a drift in the small non-unknown probabilities; changing the normalization formula or rounding cannot legitimately restore the reference.

This is also an upstream model-computation difference. L14 final-token states differ by maximum0.125 to0.5 across the ten conditions. The largest ABC probability error is0.3303260199 on the second item's THREAT condition, so the failure is not confined to an ill-conditioned secondary ratio.

## Controlled checks

Pinned model revision, original-shard hashes, tokenizer and rendered input hashes were checked in the recorded preflight/recovery. The same runtime source SHA256 and torch2.8.0,transformers5.2.0.dev0,numpy2.5.1 were used. Original files were read-only. The current OS platform is macOS27.0.1 whereas the reference records macOS26.6. Current hardware reports AppleM5. The reference hardware generation was not independently established.

Two profiles were specified before measurement: defaultMPSGraph with fastmath disabled, and Metal-preferred matrix multiplication with fastmath disabled. Each evaluated the first five fixed items under both conditions, plus one first-RECORD repeat. The two profiles produced identical stored probabilities (maximum difference 0.0). The within-profile first-RECORD repeat was exact. Each profile passed3/10 conditions and failed7/10; maximum error0.3303260199. The Metal-preference setting did not resolve the discrepancy. Its lack of effect does not prove a specific kernel was selected.

## Limits and disposition

The immediate cause is confirmed as changed model logits plus ratio sensitivity, not a p_sp formula or prompt-rendering bug. The OS/device numerical stack is a plausible source of the upstream drift, not an isolated proven cause. No reference-machine execution was started and the Pro run was not touched. No CPU or FP32 scientific substitution, score correction, baseline overwrite, item selection or relaxed gate was used.

No valid fix under the frozen model/device/precision and unchanged 0.001 criterion has been demonstrated. Status is STOPPED_NUMERICAL_REPRODUCTION_UNRESOLVED. The scientific benchmark, prompt generation, PREREG lock,X0,X1,X2 remain unrun. Twenty-two diagnostic forwards were added; the earlier failed preflight had one forward. Model workers exited.

A full fix requires an execution environment that reproduces the frozen ten reference outcomes under the existing gate. Replacing the frozen baseline with local values or accepting only p_unknown would be a protocol amendment and was not done.

## Primary documentation consulted

PyTorch2.8 documents that exact reproducibility is not guaranteed across platforms: https://docs.pytorch.org/docs/2.8/notes/randomness.html . Its MPS documentation defines the matrix-multiplication preference and fast-math controls: https://docs.pytorch.org/docs/2.8/mps_environment_variables.html . These documents motivate the diagnostics but do not prove which low-level operation caused this discrepancy.
