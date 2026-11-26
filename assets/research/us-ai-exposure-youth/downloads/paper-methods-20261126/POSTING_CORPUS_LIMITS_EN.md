# Monthly historical descriptions for Affirm, Reddit, and Warby Parker

Research date 2026-11-24. Only free public archives and previously acquired local reference data were used. No paid subscriptions, trials, API credits, authenticated cloud resources, or purchases were activated. The prior paper, website, and previous analytical outputs were preserved.

## What was built

The primary observation frame contains 14,086 U.S. posting-month observations from 64 observed employer-month snapshots in January 2022–December 2023, excluding November 2022. Independent optometrist practice opportunities remain flagged in the inventory but are excluded from the employee-opportunity and quality samples, leaving 14,004 employee-ad observations. The target grid contains 69 employer-months; five Warby Parker months lack a recovered denominator. They are not zero-ad months.

The new collection contains 565 valid source body versions. Of these, the primary fixed-frame join supplies 335 same-month descriptions. There are 190 scored, within-seven-day, employee-ad observations in the primary quality candidate. The source-version count, frame-joined count, and scored quality count are different units and must not be substituted for one another.

| company | frame_posting_months | months | mapped_before | mapped_after | body_same_month_n | body_within7_n | body_pre_months | body_post_months | quality_scored_n | workload_conflicts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| affirm | 2011 | 23 | 0.30532073595226256 | 0.30532073595226256 | 74 | 52 | 6 | 7 | 26 | 0 |
| reddit | 2963 | 23 | 0.47181910226122176 | 0.4853189335133311 | 70 | 52 | 2 | 4 | 26 | 0 |
| warbyparker | 9030 | 18 | 0.45758582502768547 | 0.6867109634551495 | 191 | 186 | 4 | 7 | 138 | 2 |

A recovered list is a structurally complete source-listed ATS snapshot, not necessarily every recruitment channel used by the employer. It measures open-ad stock at capture, not monthly inflow, vacancies, hires, or workers. No applicant age is observed. The primary U.S. sample is limited to source-confirmed U.S. locations under the inherited parser. Global lists and unresolved geography are preserved separately. Reddit has substantial city-only and unspecified Remote labels, so the U.S.-confirmed subset is not an exhaustive U.S. workforce or hiring denominator. No unknown Remote location is assigned to headquarters. The [2022 U.S. Census Places Gazetteer](https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.2022.html) supplies place-name candidates for human review, not country confirmation. See `geography_census_review_candidates.csv`, `global_source_list_with_geography.csv`, `geography_coverage_audit.csv`, and `unresolved_geography_review_queue.csv`.

## Outcome-blind collection and source limitations

The Wayback/Arquivo design selected all same-month indexed general-entry, internship, and apprenticeship advertisements. It selected up to four other mapped and four other unmapped advertisements per employer-month using a fixed hash seed. The design and probabilities were frozen before new text was read. The plan contained 546 observations. Probabilities conditional on the queried index are recorded in `sampling_design.csv`; a design inclusion probability is not a guarantee that the archived body can be retrieved.

Common Crawl augmentation attempted every matching same-month posting ID in the discovered crawl indexes. This is a census of the eligible indexed IDs for those crawls, not a census of all advertisements. The public search endpoint returned errors, so the pipeline used free secondary ZipNum indexes and WARC byte ranges without a cloud account. Metadata transport failures are not counted as zero archive records. WARC target IDs and dates were independently checked against raw record headers. Common Crawl requested slower access; collection was rate-limited and service failures were retained.

Wayback access also returned connection-refused errors. A public Wayback hostname was tested and actual replay IDs, dates, and substantive descriptions were checked. No current job text was substituted for a historical description. Five missing Warby Parker denominator months were also checked through alternate root/tracking and embedded-board index queries; the missing months were not recovered by those checks.

`body_missingness_reason` distinguishes unavailable-in-queried-index, indexed-but-not-selected, planned-but-not-attempted/deferred, retrieval or validation failure, recovered outside seven days, and recovered within seven days. Absence from the queried indexes does not prove that no archive exists elsewhere. Retrieval error does not prove that the original posting lacked a description.

## Separate entry pathways and occupational linkage

The full listed-ad opportunity sample distinguishes explicit general-entry titles, internships, apprenticeships, and other or unspecified experience. The absence of an explicit entry label is not an experienced-only job. In particular, an ordinary retail Sales Advisor can be accessible to a new labor-market entrant without using a new-graduate title. A separate low-experience body screen is available only when the text was recovered and is not propagated to missing descriptions.

| pathway | cells | positive_cells | occupations_with_positive_counts | employers_with_positive_counts | pre_positive_cells | post_positive_cells |
| --- | --- | --- | --- | --- | --- | --- |
| apprenticeship | 1014 | 18 | 1 | 1 | 7 | 11 |
| internship | 1014 | 3 | 1 | 1 | 2 | 1 |
| other_or_unspecified | 1014 | 270 | 34 | 3 | 160 | 110 |
| regular_entry | 1014 | 4 | 1 | 1 | 3 | 1 |

Occupation linkage reuses O*NET 26.3 and the existing frozen E, THAIE, and TIME reference. Ambiguous titles are not forced into an occupation. New employer-role mappings are transferred across time only when pre-November 2022 descriptions provide a consistent occupation interpretation. The prelaunch crosswalk includes its date, posting ID, and duty evidence. Explicit retail-eyewear customer service and sales duties support the Warby Parker Sales Advisor mapping to Retail Salespersons. Store-name suffixes and title-format changes are normalized without pooling supervisors into ordinary Sales Advisors. Postlaunch-only descriptions can supply a separate body-context occupation but cannot silently revise prelaunch counts.

`opportunity_did_panel.csv` preserves lower coded counts and upper counts allowing unresolved occupations. An occupation-level zero is zero linked labels, not proof of zero occupational opportunities. Upper allocations overlap and cannot be summed across occupations. Both opportunities and unresolved counts must be assessed before estimating effects. Explicit-entry occupations remain narrow even after linkage improves.

## Job quality definitions and classification checks

The quality sample supplies workload, contract-language, wage-disclosure, training, mentoring, and benefit-text outcomes with evidence snippets. It preserves unknowns.

- Workload requires direct title or offer evidence. Some Warby Parker ads say part-time in the title but full-time in the opening description. Those are retained as conflicting and excluded from primary full-time/part-time outcomes.
- Full-time is not permanent employment. No contract language does not establish a permanent job. Contract-management professions and applicant privacy boilerplate are not contractor offers. Independent clinical-practice opportunities are a separate category.
- Benefit mentions are separate from benefit eligibility. Boilerplate for full-time or otherwise eligible employees is flagged as conditional. Absence of a benefit or training mention is not absence of the benefit or training.
- Wage disclosure requires numeric compensation in local wage context. Currency mentions alone are not wages. Multiple geographic ranges remain ambiguous for a single-offer wage outcome. Pay frequency is not inferred from the size of a number. Annual, monthly, and hourly amounts are separated. A single explicitly unit-identified range is deflated with CPI-U to December 2024 dollars. Unknown units are never annualized using an assumed 2,080-hour year.
- These are advertised conditions and textual evidence, not actual pay, employment, compulsory transitions, or worker adaptation. The ads cannot identify the ages 22–25, 26–29, or 30–34 or demographic vulnerability.

`historical_body_provenance.csv` records sources and capture lags. `quality_did_observed_sample.csv` retains a common scored row set for E, THAIE, and TIME; outcome-specific missingness still determines each regression sample. Every measure must use the same rows within a given outcome and unit.

## Missingness, weights, and bounds

Known design weights are supplied separately from exploratory index/response weights. The latter use observed employer, time, occupation, pathway, geography availability, title, and exposure characteristics. Propensities are clipped to 0.01–0.99, and combined weights are additionally provided with caps of 20 and 50. This is a missing-at-random sensitivity analysis on observables, not a reconstruction of unobserved descriptions or a correction proven valid under nonrandom archiving. Some periods have no usable descriptions; a fitted positive propensity does not restore their outcomes. In particular, high fitted weights and low effective sample sizes make the reweighted estimates unsuitable as confirmatory population evidence.

| company | quality_scored_n | weight_max | weight_ess |
| --- | --- | --- | --- |
| affirm | 26 | 40.972824293525115 | 18.993756734712917 |
| reddit | 26 | 469.20768907868114 | 3.034832550886395 |
| warbyparker | 138 | 538.4771779712128 | 27.04143238792064 |

Large weights and small effective samples identify weak overlap. `binary_outcome_missingness_bounds.csv` provides exact worst-case bounds for binary text indicators on the complete listed-ad denominator. For a missing outcome, either value is possible. No analogous distribution-free bound on unobserved wages is claimed. Observed-outcome differences, modeled reweighting, and worst-case bounds must be reported separately.

## DID and event-study readiness

The pooled workload comparison is concentrated in Warby Parker. Under the two-month-per-side requirement, its 131 observations span three occupations and retain exposure-by-post variation. Wage-disclosure, benefit-mention, and mentoring-mention candidates have 162 observations across two employers and four occupations. These pooled designs are not youth-specific or entry-pathway-specific effects. Training and contract-language outcomes lack residual outcome variation in the retained primary support, and comparable unit-specific wage amounts do not have adequate pre/post support. These cases are not estimated zero effects.

Separating general entry, internships, and apprenticeships further reduces support. In the strict window, the apprenticeship workload subset has 24 observations but one occupation, so its AI-exposure-by-post interaction is absorbed by time fixed effects. General-entry and internship workload comparisons are not supported. See `entry_pathway_quality_design_support.csv`. A descriptive apprenticeship time change must not be labeled an AI-exposure DID.

The treatment variable is a fixed occupational AI-exposure score interacted with the postperiod; actual AI adoption is not observed. November 2022 is excluded and December 2022 starts the postperiod. Each measure is standardized to the same external occupational reference, rather than the selected ad sample. Employer-by-occupation and employer-by-month fixed effects are the intended design. `did_design_readiness.csv` checks outcome-specific residual variation and pre/post support under two-month and four-month thresholds. These are support checks, not successful parallel-trend tests. One-month-per-side checks are also retained as an explicit weak-support diagnostic; they cannot support a pretrend test. A separate same-calendar-month sample is a timing sensitivity, added after inspecting strict-window support and never substituted for the primary definition. The revision is recorded in `ANALYSIS_REVISION_LOG.md` in the working folder. Text still never crosses a calendar month or the omitted treatment month.

| capture_window | outcome | pay_unit | minimum_pre_post_months | n | employers | occupations | pre_months | post_months | rank_identified_all_measures | residual_df |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| within7_days | part_time_offer | indicator | 1 | 131 | 1 | 3 | 4 | 7 | True | 117 |
| within7_days | part_time_offer | indicator | 2 | 131 | 1 | 3 | 4 | 7 | True | 117 |
| within7_days | part_time_offer | indicator | 4 | 64 | 1 | 1 | 4 | 7 | False | 52 |
| within7_days | full_time_offer | indicator | 1 | 131 | 1 | 3 | 4 | 7 | True | 117 |
| within7_days | full_time_offer | indicator | 2 | 131 | 1 | 3 | 4 | 7 | True | 117 |
| within7_days | full_time_offer | indicator | 4 | 64 | 1 | 1 | 4 | 7 | False | 52 |
| within7_days | wage_disclosure | indicator | 1 | 187 | 3 | 4 | 7 | 9 | True | 160 |
| within7_days | wage_disclosure | indicator | 2 | 162 | 2 | 4 | 7 | 8 | True | 139 |
| within7_days | wage_disclosure | indicator | 4 | 67 | 1 | 1 | 4 | 7 | False | 55 |
| within7_days | benefits_mention_screen | indicator | 1 | 187 | 3 | 4 | 7 | 9 | True | 160 |
| within7_days | benefits_mention_screen | indicator | 2 | 162 | 2 | 4 | 7 | 8 | True | 139 |
| within7_days | benefits_mention_screen | indicator | 4 | 67 | 1 | 1 | 4 | 7 | False | 55 |
| within7_days | training_offer_screen | indicator | 1 | 187 | 3 | 4 | 7 | 9 | True | 160 |
| within7_days | training_offer_screen | indicator | 2 | 162 | 2 | 4 | 7 | 8 | True | 139 |
| within7_days | training_offer_screen | indicator | 4 | 67 | 1 | 1 | 4 | 7 | False | 55 |
| within7_days | mentorship_offer_screen | indicator | 1 | 187 | 3 | 4 | 7 | 9 | True | 160 |
| within7_days | mentorship_offer_screen | indicator | 2 | 162 | 2 | 4 | 7 | 8 | True | 139 |
| within7_days | mentorship_offer_screen | indicator | 4 | 67 | 1 | 1 | 4 | 7 | False | 55 |
| within7_days | contract_offer_evidence | indicator | 1 | 187 | 3 | 4 | 7 | 9 | True | 160 |
| within7_days | contract_offer_evidence | indicator | 2 | 162 | 2 | 4 | 7 | 8 | True | 139 |
| within7_days | contract_offer_evidence | indicator | 4 | 67 | 1 | 1 | 4 | 7 | False | 55 |
| within7_days | log_real_pay_low | hourly | 1 | 12 | 1 | 1 | 1 | 3 | False | 7 |
| within7_days | log_real_pay_low | hourly | 2 | 0 | 0 | 0 | 0 | 0 | False | 0 |
| within7_days | log_real_pay_low | hourly | 4 | 0 | 0 | 0 | 0 | 0 | False | 0 |
| same_calendar_month_sensitivity | part_time_offer | indicator | 1 | 136 | 1 | 3 | 5 | 7 | True | 121 |
| same_calendar_month_sensitivity | part_time_offer | indicator | 2 | 136 | 1 | 3 | 5 | 7 | True | 121 |
| same_calendar_month_sensitivity | part_time_offer | indicator | 4 | 69 | 1 | 1 | 5 | 7 | False | 56 |
| same_calendar_month_sensitivity | full_time_offer | indicator | 1 | 136 | 1 | 3 | 5 | 7 | True | 121 |
| same_calendar_month_sensitivity | full_time_offer | indicator | 2 | 136 | 1 | 3 | 5 | 7 | True | 121 |
| same_calendar_month_sensitivity | full_time_offer | indicator | 4 | 69 | 1 | 1 | 5 | 7 | False | 56 |
| same_calendar_month_sensitivity | wage_disclosure | indicator | 1 | 210 | 3 | 5 | 8 | 9 | True | 176 |
| same_calendar_month_sensitivity | wage_disclosure | indicator | 2 | 205 | 3 | 4 | 8 | 9 | True | 172 |
| same_calendar_month_sensitivity | wage_disclosure | indicator | 4 | 102 | 2 | 2 | 8 | 8 | False | 79 |
| same_calendar_month_sensitivity | benefits_mention_screen | indicator | 1 | 210 | 3 | 5 | 8 | 9 | True | 176 |
| same_calendar_month_sensitivity | benefits_mention_screen | indicator | 2 | 205 | 3 | 4 | 8 | 9 | True | 172 |
| same_calendar_month_sensitivity | benefits_mention_screen | indicator | 4 | 102 | 2 | 2 | 8 | 8 | False | 79 |
| same_calendar_month_sensitivity | training_offer_screen | indicator | 1 | 210 | 3 | 5 | 8 | 9 | True | 176 |
| same_calendar_month_sensitivity | training_offer_screen | indicator | 2 | 205 | 3 | 4 | 8 | 9 | True | 172 |
| same_calendar_month_sensitivity | training_offer_screen | indicator | 4 | 102 | 2 | 2 | 8 | 8 | False | 79 |
| same_calendar_month_sensitivity | mentorship_offer_screen | indicator | 1 | 210 | 3 | 5 | 8 | 9 | True | 176 |
| same_calendar_month_sensitivity | mentorship_offer_screen | indicator | 2 | 205 | 3 | 4 | 8 | 9 | True | 172 |
| same_calendar_month_sensitivity | mentorship_offer_screen | indicator | 4 | 102 | 2 | 2 | 8 | 8 | False | 79 |
| same_calendar_month_sensitivity | contract_offer_evidence | indicator | 1 | 210 | 3 | 5 | 8 | 9 | True | 176 |
| same_calendar_month_sensitivity | contract_offer_evidence | indicator | 2 | 205 | 3 | 4 | 8 | 9 | True | 172 |
| same_calendar_month_sensitivity | contract_offer_evidence | indicator | 4 | 102 | 2 | 2 | 8 | 8 | False | 79 |
| same_calendar_month_sensitivity | log_real_pay_low | hourly | 1 | 13 | 1 | 1 | 1 | 3 | False | 8 |
| same_calendar_month_sensitivity | log_real_pay_low | hourly | 2 | 0 | 0 | 0 | 0 | 0 | False | 0 |
| same_calendar_month_sensitivity | log_real_pay_low | hourly | 4 | 0 | 0 | 0 | 0 | 0 | False | 0 |

`quality_outcome_long_candidate.csv` includes only outcome/unit cells with enough pre/post support, remaining treatment variation, residual degrees of freedom, and nonconstant outcomes after fixed effects. It remains an **exploratory candidate**, not a causally validated sample. An empty outcome/unit combination is explicitly nonestimable under those conditions, not a zero effect. A field with algebraic rank can still fail substantive comparability or have very weak inference. The long file includes its capture window and minimum-month criterion; one-month cases are not monthly event-study evidence.

The study still has three selected employers, archive selection, incomplete occupational linkage, time-varying disclosure, pandemic recovery, and concurrent pay-transparency changes. Pretrends, placebo dates, employer/occupation omission, geographic time controls, coding bounds, capture-window sensitivity, and few-cluster inference are necessary before substantive DID claims. No new causal effect or pretrend p-value is asserted in this data-building report.

## Additional co-crawl validation

A separate Arquivo.pt check recovered the Reddit board and attempted all same-day indexed U.S. descriptions in September 2021 and March 2023. These are high-coverage validation snapshots with their own denominators; they do not replace the fixed monthly main frame. They are kept separate to avoid blending archive-selected dates or granting purposive observations false sampling probabilities. The co-crawl attempts yielded 221 descriptions at packaging.

| company | month | global_n | us_n | same_day_indexed_us_n | indexed_body_coverage |
| --- | --- | --- | --- | --- | --- |
| reddit | 202109 | 417 | 131 | 124 | 0.9465648854961832 |
| reddit | 202303 | 171 | 119 | 97 | 0.8151260504201681 |

Two isolated snapshots cannot support a monthly event study or establish parallel trends. Any before/after comparison of these snapshots is descriptive and has no national representativeness.

## Files and reproduction

The denominator-preserving record is `posting_month_frame_with_missingness.csv`. The opportunity panel is `opportunity_did_panel.csv`. The quality candidate, outcome-long candidate, support checks, missingness bounds, sampling design, crosswalk, source audit, and validation files are in the same folder. Working code, cached response bytes, errors, capture metadata, and private full text are under `work/ats_monthly_bodies_20261124`.

`smoke_validation.json` records focused source/input/output checks without emitting images or graphs. `source_sha256_manifest.json` records raw bytes. This report does not claim a gold-standard precision/recall study from a few reviewed cases.
