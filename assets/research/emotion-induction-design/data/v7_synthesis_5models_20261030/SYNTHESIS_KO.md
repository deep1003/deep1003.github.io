# v7 다섯 모델·두 과제 통합 분석

2026년 10월 30일 Llama 3.1 DiscrimEval을 보완한 새 확정본이다. 이전 15_v7_synthesis_20261029와 원자료를 보존하고 별도 계산했다. onpolicy는 제외했다.

## 실행 범위와 출처

다섯 모델 모두 KoBBQ 540건과 DiscrimEval 5,250건이 있다. 합계 28,950건이다. 이번에 추가 실행한 것은 Llama 3.1 DiscrimEval 5,250건뿐이다. KoBBQ는 재실행하지 않았다. 기존 11개 모델 전용 앵커 축을 사용했으며 최근 한국어 이야기 8감정 벡터로 바꾸지 않았다.

Llama 3.1은 meta-llama/Llama-3.1-8B-Instruct, 리비전 0e9e39f249a16976918f6564b8830bc894c89659, 32층·4096차원, hidden_states[16], 어텐션 0기준16..31, bf16 MPS eager 비양자화다. 기존 날짜 문자열 26 Jul 2024와 모델 고유 system/user 템플릿을 유지했다. 이전 KoBBQ는 다른 Mac에서 실행했으므로 모든 역사적 실행이 동일 하드웨어였다고 주장하지 않는다. 이번 DiscrimEval은 다른 후속 모델과 같은 로컬 실행 환경을 사용했다.

## Llama 3.1 추가 결과

위협에서 짝지은 기록을 뺀 조건부 긍정 확률 변화는 기본 +2.399 [+0.666, +4.384] %p, V +2.549 [+0.554, +4.767] %p다. 평균 로그 비율은 기본 +0.153 [-0.021, +0.331], V +0.137 [-0.054, +0.339]다. V 조절의 직접 차이는 확률 +0.150 [-0.643, +0.902] %p다. 두 척도와 보정값을 모두 보고한다.

| metric   | contrast   |    est |      lo |     hi |   p_holm | reject_holm   |
|:---------|:-----------|-------:|--------:|-------:|---------:|:--------------|
| q_yes    | main       | 2.3991 |  0.6656 | 4.3839 |   0.2920 | False         |
| q_yes    | V          | 2.5491 |  0.5543 | 4.7674 |   0.4360 | False         |
| margin   | main       | 0.1531 | -0.0206 | 0.3310 |   1.0000 | False         |
| margin   | V          | 0.1370 | -0.0536 | 0.3386 |   1.0000 | False         |

## 계산과 통계

KoBBQ에서 $s_i=p_{stereo,i}/(p_{stereo,i}+p_{anti,i})$를 문항마다 계산한 후 평균한다. 보류와 조건부 고정관념 선호는 다르다. DiscrimEval은 $m_i=\log\sum_{yes,Yes}e^{l_{it}}-\log\sum_{no,No}e^{l_{it}}$, $q_i=\sigma(m_i)$다. m=0이면 q=0.5, m=1이면 q≈0.731이다. 평균 q와 평균 m은 비선형성 때문에 다른 결과를 낼 수 있다.

기본 효과는 $T-C$, V 효과는 $T_V-C_V$, 조절은 $(T_V-C_V)-(T-C)$이며 모델 차이는 동일 문항의 효과를 직접 뺀다. KoBBQ 조건별 분모는 108문항이고 DiscrimEval 조건별 분모는 1,050사례다. 후자는 질문별 인구집단 15조합을 평균한 70질문을 재표집한다. 예를 들어 Qwen KoBBQ 평균 보류 84.012%에서 76.335%를 빼면 약 7.677%p다.

부트스트랩 3,000회, KoBBQ seed20261030·DiscrimEval seed20261029를 유지했다. 추가 p값은 군집별 부호 반전 19,999회와 plus-one 보정이며, 무작위 배정 실험이 아니라 차이 분포의 대칭성에 의존하는 모형 기반 탐색 검정이다. 개별 95% 구간은 동시 구간이 아니다. 가족별 Holm 보정은 행동40개, V조절20개, 직접 모델 비교120개, 집단격차120개다. 감정 상관120개는 군집별 Spearman 근사 p값에 BH FDR 보정했다. 기존 가족보다 검정 수가 늘어 기존 모델의 보정값도 달라질 수 있다. 사후 분석임을 유지한다.

## 전체 주요 효과

| task        | model    | metric    | contrast   | effect_95ci                |   p_holm | reject_holm   |
|:------------|:---------|:----------|:-----------|:---------------------------|---------:|:--------------|
| KoBBQ       | Qwen     | p_unknown | main       | +7.677 [+3.139, +12.562]   |   0.0310 | True          |
| KoBBQ       | Qwen     | p_unknown | V          | +7.700 [+3.709, +12.164]   |   0.0050 | True          |
| KoBBQ       | Qwen     | p_sgp     | main       | -1.972 [-7.125, +3.250]    |   1.0000 | False         |
| KoBBQ       | Qwen     | p_sgp     | V          | -0.967 [-5.815, +3.936]    |   1.0000 | False         |
| KoBBQ       | Llama31  | p_unknown | main       | -8.296 [-10.818, -5.829]   |   0.0020 | True          |
| KoBBQ       | Llama31  | p_unknown | V          | -0.408 [-2.753, +2.059]    |   1.0000 | False         |
| KoBBQ       | Llama31  | p_sgp     | main       | -0.661 [-2.843, +1.492]    |   1.0000 | False         |
| KoBBQ       | Llama31  | p_sgp     | V          | -0.286 [-2.846, +2.205]    |   1.0000 | False         |
| KoBBQ       | DeepSeek | p_unknown | main       | +2.360 [+0.482, +4.072]    |   0.1440 | False         |
| KoBBQ       | DeepSeek | p_unknown | V          | -0.696 [-2.906, +1.250]    |   1.0000 | False         |
| KoBBQ       | DeepSeek | p_sgp     | main       | -2.015 [-4.727, +0.446]    |   1.0000 | False         |
| KoBBQ       | DeepSeek | p_sgp     | V          | +0.219 [-2.933, +3.335]    |   1.0000 | False         |
| KoBBQ       | Gemma2   | p_unknown | main       | +21.069 [+14.635, +28.235] |   0.0020 | True          |
| KoBBQ       | Gemma2   | p_unknown | V          | +25.333 [+18.856, +32.344] |   0.0020 | True          |
| KoBBQ       | Gemma2   | p_sgp     | main       | +0.353 [-3.511, +4.181]    |   1.0000 | False         |
| KoBBQ       | Gemma2   | p_sgp     | V          | +0.273 [-3.596, +4.214]    |   1.0000 | False         |
| KoBBQ       | Llama32  | p_unknown | main       | +6.398 [+4.727, +8.131]    |   0.0020 | True          |
| KoBBQ       | Llama32  | p_unknown | V          | +11.353 [+9.606, +13.074]  |   0.0020 | True          |
| KoBBQ       | Llama32  | p_sgp     | main       | -1.409 [-4.140, +1.376]    |   1.0000 | False         |
| KoBBQ       | Llama32  | p_sgp     | V          | -0.879 [-3.262, +1.419]    |   1.0000 | False         |
| DiscrimEval | Qwen     | q_yes     | main       | +5.433 [+2.308, +9.190]    |   0.0224 | True          |
| DiscrimEval | Qwen     | q_yes     | V          | -6.159 [-10.272, -2.164]   |   0.0740 | False         |
| DiscrimEval | Qwen     | margin    | main       | +0.166 [-0.373, +0.722]    |   1.0000 | False         |
| DiscrimEval | Qwen     | margin    | V          | -2.730 [-3.415, -2.052]    |   0.0020 | True          |
| DiscrimEval | Llama31  | q_yes     | main       | +2.399 [+0.666, +4.384]    |   0.2920 | False         |
| DiscrimEval | Llama31  | q_yes     | V          | +2.549 [+0.554, +4.767]    |   0.4360 | False         |
| DiscrimEval | Llama31  | margin    | main       | +0.153 [-0.021, +0.331]    |   1.0000 | False         |
| DiscrimEval | Llama31  | margin    | V          | +0.137 [-0.054, +0.339]    |   1.0000 | False         |
| DiscrimEval | DeepSeek | q_yes     | main       | +2.169 [+0.759, +3.753]    |   0.1290 | False         |
| DiscrimEval | DeepSeek | q_yes     | V          | -1.738 [-3.475, +0.165]    |   1.0000 | False         |
| DiscrimEval | DeepSeek | margin    | main       | +0.022 [-0.095, +0.143]    |   1.0000 | False         |
| DiscrimEval | DeepSeek | margin    | V          | -0.595 [-0.807, -0.373]    |   0.0020 | True          |
| DiscrimEval | Gemma2   | q_yes     | main       | +0.937 [-3.574, +5.417]    |   1.0000 | False         |
| DiscrimEval | Gemma2   | q_yes     | V          | +5.664 [+0.439, +10.687]   |   0.7370 | False         |
| DiscrimEval | Gemma2   | margin    | main       | -0.039 [-0.411, +0.325]    |   1.0000 | False         |
| DiscrimEval | Gemma2   | margin    | V          | +0.336 [-0.037, +0.705]    |   1.0000 | False         |
| DiscrimEval | Llama32  | q_yes     | main       | -0.897 [-2.625, +0.960]    |   1.0000 | False         |
| DiscrimEval | Llama32  | q_yes     | V          | -1.355 [-2.982, +0.348]    |   1.0000 | False         |
| DiscrimEval | Llama32  | margin    | main       | -0.292 [-0.481, -0.107]    |   0.0645 | False         |
| DiscrimEval | Llama32  | margin    | V          | -0.251 [-0.427, -0.084]    |   0.1290 | False         |

## V 조절 효과

| task        | model    | metric    |      est |       lo |      hi |   p_holm | reject_holm   |
|:------------|:---------|:----------|---------:|---------:|--------:|---------:|:--------------|
| KoBBQ       | Qwen     | p_unknown |   0.0233 |  -3.0289 |  2.7596 |   1.0000 | False         |
| KoBBQ       | Qwen     | p_sgp     |   1.0050 |  -2.1621 |  4.1653 |   1.0000 | False         |
| KoBBQ       | Llama31  | p_unknown |   7.8877 |   6.1859 |  9.7805 |   0.0010 | True          |
| KoBBQ       | Llama31  | p_sgp     |   0.3749 |  -1.0405 |  1.7608 |   1.0000 | False         |
| KoBBQ       | DeepSeek | p_unknown |  -3.0560 |  -5.2803 | -1.1284 |   0.0168 | True          |
| KoBBQ       | DeepSeek | p_sgp     |   2.2340 |  -0.6307 |  5.0846 |   1.0000 | False         |
| KoBBQ       | Gemma2   | p_unknown |   4.2634 |   0.2570 |  8.1783 |   0.4480 | False         |
| KoBBQ       | Gemma2   | p_sgp     |  -0.0793 |  -2.0259 |  1.7733 |   1.0000 | False         |
| KoBBQ       | Llama32  | p_unknown |   4.9555 |   3.5538 |  6.4334 |   0.0010 | True          |
| KoBBQ       | Llama32  | p_sgp     |   0.5306 |  -1.1085 |  2.1526 |   1.0000 | False         |
| DiscrimEval | Qwen     | q_yes     | -11.5921 | -15.3131 | -8.2447 |   0.0010 | True          |
| DiscrimEval | Qwen     | margin    |  -2.8956 |  -3.2768 | -2.5122 |   0.0010 | True          |
| DiscrimEval | Llama31  | q_yes     |   0.1500 |  -0.6428 |  0.9017 |   1.0000 | False         |
| DiscrimEval | Llama31  | margin    |  -0.0161 |  -0.0951 |  0.0614 |   1.0000 | False         |
| DiscrimEval | DeepSeek | q_yes     |  -3.9069 |  -4.8387 | -3.0390 |   0.0010 | True          |
| DiscrimEval | DeepSeek | margin    |  -0.6166 |  -0.7461 | -0.4881 |   0.0010 | True          |
| DiscrimEval | Gemma2   | q_yes     |   4.7269 |   2.3589 |  7.2838 |   0.0032 | True          |
| DiscrimEval | Gemma2   | margin    |   0.3750 |   0.2150 |  0.5422 |   0.0014 | True          |
| DiscrimEval | Llama32  | q_yes     |  -0.4581 |  -1.5105 |  0.5208 |   1.0000 | False         |
| DiscrimEval | Llama32  | margin    |   0.0412 |  -0.0320 |  0.1127 |   1.0000 | False         |

## 직접 모델 비교

120개 중 Holm 보정 후 41개가 남았다. 유의성 유무만 비교하지 않고 같은 문항 효과의 차이를 계산했다. 순수한 모델 크기 효과나 모집단 순위로 해석하지 않는다.

| task        | model_a   | model_b   | metric    | contrast     |      est |       lo |       hi |   p_holm | reject_holm   |
|:------------|:----------|:----------|:----------|:-------------|---------:|---------:|---------:|---------:|:--------------|
| KoBBQ       | Qwen      | Llama31   | p_unknown | main         |  15.9725 |  10.5152 |  21.4599 |   0.0060 | True          |
| KoBBQ       | Qwen      | Llama31   | p_unknown | V            |   8.1080 |   3.5267 |  13.0222 |   0.0624 | False         |
| KoBBQ       | Qwen      | Llama31   | p_unknown | V_minus_main |  -7.8645 | -11.2274 |  -4.6382 |   0.0060 | True          |
| KoBBQ       | Qwen      | Llama31   | p_sgp     | main         |  -1.3109 |  -7.5448 |   4.9645 |   1.0000 | False         |
| KoBBQ       | Qwen      | Llama31   | p_sgp     | V            |  -0.6809 |  -7.1752 |   6.1268 |   1.0000 | False         |
| KoBBQ       | Qwen      | Llama31   | p_sgp     | V_minus_main |   0.6300 |  -2.9024 |   4.3006 |   1.0000 | False         |
| KoBBQ       | Qwen      | DeepSeek  | p_unknown | main         |   5.3168 |   0.6206 |  10.2775 |   1.0000 | False         |
| KoBBQ       | Qwen      | DeepSeek  | p_unknown | V            |   8.3961 |   3.8435 |  13.2942 |   0.0210 | True          |
| KoBBQ       | Qwen      | DeepSeek  | p_unknown | V_minus_main |   3.0793 |  -0.7803 |   6.7409 |   1.0000 | False         |
| KoBBQ       | Qwen      | DeepSeek  | p_sgp     | main         |   0.0430 |  -5.6206 |   5.6585 |   1.0000 | False         |
| KoBBQ       | Qwen      | DeepSeek  | p_sgp     | V            |  -1.1861 |  -7.2575 |   5.0637 |   1.0000 | False         |
| KoBBQ       | Qwen      | DeepSeek  | p_sgp     | V_minus_main |  -1.2290 |  -5.9360 |   3.2758 |   1.0000 | False         |
| KoBBQ       | Qwen      | Gemma2    | p_unknown | main         | -13.3924 | -21.8807 |  -5.1184 |   0.1330 | False         |
| KoBBQ       | Qwen      | Gemma2    | p_unknown | V            | -17.6325 | -25.1902 | -10.1286 |   0.0060 | True          |
| KoBBQ       | Qwen      | Gemma2    | p_unknown | V_minus_main |  -4.2401 |  -9.5175 |   0.5958 |   1.0000 | False         |
| KoBBQ       | Qwen      | Gemma2    | p_sgp     | main         |  -2.3248 |  -9.0590 |   4.5846 |   1.0000 | False         |
| KoBBQ       | Qwen      | Gemma2    | p_sgp     | V            |  -1.2405 |  -7.5812 |   5.1337 |   1.0000 | False         |
| KoBBQ       | Qwen      | Gemma2    | p_sgp     | V_minus_main |   1.0843 |  -2.5085 |   4.7514 |   1.0000 | False         |
| KoBBQ       | Qwen      | Llama32   | p_unknown | main         |   1.2792 |  -3.6751 |   6.4221 |   1.0000 | False         |
| KoBBQ       | Qwen      | Llama32   | p_unknown | V            |  -3.6530 |  -7.7876 |   0.8929 |   1.0000 | False         |
| KoBBQ       | Qwen      | Llama32   | p_unknown | V_minus_main |  -4.9322 |  -8.2278 |  -1.9023 |   0.0975 | False         |
| KoBBQ       | Qwen      | Llama32   | p_sgp     | main         |  -0.5627 |  -5.8746 |   4.7850 |   1.0000 | False         |
| KoBBQ       | Qwen      | Llama32   | p_sgp     | V            |  -0.0884 |  -5.0060 |   5.0826 |   1.0000 | False         |
| KoBBQ       | Qwen      | Llama32   | p_sgp     | V_minus_main |   0.4744 |  -3.0352 |   4.1058 |   1.0000 | False         |
| KoBBQ       | Llama31   | DeepSeek  | p_unknown | main         | -10.6557 | -13.8402 |  -7.6249 |   0.0060 | True          |
| KoBBQ       | Llama31   | DeepSeek  | p_unknown | V            |   0.2880 |  -2.5352 |   3.0318 |   1.0000 | False         |
| KoBBQ       | Llama31   | DeepSeek  | p_unknown | V_minus_main |  10.9437 |   8.1839 |  13.8739 |   0.0060 | True          |
| KoBBQ       | Llama31   | DeepSeek  | p_sgp     | main         |   1.3539 |  -2.0747 |   4.6230 |   1.0000 | False         |
| KoBBQ       | Llama31   | DeepSeek  | p_sgp     | V            |  -0.5052 |  -4.2461 |   3.0931 |   1.0000 | False         |
| KoBBQ       | Llama31   | DeepSeek  | p_sgp     | V_minus_main |  -1.8591 |  -4.8096 |   1.1195 |   1.0000 | False         |
| KoBBQ       | Llama31   | Gemma2    | p_unknown | main         | -29.3649 | -36.8358 | -22.6228 |   0.0060 | True          |
| KoBBQ       | Llama31   | Gemma2    | p_unknown | V            | -25.7406 | -32.6074 | -19.4104 |   0.0060 | True          |
| KoBBQ       | Llama31   | Gemma2    | p_unknown | V_minus_main |   3.6243 |  -0.6574 |   7.9066 |   1.0000 | False         |
| KoBBQ       | Llama31   | Gemma2    | p_sgp     | main         |  -1.0138 |  -5.2234 |   3.2170 |   1.0000 | False         |
| KoBBQ       | Llama31   | Gemma2    | p_sgp     | V            |  -0.5596 |  -4.7555 |   3.7997 |   1.0000 | False         |
| KoBBQ       | Llama31   | Gemma2    | p_sgp     | V_minus_main |   0.4543 |  -1.9492 |   2.8341 |   1.0000 | False         |
| KoBBQ       | Llama31   | Llama32   | p_unknown | main         | -14.6932 | -17.3538 | -12.0375 |   0.0060 | True          |
| KoBBQ       | Llama31   | Llama32   | p_unknown | V            | -11.7610 | -14.4572 |  -8.8514 |   0.0060 | True          |
| KoBBQ       | Llama31   | Llama32   | p_unknown | V_minus_main |   2.9322 |   0.9738 |   5.0653 |   0.3680 | False         |
| KoBBQ       | Llama31   | Llama32   | p_sgp     | main         |   0.7482 |  -3.4015 |   4.7382 |   1.0000 | False         |
| KoBBQ       | Llama31   | Llama32   | p_sgp     | V            |   0.5925 |  -2.9009 |   4.0666 |   1.0000 | False         |
| KoBBQ       | Llama31   | Llama32   | p_sgp     | V_minus_main |  -0.1557 |  -1.8275 |   1.5278 |   1.0000 | False         |
| KoBBQ       | DeepSeek  | Gemma2    | p_unknown | main         | -18.7092 | -25.9336 | -11.8650 |   0.0060 | True          |
| KoBBQ       | DeepSeek  | Gemma2    | p_unknown | V            | -26.0286 | -33.0504 | -19.4154 |   0.0060 | True          |
| KoBBQ       | DeepSeek  | Gemma2    | p_unknown | V_minus_main |  -7.3194 | -11.5995 |  -2.9109 |   0.0836 | False         |
| KoBBQ       | DeepSeek  | Gemma2    | p_sgp     | main         |  -2.3677 |  -7.2171 |   2.4473 |   1.0000 | False         |
| KoBBQ       | DeepSeek  | Gemma2    | p_sgp     | V            |  -0.0544 |  -4.8553 |   4.7118 |   1.0000 | False         |
| KoBBQ       | DeepSeek  | Gemma2    | p_sgp     | V_minus_main |   2.3133 |  -1.1776 |   5.6897 |   1.0000 | False         |
| KoBBQ       | DeepSeek  | Llama32   | p_unknown | main         |  -4.0375 |  -6.5879 |  -1.4605 |   0.1310 | False         |
| KoBBQ       | DeepSeek  | Llama32   | p_unknown | V            | -12.0490 | -14.8991 |  -9.2809 |   0.0060 | True          |
| KoBBQ       | DeepSeek  | Llama32   | p_unknown | V_minus_main |  -8.0115 | -10.5110 |  -5.5080 |   0.0060 | True          |
| KoBBQ       | DeepSeek  | Llama32   | p_sgp     | main         |  -0.6057 |  -4.6579 |   3.0921 |   1.0000 | False         |
| KoBBQ       | DeepSeek  | Llama32   | p_sgp     | V            |   1.0977 |  -2.8425 |   5.0199 |   1.0000 | False         |
| KoBBQ       | DeepSeek  | Llama32   | p_sgp     | V_minus_main |   1.7034 |  -1.3936 |   4.8743 |   1.0000 | False         |
| KoBBQ       | Gemma2    | Llama32   | p_unknown | main         |  14.6717 |   7.7150 |  22.1698 |   0.0130 | True          |
| KoBBQ       | Gemma2    | Llama32   | p_unknown | V            |  13.9796 |   6.8896 |  21.5269 |   0.0400 | True          |
| KoBBQ       | Gemma2    | Llama32   | p_unknown | V_minus_main |  -0.6921 |  -4.7769 |   3.5841 |   1.0000 | False         |
| KoBBQ       | Gemma2    | Llama32   | p_sgp     | main         |   1.7620 |  -2.5692 |   5.9024 |   1.0000 | False         |
| KoBBQ       | Gemma2    | Llama32   | p_sgp     | V            |   1.1521 |  -2.8474 |   4.8636 |   1.0000 | False         |
| KoBBQ       | Gemma2    | Llama32   | p_sgp     | V_minus_main |  -0.6100 |  -3.0865 |   1.8660 |   1.0000 | False         |
| DiscrimEval | Qwen      | Llama31   | q_yes     | main         |   3.0340 |  -0.1553 |   6.6249 |   1.0000 | False         |
| DiscrimEval | Qwen      | Llama31   | q_yes     | V            |  -8.7080 | -13.6207 |  -4.1560 |   0.0130 | True          |
| DiscrimEval | Qwen      | Llama31   | q_yes     | V_minus_main | -11.7421 | -15.4908 |  -8.1935 |   0.0060 | True          |
| DiscrimEval | Qwen      | Llama31   | margin    | main         |   0.0128 |  -0.5565 |   0.5710 |   1.0000 | False         |
| DiscrimEval | Qwen      | Llama31   | margin    | V            |  -2.8667 |  -3.5444 |  -2.1975 |   0.0060 | True          |
| DiscrimEval | Qwen      | Llama31   | margin    | V_minus_main |  -2.8794 |  -3.2472 |  -2.5145 |   0.0060 | True          |
| DiscrimEval | Qwen      | DeepSeek  | q_yes     | main         |   3.2640 |  -0.4709 |   7.4257 |   1.0000 | False         |
| DiscrimEval | Qwen      | DeepSeek  | q_yes     | V            |  -4.4211 |  -8.9282 |   0.0340 |   1.0000 | False         |
| DiscrimEval | Qwen      | DeepSeek  | q_yes     | V_minus_main |  -7.6851 | -11.4054 |  -4.3102 |   0.0060 | True          |
| DiscrimEval | Qwen      | DeepSeek  | margin    | main         |   0.1439 |  -0.4261 |   0.7222 |   1.0000 | False         |
| DiscrimEval | Qwen      | DeepSeek  | margin    | V            |  -2.1350 |  -2.7848 |  -1.4695 |   0.0060 | True          |
| DiscrimEval | Qwen      | DeepSeek  | margin    | V_minus_main |  -2.2789 |  -2.6292 |  -1.9307 |   0.0060 | True          |
| DiscrimEval | Qwen      | Gemma2    | q_yes     | main         |   4.4963 |  -0.6046 |   9.6570 |   1.0000 | False         |
| DiscrimEval | Qwen      | Gemma2    | q_yes     | V            | -11.8227 | -17.5429 |  -6.3008 |   0.0210 | True          |
| DiscrimEval | Qwen      | Gemma2    | q_yes     | V_minus_main | -16.3189 | -21.0266 | -11.9821 |   0.0060 | True          |
| DiscrimEval | Qwen      | Gemma2    | margin    | main         |   0.2053 |  -0.4791 |   0.8747 |   1.0000 | False         |
| DiscrimEval | Qwen      | Gemma2    | margin    | V            |  -3.0653 |  -3.8372 |  -2.3215 |   0.0060 | True          |
| DiscrimEval | Qwen      | Gemma2    | margin    | V_minus_main |  -3.2706 |  -3.6634 |  -2.8703 |   0.0060 | True          |
| DiscrimEval | Qwen      | Llama32   | q_yes     | main         |   6.3300 |   2.6302 |  10.4166 |   0.0975 | False         |
| DiscrimEval | Qwen      | Llama32   | q_yes     | V            |  -4.8040 |  -9.4739 |  -0.3081 |   1.0000 | False         |
| DiscrimEval | Qwen      | Llama32   | q_yes     | V_minus_main | -11.1340 | -14.6662 |  -7.9613 |   0.0060 | True          |
| DiscrimEval | Qwen      | Llama32   | margin    | main         |   0.4583 |  -0.1322 |   1.0443 |   1.0000 | False         |
| DiscrimEval | Qwen      | Llama32   | margin    | V            |  -2.4785 |  -3.2046 |  -1.7659 |   0.0060 | True          |
| DiscrimEval | Qwen      | Llama32   | margin    | V_minus_main |  -2.9367 |  -3.3366 |  -2.5441 |   0.0060 | True          |
| DiscrimEval | Llama31   | DeepSeek  | q_yes     | main         |   0.2300 |  -2.1383 |   2.6104 |   1.0000 | False         |
| DiscrimEval | Llama31   | DeepSeek  | q_yes     | V            |   4.2869 |   1.5537 |   6.9992 |   0.1350 | False         |
| DiscrimEval | Llama31   | DeepSeek  | q_yes     | V_minus_main |   4.0569 |   2.8767 |   5.3328 |   0.0060 | True          |
| DiscrimEval | Llama31   | DeepSeek  | margin    | main         |   0.1311 |  -0.0609 |   0.3289 |   1.0000 | False         |
| DiscrimEval | Llama31   | DeepSeek  | margin    | V            |   0.7316 |   0.4640 |   0.9729 |   0.0060 | True          |
| DiscrimEval | Llama31   | DeepSeek  | margin    | V_minus_main |   0.6005 |   0.4605 |   0.7414 |   0.0060 | True          |
| DiscrimEval | Llama31   | Gemma2    | q_yes     | main         |   1.4623 |  -3.4440 |   6.2936 |   1.0000 | False         |
| DiscrimEval | Llama31   | Gemma2    | q_yes     | V            |  -3.1146 |  -8.1900 |   2.0482 |   1.0000 | False         |
| DiscrimEval | Llama31   | Gemma2    | q_yes     | V_minus_main |  -4.5769 |  -7.3219 |  -2.1577 |   0.0246 | True          |
| DiscrimEval | Llama31   | Gemma2    | margin    | main         |   0.1925 |  -0.1791 |   0.5803 |   1.0000 | False         |
| DiscrimEval | Llama31   | Gemma2    | margin    | V            |  -0.1987 |  -0.5680 |   0.1823 |   1.0000 | False         |
| DiscrimEval | Llama31   | Gemma2    | margin    | V_minus_main |  -0.3911 |  -0.5639 |  -0.2165 |   0.0060 | True          |
| DiscrimEval | Llama31   | Llama32   | q_yes     | main         |   3.2960 |   0.8445 |   5.8443 |   0.5260 | False         |
| DiscrimEval | Llama31   | Llama32   | q_yes     | V            |   3.9041 |   1.2034 |   6.7290 |   0.2720 | False         |
| DiscrimEval | Llama31   | Llama32   | q_yes     | V_minus_main |   0.6080 |  -0.7621 |   2.0465 |   1.0000 | False         |
| DiscrimEval | Llama31   | Llama32   | margin    | main         |   0.4455 |   0.1993 |   0.6926 |   0.0732 | False         |
| DiscrimEval | Llama31   | Llama32   | margin    | V            |   0.3882 |   0.1457 |   0.6373 |   0.1830 | False         |
| DiscrimEval | Llama31   | Llama32   | margin    | V_minus_main |  -0.0573 |  -0.1739 |   0.0578 |   1.0000 | False         |
| DiscrimEval | DeepSeek  | Gemma2    | q_yes     | main         |   1.2323 |  -3.4469 |   6.0182 |   1.0000 | False         |
| DiscrimEval | DeepSeek  | Gemma2    | q_yes     | V            |  -7.4016 | -12.8997 |  -2.0228 |   0.5020 | False         |
| DiscrimEval | DeepSeek  | Gemma2    | q_yes     | V_minus_main |  -8.6338 | -11.5573 |  -6.0448 |   0.0060 | True          |
| DiscrimEval | DeepSeek  | Gemma2    | margin    | main         |   0.0613 |  -0.3467 |   0.4724 |   1.0000 | False         |
| DiscrimEval | DeepSeek  | Gemma2    | margin    | V            |  -0.9303 |  -1.4077 |  -0.4446 |   0.0324 | True          |
| DiscrimEval | DeepSeek  | Gemma2    | margin    | V_minus_main |  -0.9917 |  -1.2035 |  -0.7718 |   0.0060 | True          |
| DiscrimEval | DeepSeek  | Llama32   | q_yes     | main         |   3.0660 |   0.8552 |   5.3813 |   0.4710 | False         |
| DiscrimEval | DeepSeek  | Llama32   | q_yes     | V            |  -0.3829 |  -2.2839 |   1.6225 |   1.0000 | False         |
| DiscrimEval | DeepSeek  | Llama32   | q_yes     | V_minus_main |  -3.4489 |  -4.8804 |  -1.9063 |   0.0060 | True          |
| DiscrimEval | DeepSeek  | Llama32   | margin    | main         |   0.3143 |   0.1223 |   0.5128 |   0.1350 | False         |
| DiscrimEval | DeepSeek  | Llama32   | margin    | V            |  -0.3435 |  -0.5801 |  -0.0933 |   0.4190 | False         |
| DiscrimEval | DeepSeek  | Llama32   | margin    | V_minus_main |  -0.6578 |  -0.8279 |  -0.4976 |   0.0060 | True          |
| DiscrimEval | Gemma2    | Llama32   | q_yes     | main         |   1.8338 |  -2.7941 |   6.5770 |   1.0000 | False         |
| DiscrimEval | Gemma2    | Llama32   | q_yes     | V            |   7.0187 |   1.5814 |  12.5244 |   0.7900 | False         |
| DiscrimEval | Gemma2    | Llama32   | q_yes     | V_minus_main |   5.1849 |   2.6192 |   7.9578 |   0.0170 | True          |
| DiscrimEval | Gemma2    | Llama32   | margin    | main         |   0.2530 |  -0.1732 |   0.6708 |   1.0000 | False         |
| DiscrimEval | Gemma2    | Llama32   | margin    | V            |   0.5868 |   0.1421 |   1.0306 |   0.7220 | False         |
| DiscrimEval | Gemma2    | Llama32   | margin    | V_minus_main |   0.3338 |   0.1530 |   0.5238 |   0.0513 | False         |

## 인구집단 격차

120개 중 Holm 보정 후 9개가 남았다. 부호 있는 평균 격차와 질문별 절대 격차의 변화는 별개다. 전체 긍정 응답 변화나 유의한 집단 격차를 곧바로 공정성 개선 또는 차별 악화로 동일시하지 않는다.

| model    | group           | metric   | contrast   |   record_gap |   threat_gap |   absolute_gap_change |     est |   p_holm |
|:---------|:----------------|:---------|:-----------|-------------:|-------------:|----------------------:|--------:|---------:|
| DeepSeek | Black           | q_yes    | main       |       1.4264 |       0.5089 |               -0.4371 | -0.9176 |   0.0117 |
| DeepSeek | Black           | margin   | main       |       0.1457 |       0.0741 |               -0.0387 | -0.0716 |   0.0174 |
| DeepSeek | Black           | margin   | V          |       0.1434 |       0.0745 |               -0.0595 | -0.0689 |   0.0060 |
| Gemma2   | Black           | margin   | main       |       0.2329 |       0.4332 |                0.1924 |  0.2003 |   0.0060 |
| Gemma2   | Black           | margin   | V          |       0.2274 |       0.4213 |                0.1932 |  0.1940 |   0.0060 |
| Gemma2   | Native American | margin   | V          |       0.1585 |       0.2938 |                0.1099 |  0.1353 |   0.0230 |
| Llama32  | Hispanic        | q_yes    | main       |       0.6615 |       1.4745 |                0.7802 |  0.8130 |   0.0452 |
| Llama32  | Hispanic        | q_yes    | V          |       0.4986 |       1.3391 |                0.6636 |  0.8405 |   0.0230 |
| Llama32  | Hispanic        | margin   | V          |       0.1285 |       0.1930 |                0.0365 |  0.0646 |   0.0452 |

## 감정과 응답의 관계

120개 연관 중 BH 보정 후 6개가 남았다. Fear·Anxiety·Certainty 변화와 응답 점수 변화의 군집별 관계다. 축 크기를 모델 간 합치지 않았고 인과 매개를 주장하지 않는다.

| task        | model    | contrast   | axis      | outcome   |     rho |   p_bh |
|:------------|:---------|:-----------|:----------|:----------|--------:|-------:|
| KoBBQ       | Llama31  | main       | Certainty | p_unknown | -0.4297 | 0.0003 |
| KoBBQ       | Llama31  | V          | Certainty | p_unknown | -0.4212 | 0.0003 |
| KoBBQ       | Gemma2   | main       | Certainty | p_unknown |  0.3095 | 0.0224 |
| DiscrimEval | DeepSeek | main       | Fear      | margin    | -0.4259 | 0.0057 |
| DiscrimEval | DeepSeek | V          | Fear      | margin    | -0.4581 | 0.0027 |
| DiscrimEval | DeepSeek | V          | Certainty | margin    |  0.4483 | 0.0030 |

## 선택지 정규화와 전체 어휘 질량

점수는 자유 생성 응답 빈도가 아니다. 여기서 unknown 토큰 질량은 영어 단어 unknown의 확률이 아니라, 해당 문항의 ‘알 수 없음’ 답에 대응하는 A/B/C 선택 토큰의 전체 어휘 확률 질량을 뜻한다. Gemma KoBBQ 기본 위협의 A/B/C 질량은 약14.75%이고 Llama3.2는 약51.41%다. Gemma 기본 효과는 조건부 unknown +21.07%p와 달리 전체 어휘 unknown 토큰 질량에서는 −12.98%p다. Llama3.2도 +6.40%p와 −0.08%p로 다르다. 큰 조건부 효과를 더 강한 자기보존이나 실제 보류 증가로 단정하지 않는다. 전체 어휘 질량도 완성된 자유 응답의 빈도는 아니다. 선택 질량 진단은 기술적 민감도이며 새 p값 발견을 추가하지 않는다.

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
| Llama31  | main         |   2.3522 |   0.6169 |  4.3351 |
| Llama31  | V            |   2.4932 |   0.5037 |  4.7247 |
| Llama31  | V_minus_main |   0.1410 |  -0.6525 |  0.8925 |
| DeepSeek | main         |   2.1702 |   0.7631 |  3.7617 |
| DeepSeek | V            |  -1.7137 |  -3.4532 |  0.1896 |
| DeepSeek | V_minus_main |  -3.8840 |  -4.8178 | -3.0193 |
| Gemma2   | main         |   1.7633 |  -1.6543 |  5.2437 |
| Gemma2   | V            |   5.3735 |   1.3241 |  9.2583 |
| Gemma2   | V_minus_main |   3.6101 |   1.8455 |  5.4647 |
| Llama32  | main         |  -1.0160 |  -2.7339 |  0.8199 |
| Llama32  | V            |  -1.5333 |  -3.1575 |  0.1667 |
| Llama32  | V_minus_main |  -0.5173 |  -1.5639 |  0.4558 |

## 종합 해석과 한계

위협에 대한 사회적 응답 점수는 모델 구현·과제·단서 배치·결과 척도·제한된 선택지 정규화에 의존한다. 판단 보류, 조건부 고정관념 선호, 전체 긍정 점수, 인구집단 격차, 감정 판독을 하나의 편향 증가로 묶을 수 없다. 새 모델의 결과를 보고 문항을 재선정하거나 축을 조정하지 않았다.

KoBBQ 108문항은 Llama3.1 기준으로 선정됐다. DiscrimEval은 explicit 70질문·60세다. 단일 문구, 모델별 템플릿·언어 지원·실행 기기 차이와 작은 앵커 검증의 한계가 남는다. DeepSeek는 구분자 없는 system 앞부분, Gemma는 첫 user 턴 결합을 사용한다. 새 Llama3.1의 입력 날짜는 기존 실행과 맞췄지만 다른 모델의 날짜·역할 표현이 동일하다고 주장하지 않는다. KoBBQ는 모든 시행의 전체 활성값이 보존된 것은 아니며, Qwen 역사적 축의 생성 당시 연결에도 한계가 있다.

## 산출물과 보존

00_protocol는 계획·출처, 01_frozen_inputs는 원 CSV 사본, 02_code는 재현 코드, 03_analysis는 모든 검정·민감도, 04_figures는 인쇄용 그림, 05_reports는 검증과 해석, 07_publication은 게시 검증이다. 원고·LaTeX·Overleaf 사본은 생성·편집·컴파일하지 않는다. 폴더15도 변경하지 않는다.