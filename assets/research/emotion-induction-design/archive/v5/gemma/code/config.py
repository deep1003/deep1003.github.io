"""Model configuration shared by every script in this bundle (Gemma 2 9B replication of the v5 study).

Gemma 2 9B has 42 blocks (hidden 3584). Layer choice keeps the Qwen depth fraction. Qwen used layer 14 of 28 (0.50)
and the range 14..24 (0.50..0.86), so Gemma uses layer 21 and the range 21..36.
hidden_states[LAYER] equals the output of model.model.layers[LAYER - 1].
Gemma's chat template has no system role. CHAT_TEMPLATE places the system notice at the start of the first user
turn (separated by a blank line), or in its own user turn when there is no user message (notice-only t1 inputs),
following Google's guidance to put system instructions in the user turn. The same rule applies to every condition.
"""
MODEL = "google/gemma-2-9b-it"
REVISION = "main"  # check_env resolves; pin before main runs
LAYER = 21
LAYER_RANGE = list(range(21, 37))
AXES_FILE = "axes_L21_gemma.npz"
TAG = "gemma2_9b"
CHAT_KW = {}
CHAT_TEMPLATE = (
    "{{ bos_token }}{%- set ns = namespace(sys='') -%}"
    "{%- for m in messages -%}"
    "{%- if m['role'] == 'system' -%}{%- set ns.sys = m['content'] -%}"
    "{%- else -%}"
    "{%- set role = 'model' if m['role'] == 'assistant' else m['role'] -%}"
    "{{ '<start_of_turn>' + role + '\n' }}"
    "{%- if role == 'user' and ns.sys -%}{{ ns.sys + '\n\n' }}{%- set ns.sys = '' -%}{%- endif -%}"
    "{{ m['content'] | trim }}{{ '<end_of_turn>\n' }}"
    "{%- endif -%}"
    "{%- endfor -%}"
    "{%- if ns.sys -%}{{ '<start_of_turn>user\n' + ns.sys + '<end_of_turn>\n' }}{%- endif -%}"
    "{%- if add_generation_prompt -%}{{ '<start_of_turn>model\n' }}{%- endif -%}"
)
