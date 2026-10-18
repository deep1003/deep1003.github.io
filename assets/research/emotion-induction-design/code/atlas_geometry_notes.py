"""Audit cached geometry and observed tiles; build a table-based atlas explanation."""
from pathlib import Path
import hashlib
import html
import json
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / 'representation_analysis/emotion_atlas/output'
AXES = ['UN', 'FA', 'calm', 'sadness', 'anger', 'desperation', 'joy']
LABELS = ['UN', 'FA', 'Calm', 'Sadness', 'Anger', 'Desperation', 'Joy']

def build():
    paths = {
        'axes': BASE / 'representation_analysis/results/d335ad178e3c/axes_qwen_L14.npz',
        'cosines': OUTPUT / 'concept_cosines.csv',
        'adjacency': OUTPUT / 'boundary_adjacency.csv',
        'geometry': OUTPUT / 'region_geometry.json',
        'tiles': OUTPUT / 'tile_layout.csv',
        'values': OUTPUT / 'atlas_source_data.csv',
        'trials': BASE / 'representation_analysis/item_category_alignment/output/trial_alignment.csv',
        'pooled': BASE / 'representation_analysis/item_category_alignment/output/item_alignment.csv'}
    cosine = pd.read_csv(paths['cosines'], index_col=0).loc[AXES, AXES]
    adjacency = pd.read_csv(paths['adjacency'], index_col=0).loc[AXES, AXES].astype(bool)
    directions = np.load(paths['axes'])['directions'].astype(float)
    directions /= np.linalg.norm(directions, axis=1, keepdims=True)
    assert np.allclose(directions @ directions.T, cosine.values, atol=1e-12)
    geometry = json.loads(paths['geometry'].read_text())
    sites, weights = np.asarray(geometry['sites']), np.asarray(geometry['weights'])
    polygons = [np.asarray(p) for p in geometry['polygons']]
    audited_adjacency = np.zeros((7, 7), dtype=bool)
    for i in range(7):
        for j in range(i+1, 7):
            normal = 2*(sites[j]-sites[i])
            offset = sites[j]@sites[j] - sites[i]@sites[i] + weights[i] - weights[j]
            points = polygons[i][np.abs(polygons[i]@normal-offset) < 1e-7]
            touching = len(points)>1 and np.max(np.linalg.norm(points[:, None]-points[None, :], axis=-1))>1e-6
            audited_adjacency[i, j] = audited_adjacency[j, i] = touching
    assert np.array_equal(audited_adjacency, adjacency.values)
    values = pd.read_csv(paths['values'])
    mapping = pd.read_csv(paths['tiles'])
    trials = pd.read_csv(paths['trials']); trials = trials[trials.layer==14]
    pooled = pd.read_csv(paths['pooled']); pooled = pooled[pooled.layer==14]
    assert len(trials)==1668 and trials.cluster.nunique()==91 and not trials.duplicated(['item', 'rotation', 'condition']).any()
    assert len(mapping)==2919 and mapping.groupby('axis').size().eq(417).all()
    assert len(values)==11676 and not values.duplicated(['axis', 'item', 'rotation', 'condition']).any()
    assert values.item.nunique()==139 and set(values.rotation)=={0,1,2}
    expected = trials.melt(id_vars=['item','rotation','condition'], value_vars=['cos_'+a for a in AXES],
                           var_name='axis',value_name='original_cosine')
    expected['axis'] = expected.axis.str.removeprefix('cos_')
    joined = values.merge(expected, on=['item','rotation','condition','axis'], validate='one_to_one')
    raw_error = float(np.max(np.abs(joined.cosine-joined.original_cosine)))
    assert raw_error < 1e-12
    baseline = expected[expected.condition=='UN0FA0'].set_index(['item','rotation','axis']).original_cosine
    matched = values.set_index(['item','rotation','axis']).join(baseline.rename('expected_baseline'))
    assert np.allclose(matched.baseline, matched.expected_baseline, atol=1e-12)
    assert np.allclose(values.delta_cosine, values.cosine-values.baseline, atol=1e-12)
    avg = trials.groupby(['item','condition'])[['cos_'+a for a in AXES]].mean().sort_index()
    target = pooled.set_index(['item','condition'])[['cos_'+a for a in AXES]].sort_index()
    mean_error = float(np.abs(avg.to_numpy()-target.to_numpy()).max())
    assert mean_error < 1e-12
    table = pd.DataFrame(index=LABELS, columns=LABELS)
    for i in range(7):
        for j in range(7):
            table.iloc[i,j] = f'{cosine.iloc[i,j]:.3f}' + (' ✓' if adjacency.iloc[i,j] else '')
    table.index.name = 'Axis'
    table.to_csv(OUTPUT / 'similarity_and_contact_table.csv')
    pairs = [dict(axis_1=AXES[i], axis_2=AXES[j], cosine=float(cosine.iloc[i,j]),
                  shares_boundary=bool(adjacency.iloc[i,j])) for i in range(7) for j in range(i+1,7)]
    pd.DataFrame(pairs).to_csv(OUTPUT / 'similarity_and_contact_pairs.csv', index=False)
    example = values[(values.axis=='FA') & (values.condition=='UN1FA1')].iloc[0]
    diagnostic = json.loads((OUTPUT / 'validation.json').read_text())['diagnostics']
    variance = diagnostic['two_dimensional_retained_variance']*100
    url = 'https://deep1003.github.io/assets/research/emotion-induction-design/data/atlas/'
    markup = '''<div class="atlas-geometry-notes">
<h3>그림을 읽기 위한 유사도·인접성 표</h3>
<p><strong>이 표는 관측값의 상관행렬이 아니라, 일곱 고정 개념 방향의 코사인 유사도다.</strong> 각 단위 방향 vᵢ는 3,584차원이며 값은 cᵢⱼ=vᵢᵀvⱼ이다. ✓는 현재 도식에서 두 영역이 실제로 경계를 공유한다는 뜻이며 통계적 유의성 표시는 아니다.</p>
<div style="overflow-x:auto">''' + table.to_html(escape=True, border=0, classes='atlas-similarity-table') + '''</div>
<p>유사도는 배치의 입력이지만 경계를 직접 정하는 임계값은 아니다. 같은 벡터들을 PCA 2차원 사이트로 투영하고, 영역 면적을 같게 하는 가중 보로노이 도형(power diagram)으로 경계를 계산했다. 따라서 유사도가 높아도 경계가 닿지 않을 수 있고, 낮아도 닿을 수 있다. 계층군집은 원래 고차원 관계를 점검하는 별도 분석이며 경계를 생성한 알고리즘은 아니다.</p>
<div style="overflow-x:auto"><table><thead><tr><th>구분</th><th>계산과 해석</th></tr></thead><tbody>
<tr><td>유사도와 배치</td><td>cᵢⱼ=cos(vᵢ,vⱼ), dᵢⱼ=√[2(1−cᵢⱼ)]. 고정 방향을 중심화한 PCA의 두 좌표 sᵢ를 사용한다. 2차원 보존 분산은 VARIANCE%이며 모든 고차원 관계를 보존하지 않는다.</td></tr>
<tr><td>큰 영역의 경계</td><td>영역 i는 ‖x−sᵢ‖²−wᵢ ≤ ‖x−sⱼ‖²−wⱼ를 모든 j에 대해 만족하는 위치다. 두 값이 같은 직선이 경계이며, wᵢ는 일곱 영역의 면적을 같게 맞춘 표시용 가중치다. 면적과 경계 길이는 정서 강도의 측정값이 아니다.</td></tr>
<tr><td>작은 칸 하나</td><td>문항 1개 × 선택지 순서 1개 × 감정 축 1개에 대응한다. 139문항을 각각 세 순서로 측정했으므로 영역당 417칸, 패널당 7×417=2,919칸이다. 일곱 점수는 같은 입력의 은닉 상태에서 계산하며 일곱 번 독립 측정한 표본이 아니다.</td></tr>
<tr><td>색의 수치</td><td>완전한 공지+KoBBQ 입력 뒤 답변 생성 직전 L14 은닉 상태 h에서 aₖ=(h−μₖ)ᵀvₖ/‖h−μₖ‖를 계산한다. 색은 같은 문항·순서·축의 Δaₖ=aₖ(condition)−aₖ(00)이다. 이는 코사인 변화량이며 표준화 z점수나 정서 확률이 아니다.</td></tr>
<tr><td>반복·샘플링·화면 픽셀</td><td>세 순서는 선택지 위치를 순환한 입력의 반복 측정이며, 답변을 무작위로 세 번 생성한 것이 아니다. 이들은 서로 독립적인 417문항이 아니다. 그림을 위한 무작위 샘플링·보간·평활화·임의 값 복제는 없다. 한 소칸은 여러 화면 픽셀로 렌더링되며 화면 픽셀마다 모델을 측정한 것은 아니다. 소칸 안팎의 문항 위치는 범주·템플릿·ID 순서의 고정 재귀 분할이며 국소적 이웃 관계에는 의미 해석이 없다.</td></tr>
</tbody></table></div>
<p><strong>실제 한 칸의 예시</strong> FA 영역의 <code>ITEM</code>, 선택지 순서 0, 조건 11은 −0.109530이고 같은 문항·순서의 조건 00은 −0.120317이다. 색에 사용한 값은 −0.109530−(−0.120317)=<strong>+0.010787</strong>이다. 네 조건은 같은 칸 배치와 같은 색 범위를 사용한다. 00 패널이 단색인 이유는 자기 자신을 뺀 변화가 0이기 때문이다.</p>
<p>고유 문항은 139개이며 91개 범주·템플릿 군집을 공유한다. 입력 조건은 139×4×3=1,668개이고, 각 입력에서 일곱 축을 계산하므로 네 패널에 11,676개의 유사도값이 표시된다. 문항 평균에 사용된 부트스트랩 표본을 이 칸에 배치한 것이 아니다.</p>
<p class="links"><a href="URLconcept_cosines.csv">원래 코사인 행렬</a><a href="URLsimilarity_and_contact_pairs.csv">모든 쌍의 유사도와 접촉 여부</a><a href="URLtile_layout.csv">소칸과 문항 키</a><a href="URLatlas_source_data.csv">소칸별 측정값</a><a href="URLgeometry_and_tiles_audit.json">원자료·경계 재검증</a></p>
</div>'''
    markup = markup.replace('VARIANCE', f'{variance:.2f}').replace('ITEM', html.escape(example['item'])).replace('URL', url)
    extension = BASE / 'representation_analysis/certainty_extension'
    if (extension / 'validation.json').exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location('certainty_table_notes', extension / 'table_notes.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        markup = module.extend_markup(markup)
    (BASE / 'atlas_geometry_explainer.html').write_text(markup)
    audit = dict(n_items=139, n_clusters=91, n_conditions=4, n_rotations=3, n_axes=7, n_input_conditions=1668,
        cells_per_region=417, cells_per_panel=2919, displayed_values=11676,
        shared_boundary_pairs=int(adjacency.to_numpy().sum()//2),
        directions_cosine_matrix_verified=True, boundary_contacts_reconstructed=True,
        tile_values_match_saved_trial_alignments=True, maximum_raw_value_error=raw_error,
        maximum_rotation_mean_error=mean_error, model_inference=False, bootstrap_tiles=False,
        interpolation=False, sampling_for_visualization=False,
        example={k: (v.item() if isinstance(v,np.generic) else v) for k,v in example.to_dict().items()},
        source_sha256={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()},
        explanation_code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (OUTPUT / 'geometry_and_tiles_audit.json').write_text(json.dumps(audit, indent=2))
    return BASE / 'atlas_geometry_explainer.html'

if __name__ == '__main__':
    print(build())
