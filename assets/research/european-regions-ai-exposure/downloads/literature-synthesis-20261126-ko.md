# 유럽 AI 노출과 고용 연구의 핵심 결과와 최근 연구 비교

검토일 2026년 11월 26일. 기존 계산 결과를 재평가한 종합이며 원고는 수정하지 않았다. 세 결과는 학술적 의미에 따라 선정했으며 세 개의 확정적 인과효과를 의미하지 않는다.

## 1. AI 노출은 생산성이 높은 산업에 집중된다

2022년 EU27의 511개 국가×산업 셀에서 국가·산업 고정효과와 2022년 취업자 가중치를 적용하면 THAIE 0.01 증가와 취업자 1인당 실질 부가가치 6.60% 증가가 관련된다. 명목 95% 신뢰구간은 3.15~10.15%, p=.000653, 부분 가중 R²=.0538이다. 사후 검토한 320개 계수 집합에서 BH q=.0427이지만 Holm p=.2076이다. 다중 검정에 강건한 확정적 발견으로 표현할 수 없다. 콘텐츠 노출 E를 조건으로 한 추가 설명력도 입증되지 않았다.

이는 지역 패널이 아닌 국가×산업 횡단면이다. 2025년 기술 벤치마크를 2022년 구성에 적용한 노출도이며 실제 AI 도입 효과가 아니다. Brynjolfsson·Li·Raymond(2025)의 고객지원 생산성 개선은 도입 접근성을 이용한 업무 수준 연구이므로 우리의 6.60%와 크기를 비교할 수 없다. Humlum·Vestergaard(2026)의 업무 재편과 평균 소득·시간의 초기 무효과 역시 생산성과 고용이 서로 다른 조정 경로임을 보여준다.

정책적 함의는 고노출 산업을 일괄적인 고용 위험 업종으로 분류하기보다 도입, 업무 재설계, 숙련 형성을 함께 측정하는 것이다. 생산성 개선이 우리 자료에서 인과적으로 입증됐다는 주장은 하지 않는다.

## 2. 노르웨이 고노출 청년층에 상대적 약화 신호가 있다

동일한 8개 카운티의 205개 카운티×직업 셀, 네 연령·성별 집단의 고정된 2022년 조화평균 가중치를 사용했다. Q5와 Q1~Q4를 비교하며 25세 미만과 55~64세를 비교한다. 직업은 2자리 대리 분류이며 전국 2022년 11월의 3자리 직업 구성으로 THAIE를 연결했다. 노르웨이 전체 또는 유럽 전체의 효과로 일반화할 수 없다.

실제 측정월인 2022년 11월을 기준으로 2024년 11월 청년 DID는 남성 -11.10%, 여성 -5.26%이다. 청년과 고연령층 간 DDD는 남성 -9.71%, 여성 -5.08%이다. 2025년 11월에는 각각 청년 DID -15.34%, -9.05%, DDD -13.55%, -7.57%이다. 2025년 통계 변경 이후 구간은 별도로 해석한다. 변화율은 100×(exp(계수)-1)이며 퍼센트포인트가 아니다.

2024년 4분기 남성 청년 DID의 분기별 wild-bootstrap p=.0133이지만 15개 분기 Holm p=.1995이다. 남성 DDD도 .0158에서 .2370으로 바뀐다. 따라서 방향성 신호는 있지만 다중 검정에 강건한 AI의 인과적 대체 효과로 볼 수 없다. 여성·남성 점추정치 차이만으로 성별 효과 차이를 확정하지 않는다.

EconPol 61의 독일 청년층 상대적 약화, 프랑스의 청년 신규 채용 둔화, 미국 Canaries의 초년 경력 약화와 방향상 관련된다. 그러나 연령, 노출 점수, 기준시점, 모집단, 신규 채용 흐름과 재직자 고용량이 다르므로 재현이라고 부르지 않는다. 노르웨이의 Facius·Iacono 및 Hernæs·Kostøl은 강건한 청년 대체를 확인하지 못했다. 이 반대 증거를 함께 제시해야 한다.

정책은 청년 채용·수습·훈련 경로를 감시하고 멘토링과 AI 활용 교육을 평가하는 방식이 적절하다. 단기 계수만으로 고용 손실 규모를 예측하거나 특정 성별 피해를 확정할 수 없다.

## 3. 추정 대상과 시간창이 결론을 바꾼다

같은 205개 셀과 가중치의 가중 로그 비교에서 2022년 11월→2025년 11월 청년 Q5 상대 변화는 남성 -17.60%, 여성 -11.10%이다. 시간창을 2021~2022년 평균→2023~2024년 평균으로 바꾸면 +3.49%, +2.05%로 바뀐다. 카운티×시점 통제를 추가하면 +3.33%, +1.29%이다. 끝점·사전 기준·사후 평균이 함께 달라지는 비교이며 기준월 하나의 순수 효과가 아니다. 분기별 동적 모형의 계수와 이 단순 끝점 계수도 동일한 추정량이 아니다.

순차 분해는 시간창이 부호 변화의 주요 항목임을 보여주지만 순서 의존적 회계 분해이지 인과적 기여도 분해가 아니다. Facius·Iacono의 위약 시점 민감성, Hernæs·Kostøl의 전체 직업군 무효과, Humlum·Vestergaard의 도입 연계 결과는 단순 고노출 추세만으로 AI 대체를 귀속하기 어렵다는 해석과 부합한다.

정책 평가는 사전에 기간·표본·가중치·다중 검정 범위를 정하고, 고용량과 채용·이직 흐름, 실제 도입 시점을 연결해야 한다. 동적 경로, 사전 추세, 2025년 통계 변경 전후를 함께 공개하는 것이 우선이다.

## EconPol 61을 직접 옮길 수 없는 이유

독일은 전일제 20~64세 사회보험 행정자료의 2013Q1~2026Q1, 연속 노출도 Poisson 연령 DDD이다. 도제는 제외된다. 그림의 2022Q3 기준과 4분기 이동평균은 우리의 실제 2022년 11월 관측값 기준과 다르다. EU-LFS는 2021Q1~2024Q4이며 최근 12개월 신규 채용을 별도로 측정한다. 우리는 고용량, 2자리 직업 대리 노출도, 25세 미만 대 55~64세의 선택된 지역 패널이므로 수치의 직접 비교는 부적절하다. 보고서의 고용 총량과 채용의 구분을 연구 설계에 반영할 가치가 크다.

## 문헌 및 재현 경로

- Falck; Fuest; Guo (2026-11). AI and the Labor Market Productivity Driver or Job Killer. https://www.ifo.de/en/econpol/publications/2026/working-paper/ai-and-labor-market-productivity-driver-or-job-killer
- Facius; Iacono (2026). Labour Market Consequences of Generative AI Early Evidence from Norway. https://www.ifo.de/en/cesifo/publications/2026/working-paper/labor-market-consequences-generative-ai-early-evidence-norway
- Hernæs; Kostøl (2026-06). Has AI Widened Employment Gaps Tracking Early-Career Employment by Occupational Exposure in Norway. https://www.iza.org/publications/dp/18767
- Humlum; Vestergaard (2026-03-13). Still Waters Rapid Currents Early Labor Market Transformation under Generative AI. https://www.andershumlum.com/s/chatbots_260313.pdf
- Palladino; Bergeaud; Bertheau; Bunel; Degos (2026-10). Occupational exposure to generative AI firm adoption and labor market dynamics in France. https://www.banque-france.fr/en/publications-and-statistics/publications/generative-ai-first-changes-labour-market-are-affecting-young-people
- Brynjolfsson; Chandar; Chen (2026-08). Canaries in the Coal Mine Six Facts about the Recent Employment Effects of Artificial Intelligence. https://digitaleconomy.stanford.edu/app/uploads/2026/08/Canaries_August2026.pdf
- Brynjolfsson; Li; Raymond (2025-02). Generative AI at Work. https://doi.org/10.1093/qje/qjae044

기존 계산 출처는 paper_evidence_review_20261124_v1, norway_did_bridge_20261126, norway_dynamic_nov2022_20261126이다. 문헌 비교표에는 자료 범위, 방법, 한계와 적용 범위를 별도로 기록했다.
