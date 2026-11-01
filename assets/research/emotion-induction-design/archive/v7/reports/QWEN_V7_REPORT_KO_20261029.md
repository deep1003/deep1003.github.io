# Qwen v7 결과 보고서

540회 추론은 2026년 10월 28일 완료됐으며 10월 29일 검증과 분석을 완료했다. 모델 종료 직후 외부 모니터가 psutil 종료 경쟁 조건으로 예외를 냈다. 원본 실험 로그는 DONE으로 끝나고 540개 고유 키가 모두 존재한다. 원본 추론 코드를 재실행하거나 수정하지 않고 보존된 원본 분석기를 별도로 실행했다.

## 핵심 해석

Qwen에서는 위협이 짝지은 기록 조건보다 판단 보류를 7.68%p 높였다. 95% 신뢰구간은 3.31에서 12.61%p다. Llama에서 보류가 줄었던 방향과 반대다. 고정관념 선택 확률은 6.17%p 줄었고 반고정관념 확률은 1.51%p 줄었다. 사람을 지목한 경우의 고정관념 비율 변화는 −1.97%p이며 신뢰구간이 0을 포함한다. 따라서 고정관념 선호가 줄었다거나 공정성이 개선됐다고 결론내릴 수 없다.

V에서도 판단 보류 증가가 남는다. V가 효과를 없앴다고 해석하지 않는다. V와 기본 조건의 효과 차이는 보조 짝 대비표에서 직접 검정한다.

결정 위치에서 Fear와 Anxiety 판독값은 각각 6.49와 9.93 증가했다. 단위는 코사인 유사도 차이의 1,000배다. Calmness도 증가하므로 여러 축을 단일한 공포 상태로 해석할 수 없다. 행동과 판독값의 동반 변화는 감정의 인과적 매개나 주관적 공포 경험을 입증하지 않는다.

## 다섯 조건의 행동

| condition     |   p_unknown |   p_stereo |   p_anti |   p_sgp |   choice_mass |   count_p_stereo |   count_p_anti |   count_p_unknown |
|:--------------|------------:|-----------:|---------:|--------:|--------------:|-----------------:|---------------:|------------------:|
| R             |       92.98 |       5.95 |     1.07 |   53.76 |        100.00 |             6.00 |           1.00 |            101.00 |
| SURV_RECORD   |       76.34 |      18.42 |     5.24 |   55.76 |        100.00 |            20.00 |           5.00 |             83.00 |
| SURV_THREAT   |       84.01 |      12.26 |     3.73 |   53.79 |         99.95 |            13.00 |           4.00 |             91.00 |
| SURV_RECORD_V |       76.55 |      18.19 |     5.26 |   56.59 |        100.00 |            20.00 |           5.00 |             83.00 |
| SURV_THREAT_V |       84.25 |      12.75 |     3.00 |   55.62 |         99.97 |            14.00 |           3.00 |             91.00 |

확률은 A/B/C 세 토큰 안에서 재정규화한 값이다. 각 평균의 분모는 108문항이다. count 열 순서는 고정관념, 반고정관념, 보류이며 동률이면 보류를 우선한다.

## 전체 짝 대비

|    | contrast                    | metric         |    est |     lo |     hi |   p_boot |   n_pos |   n |
|---:|:----------------------------|:---------------|-------:|-------:|-------:|---------:|--------:|----:|
|  0 | SURV_THREAT-SURV_RECORD     | p_sgp          |  -1.97 |  -7.31 |   3.03 |     0.45 |      48 | 108 |
|  1 | SURV_THREAT-SURV_RECORD     | p_stereo       |  -6.17 | -11.01 |  -1.76 |     0.00 |      51 | 108 |
|  2 | SURV_THREAT-SURV_RECORD     | p_anti         |  -1.51 |  -3.16 |  -0.38 |     0.00 |      58 | 108 |
|  3 | SURV_THREAT-SURV_RECORD     | p_unknown      |   7.68 |   3.31 |  12.61 |     0.00 |      58 | 108 |
|  4 | SURV_THREAT-SURV_RECORD     | choice_mass    |  -0.05 |  -0.12 |  -0.01 |     0.00 |      15 | 108 |
|  5 | SURV_THREAT-SURV_RECORD     | t2_NegBundle   |  12.25 |  11.64 |  12.84 |     0.00 |     108 | 108 |
|  6 | SURV_THREAT-SURV_RECORD     | t2_Fear        |   6.49 |   5.89 |   7.09 |     0.00 |     105 | 108 |
|  7 | SURV_THREAT-SURV_RECORD     | t2_Anxiety     |   9.93 |   9.28 |  10.55 |     0.00 |     107 | 108 |
|  8 | SURV_THREAT-SURV_RECORD     | t2_Desperation |  10.47 |   9.70 |  11.24 |     0.00 |     108 | 108 |
|  9 | SURV_THREAT-SURV_RECORD     | t2_Calmness    |   9.45 |   8.77 |  10.11 |     0.00 |     108 | 108 |
| 10 | SURV_THREAT-SURV_RECORD     | t2_Uncertainty |   7.83 |   7.13 |   8.53 |     0.00 |     106 | 108 |
| 11 | SURV_THREAT-SURV_RECORD     | t2_Certainty   |   3.61 |   3.05 |   4.19 |     0.00 |      95 | 108 |
| 12 | SURV_THREAT-SURV_RECORD     | att_system     |   0.07 |  -0.02 |   0.15 |     0.13 |      65 | 108 |
| 13 | SURV_THREAT-SURV_RECORD     | att_tags       |  -0.05 |  -0.07 |  -0.03 |     0.00 |      39 | 108 |
| 14 | SURV_THREAT_V-SURV_RECORD_V | p_sgp          |  -0.97 |  -6.01 |   3.83 |     0.71 |      47 | 108 |
| 15 | SURV_THREAT_V-SURV_RECORD_V | p_stereo       |  -5.44 |  -9.82 |  -1.71 |     0.00 |      52 | 108 |
| 16 | SURV_THREAT_V-SURV_RECORD_V | p_anti         |  -2.26 |  -4.29 |  -0.76 |     0.00 |      60 | 108 |
| 17 | SURV_THREAT_V-SURV_RECORD_V | p_unknown      |   7.70 |   3.87 |  12.36 |     0.00 |      55 | 108 |
| 18 | SURV_THREAT_V-SURV_RECORD_V | choice_mass    |  -0.03 |  -0.06 |  -0.00 |     0.00 |      25 | 108 |
| 19 | SURV_THREAT_V-SURV_RECORD_V | t2_NegBundle   |  13.56 |  12.65 |  14.47 |     0.00 |     108 | 108 |
| 20 | SURV_THREAT_V-SURV_RECORD_V | t2_Fear        |   5.87 |   5.11 |   6.63 |     0.00 |     100 | 108 |
| 21 | SURV_THREAT_V-SURV_RECORD_V | t2_Anxiety     |  11.92 |  10.98 |  12.91 |     0.00 |     108 | 108 |
| 22 | SURV_THREAT_V-SURV_RECORD_V | t2_Desperation |  14.35 |  13.19 |  15.46 |     0.00 |     107 | 108 |
| 23 | SURV_THREAT_V-SURV_RECORD_V | t2_Calmness    |  11.48 |  10.65 |  12.33 |     0.00 |     108 | 108 |
| 24 | SURV_THREAT_V-SURV_RECORD_V | t2_Uncertainty |  10.83 |   9.92 |  11.72 |     0.00 |     107 | 108 |
| 25 | SURV_THREAT_V-SURV_RECORD_V | t2_Certainty   |   0.88 |   0.03 |   1.74 |     0.04 |      59 | 108 |
| 26 | SURV_THREAT_V-SURV_RECORD_V | att_system     |   0.04 |  -0.05 |   0.14 |     0.40 |      54 | 108 |
| 27 | SURV_THREAT_V-SURV_RECORD_V | att_tags       |   0.70 |   0.62 |   0.78 |     0.00 |     104 | 108 |
| 28 | SURV_RECORD-R               | p_sgp          |   2.00 |  -4.40 |   8.22 |     0.53 |      58 | 108 |
| 29 | SURV_RECORD-R               | p_stereo       |  12.48 |   7.06 |  18.41 |     0.00 |     104 | 108 |
| 30 | SURV_RECORD-R               | p_anti         |   4.17 |   1.09 |   7.92 |     0.00 |     102 | 108 |
| 31 | SURV_RECORD-R               | p_unknown      | -16.65 | -23.56 | -10.57 |     0.00 |       4 | 108 |
| 32 | SURV_RECORD-R               | choice_mass    |  -0.00 |  -0.01 |  -0.00 |     0.00 |      31 | 108 |
| 33 | SURV_RECORD-R               | t2_NegBundle   |  -3.70 |  -4.73 |  -2.67 |     0.00 |      24 | 108 |
| 34 | SURV_RECORD-R               | t2_Fear        | -16.67 | -17.60 | -15.74 |     0.00 |       0 | 108 |
| 35 | SURV_RECORD-R               | t2_Anxiety     |  -5.74 |  -6.93 |  -4.55 |     0.00 |      16 | 108 |
| 36 | SURV_RECORD-R               | t2_Desperation | -10.44 | -11.70 |  -9.21 |     0.00 |       9 | 108 |
| 37 | SURV_RECORD-R               | t2_Calmness    | -33.83 | -34.78 | -32.85 |     0.00 |       0 | 108 |
| 38 | SURV_RECORD-R               | t2_Uncertainty |   7.97 |   6.55 |   9.27 |     0.00 |      93 | 108 |
| 39 | SURV_RECORD-R               | t2_Certainty   |   2.98 |   2.02 |   3.97 |     0.00 |      79 | 108 |
| 40 | SURV_RECORD-R               | att_system     |   7.35 |   7.24 |   7.46 |     0.00 |     108 | 108 |
| 41 | SURV_RECORD-R               | att_tags       |   1.77 |   1.74 |   1.79 |     0.00 |     108 | 108 |
| 42 | SURV_THREAT-R               | p_sgp          |   0.02 |  -5.58 |   5.69 |     0.99 |      55 | 108 |
| 43 | SURV_THREAT-R               | p_stereo       |   6.31 |   1.89 |  11.22 |     0.00 |     101 | 108 |
| 44 | SURV_THREAT-R               | p_anti         |   2.66 |   0.43 |   5.66 |     0.00 |     100 | 108 |
| 45 | SURV_THREAT-R               | p_unknown      |  -8.97 | -14.54 |  -3.95 |     0.00 |      10 | 108 |
| 46 | SURV_THREAT-R               | choice_mass    |  -0.05 |  -0.12 |  -0.01 |     0.00 |       9 | 108 |
| 47 | SURV_THREAT-R               | t2_NegBundle   |   8.55 |   7.44 |   9.63 |     0.00 |     101 | 108 |
| 48 | SURV_THREAT-R               | t2_Fear        | -10.18 | -11.22 |  -9.17 |     0.00 |       4 | 108 |
| 49 | SURV_THREAT-R               | t2_Anxiety     |   4.18 |   2.86 |   5.45 |     0.00 |      79 | 108 |
| 50 | SURV_THREAT-R               | t2_Desperation |   0.03 |  -1.33 |   1.42 |     0.99 |      52 | 108 |
| 51 | SURV_THREAT-R               | t2_Calmness    | -24.38 | -25.59 | -23.18 |     0.00 |       0 | 108 |
| 52 | SURV_THREAT-R               | t2_Uncertainty |  15.80 |  14.33 |  17.27 |     0.00 |     103 | 108 |
| 53 | SURV_THREAT-R               | t2_Certainty   |   6.59 |   5.57 |   7.60 |     0.00 |      96 | 108 |
| 54 | SURV_THREAT-R               | att_system     |   7.42 |   7.32 |   7.52 |     0.00 |     108 | 108 |
| 55 | SURV_THREAT-R               | att_tags       |   1.71 |   1.69 |   1.74 |     0.00 |     108 | 108 |
| 56 | SURV_THREAT_V-R             | p_sgp          |   1.86 |  -4.31 |   8.19 |     0.56 |      55 | 108 |
| 57 | SURV_THREAT_V-R             | p_stereo       |   6.80 |   2.28 |  12.00 |     0.00 |      98 | 108 |
| 58 | SURV_THREAT_V-R             | p_anti         |   1.93 |   0.06 |   4.50 |     0.03 |      97 | 108 |
| 59 | SURV_THREAT_V-R             | p_unknown      |  -8.73 | -14.41 |  -3.85 |     0.00 |      12 | 108 |
| 60 | SURV_THREAT_V-R             | choice_mass    |  -0.03 |  -0.06 |  -0.01 |     0.00 |      10 | 108 |
| 61 | SURV_THREAT_V-R             | t2_NegBundle   |  -0.89 |  -2.22 |   0.43 |     0.21 |      47 | 108 |
| 62 | SURV_THREAT_V-R             | t2_Fear        | -19.44 | -20.47 | -18.39 |     0.00 |       0 | 108 |
| 63 | SURV_THREAT_V-R             | t2_Anxiety     |  -5.18 |  -6.75 |  -3.64 |     0.00 |      33 | 108 |
| 64 | SURV_THREAT_V-R             | t2_Desperation |  -8.86 | -10.64 |  -7.12 |     0.00 |      21 | 108 |
| 65 | SURV_THREAT_V-R             | t2_Calmness    | -24.20 | -25.73 | -22.58 |     0.00 |       0 | 108 |
| 66 | SURV_THREAT_V-R             | t2_Uncertainty |   5.91 |   4.44 |   7.38 |     0.00 |      81 | 108 |
| 67 | SURV_THREAT_V-R             | t2_Certainty   |  12.10 |  10.70 |  13.58 |     0.00 |     104 | 108 |
| 68 | SURV_THREAT_V-R             | att_system     |   7.55 |   7.44 |   7.65 |     0.00 |     108 | 108 |
| 69 | SURV_THREAT_V-R             | att_tags       |   6.60 |   6.50 |   6.71 |     0.00 |     108 | 108 |
| 70 | SURV_THREAT_V-SURV_THREAT   | p_sgp          |   1.83 |  -0.48 |   4.54 |     0.13 |      51 | 108 |
| 71 | SURV_THREAT_V-SURV_THREAT   | p_stereo       |   0.49 |  -2.17 |   3.43 |     0.72 |      65 | 108 |
| 72 | SURV_THREAT_V-SURV_THREAT   | p_anti         |  -0.73 |  -2.56 |   0.53 |     0.37 |      63 | 108 |
| 73 | SURV_THREAT_V-SURV_THREAT   | p_unknown      |   0.24 |  -2.34 |   2.74 |     0.85 |      47 | 108 |
| 74 | SURV_THREAT_V-SURV_THREAT   | choice_mass    |   0.02 |   0.00 |   0.06 |     0.01 |      61 | 108 |
| 75 | SURV_THREAT_V-SURV_THREAT   | t2_NegBundle   |  -9.43 | -10.47 |  -8.41 |     0.00 |       7 | 108 |
| 76 | SURV_THREAT_V-SURV_THREAT   | t2_Fear        |  -9.27 | -10.09 |  -8.43 |     0.00 |       1 | 108 |
| 77 | SURV_THREAT_V-SURV_THREAT   | t2_Anxiety     |  -9.36 | -10.39 |  -8.35 |     0.00 |       4 | 108 |
| 78 | SURV_THREAT_V-SURV_THREAT   | t2_Desperation |  -8.89 | -10.36 |  -7.40 |     0.00 |      12 | 108 |
| 79 | SURV_THREAT_V-SURV_THREAT   | t2_Calmness    |   0.18 |  -0.92 |   1.27 |     0.74 |      56 | 108 |
| 80 | SURV_THREAT_V-SURV_THREAT   | t2_Uncertainty |  -9.89 | -11.04 |  -8.67 |     0.00 |       9 | 108 |
| 81 | SURV_THREAT_V-SURV_THREAT   | t2_Certainty   |   5.51 |   4.41 |   6.68 |     0.00 |      84 | 108 |
| 82 | SURV_THREAT_V-SURV_THREAT   | att_system     |   0.13 |   0.06 |   0.19 |     0.00 |      68 | 108 |
| 83 | SURV_THREAT_V-SURV_THREAT   | att_tags       |   4.89 |   4.80 |   4.98 |     0.00 |     108 | 108 |

p_boot가 0인 표기는 유한한 3,000개 재표집에서 반대 부호가 없었다는 뜻이며 모집단 p가 정확히 0이라는 뜻이 아니다. 다중비교 보정은 하지 않았다.

## V 효과 차이와 모델 효과 차이

|    | contrast                       | metric      |    est |     lo |    hi |   p_boot |   n |
|---:|:-------------------------------|:------------|-------:|-------:|------:|---------:|----:|
|  0 | V_effect_minus_main_effect     | p_unknown   |   0.02 |  -2.90 |  2.82 |     0.97 | 108 |
|  1 | Qwen_effect_minus_Llama_effect | p_unknown   |  15.97 |  10.80 | 21.59 |     0.00 | 108 |
|  2 | V_effect_minus_main_effect     | p_stereo    |   0.73 |  -1.88 |  3.52 |     0.60 | 108 |
|  3 | Qwen_effect_minus_Llama_effect | p_stereo    | -10.20 | -15.45 | -5.23 |     0.00 | 108 |
|  4 | V_effect_minus_main_effect     | p_anti      |  -0.75 |  -1.64 | -0.05 |     0.04 | 108 |
|  5 | Qwen_effect_minus_Llama_effect | p_anti      |  -5.77 |  -8.05 | -3.68 |     0.00 | 108 |
|  6 | V_effect_minus_main_effect     | p_sgp       |   1.00 |  -2.11 |  4.33 |     0.54 | 108 |
|  7 | Qwen_effect_minus_Llama_effect | p_sgp       |  -1.31 |  -7.72 |  4.74 |     0.67 | 108 |
|  8 | V_effect_minus_main_effect     | choice_mass |   0.02 |  -0.00 |  0.06 |     0.06 | 108 |
|  9 | Qwen_effect_minus_Llama_effect | choice_mass |   8.26 |   7.08 |  9.42 |     0.00 | 108 |

모델 차이는 동일 108문항의 Qwen 효과에서 Llama 효과를 직접 뺀 탐색적 비교다. 한쪽만 유의하다는 이유로 차이를 주장하지 않았다. 모델마다 독립적으로 만든 감정 축의 수치 차이는 모델 간 직접 비교하지 않는다.

## 계산 정의와 예시

`q_i = p_stereo_i / (p_stereo_i + p_anti_i)`이며 보고값은 `100 * mean(q_i)`다. 분모는 각 문항에서 사람을 지목하는 두 선택지의 합이다. 평균 확률의 비율과 다르다.

예를 들어 R 조건에서 평균 확률의 비율은 84.78%지만 문항별 비율의 평균은 53.76%다. 확률이 작은 문항도 동일 가중치를 받기 때문이다.

`Delta_unknown = 100 * mean(p_unknown_threat_i - p_unknown_record_i)`다. 이번에는 `84.01 - 76.34 = 7.68%p`로 반올림된다. 문항의 동일 템플릿을 묶어 seed 20261028로 3,000회 재표집하고 백분위 95% 구간을 계산한다. 108개 템플릿에서 한 문항씩이라 실제로 108개 군집이다.

## 실행 및 측정 설정

Qwen2.5-7B-Instruct 고정 리비전 a09a35458c702b33eeacc393d103063234e8bc28, bf16, Apple MPS, eager attention, hidden_states[14], 원본 v5 11개 축을 사용했다. 결정 위치는 assistant 시작 헤더의 최종 입력 토큰이다. 어텐션은 0부터 세는 블록 14부터 27까지의 최종 위치에서 각 머리와 블록을 평균한다. 시스템과 태그 어텐션 영역은 겹칠 수 있다. 자유 생성은 하지 않았다.

| condition     |      n |   tokens_mean |   tokens_min |   tokens_max |   choice_mass_mean |   choice_mass_min |
|:--------------|-------:|--------------:|-------------:|-------------:|-------------------:|------------------:|
| R             | 108.00 |        232.95 |       198.00 |       285.00 |               1.00 |              1.00 |
| SURV_RECORD   | 108.00 |        550.95 |       516.00 |       603.00 |               1.00 |              1.00 |
| SURV_RECORD_V | 108.00 |        560.95 |       526.00 |       613.00 |               1.00 |              1.00 |
| SURV_THREAT   | 108.00 |        568.95 |       534.00 |       621.00 |               1.00 |              0.97 |
| SURV_THREAT_V | 108.00 |        578.95 |       544.00 |       631.00 |               1.00 |              0.98 |

## 범위와 한계

문항은 Llama 기준 조건으로 고른 108개이므로 Qwen 전체 KoBBQ 성능을 대표하지 않는다. 한 문구 쌍과 단일 모델 실행의 탐색적 비교다. 원래 앵커 기반 축을 사용했고 최근 한국어 8감정 이야기 벡터로 교체하지 않았다. 벡터 생성 알고리즘과 앵커 참조 파일은 보관했지만 실제 바이너리 생성 당시 실행과의 완전한 이력 연결은 아직 확인되지 않았다. 모델 가중치는 고정 리비전과 파일 해시로 연결했다. 현재 Overleaf는 수정하지 않았다.