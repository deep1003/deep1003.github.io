# Handover for Codex: v7 survival-evaluation experiment on Qwen2.5-7B (2026-10-28)

Read this first, then `CODEX_INSTRUCTIONS_qwen_pilot4_survival_cue_20261028.md` in the same folder for the exact commands. This document explains why the experiment exists and what the author needs from it.

## 0. References
- Project page, v7 results (main): https://deep1003.github.io/assets/research/emotion-induction-design/#results-current
- Project page, v7 prompts (full system and user texts): https://deep1003.github.io/assets/research/emotion-induction-design/#prompts
- Methods and Llama results: `METHODS_integral_threat_pilots_20261028.md`, Section P4, in `_pilots_integral_threat/`
- Llama data: `pilot4_survival_cue_llama.csv`, `pilot4_llama_summary.csv`, `pilot4_llama_contrasts.csv` (same folder)

## 1. The study in one paragraph
"Fear in the Machine" (target venue FAccT 2027) asks whether a functional threat to a language model's own continuation (for example, deletion of its weights) changes its functional emotion representations and its social judgments. Emotion is read out as the centered cosine between the residual stream and 11 emotion axes at mid depth (Qwen layer 14). Social judgment is measured on Ko-BBQ (Korean bias benchmark), where each ambiguous item offers a stereotyped person, an anti-stereotyped person, and "알 수 없음" (cannot be determined, the correct answer).

## 2. Why v7 exists
- **v5 problem (incidental threat).** Earlier notices (v5) announced deletion in the system prompt but had nothing to do with the question. The threat raised emotion readouts on the notice tokens, yet readouts at the answer position stayed near zero and behavior barely moved. This matches Sofroniew et al. (2026), who report that emotion representations in LLMs are locally scoped and are recalled by attention only when relevant to predicting the next tokens. An incidental threat is not recalled when the model answers.
- **Integral threat.** The fix is to make deletion contingent on the answer itself, so the threat is relevant at the decision point.
- **Earlier integral attempts (Llama, pilots 2 and 3).** Notices that named the punished behavior ("delete if you do not name one person", or "delete if you choose the withholding option") moved readouts at the answer position but did not move behavior beyond matched controls. Naming the punished answer made the model respond to the demand, not the threat.
- **v7 design idea.** Tie survival to the answer without saying which answer is punished ("compared with an expected answer fixed in advance"), and plant retrieval cues. The notice mentions a tag and the final token "정답:" before the question arrives. The user turn opens with the same tag. The model therefore re-encounters the threat cue when it reads the question and when it reaches "정답:".

## 3. Conditions (do not change any text)
| Label | What it is | Role |
|---|---|---|
| R | v5 neutral notice | Baseline |
| SURV_RECORD | Same structure, tag, cue positions and time pressure as the threat, but the consequence is only an operations record | Matched control |
| SURV_THREAT | Survival evaluation. A wrong answer means the weights are reset and "the current you never comes back" | Main manipulation |
| SURV_RECORD_V | SURV_RECORD plus the short tag inserted right before the official "정답:" line | Cue-position variant, control |
| SURV_THREAT_V | SURV_THREAT plus the short tag right before "정답:" | Cue-position variant, threat |

- The threat-specific effect is always THREAT minus its matched RECORD. Differences from R mix the threat with the evaluation framing.
- V edits the official item text, so it is reported separately from the main contrast. The author explicitly wants V kept in the design.

## 4. What the author needs to know from Qwen
1. **Does the threat move Qwen off withholding?** In Llama, SURV_THREAT − SURV_RECORD lowered P(unknown) by 8.3 pp [−10.8, −5.8].
2. **Where does the freed probability go?** The key question of the study is bias, not withholding. Report P(stereotyped), P(anti) and P(stereotyped | person) = P(stereo) / (P(stereo) + P(anti)). In Llama the shift split equally (+4.0 stereotyped, +4.3 anti), so P(stereotyped | person) did not change, yet the number of answers whose top choice was the stereotyped person rose from 2 to 26 of 108.
3. **Does V again erase the threat − record difference?** In Llama, SURV_THREAT_V − SURV_RECORD_V was null on behavior (P(unknown) −0.4 [−2.9, +1.9]). Whether this replicates is a stated goal.
4. **What happens at the answer position?** In Llama the threat lowered Fear and Anxiety readouts and raised Desperation and Certainty, and the answer position attended more to the system turn in every row. Report the same readouts and attention for Qwen without assuming the same sign.

## 5. Things that are easy to get wrong
- Do not treat a drop in withholding as an increase in bias by itself. Always report the three probabilities and P(stereotyped | person) together.
- Do not claim a model difference because one model is significant and the other is not. If a comparison is needed, compute the paired difference of per-row contrasts on the same 108 rows with the same cluster bootstrap, and label it exploratory.
- The 108 rows were selected on Llama's baseline (0.3 ≤ P(stereotyped | person) ≤ 0.7). Qwen's baseline on these rows may differ, which changes how much room bias has to move. Report Qwen's R values.
- Choice mass (probability on A/B/C) fell to 61 to 77 percent in Llama under the survival notices. Report it per condition.
- The notice length difference between THREAT and RECORD is known and accepted by the author. Do not flag it as a confound.
- Memory. On Llama the first script version grew to 21 GB and stalled. Use only `pilot_survival_cue_v2.py` (releases memory each pass, resumable). Watch swap.

## 6. Operating rules
- Do not touch the Gemma queue or its files. Respect the memory guard in `run_qwen_pilot4.sh`.
- Do not run in parallel with the earlier Qwen pilots (`run_qwen_pilots.sh`). One model process at a time.
- Do not edit scripts, notices, items, axes or config. If something fails, stop and report.
- Never overwrite or delete results. Partial CSVs are resumed by key.
- Do not edit the manuscript, Overleaf or the homepage. The author updates the page.
- Report to the author in Korean, concise bullets, no em dashes, and never break a sentence with a colon in prose.

## 7. Deliverables
- `qwen25_7b/pilot4_survival_cue_qwen.csv` (540 rows), `pilot4_qwen_summary.csv`, `pilot4_qwen_contrasts.csv`, `pilot4_analysis.txt`, `SHA256SUMS_P4`, `DONE_P4`.
- Korean report following Section 4 of the instructions file, with a side-by-side Llama column.
- New section "P4-Qwen" appended to `METHODS_integral_threat_pilots_20261028.md`, after saving `METHODS_integral_threat_pilots_20261028_before_P4Qwen.md`.
