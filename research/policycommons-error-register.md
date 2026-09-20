# Policy Commons 정제 오류 등록부

다음 오류 유형은 이후 모든 데이터셋에서 자동 회귀검사와 층화 표본검사로 재확인한다.

1. `Published in` 또는 장소만으로 국가를 정하지 않는다. 발행기관, Source, 기관 계층, 문서의 정책 관할을 함께 확인한다. Kosovo처럼 장소와 발행기관이 충돌하면 발행기관 관할을 우선한다.
2. HKG는 국가 분석에서 CHN으로 통합하되 원래 CSV/RIS 값은 보존한다.
3. EU 및 국제기구, 지역 네트워크의 본부·저장소 국가는 국가 발행으로 세지 않는다. 다만 국가별 지사, 국가 위원회 또는 명시적 국가 정책보고서는 국가 귀속을 허용한다.
4. 다국적 민간기업은 자동 삭제하지 않는다. 국가 지사·법인 또는 국가 정책 대응 문서인지 확인하고, 불확실하면 검토대기로 남긴다.
5. standalone agenda, 학술 conference/workshop/symposium proceedings, 채용·행사·학위·학술 단독 문서는 제외한다. 회의록, 정책, 전략, 보고서, 제출서류가 결합된 substantive bundle은 유지한다.
6. AI 용어가 제목·초록·키워드에 없다는 이유로 Non-AI로 판정하지 않는다. Policy Commons 검색은 본문 색인과 검색 provenance를 포함하므로 명백한 대체 의미만 제외한다.
7. 문서 유형이 video, image, audio, patent, dataset인 경우 정책보고서가 아니면 제외한다. 원문 페이지에서 유형을 확인한다.
8. CSV와 RIS는 정규화된 Policy Commons ID와 artifact ID로 연결한다. 제목·행 순서·파일명은 연결키로 사용하지 않는다.
9. 모든 수정은 원천 마스터를 보존하고, 제외 행·규칙 ID·근거·실행 시드를 별도 기록한다. 신규 오류는 failing example과 유지되어야 하는 counterexample을 함께 등록한다.
10. 국가별 AI 정책 관심도 분석의 발행기관 범위는 정부 부처·산하기관·지방정부·공공 연구소·정부출연 연구기관과 정부 연구과제를 수행하는 기업 연구소를 포함한다. 본사나 지사가 특정 국가에 있다는 사실만으로는 충분하지 않다. 명백한 다국적 민간기업의 일반 사업·제품·홍보 문서는 국가 정책 관심도의 대표 자료로 보지 않고 분석 행에서 제외한다. 단, 국가 정부의 위탁·출연·정책과제 수행 증거가 있으면 별도 근거를 기록하고 포함한다.

## Policy Commons 원문 근거를 사용한 기관·국가 귀속 기준

### 포함하는 발행기관

- 정부 부처, 정부 산하기관, 지방정부, 공공 연구소와 국책 연구기관은 `issuer_country`를 해당 국가로 귀속한다. 예를 들어 [Government of Sweden 발행 AI 규제 대응 문서](https://policycommons.net/artifacts/44770242/internetstiftelsens-response-to-ai-regulation-adaptations-sou-2025101/45669071/)는 발행기관과 국가 정책 맥락이 모두 스웨덴으로 확인된다.
- 정부가 직접 발행하거나 정부 산하 기관이 발행한 경우, `Published in`이 도시명이어도 발행기관 관할을 우선한다. [Government of Canada 출처가 명시된 의회 문서](https://policycommons.net/artifacts/4252309/evidence-standing-committee-on-canadian-heritage/5061382/)는 Ottawa라는 장소값보다 Government of Canada와 캐나다 의회 소속 정보를 우선한다.
- 국가 정부가 지원한 공공 연구기관·대학·연구소의 정책·기술 보고서는 해당 국가의 정책 관심도 자료로 유지한다. [캐나다 정부 연구기관의 AI 특허 landscape 보고서](https://policycommons.net/artifacts/54150589/processing-artificial-intelligence/55048942/)는 캐나다 기관과 캐나다 정책·기술 맥락이 명시되어 있다.

### 제외하거나 별도 검토하는 발행기관

- 다국적 민간기업은 본사 또는 지사가 특정 국가에 있다는 이유만으로 국가 정책 관심도를 대표한다고 보지 않는다. 예를 들어 [Abbott (United States) 자료](https://policycommons.net/artifacts/14004974/beyond-intervention/)는 미국 본사의 다국적 민간기업 자료이므로 `USA` 출처 정보는 보존하되 주 분석 문서·국가 행에서는 제외한다.
- 다만 다국적 기업의 국가별 연구소가 정부 위탁·출연 연구를 수행하거나 국가 정책과 직접 연결되는 근거가 원문에 있으면 `government_research_evidence`를 기록하고 포함할 수 있다.
- 국제기구와 EU 기관은 본부 위치나 저장소 위치를 국가 발행으로 변환하지 않는다. [European Union Fourth Framework Programme](https://policycommons.net/artifacts/294457/the-fourth-framework-programme-for-reserach-and-technological-development/1183995/)처럼 Rights와 저자가 European Union으로 명시된 자료는 EU·초국가 문서로 별도 분류한다.
- [EUAA의 AI·로보틱스 문서](https://policycommons.net/artifacts/2024412/1/2776854/)처럼 `Published in Malta`가 표시되어도 발행기관이 European Union Agency for Asylum이면 몰타 국가 문서로 자동 귀속하지 않는다. 국가 지사 또는 국가별 정책 대상이 명확한 경우에만 국가 귀속을 검토한다.

### 적용 순서

1. Policy Commons 원문에서 발행기관, Source, 기관 계층, Rights, Published in을 확인한다.
2. 발행기관이 정부·공공·국책 연구기관인지 판정한다.
3. 민간기업이면 정부 연구과제 수행 증거를 확인한다.
4. 국제기구·EU·지역 네트워크이면 국가 소재지와 국가 정책 대상 여부를 분리한다.
5. `issuer_country`, `country_scope_class`, `government_research_evidence`, `country_decision_source`를 기록한다.
6. 근거가 부족하면 삭제하지 않고 `manual_review`로 보존한다.

## 최근 회귀검사 항목

- 국가 분류 단위와 문서-국가 1:1 행을 분리 보고
- Kosovo, Ottawa/Canada, HKG/China, EU·국제기구 충돌 테스트
- agenda substantive-bundle 예외 테스트
- 국제·지역 네트워크와 국가 지사의 구분
- 메타데이터 AI 용어 부재의 비배제 원칙
- 접근 불가 페이지는 정답으로 간주하지 않고 `unverifiable`로 기록
