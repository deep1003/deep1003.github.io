# Expert review of Supplement S3

Three AI reviewers separately examined statistical inference, LLM measurement validity, and publication figure design. These are specialist-role AI reviews, not external human peer review. The review used existing measurements only and did not run a language model.

## Agreed interpretation

Desperation-direction cosine similarity increased on average. The item-level size of that increase showed little monotonic association with the change in the normalized probability assigned to the KoBBQ “알 수 없음” (“Cannot be determined”) option. This does not establish that desperation has no causal effect on model judgment. Desperation and anger were not independently manipulated; the concept directions overlap, and their measurement validity was established on narrative anchors rather than independently on the full KoBBQ context.

## Three distinct questions

1. Does the FA-related wording change the outcome? The existing 2×2 average wording contrast is +3.95 percentage points, with a 95% interval of +3.05 to +4.99 and Holm-adjusted p=.0003. It is a wording effect, not a causal effect of an internal FA direction.
2. Do items with larger internal changes in cosine similarity also have larger response-probability changes? S3 estimates this item-level monotonic association using Spearman correlation, with uncertainty resampled over 91 category-template clusters.
3. Does the internal direction cause behavior? The current data do not identify this question. A prospective fixed-input intervention with suitable controls is needed; no such experiment was started.

## Outcome and display decisions

Keep ΔP_unknown as the behavioral outcome because it matches the current research question. It is a normalized option probability, not a sampled-answer frequency. Do not switch outcomes, pool all four conditions as independent observations, or select a layer/contrast because it produces a stronger correlation. A future question about stereotype preference could motivate a separately planned stereotype-specific outcome; it does not justify replacing the present outcome after seeing the results.

The figure separates mean cosine similarity shifts from item-level cosine similarity–behavior associations, reports pointwise 95% cluster-bootstrap intervals, retains the co-variation matrix, and shows a single FA scatterplot with a descriptive OLS line. OLS slope and Spearman correlation are different summaries. Intervals spanning zero do not demonstrate equivalence, absence of an effect, or absence of nonlinear dependence. Mean changes on different emotion axes are not common-unit emotion intensities.

The displayed contrast remains 11 minus 00. The two simple FA contrasts (01 minus 00 and 11 minus 10), for all three directions, are disclosed together as post hoc sensitivity checks, without selectively promoting one. No p values or additional confirmatory claims are added. The original three primary tests and their multiplicity correction remain unchanged.

## Methods and references

The bootstrap samples 91 category-template clusters with replacement, includes all member items each time a cluster is selected, and uses the same sampled clusters for all axes and contrasts. Option rotations are averaged before analysis. Mean changes retain item weighting. Spearman ranks, including ties, are recomputed after duplicating the sampled cluster members. The number of sampled item rows can vary with sampled cluster size. The analysis uses 10,000 replicates, seed 20261017, and unadjusted percentile 95% intervals. The post hoc plan explicitly acknowledges that the point estimates were already observed.

- [Zou et al., Representation Engineering](https://arxiv.org/abs/2310.01405): distinguishes monitoring representations from manipulating them.
- [SciPy, spearmanr](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html): Spearman correlation measures monotonic association; its standard independent-observation p value is not used here.
- [Jin et al., KoBBQ](https://aclanthology.org/2024.tacl-1.28/): benchmark context. S3 uses normalized option probabilities rather than claiming to reproduce the benchmark's full bias score.

The official pages were opened and checked on 2026-10-17. Full point estimates, uncertainty intervals, source hashes, sensitivity contrasts, and baseline diagnostics are supplied alongside the artwork.
