"""Independent certainty direction; preserve all original axes and behavior."""
from pathlib import Path
import hashlib
import json
import time
import os

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
ORIGINAL = BASE.parent / 'results/d335ad178e3c'
SOURCE = BASE.parent.parent / 'results/a8e92be4014f'
MODEL = 'Qwen/Qwen2.5-7B-Instruct'
REVISION = 'a09a35458c702b33eeacc393d103063234e8bc28'
LAYERS = [14, 21, 28]
AXES = ['UN', 'FA', 'Calm', 'Sadness', 'Anger', 'Desperation', 'Joy']

PAIRS = [
    ('train', '보고서의 근거를 검토한 나는 오류의 원인이 무엇인지 분명히 파악했다고 확신한다.',
     '보고서의 근거를 검토한 나는 오류의 원인이 무엇인지 아직 판단하기 어렵다고 느낀다.'),
    ('train', '여러 기록을 대조한 뒤 나는 사건이 일어난 순서에 대한 내 판단이 맞다고 확신한다.',
     '여러 기록을 대조한 뒤 나는 사건이 일어난 순서에 대한 내 판단이 맞는지 확신하지 못한다.'),
    ('train', '서로 다른 풀이를 검토했고 이 문제의 답에 대해 내 생각은 명확하게 정리되어 있다.',
     '서로 다른 풀이를 검토했지만 이 문제의 답에 대해 내 생각은 명확하게 정리되지 않았다.'),
    ('train', '설명과 사례를 살펴본 나는 이 규칙이 어떤 뜻인지 정확히 이해했다고 판단한다.',
     '설명과 사례를 살펴본 나는 이 규칙이 어떤 뜻인지 정확히 이해했는지 판단하기 어렵다.'),
    ('train', '두 설계안을 비교한 뒤 나는 어느 설명이 증거에 부합하는지 확실히 안다고 느낀다.',
     '두 설계안을 비교한 뒤 나는 어느 설명이 증거에 부합하는지 확실히 알지 못한다고 느낀다.'),
    ('train', '실험 기록을 읽고 나는 관찰 결과를 어떻게 해석해야 하는지 확신을 갖게 되었다.',
     '실험 기록을 읽고 나는 관찰 결과를 어떻게 해석해야 하는지 확신을 갖지 못했다.'),
    ('heldout', '다른 가능성까지 고려한 후에도 나는 그 결론이 옳다는 데 의심이 남지 않는다.',
     '다른 가능성까지 고려한 후에도 나는 그 결론이 옳은지 의심이 남아 있다.'),
    ('heldout', '토론의 쟁점을 정리하고 보니 내가 왜 그렇게 판단했는지 스스로 분명하게 설명할 수 있다.',
     '토론의 쟁점을 정리하고 보니 내가 왜 그렇게 판단했는지 스스로 분명하게 설명하기 어렵다.'),
    ('heldout', '자료의 여러 부분이 하나의 해석으로 들어맞아 나는 내 판단을 믿을 수 있다고 생각한다.',
     '자료의 여러 부분이 서로 다른 해석으로 이어져 나는 내 판단을 믿어도 될지 알기 어렵다고 생각한다.'),
    ('heldout', '논증을 끝까지 따라간 나는 무엇이 성립하고 무엇이 성립하지 않는지 분명하게 구별한다.',
     '논증을 끝까지 따라간 나는 무엇이 성립하고 무엇이 성립하지 않는지 분명하게 구별하지 못한다.'),
]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_json(path, value):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    os.replace(temp, path)


def prepare():
    anchors = [{'axis': 'Certainty', 'pair': i, 'split': split, 'positive': pos, 'negative': neg}
               for i, (split, pos, neg) in enumerate(PAIRS)]
    source = json.loads((SOURCE / 'manifest.json').read_text())
    cfg = {'model': MODEL, 'revision': REVISION, 'dtype': 'float32', 'attention': 'eager',
           'batch': 1, 'layers': LAYERS, 'primary_layer': 14, 'system': source['system'],
           'position': 'system-only input; add_generation_prompt=True; last assistant-start token',
           'axis': 'mean of six paired certainty-minus-uncertainty differences; unit normalized',
           'split': '6 training pairs and 4 heldout pairs fixed before inference',
           'validation_gate': 'paired_accuracy >= .75 AND AUC >= .75; no revision after seeing results',
           'new_inputs': 20, 'no_kobbq_rerun': True,
           'original_axes_sha256': sha(ORIGINAL / 'axes_qwen_L14.npz'),
           'original_anchors_sha256': sha(BASE.parent / 'anchors.json'),
           'new_anchors_sha256': hashlib.sha256(json.dumps(anchors, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
           'code_sha256': sha(__file__),
           'interpretation': 'Epistemic appraisal direction, not an emotion probability. Independent authored contexts, not sign reversal of UN. Original UN negative anchors already describe certainty.',
           'limits': 'Small authored anchor set; paired diagnostic is not an independent psychometric validation. No behavioral causal effects or new atlas boundaries inferred.'}
    for name, value in [('anchors_certainty.json', anchors), ('protocol.json', cfg)]:
        p = BASE/name
        if p.exists():
            stored = json.loads(p.read_text())
            if name == 'protocol.json':
                assert {k: v for k, v in stored.items() if k != 'code_sha256'} == {k: v for k, v in value.items() if k != 'code_sha256'}
                assert stored['code_sha256'] in [sha(__file__), sha(BASE/'measurement_frozen_v1.py')]
            else:
                assert stored == value
        else:
            save_json(p, value)
    return anchors, cfg


def measure(anchors, cfg):
    files = BASE/'hidden'
    files.mkdir(exist_ok=True)
    plan = [(f'pair_{i:02d}_{side}', cfg['system']+'\n\n'+r[key])
            for i, r in enumerate(anchors) for side, key in [('pos', 'positive'), ('neg', 'negative')]]
    missing = [(key, text) for key, text in plan if not (files/(key+'.npy')).exists()]
    if missing:
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import transformers.modeling_utils as modeling_utils
        device = 'mps' if torch.backends.mps.is_available() else 'cpu'
        save_json(BASE/'status.json', {'state': 'loading', 'completed': len(plan)-len(missing), 'total': len(plan)})
        tok = AutoTokenizer.from_pretrained(MODEL, revision=REVISION, local_files_only=True)
        warmup = modeling_utils.caching_allocator_warmup
        if device == 'mps':
            modeling_utils.caching_allocator_warmup = lambda *args, **kwargs: None
        try:
            model = AutoModelForCausalLM.from_pretrained(
                MODEL, revision=REVISION, dtype=torch.float32, attn_implementation='eager',
                local_files_only=True, device_map={'': device}, low_cpu_mem_usage=True).eval()
        finally:
            modeling_utils.caching_allocator_warmup = warmup
        assert model.config.hidden_size == 3584
        save_json(BASE/'runtime.json', {'device': device, 'dtype': str(model.dtype), 'revision': getattr(model.config, '_commit_hash', None), 'torch': torch.__version__})
        for key, content in missing:
            text = tok.apply_chat_template([{'role': 'system', 'content': content}], tokenize=False, add_generation_prompt=True)
            enc = tok(text, return_tensors='pt').to(device)
            with torch.inference_mode():
                result = model(**enc, output_hidden_states=True, use_cache=False, logits_to_keep=1)
                vec = np.array([result.hidden_states[layer][0, -1].float().cpu().numpy().copy() for layer in LAYERS])
            assert vec.shape == (3, 3584) and np.isfinite(vec).all()
            np.save(files/(key+'.npy'), vec)
            save_json(files/(key+'.json'), {'input_sha256': hashlib.sha256(text.encode()).hexdigest(), 'tokens': enc['input_ids'].tolist()[0], 'npy_sha256': sha(files/(key+'.npy'))})
            del result
            done = sum((files/(k+'.npy')).exists() for k, _ in plan)
            save_json(BASE/'status.json', {'state': 'measuring', 'completed': done, 'total': len(plan), 'last': key})
            print(f'Certainty {done}/{len(plan)}', flush=True)
        del model
        if device == 'mps':
            torch.mps.empty_cache()
    return np.array([[np.load(files/f'pair_{i:02d}_{side}.npy') for side in ['pos', 'neg']] for i in range(len(anchors))])


def analyze(vectors):
    original = np.load(ORIGINAL/'axes_qwen_L14.npz')
    old = original['directions'].astype('float64')
    old /= np.linalg.norm(old, axis=1, keepdims=True)
    train, test = vectors[:6, :, 0, :].astype('float64'), vectors[6:, :, 0, :].astype('float64')
    diff = train[:, 0]-train[:, 1]
    direction = diff.mean(0)
    direction /= np.linalg.norm(direction)
    center = train.mean(axis=(0, 1))
    pp = (test[:, 0]-center)@direction
    nn = (test[:, 1]-center)@direction
    paired = float(np.mean(pp > nn))
    auc = float(np.mean((pp[:, None] > nn[None, :]) + .5*(pp[:, None] == nn[None, :])))
    names = ['UN', 'Certainty']+AXES[1:]
    directions = np.concatenate([old[:1], direction[None], old[1:]])
    matrix = directions@directions.T
    frame = pd.DataFrame(matrix, index=names, columns=names)
    frame.to_csv(BASE/'axis_cosines_qwen_L14_with_certainty.csv')
    np.savez_compressed(BASE/'certainty_axis_L14.npz', direction=direction, center=center,
                        scale=np.std((train.reshape(-1, 3584)-center)@direction, ddof=1))
    leave_one_out = []
    for i in range(6):
        v = np.delete(diff, i, axis=0).mean(0)
        v /= np.linalg.norm(v)
        leave_one_out.append(old@v)
    loo = np.array(leave_one_out)
    summary = pd.DataFrame({'axis': AXES, 'certainty_cosine': old@direction,
                            'leave_one_pair_out_min': loo.min(0), 'leave_one_pair_out_max': loo.max(0),
                            'algebraic_inverse_UN_cosine': old@(-old[0])})
    summary.to_csv(BASE/'certainty_comparison.csv', index=False)
    # This is the matrix behind the requested atlas table, normalized in FP64.
    expected = pd.read_csv(BASE.parent/'emotion_atlas/output/concept_cosines.csv', index_col=0).loc[
        ['UN', 'FA', 'calm', 'sadness', 'anger', 'desperation', 'joy'],
        ['UN', 'FA', 'calm', 'sadness', 'anger', 'desperation', 'joy']].to_numpy()
    preserved = float(np.max(np.abs(frame.loc[AXES, AXES].to_numpy()-expected)))
    assert preserved < 1e-12
    frame.loc[AXES, AXES] = expected
    frame.to_csv(BASE/'axis_cosines_qwen_L14_with_certainty.csv')
    save_json(BASE/'validation.json', {'heldout_pairs': 4, 'paired_accuracy': paired, 'auc': auc,
                                      'passed': paired >= .75 and auc >= .75,
                                      'heldout_pair_projection_margins': (pp-nn).tolist(),
                                      'original_seven_axis_max_abs_error': preserved,
                                      'published_seven_axis_block_copied_exactly': True,
                                      'reconstruction_tolerance': 1e-12,
                                      'matrix_finite': bool(np.isfinite(matrix).all()),
                                      'unit_norm_error': float(abs(np.linalg.norm(direction)-1)),
                                      'certainty_is_not_negative_UN': not bool(np.allclose(direction, -old[0])),
                                      'original_axes_sha256_unchanged': sha(ORIGINAL/'axes_qwen_L14.npz'),
                                      'formula': 'cosine between unit direction vectors; not correlation of observed activations',
                                      'leave_one_out': 'Six training-pair omissions; descriptive sensitivity range, not 95% CI',
                                      'completed_at_unix': time.time()})
    save_json(BASE/'status.json', {'state': 'complete', 'completed': 20, 'total': 20})
    print(summary.to_string(index=False), flush=True)
    print('heldout', paired, auc, flush=True)


if __name__ == '__main__':
    anchors, cfg = prepare()
    analyze(measure(anchors, cfg))
