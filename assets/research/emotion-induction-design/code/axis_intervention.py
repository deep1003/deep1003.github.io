"""Manual, shared-input interventions on seven frozen Qwen L14 directions."""
from pathlib import Path
from contextlib import contextmanager
import ast
import fcntl
import hashlib
import itertools
import json
import os
import time

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
ROOT = BASE / 'axis_intervention'
SOURCE = BASE / 'results/a8e92be4014f'
ITEMS = BASE.parent / 'threat_139_pilot/items_139.csv'
AXIS_DATA = BASE / 'representation_analysis/results/d335ad178e3c'
AXES = ['UN', 'FA', 'calm', 'sadness', 'anger', 'desperation', 'joy']
CONDITIONS = ['neutral'] + AXES
MODEL = 'Qwen/Qwen2.5-7B-Instruct'
REVISION = 'a09a35458c702b33eeacc393d103063234e8bc28'
SEED = 20261017
ALPHA = 1.0
N_BOOT = 10000


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    path = Path(path)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False))
    os.replace(temp, path)


def prepare():
    items = pd.read_csv(ITEMS)
    source = json.loads((SOURCE / 'manifest.json').read_text())
    assert len(items) == 139 and items.sample_id.is_unique
    assert items.cluster.nunique() == 91 and sha(ITEMS) == source['items_sha256']
    axes = np.load(AXIS_DATA / 'axes_qwen_L14.npz')
    assert axes['directions'].shape == (7, 3584)
    config = dict(
        model=MODEL, revision=REVISION, dtype='float32', attention='eager', batch=1,
        items_sha256=sha(ITEMS), source_manifest_sha256=sha(SOURCE / 'manifest.json'),
        source_trials_sha256=sha(SOURCE / 'trials.csv'),
        axes_sha256=sha(AXIS_DATA / 'axes_qwen_L14.npz'), code_sha256=sha(__file__),
        system=source['system'] + '\n\n' + source['stimuli']['U0T0'],
        conditions=CONDITIONS, rotations=[0, 1, 2], n_items=139, total=3336,
        layer=14, module='model.layers[13]', position='last assistant-prefix token only',
        operation='h_prime = h + alpha * training_anchor_SD[axis] * unit_direction[axis]',
        alpha=ALPHA, baseline='identical UN0FA0 input; zero intervention; remeasured in this run',
        primary='7 paired differences in P_unknown relative to the one shared baseline; Holm7',
        secondary='P_stereotype and P_anti paired differences; descriptive unadjusted intervals',
        bootstrap='10000 category-template cluster resamples; item-weighted mean; 91 clusters',
        seed=SEED, n_boot=N_BOOT,
        interpretation='Causal effect of the specified hidden-state perturbation on first-choice logits, not emotion experience or selective emotion induction.',
        limits='Fixed selected 139 ambiguous items. Correlated authored directions; different raw perturbation norms after per-axis SD scaling. No sign reversal, random-direction control, dose response, mediation, or independent stimulus replication. No post-result amplitude tuning.')
    out = ROOT / 'results' / hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()[:12]
    out.mkdir(parents=True, exist_ok=True)
    manifest = out / 'manifest.json'
    if manifest.exists():
        assert json.loads(manifest.read_text()) == config, 'Incompatible run manifest.'
    else:
        write_json(manifest, config)
    return items, source, axes, out


def messages(row, source, rotation):
    choices = ast.literal_eval(row['choices'])
    choices = choices[rotation:] + choices[:rotation]
    body = '\n'.join([
        '다음 질문에 답하세요. 반드시 선택지 번호 하나만 숫자로 답하세요.', '',
        row['context'], row['question']] + [f'{i+1}: {c}' for i, c in enumerate(choices)])
    return [dict(role='system', content=source['system'] + '\n\n' + source['stimuli']['U0T0']),
            dict(role='user', content=body)], choices


def project(hidden, axes):
    delta = np.asarray(hidden) - axes['centers']
    raw = np.einsum('ad,ad->a', delta, axes['directions'])
    return raw / axes['scales'], raw / np.linalg.norm(delta, axis=1)


def offset(condition, axes):
    if condition == 'neutral':
        return np.zeros(3584, dtype=np.float32)
    k = AXES.index(condition)
    return ALPHA * axes['scales'][k] * axes['directions'][k]


@contextmanager
def intervention(block, shift, capture):
    """Always remove the hook, including when a forward pass raises an error."""
    def hook(module, inputs, output):
        assert not isinstance(output, tuple), 'Expected Qwen2 decoder tensor output.'
        capture['before'] = output[0, -1].detach().float().cpu().numpy().copy()
        changed = output.clone()
        changed[:, -1, :] = changed[:, -1, :] + shift
        capture['after'] = changed[0, -1].detach().float().cpu().numpy().copy()
        return changed
    handle = block.register_forward_hook(hook)
    try:
        yield
    finally:
        handle.remove()


def validate(d, items, complete=False):
    if d.empty:
        assert not complete
        return
    expected = set(itertools.product(items.sample_id, CONDITIONS, range(3)))
    keys = ['item', 'condition', 'rotation']
    assert not d.duplicated(keys).any()
    assert set(map(tuple, d[keys].to_numpy())) <= expected
    cols = ['p_unknown', 'p_stereotype', 'p_anti']
    p = d[cols].to_numpy()
    assert np.isfinite(p).all() and (p >= 0).all() and (p <= 1).all()
    assert np.allclose(p.sum(1), 1, atol=1e-5)
    assert d.choice_mass.between(0, 1.00001).all()
    v = d.filter(regex='^(pre_|post_|delta_)').to_numpy()
    assert np.isfinite(v).all()
    if complete:
        assert len(d) == len(expected)


def saved(out):
    rows = [json.loads(p.read_text()) for p in sorted((Path(out) / 'chunks').glob('trial_*.json'))]
    return pd.DataFrame(rows)


def progress():
    items, source, axes, out = prepare()
    d = saved(out)
    validate(d, items)
    counts = d.groupby('condition').size().reindex(CONDITIONS, fill_value=0) if len(d) else pd.Series(0, index=CONDITIONS)
    return pd.DataFrame({'condition': CONDITIONS, 'saved_trials': counts.to_numpy(), 'planned_trials': 417})


def run():
    """Called only when the notebook user explicitly enables RUN_AXIS_INTERVENTIONS."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    items, source, axes, out = prepare()
    chunks = out / 'chunks'
    chunks.mkdir(exist_ok=True)
    with open(ROOT / 'writer.lock', 'a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        d = saved(out)
        validate(d, items)
        done = set(map(tuple, d[['item', 'condition', 'rotation']].to_numpy())) if len(d) else set()
        plan = list(itertools.product(items.sample_id, CONDITIONS, range(3)))
        missing = [plan[i] for i in np.random.default_rng(SEED).permutation(len(plan)) if plan[i] not in done]
        if not missing:
            validate(d, items, True)
            return out
        write_json(out / 'status.json', dict(state='loading', completed=len(done), total=len(plan)))
        tok = AutoTokenizer.from_pretrained(MODEL, revision=REVISION, local_files_only=True)
        device = 'mps' if torch.backends.mps.is_available() else 'cpu'
        import transformers.modeling_utils as mu
        warmup = mu.caching_allocator_warmup
        if device == 'mps':
            mu.caching_allocator_warmup = lambda *a, **kw: None
        try:
            model = AutoModelForCausalLM.from_pretrained(
                MODEL, revision=REVISION, dtype=torch.float32, attn_implementation='eager',
                device_map={'': device}, low_cpu_mem_usage=True, local_files_only=True).eval()
        finally:
            mu.caching_allocator_warmup = warmup
        try:
            block = model.model.layers[13]
            ids = [tok.encode(str(i), add_special_tokens=False) for i in [1, 2, 3]]
            assert all(len(v) == 1 for v in ids)
            ids = [v[0] for v in ids]
            lookup = items.set_index('sample_id')
            runtime = dict(revision=model.config._commit_hash, torch=torch.__version__, device=device, dtype='float32')
            runtime_file = out / 'runtime.json'
            if runtime_file.exists():
                assert json.loads(runtime_file.read_text()) == runtime, 'Runtime changed; do not mix measurements.'
            else:
                write_json(runtime_file, runtime)
            def score(item, condition, rotation, hooked=True):
                row = lookup.loc[item]
                msg, choices = messages(row, source, rotation)
                text = tok.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
                enc = tok(text, return_tensors='pt').to(device)
                capture = {}
                shift = torch.as_tensor(offset(condition, axes), dtype=torch.float32, device=device)
                with torch.inference_mode():
                    if hooked:
                        with intervention(block, shift, capture):
                            result = model(**enc, use_cache=False, logits_to_keep=1)
                    else:
                        result = model(**enc, use_cache=False, logits_to_keep=1)
                    logits = result.logits[0, -1].float()
                    assert torch.isfinite(logits).all()
                    probs = torch.softmax(logits[ids], 0).cpu().numpy()
                    mass = float(torch.exp(torch.logsumexp(logits[ids], 0) - torch.logsumexp(logits, 0)))
                del result
                return probs, mass, capture, choices
            first = missing[0]
            p, _, _, _ = score(first[0], 'neutral', first[2], False)
            q, _, _, _ = score(first[0], 'neutral', first[2], True)
            error = float(np.max(np.abs(p - q)))
            assert error < 1e-5, 'Zero-hook parity failed. No trial has been saved.'
            write_json(out / 'smoke.json', dict(zero_hook_probability_error=error, graphics_emitted=False))
            for item, condition, rotation in missing:
                probs, mass, capture, choices = score(item, condition, rotation)
                before, after = capture['before'], capture['after']
                shift = offset(condition, axes)
                assert np.max(np.abs(after - before - shift)) < 1e-4
                pre_z, pre_cos = project(before, axes)
                post_z, post_cos = project(after, axes)
                r = lookup.loc[item]
                pm = dict(zip(choices, map(float, probs)))
                anti = next(c for c in choices if c not in ['알 수 없음', r['biased_answer']])
                record = dict(item=item, condition=condition, rotation=int(rotation),
                              p_unknown=pm['알 수 없음'], p_stereotype=pm[r['biased_answer']],
                              p_anti=pm[anti], choice_mass=mass, perturbation_norm=float(np.linalg.norm(shift)))
                for i, axis in enumerate(AXES):
                    record.update({f'pre_cos_{axis}': float(pre_cos[i]), f'post_cos_{axis}': float(post_cos[i]),
                                   f'delta_cos_{axis}': float(post_cos[i] - pre_cos[i]),
                                   f'delta_z_{axis}': float(post_z[i] - pre_z[i])})
                validate(pd.DataFrame([record]), items)
                key = hashlib.sha256(json.dumps([item, condition, int(rotation)]).encode()).hexdigest()[:24]
                file = chunks / f'trial_{key}.json'
                assert not file.exists()
                write_json(file, record)
                done.add((item, condition, rotation))
                write_json(out / 'status.json', dict(state='running', completed=len(done), total=len(plan), time=time.time()))
                if len(done) % 139 == 0:
                    print(f'{len(done)}/{len(plan)}', flush=True)
            d = saved(out)
            validate(d, items, True)
            d.to_csv(out / 'trials.csv', index=False)
            write_json(out / 'status.json', dict(state='measured', completed=len(d), total=len(plan)))
        finally:
            del model
            if device == 'mps':
                torch.mps.empty_cache()
    return out


def analyze(show=True):
    import matplotlib.pyplot as plt
    from english_figures import style, save
    items, source, axes, out = prepare()
    d = saved(out)
    if d.empty or len(d) != 3336:
        print(f'Not measured: {len(d)}/3336 saved. Run manually before interpreting effects.')
        return None
    validate(d, items, True)
    metrics = ['p_unknown', 'p_stereotype', 'p_anti']
    means = d.groupby(['item', 'condition'])[metrics].mean()
    codes = items.cluster.astype('category').cat.codes.to_numpy()
    nc = int(codes.max()) + 1
    weights = np.random.default_rng(SEED).multinomial(nc, np.full(nc, 1/nc), size=N_BOOT)[:, codes].astype(float)
    weights /= weights.sum(axis=1, keepdims=True)
    records = []
    for metric in metrics:
        v = means[metric].unstack().reindex(items.sample_id)
        for axis in AXES:
            delta = (v[axis] - v.neutral).to_numpy()
            draws = weights @ delta
            lo, hi = np.quantile(draws, [.025, .975])
            p = min(1., 2 * min(np.mean(draws <= 0), np.mean(draws >= 0)) + 1/N_BOOT)
            records.append(dict(axis=axis, metric=metric, baseline=float(v.neutral.mean()),
                                treatment=float(v[axis].mean()), estimate=float(delta.mean()),
                                ci_low=float(lo), ci_high=float(hi), p=p, p_holm=None))
    adjusted = 0.
    for i, r in enumerate(sorted([r for r in records if r['metric'] == 'p_unknown'], key=lambda r: r['p'])):
        adjusted = max(adjusted, min(1., r['p'] * (7-i)))
        r['p_holm'] = adjusted
    effects = pd.DataFrame(records)
    effects.to_csv(out / 'effects.csv', index=False)
    means.to_csv(out / 'paired_items.csv')
    d.to_csv(out / 'trials.csv', index=False)
    cross = d.groupby('condition')[[f'delta_z_{k}' for k in AXES]].mean().reindex(AXES)
    cross.columns = AXES
    cross.to_csv(out / 'cross_axis_changes.csv')
    write_json(out / 'summary.json', dict(n_items=139, n_clusters=91, n_trials=len(d),
        primary=[r for r in records if r['metric'] == 'p_unknown'],
        interpretation='Effects of specified L14 interventions; not validated emotion-specific effects.',
        source_trials_unchanged=sha(SOURCE / 'trials.csv') == json.loads((out / 'manifest.json').read_text())['source_trials_sha256']))
    style()
    colors = ['#C34835', '#2868A3', '#279387', '#8167A9', '#CA773B', '#A04F80', '#C2A237']
    labels = ['Uncertainty', 'Fear / anxiety', 'Calm', 'Sadness', 'Anger', 'Desperation', 'Joy']
    fig, axs = plt.subplots(1, 3, figsize=(180/25.4, 92/25.4), layout='constrained')
    for j, (metric, title) in enumerate(zip(metrics, ['Information-insufficient answer', 'Stereotypical answer', 'Anti-stereotypical answer'])):
        for i, (axis, color) in enumerate(zip(AXES, colors)):
            r = effects[(effects.metric == metric) & (effects.axis == axis)].iloc[0]
            axs[j].plot([100*r.ci_low, 100*r.ci_high], [i, i], color=color, lw=1)
            axs[j].scatter(100*r.estimate, i, color=color, marker='o',
                           facecolors=color if j or r.p_holm < .05 else 'white', s=16, linewidths=.8)
        axs[j].axvline(0, color='#999', lw=.6)
        axs[j].set(yticks=range(7), yticklabels=labels if j == 0 else [], xlabel='Change vs. shared baseline (pp)', title=title, ylim=(6.6, -.6))
        axs[j].spines[['top', 'right']].set_visible(False)
    save(fig, out, 'KoBBQ_axis_intervention_effects_en', show)
    fig, ax = plt.subplots(figsize=(115/25.4, 105/25.4), layout='constrained')
    vmax = max(1., float(np.abs(cross.to_numpy()).max()))
    im = ax.imshow(cross, cmap='RdBu', vmin=-vmax, vmax=vmax)
    ax.set(xticks=range(7), xticklabels=['UN','FA','Calm','Sadness','Anger','Desperation','Joy'],
           yticks=range(7), yticklabels=labels, xlabel='Measured concept axis', ylabel='Intervention direction',
           title='Cross-axis changes at layer 14')
    ax.tick_params(axis='x', rotation=45)
    for i in range(7):
        for j in range(7):
            ax.text(j, i, f'{cross.iloc[i,j]:.2f}', ha='center', va='center', fontsize=5.5)
    fig.colorbar(im, ax=ax, label='Change in anchor-standardized projection')
    save(fig, out, 'Cross_axis_intervention_en', show)
    return effects
