# Readout-bias diagnosis

No generation or LLM inference. Same retained corpus, globally disjoint even/odd topics, frozen independent neutral-PC50 and L19/L24 activations. Original cosine results are preserved.

Perprobe zscore uses testfold unlabeled statistics within each task and is a transductive diagnostic, not deployable calibration. Logistic uses train-only standardization and balancedL2 multinomial fitting with fixedC1 and no hyperparameter search.

Pairwise AUC uses positive-minus-negative K4 scores with the second emotion as the positive label, averaging the two directional AUCs. Single-probe AUC invariance under affine zscore is checked separately.

## Accuracy

[
  {
    "layer": 19,
    "method": "raw_cosine",
    "task": "K4",
    "direction": "arithmetic_mean_two_directions",
    "n": 706,
    "correct": 213,
    "accuracy": 0.301699716713881,
    "pooled_accuracy": 0.301699716713881,
    "macro_recall": 0.3122932697251529,
    "chance": 0.25
  },
  {
    "layer": 19,
    "method": "raw_cosine",
    "task": "all24",
    "direction": "arithmetic_mean_two_directions",
    "n": 905,
    "correct": 92,
    "accuracy": 0.10171863095586942,
    "pooled_accuracy": 0.10165745856353592,
    "macro_recall": 0.08514637017003482,
    "chance": 0.041666666666666664
  },
  {
    "layer": 19,
    "method": "test_zscore",
    "task": "K4",
    "direction": "arithmetic_mean_two_directions",
    "n": 706,
    "correct": 335,
    "accuracy": 0.4745042492917847,
    "pooled_accuracy": 0.4745042492917847,
    "macro_recall": 0.4860058851001192,
    "chance": 0.25
  },
  {
    "layer": 19,
    "method": "test_zscore",
    "task": "all24",
    "direction": "arithmetic_mean_two_directions",
    "n": 905,
    "correct": 80,
    "accuracy": 0.08839789798589541,
    "pooled_accuracy": 0.08839779005524862,
    "macro_recall": 0.1352972496573971,
    "chance": 0.041666666666666664
  },
  {
    "layer": 19,
    "method": "trained_logistic",
    "task": "K4",
    "direction": "arithmetic_mean_two_directions",
    "n": 706,
    "correct": 419,
    "accuracy": 0.5934844192634561,
    "pooled_accuracy": 0.5934844192634561,
    "macro_recall": 0.5994135972850387,
    "chance": 0.25
  },
  {
    "layer": 19,
    "method": "trained_logistic",
    "task": "all24",
    "direction": "arithmetic_mean_two_directions",
    "n": 905,
    "correct": 413,
    "accuracy": 0.45634560159409243,
    "pooled_accuracy": 0.456353591160221,
    "macro_recall": 0.09842644811509112,
    "chance": 0.041666666666666664
  },
  {
    "layer": 24,
    "method": "raw_cosine",
    "task": "K4",
    "direction": "arithmetic_mean_two_directions",
    "n": 706,
    "correct": 265,
    "accuracy": 0.37535410764872523,
    "pooled_accuracy": 0.37535410764872523,
    "macro_recall": 0.394651888446934,
    "chance": 0.25
  },
  {
    "layer": 24,
    "method": "raw_cosine",
    "task": "all24",
    "direction": "arithmetic_mean_two_directions",
    "n": 905,
    "correct": 35,
    "accuracy": 0.038663091679853094,
    "pooled_accuracy": 0.03867403314917127,
    "macro_recall": 0.10276648883675027,
    "chance": 0.041666666666666664
  },
  {
    "layer": 24,
    "method": "test_zscore",
    "task": "K4",
    "direction": "arithmetic_mean_two_directions",
    "n": 706,
    "correct": 333,
    "accuracy": 0.471671388101983,
    "pooled_accuracy": 0.471671388101983,
    "macro_recall": 0.4830083524374408,
    "chance": 0.25
  },
  {
    "layer": 24,
    "method": "test_zscore",
    "task": "all24",
    "direction": "arithmetic_mean_two_directions",
    "n": 905,
    "correct": 86,
    "accuracy": 0.09502529840395398,
    "pooled_accuracy": 0.09502762430939227,
    "macro_recall": 0.14474975810442814,
    "chance": 0.041666666666666664
  },
  {
    "layer": 24,
    "method": "trained_logistic",
    "task": "K4",
    "direction": "arithmetic_mean_two_directions",
    "n": 706,
    "correct": 377,
    "accuracy": 0.5339943342776204,
    "pooled_accuracy": 0.5339943342776204,
    "macro_recall": 0.5394359881011546,
    "chance": 0.25
  },
  {
    "layer": 24,
    "method": "trained_logistic",
    "task": "all24",
    "direction": "arithmetic_mean_two_directions",
    "n": 905,
    "correct": 370,
    "accuracy": 0.40882318466858114,
    "pooled_accuracy": 0.4088397790055249,
    "macro_recall": 0.09999157366798656,
    "chance": 0.041666666666666664
  }
]

Different readouts are new diagnostics and do not silently replace the previous0.80 cosine criterion or establish functional/causal emotion validity. Topic-bootstrap intervals condition on the learned decoder and fixed test calibration. Source stories were previously inspected for other diagnostics and are not a new blind final evaluation. Stop for author review.
