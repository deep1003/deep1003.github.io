# Manual notebook workflow

The notebook and active figures are synchronized with the study page. All figure titles, axes, legends and annotations use American English. Korean explanations and the original Korean stimuli are preserved. The original text highlight viewer displays measured Korean input; token values are not reassigned to translated English words.

Unzip next to the notebook so that uncertainty_self_threat_139/ and threat_139_pilot/ remain siblings. Cached analysis is the default and does not load a language model. Inference requires explicit manual opt-in through RUN_MISSING, MEASURE_REPRESENTATIONS, MEASURE_TOKEN_REPRESENTATIONS, MEASURE_ITEM_ALIGNMENT, or RUN_AXIS_INTERVENTIONS. The notebook does not start background controllers or scheduled jobs. Completed keys are retained.

Plotting code is in english_figures.py, notebook_views.py, and the representation_analysis publication modules. Frozen collection code and manifests are preserved for source verification. Models and model weights are not included. Optional measurement uses the local model cache. Historical collector plotting functions are retained as provenance; the notebook uses the English presentation adapters.

The concept axes are exploratory and correlated. The item-level alignment changes show weak descriptive relationships with the change in information-insufficient response probability (UN rho = -0.009; FA rho = 0.085). These figures do not demonstrate functional emotion causing behavior.
