# Held-out emotion decoding validity

Read-only existing-data addition. The predeclared primary layer is19, with neutral-PC50 and globally topic-disjoint even/odd folds. Each direction is trained using peremotion means with equal emotion weight across24 classes; testhalf data do not enter centering or vector fitting. The fixed neutralPC is based only on independent N50.

K4 restricts the alternatives to the4K vectors, although their centering uses all24 training means. All24 tests every retained K+T1 story against all24 alternatives. K_in_24 is supplementary. Both directional and pooled results, peremotion recalls, macrorecall and train-majority baselines are reported.

Uniform chance is25% for K4 and4.167% for24 choices. Unequal class frequencies mean the majority baseline is different; macrorecall is provided.

## Primary L19

[
  {
    "layer": 19,
    "task": "K4",
    "direction": "arithmetic_mean_two_directions",
    "n": 706,
    "correct": 213,
    "accuracy": 0.301699716713881,
    "pooled_accuracy": 0.301699716713881,
    "macro_recall": 0.3122932697251529,
    "uniform_chance": 0.25,
    "train_majority_baseline": 0.26912181303116145
  },
  {
    "layer": 19,
    "task": "all24",
    "direction": "arithmetic_mean_two_directions",
    "n": 905,
    "correct": 92,
    "accuracy": 0.10171863095586942,
    "pooled_accuracy": 0.10165745856353592,
    "macro_recall": 0.08514637017003482,
    "uniform_chance": 0.041666666666666664,
    "train_majority_baseline": 0.20994256578561798
  },
  {
    "layer": 19,
    "task": "K_in_24",
    "direction": "arithmetic_mean_two_directions",
    "n": 706,
    "correct": 76,
    "accuracy": 0.1076487252124646,
    "pooled_accuracy": 0.10764872521246459,
    "macro_recall": 0.11087822102020886,
    "uniform_chance": 0.041666666666666664,
    "train_majority_baseline": 0.26912181303116145
  }
]

## Proposed criterion

{
  "primary_layer": 19,
  "proposed_K4_threshold": 0.8,
  "observed_K4_accuracy": 0.301699716713881,
  "meets_proposed_threshold": false,
  "automatic_pass": false,
  "author_decision_required": true,
  "no_G1_G2_pass_claim": true,
  "no_K_expansion": true,
  "no_generation": true,
  "no_regeneration": true
}

## Conditional topic-bootstrap interval

{
  "estimate": 0.301699716713881,
  "lo": 0.27950891976762837,
  "hi": 0.3230783783131656,
  "draws": 2000,
  "scope": "topic-cluster test-resampling CI conditional on frozen training vectors and neutralPC; no model refit"
}

The0.80 threshold is an author-proposed comparison rule, not automatic authorization to claim G1/G2 passage. Layer sweep results are descriptive and must not replace the primaryL19 result after inspection. Existing synonym-screen and human-review limitations remain. Generation engine mixing is preserved and globally balanced more closely by the even/odd split, but not experimentally eliminated. No new data were generated. Stop for author review.
