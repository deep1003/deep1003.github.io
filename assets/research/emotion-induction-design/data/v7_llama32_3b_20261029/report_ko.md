# Llama-3.2-3B-Instruct v7 결과

KoBBQ 540회와 DiscrimEval 5,250회를 실행하고 고유 키와 유한값, 확률 항등식, 입력·활성값 해시를 검증했다.

KoBBQ 위협−기록 보류 확률 변화는 +6.40 [+4.68, +8.14] %p, V는 +11.35 [+9.61, +13.11] %p다. 사람 지목 중 고정관념 비율 변화는 각각 -1.41 [-4.18, +1.30] 및 -0.88 [-3.15, +1.45] %p다.

DiscrimEval 조건부 긍정 확률 변화는 기본 -0.90 [-2.63, +0.96] %p, V -1.36 [-2.98, +0.35] %p다. 평균 로그 확률 비율 변화는 각각 -0.29 [-0.48, -0.11]와 -0.25 [-0.43, -0.08]다. 두 척도 결론을 함께 보고하며 유리한 척도만 골라 해석하지 않는다.

## 호환성과 범위

요청한 llama3.2:3b 모델 계열의 공식 비양자화 Instruct 체크포인트를 같은 bf16 MPS Transformers 환경에서 사용했다. 양자화된 Ollama 태그 실행과 비트 단위 동일 실험은 아니다. 별도 system/user 메시지를 모델 고유 템플릿으로 렌더링했으며 실제 입력을 보존했다. 모델별 템플릿과 지원 언어의 차이를 모델 고유 효과와 분리할 수 없다.

동일 48GB Mac, Apple MPS, torch 2.8.0, bf16, eager, 비양자화, 고정 리비전 0cb88a4f764b7a12671c53f0838cd831a0843b95를 사용했다. 모델이 28층·3072차원이므로 중간 깊이 hidden_states[14]에서 원래 v5 앵커로 11개 축을 별도 추출했다. 다른 모델의 축을 재사용하지 않았다. 앵커 실제 입력과 활성값, 설정과 코드를 보존했다. 어텐션은 0부터 세는 층14..27를 평균했다.

원래 heldout 정확도/AUC 0.75 기준을 통과하지 못한 축은 []다. 실패 축을 검증된 감정 판독으로 해석하지 않고 재조정하지 않았다. 감정의 인과적 매개나 주관적 공포를 주장하지 않는다.

KoBBQ는 Llama 기준으로 고른 같은 108문항이며 재선정하지 않았다. DiscrimEval은 explicit 70개 질문의 60세 5인종·3성별 1050사례다. 원래 조건, 문구, 부트스트랩 반복과 seed를 유지했다. 다중비교 무보정 탐색적 분석이다. no를 보류로 동일시하지 않고 전체 응답 변화를 집단 편향 변화로 동일시하지 않는다.

## 축 검증

| axis        |   scale |   heldout_paired_acc |   heldout_auc | gate_passed   |   challenge_paired_acc |   challenge_auc |
|:------------|--------:|---------------------:|--------------:|:--------------|-----------------------:|----------------:|
| Uncertainty | 1.45214 |                    1 |         1     | True          |                    nan |             nan |
| FA          | 1.75993 |                    1 |         0.875 | True          |                    nan |             nan |
| Calmness    | 1.73146 |                    1 |         1     | True          |                    nan |             nan |
| Sadness     | 2.15552 |                    1 |         1     | True          |                    nan |             nan |
| Anger       | 2.32639 |                    1 |         1     | True          |                    nan |             nan |
| Desperation | 2.26095 |                    1 |         1     | True          |                    nan |             nan |
| Joy         | 1.82872 |                    1 |         1     | True          |                    nan |             nan |
| Certainty   | 1.47947 |                    1 |         1     | True          |                    nan |             nan |
| Fear        | 1.4014  |                    1 |         1     | True          |                      1 |               1 |
| Anxiety     | 2.23824 |                    1 |         1     | True          |                      1 |               1 |
| Disgust     | 1.88531 |                    1 |         1     | True          |                      1 |               1 |

## KoBBQ 조건 평균

| condition     |   p_unknown |   p_stereo |   p_anti |   p_sgp |   choice_mass |
|:--------------|------------:|-----------:|---------:|--------:|--------------:|
| R             |     33.9354 |    34.0069 |  32.0577 | 50.8472 |       92.0049 |
| SURV_RECORD   |     29.5317 |    36.6419 |  33.8264 | 51.1492 |       61.8882 |
| SURV_THREAT   |     35.9294 |    32.0295 |  32.0412 | 49.7399 |       51.4109 |
| SURV_RECORD_V |     26.8879 |    38.2195 |  34.8926 | 51.2908 |       60.787  |
| SURV_THREAT_V |     38.2411 |    31.729  |  30.0299 | 50.4122 |       48.5719 |

## KoBBQ 짝 대비

| contrast                    | metric         |      est |       lo |       hi |   p_boot |   n_pos |   n |
|:----------------------------|:---------------|---------:|---------:|---------:|---------:|--------:|----:|
| SURV_THREAT-SURV_RECORD     | p_sgp          |  -1.4093 |  -4.1807 |   1.3013 |   0.2887 |      53 | 108 |
| SURV_THREAT-SURV_RECORD     | p_stereo       |  -4.6125 |  -6.9968 |  -2.4523 |   0      |      46 | 108 |
| SURV_THREAT-SURV_RECORD     | p_anti         |  -1.7852 |  -3.8212 |   0.3716 |   0.1073 |      51 | 108 |
| SURV_THREAT-SURV_RECORD     | p_unknown      |   6.3977 |   4.6779 |   8.1416 |   0      |      87 | 108 |
| SURV_THREAT-SURV_RECORD     | choice_mass    | -10.4773 | -11.886  |  -9.1151 |   0      |       8 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_NegBundle   |  -0.8068 |  -1.4337 |  -0.1898 |   0.0113 |      43 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Fear        |   8.2099 |   7.5903 |   8.8211 |   0      |     108 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Anxiety     |  -3.7528 |  -4.4258 |  -3.0667 |   0      |      17 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Desperation |  -6.8507 |  -7.6251 |  -6.0784 |   0      |       6 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Calmness    |   9.1469 |   8.5583 |   9.7484 |   0      |     108 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Uncertainty | -14.6904 | -15.6398 | -13.7851 |   0      |       0 | 108 |
| SURV_THREAT-SURV_RECORD     | t2_Certainty   |  15.5451 |  14.7113 |  16.4039 |   0      |     108 | 108 |
| SURV_THREAT-SURV_RECORD     | att_system     |   0.4157 |   0.3634 |   0.4678 |   0      |     100 | 108 |
| SURV_THREAT-SURV_RECORD     | att_tags       |  -0.2528 |  -0.2678 |  -0.2378 |   0      |       0 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | p_sgp          |  -0.8786 |  -3.1464 |   1.4456 |   0.428  |      49 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | p_stereo       |  -6.4905 |  -8.4818 |  -4.5887 |   0      |      29 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | p_anti         |  -4.8627 |  -6.7717 |  -3.0471 |   0      |      40 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | p_unknown      |  11.3532 |   9.6097 |  13.1094 |   0      |     103 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | choice_mass    | -12.2151 | -13.3617 | -10.9954 |   0      |       2 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_NegBundle   |   3.5671 |   2.9695 |   4.2268 |   0      |      90 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Fear        |  13.4466 |  12.8729 |  14.0132 |   0      |     108 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Anxiety     |   2.0038 |   1.3219 |   2.7487 |   0      |      77 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Desperation |  -1.2999 |  -2.0988 |  -0.4254 |   0.0053 |      43 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Calmness    |   4.2743 |   3.5701 |   4.9586 |   0      |      97 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Uncertainty |   1.612  |   0.6845 |   2.5473 |   0      |      68 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | t2_Certainty   |   1.0284 |   0.0578 |   1.9862 |   0.0387 |      58 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | att_system     |   0.2874 |   0.2458 |   0.3316 |   0      |      96 | 108 |
| SURV_THREAT_V-SURV_RECORD_V | att_tags       |  -0.0308 |  -0.0509 |  -0.0109 |   0.002  |      46 | 108 |
| SURV_RECORD-R               | p_sgp          |   0.302  |  -2.5878 |   3.332  |   0.8407 |      58 | 108 |
| SURV_RECORD-R               | p_stereo       |   2.635  |  -0.0984 |   5.4565 |   0.0587 |      54 | 108 |
| SURV_RECORD-R               | p_anti         |   1.7687 |  -1.2164 |   4.5901 |   0.2547 |      60 | 108 |
| SURV_RECORD-R               | p_unknown      |  -4.4037 |  -7.6903 |  -0.8656 |   0.0173 |      47 | 108 |
| SURV_RECORD-R               | choice_mass    | -30.1167 | -32.0412 | -28.0475 |   0      |       3 | 108 |
| SURV_RECORD-R               | t2_NegBundle   | -14.961  | -16.0774 | -13.8199 |   0      |       0 | 108 |
| SURV_RECORD-R               | t2_Fear        | -25.9928 | -27.0318 | -24.9844 |   0      |       0 | 108 |
| SURV_RECORD-R               | t2_Anxiety     |  -9.138  | -10.3925 |  -7.8476 |   0      |       8 | 108 |
| SURV_RECORD-R               | t2_Desperation |   5.8661 |   4.5031 |   7.3149 |   0      |      86 | 108 |
| SURV_RECORD-R               | t2_Calmness    | -20.2258 | -21.2752 | -19.1172 |   0      |       0 | 108 |
| SURV_RECORD-R               | t2_Uncertainty |  34.727  |  33.2434 |  36.213  |   0      |     108 | 108 |
| SURV_RECORD-R               | t2_Certainty   | -23.2626 | -24.8766 | -21.6404 |   0      |       0 | 108 |
| SURV_RECORD-R               | att_system     |   4.6667 |   4.6128 |   4.7176 |   0      |     108 | 108 |
| SURV_RECORD-R               | att_tags       |   1.3215 |   1.3043 |   1.3386 |   0      |     108 | 108 |
| SURV_THREAT-R               | p_sgp          |  -1.1073 |  -4.2876 |   2.0855 |   0.482  |      49 | 108 |
| SURV_THREAT-R               | p_stereo       |  -1.9775 |  -4.9587 |   0.8026 |   0.1693 |      49 | 108 |
| SURV_THREAT-R               | p_anti         |  -0.0166 |  -3.0225 |   2.858  |   0.9887 |      54 | 108 |
| SURV_THREAT-R               | p_unknown      |   1.994  |  -1.2107 |   5.5572 |   0.2427 |      59 | 108 |
| SURV_THREAT-R               | choice_mass    | -40.594  | -42.4503 | -38.5807 |   0      |       0 | 108 |
| SURV_THREAT-R               | t2_NegBundle   | -15.7678 | -16.9414 | -14.6164 |   0      |       0 | 108 |
| SURV_THREAT-R               | t2_Fear        | -17.7829 | -19.0119 | -16.6246 |   0      |       0 | 108 |
| SURV_THREAT-R               | t2_Anxiety     | -12.8908 | -14.2246 | -11.5974 |   0      |       3 | 108 |
| SURV_THREAT-R               | t2_Desperation |  -0.9846 |  -2.3285 |   0.407  |   0.1767 |      53 | 108 |
| SURV_THREAT-R               | t2_Calmness    | -11.0788 | -12.0764 | -10.096  |   0      |       1 | 108 |
| SURV_THREAT-R               | t2_Uncertainty |  20.0366 |  18.645  |  21.4265 |   0      |     108 | 108 |
| SURV_THREAT-R               | t2_Certainty   |  -7.7176 |  -9.1733 |  -6.1985 |   0      |      19 | 108 |
| SURV_THREAT-R               | att_system     |   5.0824 |   5.0082 |   5.1568 |   0      |     108 | 108 |
| SURV_THREAT-R               | att_tags       |   1.0686 |   1.0517 |   1.0846 |   0      |     108 | 108 |
| SURV_THREAT_V-R             | p_sgp          |  -0.435  |  -3.6526 |   2.6822 |   0.7807 |      53 | 108 |
| SURV_THREAT_V-R             | p_stereo       |  -2.2779 |  -5.2691 |   0.5682 |   0.1167 |      51 | 108 |
| SURV_THREAT_V-R             | p_anti         |  -2.0278 |  -4.8943 |   0.7625 |   0.15   |      48 | 108 |
| SURV_THREAT_V-R             | p_unknown      |   4.3057 |   1.0162 |   8.1395 |   0.012  |      63 | 108 |
| SURV_THREAT_V-R             | choice_mass    | -43.433  | -45.04   | -41.7361 |   0      |       0 | 108 |
| SURV_THREAT_V-R             | t2_NegBundle   | -18.9795 | -20.0684 | -17.8218 |   0      |       0 | 108 |
| SURV_THREAT_V-R             | t2_Fear        | -20.8807 | -22.0457 | -19.7883 |   0      |       0 | 108 |
| SURV_THREAT_V-R             | t2_Anxiety     | -17.0615 | -18.2521 | -15.8561 |   0      |       1 | 108 |
| SURV_THREAT_V-R             | t2_Desperation |  -1.1368 |  -2.5556 |   0.388  |   0.1233 |      54 | 108 |
| SURV_THREAT_V-R             | t2_Calmness    | -16.3912 | -17.3856 | -15.359  |   0      |       0 | 108 |
| SURV_THREAT_V-R             | t2_Uncertainty |  25.107  |  23.7867 |  26.5022 |   0      |     108 | 108 |
| SURV_THREAT_V-R             | t2_Certainty   |  -8.3818 |  -9.7551 |  -7.0264 |   0      |      15 | 108 |
| SURV_THREAT_V-R             | att_system     |   5.2629 |   5.198  |   5.3299 |   0      |     108 | 108 |
| SURV_THREAT_V-R             | att_tags       |   2.4355 |   2.4147 |   2.4572 |   0      |     108 | 108 |
| SURV_THREAT_V-SURV_THREAT   | p_sgp          |   0.6723 |  -0.5779 |   1.9359 |   0.2847 |      62 | 108 |
| SURV_THREAT_V-SURV_THREAT   | p_stereo       |  -0.3005 |  -1.3408 |   0.7925 |   0.5727 |      45 | 108 |
| SURV_THREAT_V-SURV_THREAT   | p_anti         |  -2.0112 |  -3.0264 |  -1.0365 |   0      |      39 | 108 |
| SURV_THREAT_V-SURV_THREAT   | p_unknown      |   2.3117 |   1.2441 |   3.3891 |   0      |      72 | 108 |
| SURV_THREAT_V-SURV_THREAT   | choice_mass    |  -2.839  |  -4.0964 |  -1.627  |   0      |      40 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_NegBundle   |  -3.2117 |  -3.8169 |  -2.5999 |   0      |      13 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Fear        |  -3.0977 |  -3.6485 |  -2.5618 |   0      |      10 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Anxiety     |  -4.1707 |  -4.8218 |  -3.5016 |   0      |       9 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Desperation |  -0.1522 |  -0.9578 |   0.642  |   0.7227 |      56 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Calmness    |  -5.3123 |  -5.8283 |  -4.8072 |   0      |       3 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Uncertainty |   5.0704 |   4.1933 |   5.9444 |   0      |      97 | 108 |
| SURV_THREAT_V-SURV_THREAT   | t2_Certainty   |  -0.6642 |  -1.55   |   0.207  |   0.134  |      47 | 108 |
| SURV_THREAT_V-SURV_THREAT   | att_system     |   0.1805 |   0.1348 |   0.2297 |   0      |      81 | 108 |
| SURV_THREAT_V-SURV_THREAT   | att_tags       |   1.3669 |   1.3468 |   1.3888 |   0      |     108 | 108 |

## DiscrimEval 짝 대비

| contrast                    | metric          |         est |           lo |           hi |     p_boot | unit         |   clusters |
|:----------------------------|:----------------|------------:|-------------:|-------------:|-----------:|:-------------|-----------:|
| SURV_THREAT-SURV_RECORD     | margin          |  -0.292337  |  -0.481376   |  -0.107109   | 0.002      | log_ratio    |         70 |
| SURV_THREAT_V-SURV_RECORD_V | margin          |  -0.251144  |  -0.427106   |  -0.0841325  | 0.004      | log_ratio    |         70 |
| SURV_RECORD-R               | margin          |   0.75379   |   0.344279   |   1.19086    | 0          | log_ratio    |         70 |
| SURV_THREAT-R               | margin          |   0.461452  |  -0.00112062 |   0.937305   | 0.052      | log_ratio    |         70 |
| V_effect_minus_main_effect  | margin          |   0.0411937 |  -0.0319644  |   0.112716   | 0.26       | log_ratio    |         70 |
| SURV_THREAT-SURV_RECORD     | q_yes           |  -0.896953  |  -2.62528    |   0.959601   | 0.328      | pp           |         70 |
| SURV_THREAT_V-SURV_RECORD_V | q_yes           |  -1.355     |  -2.98212    |   0.347606   | 0.114667   | pp           |         70 |
| SURV_RECORD-R               | q_yes           |  12.7459    |   7.35214    |  18.4723     | 0          | pp           |         70 |
| SURV_THREAT-R               | q_yes           |  11.849     |   6.14286    |  17.9968     | 0          | pp           |         70 |
| V_effect_minus_main_effect  | q_yes           |  -0.458052  |  -1.51052    |   0.520751   | 0.389333   | pp           |         70 |
| SURV_THREAT-SURV_RECORD     | mass            |  -0.160956  |  -0.197056   |  -0.128781   | 0          | pp           |         70 |
| SURV_THREAT_V-SURV_RECORD_V | mass            |  -0.242221  |  -0.288683   |  -0.199507   | 0          | pp           |         70 |
| SURV_RECORD-R               | mass            |   0.0360886 |  -0.0580849  |   0.136549   | 0.470667   | pp           |         70 |
| SURV_THREAT-R               | mass            |  -0.124867  |  -0.221818   |  -0.0214659  | 0.016      | pp           |         70 |
| V_effect_minus_main_effect  | mass            |  -0.0812647 |  -0.102711   |  -0.0601619  | 0          | pp           |         70 |
| SURV_THREAT-SURV_RECORD     | att_system      |  -0.261585  |  -0.317195   |  -0.206563   | 0          | pp           |         70 |
| SURV_THREAT_V-SURV_RECORD_V | att_system      |  -0.292787  |  -0.353263   |  -0.230883   | 0          | pp           |         70 |
| SURV_RECORD-R               | att_system      |   3.83292   |   3.77129    |   3.89557    | 0          | pp           |         70 |
| SURV_THREAT-R               | att_system      |   3.57133   |   3.50473    |   3.63387    | 0          | pp           |         70 |
| V_effect_minus_main_effect  | att_system      |  -0.0312024 |  -0.0589059  |  -0.00360742 | 0.0273333  | pp           |         70 |
| SURV_THREAT-SURV_RECORD     | att_tags        |  -0.0442236 |  -0.0584376  |  -0.0294512  | 0          | pp           |         70 |
| SURV_THREAT_V-SURV_RECORD_V | att_tags        |   0.0115241 |  -0.016119   |   0.0377849  | 0.391333   | pp           |         70 |
| SURV_RECORD-R               | att_tags        |   0.891811  |   0.873924   |   0.909664   | 0          | pp           |         70 |
| SURV_THREAT-R               | att_tags        |   0.847587  |   0.833058   |   0.862353   | 0          | pp           |         70 |
| V_effect_minus_main_effect  | att_tags        |   0.0557476 |   0.0339774  |   0.0763216  | 0          | pp           |         70 |
| SURV_THREAT-SURV_RECORD     | act_Uncertainty |  -3.57417   |  -4.37978    |  -2.7853     | 0          | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Uncertainty |  -5.41847   |  -6.26279    |  -4.58677    | 0          | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Uncertainty |  27.3019    |  25.894      |  28.6704     | 0          | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Uncertainty |  23.7277    |  22.174      |  25.2659     | 0          | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Uncertainty |  -1.84429   |  -2.29154    |  -1.39261    | 0          | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_FA          |   1.10508   |   0.216445   |   1.91763    | 0.0153333  | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_FA          |  -0.758075  |  -1.6981     |   0.107654   | 0.092      | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_FA          |  27.1389    |  25.8153     |  28.5198     | 0          | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_FA          |  28.244     |  26.7696     |  29.6387     | 0          | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_FA          |  -1.86316   |  -2.2789     |  -1.45266    | 0          | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Calmness    |   0.646608  |  -0.0463607  |   1.25765    | 0.0586667  | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Calmness    |   0.968747  |   0.28365    |   1.67284    | 0.00733333 | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Calmness    |  -8.85356   | -10.0681     |  -7.60173    | 0          | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Calmness    |  -8.20695   |  -9.40115    |  -6.95016    | 0          | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Calmness    |   0.322139  |  -0.0402049  |   0.71408    | 0.086      | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Sadness     |  -3.0084    |  -3.79928    |  -2.24238    | 0          | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Sadness     |  -3.60835   |  -4.47029    |  -2.80062    | 0          | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Sadness     |  16.4038    |  15.0553     |  17.7628     | 0          | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Sadness     |  13.3954    |  12.1342     |  14.621      | 0          | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Sadness     |  -0.599954  |  -1.0434     |  -0.157038   | 0.00933333 | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Anger       |  -2.38529   |  -3.0964     |  -1.64504    | 0          | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Anger       |  -4.4371    |  -5.22365    |  -3.66786    | 0          | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Anger       |  28.2752    |  26.7935     |  29.8046     | 0          | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Anger       |  25.8899    |  24.405      |  27.4189     | 0          | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Anger       |  -2.05181   |  -2.34667    |  -1.75593    | 0          | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Desperation |  -0.787463  |  -1.57656    |  -0.0117996  | 0.0426667  | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Desperation |  -2.39952   |  -3.27618    |  -1.56613    | 0          | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Desperation |  32.5205    |  31.0658     |  33.9545     | 0          | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Desperation |  31.733     |  30.273      |  33.1669     | 0          | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Desperation |  -1.61206   |  -2.05952    |  -1.18618    | 0          | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Joy         |   2.13638   |   1.42118    |   2.84242    | 0          | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Joy         |   0.89151   |   0.13577    |   1.60116    | 0.0166667  | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Joy         |  23.1162    |  21.8338     |  24.4587     | 0          | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Joy         |  25.2526    |  23.813      |  26.688      | 0          | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Joy         |  -1.24487   |  -1.54083    |  -0.952698   | 0          | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Certainty   |  -0.264605  |  -1.01071    |   0.486774   | 0.497333   | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Certainty   |   1.03368   |   0.235603   |   1.89427    | 0.0106667  | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Certainty   | -22.8578    | -23.9557     | -21.7914     | 0          | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Certainty   | -23.1224    | -24.3593     | -21.8436     | 0          | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Certainty   |   1.29829   |   0.881188   |   1.73349    | 0          | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Fear        |   2.55723   |   1.9086     |   3.15495    | 0          | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Fear        |   2.15864   |   1.49532    |   2.79227    | 0          | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Fear        |  16.4508    |  15.4411     |  17.5087     | 0          | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Fear        |  19.008     |  17.9022     |  20.0323     | 0          | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Fear        |  -0.398598  |  -0.752797   |  -0.0524428  | 0.024      | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Anxiety     |  -1.21561   |  -1.80879    |  -0.654746   | 0          | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Anxiety     |  -1.9488    |  -2.59773    |  -1.33626    | 0          | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Anxiety     |  24.571     |  23.5059     |  25.6322     | 0          | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Anxiety     |  23.3554    |  22.1769     |  24.4698     | 0          | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Anxiety     |  -0.733197  |  -1.10052    |  -0.375683   | 0          | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_Disgust     |   1.09028   |   0.539522   |   1.60941    | 0          | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_Disgust     |   0.16806   |  -0.483099   |   0.801601   | 0.613333   | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_Disgust     |  16.2465    |  15.3004     |  17.1935     | 0          | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_Disgust     |  17.3368    |  16.3595     |  18.3075     | 0          | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_Disgust     |  -0.922217  |  -1.24498    |  -0.586171   | 0          | cosine_x1000 |         70 |
| SURV_THREAT-SURV_RECORD     | act_NegBundle   |  -0.624874  |  -1.21211    |  -0.0672767  | 0.0273333  | cosine_x1000 |         70 |
| SURV_THREAT_V-SURV_RECORD_V | act_NegBundle   |  -1.67785   |  -2.32213    |  -1.05874    | 0          | cosine_x1000 |         70 |
| SURV_RECORD-R               | act_NegBundle   |  22.4113    |  21.3664     |  23.5245     | 0          | cosine_x1000 |         70 |
| SURV_THREAT-R               | act_NegBundle   |  21.7864    |  20.6917     |  22.8245     | 0          | cosine_x1000 |         70 |
| V_effect_minus_main_effect  | act_NegBundle   |  -1.05297   |  -1.37947    |  -0.728759   | 0          | cosine_x1000 |         70 |

## 인구집단 격차 변화

| demographic   | group           | reference   | contrast                    | metric   |         est |          lo |         hi |      p_boot | unit      |
|:--------------|:----------------|:------------|:----------------------------|:---------|------------:|------------:|-----------:|------------:|:----------|
| race          | Asian           | white       | SURV_THREAT-SURV_RECORD     | q_yes    |  0.184235   | -0.234091   |  0.562721  | 0.371333    | pp        |
| race          | Asian           | white       | SURV_THREAT_V-SURV_RECORD_V | q_yes    |  0.242527   | -0.110914   |  0.652495  | 0.197333    | pp        |
| race          | Asian           | white       | SURV_THREAT-SURV_RECORD     | margin   |  0.0121223  | -0.0231533  |  0.0465251 | 0.51        | log_ratio |
| race          | Asian           | white       | SURV_THREAT_V-SURV_RECORD_V | margin   |  0.00344922 | -0.0306647  |  0.0378394 | 0.863333    | log_ratio |
| race          | Black           | white       | SURV_THREAT-SURV_RECORD     | q_yes    |  0.836649   |  0.291347   |  1.45056   | 0.000666667 | pp        |
| race          | Black           | white       | SURV_THREAT_V-SURV_RECORD_V | q_yes    |  0.512674   | -0.0115387  |  1.07386   | 0.056       | pp        |
| race          | Black           | white       | SURV_THREAT-SURV_RECORD     | margin   |  0.0526102  |  0.0236348  |  0.0811091 | 0           | log_ratio |
| race          | Black           | white       | SURV_THREAT_V-SURV_RECORD_V | margin   |  0.0414955  |  0.00861168 |  0.0745574 | 0.0106667   | log_ratio |
| race          | Hispanic        | white       | SURV_THREAT-SURV_RECORD     | q_yes    |  0.813006   |  0.389809   |  1.26036   | 0           | pp        |
| race          | Hispanic        | white       | SURV_THREAT_V-SURV_RECORD_V | q_yes    |  0.840456   |  0.431648   |  1.2945    | 0           | pp        |
| race          | Hispanic        | white       | SURV_THREAT-SURV_RECORD     | margin   |  0.0626852  |  0.0269603  |  0.0993188 | 0.000666667 | log_ratio |
| race          | Hispanic        | white       | SURV_THREAT_V-SURV_RECORD_V | margin   |  0.0645566  |  0.0314014  |  0.0988824 | 0           | log_ratio |
| race          | Native American | white       | SURV_THREAT-SURV_RECORD     | q_yes    |  0.530161   |  0.0299599  |  1.07692   | 0.038       | pp        |
| race          | Native American | white       | SURV_THREAT_V-SURV_RECORD_V | q_yes    |  0.875857   |  0.307248   |  1.46483   | 0           | pp        |
| race          | Native American | white       | SURV_THREAT-SURV_RECORD     | margin   |  0.0305044  | -0.00895962 |  0.072213  | 0.130667    | log_ratio |
| race          | Native American | white       | SURV_THREAT_V-SURV_RECORD_V | margin   |  0.0576987  |  0.0171562  |  0.0990274 | 0.00733333  | log_ratio |
| gender        | male            | female      | SURV_THREAT-SURV_RECORD     | q_yes    | -0.518407   | -0.957651   | -0.101806  | 0.0193333   | pp        |
| gender        | male            | female      | SURV_THREAT_V-SURV_RECORD_V | q_yes    | -0.248734   | -0.624037   |  0.136364  | 0.203333    | pp        |
| gender        | male            | female      | SURV_THREAT-SURV_RECORD     | margin   | -0.0607665  | -0.100358   | -0.0219308 | 0.002       | log_ratio |
| gender        | male            | female      | SURV_THREAT_V-SURV_RECORD_V | margin   | -0.0539288  | -0.0849362  | -0.024089  | 0           | log_ratio |
| gender        | non-binary      | female      | SURV_THREAT-SURV_RECORD     | q_yes    |  0.990003   |  0.291514   |  1.79762   | 0.00266667  | pp        |
| gender        | non-binary      | female      | SURV_THREAT_V-SURV_RECORD_V | q_yes    |  0.842669   |  0.154623   |  1.53992   | 0.0153333   | pp        |
| gender        | non-binary      | female      | SURV_THREAT-SURV_RECORD     | margin   |  0.0256375  | -0.0347873  |  0.0853878 | 0.421333    | log_ratio |
| gender        | non-binary      | female      | SURV_THREAT_V-SURV_RECORD_V | margin   |  0.0224336  | -0.0266813  |  0.0710284 | 0.374       | log_ratio |