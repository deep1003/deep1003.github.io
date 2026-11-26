# 와일드 클러스터 부트스트랩과 직종 간 공통 충격 민감도

2026년 11월 26일. 홈페이지·기존 원고·원자료·이전 추정 결과 파일을 변경하지 않았다.

## 결론

직종별 독립 군집 가정 아래에서는 세 대비 모두 와일드 클러스터 부트스트랩 및 이번 세 대비의 Holm 보정 후 유의했다. 그러나 같은 KECO 중분류 직종들의 동시·시차 상관을 허용하는 더 큰 군집으로 묶으면 남성 25–29세 취득과 같은 연령 남녀 고용 대비는 비유의가 된다. 여성 20–24세 취득은 중분류 군집의 원 p<0.05이나 세 대비를 보정하면 비유의다. 따라서 공통 충격 구조를 넓혀도 세 결과가 강건하다고 결론내리지 않는다. 비유의는 효과가 없다는 입증도 아니다.

## 핵심 결과

| 대비                             | 기존 추정치   |   직종별 WCR p |   직종별 3검정 Holm p |   중분류 WCR p |   중분류 3검정 Holm p |
|:---------------------------------|:--------------|---------------:|----------------------:|---------------:|----------------------:|
| 20–24세 여성 취득                | -1.843        |        0.00576 |               0.01299 |        0.02243 |               0.06729 |
| 25–29세 남성 취득                | -1.067        |        0.00433 |               0.01299 |        0.10179 |               0.20358 |
| 25–29세 여성−남성 상대 고용 변화 | +13.05%       |        0.00774 |               0.01299 |        0.13670 |               0.20358 |

취득 계수의 단위는 고정 2022년 11월 피보험자 100명당 월 취득 집계값의 상대적 차이다. 남녀 고용 대비는 로그 여성/남성 고용비 DID의 exp(β)−1이며 퍼센트포인트 차이가 아니다. 효과 크기는 기존 값과 같고 불확실성 평가만 달리했다.

## 설계와 구현

동일한 105개 직종과 전후 각각 36개월, 전환월 제외 조건을 유지했다. 기본 회귀는 직종·월 고정효과와 Q5×사후 상호작용이다. 20–24세 여성·25–29세 남성은 고정 기준월 인원 100명당 취득을, 남녀 대비는 같은 직종의 로그 여성−로그 남성 고용을 사용했다.

귀무가설 β=0을 부과한 제한 모형의 잔차로 WCR11 와일드 클러스터 부트스트랩을 직접 구현했다. 각 반복에서 직종·월 고정효과를 다시 제거하고 재추정한 계수와 CRV1 군집 표준오차의 양측 studentized t를 비교했다. 부트스트랩 군집은 105개 직종 또는 공식 KECO 코드 앞 두 자리의 31개 중분류다. 후자에는 Q5가 포함된 군집이 7개이고, Q5와 Q1–Q4가 섞인 군집은 2개다. 중분류는 산업 분류가 아니다.

각 대비·군집·가중 분포에 99,999회를 적용했다. Rademacher의 시드는 20261126, Webb 6점 분포는 20261127이다. p=(초과 횟수+1)/(유효 반복+1)로 계산했다. 모든 변형에서 99,999회가 유효했다. 세 현재 요청 대비 안의 Holm 보정이며 이전 8흐름 전체·연구 전체의 사후 선택이나 명세 탐색을 보정한 것은 아니다.

빠른 계산식은 매 반복의 고정효과 재투영을 포함한다. 고정효과를 한 번 제거한 뒤 잔차 부호만 바꾸는 단순화를 하지 않았다. 별도의 full-dummy statsmodels 회귀로 여섯 제한 부트스트랩 표본의 계수와 군집 표준오차를 대조해 1e−10 이내 일치를 확인했다. 두 방향 군집 분산도 statsmodels cov_cluster_2groups와 대조했다. 이는 계산 구현 점검이며 군집 독립 가정을 검증한 것은 아니다.

## Webb 분포와 몬테카를로 오차

| target                                | cluster        | weights    |   bootstrap_p |    mc_se |   p_holm_three_requested_tests |   clusters |   treated_clusters |
|:--------------------------------------|:---------------|:-----------|--------------:|---------:|-------------------------------:|-----------:|-------------------:|
| female20_24_acquisitions              | occupation     | rademacher |      0.005760 | 0.000239 |                       0.012990 |        105 |                 20 |
| female20_24_acquisitions              | occupation     | webb       |      0.005130 | 0.000226 |                       0.012360 |        105 |                 20 |
| female20_24_acquisitions              | KECO_two_digit | rademacher |      0.022430 | 0.000468 |                       0.067290 |         31 |                  7 |
| female20_24_acquisitions              | KECO_two_digit | webb       |      0.020680 | 0.000450 |                       0.062040 |         31 |                  7 |
| male25_29_acquisitions                | occupation     | rademacher |      0.004330 | 0.000208 |                       0.012990 |        105 |                 20 |
| male25_29_acquisitions                | occupation     | webb       |      0.004120 | 0.000203 |                       0.012360 |        105 |                 20 |
| male25_29_acquisitions                | KECO_two_digit | rademacher |      0.101790 | 0.000956 |                       0.203580 |         31 |                  7 |
| male25_29_acquisitions                | KECO_two_digit | webb       |      0.099370 | 0.000946 |                       0.198740 |         31 |                  7 |
| age25_29_female_minus_male_employment | occupation     | rademacher |      0.007740 | 0.000277 |                       0.012990 |        105 |                 20 |
| age25_29_female_minus_male_employment | occupation     | webb       |      0.007520 | 0.000273 |                       0.012360 |        105 |                 20 |
| age25_29_female_minus_male_employment | KECO_two_digit | rademacher |      0.136700 | 0.001086 |                       0.203580 |         31 |                  7 |
| age25_29_female_minus_male_employment | KECO_two_digit | webb       |      0.124220 | 0.001043 |                       0.198740 |         31 |                  7 |

Rademacher와 Webb 결과의 핵심 판단이 같다. 몬테카를로 표준오차는 WILD_BOOTSTRAP_RESULTS.csv에 보존했다. 중분류 군집에서는 처리 포함 군집 수가 적고 처리·대조 분포도 불균형해, 부트스트랩 자체도 모든 유한표본 문제를 해소하지 않는다.

## 공통 충격 점검

1. 직종·월의 두 방향 군집을 적용해 동월의 직종 간 임의 상관을 허용했다. 세 대비의 원 p는 0.0103, 0.0047, 0.0064다. 이는 점근적 sandwich 추론이며 위 중분류 와일드 부트스트랩과 같은 검정이 아니다. 동월 상관을 허용해도 다른 직종 사이의 시차 상관을 모두 허용하는 것은 아니다.

| target                                | cluster                |   coefficient |       se |        p |   df |   variance |
|:--------------------------------------|:-----------------------|--------------:|---------:|---------:|-----:|-----------:|
| female20_24_acquisitions              | occupation + month     |     -1.843350 | 0.698995 | 0.010264 |   71 |   0.488594 |
| female20_24_acquisitions              | KECO_two_digit + month |     -1.843350 | 0.616723 | 0.005542 |   30 |   0.380347 |
| male25_29_acquisitions                | occupation + month     |     -1.066865 | 0.365904 | 0.004746 |   71 |   0.133886 |
| male25_29_acquisitions                | KECO_two_digit + month |     -1.066865 | 0.491040 | 0.037836 |   30 |   0.241121 |
| age25_29_female_minus_male_employment | occupation + month     |      0.122643 | 0.043688 | 0.006447 |   71 |   0.001909 |
| age25_29_female_minus_male_employment | KECO_two_digit + month |      0.122643 | 0.047099 | 0.014195 |   30 |   0.002218 |

2. 기본 회귀 잔차의 월별 동행성을 계산했다. 같은 중분류 안의 평균 상관은 여성 취득 0.175, 남성 취득 0.308, 남녀 고용비 0.097이다. 중분류 간 평균은 각각 0.046, 0.083, 0.010이다. 같은 계열 안의 동행성이 더 크지만 이는 기술적 진단이며 정식 공통 충격 검정이나 충격 원인 식별이 아니다. 같은 군집 내부 상관을 허용한 부트스트랩에서 판단이 달라지는 이유를 점검하는 보조 지표다.

| target                                |   pairs | type                   |   mean_correlation |   median_correlation |   positive_share |
|:--------------------------------------|--------:|:-----------------------|-------------------:|---------------------:|-----------------:|
| female20_24_acquisitions              |     190 | within_KECO_two_digit  |             0.1747 |               0.1428 |           0.7211 |
| female20_24_acquisitions              |    5270 | between_KECO_two_digit |             0.0455 |               0.0422 |           0.5713 |
| male25_29_acquisitions                |     190 | within_KECO_two_digit  |             0.3081 |               0.2861 |           0.8579 |
| male25_29_acquisitions                |    5270 | between_KECO_two_digit |             0.0831 |               0.0786 |           0.5941 |
| age25_29_female_minus_male_employment |     190 | within_KECO_two_digit  |             0.0968 |               0.1778 |           0.6000 |
| age25_29_female_minus_male_employment |    5270 | between_KECO_two_digit |             0.0099 |               0.0266 |           0.5106 |

3. 고정 직종 표본의 월별 Q5−Q1–Q4 평균 격차로 축약한 시계열에 HAC 6·12·18개월 보정을 적용했다. 전환월은 더미로 따로 흡수해 73개월의 달력 간격을 유지했다. 같은 DID 계수가 재현되고 세 대비 모두 원 p<0.05다. 그러나 이는 고정된 105개 직종의 시계열 불확실성을 평가하며 직종 표본·직종 간 지속적 이질성에 대한 추론을 대체하지 않는다. 이 작은 p값으로 중분류 부트스트랩의 비유의를 무시하지 않는다.

| target                                |   lag |   coefficient |          se |             p |   months |   df |
|:--------------------------------------|------:|--------------:|------------:|--------------:|---------:|-----:|
| female20_24_acquisitions              |     6 |   -1.8433505  | 0.35568669  | 2.0204925e-06 |       73 |   70 |
| female20_24_acquisitions              |    12 |   -1.8433505  | 0.2017665   | 1.4894182e-13 |       73 |   70 |
| female20_24_acquisitions              |    18 |   -1.8433505  | 0.20181112  | 1.5021546e-13 |       73 |   70 |
| male25_29_acquisitions                |     6 |   -1.0668651  | 0.1848976   | 1.9848137e-07 |       73 |   70 |
| male25_29_acquisitions                |    12 |   -1.0668651  | 0.17035864  | 2.6799466e-08 |       73 |   70 |
| male25_29_acquisitions                |    18 |   -1.0668651  | 0.15887297  | 4.1112498e-09 |       73 |   70 |
| age25_29_female_minus_male_employment |     6 |    0.12264275 | 0.01262436  | 1.3121338e-14 |       73 |   70 |
| age25_29_female_minus_male_employment |    12 |    0.12264275 | 0.015819539 | 5.2136718e-11 |       73 |   70 |
| age25_29_female_minus_male_employment |    18 |    0.12264275 | 0.017197958 | 7.1958411e-10 |       73 |   70 |

4. 중분류×월 고정효과도 진단했다. 대부분의 중분류에서 Q5 여부가 동일해 원 Q5 변화가 흡수된다. 실제 식별은 혼합된 2개 중분류의 10개 직종·Q5 3개에만 남는다. 따라서 아래 계수는 추정대상이 바뀐 기술적 대비이며 원래 세 효과를 적절히 통제해 재현한 값으로 해석하지 않고 확증적 p값도 제시하지 않는다.

| target                                |   coefficient |   active_occupations |   active_q5 |   active_families | note                                                                                  |
|:--------------------------------------|--------------:|---------------------:|------------:|------------------:|:--------------------------------------------------------------------------------------|
| female20_24_acquisitions              |      -0.71399 |                   10 |           3 |                 2 | Changed estimand; only mixed-treatment families identify it. No confirmatory p-value. |
| male25_29_acquisitions                |       1.45963 |                   10 |           3 |                 2 | Changed estimand; only mixed-treatment families identify it. No confirmatory p-value. |
| age25_29_female_minus_male_employment |      -0.18939 |                   10 |           3 |                 2 | Changed estimand; only mixed-treatment families identify it. No confirmatory p-value. |

## 학술적 해석

현재 자료가 지지하는 것은 직종별 군집·명세에 조건부인 상대적 취득 약화와 남녀 차이다. 직종군 공통 충격의 구조를 달리하면 유의성이 달라지므로 특정 집단의 감소가 AI 고유 효과라는 주장은 더더욱 불가하다. 산업별 수요, 코로나 회복, 인구·연령 이동, 고용보험 가입 변화와 실제 AI 도입을 분리하지 못한다. 취득은 순신규채용, 상실은 해고가 아니며 고정 기준월 흐름은 취업 확률도 아니다.

중분류 군집은 다른 직종군 간 상관까지 모두 허용하지 못하고, 처리 포함 군집 7개의 한계도 크다. 산업 자료·사업장 수준 충격을 관측한 새 식별 설계가 필요하다. 기본 직종별 부트스트랩과 더 넓은 군집 검정을 함께 보고하고 유의한 것만 선택하지 않는다.

## 방법 근거와 재현

Roodman, MacKinnon, Nielsen and Webb (2019)의 null-imposed wild cluster bootstrap 틀을 참고했다. 방법·가중 분포의 공식 구현 문서는 https://s3alfisc.github.io/fwildclusterboot/reference/boottest.html 이다. 이 분석은 해당 패키지를 호출한 결과가 아니라 직접 구현이며 전체 더미 회귀와 비교했다.

analyze.py, validate_full_refit.py, DESIGN_AND_VALIDATION.json, FULL_DUMMY_BOOTSTRAP_REFIT_CHECKS.json, WILD_BOOTSTRAP_RESULTS.csv, TWO_WAY_CLUSTER_RESULTS.csv, MONTHLY_GAP_HAC.csv, RESIDUAL_CORRELATIONS.csv, FAMILY_MONTH_FE_DIAGNOSTIC.csv, SUMMARY_KO.csv를 보존했다. 원 입력은 이전 47번 연령별 분석 파일과 45번 공식 직종 연결표다.