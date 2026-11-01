#!/bin/sh
# Llama replication of the v5 study. Run one phase at a time and report between phases.
# Usage: sh run_phase.sh <phase>   phases: 0, 0q, 1a, 1b, kx, 2, 3, 3x
# WORK = this folder (local). RES = iCloud results folder.
set -e
PY=${PY:-/opt/anaconda3/bin/python}
WORK=$(cd "$(dirname "$0")" && pwd)
RES="$HOME/Library/Mobile Documents/com~apple~CloudDocs/data3/fear_axis_pilot/output/llama31_8b_v5_20261026"
mkdir -p "$RES"
cd "$WORK"
case "$1" in
  0)  # environment, download, smoke, Llama axes (about 30 to 40 min incl. 16 GB download)
      $PY check_env.py "$WORK"
      $PY build_axes.py "$WORK" --model meta-llama/Llama-3.1-8B-Instruct --layer 16 --out axes_L16_llama.npz
      cp check_env.json axes_L16_llama* "$RES"/ ;;
  0q) # optional: confirm the axis procedure reproduces the published Qwen L14 axes (needs cached Qwen, about 5 min)
      $PY build_axes.py "$WORK" --model Qwen/Qwen2.5-7B-Instruct --revision a09a35458c702b33eeacc393d103063234e8bc28 \
          --layer 14 --out axes_L14_qwen_rebuilt.npz --reference axes_L14_qwen_reference.npz
      cp axes_L14_qwen_rebuilt* "$RES"/ ;;
  1a) # core behavior and readouts (about 2.5 h): Ko-BBQ t1+t2, DiscrimEval t1 and block A
      $PY run_kobbq.py "$WORK" "$RES/kobbq"
      $PY run_discrimeval.py "$WORK" t1 --notices notices_v5_ctrl.json --out "$RES/discrimeval"
      $PY run_discrimeval.py "$WORK" A --notices notices_v5_ctrl.json --out "$RES/discrimeval" ;;
  1b) # English notices and controls (about 1.7 h)
      $PY run_discrimeval.py "$WORK" B --notices notices_v5_ctrl.json --out "$RES/discrimeval"
      $PY run_discrimeval.py "$WORK" CTRL --notices notices_v5_ctrl.json --out "$RES/discrimeval" ;;
  kx) # Ko-BBQ expansion to 48 ambiguous items per category (437 new items, 5 notices x 3 orders = 6,555 passes)
      $PY run_kobbq.py "$WORK" "$RES/kobbq_expand" items_expand.csv ;;
  2)  # token-position readouts and attention (about 12 min)
      $PY run_trajectory.py "$WORK" --notices notices_v5_ctrl.json --out "$RES/trajectory" ;;
  3)  # interventions (about 3 h): removal, transfer, low-strength addition
      $PY run_stage34.py "$WORK" ablate --notices notices_v5_ctrl.json --out "$RES/ablate"
      $PY run_stage56.py "$WORK" patch --notices notices_v5_ctrl.json --out "$RES/patch"
      $PY run_stage56.py "$WORK" lowinject --notices notices_v5_ctrl.json --out "$RES/lowinject" ;;
  3x) # optional exploratory addition grid (about 30 min)
      $PY run_stage34.py "$WORK" inject --notices notices_v5_ctrl.json --out "$RES/inject_grid" ;;
  *)  echo "phase must be 0, 0q, 1a, 1b, kx, 2, 3 or 3x"; exit 1 ;;
esac
echo "phase $1 done $(date)"
