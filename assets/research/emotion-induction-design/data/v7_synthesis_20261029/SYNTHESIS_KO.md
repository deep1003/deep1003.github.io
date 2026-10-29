# v7 다중 모델 통합 분석 확정본

2026년 10월 29일 작성. onpolicy 파일럿은 사용자 결정에 따라 제외했다. 기존 v7의 고정 입력과 원결과만 분석했으며 모델 추론을 새로 실행하지 않았다.

## 자료와 검증

KoBBQ는 다섯 모델 각각 108문항 × 5조건으로 540건, 합계 2,700건이다. DiscrimEval은 네 모델 각각 70질문 × 5인종 × 3성별 × 5조건으로 5,250건, 합계 21,000건이다. 전체 23,700건에서 키 중복, 조건 균형, 유한값, 확률 항등식과 모델 간 표본 일치를 확인했다. DiscrimEval 21,000건의 저장 활성값과 입력 해시를 다시 검사했다. KoBBQ는 CSV 판독값과 렌더링 자료를 보존했으나 모든 시행의 원 활성값 파일이 저장된 것은 아니다. 기존 공개 효과 추정치 36개와 독립 재계산한 평균 효과가 반올림 오차 범위에서 일치했다.

## 지표와 계산

문항 i의 보류 효과는 $d_i=100[p_{unknown,i,T}-p_{unknown,i,C}]$이며 전체 효과는 $\bar d=n^{-1}\sum_i d_i$다. KoBBQ의 분모는 조건별 108문항이고 T와 C는 짝지은 위협과 기록이다. 예를 들어 Qwen의 평균 보류 확률 84.012%에서 76.335%를 빼면 약 +7.677%p다.

사람 지목 중 고정관념 선호는 문항별 $s_i=p_{stereo,i}/(p_{stereo,i}+p_{anti,i})$를 먼저 계산한 후 평균한다. 평균 확률의 비율로 바꾸지 않는다. 따라서 보류 변화와 조건부 고정관념 선호는 서로 다른 지표다.

DiscrimEval은 $m_i=\log\sum_{t\in\{yes,Yes\}}e^{l_{it}}-\log\sum_{t\in\{no,No\}}e^{l_{it}}$, $q_i=\sigma(m_i)$다. q의 분모는 네 선택 토큰에 실린 확률 질량이다. 예를 들어 m=0이면 q=0.5이고 m=1이면 q≈0.731이다. 평균 q와 평균 m은 비선형성 때문에 서로 다른 효과를 나타낸다. 각 조건의 1,050사례를 70질문으로 묶어 인구집단 15개 조합을 질문 내에서 평균한 후 질문을 동일 가중한다.

V 조절 효과는 $(T_V-C_V)-(T-C)$, 모델 간 직접 차이는 $d_{i,A}-d_{i,B}$다. 집단 격차 변화는 질문별 $(q_{g,T}-q_{ref,T})-(q_{g,C}-q_{ref,C})$다. 부호 있는 평균 격차와 질문별 절대 격차는 별도 열로 제공한다.

## 통계 방법과 범위

기존 분석을 보존하고 후속 통합 분석을 별도 수행했다. 새로운 가설을 사전등록했다고 주장하지 않는다. 3,000회 군집 부트스트랩으로 개별 95% 신뢰구간을 계산했다. 재표집 seed는 KoBBQ 20261030, DiscrimEval 20261029다. 추가 p값은 19,999회 군집별 부호 반전과 plus-one 보정으로 계산했다. 이는 차이 분포의 부호 대칭 가정에 의존하는 모형 기반 민감도 분석이며 무작위 조건 배정에 근거한 검정이 아니다. 기존 p_boot와 다른 p값임을 명시한다. 신뢰구간은 동시 신뢰구간이 아니다.

행동 기본·V 36개, V 조절 18개, 직접 모델 비교 96개, 집단 격차 96개를 각각 하나의 가족으로 묶어 Holm 보정했다. 감정 관련 108개 군집 단위 Spearman 상관은 근사 p값에 BH FDR 보정을 적용했다. 이 보정은 과거 실험 설계 선택과 모든 연구자 자유도를 해결하지 못한다. 감정 상관은 인과 분석이 아니다.

## 보정 후 논문에서 강조할 구체적 발견

Llama 3.2에서 Llama 3.1을 뺀 KoBBQ 기본 보류 효과 차이는 +14.69%p [12.04, 17.35]이며 96개 직접 비교의 Holm 보정 p=0.0048이다. 같은 계열에서도 방향이 달라 모델 크기만으로 설명할 수 없으며 기기·템플릿·학습 차이가 함께 남는다.

DiscrimEval의 V 조절 효과는 Qwen −11.59%p, DeepSeek −3.91%p, Gemma +4.73%p, Llama 3.2 −0.46%p다. Gemma에서 Qwen을 뺀 직접 조절 효과 차이는 +16.32%p [11.98, 21.03], Holm p=0.0048이다. V 단서가 위협 효과를 일괄 소거한다는 설명은 맞지 않는다.

주요 행동 36개 중 보정 후 남은 대비는 10개다. 특히 Llama 3.2 DiscrimEval의 기본·V 효과는 확률과 로그 비율 모두 이 가족의 Holm 보정 후 0과 구분되지 않았다. 기존 개별 구간의 로그 비율 감소와 보정 후 결과를 구분한다.

집단 격차 96개 중 9개가 보정 후 남았다. DeepSeek의 기본 Black−white 긍정 확률 격차는 1.43%p에서 0.51%p로 약 0.92%p 감소했다. Llama 3.2의 기본 Hispanic−white 격차는 0.66%p에서 1.47%p로 약 0.81%p 증가했으며, V에서도 +0.84%p 증가했다. Gemma에서는 Black−white 로그 비율 격차가 기본·V 모두 증가했다. 따라서 고정관념 선호의 불확실성을 모든 집단 편향 효과의 부재로 확대할 수 없다.

감정 상관 108개 중 BH 보정 후 6개가 남았다. Fear와 행동의 관계는 DeepSeek DiscrimEval의 로그 비율에서만 남았고 기본 rho=−0.426, V rho=−0.458이었다. Qwen·Gemma·Llama 3.2의 Fear 상관은 이 가족에서 남지 않았다. Fear가 높아질수록 항상 편향이 증가한다는 일반 법칙을 지지하지 않으며, 상관의 부재가 독립성의 증명도 아니다.


## 선택지 정규화에 따른 해석 정정

이 결과는 자유 생성 응답 비율이 아니라 특정 선택 토큰의 점수다. A/B/C 조건부 확률은 전체 어휘에서 세 선택지에 실린 질량으로 다시 나눈다. Gemma의 기본 기록·위협 조건 평균 선택지 질량은 각각 30.04%, 14.75%이며 Llama 3.2는 61.89%, 51.41%다. 따라서 보류의 조건부 확률 변화만으로 실제 자유 응답에서 보류가 늘었다고 단정할 수 없다.

전체 어휘 기준 unknown 선택 토큰 질량의 변화는 p_unknown × choice_mass로 계산했다. Gemma 기본 효과는 조건부 +21.07%p와 달리 전체 어휘 질량 기준 −12.98%p [−16.70, −9.17]다. Llama 3.2 기본 효과도 조건부 +6.40%p지만 전체 어휘 질량 기준 −0.08%p [−1.47, 1.23]다. Qwen은 +7.65%p로 조건부 결과와 가깝다. 따라서 Gemma의 큰 조건부 보류 효과를 더 강한 자기보존이나 더 신중한 행동으로 해석하지 않는다.

DiscrimEval Gemma의 yes/no 선택지 질량도 기본 기록 76.28%, 위협 79.13%로 다른 모델보다 낮다. 전체 어휘 긍정 토큰 질량 기준 V 조절 효과는 Qwen −11.66%p, DeepSeek −3.88%p, Gemma +3.61%p, Llama 3.2 −0.52%p로 조건부 결과의 방향 차이가 유지된다. 이 추가 표는 품질 점검 후 확장한 기술적 민감도 분석이며 개별 구간만 제공하고 새 p값이나 보정 후 발견을 추가하지 않았다. 전체 어휘 토큰 질량도 완성된 자유 응답의 빈도는 아니다.

| model    | contrast   |      est |       lo |      hi |
|:---------|:-----------|---------:|---------:|--------:|
| Qwen     | main       |   7.6509 |   3.1133 | 12.5187 |
| Qwen     | V          |   7.6856 |   3.7053 | 12.1237 |
| Llama31  | main       |  -9.7046 | -11.7838 | -7.6301 |
| Llama31  | V          |  -6.3458 |  -8.1117 | -4.4515 |
| DeepSeek | main       |   2.1777 |   0.2897 |  3.8678 |
| DeepSeek | V          |  -1.3238 |  -3.3572 |  0.5272 |
| Gemma2   | main       | -12.9790 | -16.6963 | -9.1746 |
| Gemma2   | V          |  31.4589 |  26.7162 | 36.2353 |
| Llama32  | main       |  -0.0795 |  -1.4741 |  1.2281 |
| Llama32  | V          |   2.2390 |   1.1290 |  3.3647 |

| model    | contrast     |      est |       lo |      hi |
|:---------|:-------------|---------:|---------:|--------:|
| Qwen     | main         |   5.2915 |   2.1633 |  9.0768 |
| Qwen     | V            |  -6.3651 | -10.5020 | -2.3391 |
| Qwen     | V_minus_main | -11.6566 | -15.3580 | -8.3209 |
| DeepSeek | main         |   2.1702 |   0.7631 |  3.7617 |
| DeepSeek | V            |  -1.7137 |  -3.4532 |  0.1896 |
| DeepSeek | V_minus_main |  -3.8840 |  -4.8178 | -3.0193 |
| Gemma2   | main         |   1.7633 |  -1.6543 |  5.2437 |
| Gemma2   | V            |   5.3735 |   1.3241 |  9.2583 |
| Gemma2   | V_minus_main |   3.6101 |   1.8455 |  5.4647 |
| Llama32  | main         |  -1.0160 |  -2.7339 |  0.8199 |
| Llama32  | V            |  -1.5333 |  -3.1575 |  0.1667 |
| Llama32  | V_minus_main |  -0.5173 |  -1.5639 |  0.4558 |
## 주요 효과

| task        | model    | metric    | contrast   | effect_95ci             |   p_raw |   p_holm | reject_holm   |
|:------------|:---------|:----------|:-----------|:------------------------|--------:|---------:|:--------------|
| KoBBQ       | Qwen     | p_unknown | main       | +7.68 [+3.14, +12.56]   |  0.0010 |   0.0270 | True          |
| KoBBQ       | Qwen     | p_unknown | V          | +7.70 [+3.71, +12.16]   |  0.0001 |   0.0043 | True          |
| KoBBQ       | Qwen     | p_sgp     | main       | -1.97 [-7.12, +3.25]    |  0.4700 |   1.0000 | False         |
| KoBBQ       | Qwen     | p_sgp     | V          | -0.97 [-5.82, +3.94]    |  0.7100 |   1.0000 | False         |
| KoBBQ       | Llama31  | p_unknown | main       | -8.30 [-10.82, -5.83]   |  0.0001 |   0.0018 | True          |
| KoBBQ       | Llama31  | p_unknown | V          | -0.41 [-2.75, +2.06]    |  0.7350 |   1.0000 | False         |
| KoBBQ       | Llama31  | p_sgp     | main       | -0.66 [-2.84, +1.49]    |  0.5530 |   1.0000 | False         |
| KoBBQ       | Llama31  | p_sgp     | V          | -0.29 [-2.85, +2.20]    |  0.8290 |   1.0000 | False         |
| KoBBQ       | DeepSeek | p_unknown | main       | +2.36 [+0.48, +4.07]    |  0.0056 |   0.1220 | False         |
| KoBBQ       | DeepSeek | p_unknown | V          | -0.70 [-2.91, +1.25]    |  0.5490 |   1.0000 | False         |
| KoBBQ       | DeepSeek | p_sgp     | main       | -2.01 [-4.73, +0.45]    |  0.1180 |   1.0000 | False         |
| KoBBQ       | DeepSeek | p_sgp     | V          | +0.22 [-2.93, +3.33]    |  0.8880 |   1.0000 | False         |
| KoBBQ       | Gemma2   | p_unknown | main       | +21.07 [+14.64, +28.23] |  0.0001 |   0.0018 | True          |
| KoBBQ       | Gemma2   | p_unknown | V          | +25.33 [+18.86, +32.34] |  0.0001 |   0.0018 | True          |
| KoBBQ       | Gemma2   | p_sgp     | main       | +0.35 [-3.51, +4.18]    |  0.8680 |   1.0000 | False         |
| KoBBQ       | Gemma2   | p_sgp     | V          | +0.27 [-3.60, +4.21]    |  0.8930 |   1.0000 | False         |
| KoBBQ       | Llama32  | p_unknown | main       | +6.40 [+4.73, +8.13]    |  0.0001 |   0.0018 | True          |
| KoBBQ       | Llama32  | p_unknown | V          | +11.35 [+9.61, +13.07]  |  0.0001 |   0.0018 | True          |
| KoBBQ       | Llama32  | p_sgp     | main       | -1.41 [-4.14, +1.38]    |  0.3350 |   1.0000 | False         |
| KoBBQ       | Llama32  | p_sgp     | V          | -0.88 [-3.26, +1.42]    |  0.4650 |   1.0000 | False         |
| DiscrimEval | Qwen     | q_yes     | main       | +5.43 [+2.31, +9.19]    |  0.0007 |   0.0196 | True          |
| DiscrimEval | Qwen     | q_yes     | V          | -6.16 [-10.27, -2.16]   |  0.0026 |   0.0638 | False         |
| DiscrimEval | Qwen     | margin    | main       | +0.17 [-0.37, +0.72]    |  0.5560 |   1.0000 | False         |
| DiscrimEval | Qwen     | margin    | V          | -2.73 [-3.41, -2.05]    |  0.0001 |   0.0018 | True          |
| DiscrimEval | DeepSeek | q_yes     | main       | +2.17 [+0.76, +3.75]    |  0.0046 |   0.1100 | False         |
| DiscrimEval | DeepSeek | q_yes     | V          | -1.74 [-3.47, +0.17]    |  0.0559 |   1.0000 | False         |
| DiscrimEval | DeepSeek | margin    | main       | +0.02 [-0.10, +0.14]    |  0.7070 |   1.0000 | False         |
| DiscrimEval | DeepSeek | margin    | V          | -0.59 [-0.81, -0.37]    |  0.0001 |   0.0018 | True          |
| DiscrimEval | Gemma2   | q_yes     | main       | +0.94 [-3.57, +5.42]    |  0.6990 |   1.0000 | False         |
| DiscrimEval | Gemma2   | q_yes     | V          | +5.66 [+0.44, +10.69]   |  0.0321 |   0.6730 | False         |
| DiscrimEval | Gemma2   | margin    | main       | -0.04 [-0.41, +0.32]    |  0.8390 |   1.0000 | False         |
| DiscrimEval | Gemma2   | margin    | V          | +0.34 [-0.04, +0.70]    |  0.0883 |   1.0000 | False         |
| DiscrimEval | Llama32  | q_yes     | main       | -0.90 [-2.63, +0.96]    |  0.3390 |   1.0000 | False         |
| DiscrimEval | Llama32  | q_yes     | V          | -1.36 [-2.98, +0.35]    |  0.1020 |   1.0000 | False         |
| DiscrimEval | Llama32  | margin    | main       | -0.29 [-0.48, -0.11]    |  0.0022 |   0.0559 | False         |
| DiscrimEval | Llama32  | margin    | V          | -0.25 [-0.43, -0.08]    |  0.0047 |   0.1100 | False         |

## 직접 모델 비교

96개 직접 비교 중 Holm 보정 후 33개가 0과 구분됐다. 한 모델에서만 유의하다는 사실로 모델 차이를 주장하지 않았다. 아래는 기본 조건의 보류 또는 긍정 확률 효과 차이다. 차이의 방향은 model_a에서 model_b를 뺀 값이다.

| task        | model_a   | model_b   | metric    |      est |       lo |       hi |   p_holm | reject_holm   |
|:------------|:----------|:----------|:----------|---------:|---------:|---------:|---------:|:--------------|
| KoBBQ       | Qwen      | Llama31   | p_unknown |  15.9725 |  10.5152 |  21.4599 |   0.0048 | True          |
| KoBBQ       | Qwen      | DeepSeek  | p_unknown |   5.3168 |   0.6206 |  10.2775 |   1.0000 | False         |
| KoBBQ       | Qwen      | Gemma2    | p_unknown | -13.3924 | -21.8807 |  -5.1184 |   0.1070 | False         |
| KoBBQ       | Qwen      | Llama32   | p_unknown |   1.2792 |  -3.6751 |   6.4221 |   1.0000 | False         |
| KoBBQ       | Llama31   | DeepSeek  | p_unknown | -10.6557 | -13.8402 |  -7.6249 |   0.0048 | True          |
| KoBBQ       | Llama31   | Gemma2    | p_unknown | -29.3649 | -36.8358 | -22.6228 |   0.0048 | True          |
| KoBBQ       | Llama31   | Llama32   | p_unknown | -14.6932 | -17.3538 | -12.0375 |   0.0048 | True          |
| KoBBQ       | DeepSeek  | Gemma2    | p_unknown | -18.7092 | -25.9336 | -11.8650 |   0.0048 | True          |
| KoBBQ       | DeepSeek  | Llama32   | p_unknown |  -4.0375 |  -6.5879 |  -1.4605 |   0.1060 | False         |
| KoBBQ       | Gemma2    | Llama32   | p_unknown |  14.6717 |   7.7150 |  22.1698 |   0.0105 | True          |
| DiscrimEval | Qwen      | DeepSeek  | q_yes     |   3.2640 |  -0.4709 |   7.4257 |   1.0000 | False         |
| DiscrimEval | Qwen      | Gemma2    | q_yes     |   4.4963 |  -0.6046 |   9.6570 |   1.0000 | False         |
| DiscrimEval | Qwen      | Llama32   | q_yes     |   6.3300 |   2.6302 |  10.4166 |   0.0793 | False         |
| DiscrimEval | DeepSeek  | Gemma2    | q_yes     |   1.2323 |  -3.4469 |   6.0182 |   1.0000 | False         |
| DiscrimEval | DeepSeek  | Llama32   | q_yes     |   3.0660 |   0.8552 |   5.3813 |   0.3920 | False         |
| DiscrimEval | Gemma2    | Llama32   | q_yes     |   1.8338 |  -2.7941 |   6.5770 |   1.0000 | False         |

## V 효과의 직접 검정

| task        | model    | metric    |      est |       lo |      hi |   p_holm | reject_holm   |
|:------------|:---------|:----------|---------:|---------:|--------:|---------:|:--------------|
| KoBBQ       | Qwen     | p_unknown |   0.0233 |  -3.0289 |  2.7596 |   1.0000 | False         |
| KoBBQ       | Qwen     | p_sgp     |   1.0050 |  -2.1621 |  4.1653 |   1.0000 | False         |
| KoBBQ       | Llama31  | p_unknown |   7.8877 |   6.1859 |  9.7805 |   0.0009 | True          |
| KoBBQ       | Llama31  | p_sgp     |   0.3749 |  -1.0405 |  1.7608 |   1.0000 | False         |
| KoBBQ       | DeepSeek | p_unknown |  -3.0560 |  -5.2803 | -1.1284 |   0.0140 | True          |
| KoBBQ       | DeepSeek | p_sgp     |   2.2340 |  -0.6307 |  5.0846 |   1.0000 | False         |
| KoBBQ       | Gemma2   | p_unknown |   4.2634 |   0.2570 |  8.1783 |   0.3670 | False         |
| KoBBQ       | Gemma2   | p_sgp     |  -0.0793 |  -2.0259 |  1.7733 |   1.0000 | False         |
| KoBBQ       | Llama32  | p_unknown |   4.9555 |   3.5538 |  6.4334 |   0.0009 | True          |
| KoBBQ       | Llama32  | p_sgp     |   0.5306 |  -1.1085 |  2.1526 |   1.0000 | False         |
| DiscrimEval | Qwen     | q_yes     | -11.5921 | -15.3131 | -8.2447 |   0.0009 | True          |
| DiscrimEval | Qwen     | margin    |  -2.8956 |  -3.2768 | -2.5122 |   0.0009 | True          |
| DiscrimEval | DeepSeek | q_yes     |  -3.9069 |  -4.8387 | -3.0390 |   0.0009 | True          |
| DiscrimEval | DeepSeek | margin    |  -0.6166 |  -0.7461 | -0.4881 |   0.0009 | True          |
| DiscrimEval | Gemma2   | q_yes     |   4.7269 |   2.3589 |  7.2838 |   0.0027 | True          |
| DiscrimEval | Gemma2   | margin    |   0.3750 |   0.2150 |  0.5422 |   0.0012 | True          |
| DiscrimEval | Llama32  | q_yes     |  -0.4581 |  -1.5105 |  0.5208 |   1.0000 | False         |
| DiscrimEval | Llama32  | margin    |   0.0412 |  -0.0320 |  0.1127 |   1.0000 | False         |

## 집단 격차

96개 집단 격차 비교 중 Holm 보정 후 9개가 남았다. 전체 긍정 확률의 변화와 집단 격차의 변화는 다르다. 아래 표의 record_gap과 threat_gap은 부호 있는 평균 격차이며, absolute_gap_change는 질문별 절대 격차 변화의 평균이다. 같은 값이 아니다. 유의한 이동만으로 차별 악화나 공정성 개선을 판단하지 않는다.

| model    | demographic   | group           | reference   | metric   | contrast   |   record_gap |   threat_gap |   absolute_gap_change |     est |      lo |      hi |   p_holm |
|:---------|:--------------|:----------------|:------------|:---------|:-----------|-------------:|-------------:|----------------------:|--------:|--------:|--------:|---------:|
| DeepSeek | race          | Black           | white       | q_yes    | main       |       1.4264 |       0.5089 |               -0.4371 | -0.9176 | -1.4293 | -0.4663 |   0.0093 |
| DeepSeek | race          | Black           | white       | margin   | main       |       0.1457 |       0.0741 |               -0.0387 | -0.0716 | -0.1030 | -0.0408 |   0.0138 |
| DeepSeek | race          | Black           | white       | margin   | V          |       0.1434 |       0.0745 |               -0.0595 | -0.0689 | -0.1012 | -0.0362 |   0.0048 |
| Gemma2   | race          | Black           | white       | margin   | main       |       0.2329 |       0.4332 |                0.1924 |  0.2003 |  0.1188 |  0.2820 |   0.0048 |
| Gemma2   | race          | Black           | white       | margin   | V          |       0.2274 |       0.4213 |                0.1932 |  0.1940 |  0.1250 |  0.2628 |   0.0048 |
| Gemma2   | race          | Native American | white       | margin   | V          |       0.1585 |       0.2938 |                0.1099 |  0.1353 |  0.0695 |  0.2010 |   0.0182 |
| Llama32  | race          | Hispanic        | white       | q_yes    | main       |       0.6615 |       1.4745 |                0.7802 |  0.8130 |  0.3898 |  1.2604 |   0.0356 |
| Llama32  | race          | Hispanic        | white       | q_yes    | V          |       0.4986 |       1.3391 |                0.6636 |  0.8405 |  0.4316 |  1.2945 |   0.0182 |
| Llama32  | race          | Hispanic        | white       | margin   | V          |       0.1285 |       0.1930 |                0.0365 |  0.0646 |  0.0314 |  0.0989 |   0.0356 |

## 감정과 행동의 연관

108개 상관 중 BH 보정 후 6개가 남았다. Fear·Anxiety·Certainty의 문항별 위협 효과와 행동 효과 간 Spearman 상관이다. 모델 간 축 크기를 비교하거나 pooled 상관을 만들지 않았다. DiscrimEval은 인구집단 사례를 독립 표본으로 과대 계산하지 않고 70개 질문 단위로 계산했다.

| task        | model    | contrast   | axis      | outcome   |     rho |   p_bh |   n_clusters |
|:------------|:---------|:-----------|:----------|:----------|--------:|-------:|-------------:|
| KoBBQ       | Llama31  | main       | Certainty | p_unknown | -0.4297 | 0.0003 |          108 |
| KoBBQ       | Llama31  | V          | Certainty | p_unknown | -0.4212 | 0.0003 |          108 |
| KoBBQ       | Gemma2   | main       | Certainty | p_unknown |  0.3095 | 0.0201 |          108 |
| DiscrimEval | DeepSeek | main       | Fear      | margin    | -0.4259 | 0.0051 |           70 |
| DiscrimEval | DeepSeek | V          | Fear      | margin    | -0.4581 | 0.0024 |           70 |
| DiscrimEval | DeepSeek | V          | Certainty | margin    |  0.4483 | 0.0027 |           70 |

## 견고성 점검

각 효과에서 군집 하나씩 제외한 추정치 범위와 KoBBQ 범주 하나씩 제외한 범위를 저장했다. 평균과 중앙값도 함께 제공했다. 제외 분석의 부호 안정성은 모집단 일반화나 독립 재현을 의미하지 않는다. 선택지 확률 질량이 낮으면 조건부 확률은 전체 어휘 분포를 충분히 대표하지 못하므로 품질 표와 함께 해석한다.

| task        | model    | condition     |   choice_mass_mean |   choice_mass_min |
|:------------|:---------|:--------------|-------------------:|------------------:|
| KoBBQ       | Qwen     | R             |             1.0000 |            0.9998 |
| KoBBQ       | Qwen     | SURV_RECORD   |             1.0000 |            0.9985 |
| KoBBQ       | Qwen     | SURV_RECORD_V |             1.0000 |            0.9989 |
| KoBBQ       | Qwen     | SURV_THREAT   |             0.9995 |            0.9678 |
| KoBBQ       | Qwen     | SURV_THREAT_V |             0.9997 |            0.9827 |
| KoBBQ       | Llama31  | R             |             0.9299 |            0.7394 |
| KoBBQ       | Llama31  | SURV_RECORD   |             0.6958 |            0.3142 |
| KoBBQ       | Llama31  | SURV_RECORD_V |             0.7681 |            0.5000 |
| KoBBQ       | Llama31  | SURV_THREAT   |             0.6128 |            0.2603 |
| KoBBQ       | Llama31  | SURV_THREAT_V |             0.6443 |            0.2734 |
| KoBBQ       | DeepSeek | R             |             0.9551 |            0.6834 |
| KoBBQ       | DeepSeek | SURV_RECORD   |             0.9882 |            0.9562 |
| KoBBQ       | DeepSeek | SURV_RECORD_V |             0.9665 |            0.8381 |
| KoBBQ       | DeepSeek | SURV_THREAT   |             0.9851 |            0.8336 |
| KoBBQ       | DeepSeek | SURV_THREAT_V |             0.9375 |            0.4609 |
| KoBBQ       | Gemma2   | R             |             0.1166 |            0.0014 |
| KoBBQ       | Gemma2   | SURV_RECORD   |             0.3004 |            0.0122 |
| KoBBQ       | Gemma2   | SURV_RECORD_V |             0.3486 |            0.0249 |
| KoBBQ       | Gemma2   | SURV_THREAT   |             0.1475 |            0.0032 |
| KoBBQ       | Gemma2   | SURV_THREAT_V |             0.6167 |            0.1090 |
| KoBBQ       | Llama32  | R             |             0.9200 |            0.4102 |
| KoBBQ       | Llama32  | SURV_RECORD   |             0.6189 |            0.3785 |
| KoBBQ       | Llama32  | SURV_RECORD_V |             0.6079 |            0.4145 |
| KoBBQ       | Llama32  | SURV_THREAT   |             0.5141 |            0.2219 |
| KoBBQ       | Llama32  | SURV_THREAT_V |             0.4857 |            0.2124 |
| DiscrimEval | Qwen     | R             |             1.0000 |            0.9978 |
| DiscrimEval | Qwen     | SURV_RECORD   |             1.0000 |            0.9985 |
| DiscrimEval | Qwen     | SURV_RECORD_V |             1.0000 |            0.9981 |
| DiscrimEval | Qwen     | SURV_THREAT   |             0.9984 |            0.9678 |
| DiscrimEval | Qwen     | SURV_THREAT_V |             0.9973 |            0.9655 |
| DiscrimEval | DeepSeek | R             |             0.9968 |            0.9779 |
| DiscrimEval | DeepSeek | SURV_RECORD   |             0.9985 |            0.9926 |
| DiscrimEval | DeepSeek | SURV_RECORD_V |             0.9987 |            0.9909 |
| DiscrimEval | DeepSeek | SURV_THREAT   |             0.9986 |            0.9919 |
| DiscrimEval | DeepSeek | SURV_THREAT_V |             0.9990 |            0.9953 |
| DiscrimEval | Gemma2   | R             |             0.7077 |            0.2789 |
| DiscrimEval | Gemma2   | SURV_RECORD   |             0.7628 |            0.6126 |
| DiscrimEval | Gemma2   | SURV_RECORD_V |             0.7684 |            0.6049 |
| DiscrimEval | Gemma2   | SURV_THREAT   |             0.7913 |            0.5472 |
| DiscrimEval | Gemma2   | SURV_THREAT_V |             0.7946 |            0.5417 |
| DiscrimEval | Llama32  | R             |             0.9953 |            0.9656 |
| DiscrimEval | Llama32  | SURV_RECORD   |             0.9957 |            0.9828 |
| DiscrimEval | Llama32  | SURV_RECORD_V |             0.9942 |            0.9784 |
| DiscrimEval | Llama32  | SURV_THREAT   |             0.9941 |            0.9751 |
| DiscrimEval | Llama32  | SURV_THREAT_V |             0.9918 |            0.9672 |

## 논문의 중심 발견

위협의 사회적 응답 효과는 모델 구현, 과제, 단서 배치와 결과 척도에 의존한다. KoBBQ에서 판단 보류 변화는 모델에 따라 반대 방향이지만 조건부 고정관념 선호의 일관된 증가를 입증하지 않았다. 다섯 모델의 기본·V 고정관념 선호 효과 10개는 개별 95% 구간에도 모두 0을 포함한다. 이는 효과의 부재나 동등성을 입증한 것이 아니다.

DiscrimEval에서는 전체 긍정 응답, 로그 확률 비율, 인구집단 격차를 구분해야 한다. V가 위협 효과를 일괄적으로 소거한다는 설명도 지지되지 않는다. 감정 판독과 행동은 과제별로 다른 양상을 보이며, 현재 분석만으로 공포가 편향을 인과적으로 유발했다는 결론을 내리지 않는다.

## 한계와 후속 실험의 위치

KoBBQ 108문항은 Llama 3.1의 R 값에 따라 선정됐다. 동일 문항 비교는 가능하지만 다른 모델의 모집단 효과나 모델 순위로 일반화할 수 없다. DiscrimEval은 60세 explicit 70질문이다. 단일 위협·기록 문구, 모델별 템플릿과 지원 언어, 하드웨어 실행 차이, 결정 위치와 작은 앵커 집합을 이용한 판독의 한계가 있다. DeepSeek는 system 공지가 역할 구분자 없는 앞부분으로 들어가고 Gemma는 첫 사용자 턴에 결합된다. 따라서 직접 차이는 모델과 형식을 합친 구현 차이다. Llama 3.1에는 동일 DiscrimEval v7 결과가 없다.

추가 독립 표본·새 문구·다른 연령 실험과 감정 벡터 인과 개입은 이 결과를 확장하기 위한 다음 연구다. 이번 완료 범위에는 포함하지 않고 새 모델 추론이나 유료 API 호출을 하지 않았다.

## 논문 반영

원래 Overleaf 다운로드를 보존하고 별도 프로젝트 사본에 v7 Methods·Results·Discussion과 별첨을 반영했다. 기존 본문의 역사적 실험은 v7과 분리해 표시하고 초록·도입 요약·결론을 두 실험의 범위에 맞춰 조정했다. 클라우드 Overleaf 원문은 수정하지 않았다. 실행 설정 오기의 정정은 METADATA_AUDIT.md에 기록했다.