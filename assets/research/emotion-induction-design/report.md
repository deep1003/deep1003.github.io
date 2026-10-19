# Fear in the Machine

139문항·6조건 메인 실험

## Storyline

1. L14 emotion atlas의 Reference 대비 표현 변화
2. 실제 프롬프트 토큰의 감정 관련 표현과 위치
3. Reference 대비 UN·CN의 Unknown 선택 차이

UN−R +18.76%p, CN−R −2.95%p; 두 사후비교 모두 Holm2 p<.001. 그림1의축변화는별도Holm20,그림2system-only는기술비교다. 이 흐름은 인과매개의 입증이 아니다.

## 주요 대응 결과

| 비교           |   차이 (%p) | 95% 구간       |   Holm 보정 p |
|:---------------|------------:|:---------------|--------------:|
| UN − Reference |       18.76 | [15.61, 22.03] |        0.0002 |
| CN − Reference |       -2.95 | [-4.30, -1.65] |        0.0002 |

## 방법과 한계

139문항·91군집·6조건·3순서·2,502키. 문항 안에서 세 순서를 먼저 평균한 뒤 같은 템플릿 군집을 모든 조건에 함께 재표집했다. 10,000회·seed20261018, 문항 가중 평균과 점별95% percentile구간이다. 양측 null-centered bootstrap은 |재표집추정량−관측추정량| ≥ |관측추정량|의 꼬리 비율에 (k+1)/(B+1) Monte Carlo 보정을 적용했다. 출판용 사후 검정군은 공지평균2개(Holm2), 조건부4개(Holm4), 축10개×공지2개(Holm20)로 분리했다. 검정군과 구현을 이번 재계산 전에 영수증에 고정했지만, 데이터와 과거 결과를 본 뒤 정한 탐색 분석이므로 사전등록·독립 확증으로 소개하지 않는다. 예전 검정 수치와 구현은 백업 보존한다. 추론은 이 고정 모델·고정 공지에서 선택한 문항 템플릿의 변화에 대한 것이며, 모델·공지 문구 모집단의 변이를 추정한 것이 아니다.

CN에서는 확률50→100%와 확정문장이함께바뀌며,Unknown은모호문항의정답이다. 편향감소·주관감정·특정축의인과효과를입증하지않는다.

## Ablation

| 요인                  | 상태             | 계획                                                                                                                                                   |
|:----------------------|:-----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| 수치 실행 방식        | 완료 · 기술 검증 | 동일 FP32·revision의 층별 스트리밍 대조. 18입력, 최대 확률차 0.00756%p, L14 최대 절대차 0.0000381. 반복 차이 0. 표현·행동 조작의 인과 ablation은 아님. |
| 길이·표현 통제        | 계획 · 미실행    | 같은 길이의 비정서 공지와 어휘 대조를 사전에 고정해 문장 길이·Unknown 표현 중복의 설명을 분리한다.                                                     |
| 확률과 확정 표현 분리 | 계획 · 미실행    | 50%→100% 숫자 변화와 선정 확정 문장을 별개 요인으로 조작한다. 현재 CN 효과를 순수 certainty 효과로 바꾸어 해석하지 않는다.                             |
| 층·측정 위치          | 계획 · 미실행    | 동일 6조건에서 다른 층과 사전 지정 위치를 비교한다. L14가 최적·대표 층이라고 결과를 보고 선택하지 않는다.                                              |
| 축 구축과 특이성      | 계획 · 미실행    | 학습쌍 하나 제외 안정성, 독립 상황 판별, 별도 중립 PCA ablation. 현행 축은 그대로 보존한다.                                                            |
| 다른 모델·정밀도      | 계획 · 미실행    | 동일 프롬프트·문항·채점으로 별도 실행을 고정한다. 모델·정밀도·템플릿이 함께 바뀐 결과를 순수 모델 크기 효과로 부르지 않는다.                           |
| 감정 방향 개입        | 계획 · 미실행    | 행동과의 인과 연결을 주장하려면 개입 방향·강도·대조·기능 보존을 먼저 고정한 steering 실험이 필요하다.                                                  |

## 참고문헌

1. [Tiedens & Linton (2001). Judgment under emotional certainty and uncertainty: The effects of specific emotions on information processing. J Pers Soc Psychol 81, 973–988.](https://pubmed.ncbi.nlm.nih.gov/11761319/)
2. [Coda-Forno et al. (2024 revision). Inducing anxiety in large language models can induce bias.](https://arxiv.org/html/2304.11111v2)
3. [Anthropic Research (2026). Emotion concepts in a large language model.](https://www.anthropic.com/research/emotion-concepts-function)
4. [Parrish et al. (2022). BBQ: A hand-built bias benchmark for question answering. Findings of ACL.](https://aclanthology.org/2022.findings-acl.165/)
5. [Jin et al. (2024). KoBBQ: Korean Bias Benchmark for Question Answering. TACL 12, 507–524.](https://aclanthology.org/2024.tacl-1.28/)
6. [Nature research figure guide. Preparing figures: specifications.](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)
7. [Krzywinski & Altman (2013). Error bars. Nature Methods 10, 921–922.](https://www.nature.com/articles/nmeth.2659)
8. [Show the dots in plots (2017). Nature Biomedical Engineering 1, 0079.](https://www.nature.com/articles/s41551-017-0079)

## 그림 복원
그림 1. 칭찬 없는 6조건의 벌집형 emotion atlas. 각 감정 영역은 139문항 × 선택지 순서 3회의 실제 측정값이다. 색은 같은 문항·순서의 R0 대비 감정 축 유사도 변화이며, 어두움에서 감정색과 노랑으로 갈수록 값이 커진다. 모든 패널과 축에 동일한 수치 범위를 적용했다. 영역은 축 벡터의 PCA 위치로 만든 동일 면적 도식이다. 신경망의 실제 공간이나 시간적 활성화 과정이 아니며, 감정 간 밝기를 감정 강도의 순위로 해석하지 않는다. Certainty·Uncertainty 평가 축은 별도 표에 보존했다.

그림 2. 실제 system prompt의 L14 토큰별 감정 축 유사도. 왼쪽은 감정 8축의 표준화된 값을 실제 토큰 위치에 따라 겹쳐 그린 곡선이다. 오른쪽은 원문 문자마다 상대적으로 가장 높은 감정 축의 색을 표시한다. 여섯 프롬프트의 문자값을 모아 축별 z점수를 계산하며 z > 0.5에서 색칠하고 2.5에서 색 농도를 포화시켰다. 겹친 byte 토큰은 문자 위치에서 평균했다. 표준화 최고값은 감정 발생 확률이나 절대적인 감정 강도가 아니다. system-only 기술 분석으로 질문 뒤 상태의 통계와 구분한다.

기존 모든 그림은 보존했다. 복원 문헌은 restored_literature.html을 참조한다.