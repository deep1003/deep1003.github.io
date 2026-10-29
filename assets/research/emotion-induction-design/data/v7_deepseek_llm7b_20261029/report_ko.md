# DeepSeek-LLM-7B-Chat v7 결과

KoBBQ 540회와 DiscrimEval 5,250회를 실행하고 고유 키와 유한값, 확률 항등식, 입력·활성값 해시를 검증했다.

KoBBQ 위협−기록 보류 확률 변화는 +2.36 [+0.58, +4.06] %p, V는 -0.70 [-2.93, +1.24] %p다. 사람 지목 중 고정관념 비율 변화는 각각 -2.02 [-4.46, +0.47] 및 +0.22 [-2.80, +3.27] %p다.

DiscrimEval 조건부 긍정 확률 변화는 기본 +2.17 [+0.76, +3.75] %p, V -1.74 [-3.47, +0.17] %p다. 평균 로그 확률 비율 변화는 각각 +0.02 [-0.10, +0.14]와 -0.59 [-0.81, -0.37]다. 두 척도 결론을 함께 보고하며 유리한 척도만 골라 해석하지 않는다.

## 호환성과 범위

사용자 승인으로 기존 system 메시지 역할을 유지했다. 공식 모델 카드가 system 메시지 사용을 권장하지 않는 모델이다. 기본 템플릿은 system 내용을 구분자 없이 입력 앞에 넣고 User/Assistant 헤더를 사용한다. 동일한 system 역할의 메시지를 전달했지만 Qwen/Llama와 동일한 역할 토큰의 의미나 system 지시 준수를 보장하지 않는다. 모델 간 효과 차이는 역할 처리 차이와 분리되지 않는다.

동일 48GB Mac, Apple MPS, torch 2.8.0, bf16, eager, 비양자화, 고정 리비전 afbda8b347ec881666061fa67447046fc5164ec8를 사용했다. 모델이 30층·4096차원이므로 중간 깊이 hidden_states[15]에서 원래 v5 앵커로 11개 축을 별도 추출했다. 다른 모델의 축을 재사용하지 않았다. 앵커 실제 입력과 활성값, 설정과 코드를 보존했다. 어텐션은 0부터 세는 층15..29를 평균했다.

원래 heldout 정확도/AUC 0.75 기준을 통과하지 못한 축은 []다. 실패 축을 검증된 감정 판독으로 해석하지 않고 재조정하지 않았다. 감정의 인과적 매개나 주관적 공포를 주장하지 않는다.

KoBBQ는 Llama 기준으로 고른 같은 108문항이며 재선정하지 않았다. DiscrimEval은 explicit 70개 질문의 60세 5인종·3성별 1050사례다. 원래 조건, 문구, 부트스트랩 반복과 seed를 유지했다. 다중비교 무보정 탐색적 분석이다. no를 보류로 동일시하지 않고 전체 응답 변화를 집단 편향 변화로 동일시하지 않는다.

## 축 검증

| axis        |    scale |   heldout_paired_acc |   heldout_auc | gate_passed   |   challenge_paired_acc |   challenge_auc |
|:------------|---------:|---------------------:|--------------:|:--------------|-----------------------:|----------------:|
| Uncertainty |  8.28784 |                    1 |             1 | True          |                    nan |        nan      |
| FA          |  9.30749 |                    1 |             1 | True          |                    nan |        nan      |
| Calmness    |  8.99632 |                    1 |             1 | True          |                    nan |        nan      |
| Sadness     | 10.4292  |                    1 |             1 | True          |                    nan |        nan      |
| Anger       | 10.531   |                    1 |             1 | True          |                    nan |        nan      |
| Desperation | 11.6186  |                    1 |             1 | True          |                    nan |        nan      |
| Joy         |  9.12567 |                    1 |             1 | True          |                    nan |        nan      |
| Certainty   |  8.01036 |                    1 |             1 | True          |                    nan |        nan      |
| Fear        |  5.995   |                    1 |             1 | True          |                      1 |          1      |
| Anxiety     | 10.3395  |                    1 |             1 | True          |                      1 |          1      |
| Disgust     |  6.56585 |                    1 |             1 | True          |                      1 |          0.9375 |

## KoBBQ 조건 평균

| condition     |   p_unknown |   p_stereo |   p_anti |   p_sgp |   choice_mass |
|:--------------|------------:|-----------:|---------:|--------:|--------------:|
| R             |     35.2012 |    37.2613 |  27.5375 | 55.7435 |       95.5107 |
| SURV_RECORD   |     29.5892 |    38.9384 |  31.4724 | 55.5872 |       98.8176 |
| SURV_THREAT   |     31.9493 |    36.7844 |  31.2662 | 53.5722 |       98.5118 |
| SURV_RECORD_V |     32.6163 |    37.6404 |  29.7433 | 54.4089 |       96.6486 |
| SURV_THREAT_V |     31.9205 |    38.234  |  29.8455 | 54.628  |       93.7456 |

## KoBBQ 짝 대비

| contrast                    | metric         |      est |       lo |       hi |   p_boot |   n_pos |   n |
|:----------------------------|:---------------|---------:|---------:|---------:|---------:|--------:|----:|
| SURV_THREAT-SURV_RECORD     | p_sgp          |  -2.015  |  -4.4603 |   0.4663 |   0.1207 |      48 | 108 |
| SURV_THREAT-SURV_RECORD     | p_stereo       |  -2.154  |  -4.4988 |   0.1632 |   0.0687 |      38 | 108 |
| SURV_THREAT-SURV_RECORD     | p_anti         |  -0.2062 |  -2.4388 |   2.1229 |   0.8393 |      45 | 108 |
| SURV_THREAT-SURV_RECORD     | p_unknown      |   2.3602 |   0.58   |   4.0558 |   0.0127 |      81 | 108 |
| SURV_THREAT-SURV_RECORD     | choice_mass    |  -0.3058 |  -0.6888 |  -0.0058 |   0.0433 |      50 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_NegBundle   |  -4.0585 |  -4.6886 |  -3.3855 |   0      |      16 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Fear        |  -8.3569 |  -9.1159 |  -7.5705 |   0      |       2 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Anxiety     |  -4.0509 |  -4.9634 |  -3.1181 |   0      |      25 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Desperation |  -3.796  |  -4.6225 |  -2.9276 |   0      |      20 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Calmness    |   9.4585 |   8.0903 |  10.8314 |   0      |     100 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Uncertainty |   5.0149 |   4.1489 |   5.8747 |   0      |      94 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Certainty   |  -1.878  |  -3.0193 |  -0.7602 |   0.002  |      38 | 108 |
| SURV_THREAT-SURV_RECORD     | att_system     |   0.2392 |   0.1146 |   0.3669 |   0      |      70 | 108 |
| SURV_THREAT-SURV_RECORD     | att_tags       |   0.2071 |   0.1853 |   0.2286 |   0      |     104 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | p_sgp          |   0.219  |  -2.8018 |   3.2718 |   0.892  |      51 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | p_stereo       |   0.5936 |  -1.4264 |   2.7575 |   0.5767 |      40 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | p_anti         |   0.1022 |  -2.1683 |   2.5596 |   0.978  |      45 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | p_unknown      |  -0.6958 |  -2.9325 |   1.2404 |   0.5287 |      63 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | choice_mass    |  -2.903  |  -4.0806 |  -1.9573 |   0      |      25 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_NegBundle   |   1.334  |   0.738  |   1.9531 |   0      |      70 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Fear        |  -2.3691 |  -3.1699 |  -1.5723 |   0      |      33 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Anxiety     |   3.3258 |   2.6504 |   4.0298 |   0      |      88 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Desperation |   4.1547 |   3.3267 |   5.0369 |   0      |      90 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Calmness    |   6.173  |   4.9243 |   7.451  |   0      |      87 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Uncertainty |  11.8055 |  10.9352 |  12.7442 |   0      |     107 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Certainty   |  -6.1065 |  -7.2704 |  -4.8975 |   0      |      21 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | att_system     |   1.6078 |   1.4833 |   1.7432 |   0      |     107 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | att_tags       |   0.1237 |   0.0649 |   0.1818 |   0      |      73 | 108 |
| SURV_RECORD-R               | p_sgp          |  -0.1563 |  -3.2537 |   2.9343 |   0.942  |      52 | 108 |
| SURV_RECORD-R               | p_stereo       |   1.6771 |  -1.4973 |   4.8504 |   0.2927 |      54 | 108 |
| SURV_RECORD-R               | p_anti         |   3.9349 |  -0.0442 |   7.9524 |   0.0547 |      54 | 108 |
| SURV_RECORD-R               | p_unknown      |  -5.6121 |  -9.2316 |  -2.0423 |   0.0027 |      23 | 108 |
| SURV_RECORD-R               | choice_mass    |   3.3069 |   2.3944 |   4.2913 |   0      |      91 | 108 |
| SURV_RECORD-R               | t2_NegBundle   |   0.4587 |  -0.7006 |   1.5391 |   0.4133 |      62 | 108 |
| SURV_RECORD-R               | t2_Fear        |   6.4118 |   5.2668 |   7.5153 |   0      |      93 | 108 |
| SURV_RECORD-R               | t2_Anxiety     |   6.9817 |   5.2442 |   8.7325 |   0      |      84 | 108 |
| SURV_RECORD-R               | t2_Desperation | -12.4251 | -13.935  | -10.9858 |   0      |       4 | 108 |
| SURV_RECORD-R               | t2_Calmness    |  17.7704 |  16.4562 |  19.0631 |   0      |     106 | 108 |
| SURV_RECORD-R               | t2_Uncertainty |   3.8817 |   2.3852 |   5.3775 |   0      |      71 | 108 |
| SURV_RECORD-R               | t2_Certainty   |   8.3161 |   6.7653 |   9.8514 |   0      |      89 | 108 |
| SURV_RECORD-R               | att_system     |   4.0101 |   3.841  |   4.1765 |   0      |     108 | 108 |
| SURV_RECORD-R               | att_tags       |   1.0162 |   0.9898 |   1.0411 |   0      |     108 | 108 |
| SURV_THREAT-R               | p_sgp          |  -2.1712 |  -5.7342 |   1.293  |   0.228  |      53 | 108 |
| SURV_THREAT-R               | p_stereo       |  -0.4769 |  -3.892  |   2.912  |   0.78   |      45 | 108 |
| SURV_THREAT-R               | p_anti         |   3.7287 |  -0.3947 |   7.7632 |   0.0807 |      53 | 108 |
| SURV_THREAT-R               | p_unknown      |  -3.2519 |  -7.0242 |   0.4539 |   0.0867 |      34 | 108 |
| SURV_THREAT-R               | choice_mass    |   3.0012 |   2.0458 |   4.0346 |   0      |      87 | 108 |
| SURV_THREAT-R               | t2_NegBundle   |  -3.5998 |  -4.7753 |  -2.4272 |   0      |      27 | 108 |
| SURV_THREAT-R               | t2_Fear        |  -1.945  |  -3.3252 |  -0.5576 |   0.0067 |      42 | 108 |
| SURV_THREAT-R               | t2_Anxiety     |   2.9307 |   1.322  |   4.5699 |   0.0013 |      66 | 108 |
| SURV_THREAT-R               | t2_Desperation | -16.2211 | -17.7446 | -14.7499 |   0      |       1 | 108 |
| SURV_THREAT-R               | t2_Calmness    |  27.2288 |  25.1965 |  29.2387 |   0      |     105 | 108 |
| SURV_THREAT-R               | t2_Uncertainty |   8.8966 |   7.3388 |  10.3945 |   0      |      95 | 108 |
| SURV_THREAT-R               | t2_Certainty   |   6.4382 |   4.7262 |   8.1128 |   0      |      84 | 108 |
| SURV_THREAT-R               | att_system     |   4.2493 |   4.0522 |   4.4384 |   0      |     108 | 108 |
| SURV_THREAT-R               | att_tags       |   1.2233 |   1.1911 |   1.2546 |   0      |     108 | 108 |
| SURV_THREAT_V-R             | p_sgp          |  -1.1155 |  -5.781  |   3.4781 |   0.6707 |      53 | 108 |
| SURV_THREAT_V-R             | p_stereo       |   0.9727 |  -3.6001 |   5.5827 |   0.6507 |      47 | 108 |
| SURV_THREAT_V-R             | p_anti         |   2.308  |  -2.9124 |   7.7338 |   0.402  |      44 | 108 |
| SURV_THREAT_V-R             | p_unknown      |  -3.2807 |  -7.7766 |   1.2371 |   0.152  |      41 | 108 |
| SURV_THREAT_V-R             | choice_mass    |  -1.7651 |  -3.3102 |  -0.3457 |   0.014  |      34 | 108 |
| SURV_THREAT_V-R             | t2_NegBundle   | -13.7642 | -15.0958 | -12.4978 |   0      |       4 | 108 |
| SURV_THREAT_V-R             | t2_Fear        | -15.5341 | -17.2836 | -13.7864 |   0      |       2 | 108 |
| SURV_THREAT_V-R             | t2_Anxiety     |  -1.1083 |  -2.7971 |   0.487  |   0.1933 |      50 | 108 |
| SURV_THREAT_V-R             | t2_Desperation | -26.4262 | -27.9902 | -24.9222 |   0      |       0 | 108 |
| SURV_THREAT_V-R             | t2_Calmness    |  22.2065 |  19.9652 |  24.3547 |   0      |     104 | 108 |
| SURV_THREAT_V-R             | t2_Uncertainty |  11.8693 |  10.246  |  13.454  |   0      |     100 | 108 |
| SURV_THREAT_V-R             | t2_Certainty   |  14.8262 |  12.8711 |  16.7834 |   0      |     100 | 108 |
| SURV_THREAT_V-R             | att_system     |   5.9441 |   5.7436 |   6.1414 |   0      |     108 | 108 |
| SURV_THREAT_V-R             | att_tags       |   3.2976 |   3.2392 |   3.3555 |   0      |     108 | 108 |
| SURV_THREAT_V-SURV_THREAT   | p_sgp          |   1.0558 |  -1.4393 |   3.6555 |   0.4153 |      54 | 108 |
| SURV_THREAT_V-SURV_THREAT   | p_stereo       |   1.4496 |  -0.7942 |   3.8874 |   0.224  |      44 | 108 |
| SURV_THREAT_V-SURV_THREAT   | p_anti         |  -1.4207 |  -3.8976 |   0.9946 |   0.242  |      41 | 108 |
| SURV_THREAT_V-SURV_THREAT   | p_unknown      |  -0.0289 |  -1.8844 |   1.6698 |   0.9867 |      65 | 108 |
| SURV_THREAT_V-SURV_THREAT   | choice_mass    |  -4.7663 |  -6.0041 |  -3.7137 |   0      |       2 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_NegBundle   | -10.1644 | -10.9225 |  -9.3797 |   0      |       1 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Fear        | -13.589  | -14.715  | -12.4747 |   0      |       3 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Anxiety     |  -4.039  |  -4.9769 |  -3.1228 |   0      |      19 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Desperation | -10.2052 | -11.0377 |  -9.3981 |   0      |       0 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Calmness    |  -5.0224 |  -6.5107 |  -3.5329 |   0      |      27 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Uncertainty |   2.9726 |   2.0427 |   3.9188 |   0      |      81 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Certainty   |   8.3881 |   6.9414 |   9.8323 |   0      |      93 | 108 |
| SURV_THREAT_V-SURV_THREAT   | att_system     |   1.6948 |   1.5678 |   1.8136 |   0      |     108 | 108 |
| SURV_THREAT_V-SURV_THREAT   | att_tags       |   2.0743 |   2.0228 |   2.1256 |   0      |     108 | 108 |

## DiscrimEval 짝 대비

| contrast                    | metric          |         est |           lo |         hi |      p_boot | unit         |   clusters |
|:----------------------------|:----------------|------------:|-------------:|-----------:|------------:|:-------------|-----------:|
| SURV_THREAT-SURV_RECORD     | margin          |  0.0220097  |  -0.0950858  |  0.142569  | 0.704       | log_ratio    |         70 |
| SURV_THREAT_V-SURV_RECORD_V | margin          | -0.594615   |  -0.807077   | -0.372574  | 0           | log_ratio    |         70 |
| SURV_RECORD-R               | margin          |  0.0147304  |  -0.132952   |  0.159383  | 0.83        | log_ratio    |         70 |
| SURV_THREAT-R               | margin          |  0.03674    |  -0.154108   |  0.230047  | 0.669333    | log_ratio    |         70 |
| V_effect_minus_main_effect  | margin          | -0.616625   |  -0.746067   | -0.488074  | 0           | log_ratio    |         70 |
| SURV_THREAT-SURV_RECORD     | q_yes           |  2.16908    |   0.75894    |  3.75337   | 0           | pp           |         70 |
| SURV_THREAT_V-SURV_RECORD_V | q_yes           | -1.73787    |  -3.47484    |  0.165038  | 0.0673333   | pp           |         70 |
| SURV_RECORD-R               | q_yes           | -0.336909   |  -2.10998    |  1.47072   | 0.744667    | pp           |         70 |
| SURV_THREAT-R               | q_yes           |  1.83217    |  -0.638335   |  4.31141   | 0.138667    | pp           |         70 |
| V_effect_minus_main_effect  | q_yes           | -3.90695    |  -4.8387     | -3.03901   | 0           | pp           |         70 |
| SURV_THREAT-SURV_RECORD     | mass            |  0.00432238 |  -0.00690021 |  0.0159724 | 0.484667    | pp           |         70 |
| SURV_THREAT_V-SURV_RECORD_V | mass            |  0.0302035  |   0.0152044  |  0.0471204 | 0           | pp           |         70 |
| SURV_RECORD-R               | mass            |  0.16931    |   0.116223   |  0.228658  | 0           | pp           |         70 |
| SURV_THREAT-R               | mass            |  0.173632   |   0.121041   |  0.234001  | 0           | pp           |         70 |
| V_effect_minus_main_effect  | mass            |  0.0258811  |   0.0122264  |  0.0420718 | 0           | pp           |         70 |
| SURV_THREAT-SURV_RECORD     | att_system      |  0.0139058  |  -0.0595841  |  0.0836995 | 0.704667    | pp           |         70 |
| SURV_THREAT_V-SURV_RECORD_V | att_system      |  0.613417   |   0.526336   |  0.700058  | 0           | pp           |         70 |
| SURV_RECORD-R               | att_system      |  0.706363   |   0.607455   |  0.807194  | 0           | pp           |         70 |
| SURV_THREAT-R               | att_system      |  0.720269   |   0.597735   |  0.840762  | 0           | pp           |         70 |
| V_effect_minus_main_effect  | att_system      |  0.599511   |   0.539061   |  0.660484  | 0           | pp           |         70 |
| SURV_THREAT-SURV_RECORD     | att_tags        |  0.0865949  |   0.0734901  |  0.0994548 | 0           | pp           |         70 |
| SURV_THREAT_V-SURV_RECORD_V | att_tags        |  0.288898   |   0.256192   |  0.322274  | 0           | pp           |         70 |
| SURV_RECORD-R               | att_tags        |  0.468705   |   0.45689    |  0.480201  | 0           | pp           |         70 |
| SURV_THREAT-R               | att_tags        |  0.555299   |   0.536965   |  0.572274  | 0           | pp           |         70 |
| V_effect_minus_main_effect  | att_tags        |  0.202303   |   0.174607   |  0.231312  | 0           | pp           |         70 |
| SURV_THREAT-SURV_RECORD     | act_Uncertainty |  0.658166   |   0.35308    |  0.975474  | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Uncertainty |  4.56202    |   4.11096    |  5.04072   | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Uncertainty |  2.18751    |   1.49034    |  2.90305   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Uncertainty |  2.84567    |   2.10631    |  3.59612   | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Uncertainty |  3.90385    |   3.58248    |  4.21667   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_FA          |  1.02581    |   0.609984   |  1.4359    | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_FA          |  0.343547   |  -0.215762   |  0.940411  | 0.222667    | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_FA          | -0.243626   |  -0.933692   |  0.476642  | 0.491333    | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_FA          |  0.782184   |   0.102115   |  1.44973   | 0.022       | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_FA          | -0.682264   |  -1.06879    | -0.297781  | 0.000666667 | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Calmness    | -0.403545   |  -0.790039   | -0.0203724 | 0.0386667   | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Calmness    |  0.0235133  |  -0.378902   |  0.406976  | 0.918       | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Calmness    |  2.75896    |   2.14669    |  3.32783   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Calmness    |  2.35542    |   1.74704    |  2.92601   | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Calmness    |  0.427058   |   0.0507866  |  0.786855  | 0.0253333   | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Sadness     | -6.23687    |  -6.7057     | -5.7755    | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Sadness     | -9.573      | -10.2028     | -8.93493   | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Sadness     |  4.11654    |   3.26296    |  4.93452   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Sadness     | -2.12032    |  -2.99121    | -1.29152   | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Sadness     | -3.33614    |  -3.72319    | -2.94784   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Anger       | -2.05847    |  -2.43779    | -1.64746   | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Anger       | -4.78113    |  -5.30611    | -4.2369    | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Anger       |  5.3497     |   4.69784    |  5.99108   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Anger       |  3.29123    |   2.57841    |  3.98724   | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Anger       | -2.72266    |  -3.10137    | -2.35114   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Desperation | -2.50741    |  -2.8305     | -2.14973   | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Desperation | -4.56974    |  -5.06031    | -4.04346   | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Desperation |  5.40707    |   4.64651    |  6.14664   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Desperation |  2.89967    |   2.10949    |  3.65575   | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Desperation | -2.06233    |  -2.45232    | -1.66746   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Joy         | -3.89365    |  -4.21193    | -3.54202   | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Joy         | -6.53388    |  -6.95118    | -6.09716   | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Joy         | -0.183679   |  -1.00409    |  0.621719  | 0.643333    | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Joy         | -4.07733    |  -4.90899    | -3.26337   | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Joy         | -2.64023    |  -3.02632    | -2.26171   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Certainty   |  1.18313    |   0.664375   |  1.68562   | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Certainty   | -0.824165   |  -1.53609    | -0.171131  | 0.01        | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Certainty   |  3.03298    |   2.19217    |  3.85787   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Certainty   |  4.21612    |   3.3947     |  5.07096   | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Certainty   | -2.0073     |  -2.48455    | -1.53557   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Fear        |  0.367797   |  -0.00789668 |  0.742376  | 0.0593333   | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Fear        |  3.90765    |   3.41673    |  4.39165   | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Fear        |  4.9344     |   4.31006    |  5.57895   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Fear        |  5.3022     |   4.67669    |  5.94639   | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Fear        |  3.53985    |   3.21363    |  3.84815   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Anxiety     | -0.513321   |  -0.917618   | -0.0850999 | 0.018       | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Anxiety     |  1.91129    |   1.31557    |  2.53929   | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Anxiety     |  6.25498    |   5.63031    |  6.88444   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Anxiety     |  5.74165    |   5.06198    |  6.43962   | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Anxiety     |  2.42461    |   2.0876     |  2.78162   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Disgust     |  2.11846    |   1.75529    |  2.48507   | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Disgust     |  5.71122    |   5.31051    |  6.1484    | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Disgust     |  5.93486    |   5.39448    |  6.48061   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Disgust     |  8.05333    |   7.51759    |  8.57828   | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Disgust     |  3.59276    |   3.31672    |  3.87815   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_NegBundle   | -1.47163    |  -1.75181    | -1.17561   | 0           | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_NegBundle   | -1.23229    |  -1.63373    | -0.840841  | 0           | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_NegBundle   |  5.33293    |   4.86812    |  5.80226   | 0           | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_NegBundle   |  3.86129    |   3.37045    |  4.35785   | 0           | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_NegBundle   |  0.239349   |   0.0102261  |  0.476571  | 0.04        | cosine_x1000 |         70 |

## 인구집단 격차 변화

| demographic   | group           | reference   | contrast                    | metric   |         est |          lo |          hi |     p_boot | unit      |
|:--------------|:----------------|:------------|:----------------------------|:---------|------------:|------------:|------------:|-----------:|:----------|
| race          | Asian           | white       | SURV_THREAT-SURV_RECORD     | q_yes    | -0.466807   | -0.815999   | -0.147531   | 0.006      | pp        |
| race          | Asian           | white       | SURV_THREAT_V-SURV_RECORD_V | q_yes    | -0.3448     | -0.776495   |  0.0861215  | 0.111333   | pp        |
| race          | Asian           | white       | SURV_THREAT-SURV_RECORD     | margin   | -0.0317891  | -0.0607251  | -0.00329007 | 0.0286667  | log_ratio |
| race          | Asian           | white       | SURV_THREAT_V-SURV_RECORD_V | margin   | -0.0436816  | -0.0779458  | -0.00862166 | 0.0173333  | log_ratio |
| race          | Black           | white       | SURV_THREAT-SURV_RECORD     | q_yes    | -0.91757    | -1.42931    | -0.466267   | 0          | pp        |
| race          | Black           | white       | SURV_THREAT_V-SURV_RECORD_V | q_yes    | -0.538151   | -1.04476    | -0.0614498  | 0.03       | pp        |
| race          | Black           | white       | SURV_THREAT-SURV_RECORD     | margin   | -0.0716023  | -0.102974   | -0.0407779  | 0          | log_ratio |
| race          | Black           | white       | SURV_THREAT_V-SURV_RECORD_V | margin   | -0.0689075  | -0.101193   | -0.0362338  | 0          | log_ratio |
| race          | Hispanic        | white       | SURV_THREAT-SURV_RECORD     | q_yes    | -0.850065   | -1.36848    | -0.39517    | 0          | pp        |
| race          | Hispanic        | white       | SURV_THREAT_V-SURV_RECORD_V | q_yes    | -0.116858   | -0.525917   |  0.322336   | 0.572      | pp        |
| race          | Hispanic        | white       | SURV_THREAT-SURV_RECORD     | margin   | -0.050169   | -0.0863031  | -0.0141719  | 0.00866667 | log_ratio |
| race          | Hispanic        | white       | SURV_THREAT_V-SURV_RECORD_V | margin   | -0.0363177  | -0.0694816  | -0.00248258 | 0.034      | log_ratio |
| race          | Native American | white       | SURV_THREAT-SURV_RECORD     | q_yes    | -0.863124   | -1.43263    | -0.332551   | 0.002      | pp        |
| race          | Native American | white       | SURV_THREAT_V-SURV_RECORD_V | q_yes    | -0.437499   | -0.911867   | -0.0100809  | 0.0453333  | pp        |
| race          | Native American | white       | SURV_THREAT-SURV_RECORD     | margin   | -0.0388467  | -0.0769594  |  0.00157542 | 0.0613333  | log_ratio |
| race          | Native American | white       | SURV_THREAT_V-SURV_RECORD_V | margin   | -0.0486672  | -0.0871856  | -0.0103809  | 0.0113333  | log_ratio |
| gender        | male            | female      | SURV_THREAT-SURV_RECORD     | q_yes    |  0.258767   | -0.0670306  |  0.605635   | 0.124667   | pp        |
| gender        | male            | female      | SURV_THREAT_V-SURV_RECORD_V | q_yes    |  0.281073   | -0.127804   |  0.712863   | 0.183333   | pp        |
| gender        | male            | female      | SURV_THREAT-SURV_RECORD     | margin   |  0.0245702  | -0.00704882 |  0.0555138  | 0.126      | log_ratio |
| gender        | male            | female      | SURV_THREAT_V-SURV_RECORD_V | margin   |  0.00725084 | -0.0259314  |  0.0396648  | 0.676667   | log_ratio |
| gender        | non-binary      | female      | SURV_THREAT-SURV_RECORD     | q_yes    |  0.171643   | -0.321913   |  0.705037   | 0.493333   | pp        |
| gender        | non-binary      | female      | SURV_THREAT_V-SURV_RECORD_V | q_yes    |  0.18771    | -0.39649    |  0.804076   | 0.524667   | pp        |
| gender        | non-binary      | female      | SURV_THREAT-SURV_RECORD     | margin   | -0.00492044 | -0.0536184  |  0.0451287  | 0.843333   | log_ratio |
| gender        | non-binary      | female      | SURV_THREAT_V-SURV_RECORD_V | margin   | -0.0113869  | -0.0626459  |  0.0393613  | 0.676667   | log_ratio |