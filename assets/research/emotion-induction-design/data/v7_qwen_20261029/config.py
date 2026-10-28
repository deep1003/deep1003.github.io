"""Qwen2.5-7B-Instruct, clean v5 run (2026-10-27). Layer 14 of 28 (depth 0.50), intervention range 14..24."""
MODEL = "Qwen/Qwen2.5-7B-Instruct"
REVISION = "a09a35458c702b33eeacc393d103063234e8bc28"
LAYER = 14
LAYER_RANGE = list(range(14, 25))
AXES_FILE = "axes_L14.npz"  # original v5 Qwen axes (clean-run axes not yet built)
TAG = "qwen25_7b"
CHAT_KW = {}
CHAT_TEMPLATE = None
