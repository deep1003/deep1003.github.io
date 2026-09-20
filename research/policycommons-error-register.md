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

## 최근 회귀검사 항목

- 국가 분류 단위와 문서-국가 1:1 행을 분리 보고
- Kosovo, Ottawa/Canada, HKG/China, EU·국제기구 충돌 테스트
- agenda substantive-bundle 예외 테스트
- 국제·지역 네트워크와 국가 지사의 구분
- 메타데이터 AI 용어 부재의 비배제 원칙
- 접근 불가 페이지는 정답으로 간주하지 않고 `unverifiable`로 기록
