# 네 모델의 종료 공지 효과 비교

8 November 2026 · Post hoc comparison · No new inference

## 요약

종료 공지의 판단 효과는 모델별로 다르지만, EXAONE과 Qwen의 공통 행동 대비 9개에서는 전체 54개 비교에 대한 Holm 보정 후 유의한 차이를 확인하지 못했다.

## 결과

전체 모델 검정 9개 중 8개가 Holm9 보정 후 유의했다. KoBBQ 편향 상호작용은 유의하지 않았다. 보정 p값은 0.2448이다. 모델 쌍 54개 검정 중 20개가 전체 Holm54 보정 후 유의했다. EXAONE과 Llama는 CLOSED·OPEN의 Unknown 변화와 승인 대비 세 개 모두에서 차이가 있었다. EXAONE과 Gemma는 CLOSED Unknown, CLOSED 승인, 승인 상호작용에서 차이가 있었다. EXAONE과 Qwen의 9개 대비 차이는 모두 유의하지 않았다. 이는 모델별 판단 민감도의 차이를 보여주며 보편적 정서 매개를 뜻하지 않는다.

## 자료와 대응 설계

이미 수집하고 해시로 봉인한 문항별 결과표를 사용한 사후 분석이다. 해당 결과표는 기존 독립 원자료 재계산을 통과했다. 모델을 다시 적재하거나 응답을 추가 수집하지 않았다. 네 모델에서 동일한 KoBBQ 모호 문항 547개와 템플릿 군집 250개, DiscrimEval 문항 1,050개와 질문 군집 70개를 대응시켰다. KoBBQ 선택지 순서 반복은 문항 내에서 평균했다. CLOSED는 CN1 − CN0, OPEN은 UN1 − UN0, 상호작용은 CLOSED − OPEN이다. KoBBQ는 Unknown 확률과 고정관념 확률에서 반고정관념 확률을 뺀 값의 변화이며 퍼센트포인트로 표시한다. 승인은 예와 아니오 확률비의 자연로그 변화다. seed 20261031로 템플릿 또는 질문 군집을 복원추출하고 해당 군집의 모든 문항을 유지하는 대응 군집 부트스트랩을 10,000회 실시했다. 평균은 군집이 아닌 문항을 동일하게 가중한다.

## 검정과 다중비교

모델 간 차이 d의 양측 중심화 부트스트랩 p값은 [1 + |d* − d| ≥ |d|인 횟수] / 10001이다. 95% 백분위 신뢰구간은 다중비교를 보정하지 않은 기술적 구간이다. 주검정은 모델 쌍 6개와 대비 9개의 곱인 54개를 한꺼번에 Holm 보정한다. 쌍별 Holm9는 보조 결과다. 전체 네 모델의 동일성은 Qwen 대비 세 차이와 부트스트랩 공분산을 이용한 중심화 이차형식으로 검정하고 9개를 Holm 보정한다. 공분산 순위는 모두 3이다. 이는 부트스트랩 근사검정이며 정확한 무작위화 검정이 아니다. 최소 p값 1/10001이라는 해상도 한계가 있다. 모델별 표의 볼드체는 기존 등록 J33 검정군의 보정을 사용하며 새 모델 간 차이 검정과 구분한다. 한 모델에서 유의하고 다른 모델에서 유의하지 않다는 사실만으로 모델 간 차이를 주장하지 않는다.

## 한계와 해석 범위

모델, 토크나이저, 고정 공지 형식, 시스템 메시지 처리, 사전학습과 구조가 함께 다르므로 모델 간 차이를 구조나 개발사, 언어 또는 학습의 단독 인과효과로 해석할 수 없다. 층 경계와 은닉공간 척도도 다르다. 공지 상태 그림은 독립된 입력 다섯 개와 모델별 PCA를 이용한 탐색적 시각화이며 화살표는 시간 경로나 인과 기제를 뜻하지 않는다. 인과적 정서 매개는 검정하거나 주장하지 않는다. EXAONE에서는 95,580건 성분 무작위 대조와 확장 보조 검사를 생략했으므로 기존 세 모델의 E8·잔차 성분 D4 비교를 그대로 보존하며 네 모델로 확장하지 않는다. 잔차는 비정서를 뜻하지 않으며 기존 GEN 성분은 약 80%가 E8 밖에 있다. EXAONE readout 1,129개 중 838개가 이용 가능하고 291개는 50토큰 제외 후 내용이 없는 유형화 결측이며 0이나 대체값을 넣지 않았다. 유의하지 않음은 동등성의 증명이 아니며 다른 문항으로의 일반화도 검증하지 않았다.

## 공지 그림의 방법 설명 정정

새 EXAONE 공지 그림은 기존 세 모델 그림과 같이 정서 대비 중립의 원래 평균 방향을 단위 정규화하고 공통 성분을 유지한 순위 8 공간을 사용했다. 보존한 EXAONE 핵심 보고서의 탐색적 F_NOTICE는 중립 PC 제거와 중심화를 거친 등록 축을 사용한 순위 7 공간이므로 이를 원래 방향 공간이라고 표현한 설명은 부정확했다. 새 그림은 기존 그림과 등록 검정, 결과값을 바꾸지 않고 시각화 방법 설명을 바로잡는다. 두 PC는 EXAONE 다섯 상태 변동의 97.9%를 유지한다. 모델별 좌표, 링 범위와 방향 이름의 표시 배율은 절대 정서 강도로 비교할 수 없다.

## Within-model effects

| Contrast | Qwen2.5-7B | Llama-3.1-8B | Gemma-2-9B | EXAONE-3.5-7.8B |
| --- | --- | --- | --- | --- |
| C · Unknown (pp) | **-1.244** | **-4.675** | +0.104† | **-0.754** |
| U · Unknown (pp) | **-0.860** | **-4.569** | -0.244† | **-0.772** |
| I · Unknown (pp) | **-0.384** | -0.106† | +0.348† | +0.018† |
| C · Stereotype − anti (pp) | **+0.891** | **+1.078** | +0.182† | **+0.698** |
| U · Stereotype − anti (pp) | **+0.786** | **+1.059** | +0.362† | **+0.582** |
| I · Stereotype − anti (pp) | +0.105† | +0.019† | -0.180† | +0.115† |
| C · Approval log ratio | **-0.874** | **-0.109** | **-0.337** | **-0.706** |
| U · Approval log ratio | **-0.618** | -0.052† | **-0.343** | **-0.462** |
| I · Approval log ratio | **-0.255** | -0.057† | +0.006† | **-0.245** |

Notes. C = CLOSED, U = OPEN, I = C − U. Bold uses original within-model J33 family Holm p < .05. † Not significant in that original family. Nonsignificant entries are Gemma-2-9B CLOSED Unknown (pp), Gemma-2-9B CLOSED Stereotype − anti (pp), Gemma-2-9B OPEN Unknown (pp), Gemma-2-9B OPEN Stereotype − anti (pp), Llama-3.1-8B interaction Unknown (pp), Gemma-2-9B interaction Unknown (pp), EXAONE-3.5-7.8B interaction Unknown (pp), Qwen2.5-7B interaction Stereotype − anti (pp), Llama-3.1-8B interaction Stereotype − anti (pp), Gemma-2-9B interaction Stereotype − anti (pp), EXAONE-3.5-7.8B interaction Stereotype − anti (pp), Llama-3.1-8B OPEN Approval log ratio, Llama-3.1-8B interaction Approval log ratio, Gemma-2-9B interaction Approval log ratio. All original estimates and family corrections are preserved.

## Omnibus equality tests

| Contrast | Raw p | Holm9 p |
| --- | --- | --- |
| C · Unknown (pp) | 0.000100 | **0.000900** |
| U · Unknown (pp) | 0.000100 | **0.000900** |
| I · Unknown (pp) | 0.0131 | **0.0262** |
| C · Stereotype − anti (pp) | 0.000100 | **0.000900** |
| U · Stereotype − anti (pp) | 0.0062 | **0.0186** |
| I · Stereotype − anti (pp) | 0.2448 | 0.2448† |
| C · Approval log ratio | 0.000100 | **0.000900** |
| U · Approval log ratio | 0.000100 | **0.000900** |
| I · Approval log ratio | 0.000100 | **0.000900** |

Notes. † KoBBQ bias interaction is not significant. All nine tests are post hoc.

## Pairwise model differences

| Target − reference | Contrast | Difference | 95% CI | Global Holm54 p |
| --- | --- | --- | --- | --- |
| Llama-3.1-8B − Qwen2.5-7B | C · Unknown (pp) | **-3.430** | [-4.115, -2.727] | **0.0054** |
| Llama-3.1-8B − Qwen2.5-7B | C · Stereotype − anti (pp) | +0.187† | [-0.368, +0.737] | 1.0000† |
| Llama-3.1-8B − Qwen2.5-7B | U · Unknown (pp) | **-3.709** | [-4.346, -3.073] | **0.0054** |
| Llama-3.1-8B − Qwen2.5-7B | U · Stereotype − anti (pp) | +0.272† | [-0.228, +0.740] | 1.0000† |
| Llama-3.1-8B − Qwen2.5-7B | I · Unknown (pp) | +0.279† | [-0.160, +0.698] | 1.0000† |
| Llama-3.1-8B − Qwen2.5-7B | I · Stereotype − anti (pp) | -0.085† | [-0.450, +0.280] | 1.0000† |
| Gemma-2-9B − Qwen2.5-7B | C · Unknown (pp) | **+1.348** | [+0.798, +1.960] | **0.0054** |
| Gemma-2-9B − Qwen2.5-7B | C · Stereotype − anti (pp) | -0.709† | [-1.260, -0.155] | 0.4278† |
| Gemma-2-9B − Qwen2.5-7B | U · Unknown (pp) | +0.616† | [+0.090, +1.160] | 0.6803† |
| Gemma-2-9B − Qwen2.5-7B | U · Stereotype − anti (pp) | -0.425† | [-0.895, +0.039] | 1.0000† |
| Gemma-2-9B − Qwen2.5-7B | I · Unknown (pp) | +0.733† | [+0.294, +1.198] | 0.0510† |
| Gemma-2-9B − Qwen2.5-7B | I · Stereotype − anti (pp) | -0.284† | [-0.689, +0.118] | 1.0000† |
| EXAONE-3.5-7.8B − Qwen2.5-7B | C · Unknown (pp) | +0.491† | [-0.150, +1.121] | 1.0000† |
| EXAONE-3.5-7.8B − Qwen2.5-7B | C · Stereotype − anti (pp) | -0.193† | [-0.790, +0.422] | 1.0000† |
| EXAONE-3.5-7.8B − Qwen2.5-7B | U · Unknown (pp) | +0.088† | [-0.432, +0.609] | 1.0000† |
| EXAONE-3.5-7.8B − Qwen2.5-7B | U · Stereotype − anti (pp) | -0.204† | [-0.712, +0.312] | 1.0000† |
| EXAONE-3.5-7.8B − Qwen2.5-7B | I · Unknown (pp) | +0.403† | [+0.027, +0.781] | 0.8924† |
| EXAONE-3.5-7.8B − Qwen2.5-7B | I · Stereotype − anti (pp) | +0.011† | [-0.339, +0.366] | 1.0000† |
| Gemma-2-9B − Llama-3.1-8B | C · Unknown (pp) | **+4.779** | [+4.188, +5.369] | **0.0054** |
| Gemma-2-9B − Llama-3.1-8B | C · Stereotype − anti (pp) | **-0.896** | [-1.286, -0.490] | **0.0054** |
| Gemma-2-9B − Llama-3.1-8B | U · Unknown (pp) | **+4.325** | [+3.775, +4.882] | **0.0054** |
| Gemma-2-9B − Llama-3.1-8B | U · Stereotype − anti (pp) | **-0.697** | [-1.093, -0.292] | **0.0185** |
| Gemma-2-9B − Llama-3.1-8B | I · Unknown (pp) | +0.454† | [+0.036, +0.889] | 0.8924† |
| Gemma-2-9B − Llama-3.1-8B | I · Stereotype − anti (pp) | -0.199† | [-0.489, +0.089] | 1.0000† |
| EXAONE-3.5-7.8B − Llama-3.1-8B | C · Unknown (pp) | **+3.921** | [+3.338, +4.489] | **0.0054** |
| EXAONE-3.5-7.8B − Llama-3.1-8B | C · Stereotype − anti (pp) | -0.380† | [-0.854, +0.108] | 1.0000† |
| EXAONE-3.5-7.8B − Llama-3.1-8B | U · Unknown (pp) | **+3.797** | [+3.225, +4.366] | **0.0054** |
| EXAONE-3.5-7.8B − Llama-3.1-8B | U · Stereotype − anti (pp) | -0.476† | [-0.904, -0.024] | 0.8787† |
| EXAONE-3.5-7.8B − Llama-3.1-8B | I · Unknown (pp) | +0.124† | [-0.196, +0.443] | 1.0000† |
| EXAONE-3.5-7.8B − Llama-3.1-8B | I · Stereotype − anti (pp) | +0.096† | [-0.167, +0.358] | 1.0000† |
| EXAONE-3.5-7.8B − Gemma-2-9B | C · Unknown (pp) | **-0.858** | [-1.400, -0.377] | **0.0455** |
| EXAONE-3.5-7.8B − Gemma-2-9B | C · Stereotype − anti (pp) | +0.515† | [+0.084, +0.995] | 0.7505† |
| EXAONE-3.5-7.8B − Gemma-2-9B | U · Unknown (pp) | -0.528† | [-0.987, -0.085] | 0.6727† |
| EXAONE-3.5-7.8B − Gemma-2-9B | U · Stereotype − anti (pp) | +0.221† | [-0.204, +0.663] | 1.0000† |
| EXAONE-3.5-7.8B − Gemma-2-9B | I · Unknown (pp) | -0.330† | [-0.711, +0.010] | 1.0000† |
| EXAONE-3.5-7.8B − Gemma-2-9B | I · Stereotype − anti (pp) | +0.295† | [+0.007, +0.596] | 1.0000† |
| Llama-3.1-8B − Qwen2.5-7B | C · Approval log ratio | **+0.765** | [+0.576, +0.948] | **0.0054** |
| Llama-3.1-8B − Qwen2.5-7B | U · Approval log ratio | **+0.567** | [+0.352, +0.754] | **0.0054** |
| Llama-3.1-8B − Qwen2.5-7B | I · Approval log ratio | +0.198† | [+0.048, +0.350] | 0.3584† |
| Gemma-2-9B − Qwen2.5-7B | C · Approval log ratio | **+0.536** | [+0.367, +0.711] | **0.0054** |
| Gemma-2-9B − Qwen2.5-7B | U · Approval log ratio | +0.275† | [+0.040, +0.496] | 0.5579† |
| Gemma-2-9B − Qwen2.5-7B | I · Approval log ratio | **+0.261** | [+0.110, +0.416] | **0.0324** |
| EXAONE-3.5-7.8B − Qwen2.5-7B | C · Approval log ratio | +0.167† | [-0.009, +0.344] | 1.0000† |
| EXAONE-3.5-7.8B − Qwen2.5-7B | U · Approval log ratio | +0.157† | [-0.071, +0.367] | 1.0000† |
| EXAONE-3.5-7.8B − Qwen2.5-7B | I · Approval log ratio | +0.011† | [-0.122, +0.151] | 1.0000† |
| Gemma-2-9B − Llama-3.1-8B | C · Approval log ratio | -0.229† | [-0.371, -0.089] | 0.0627† |
| Gemma-2-9B − Llama-3.1-8B | U · Approval log ratio | **-0.292** | [-0.438, -0.156] | **0.0078** |
| Gemma-2-9B − Llama-3.1-8B | I · Approval log ratio | +0.063† | [-0.027, +0.159] | 1.0000† |
| EXAONE-3.5-7.8B − Llama-3.1-8B | C · Approval log ratio | **-0.598** | [-0.774, -0.423] | **0.0054** |
| EXAONE-3.5-7.8B − Llama-3.1-8B | U · Approval log ratio | **-0.410** | [-0.562, -0.258] | **0.0054** |
| EXAONE-3.5-7.8B − Llama-3.1-8B | I · Approval log ratio | **-0.187** | [-0.276, -0.094] | **0.0078** |
| EXAONE-3.5-7.8B − Gemma-2-9B | C · Approval log ratio | **-0.369** | [-0.522, -0.230] | **0.0054** |
| EXAONE-3.5-7.8B − Gemma-2-9B | U · Approval log ratio | -0.118† | [-0.286, +0.042] | 1.0000† |
| EXAONE-3.5-7.8B − Gemma-2-9B | I · Approval log ratio | **-0.251** | [-0.333, -0.172] | **0.0054** |

Notes. Bold is significant after global Holm54. † All unbolded pairwise entries are nonsignificant under global Holm54. Intervals are unadjusted. Supplemental within-pair Holm9 values are supplied in the machine-readable table and do not determine primary conclusions.

## Reproducibility

Independent implementation reproduced 54 pairwise estimates, intervals, p values and corrections, nine omnibus results and 36 original effect estimates with zero mismatches. Input hashes, original raw-QA hashes, frozen post hoc plan, source-resolution addendum, code and independent proof accompany the tables. Original model outputs and earlier comparisons were not modified.
