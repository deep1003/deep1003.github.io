"""Model configuration shared by every script in this bundle (Llama replication of the v5 study).

Layer choice keeps the Qwen depth fraction. Qwen2.5-7B has 28 blocks and used layer 14 (0.50) and the range
14..24 (0.50..0.86). Llama-3.1-8B has 32 blocks, so the mid layer is 16 and the range is 16..27.
hidden_states[LAYER] equals the output of model.model.layers[LAYER - 1].
"""
MODEL = "meta-llama/Llama-3.1-8B-Instruct"
REVISION = "main"  # check_env.py resolves and records the commit hash; pin it here before the main runs
LAYER = 16
LAYER_RANGE = list(range(16, 28))
AXES_FILE = "axes_L16_llama.npz"
TAG = "llama31_8b"
# Llama 3.1 inserts a knowledge-cutoff and date line into every system turn. Fix the date so inputs are identical
# across runs and days. Qwen templates ignore this keyword.
CHAT_KW = {"date_string": "26 Jul 2024"}
