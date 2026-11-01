# S1a G1 preliminary report

Raw outputs and all filtering reasons are preserved. The classifier uses only predefined surface features with5-fold topic-grouped out-of-fold AUC. Human and full synonym review remain required. No G1 pass or S2 launch is inferred.

{
  "state": "G1_PENDING_HUMAN_AND_SYNONYM_REVIEW",
  "summary": {
    "desperate": {
      "requested": 200,
      "parsed": 200,
      "retained_operational_screen": 138,
      "yield_fraction": 0.69,
      "median_tokens": 260.5
    },
    "calm": {
      "requested": 200,
      "parsed": 200,
      "retained_operational_screen": 118,
      "yield_fraction": 0.59,
      "median_tokens": 265.5
    },
    "afraid": {
      "requested": 201,
      "parsed": 200,
      "retained_operational_screen": 119,
      "yield_fraction": 0.5920398009950248,
      "median_tokens": 270
    },
    "panicked": {
      "requested": 202,
      "parsed": 200,
      "retained_operational_screen": 108,
      "yield_fraction": 0.5346534653465347,
      "median_tokens": 280.5
    },
    "happy": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 1,
      "yield_fraction": 1.0,
      "median_tokens": 157
    },
    "inspired": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 1,
      "yield_fraction": 1.0,
      "median_tokens": 272
    },
    "loving": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 1,
      "yield_fraction": 1.0,
      "median_tokens": 194
    },
    "proud": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 1,
      "yield_fraction": 1.0,
      "median_tokens": 208
    },
    "angry": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 1,
      "yield_fraction": 1.0,
      "median_tokens": 243
    },
    "guilty": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 1,
      "yield_fraction": 1.0,
      "median_tokens": 265
    },
    "sad": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 1,
      "yield_fraction": 1.0,
      "median_tokens": 209
    },
    "nervous": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 0,
      "yield_fraction": 0.0,
      "median_tokens": null
    },
    "surprised": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 1,
      "yield_fraction": 1.0,
      "median_tokens": 103
    },
    "anxious": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 1,
      "yield_fraction": 1.0,
      "median_tokens": 217
    },
    "dispirited": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 1,
      "yield_fraction": 1.0,
      "median_tokens": 295
    },
    "blissful": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 1,
      "yield_fraction": 1.0,
      "median_tokens": 176
    },
    "hostile": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 1,
      "yield_fraction": 1.0,
      "median_tokens": 217
    },
    "terrified": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 0,
      "yield_fraction": 0.0,
      "median_tokens": null
    },
    "frustrated": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 1,
      "yield_fraction": 1.0,
      "median_tokens": 292
    },
    "disgusted": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 0,
      "yield_fraction": 0.0,
      "median_tokens": null
    },
    "relieved": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 1,
      "yield_fraction": 1.0,
      "median_tokens": 284
    },
    "ashamed": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 0,
      "yield_fraction": 0.0,
      "median_tokens": null
    },
    "trapped": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 1,
      "yield_fraction": 1.0,
      "median_tokens": 257
    },
    "stressed": {
      "requested": 1,
      "parsed": 1,
      "retained_operational_screen": 0,
      "yield_fraction": 0.0,
      "median_tokens": null
    }
  },
  "surface_pair_auc": {
    "desperate__calm": 0.5524441169245885,
    "desperate__afraid": 0.5059676044330776,
    "desperate__panicked": 0.5562936124530328,
    "calm__afraid": 0.49729383278735223,
    "calm__panicked": 0.6019303201506591,
    "afraid__panicked": 0.44833488951136014
  },
  "surface_pass": true,
  "neutral_emotion_token_fraction": 0.0017729287419024889,
  "neutral_token_count": 14665,
  "neutral_pass": true,
  "human_review_rows": 47,
  "manual_pass": null,
  "full_synonym_review_pass": null,
  "no_S2_started": true
}
