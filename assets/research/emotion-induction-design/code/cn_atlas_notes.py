"""Similarity, contact and tile methods for the cached eight-axis atlas."""
from pathlib import Path
import json
import pandas as pd

BASE=Path(__file__).resolve().parent
DATA=BASE/'representation_analysis/certainty_extension/atlas8'
PUBLIC='https://deep1003.github.io/assets/research/emotion-induction-design/data/atlas-cn/'


def render():
    matrix=pd.read_csv(DATA/'concept_cosines.csv',index_col=0)
    adj=pd.read_csv(DATA/'boundary_adjacency.csv',index_col=0)
    validation=json.loads((DATA/'validation.json').read_text())
    retained=validation['two_dimensional_retained_variance']*100
    table='<table class="dataframe atlas-similarity-table"><thead><tr><th scope="col">Axis</th>'
    table+=''.join(f'<th scope="col">{a}</th>' for a in matrix.index)+'</tr></thead><tbody>'
    for a in matrix.index:
        table+=f'<tr><th scope="row">{a}</th>'
        for b in matrix.columns:
            table+=f'<td>{matrix.loc[a,b]:.3f}'+(' ✓' if adj.loc[a,b] else '')+'</td>'
        table+='</tr>'
    table+='</tbody></table>'
    rows=[('유사도와 배치',f'cᵢⱼ=cos(vᵢ,vⱼ), dᵢⱼ=√[2(1−cᵢⱼ)]. 여덟 고정 방향을 중심화한 PCA의 두 좌표 sᵢ를 사용한다. 2차원 보존 분산은 {retained:.2f}%이며 모든 고차원 관계를 보존하지 않는다.'),
          ('큰 영역의 경계','영역 i는 ‖x−sᵢ‖²−wᵢ ≤ ‖x−sⱼ‖²−wⱼ를 모든 j에 대해 만족하는 위치다. 두 값이 같은 직선이 경계이며, wᵢ는 여덟 영역의 면적을 같게 맞춘 표시용 가중치다. 면적과 경계 길이는 감정 강도의 측정값이 아니다. CN 추가에 따라 PCA·경계·인접성을 다시 계산했으며 기존 일곱 영역의 경계를 그대로 복사하지 않았다.'),
          ('작은 칸 하나','문항 1개 × 선택지 순서 1개 × 개념 축 1개에 대응한다. 139문항을 각각 세 순서로 측정했으므로 영역당 417칸, 패널당 8×417=3,336칸이다. 여덟 점수는 같은 입력의 은닉 상태에서 계산하며 여덟 번 독립 측정한 표본이 아니다.'),
          ('색의 수치','완전한 공지+KoBBQ 입력 뒤 답변 생성 직전 L14 은닉 상태 h에서 aₖ=(h−μₖ)ᵀvₖ/‖h−μₖ‖를 계산한다. 색은 같은 문항·순서·축의 Δaₖ=aₖ(condition)−aₖ(00)이다. 이는 코사인 변화량이며 표준화 z점수나 정서 확률이 아니다. 모든 축·조건의 수치 범위는 −0.008~+0.016으로 같다. 색상은 축을 구분하며, 서로 다른 색상 램프의 시각적 밝기가 정확히 같은 지각적 크기를 뜻하지 않는다.'),
          ('반복·샘플링·화면 픽셀','세 순서는 선택지 위치를 순환한 입력의 반복 측정이며, 답변을 무작위로 세 번 생성한 것이 아니다. 이들은 서로 독립적인 417문항이 아니다. 그림을 위한 무작위 샘플링·보간·평활화·임의 값 복제는 없다. 한 소칸은 여러 화면 픽셀로 렌더링되며 화면 픽셀마다 모델을 측정한 것은 아니다. 소칸 안팎의 문항 위치는 범주·템플릿·ID 순서의 고정 재귀 분할이며 국소적 이웃 관계에는 의미 해석이 없다.')]
    methods='<table><thead><tr><th>구분</th><th>계산과 해석</th></tr></thead><tbody>'+''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a,b in rows)+'</tbody></table>'
    return f'''<div class="atlas-geometry-notes" data-atlas-version="eight-axis-CN">
<h3>그림을 읽기 위한 유사도·인접성 표</h3>
<p><strong>이 표는 관측값의 상관행렬이 아니라, 여덟 고정 개념 방향의 코사인 유사도다.</strong> CN은 Certainty(확실성)이며 감정명이 아니라 인지적 평가의 대조 개념이다. 각 단위 방향 vᵢ는 3,584차원이며 값은 cᵢⱼ=vᵢᵀvⱼ이다. ✓는 아래 8영역 도식에서 두 영역이 실제로 경계를 공유한다는 뜻이며 통계적 유의성 표시는 아니다.</p>
<div style="overflow-x:auto">{table}</div>
<p>유사도는 배치의 입력이지만 경계를 직접 정하는 임계값은 아니다. 같은 벡터들을 PCA 2차원 사이트로 투영하고, 영역 면적을 같게 하는 가중 보로노이 도형(power diagram)으로 경계를 계산했다. 따라서 유사도가 높아도 경계가 닿지 않을 수 있고, 낮아도 닿을 수 있다. 계층군집은 원래 고차원 관계를 점검하는 별도 분석이며 경계를 생성한 알고리즘은 아니다.</p>
<div style="overflow-x:auto">{methods}</div>
<p><strong>실제 한 칸의 예시</strong> FA 영역의 <code>age-001b-002-amb-cnt</code>, 선택지 순서 0, 조건 11은 −0.109530이고 같은 문항·순서의 조건 00은 −0.120317이다. 색에 사용한 값은 −0.109530−(−0.120317)=<strong>+0.010787</strong>이다. 네 조건은 같은 칸 배치와 같은 색 범위를 사용한다. 00 패널은 축마다 모든 변화가 0이므로 각 영역 안이 단색이며, 영역 사이 색상은 축 식별용이다.</p>
<p>고유 문항은 139개이며 91개 범주·템플릿 군집을 공유한다. 입력 조건은 139×4×3=1,668개이고, 각 입력에서 여덟 축을 계산하므로 네 패널에 13,344개의 정렬값이 표시된다. 문항 평균에 사용된 부트스트랩 표본을 이 칸에 배치한 것이 아니다. 기존 일곱 축의 점수는 보존했고 CN 점수만 저장된 동일 은닉 상태에서 추가 계산했다. 모델과 행동 실험을 다시 실행하지 않았다.</p>
<details id="certainty-extension-note"><summary>CN 방향의 구성과 해석 범위</summary><p>독립적으로 작성한 확실성·불확실성 문장 10쌍 중 6쌍으로 CN 방향을 추정하고 보류한 4쌍에서 검증했다. 보류 쌍 정확도 1.00, AUC 1.00은 소규모 작성 문장의 탐색적 진단이며 광범위한 구성 타당성을 입증하지 않는다. CN은 기존 UN의 단순 부호 반전이 아니다. CN과 감정 축의 코사인은 인간의 감정별 인지적 평가를 직접 검증한 값이 아니며, 감정 경험이나 행동 원인을 입증하지 않는다.</p></details>
<p class="links"><a href="{PUBLIC}concept_cosines.csv">8×8 코사인 표</a><a href="{PUBLIC}boundary_adjacency.csv">새 경계 인접성</a><a href="{PUBLIC}tile_layout.csv">소칸과 문항 키</a><a href="{PUBLIC}atlas_source_data.csv">소칸별 측정값</a><a href="{PUBLIC}validation.json">보존·경계 검증</a><a href="{PUBLIC}hierarchical_linkage.csv">계층군집 점검</a></p></div>'''

if __name__=='__main__':
    (DATA/'geometry_and_tiles.html').write_text(render())
