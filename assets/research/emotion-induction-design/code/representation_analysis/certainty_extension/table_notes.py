"""Render the cached eight-axis table; never load a model or change atlas geometry."""
from pathlib import Path
import json

import pandas as pd
from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parent
PUBLIC = 'https://deep1003.github.io/assets/research/emotion-induction-design/data/l14/certainty-extension/'


def extend_markup(markup):
    atlas8 = BASE / 'atlas8/geometry_and_tiles.html'
    if atlas8.exists():
        return atlas8.read_text()
    validation = json.loads((BASE/'validation.json').read_text())
    matrix = pd.read_csv(BASE/'axis_cosines_qwen_L14_with_certainty.csv', index_col=0)
    names = matrix.index.tolist()
    soup = BeautifulSoup(markup, 'html.parser')
    wrapper = soup.find(class_='atlas-geometry-notes')
    original = wrapper.find('table', class_='atlas-similarity-table')
    contact = {}
    columns = [x.get_text(strip=True) for x in original.find('thead').find('tr').find_all('th')][1:]
    for row in original.find('tbody').find_all('tr'):
        axis = row.find('th').get_text(strip=True)
        for other, cell in zip(columns, row.find_all('td')):
            contact[axis, other] = '✓' in cell.get_text()
    table = soup.new_tag('table', attrs={'class': 'dataframe atlas-similarity-table', 'data-certainty-extension': 'measured-L14'})
    head = soup.new_tag('thead')
    row = soup.new_tag('tr')
    for name in ['Axis']+names:
        cell = soup.new_tag('th', scope='col')
        cell.string = 'CN' if name == 'Certainty' else name
        row.append(cell)
    head.append(row)
    table.append(head)
    body = soup.new_tag('tbody')
    for a in names:
        row = soup.new_tag('tr')
        label = soup.new_tag('th', scope='row')
        label.string = 'CN' if a == 'Certainty' else a
        row.append(label)
        for b in names:
            cell = soup.new_tag('td')
            cell.string = f'{matrix.loc[a, b]:.3f}' + (' ✓' if 'Certainty' not in [a, b] and contact.get((a, b), False) else '')
            if 'Certainty' in [a, b]:
                cell['style'] = 'background:#f3f4f6'
            row.append(cell)
        body.append(row)
    table.append(body)
    original.replace_with(table)
    wrapper.find('p').clear()
    wrapper.find('p').append(BeautifulSoup('<strong>이 표는 관측값의 상관행렬이 아니라, 기존 일곱 고정 개념 방향과 새 Certainty 인지적 평가 방향의 코사인 유사도다.</strong> 각 방향은 Qwen2.5-7B의 L14, 3,584차원 단위 벡터다. ✓는 기존 일곱 영역 사이의 실제 경계 접촉만 표시하며 통계적 유의성이 아니다. Certainty에는 새 영역을 만들지 않았으므로 관련 칸에 ✓를 붙이지 않았다.', 'html.parser'))
    for old in wrapper.select('#certainty-extension-note'):
        old.decompose()
    values = ', '.join(f'{name} {matrix.loc["Certainty", name]:+.3f}' for name in names if name != 'Certainty')
    note = BeautifulSoup(f'''<div id="certainty-extension-note" class="note">
<p><strong>Certainty 추가 측정.</strong> 상황과 판단에 대한 주관적 확실성을 기술한 새 한국어 문장 10쌍을 고정했다. 6쌍으로 확실성−불확실성 평균 차이 방향을 추정하고, 별도 4쌍으로 검증했다. 기존과 같은 모델 revision·FP32·eager·시스템 입력 뒤 답변 시작 직전 위치에서 새 입력 20개만 측정했다. 보류 쌍 정확도 {validation['paired_accuracy']:.2f}, AUC {validation['auc']:.2f}로 기존 검증 기준(각 .75 이상)을 통과했다. 소규모 작성 문장에 대한 탐색적 진단이며 광범위한 구성 타당성을 입증하지 않는다.</p>
<p>{values}.</p>
<p>기존 UN의 대조 문장도 이미 확실성을 기술한다. 그 축의 부호를 뒤집으면 UN과의 유사도는 정의상 −1이다. 여기의 Certainty는 새 문장에서 독립적으로 추정했으므로 그 값이 강제되지 않는다. 기존 일곱 축·행동 결과·아틀라스 경계는 유지했다. 분노와 Certainty의 음의 유사도를 인간의 분노가 불확실하다는 증거로 해석하지 않는다. 이 표는 작성 문장으로 구성한 모델 내부 방향의 관계이며, 감정별 인지적 평가를 직접 측정한 결과가 아니다.</p>
<p class="links"><a href="{PUBLIC}axis_cosines_qwen_L14_with_certainty.csv">8×8 수치 표</a><a href="{PUBLIC}anchors_certainty.json">새 문장과 분할</a><a href="{PUBLIC}validation.json">보류 검증</a><a href="{PUBLIC}certainty_comparison.csv">문장 쌍 제외 민감도</a><a href="{PUBLIC}protocol.json">측정 설정</a></p>
</div>''', 'html.parser')
    table.parent.insert_after(note)
    return str(soup)


if __name__ == '__main__':
    target = BASE.parent.parent/'atlas_geometry_explainer.html'
    target.write_text(extend_markup(target.read_text()))
    print(target)
