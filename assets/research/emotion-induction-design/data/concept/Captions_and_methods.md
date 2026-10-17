# Figure legends

## Figure 1. Uncertainty and threat wording shift semantic and internal concept-alignment profiles

a,b, Principal-component projections of seven anchor-standardized concept-alignment scores for four fixed system prompts. Semantic representations were obtained from multilingual-e5-small sentence embeddings (a); internal representations were obtained from Qwen2.5-7B-Instruct hidden states at layer 14, at the assistant-start position before generation (b). PCA was fitted separately in each representation space after centering the four prompt profiles. Features were not rescaled again before PCA. Both panels preserve equal horizontal and vertical coordinate scales. Axis percentages indicate explained variance, not statistical confidence or measurement validity. Prompt codes denote binary UN and FA factors, respectively: 00, reference; 01, fear/anxiety-associated self-threat wording only; 10, uncertainty wording only; 11, both. FA is the experimental wording label, not a verified emotional state. c,d, Changes in anchor-standardized projections relative to prompt 00, for the semantic (c) and internal (d) representations. Each concept direction was estimated from six authored positive–control sentence pairs; four additional pairs per concept were held out. Standardization used the training-anchor projection standard deviation. Zero-reference entries are zero by definition. Identical color limits support consistent reading of sign and magnitude, but the two spaces have different models, pooling procedures and anchor calibrations; their numerical magnitudes are not directly comparable as emotion intensities. These are exploratory alignments with constructed concept directions, not emotion probabilities, subjective experiences or causal emotion mechanisms. There are four fixed prompt observations, not 139 independent representation observations. No KoBBQ questions or generated responses enter these panels. No inferential tests or confidence intervals are shown. Source data and PCA loadings accompany the figure.

## Extended Data Figure 1. Overlapping concept directions limit emotion-specific interpretation

a,b, Cosine similarities between the seven concept directions in semantic (a) and layer-14 internal (b) spaces. Self-similarities on the diagonal are omitted. c, For each of four held-out positive–control sentence pairs per concept, the normalized representation difference was compared with all seven training-derived unit directions. Points show how often the intended concept direction had the largest cosine. This paired identification diagnostic is not classification accuracy on independent, unpaired prompts; four authored pairs per concept provide limited evidence of generalization. Semantic FA is identified in only one of four held-out pairs. d, Loadings of the seven scores on internal-profile PC1. The overall sign of a principal component is arbitrary. The sign of PC1 was oriented so that prompt 11 lies above prompt 00 on PC1. All loadings are positive, consistent with a shared alignment component rather than selective activation of a single emotion. Positive alignment with both calm and fear/anxiety therefore does not demonstrate simultaneous opposing emotional experiences. No uncertainty intervals are estimated from these four fixed prompt profiles.

# 한국어 해석

본문 그림은 같은 네 공지가 의미 공간과 7B 내부 공간에서 어떻게 구분되는지 보여준다. 열 순서는 00 중립, 01 FA, 10 UN, 11 UN+FA다. 의미 공간에서는 평온·기쁨 방향이 일부 감소하지만, 내부 공간에서는 모든 개념 방향이 함께 증가한다. 이를 다양한 감정을 동시에 경험한다는 증거로 해석하면 안 된다.

보조 그림은 그 이유를 점검한다. 내부 개념 축들에는 큰 겹침이 있고, 내부 PCA의 제1성분에는 일곱 개념이 모두 양의 가중치로 기여한다. 특히 의미 공간의 FA 축은 다른 감정과의 구분 점검에서 네 쌍 중 한 쌍만 올바르게 구분한다. 따라서 이 그림은 탐색적 개념 정렬 결과로 제출할 수 있으나, 검증된 정서 활성 지표라고 주장하기에는 기준 문장과 독립 검증이 더 필요하다. PCA의 높은 설명분산은 이 측정상의 한계를 해결하지 않는다.

# Artwork and reproducibility

- Figure width 180 mm; Arial body text 7 pt, minimum 5 pt; panel labels 8 pt bold lowercase.
- Editable vector PDF and SVG, RGB. PDF fonts use Type 42; SVG text is retained as text. PNG is rendered at 600 dpi, with separate 180 dpi previews.
- PCA panels use equal data aspect ratios. Heatmaps share limits of −0.65 to +0.65 and a white zero center. Categorical color and shape distinguish conditions; quantitative color encodes projection changes.
- The source measurements and experimental stimuli are unchanged. Only cached CSV and JSON inputs are read. No language-model inference is performed by the plotting script.
- `source_data/` contains plotted changes, PCA coordinates, loadings, axis cosines and held-out counts; `provenance.json` records input and plotting-code hashes.
- Regenerate with `python build_figures.py` from the parent publication_figures folder. The notebook includes the same invocation and saved image outputs.
- Final formatting must be checked against the specific journal and article type before submission. Styling does not imply suitability for acceptance.

# Visual references inspected

The references inform panel organization, shared quantitative scales and clear encoding, not copied artwork or data. The older paper's rainbow palette was not adopted; categorical and continuous palettes serve different purposes here.

1. Nature Research Figure Guide, Preparing figures: our specifications. Standard sans-serif fonts, editable vector text, 5–7 pt body text, 8 pt panel letters, accessible color, and minimal decoration. https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/
2. Compositionality of social gaze in the prefrontal-amygdala circuits. Nature Communications 17, 7478 (2026), Fig. 2, PDF page 5. Aligned matrix panels, common color scales and clearly separated methodological versus inferential panels. https://www.nature.com/articles/s41467-026-74347-8
3. Temporal structure of natural language processing in the human brain corresponds to layered hierarchy of large language models. Nature Communications 16, 10529 (2025), Fig. 2, PDF page 4. Compact lettered panels and separation of model-layer summaries from individual plotted quantities. https://www.nature.com/articles/s41467-025-65518-0

References accessed and PDF figures visually inspected on 17 October 2026. Local reference PDFs are retained separately and are not part of the submission artwork.
