# Manual notebook workflow

The study uses four main-text figures (M1–M4) and three supplementary figures (S1–S3), listed in figure_catalog.json. Figure display reads existing artwork and never calls a plotting builder. Set SHOW_SUPPLEMENT=True to display the three supplements. Progress is shown as tables. Explicit measurement flags default to False; no model inference or background jobs start automatically.

Before M3, the notebook and website show a cosine-similarity/contact table and an audited explanation of geometry and observed cells. Geometry is PCA plus an equal-area power diagram, not correlation thresholding; each cell is one item–choice-rotation–axis value.

Supplement S3 relates FA, desperation, and anger changes in cosine similarity to behavioral changes using existing observations only. It is a post hoc descriptive analysis with 10,000 paired template-cluster bootstrap replicates and pointwise unadjusted 95% intervals, not a test of independent or combined causal emotion effects. The existing outcome and three primary hypothesis tests are unchanged.

The combined effect (11 minus 00) is an additional descriptive contrast, distinct from the interaction difference in differences. Its unadjusted 95% interval uses the same paired cluster bootstrap. The three primary tests and their Holm adjustment are unchanged.

All charts use American English, consistent 00/01/10/11 colors, 600 dpi PNG and vector PDF/SVG exports. The original Korean stimuli remain Korean. Internal cosine similarity is not evidence of experienced emotion or emotion-specific causal mediation.

The ZIP contains the same notebook source without embedded output images, with each of the seven PNGs stored once, code and cached measurements. Execute display cells to view them. The separately downloadable notebook retains four main-text figures as saved outputs. Unzip beside uncertainty_self_threat_139/ and threat_139_pilot/. Models and model weights are not included. PDF/SVG files are downloaded individually from the website.

Raw measurements, frozen collectors, hashes, and numerical checks are preserved. Older figure variants are retained in the local timestamped recovery backup and original analysis folders, outside the active figure set. Optional historic renderers remain available as implementation records and are not called by the default notebook.
