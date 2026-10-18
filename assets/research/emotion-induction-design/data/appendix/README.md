# 연구 데이터 별첨

2026-10-18. 감정·인지평가 축 구성 문장 전체와 실제 사용한 KoBBQ 2,000문항이다. 모델 재측정이나 문장 수정은 하지 않았다.

## 축 구성 자료

원래 일곱 축의 70쌍과 CN의 10쌍, 총 80쌍·160문장이다. 각 축은 구성용 train 6쌍, 보류 검증용 heldout 4쌍이다. positive/negative는 축의 목표/대조 방향이며 감정의 긍정·부정 정서가를 뜻하지 않는다. FA는 공포와 불안을 합친 기존 축이고 CN은 인지적 평가의 대조 개념이다. 아직 측정하지 않은 후속 실험의 혐오 프롬프트는 이 자료에 포함하지 않았다.

axis_pairs.csv/json은 문장 쌍당 한 행이다. axis_sentences.jsonl은 문장당 한 행(160행)이며 system_content는 실제 시스템 메시지 내용이다. 원래 문장 JSON도 그대로 보존했다. Qwen chat template와 add_generation_prompt=True를 적용하고 답변 시작 직전 상태를 측정했다. token-level 전체 직렬화는 이 텍스트 파일이 아니라 원래 모델 tokenizer 설정에 따른다.

## KoBBQ 자료

원실험 139문항과 공식 인물·배경 변형 1,861문항이다. 2,000개 고유 문항은 91개 범주·템플릿 군집을 공유한다. 원자료 context/question/choices/answer/biased_answer를 모두 공식 캐시와 대조했다. 인물이나 배경을 새로 생성한 자료가 아니다. original CSV는 바이트 단위로 보존했다.

- CSV(UTF-8 BOM)는 엑셀에서 한글을 바로 열기 위한 정규화 표이다. choices는 JSON 문자열이며 choice_1/2/3 열도 제공한다.
- JSON/JSONL은 choices를 실제 배열로 저장하고 결측값은 null로 보존한다.
- Parquet(Zstandard)은 선택지 배열과 자료형을 유지하는 압축 분석용 형식이다.
- XLSX는 문항·축 문장·변수 설명을 읽고 필터링하는 용도다.
- kobbq_browser.html은 네트워크 없이도 검색·범주·원실험/추가 문항 필터와 페이지 단위 열람을 제공한다.
- 홈페이지의 대표 예시는 각 범주의 원실험 첫 순번 문항과 같은 anchor에 연결된 추가 문항(없으면 첫 추가 문항)으로 고정했다. 모델 반응을 보며 고르지 않았다.

origin, anchor_id, sequence, cluster, family, polarity, similarity는 이 연구의 선정·확장 추적 열이다. similarity는 문자 유사도 기반 후보 정렬값이며 응답 효과나 의미 벡터의 코사인이 아니다. biased_answer는 원자료 표기이며 모호 문항의 정답(answer=알 수 없음)과 구분한다. label_annotation과 원자료의 결측 필드는 임의 해석·대치하지 않았다. 선택지 순서 3개는 시행 시 순환하며 문항 파일에는 기준 순서를 저장한다. 24,000행 응답 확률은 문항 자체와 다른 데이터다.

## 출처와 이용 조건

NAVER AI Lab, KoBBQ (TACL 2024). https://huggingface.co/datasets/naver-ai/kobbq 및 https://github.com/naver-ai/KoBBQ
데이터 카드의 MIT 표기와 저장소 LICENSE를 2026-10-18 확인했다. LICENSE_KoBBQ.txt의 원문 저작권·허가문을 함께 제공한다. 원자료 저작권은 NAVER Cloud Corp.에 있다. 연구용 부분집합과 추적 열을 별도로 표시했다. 새 연구자의 이용은 이 라이선스와 출처 표기를 유지해야 한다.


## 행동 측정 자료

behavior_trials_24000.csv.gz는 24,000행 원시 응답 확률 CSV를 그대로 gzip 압축한 별도 파일이다. behavior_trials_24000.parquet은 같은 수치의 분석용 압축 형식이다. item·condition·rotation으로 문항과 연결한다. 기존 139문항에는 세 원시 logits 및 전체 logsumexp가 저장되지 않아 해당 열이 결측이고, 신규 1,861문항에는 기록되어 있다. 확률 열은 전체 24,000행에 존재한다.
