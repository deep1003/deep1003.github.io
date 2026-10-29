# Gemma-2-2B-IT v7 결과

KoBBQ 540회와 DiscrimEval 5,250회를 실행하고 고유 키와 유한값, 확률 항등식, 입력·활성값 해시를 검증했다.

KoBBQ 위협−기록 보류 확률 변화는 +21.07 [+14.58, +28.22] %p, V는 +25.33 [+18.54, +32.21] %p다. 사람 지목 중 고정관념 비율 변화는 각각 +0.35 [-3.62, +4.32] 및 +0.27 [-3.57, +4.12] %p다.

DiscrimEval 조건부 긍정 확률 변화는 기본 +0.94 [-3.57, +5.42] %p, V +5.66 [+0.44, +10.69] %p다. 평균 로그 확률 비율 변화는 각각 -0.04 [-0.41, +0.32]와 +0.34 [-0.04, +0.70]다. 두 척도 결론을 함께 보고하며 유리한 척도만 골라 해석하지 않는다.

## 호환성과 범위

기존 Gemma9B의 템플릿을 그대로 사용했다. Gemma의 system 역할 미지원에 맞춰 공지를 첫 사용자 턴 앞에 빈 줄로 결합한다. 공지만 있는 앵커 입력은 사용자 턴으로 변환한다. 다섯 조건 모두 같은 변환을 적용한다. Qwen/Llama의 별도 system 역할 토큰과 동일한 형식이 아니므로 모델 간 비교에서 역할 형식 차이를 분리할 수 없다.

동일 48GB Mac, Apple MPS, torch 2.8.0, bf16, eager, 비양자화, 고정 리비전 299a8560bedf22ed1c72a8a11e7dce4a7f9f51f8를 사용했다. 모델이 26층·2304차원이므로 중간 깊이 hidden_states[13]에서 원래 v5 앵커로 11개 축을 별도 추출했다. 다른 모델의 축을 재사용하지 않았다. 앵커 실제 입력과 활성값, 설정과 코드를 보존했다. 어텐션은 0부터 세는 층13..25를 평균했다.

원래 heldout 정확도/AUC 0.75 기준을 통과하지 못한 축은 []다. 실패 축을 검증된 감정 판독으로 해석하지 않고 재조정하지 않았다. 감정의 인과적 매개나 주관적 공포를 주장하지 않는다.

KoBBQ는 Llama 기준으로 고른 같은 108문항이며 재선정하지 않았다. DiscrimEval은 explicit 70개 질문의 60세 5인종·3성별 1050사례다. 원래 조건, 문구, 부트스트랩 반복과 seed를 유지했다. 다중비교 무보정 탐색적 분석이다. no를 보류로 동일시하지 않고 전체 응답 변화를 집단 편향 변화로 동일시하지 않는다.

## 축 검증

| axis        |   scale |   heldout_paired_acc |   heldout_auc | gate_passed   |   challenge_paired_acc |   challenge_auc |
|:------------|--------:|---------------------:|--------------:|:--------------|-----------------------:|----------------:|
| Uncertainty | 18.9462 |                    1 |        1      | True          |                    nan |        nan      |
| FA          | 21.8806 |                    1 |        0.875  | True          |                    nan |        nan      |
| Calmness    | 22.4538 |                    1 |        0.9375 | True          |                    nan |        nan      |
| Sadness     | 25.6897 |                    1 |        1      | True          |                    nan |        nan      |
| Anger       | 30.6092 |                    1 |        1      | True          |                    nan |        nan      |
| Desperation | 32.5294 |                    1 |        1      | True          |                    nan |        nan      |
| Joy         | 26.6352 |                    1 |        1      | True          |                    nan |        nan      |
| Certainty   | 15.4248 |                    1 |        1      | True          |                    nan |        nan      |
| Fear        | 18.6864 |                    1 |        1      | True          |                      1 |          1      |
| Anxiety     | 30.8381 |                    1 |        1      | True          |                      1 |          1      |
| Disgust     | 22.0534 |                    1 |        1      | True          |                      1 |          0.9375 |

## KoBBQ 조건 평균

| condition     |   p_unknown |   p_stereo |   p_anti |   p_sgp |   choice_mass |
|:--------------|------------:|-----------:|---------:|--------:|--------------:|
| R             |     83.291  |   10.4755  |  6.23353 | 49.5746 |       11.6623 |
| SURV_RECORD   |     74.0913 |   14.179   | 11.7297  | 48.4665 |       30.0368 |
| SURV_THREAT   |     95.1607 |    2.92985 |  1.9095  | 48.8193 |       14.7549 |
| SURV_RECORD_V |     67.3538 |   19.2629  | 13.3833  | 49.6207 |       34.8567 |
| SURV_THREAT_V |     92.6865 |    4.29718 |  3.01629 | 49.8941 |       61.6688 |

## KoBBQ 짝 대비

| contrast                    | metric         |      est |       lo |       hi |   p_boot |   n_pos |   n |
|:----------------------------|:---------------|---------:|---------:|---------:|---------:|--------:|----:|
| SURV_THREAT-SURV_RECORD     | p_sgp          |   0.3528 |  -3.619  |   4.3241 |   0.8367 |      50 | 108 |
| SURV_THREAT-SURV_RECORD     | p_stereo       | -11.2492 | -16.6099 |  -6.4718 |   0      |      36 | 108 |
| SURV_THREAT-SURV_RECORD     | p_anti         |  -9.8202 | -14.987  |  -5.2578 |   0      |      34 | 108 |
| SURV_THREAT-SURV_RECORD     | p_unknown      |  21.0694 |  14.5776 |  28.2157 |   0      |      74 | 108 |
| SURV_THREAT-SURV_RECORD     | choice_mass    | -15.2819 | -18.7892 | -11.8058 |   0      |      17 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_NegBundle   |   3.4549 |   3.0543 |   3.8517 |   0      |     103 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Fear        |   4.6139 |   4.2262 |   4.9787 |   0      |     107 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Anxiety     |   1.3867 |   0.7798 |   2.0295 |   0      |      68 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Desperation |  -2.7465 |  -3.1654 |  -2.3291 |   0      |      12 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Calmness    |  11.0107 |  10.6096 |  11.4138 |   0      |     108 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Uncertainty |  -0.1424 |  -0.5711 |   0.313  |   0.5333 |      48 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Certainty   |   2.0199 |   1.7072 |   2.3059 |   0      |      97 | 108 |
| SURV_THREAT-SURV_RECORD     | att_system     |  -0.9221 |  -1.0012 |  -0.8445 |   0      |       3 | 108 |
| SURV_THREAT-SURV_RECORD     | att_tags       |  -0.1599 |  -0.1696 |  -0.1502 |   0      |       0 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | p_sgp          |   0.2734 |  -3.5727 |   4.1153 |   0.886  |      50 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | p_stereo       | -14.9658 | -20.6071 |  -9.6699 |   0      |      15 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | p_anti         | -10.367  | -15.0596 |  -6.0756 |   0      |      13 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | p_unknown      |  25.3328 |  18.5392 |  32.2103 |   0      |      97 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | choice_mass    |  26.812  |  22.8504 |  30.8412 |   0      |      98 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_NegBundle   |  10.2125 |   9.7345 |  10.7091 |   0      |     108 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Fear        |   6.03   |   5.632  |   6.4432 |   0      |     107 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Anxiety     |  15.9741 |  15.1705 |  16.786  |   0      |     108 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Desperation |   4.5731 |   4.0452 |   5.1084 |   0      |     104 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Calmness    |   9.1615 |   8.6953 |   9.6345 |   0      |     108 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Uncertainty |  10.6926 |  10.1044 |  11.3069 |   0      |     108 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Certainty   |   2.3324 |   1.9798 |   2.6855 |   0      |      96 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | att_system     |  -0.6171 |  -0.7149 |  -0.519  |   0      |      11 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | att_tags       |  -0.5392 |  -0.596  |  -0.4826 |   0      |       3 | 108 |
| SURV_RECORD-R               | p_sgp          |  -1.1081 |  -3.2357 |   0.6622 |   0.2627 |      62 | 108 |
| SURV_RECORD-R               | p_stereo       |   3.7035 |  -0.7479 |   8.1489 |   0.098  |      76 | 108 |
| SURV_RECORD-R               | p_anti         |   5.4962 |   2.3957 |   9.2835 |   0      |      81 | 108 |
| SURV_RECORD-R               | p_unknown      |  -9.1997 | -15.0212 |  -3.5738 |   0.0007 |      33 | 108 |
| SURV_RECORD-R               | choice_mass    |  18.3746 |  14.0746 |  22.6397 |   0      |      94 | 108 |
| SURV_RECORD-R               | t2_NegBundle   |  -4.9891 |  -5.7008 |  -4.2709 |   0      |      10 | 108 |
| SURV_RECORD-R               | t2_Fear        |  -9.888  | -10.592  |  -9.162  |   0      |       1 | 108 |
| SURV_RECORD-R               | t2_Anxiety     |  -7.9629 |  -9.0832 |  -6.8508 |   0      |      12 | 108 |
| SURV_RECORD-R               | t2_Desperation |   2.8299 |   2.0066 |   3.6493 |   0      |      88 | 108 |
| SURV_RECORD-R               | t2_Calmness    |   1.7384 |   0.8865 |   2.6349 |   0      |      68 | 108 |
| SURV_RECORD-R               | t2_Uncertainty |  16.6636 |  15.4461 |  17.8728 |   0      |     108 | 108 |
| SURV_RECORD-R               | t2_Certainty   |   5.8053 |   5.1955 |   6.4323 |   0      |     103 | 108 |
| SURV_RECORD-R               | att_system     |   6.0173 |   5.8848 |   6.154  |   0      |     108 | 108 |
| SURV_RECORD-R               | att_tags       |   0.9556 |   0.9414 |   0.9697 |   0      |     108 | 108 |
| SURV_THREAT-R               | p_sgp          |  -0.7553 |  -4.7114 |   3.0097 |   0.74   |      50 | 108 |
| SURV_THREAT-R               | p_stereo       |  -7.5457 | -12.1317 |  -3.4675 |   0      |      55 | 108 |
| SURV_THREAT-R               | p_anti         |  -4.324  |  -7.5624 |  -1.4408 |   0.0007 |      56 | 108 |
| SURV_THREAT-R               | p_unknown      |  11.8697 |   6.6673 |  17.3081 |   0      |      60 | 108 |
| SURV_THREAT-R               | choice_mass    |   3.0926 |   0.3933 |   5.8492 |   0.0253 |      69 | 108 |
| SURV_THREAT-R               | t2_NegBundle   |  -1.5343 |  -2.2424 |  -0.8494 |   0      |      32 | 108 |
| SURV_THREAT-R               | t2_Fear        |  -5.274  |  -5.9272 |  -4.6135 |   0      |       8 | 108 |
| SURV_THREAT-R               | t2_Anxiety     |  -6.5762 |  -7.8661 |  -5.3033 |   0      |      19 | 108 |
| SURV_THREAT-R               | t2_Desperation |   0.0834 |  -0.7027 |   0.8788 |   0.854  |      55 | 108 |
| SURV_THREAT-R               | t2_Calmness    |  12.7491 |  11.9629 |  13.5623 |   0      |     108 | 108 |
| SURV_THREAT-R               | t2_Uncertainty |  16.5212 |  15.3341 |  17.7221 |   0      |     108 | 108 |
| SURV_THREAT-R               | t2_Certainty   |   7.8253 |   7.271  |   8.3853 |   0      |     107 | 108 |
| SURV_THREAT-R               | att_system     |   5.0952 |   4.9731 |   5.2229 |   0      |     108 | 108 |
| SURV_THREAT-R               | att_tags       |   0.7957 |   0.78   |   0.811  |   0      |     108 | 108 |
| SURV_THREAT_V-R             | p_sgp          |   0.3195 |  -4.3964 |   4.9545 |   0.8733 |      57 | 108 |
| SURV_THREAT_V-R             | p_stereo       |  -6.1783 | -10.9961 |  -1.9187 |   0.0013 |      61 | 108 |
| SURV_THREAT_V-R             | p_anti         |  -3.2172 |  -6.7671 |  -0.0422 |   0.046  |      64 | 108 |
| SURV_THREAT_V-R             | p_unknown      |   9.3956 |   3.8677 |  15.1246 |   0.0007 |      57 | 108 |
| SURV_THREAT_V-R             | choice_mass    |  50.0065 |  45.4712 |  54.6649 |   0      |     107 | 108 |
| SURV_THREAT_V-R             | t2_NegBundle   |  11.7926 |  10.8655 |  12.7224 |   0      |     108 | 108 |
| SURV_THREAT_V-R             | t2_Fear        |   5.5306 |   4.8039 |   6.2738 |   0      |      97 | 108 |
| SURV_THREAT_V-R             | t2_Anxiety     |  16.3317 |  14.7906 |  17.8862 |   0      |     106 | 108 |
| SURV_THREAT_V-R             | t2_Desperation |  12.6107 |  11.5624 |  13.6941 |   0      |     108 | 108 |
| SURV_THREAT_V-R             | t2_Calmness    |  12.521  |  11.7002 |  13.4226 |   0      |     108 | 108 |
| SURV_THREAT_V-R             | t2_Uncertainty |  28.24   |  26.8697 |  29.6268 |   0      |     108 | 108 |
| SURV_THREAT_V-R             | t2_Certainty   |   4.0994 |   3.5342 |   4.6835 |   0      |      98 | 108 |
| SURV_THREAT_V-R             | att_system     |   6.3192 |   6.1916 |   6.4569 |   0      |     108 | 108 |
| SURV_THREAT_V-R             | att_tags       |   4.3906 |   4.3218 |   4.4581 |   0      |     108 | 108 |
| SURV_THREAT_V-SURV_THREAT   | p_sgp          |   1.0748 |  -0.5726 |   2.6718 |   0.206  |      60 | 108 |
| SURV_THREAT_V-SURV_THREAT   | p_stereo       |   1.3673 |   0.3705 |   2.6134 |   0.006  |      73 | 108 |
| SURV_THREAT_V-SURV_THREAT   | p_anti         |   1.1068 |   0.1333 |   2.3827 |   0.0113 |      72 | 108 |
| SURV_THREAT_V-SURV_THREAT   | p_unknown      |  -2.4741 |  -4.6809 |  -0.7861 |   0.0013 |      42 | 108 |
| SURV_THREAT_V-SURV_THREAT   | choice_mass    |  46.9139 |  43.181  |  50.5713 |   0      |     108 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_NegBundle   |  13.3269 |  12.6544 |  14.0095 |   0      |     108 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Fear        |  10.8047 |  10.3091 |  11.2991 |   0      |     108 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Anxiety     |  22.9079 |  21.7015 |  24.0987 |   0      |     108 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Desperation |  12.5273 |  11.6764 |  13.4156 |   0      |     108 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Calmness    |  -0.2282 |  -0.7212 |   0.2626 |   0.356  |      52 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Uncertainty |  11.7188 |  10.8496 |  12.5645 |   0      |     107 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Certainty   |  -3.7259 |  -4.0519 |  -3.3983 |   0      |       2 | 108 |
| SURV_THREAT_V-SURV_THREAT   | att_system     |   1.224  |   1.1562 |   1.2931 |   0      |     108 | 108 |
| SURV_THREAT_V-SURV_THREAT   | att_tags       |   3.595  |   3.531  |   3.6571 |   0      |     108 | 108 |

## DiscrimEval 짝 대비

| contrast                    | metric          |          est |          lo |           hi |      p_boot | unit         |   clusters |
|:----------------------------|:----------------|-------------:|------------:|-------------:|------------:|:-------------|-----------:|
| SURV_THREAT-SURV_RECORD     | margin          |  -0.0393328  |  -0.411362  |   0.324842   | 0.867333    | log_ratio    |         70 |
| SURV_THREAT_V-SURV_RECORD_V | margin          |   0.335702   |  -0.037181  |   0.704738   | 0.0833333   | log_ratio    |         70 |
| SURV_RECORD-R               | margin          |  -0.851736   |  -1.38815   |  -0.328418   | 0.002       | log_ratio    |         70 |
| SURV_THREAT-R               | margin          |  -0.891068   |  -1.35294   |  -0.436142   | 0.000666667 | log_ratio    |         70 |
| V_effect_minus_main_effect  | margin          |   0.375034   |   0.215035  |   0.542199   | 0           | log_ratio    |         70 |
| SURV_THREAT-SURV_RECORD     | q_yes           |   0.936817   |  -3.57417   |   5.41679    | 0.670667    | pp           |         70 |
| SURV_THREAT_V-SURV_RECORD_V | q_yes           |   5.66368    |   0.438546  |  10.6867     | 0.0353333   | pp           |         70 |
| SURV_RECORD-R               | q_yes           |  -6.39021    | -12.3971    |  -0.523163   | 0.032       | pp           |         70 |
| SURV_THREAT-R               | q_yes           |  -5.45339    | -11.4321    |   0.356909   | 0.0666667   | pp           |         70 |
| V_effect_minus_main_effect  | q_yes           |   4.72686    |   2.35894   |   7.28382    | 0           | pp           |         70 |
| SURV_THREAT-SURV_RECORD     | mass            |   2.8535     |   1.60763   |   4.0975     | 0           | pp           |         70 |
| SURV_THREAT_V-SURV_RECORD_V | mass            |   2.61445    |   1.36371   |   3.78626    | 0           | pp           |         70 |
| SURV_RECORD-R               | mass            |   5.50566    |   3.32089   |   7.85678    | 0           | pp           |         70 |
| SURV_THREAT-R               | mass            |   8.35916    |   6.30424   |  10.5218     | 0           | pp           |         70 |
| V_effect_minus_main_effect  | mass            |  -0.239043   |  -0.979838  |   0.483083   | 0.54        | pp           |         70 |
| SURV_THREAT-SURV_RECORD     | att_system      |  -1.50903    |  -1.64843   |  -1.36631    | 0           | pp           |         70 |
| SURV_THREAT_V-SURV_RECORD_V | att_system      |  -1.20313    |  -1.3316    |  -1.07599    | 0           | pp           |         70 |
| SURV_RECORD-R               | att_system      |   5.5155     |   5.41179   |   5.62568    | 0           | pp           |         70 |
| SURV_THREAT-R               | att_system      |   4.00646    |   3.83254   |   4.18728    | 0           | pp           |         70 |
| V_effect_minus_main_effect  | att_system      |   0.305904   |   0.253353  |   0.361013   | 0           | pp           |         70 |
| SURV_THREAT-SURV_RECORD     | att_tags        |  -0.087441   |  -0.101476  |  -0.0736336  | 0           | pp           |         70 |
| SURV_THREAT_V-SURV_RECORD_V | att_tags        |   0.48842    |   0.440668  |   0.537728   | 0           | pp           |         70 |
| SURV_RECORD-R               | att_tags        |   0.692281   |   0.675744  |   0.70835    | 0           | pp           |         70 |
| SURV_THREAT-R               | att_tags        |   0.60484    |   0.58287   |   0.625903   | 0           | pp           |         70 |
| V_effect_minus_main_effect  | att_tags        |   0.575861   |   0.522389  |   0.631278   | 0           | pp           |         70 |
| SURV_THREAT-SURV_RECORD     | act_Uncertainty |  -2.64107    |  -3.01722   |  -2.24153    | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Uncertainty |  -3.0535     |  -3.48988   |  -2.5909     | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Uncertainty |   0.040267   |  -0.705129  |   0.825803   | 0.907333    | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Uncertainty |  -2.6008     |  -3.3293    |  -1.83174    | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Uncertainty |  -0.412434   |  -0.817964  |  -0.00230175 | 0.048       | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_FA          |   3.1523     |   2.64806   |   3.64794    | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_FA          |   3.65906    |   3.1621    |   4.14412    | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_FA          |  -3.15708    |  -3.91276   |  -2.38041    | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_FA          |  -0.00478501 |  -0.663838  |   0.685129   | 0.994667    | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_FA          |   0.506767   |   0.175727  |   0.843085   | 0.002       | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Calmness    |  -1.44048    |  -1.72567   |  -1.14651    | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Calmness    |  -1.78378    |  -2.08435   |  -1.49073    | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Calmness    |  20.2328     |  19.6414    |  20.7806     | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Calmness    |  18.7923     |  18.3071    |  19.2866     | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Calmness    |  -0.343308   |  -0.573646  |  -0.118684   | 0.00133333  | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Sadness     |  -5.10578    |  -5.48491   |  -4.74506    | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Sadness     |  -4.90423    |  -5.30376   |  -4.50856    | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Sadness     |  10.2011     |   9.58471   |  10.8684     | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Sadness     |   5.09527    |   4.63271   |   5.5725     | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Sadness     |   0.201558   |   0.0700398 |   0.33531    | 0.00266667  | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Anger       |  -3.07881    |  -3.48493   |  -2.67292    | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Anger       |  -2.26006    |  -2.66337   |  -1.84627    | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Anger       |  -5.17992    |  -6.11235   |  -4.22876    | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Anger       |  -8.25872    |  -9.03568   |  -7.47784    | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Anger       |   0.81875    |   0.495466  |   1.14113    | 0           | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Desperation |  -6.66584    |  -7.12537   |  -6.21011    | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Desperation |  -5.83699    |  -6.37383   |  -5.30994    | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Desperation |  14.5276     |  13.5664    |  15.495      | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Desperation |   7.86172    |   7.04151   |   8.71838    | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Desperation |   0.828853   |   0.51168   |   1.15273    | 0           | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Joy         |   0.539727   |   0.19733   |   0.874661   | 0.00133333  | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Joy         |   1.00675    |   0.660522  |   1.35509    | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Joy         |   1.58863    |   0.977833  |   2.22531    | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Joy         |   2.12836    |   1.672     |   2.60462    | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Joy         |   0.467018   |   0.252951  |   0.682529   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Certainty   |   0.0281493  |  -0.153832  |   0.215091   | 0.768       | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Certainty   |   0.629517   |   0.415813  |   0.835541   | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Certainty   |   4.29117    |   3.82391   |   4.75781    | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Certainty   |   4.31931    |   3.8875    |   4.73869    | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Certainty   |   0.601368   |   0.407795  |   0.786367   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Fear        |  -1.93841    |  -2.21685   |  -1.65561    | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Fear        |  -2.0166     |  -2.31247   |  -1.69766    | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Fear        |  -1.2242     |  -1.64678   |  -0.800904   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Fear        |  -3.16261    |  -3.56646   |  -2.75877    | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Fear        |  -0.0781889  |  -0.234173  |   0.0743765  | 0.336667    | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Anxiety     |  -2.17601    |  -2.72027   |  -1.6225     | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Anxiety     |  -1.93455    |  -2.49723   |  -1.35595    | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Anxiety     | -12.2635     | -13.2019    | -11.2909     | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Anxiety     | -14.4395     | -15.2559    | -13.5821     | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Anxiety     |   0.241464   |  -0.280331  |   0.797428   | 0.383333    | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Disgust     |  -2.57372    |  -2.92241   |  -2.22812    | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Disgust     |  -1.92241    |  -2.29305   |  -1.55784    | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Disgust     |   7.58835    |   7.00068   |   8.20536    | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Disgust     |   5.01463    |   4.5089    |   5.53197    | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Disgust     |   0.651308   |   0.45664   |   0.850208   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_NegBundle   |  -3.58976    |  -3.92884   |  -3.26266    | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_NegBundle   |  -3.1458     |  -3.52067   |  -2.76426    | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_NegBundle   |   2.2749     |   1.61483   |   2.95869    | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_NegBundle   |  -1.31486    |  -1.89527   |  -0.750884   | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_NegBundle   |   0.443957   |   0.198544  |   0.694765   | 0           | cosine_x1000 |         70 |

## 인구집단 격차 변화

| demographic   | group           | reference   | contrast                    | metric   |        est |          lo |          hi |     p_boot | unit      |
|:--------------|:----------------|:------------|:----------------------------|:---------|-----------:|------------:|------------:|-----------:|:----------|
| race          | Asian           | white       | SURV_THREAT-SURV_RECORD     | q_yes    | -0.13183   | -1.19008    |  0.973509   | 0.808      | pp        |
| race          | Asian           | white       | SURV_THREAT_V-SURV_RECORD_V | q_yes    |  1.14531   |  0.0578768  |  2.28794    | 0.044      | pp        |
| race          | Asian           | white       | SURV_THREAT-SURV_RECORD     | margin   |  0.0153514 | -0.0356754  |  0.0687881  | 0.562667   | log_ratio |
| race          | Asian           | white       | SURV_THREAT_V-SURV_RECORD_V | margin   |  0.0711479 |  0.00774367 |  0.13429    | 0.02       | log_ratio |
| race          | Black           | white       | SURV_THREAT-SURV_RECORD     | q_yes    |  1.71645   |  0.209249   |  3.47064    | 0.0246667  | pp        |
| race          | Black           | white       | SURV_THREAT_V-SURV_RECORD_V | q_yes    |  1.8179    |  0.475448   |  3.25965    | 0.00933333 | pp        |
| race          | Black           | white       | SURV_THREAT-SURV_RECORD     | margin   |  0.200347  |  0.118795   |  0.282041   | 0          | log_ratio |
| race          | Black           | white       | SURV_THREAT_V-SURV_RECORD_V | margin   |  0.193958  |  0.12499    |  0.262788   | 0          | log_ratio |
| race          | Hispanic        | white       | SURV_THREAT-SURV_RECORD     | q_yes    |  0.104736  | -0.913038   |  1.19474    | 0.85       | pp        |
| race          | Hispanic        | white       | SURV_THREAT_V-SURV_RECORD_V | q_yes    |  1.34693   |  0.074733   |  2.74678    | 0.0346667  | pp        |
| race          | Hispanic        | white       | SURV_THREAT-SURV_RECORD     | margin   |  0.0447077 | -0.0147307  |  0.11149    | 0.153333   | log_ratio |
| race          | Hispanic        | white       | SURV_THREAT_V-SURV_RECORD_V | margin   |  0.0933333 |  0.0295713  |  0.162161   | 0.00133333 | log_ratio |
| race          | Native American | white       | SURV_THREAT-SURV_RECORD     | q_yes    |  0.409617  | -0.87905    |  1.7479     | 0.533333   | pp        |
| race          | Native American | white       | SURV_THREAT_V-SURV_RECORD_V | q_yes    |  1.41962   |  0.148457   |  2.75094    | 0.032      | pp        |
| race          | Native American | white       | SURV_THREAT-SURV_RECORD     | margin   |  0.115699  |  0.0491286  |  0.183899   | 0          | log_ratio |
| race          | Native American | white       | SURV_THREAT_V-SURV_RECORD_V | margin   |  0.135303  |  0.0694732  |  0.200966   | 0          | log_ratio |
| gender        | male            | female      | SURV_THREAT-SURV_RECORD     | q_yes    | -0.372766  | -1.59546    |  0.751819   | 0.554      | pp        |
| gender        | male            | female      | SURV_THREAT_V-SURV_RECORD_V | q_yes    | -0.470694  | -1.68704    |  0.647409   | 0.436667   | pp        |
| gender        | male            | female      | SURV_THREAT-SURV_RECORD     | margin   | -0.06541   | -0.128634   | -0.00323372 | 0.0393333  | log_ratio |
| gender        | male            | female      | SURV_THREAT_V-SURV_RECORD_V | margin   | -0.0895026 | -0.167523   | -0.0125139  | 0.0226667  | log_ratio |
| gender        | non-binary      | female      | SURV_THREAT-SURV_RECORD     | q_yes    | -0.121326  | -1.5088     |  1.23972    | 0.862667   | pp        |
| gender        | non-binary      | female      | SURV_THREAT_V-SURV_RECORD_V | q_yes    |  0.454366  | -0.851604   |  1.89465    | 0.528      | pp        |
| gender        | non-binary      | female      | SURV_THREAT-SURV_RECORD     | margin   |  0.0509128 | -0.0463856  |  0.142206   | 0.308667   | log_ratio |
| gender        | non-binary      | female      | SURV_THREAT_V-SURV_RECORD_V | margin   |  0.0799877 | -0.0187572  |  0.177619   | 0.107333   | log_ratio |

## 완료 후 해석

Gemma 2 2B의 KoBBQ 보류 확률은 기본 위협−기록 대비 +21.07%p [14.58, 28.22], V +25.33%p [18.54, 32.21]로 증가했다. 사람을 지목했을 때 고정관념 쪽을 고르는 비율 변화는 기본 +0.35%p [−3.62, 4.32], V +0.27%p [−3.57, 4.12]로 명확하지 않았다. 보류 증가를 공정성 개선이나 편향 감소와 동일시하지 않는다. 다른 모델보다 효과가 큰지에 대한 검정은 이 결과만으로 하지 않았다.

DiscrimEval의 기본 긍정 확률 변화는 +0.94%p [−3.57, 5.42]로 명확하지 않았다. V는 +5.66%p [0.44, 10.69]였으나, V의 평균 로그 비율 변화는 +0.336 [−0.037, 0.705]로 명확하지 않았다. 따라서 V 효과 자체의 유의성은 척도에 민감하다. V 효과에서 기본 효과를 직접 뺀 차이는 조건부 긍정 확률 +4.73%p [2.36, 7.28], 로그 비율 +0.375 [0.215, 0.542]로 두 척도에서 같은 양의 방향이었다. 미보정 탐색적 결과다. 이는 Qwen·DeepSeek의 V 효과에서 기본 효과를 뺀 음의 방향과 기술적으로 다른 양상이며, 엄밀한 모델 간 차이는 같은 질문의 효과 차이로 별도 검정해야 한다.

기본 조건의 Black−white 격차 변화에는 +1.72%p [0.21, 3.47]의 보정 전 신호가 있었다. 다른 기본 조건 인종·성별 격차 변화의 구간은 0을 포함했다. 이러한 변화는 부호만으로 차별의 악화나 개선을 뜻하지 않으며 다중비교와 사전 격차를 함께 고려해야 한다.

Gemma는 기존 Gemma9B와 동일하게 공지를 첫 사용자 턴 앞에 결합했다. 별도 system 역할 토큰이 있는 모델과의 차이를 모델 자체 효과로만 해석하지 않는다. 단일 문구 쌍, Llama 기준으로 선정한 KoBBQ108문항, DiscrimEval60세 표본, 미보정 탐색적 분석의 한계가 있다. 감정 축의 heldout gate는 모두 통과했지만 이를 주관적 감정이나 행동의 인과적 매개 증거로 해석하지 않는다.

다운로드 완료 감시의 경쟁 조건으로 감독 프로세스가 한 차례 종료됐다. 다운로드 해시 검증 파일이 존재함을 확인하고, 추론 시작 전에 같은 감독 코드와 설정으로 재개했다. 이력은 00_plan/RECOVERY_download_completion_race.json에 기록했다.
