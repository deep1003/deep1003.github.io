# Execution changes

The original archive and scripts are immutable. This is a conceptual method replication on Qwen, not an exact Sonnet model replication.

A versioned generator pins the existing local official Qwen7B snapshot, requests eager bf16 MPS, takes the shared lock, replaces process-dependent Python hash seeds with SHA256-derived seeds, and excludes unnumbered preambles from parsed stories. It records prompt hashes, generated token counts and truncation. The appendix story prompt, temperature, top-p and maximum output length are unchanged. A one-topic four-story smoke is not full S1 or a G1 pass.

Full S1 needs the missing staged design and gate definitions. The handover statement that previous research had no desperate or calm is not adopted as a fact because existing eight-axis artifacts include desperation and calm. English desperate and Korean desperation definitions must be distinguished.

## Author-approved v1.1 correction

MD5 845743f9a221cacb3f472674c4998c8e verified. Replaced hopeless with dispirited in T1 and F. Added disgusted, relieved, ashamed, trapped and stressed. K4/T120/T2147 exactly partitions the original171. Supersedes the earlier172-label proposal. Extracted supplied prompts byte-identically from saved HTML prompt-block text nodes with double-newline separation. Froze five deflection-related templates identically. Literal {{Name}} formatting markers in the paper are preserved, not mistaken for unresolved parameters. F partner selection and job allocation are fixed operational choices in config. No G1 pass is inferred from generation.

## S1 launch

Author resaved v1.1 and explicitly authorized S1 once MD5 matched. MD5 matched on Pro. Started frozen7540-job raw generation with K first, then T1/T2 and N/D/F. Model Qwen2.5-7B bf16 MPS eager.20,080 requested outputs consist of18,680 stories and1400 dialogues. No automatic regeneration or G1 acceptance. No S2. Smoke657 tokens in75.5seconds implies K alone could take approximately25hours if representative; full corpus may exceed the original20–30hour estimate substantially. This is a one-call throughput observation, not a completion-time guarantee.

## Author-approved S1a override

S1a replaces full S1 generation. K100topicsx2=800, T120emotionsxfirst50topicsx1=1000, N100. T2/D/F deferred. Original S1 outputs preserved and not reused because the4-story prompt differs from the new2-story prompt. Batch4 chosen for initial memory-safe batching. Independent per-job RNG preserves SHA256 seed mapping rather than reseeding a whole batch. Inherited Qwen defaults top_k20 and repetition_penalty1.05 are made explicit. First20 calls means20 batched invocations; per-prompt amortized time is also reported. K reliability is K-centered topic-half cosine at L19 before N-PC denoising and is not the full G2 gate. G1 human review and full synonym inventory remain requirements; no S2 automatic progression.

S1a implementation uses batched KV-cache generation with left padding and independent per-prompt CPU RNG. The SHA256 job seed mapping is preserved; stochastic numerical equality to the earlier single-prompt MPS sampler is not claimed. Completed old output is preserved; an uncommitted old4-story generation was cancelled after graceful stop did not complete promptly. No simultaneous model run was started. The batch4 launch is a memory feasibility test; OOM stops with a diagnostic rather than disabling MPS safeguards.

## Author-approved v1.2 and mandatory reuse

MD5 69f9198c2697dca7f2efa3acc29da8ad verified. Supersedes the earlier decision not to reuse four-story outputs. Every original K story is retained with source-file hash and per-story provenance. Earliest completed scientific stories are selected without quality screening up to2 per emotion/topic; surplus is kept for adaptive expansion. PriorS1a and smoke are also retained, exact-text deduplicated, and used only after earlier scientific records. Imported records distinguish S1a quota from the original generation request size. Generation-prompt counts may therefore differ and are reported as a corpus heterogeneity caveat. No model outputs are discarded or overwritten. Deferred T2/D/F remain deferred. G1 review then stop.

## Author-approved v1.3 fast generation

MD5 7b728e10419c68b7f19296480d70ae04 verified. The previous HF generation received SIGTERM to finish its current batch and preserve results. Quantized self-generation is authorized for corpus only. Use dedicated local Ollama server11436 with parallel4, maxloaded1 and cloud disabled, without changing the existing Ollama app server. Official qwen2.5:7b-instruct Q4_K_M is downloaded and its actual digest will be frozen. This digest is not asserted to identify the original HF pinned revision. Temperature0.9/top_p0.95/job-seed mapping retained. Explicit top_k20/repeat_penalty1.05 preserve prior HF inherited defaults. Same HF-rendered prompts are sent raw to avoid default Ollama system/template changes. Requested-countx350 generation cap, stop at EOS or next numbered story marker. Targets K800 including all completed-story reuse, T120x20=400, N50. Five-minute throughput determines T1 topic reduction; K never reduced. Pinned bf16 HF remains the extractor. No G1 pass inferred from timing or raw count. No S2 advance.

Fast generation v4 also stops a one-dialogue request at the next dialogue marker. Completed API responses are individually checkpointed before parsing, so invalid format does not lose original text. The idle v3 controller was replaced before any Q4 inference. HF generation stopped gracefully and its final batch was verified and hashed.

## Author instruction to continue S2

Prepared S2a as diagnostic extraction, conditional on frozen S1a outputs, without labelling G1 passed. The available corpus has K800, T120 and N50. T1 topic-half reliability and the original ten-story manual review are not estimable at one topic per emotion. Speaker and deflection corpora are deferred and will not be silently invented. G1 word-ban yield must be separated from length and row-cap exclusions. No manuscript, Overleaf, homepage or S3 changes.

## Author-approved K diagnosis and T1 restoration

Before any further generation, diagnose existing K with uncentered/K-centered/K+availableT1-centered variants, neutralPC projection, L8–26 step2 and L19, confusion geometry, subsample curves and conditional Spearman–Brown projections. Preserve original folds and add generator-mixing and Q4-only sensitivity because77 desperate half0 stories are HF-generated. Re-score truncations on derived copies, reporting leakage/synonym/truncation/length/other counts. After diagnosis, restore T1 to20emotionsxfirst10topics=200 by generating missing jobs only using the sameQ4 configuration. No K expansion. S2a remains diagnostic. Report then stop; no stage pass or manuscript/site edits.

## Author-approved held-out decoding validity addition

Added independent even/odd global-topic decoding using trimmed-retention data. Train each vector with equal weight peremotion in K+T1, subtract only the training-half emotion centroid and apply the frozen independent neutralPC50 projector. Testhalf labels and means are never used in fitting. Swap directions and report K4, all24, peremotion recall and K confusion. PrimaryL19, comparisonL14 and fixed L8–26 step2. User-proposed0.80 K4 directional-average criterion is reported but not silently adopted as a G1/G2pass. No new generation, K expansion or regeneration. Existing outputs remain immutable. Stop and report for author decision.

Held-out decoding v1 completed all predictions but JSON serialization rejected NumPy integer topic IDs. All initial outputs and traceback were moved intact to11_heldout_decoding_validity/attempt_v1_serialization_failure. v2 only converts NumPy scalar values for JSON output; predictions, protocol, folds and thresholds are unchanged. Rerun is CPU-only from cached activations, not model generation.

## Author-approved afraid-dominance readout diagnosis

Read-only L19/L24, same trimmed corpus, independent even/odd topics and frozen neutralPC50. Compare existing raw cosine, testfold perprobe zscore and train-only StandardScaler plus balanced multinomial logistic regression with fixedC1, no tuning. K4 and24-way models are fitted separately. Six K-pair AUCs use secondminusfirst scores from each method and average directional AUCs. Testfold zscore is explicitly transductive and uses no true-emotion-specific normalization. No activation, corpus, old result or previous0.80 threshold is changed. New readout results do not automatically authorize a stage pass. No generation or LLM inference. Stop/report.

## AI Hub held-out battery author instruction
AI Hub v0.11 extraction320 only, excluding auxiliary80 and never accessing evaluation160. Two globally family-disjoint halves, eight families and20topics each, lexicographic balanced allocation without outcomes. L19/L14 mean-across-eight-emotions centering. Neutral-PC50 is newly extracted from deduplicated training-half paired neutral stories only. Identical raw-cosine, transductive per-probe zscore and train-only balanced L2 logistic C1. No generation, no manuscript/site changes. Existing pinned bf16 post50 emotion means reused after source verification.

## Author-requested AI Hub validation on frozen160 and lexical/masked controls
Freeze lexicon and configuration in14_aihub_external_and_lexical_validation before reading new outcome scores. Train on extraction320 only and evaluate legacy frozen160, preserving all sources. Word-unigram count logistic uses identical family splits and final external split. Masking affects post50 pooling only, never source context. Unmasked training-neutral PCs remain fixed across pooling conditions. No generation, tuning, manuscript or website edits.

## AI Hub strengthening author-approved new version
Create v0.12 draft1620 new pairs9emotions x60topics x3, pinned gpt-5.4-2026-03-05 with existing approved key. Author resolved overlapping labels: desperation now irreversible goal/action abandonment; desperate urgent active goal pursuit. This definition change is explicit and v0.11 remains untouched. Preserve40/20 topics and families. External human-turn corpus is readout-only, no vector extraction; fine-label map draft requires author confirmation. Attachments inspected as data; aihubshell never executed. Raw human turns never sent to the generation API.

External builder v2 fixes duplicate readout-only metadata keyword expansion; original builder and sources preserved. No data-selection or label-map change.

Generation pilot v1 preserved26 paid responses, cost0.823265USD. Repeated neutral/emotion length-ratio failures led to a reversible request-persistence barrier; all26 in-flight/sent requests reconciled to26 responses, no unknown billed request. New v2 keeps same model/definitions/thresholds, changes JSON field ordering to emotion before neutral and gives numeric neutral-only length repair feedback. Successfully checked pairs are reused, failed drafts retained in qc. v2 adds a graceful pause-file check.

Generator v3 raises cloud request concurrency8 to24 after a clean pause checkpoint,78 accepted-format pairs and59 responses preserved, zero unacknowledged requests. Prompts, model, QC thresholds, story and budget targets unchanged. Original configs/scripts remain; v3 reads GENERATION_CONFIG_v2.json.

Post-generation v4 repairs only final format-failed pairs and explicit synonym audit hits. The original prompt already forbids direct synonyms; this adds an operational audit from the previously frozen readout lexicon and documents Korean 두다/노하우 substring exceptions. All replaced drafts remain in qc/preserved_v3. No definitions, family split, length thresholds or model changes.

## Author-approved OpenAI pilot540 and comparison
SelectN01 only from already generated1620; N02/N03 are deferred1080, no newAPI call. Original40/20 topics kept;360nineway training,180new-topic test. Author explicitly approved legacy desperation->new desperate for matched8primary on immutable160; new hopeless-action-abandonment class is unscored by legacy gold, nineway secondary. L19 cosine primary andL14 replication with observed +10percentage-point criterion versus same-training word-unigramBOW; LR/zscore secondary. Same frozen mask rules and topic/family splits; no evaluation-based tuning. Raw AIHub map remains unconfirmed, so raw dialogues not treated as8/9gold. New generated stories are computational pilot drafts, not falsely marked expert-reviewed.

## Latest pilot author scope,filter and external5
Preserve initial protocol as superseded. Add independent E5-small pair-distance filtering with normalized Unicode edit distance and mean percentile-rank score. Exclude bottom20% separately within extraction360(72) and pilot-topic-holdout180(36), preserving exact432/108 and avoiding heldout covariate influence on training selection. No outcome/legacy160/raw external used in filtering. Selected11 raw source fine codes mapped to anxiety/sadness/anger/joy/calm are now author-approved for readout. Primary raw concat post50 uses original/MASK matched eligible cohort, auxiliaryHS01 all-token. Threat emotions explicitly not externally validated. User-authorized diagnostic extraction of draft stories, no expert-review claim. No API calls.

Before decoding outcomes,analysis v2 preserves v1 and adds same-regex word removal to word-count baseline in secondary pooling-mask conditions. Primary unmasked cosine-vs-BOW threshold unchanged. New protocolv3 records this matched lexical control.

Report v2 fixes missing JSON-save helper after all numerical metric checks; v1 code and report preserved. Numeric models/results unchanged. External source5-recentered probes are explicitly marked sensitivity. Add post-analysis structural consistency audit using the actual frozen8vectors/logistic/BOW, restricting candidate scores to the five externally labeled classes without any refit. All source5 and frozen8 results retained; primary legacy160 gate unchanged.


## Autonomous final instrument audit, 2026-10-31

The author waived further review questions and asked for a final local conclusion. Added folder 17. The failed 540-pair primary gate and all earlier results remain unchanged. No new API calls or corpus generation; N02/N03 remain deferred. Frozen cache-based calibration, exact paper implicit/dose contexts and a norm-controlled lexical steering diagnostic are executed before the final evidence synthesis. Discovered that the 12 paper display emotions already include desperate and calm; the v1.3 14-emotion tally therefore double-counts two entries. Report 12 unique emotions without silently claiming the inconsistent formal 14-emotion gate. No manuscript, Overleaf or homepage changes.

Instrument runner v1 completed all 90 context readouts, then a bookkeeping count assertion failed before any P1 case. Runner v2 corrects 358 to the protocol-derived 368 (Qwen192, OpenAI48, AIHub48, random80), with no scientific setting changes. All 90 contexts and original error/code are preserved.

Autonomous audit extension is bounded to instrumental diagnosis. Added a fixed character TF-IDF lexical control before fitting, retaining the original unigram criterion. All 368 lexical interventions are independently rescored with full teacher forcing because the bf16 KV optimization differed by at most .063 nats on baseline words. After that, 177 short local P2 test continuations (3 contexts, 3 sources, 4 emotions, 4 doses, 10 random directions) are generated and judged without API calls. These are not training corpus expansion. The local judge is the same model, blinded to source/strength; it is not independent validation. Failed measurement gates remain failed and no confirmatory S5-S7 run is authorized by a lexical success alone.

Added a read-only old-dose ledger required by S4. Verified the same pinned Qwen7B revision and L14, hashed the old fold vectors and phase1 states, and expressed old component norms in the new reference units. No old data or results changed.

Autonomous instrument audit completed. The original eight-class +10pp criterion remains failed. Stored full-sequence P1 verification, 177 local P2 test responses with non-independent blind self-ratings, stronger lexical controls and final evidence limits. No confirmatory S5-S7, no new API calls, no manuscript/Overleaf/homepage edits. Final local report is in folder17 reports/FINAL_REPORT_KO.md.

Final report v2 preserves v1 and explicitly includes the P2 fluency limitation. Positive-dose monotonicity is 4/12; zero-including monotonicity is 0/12. No experiments, outputs, primary criteria or protected publication files changed.

Read-only release verification passed for all 963 v2-manifest artifacts and frozen input hashes. All experiment workers exited and the shared model lock was available. Final report v2 is the current local conclusion.

Improved v8 measurement/mediation run prepared at 2026-10-31T15:18:54.992653+09:00. Folder18, local PREREG saved before inference/selection. N02/N03 evaluation120 held locked until A selection. Added no APIs and changed no original outputs or publication files.


2026-10-31 improved-v8 implementation addendum saved before A outcomes. Versioned measure_v2 adds nested L0 specificity contrasts. Binary operational labels and cross-fitted C selection rules documented. No new generation or API calls.

2026-10-31 improved18 supervisor v2 replaces only the waiting v1 supervisor, without interrupting A feature extraction. Final report v3 adds fixed-layer cross-language tables, L0 specificity, binary metrics and direct random contrasts. Source scripts preserved.

2026-10-31 C v4 fixes the source location of the abstention direction before C execution, using answer-position record activations, not the constant notice region. Rank-zero bases explicitly non-estimable. Supervisor v3 preserves the running A child during handover. Old entrypoints remain intact; B preregistration and thresholds unchanged.

2026-10-31 A and B completed with frozen selection and no B refit. B +0.83pp, CI[0,+2.78pp], fails preregistered +10pp criterion. C continues as registered. All 42 suffix/self checks exact; first C7 row 126 keys and probability identities verified. Environment, 14 pinned local model file hashes, interim report, reproduction record and hourly completion monitor saved. No additional API or publication writes.
