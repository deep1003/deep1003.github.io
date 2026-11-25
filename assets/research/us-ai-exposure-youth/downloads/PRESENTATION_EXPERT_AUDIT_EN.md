# Independent presentation and interpretation audit

Reviewed on November 25, 2026. This review inspected source code, published HTML, compact chart records, regression tables, event-study plotting logic, and scientific wording. No plots were emitted. No outside employment data were added.

## Confirmed defects and repairs

1. **High priority, contradictory active methods.** Before repair, `index.html` line 8 described an annual-2022-mean denominator, a January 2017 main estimation start, old support percentages, and a September–November event reference. The active `story.js` points transformation already divided every supported curve by its own November 2022 value and began at November 2022, while current symmetric models use December 2018 as the primary start and August–October 2022 as the event reference. The methods text was stale, not evidence of incorrect active chart normalization. `publish.py` lines 101–105 updated only a top paragraph. The complete current detailed Methods section has been replaced, while explicitly archived results remain unchanged.

2. **Medium priority, false CSV observation status.** In `story.js` lines 535–541 before repair, every noninterpolated record was exported with `status=observed`, including null values caused by missing or insufficient sample support. Such rows could be misread as observed zero or ordinary observations. Both the active site script and source script now export these as `unavailable`. No underlying numerical values were changed.

3. **Low priority, incorrect accessible chart description.** Sex charts inherited a fallback SVG description saying occupation was held fixed and only a selected age curve was shown. The actual charts pool within quintile and compare women with men. Both scripts now describe those groups and clarify that the gray gap is descriptive, rather than confidence shading.

4. **Low priority, duration wording.** `report.py` line 254 referred to a nearly four-year post-period while discussing the 36-month robustness window. The correct duration for that window is three years. This issue was referred to the lead agent, who owns report generation.

## Checks passed

The active `points()` function renormalizes annual-base stored units to November 2022. The common annual denominator cancels algebraically. For all 1,260 series-by-outcome combinations across six chart families, 821 have supported positive November baselines and rebased values equal exactly 100. The other 439 have unavailable baselines and are suppressed. There are 37,542 supported post-baseline observations. These counts include occupation-specific and broad-family cells, rather than only the main quintile panels. The frozen occupation selector filters both occupation scope and selected age. Software developers remain Q4; it does not fabricate five within-occupation exposure groups.

The October 2025 dashed bridge is used only when both neighboring months meet support criteria. Observed paths stop around the estimated point, and the descriptive sex-gap fill excludes it. The active text distinguishes employment counts from employment rates, repeated stocks from individual transitions, full-time status from contract permanence, and descriptive paths from DID estimates. Event-study figure code separates pandemic gaps and the transition month and labels its intervals as pointwise. Primary DID estimates and multiplicity statements match their result tables. No evidence was found that active chart indices use the wrong baseline or that numerical findings were changed through palette or display filtering.

## Interpretation limits that remain

Monthly charts do not display CPS sampling intervals, so visual distance alone is not a significance test. A one-month baseline is noisy for small age-by-sex-by-quintile cells. Independent normalization of women and men compares proportional paths and does not measure their employment-level gap. Showing only November 2022 onward is suitable for the requested descriptive comparison but cannot diagnose pretrends; the separate pre-period event figures are essential. Nonsignificant direct age and FT/PT tests do not prove identical effects or establish no displacement. The current text generally makes these distinctions correctly.

## Reproduction

Run `work/us_symmetric_validation_20261125/apply_presentation_audit.py` after `publish.py`. The script is idempotent, preserves archived specifications, patches the active and reusable JavaScript copies, and writes `tables/presentation_audit_checks.json`. It emits no images. These are presentation and arithmetic checks, not validation of the causal assumptions or complete CPS survey variance.
