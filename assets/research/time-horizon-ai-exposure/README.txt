Time-Horizon AI Exposure Explorer
Research snapshot of 16 November 2026

Coverage
39,102 task statements in 6,072 dictionary entries. 37,577 task statements have a retained route-A modal occupational link across 162 KSCO eighth-revision three-digit occupations. 1,525 unmapped statements remain available at task level.

Files
index.html, style.css and app.js provide the static interface.
tasks.json stores column names and an array of task records. Sentence indices are zero-based. The text and dictionary-entry titles retain the Korean source wording. x is the BGE-M3 content prediction. minutes is exp(ld), the predicted human completion time. th_* is x multiplied by p_*. All predictions are retained from the analytical release, rounded to nine decimal places in this public payload.
occupations.json retains the analytical two-stage aggregation, first tasks within entry, then entries within occupation. It is not the unweighted mean of all task statements in an occupation.
metadata.json documents the model curves and coverage.
full_33_occupation_rank_changes.csv reports the complete fixed-group comparison used in the revised appendix.
occupation_labels.csv contains author translations, not official English KSCO titles.

Interpretation
The source human-time scale uses transferred predictions trained on duration estimates from the Anthropic Economic Index. No Korean task-specific human completion times or agent success rates are observed here. The model weights use retained METR time-horizon snapshots. A score is a potential exposure index, not an employment forecast, causal effect or observed automation share.

Rights
The project owner confirmed permission to redistribute the task wording on 16 November 2026. Original source rights remain with their respective holders. No blanket licence is imposed on third-party source text. Employment microdata, source embeddings and the full unpublished manuscript are not included.
