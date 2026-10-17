# Concept atlas, hierarchy, and UMAP methods

The atlas is a schematic display of seven constructed concept directions, not a neural map. Original 3,584-dimensional unit directions determine cosine distances and PCA sites; the two-dimensional retained variance is 0.597916. The normalized distance stress is 0.351747. No behavioral outcome or measured alignment intensity determines the region sites or boundaries.

## Region geometry and observed cells

Power cells satisfy ||x-s_i||²-w_i ≤ ||x-s_j||²-w_j for every j. Convex half-plane clipping within a 256-edge circular outline gives vector boundaries. Weights are solved numerically to equalize region area. Equal area is a display constraint, not an estimate of emotional prevalence. This use of power geometry follows the definition in [Aurenhammer (1987)](https://epubs.siam.org/doi/abs/10.1137/0216006).

Each region is recursively partitioned into 139 equal-area item cells, each further partitioned into three observed choice-rotation cells. Assignment is fixed by category, category-template cluster, item ID, and recursive partition order. Positions inside a region have no semantic or anatomical meaning. There are 417 observed item-rotation values per region, 2,919 displayed cells per panel, and 11,676 values across four conditions. These are repeated measurements of 139 items, not 417 or 2,919 independent items. No values are interpolated, duplicated to create extra cells, or smoothed.

Changes are paired against the same item, rotation, and axis under UN0FA0. All three-rotation averages match the preserved item-level means at absolute tolerance 1e-12. The original behavioral analyses and raw measurements are unchanged. Absolute and change figures have separate labeled ranges, each held fixed across conditions. FA is retained as a combined direction because separate F and A measures do not exist in these data.

## Hierarchy and contact

Average linkage operates on original 1-cosine distances, with optimal leaf ordering. Ward linkage is not applied to cosine dissimilarities. Definitions and implementation are documented by [SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html), which cites Bar-Joseph, Gifford, and Jaakkola (2001) for optimal leaf ordering. The cophenetic correlation is 0.795451. The dendrogram is a separate diagnostic; it does not generate the power-cell boundaries. Boundary-contact pairs are shown with their original-space cosines. Contact must not be interpreted as a high-similarity threshold, and noncontact does not imply low similarity.

## UMAP companion

A single joint UMAP uses 556 item-condition profiles with seven original cosine-alignment features, not all 3,584 hidden-state dimensions. The primary configuration is fixed before fitting: Euclidean distance, 15 neighbors, min_dist=0.3, two dimensions, 300 epochs, seed 42, one job. Sensitivity settings are (neighbors, seed) = (5,42), (30,42), (15,13), and (15,97). All five settings are reported; the primary layout is not selected for appearance. Colors indicate conditions in order 00,01,10,11; all item markers are circles. No territory boundaries, interpolated color surfaces, or categorical cluster claims are added. These 556 profiles are four repeated conditions for 139 selected items.

The primary trustworthiness at k=10 is 0.9744 and original-neighbor recall is 0.5683. Across all five settings these range from 0.9691 to 0.9774 and 0.5171 to 0.5822, respectively. These quantify limited aspects of neighborhood preservation, not construct validity or emotion-specific function. UMAP distances, gaps, and density are exploratory. See [McInnes, Healy, and Melville](https://arxiv.org/abs/1802.03426), [the developers' clustering cautions](https://umap-learn.readthedocs.io/en/latest/clustering.html), and [reproducibility guidance](https://umap-learn.readthedocs.io/en/latest/reproducibility.html).

## Expert-method review and interpretation

Three AI specialist roles reviewed geometry/clustering, fear-anxiety construct validity, and UMAP methodology. This is AI-assisted methodological review, not external human peer review. The agreed checks were retention of original measurements; explicit paired rotation keys; no inflation of independent sample size; separate reporting of geometry and true similarity; pre-fixed UMAP parameters with all sensitivity results; and retention of FA pending independent F/A validation. Fear/anxiety review and a prospective minimal validation plan are supplied separately. No new language-model inference was run.

## Reproduction

The notebook reads cached UMAP coordinates by default. Local refitting used an isolated Python environment with NumPy 2.1.3, Numba 0.61.0, and umap-learn 0.5.12 to avoid changing the notebook kernel's installed packages. Cached plotting does not import Numba or require this environment. A deliberate refit requires compatible UMAP dependencies; do not downgrade packages inside an active experiment kernel.
