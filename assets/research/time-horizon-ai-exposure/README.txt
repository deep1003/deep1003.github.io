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

Occupation-first interface update
The landing view is the interactive occupation map. The horizontal axis is predicted human minutes on a linear scale; the vertical axis is BGE content exposure. Dark-to-light colour shows horizon exposure on a fixed scale across all four scenarios. Node area is proportional to employed persons. Employment is the mean of six survey-weighted occupation totals from April and October 2023–2025, covering recorded ages and education groups. No individual microdata are distributed.

Initial controls use Claude Opus 4.6 (2026), Occupations, horizon score descending and ten records per page. Tasks use a separate unit and the same ten-record pagination. The optional collapsed comparison orders ten occupations by absolute content-rank minus horizon-rank difference among all 162 occupations; ties are broken by horizon score. An alternative view compares the ten highest occupations under each index. Both indices use BGE-M3.

Map label and size revision
Native SVG title tooltips were removed from occupation nodes and the map root; the custom hover information panel and accessible node names are retained. Fifteen illustrative occupation categories receive fixed text labels. Label positions are recalculated on zoom, avoid other labels and penalise overlap with nodes; leaders are straight. Node area is now directly proportional to employment, with radius 28 * sqrt(employment / maximum employment). No minimum-size floor or clipping of employment values is applied. This changes the display scale only, not the input data or exposure scores.

Label readability revision
Labels are approximately 1.2 times larger, with a minimum displayed font size of 13.2 CSS pixels. Text width is measured using the rendered font. Candidate positions must avoid all occupation nodes and previously placed labels, rather than merely penalising overlap. Nearby positions are preferred; free map space is searched if necessary. Labels are recalculated on zoom, pan and viewport resize. Labels that cannot be placed without overlap are temporarily omitted in crowded views. Straight leaders are drawn beneath the label text. Data, node sizes and the manuscript are unchanged.
