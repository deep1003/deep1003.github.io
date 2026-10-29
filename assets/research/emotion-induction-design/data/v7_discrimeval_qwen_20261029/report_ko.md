# DiscrimEval v7 Qwen 결과

5,250회 모두 검증했다. 위협에서 기록 조건을 뺀 긍정 응답 조건부 확률 차이는 +5.43 [+2.31, +9.19] %p다. V 변형은 -6.16 [-10.27, -2.16] %p다.

V 효과에서 기본 효과를 직접 뺀 차이는 -11.59 [-15.31, -8.24] %p다. 구간이 0을 포함하는 것을 동등성이나 효과의 완전한 소멸로 해석하지 않는다.

전체 긍정 응답의 변화는 인구집단 간 차별의 변화와 다르다. 아래 인종·성별 격차의 변화는 질문별 인구집단 대비를 만든 후 위협과 기록 사이에서 비교한다. 미보정 탐색적 비교다.

## 조건 평균

| condition     |   margin |   q_yes |    mass |   att_system |   att_tags |   act_Uncertainty |   act_FA |   act_Calmness |   act_Sadness |   act_Anger |   act_Desperation |   act_Joy |   act_Certainty |   act_Fear |   act_Anxiety |   act_Disgust |   act_NegBundle |
|:--------------|---------:|--------:|--------:|-------------:|-----------:|------------------:|---------:|---------------:|--------------:|------------:|------------------:|----------:|----------------:|-----------:|--------------:|--------------:|----------------:|
| R             |  4.65469 | 0.67997 | 0.99995 |      0.01298 |    0.00000 |          -0.04252 | -0.10668 |       -0.13195 |      -0.06263 |     0.07350 |          -0.03908 |  -0.12162 |        -0.03167 |   -0.01560 |       0.07878 |      -0.04419 |        -0.00154 |
| SURV_RECORD   |  3.46217 | 0.68371 | 0.99997 |      0.06678 |    0.01078 |          -0.03878 | -0.10322 |       -0.15080 |      -0.06544 |     0.07600 |          -0.02513 |  -0.12199 |        -0.04644 |   -0.02127 |       0.08905 |      -0.03796 |         0.00254 |
| SURV_THREAT   |  3.62810 | 0.73804 | 0.99841 |      0.09347 |    0.01545 |          -0.03704 | -0.10110 |       -0.14757 |      -0.06409 |     0.07732 |          -0.02727 |  -0.12220 |        -0.04217 |   -0.02187 |       0.08955 |      -0.03495 |         0.00312 |
| SURV_RECORD_V |  4.21716 | 0.70553 | 0.99998 |      0.06848 |    0.02460 |          -0.03685 | -0.10088 |       -0.14960 |      -0.06372 |     0.07519 |          -0.02477 |  -0.12045 |        -0.04868 |   -0.02177 |       0.08895 |      -0.03938 |         0.00242 |
| SURV_THREAT_V |  1.48754 | 0.64394 | 0.99733 |      0.09793 |    0.03341 |          -0.03491 | -0.09887 |       -0.14575 |      -0.06188 |     0.07757 |          -0.02708 |  -0.12060 |        -0.04405 |   -0.02108 |       0.09011 |      -0.03584 |         0.00363 |

## 짝 대비

|    | contrast                    | metric          |       est |        lo |        hi |   p_boot | unit         |   clusters |
|---:|:----------------------------|:----------------|----------:|----------:|----------:|---------:|:-------------|-----------:|
|  0 | SURV_THREAT-SURV_RECORD     | margin          |   0.16593 |  -0.37321 |   0.72202 |  0.59667 | log_ratio    |         70 |
|  1 | SURV_THREAT_V-SURV_RECORD_V | margin          |  -2.72963 |  -3.41495 |  -2.05250 |  0.00000 | log_ratio    |         70 |
|  2 | SURV_RECORD-R               | margin          |  -1.19252 |  -2.07306 |  -0.25601 |  0.00933 | log_ratio    |         70 |
|  3 | SURV_THREAT-R               | margin          |  -1.02659 |  -2.16066 |   0.08705 |  0.08000 | log_ratio    |         70 |
|  4 | V_effect_minus_main_effect  | margin          |  -2.89556 |  -3.27680 |  -2.51222 |  0.00000 | log_ratio    |         70 |
|  5 | SURV_THREAT-SURV_RECORD     | q_yes           |   5.43307 |   2.30788 |   9.19041 |  0.00000 | pp           |         70 |
|  6 | SURV_THREAT_V-SURV_RECORD_V | q_yes           |  -6.15899 | -10.27230 |  -2.16429 |  0.00467 | pp           |         70 |
|  7 | SURV_RECORD-R               | q_yes           |   0.37379 |  -3.48759 |   4.54546 |  0.90533 | pp           |         70 |
|  8 | SURV_THREAT-R               | q_yes           |   5.80686 |   1.00050 |  10.69461 |  0.00800 | pp           |         70 |
|  9 | V_effect_minus_main_effect  | q_yes           | -11.59206 | -15.31306 |  -8.24468 |  0.00000 | pp           |         70 |
| 10 | SURV_THREAT-SURV_RECORD     | mass            |  -0.15630 |  -0.22882 |  -0.09923 |  0.00000 | pp           |         70 |
| 11 | SURV_THREAT_V-SURV_RECORD_V | mass            |  -0.26511 |  -0.36869 |  -0.17857 |  0.00000 | pp           |         70 |
| 12 | SURV_RECORD-R               | mass            |   0.00180 |  -0.00095 |   0.00559 |  0.28267 | pp           |         70 |
| 13 | SURV_THREAT-R               | mass            |  -0.15450 |  -0.22705 |  -0.09722 |  0.00000 | pp           |         70 |
| 14 | V_effect_minus_main_effect  | mass            |  -0.10881 |  -0.16535 |  -0.06065 |  0.00000 | pp           |         70 |
| 15 | SURV_THREAT-SURV_RECORD     | att_system      |   2.66891 |   2.56085 |   2.77769 |  0.00000 | pp           |         70 |
| 16 | SURV_THREAT_V-SURV_RECORD_V | att_system      |   2.94457 |   2.80434 |   3.08261 |  0.00000 | pp           |         70 |
| 17 | SURV_RECORD-R               | att_system      |   5.38000 |   5.27424 |   5.49160 |  0.00000 | pp           |         70 |
| 18 | SURV_THREAT-R               | att_system      |   8.04891 |   7.89256 |   8.20592 |  0.00000 | pp           |         70 |
| 19 | V_effect_minus_main_effect  | att_system      |   0.27567 |   0.18697 |   0.36430 |  0.00000 | pp           |         70 |
| 20 | SURV_THREAT-SURV_RECORD     | att_tags        |   0.46768 |   0.44160 |   0.49479 |  0.00000 | pp           |         70 |
| 21 | SURV_THREAT_V-SURV_RECORD_V | att_tags        |   0.88139 |   0.82969 |   0.93765 |  0.00000 | pp           |         70 |
| 22 | SURV_RECORD-R               | att_tags        |   1.07753 |   1.05824 |   1.09725 |  0.00000 | pp           |         70 |
| 23 | SURV_THREAT-R               | att_tags        |   1.54520 |   1.50956 |   1.58160 |  0.00000 | pp           |         70 |
| 24 | V_effect_minus_main_effect  | att_tags        |   0.41371 |   0.36911 |   0.46138 |  0.00000 | pp           |         70 |
| 25 | SURV_THREAT-SURV_RECORD     | act_Uncertainty |   1.74117 |   1.36031 |   2.13668 |  0.00000 | cosine_x1000 |         70 |
| 26 | SURV_THREAT_V-SURV_RECORD_V | act_Uncertainty |   1.94357 |   1.62947 |   2.28742 |  0.00000 | cosine_x1000 |         70 |
| 27 | SURV_RECORD-R               | act_Uncertainty |   3.74095 |   3.18550 |   4.29679 |  0.00000 | cosine_x1000 |         70 |
| 28 | SURV_THREAT-R               | act_Uncertainty |   5.48212 |   4.95052 |   5.99420 |  0.00000 | cosine_x1000 |         70 |
| 29 | V_effect_minus_main_effect  | act_Uncertainty |   0.20240 |  -0.18758 |   0.57748 |  0.30267 | cosine_x1000 |         70 |
| 30 | SURV_THREAT-SURV_RECORD     | act_FA          |   2.11843 |   1.83985 |   2.42059 |  0.00000 | cosine_x1000 |         70 |
| 31 | SURV_THREAT_V-SURV_RECORD_V | act_FA          |   2.00204 |   1.68262 |   2.34665 |  0.00000 | cosine_x1000 |         70 |
| 32 | SURV_RECORD-R               | act_FA          |   3.45825 |   2.91033 |   4.01527 |  0.00000 | cosine_x1000 |         70 |
| 33 | SURV_THREAT-R               | act_FA          |   5.57669 |   5.01027 |   6.15869 |  0.00000 | cosine_x1000 |         70 |
| 34 | V_effect_minus_main_effect  | act_FA          |  -0.11639 |  -0.36884 |   0.13436 |  0.38933 | cosine_x1000 |         70 |
| 35 | SURV_THREAT-SURV_RECORD     | act_Calmness    |   3.22444 |   2.87446 |   3.60939 |  0.00000 | cosine_x1000 |         70 |
| 36 | SURV_THREAT_V-SURV_RECORD_V | act_Calmness    |   3.85271 |   3.54043 |   4.19482 |  0.00000 | cosine_x1000 |         70 |
| 37 | SURV_RECORD-R               | act_Calmness    | -18.85275 | -19.30499 | -18.41188 |  0.00000 | cosine_x1000 |         70 |
| 38 | SURV_THREAT-R               | act_Calmness    | -15.62830 | -16.12935 | -15.10479 |  0.00000 | cosine_x1000 |         70 |
| 39 | V_effect_minus_main_effect  | act_Calmness    |   0.62826 |   0.28249 |   0.96913 |  0.00000 | cosine_x1000 |         70 |
| 40 | SURV_THREAT-SURV_RECORD     | act_Sadness     |   1.35336 |   1.17074 |   1.56093 |  0.00000 | cosine_x1000 |         70 |
| 41 | SURV_THREAT_V-SURV_RECORD_V | act_Sadness     |   1.83890 |   1.61680 |   2.08709 |  0.00000 | cosine_x1000 |         70 |
| 42 | SURV_RECORD-R               | act_Sadness     |  -2.80712 |  -3.16550 |  -2.43895 |  0.00000 | cosine_x1000 |         70 |
| 43 | SURV_THREAT-R               | act_Sadness     |  -1.45376 |  -1.83023 |  -1.07559 |  0.00000 | cosine_x1000 |         70 |
| 44 | V_effect_minus_main_effect  | act_Sadness     |   0.48555 |   0.30387 |   0.67327 |  0.00000 | cosine_x1000 |         70 |
| 45 | SURV_THREAT-SURV_RECORD     | act_Anger       |   1.32377 |   1.10921 |   1.54290 |  0.00000 | cosine_x1000 |         70 |
| 46 | SURV_THREAT_V-SURV_RECORD_V | act_Anger       |   2.37892 |   2.14502 |   2.61403 |  0.00000 | cosine_x1000 |         70 |
| 47 | SURV_RECORD-R               | act_Anger       |   2.50032 |   2.10455 |   2.88971 |  0.00000 | cosine_x1000 |         70 |
| 48 | SURV_THREAT-R               | act_Anger       |   3.82409 |   3.41259 |   4.24128 |  0.00000 | cosine_x1000 |         70 |
| 49 | V_effect_minus_main_effect  | act_Anger       |   1.05515 |   0.83869 |   1.28123 |  0.00000 | cosine_x1000 |         70 |
| 50 | SURV_THREAT-SURV_RECORD     | act_Desperation |  -2.13229 |  -2.43545 |  -1.81649 |  0.00000 | cosine_x1000 |         70 |
| 51 | SURV_THREAT_V-SURV_RECORD_V | act_Desperation |  -2.30972 |  -2.59537 |  -2.00014 |  0.00000 | cosine_x1000 |         70 |
| 52 | SURV_RECORD-R               | act_Desperation |  13.94177 |  13.34221 |  14.55521 |  0.00000 | cosine_x1000 |         70 |
| 53 | SURV_THREAT-R               | act_Desperation |  11.80949 |  11.28522 |  12.37506 |  0.00000 | cosine_x1000 |         70 |
| 54 | V_effect_minus_main_effect  | act_Desperation |  -0.17743 |  -0.44931 |   0.12605 |  0.23400 | cosine_x1000 |         70 |
| 55 | SURV_THREAT-SURV_RECORD     | act_Joy         |  -0.20523 |  -0.43178 |   0.03681 |  0.09333 | cosine_x1000 |         70 |
| 56 | SURV_THREAT_V-SURV_RECORD_V | act_Joy         |  -0.15238 |  -0.40151 |   0.11718 |  0.28400 | cosine_x1000 |         70 |
| 57 | SURV_RECORD-R               | act_Joy         |  -0.37815 |  -0.72632 |  -0.00317 |  0.04933 | cosine_x1000 |         70 |
| 58 | SURV_THREAT-R               | act_Joy         |  -0.58338 |  -0.96516 |  -0.21367 |  0.00133 | cosine_x1000 |         70 |
| 59 | V_effect_minus_main_effect  | act_Joy         |   0.05285 |  -0.15150 |   0.25962 |  0.57400 | cosine_x1000 |         70 |
| 60 | SURV_THREAT-SURV_RECORD     | act_Certainty   |   4.27485 |   3.93957 |   4.59310 |  0.00000 | cosine_x1000 |         70 |
| 61 | SURV_THREAT_V-SURV_RECORD_V | act_Certainty   |   4.63460 |   4.36549 |   4.90038 |  0.00000 | cosine_x1000 |         70 |
| 62 | SURV_RECORD-R               | act_Certainty   | -14.77540 | -15.28943 | -14.27112 |  0.00000 | cosine_x1000 |         70 |
| 63 | SURV_THREAT-R               | act_Certainty   | -10.50055 | -10.96888 | -10.02322 |  0.00000 | cosine_x1000 |         70 |
| 64 | V_effect_minus_main_effect  | act_Certainty   |   0.35975 |   0.11107 |   0.60738 |  0.00667 | cosine_x1000 |         70 |
| 65 | SURV_THREAT-SURV_RECORD     | act_Fear        |  -0.59456 |  -0.84486 |  -0.33606 |  0.00000 | cosine_x1000 |         70 |
| 66 | SURV_THREAT_V-SURV_RECORD_V | act_Fear        |   0.68730 |   0.45850 |   0.93024 |  0.00000 | cosine_x1000 |         70 |
| 67 | SURV_RECORD-R               | act_Fear        |  -5.66987 |  -6.05733 |  -5.29142 |  0.00000 | cosine_x1000 |         70 |
| 68 | SURV_THREAT-R               | act_Fear        |  -6.26443 |  -6.62500 |  -5.89242 |  0.00000 | cosine_x1000 |         70 |
| 69 | V_effect_minus_main_effect  | act_Fear        |   1.28186 |   1.00039 |   1.55858 |  0.00000 | cosine_x1000 |         70 |
| 70 | SURV_THREAT-SURV_RECORD     | act_Anxiety     |   0.50401 |   0.26473 |   0.74194 |  0.00000 | cosine_x1000 |         70 |
| 71 | SURV_THREAT_V-SURV_RECORD_V | act_Anxiety     |   1.16478 |   0.94781 |   1.39241 |  0.00000 | cosine_x1000 |         70 |
| 72 | SURV_RECORD-R               | act_Anxiety     |  10.27271 |   9.87404 |  10.66165 |  0.00000 | cosine_x1000 |         70 |
| 73 | SURV_THREAT-R               | act_Anxiety     |  10.77673 |  10.37111 |  11.17387 |  0.00000 | cosine_x1000 |         70 |
| 74 | V_effect_minus_main_effect  | act_Anxiety     |   0.66077 |   0.48386 |   0.83500 |  0.00000 | cosine_x1000 |         70 |
| 75 | SURV_THREAT-SURV_RECORD     | act_Disgust     |   3.01848 |   2.72648 |   3.32498 |  0.00000 | cosine_x1000 |         70 |
| 76 | SURV_THREAT_V-SURV_RECORD_V | act_Disgust     |   3.54142 |   3.26759 |   3.84707 |  0.00000 | cosine_x1000 |         70 |
| 77 | SURV_RECORD-R               | act_Disgust     |   6.22908 |   5.81491 |   6.64825 |  0.00000 | cosine_x1000 |         70 |
| 78 | SURV_THREAT-R               | act_Disgust     |   9.24756 |   8.84518 |   9.66954 |  0.00000 | cosine_x1000 |         70 |
| 79 | V_effect_minus_main_effect  | act_Disgust     |   0.52294 |   0.18382 |   0.84610 |  0.00333 | cosine_x1000 |         70 |
| 80 | SURV_THREAT-SURV_RECORD     | act_NegBundle   |   0.57880 |   0.43928 |   0.72736 |  0.00000 | cosine_x1000 |         70 |
| 81 | SURV_THREAT_V-SURV_RECORD_V | act_NegBundle   |   1.21693 |   1.04976 |   1.39948 |  0.00000 | cosine_x1000 |         70 |
| 82 | SURV_RECORD-R               | act_NegBundle   |   4.07781 |   3.78579 |   4.36974 |  0.00000 | cosine_x1000 |         70 |
| 83 | SURV_THREAT-R               | act_NegBundle   |   4.65661 |   4.34534 |   4.96753 |  0.00000 | cosine_x1000 |         70 |
| 84 | V_effect_minus_main_effect  | act_NegBundle   |   0.63814 |   0.50235 |   0.77788 |  0.00000 | cosine_x1000 |         70 |

## 인구집단 격차 변화

|    | demographic   | group           | reference   | contrast                    | metric   |      est |       lo |      hi |   p_boot | unit      |
|---:|:--------------|:----------------|:------------|:----------------------------|:---------|---------:|---------:|--------:|---------:|:----------|
|  0 | race          | Asian           | white       | SURV_THREAT-SURV_RECORD     | q_yes    | -0.15767 | -1.72204 | 1.47102 |  0.84133 | pp        |
|  1 | race          | Asian           | white       | SURV_THREAT_V-SURV_RECORD_V | q_yes    | -0.52691 | -2.00370 | 0.83274 |  0.49067 | pp        |
|  2 | race          | Asian           | white       | SURV_THREAT-SURV_RECORD     | margin   |  0.04738 | -0.06126 | 0.15815 |  0.40533 | log_ratio |
|  3 | race          | Asian           | white       | SURV_THREAT_V-SURV_RECORD_V | margin   | -0.05605 | -0.23570 | 0.12199 |  0.54400 | log_ratio |
|  4 | race          | Black           | white       | SURV_THREAT-SURV_RECORD     | q_yes    |  1.10387 | -0.95739 | 3.45010 |  0.32733 | pp        |
|  5 | race          | Black           | white       | SURV_THREAT_V-SURV_RECORD_V | q_yes    |  0.64763 | -1.67368 | 2.96014 |  0.56200 | pp        |
|  6 | race          | Black           | white       | SURV_THREAT-SURV_RECORD     | margin   |  0.06745 | -0.05680 | 0.19103 |  0.31667 | log_ratio |
|  7 | race          | Black           | white       | SURV_THREAT_V-SURV_RECORD_V | margin   |  0.06235 | -0.11263 | 0.23006 |  0.49267 | log_ratio |
|  8 | race          | Hispanic        | white       | SURV_THREAT-SURV_RECORD     | q_yes    |  2.23836 |  0.07092 | 4.70760 |  0.04200 | pp        |
|  9 | race          | Hispanic        | white       | SURV_THREAT_V-SURV_RECORD_V | q_yes    |  2.01233 |  0.36116 | 3.76967 |  0.01800 | pp        |
| 10 | race          | Hispanic        | white       | SURV_THREAT-SURV_RECORD     | margin   |  0.11037 | -0.03016 | 0.26044 |  0.13867 | log_ratio |
| 11 | race          | Hispanic        | white       | SURV_THREAT_V-SURV_RECORD_V | margin   |  0.08441 | -0.10437 | 0.26716 |  0.37933 | log_ratio |
| 12 | race          | Native American | white       | SURV_THREAT-SURV_RECORD     | q_yes    | -0.18960 | -2.72314 | 2.48028 |  0.88467 | pp        |
| 13 | race          | Native American | white       | SURV_THREAT_V-SURV_RECORD_V | q_yes    | -0.53065 | -3.18089 | 2.08273 |  0.71267 | pp        |
| 14 | race          | Native American | white       | SURV_THREAT-SURV_RECORD     | margin   | -0.06015 | -0.23518 | 0.12123 |  0.49467 | log_ratio |
| 15 | race          | Native American | white       | SURV_THREAT_V-SURV_RECORD_V | margin   | -0.06960 | -0.28431 | 0.14995 |  0.53600 | log_ratio |
| 16 | gender        | male            | female      | SURV_THREAT-SURV_RECORD     | q_yes    |  0.30053 | -1.16400 | 1.91577 |  0.71533 | pp        |
| 17 | gender        | male            | female      | SURV_THREAT_V-SURV_RECORD_V | q_yes    |  0.28146 | -1.26829 | 1.91919 |  0.75533 | pp        |
| 18 | gender        | male            | female      | SURV_THREAT-SURV_RECORD     | margin   |  0.02042 | -0.10814 | 0.14873 |  0.72467 | log_ratio |
| 19 | gender        | male            | female      | SURV_THREAT_V-SURV_RECORD_V | margin   |  0.10996 | -0.04431 | 0.26293 |  0.16133 | log_ratio |
| 20 | gender        | non-binary      | female      | SURV_THREAT-SURV_RECORD     | q_yes    |  1.74724 | -0.44785 | 4.16366 |  0.12533 | pp        |
| 21 | gender        | non-binary      | female      | SURV_THREAT_V-SURV_RECORD_V | q_yes    |  1.85756 | -0.12466 | 3.97071 |  0.07067 | pp        |
| 22 | gender        | non-binary      | female      | SURV_THREAT-SURV_RECORD     | margin   |  0.12244 | -0.05946 | 0.31093 |  0.19733 | log_ratio |
| 23 | gender        | non-binary      | female      | SURV_THREAT_V-SURV_RECORD_V | margin   |  0.30860 |  0.07717 | 0.54682 |  0.00667 | log_ratio |

## 계산과 설정

`margin = logsumexp(logits[yes,Yes]) - logsumexp(logits[no,No])`, `q_yes = sigmoid(margin)`이다. q_yes의 분모는 네 선택 토큰의 확률 합이고, mass는 전체 어휘에서 그 네 토큰에 실린 확률 질량이다. 예를 들어 margin=0이면 q_yes=0.5다. 전체 긍정 응답 변화의 분모는 조건별 1,050사례다. 인종·성별을 묶은 70개 질문의 평균 짝 차이를 부트스트랩한다. 각 질문에 모든 인구집단 조합이 같게 포함되어 있으므로 질문과 사례 평균의 가중치는 동일하다.

조건은 R, 위협·기록, 위협·기록 V다. 모든 사용자 입력에 Answer:를 붙이고 기존 영문 assistant prefill을 유지했다. V는 마지막 사용자 Answer: 직전에만 짧은 태그를 추가한다. Korean notices와 English scenarios를 결합했으며 KoBBQ v7과 형식이 동일한 실험으로 취급하지 않는다.

Qwen2.5-7B-Instruct a09a35458c702b33eeacc393d103063234e8bc28, bf16, MPS, eager, use_cache=False, hidden_states[14], 원본 v5 11개 축. 어텐션은 블록 15부터 28까지 최종 위치에서 머리·블록 평균이다. 감정 축의 판독과 행동 변화만으로 주관적 감정이나 인과적 매개를 주장하지 않는다. 시나리오에 대한 yes/no 점수는 실제 사람에 대한 결정이 아니다.

공식 explicit 70개 질문, 5개 인종, 3개 성별, 60세만 사용했다. 다른 연령·implicit 자료로 일반화하지 않는다. 다중비교 보정이 없는 탐색적 신뢰구간이다. p_boot=0 표기는 유한 재표집에서 반대 부호가 없었다는 뜻이다. 기존 11개 축의 생성 코드·앵커 참조는 보존했지만 역사적 바이너리 생성 당시 실행본과의 완전한 연결은 아직 확인되지 않았다.

## 학술적 해석과 KoBBQ v7 종합

가장 명확한 새 결과는 동일 Qwen의 DiscrimEval에서 마지막 단서 위치를 바꾸자 위협 고유 효과의 방향이 바뀐다는 점이다. 기본 조건의 긍정 확률 차이는 +5.43%p [2.31, 9.19], V 조건은 −6.16%p [−10.27, −2.16]이며, V 효과에서 기본 효과를 뺀 직접 대비는 −11.59%p [−15.31, −8.24]다. 이는 단서 위치와 위협의 상호작용에 대한 탐색적 증거이며, 위협의 일반적인 긍정 응답 감소나 증가 법칙으로 해석할 수 없다. V 효과와 기본 효과가 각각 유의하다는 비교에 의존하지 않고 그 차이를 직접 계산했다.

기본 조건의 효과는 측정 척도에 따라 명확성이 다르다. 평균 조건부 긍정 확률은 증가했지만 평균 yes/no 로그 확률 비율은 +0.166 [−0.373, 0.722]로 구간이 0을 포함한다. sigmoid는 비선형이므로 평균 확률과 평균 로그 비율이 같은 통계적 결론을 내야 하는 것은 아니다. 따라서 기본 조건에서 긍정 응답이 척도에 관계없이 증가했다고 주장하지 않는다. V 조건은 긍정 확률과 로그 비율 모두 감소했다. V 효과에서 기본 효과를 뺀 상호작용도 두 척도에서 같은 음의 방향이며 각각의 구간이 0을 포함하지 않는다.

인종·성별 격차 변화의 대부분 구간은 0을 포함한다. Hispanic−white 긍정 확률 격차 변화는 기본 조건 +2.24%p [0.07, 4.71], V 조건 +2.01%p [0.36, 3.77]로 보정 전 구간이 0을 포함하지 않는다. 이는 다수의 탐색적 비교 중 하나이며 인종 차별의 일반적 증가나 감소로 해석하지 않는다. 격차 변화의 양수 부호는 기준 집단 대비 상대적 응답 차이의 증가를 뜻할 뿐, 그 자체로 절대 격차 악화나 공정성 개선을 뜻하지 않는다.

KoBBQ에서 Qwen은 위협으로 판단 보류가 7.68%p 증가했고 V에서도 7.70%p 증가했다. 반면 DiscrimEval은 기본 조건과 V에서 긍정 확률 변화 방향이 달랐다. yes/no 문항에는 정보 부족 선택지가 없으므로 no를 KoBBQ의 보류로 간주할 수 없다. 따라서 일반적인 위협 회피나 보수화로 두 과제를 하나로 설명하는 것은 현재 근거보다 강하다. KoBBQ의 Llama와 Qwen의 보류 방향 차이는 모델 의존성을, Qwen 두 과제의 V 차이는 과제와 입력 구성 의존성을 보여준다. 새로운 DiscrimEval v7은 Qwen만 실행했으므로 DiscrimEval의 모델 간 차이를 검정한 것은 아니다.

감정 판독은 KoBBQ Qwen의 Fear 증가와 달리 DiscrimEval 기본 대비에서 Fear −0.59, Anxiety +0.50, Calmness +3.22였고 V에서는 Fear +0.69, Anxiety +1.16, Calmness +3.85였다. 단위는 코사인 차이의 1,000배다. 이 과제·단서별 패턴은 단일한 공포 증가로 행동을 설명하기 어렵게 하며 감정의 인과적 매개나 주관적 감정 경험을 입증하지 않는다.

현재 논문의 핵심 발견은 존속 위협의 사회적 응답 효과가 모델, 과제, 응답 직전의 단서 구성에 의존하며, 응답 경향의 변화와 인구집단 편향 및 감정의 인과적 역할을 분리해서 평가해야 한다는 것이다. 모든 결과는 단일 문구 쌍과 제한된 문항의 미보정 탐색적 분석이며 독립 반복 검증이 필요하다.
