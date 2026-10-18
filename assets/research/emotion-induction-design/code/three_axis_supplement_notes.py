"""Publication explanation and compact tables for cached S3 uncertainty estimates."""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / 'representation_analysis/three_axis_supplement/output'
NAMES = {'FA':'공포·불안(FA)', 'desperation':'절박함', 'anger':'분노'}

def build_notes():
    data = pd.read_csv(OUTPUT/'behavior_associations.csv')
    sensitivity = pd.read_csv(OUTPUT/'contrast_sensitivity.csv')
    compact = pd.DataFrame([{
        '방향':NAMES[r.axis],
        '평균 유사도 변화 [95% 구간]':f'{r.mean_delta_cosine:.6f} [{r.mean_ci_low:.6f}, {r.mean_ci_high:.6f}]',
        '응답 변화와 Spearman ρ [95% 구간]':f'{r.spearman_rho:+.3f} [{r.rho_ci_low:+.3f}, {r.rho_ci_high:+.3f}]'}
        for r in data.itertuples()])
    other = pd.DataFrame([{'대비':r.contrast,'방향':NAMES[r.axis],
        'Spearman ρ [95% 구간]':f'{r.spearman_rho:+.3f} [{r.rho_ci_low:+.3f}, {r.rho_ci_high:+.3f}]'}
        for r in sensitivity.itertuples()])
    markup = '''<div class="s3-reviewed-notes"><h3>유사도 증가, 문구 효과, 문항별 연관성을 구분한다</h3>
<p><strong>절박함 방향의 평균 유사도는 증가했지만, 그 증가량이 큰 문항에서 정보 부족 응답 확률도 크게 증가한다는 관계는 뚜렷하지 않았다.</strong> 이것은 절박함이 판단에 영향을 주지 못한다는 인과적 무효 증거가 아니다.</p>
<p>여기서 P<sub>unknown</sub>은 세 선택지 안에서 정규화한 모델의 ‘알 수 없음’ 확률이다. 영문에서는 <em>P(Cannot be determined)</em>로 표기하며 기존 <em>information-insufficient response probability</em>와 같은 변수다. 실제 답변을 반복 생성해 얻은 선택 빈도가 아니다. S3는 같은 문항의 11−00 유사도 변화와 확률 변화의 관계를 측정한다.</p>
<div style="overflow-x:auto">''' + compact.to_html(index=False,border=0) + '''</div>
<p>각 구간은 91개 범주·템플릿 군집을 10,000회 복원 추출한 보정 전 95% 백분위 구간이다. 같은 군집 추출을 모든 축·대비에 적용하고 각 군집의 전체 문항을 함께 포함했다. 선택지 순서는 문항 안에서 먼저 평균했다. 상관계수의 구간이 0을 포함한다고 무효 효과나 동등성이 입증되는 것은 아니다.</p>
<p><strong>FA 문구의 효과와 내부 FA 유사도의 상관은 다른 질문이다.</strong> FA 문구 평균 효과는 기존 주요 분석에서 +3.95%p(95% 구간 +3.05~+4.99%p, Holm p=.0003)였다. 반면 S3의 ρ=0.085는 내부 유사도가 많이 달라진 문항이 더 큰 응답 변화를 보이는지를 묻는다. 양의 평균 문구 효과와 약한 문항별 상관은 동시에 성립할 수 있다. 내부 FA 방향 자체의 인과 효과는 아직 측정하지 않았다.</p>
<p>FA·절박함·분노 유사도 변화 사이에는 강한 동반 변화가 관찰되지만, 고정 축도 서로 겹친다. 이 둘을 독립적인 세 정서 기제가 함께 작동했다는 증거로 해석하지 않는다. 축별 변화량의 크기도 공통 단위의 정서 강도 서열은 아니다.</p>
<details><summary>사후 민감도 분석 · 동일 지표의 세 대비를 모두 공개</summary>
<p>주 그림은 11−00을 유지한다. 01−00과 11−10에서도 세 방향을 모두 같은 방법으로 확인했으며, 유리한 대비만 선택하지 않았다. 특히 FA 정렬과 응답 변화의 상관은 01−00에서 음수이고 11−10에서는 더 약하다. 이는 안정적인 강한 양의 관계를 뒷받침하지 않으며, 어느 대비도 정서의 인과 효과를 식별하지 않는다. 모든 구간은 개별 95% 구간이며 다중비교 보정이나 새로운 확증 검정을 추가하지 않았다.</p>
<div style="overflow-x:auto">''' + other.to_html(index=False,border=0) + '''</div></details>
<details><summary>세 전문 역할의 AI 자문과 측정·통계 한계</summary>
<p>통계, LLM 내부 측정, 논문 시각화 역할의 AI 검토 세 건을 별도로 수행했다. 인간 전문가의 외부 동료심사는 아니다. 세 검토 모두 ΔP<sub>unknown</sub> 유지, 군집 신뢰구간 추가, 인과적 무효 단정 금지에 동의했다.</p>
<p>상관이 강해지는 지표·층·문항·대비를 사후에 고르거나 네 조건을 독립 관측처럼 합치지 않는다. 고정관념 선호 자체를 묻는 후속 연구라면 별도의 지표 계획이 필요하지만, 여기서는 결과를 보고 지표를 교체하지 않았다. 시스템 공지의 기준 문장으로 구성한 축을 전체 KoBBQ 입력에 적용한 전이 타당도와 특이성도 추가 검증이 필요하다. 천장·바닥 효과와 좁은 유사도 변화 범위는 진단 대상이며 현재 연관성의 원인으로 확정하지 않는다.</p>
<p>그림의 회색 선은 기술적 OLS 적합선이며 Spearman ρ의 적합선이나 인과 효과가 아니다. Spearman ρ는 단조 연관의 요약이다. 약한 ρ만으로 비선형 관계까지 배제할 수 없으며, 벡터의 기능적 기여에는 별도 개입과 대조가 필요하다.</p>
<p><a href="https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html">Spearman 정의 · SciPy</a> · <a href="https://arxiv.org/abs/2310.01405">표현 읽기와 개입 · Representation Engineering</a> · <a href="https://aclanthology.org/2024.tacl-1.28/">KoBBQ 원 논문</a></p></details></div>'''
    (OUTPUT/'Interpretation.html').write_text(markup)
    return OUTPUT/'Interpretation.html'

if __name__=='__main__':
    print(build_notes())
