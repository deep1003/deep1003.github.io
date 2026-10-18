# MacBook Air handover

## 인수 작업

`EXPERIMENT_PLAN_139.md`를 먼저 읽는다. 작업은 39개가 아니라 **139문항·91군집·8조건·3순서, 총3,336키**다. 현재 Mac에서는 실행하지 않았다. 기존 네 조건 및 12문항 Certainty 결과는 원본으로 보존한다. 새로운 감정 이름은 Fear, Anxiety, Anger, Disgust, Calmness, Sadness, Desperation, Joy이며 Certainty·Uncertainty는 평가 축, FA는 Legacy다.

이 handover는 원래 연구를 대체하지 않는다. 6개 기본 조건과 운영팀 능력 평가를 추가한 2개 조건을 구분한다. 평가 문구를 붙인 결과를 순수 Certainty 효과로 보고하지 않는다. Unknown 감소를 정답률 향상으로 표현하지 않는다.

## 파일 배치

압축파일을 새 작업 폴더에 풀고 그 폴더를 작업 루트로 사용한다. 이전 Mac의 절대 경로를 만들 필요가 없다.

- `EXPERIMENT_PLAN_139.md` 전체 계획과 8개 system prompts
- `inputs/protocol.json` 표본·모델·대비·실행 경계
- `inputs/prompts_8.json` 공백·줄바꿈 포함 실제 system 원문과 해시
- `inputs/items_139.csv` 원본 139문항
- `inputs/analysis_splits.csv` 개발12·신규127·군집비중첩119 구분
- `inputs/prompt_lengths.csv` 실제 문자 수와 tokenizer 길이
- `inputs/axes_L14.npz` 고정 10개 주축 및 Legacy FA
- `inputs/anchors_*.json` 축 구축 원문과 분할
- `cache/original/` 기존 네 조건1,668키 및 L14 상태
- `cache/cn12/` 기존12문항 Certainty72키 및 L14 상태
- `cache/system_tokens_L14/` 기존6개 system-only 추적
- `reference_code/pilot_runner_frozen.py` 이전 실행 원형, 실행 대상 아님
- `measurement.py` 원형에서 변경 없이 복사한 측정 함수
- `run_air.py` 상대 경로 기반 실행·재개·검증·구간 계산
- `certainty_uncertainty_139_air.ipynb` 계획과 저장 결과 확인용 노트북
- `CHECKSUMS.json` 입력·캐시·측정 코드 해시

## 실행 전에 할 일

1. 새 폴더에 압축을 풀고 파일 해시를 검증한다. 원래 폴더에 덮어 풀지 않는다.
2. Apple Silicon 여부, 통합 메모리, 여유 디스크 및 다른 모델 프로세스를 확인한다. 32GB급 미만이면 FP32 기준 실행을 시작하지 않는다. 32GB급도 로딩 성공을 보장하지 않는다.
3. 프로젝트 전용 Python3.13 환경을 만들고 `requirements-reference.txt`를 설치한다. 기준 transformers는 개발 버전이므로 기록된 git commit으로 설치한다. 설치에 실패하면 임의 최신 버전으로 대신 실행하지 않는다.
4. 정확한 모델 revision을 로컬에 준비한다. 기본 실행기는 자동 다운로드하지 않는다. 가중치는 zip에 없다.
5. 전처리·선택지·모델 입력 생성은 `measurement.messages`의 원형을 유지한다. 실제 숫자1·2·3의 token ID는16·17·18인지 확인한다. tokenizer·chat template가 달라지면 재사용을 중단하고 보고한다.
6. 기본 검증을 실행한다. 이 단계는 모델 추론·이미지 표시를 하지 않는다.

```bash
python run_air.py
```

기대 출력은 items139, clusters91, conditions8, target3336, cached1740, new_required1596이다. 이 검증은 추론 성능과 수치 일치까지 보증하지 않는다.

## 모델 준비 명령

아래 명령은 수신 MacBook Air에서만, 디스크·메모리 확인 후 실행한다.

```bash
python -m pip install -r requirements-reference.txt
hf download Qwen/Qwen2.5-7B-Instruct --revision a09a35458c702b33eeacc393d103063234e8bc28
```

## 실행과 백그라운드 관리

입력과 런타임 확인 후에만 명시적으로 시작한다.

```bash
python -u run_air.py --execute > run.log 2>&1
```

위 명령 자체는 포그라운드다. 백그라운드 실행을 맡는 Codex는 같은 명령을 `subprocess.Popen(..., start_new_session=True)`로 한 번만 시작하고 실제 PID·명령·시작 시각을 새 `controller.json`에 기록한다. 새 스레드의 heartbeat는 정상 진행 시 조용히 유지하고, 완료·확인된 오류·필요한 사용자 조치에만 알린다. 이전 Mac의 PID나 자동화를 재사용하지 않는다. notebook에서 별도 실행 커널을 동시에 만들지 않는다.

`results/new_trials.csv`를 매 키 저장하며 동일 명령은 저장된 키를 건너뛴다. 재개 전 실제 프로세스가 종료되었는지 확인하고 `writer.lock`을 존중한다. 멈춰 있는 동일 프로세스가 있으면 중복 실행하지 않는다. 실험 도중 표본·문구·축·선택 기준을 바꾸지 않는다.

기준 실행은 기존1,740키를 보존하여 재사용하고 새1,596행만 측정한다. 별도로 새 system-only2개를 추론한다. 메모리 부족 시 FP16·4bit·더 작은 모델로 자동 전환하거나 새 결과를 기존 FP32 캐시에 섞지 않는다. 해당 경우 실행 제약과 별도 실험 대안을 사용자에게 보고한다.

## 분석과 최종 인수 기준

실행기는 모든 목표 키가 모인 다음 세 순서의 문항별 평균과 대응 군집 bootstrap10,000회의 점별95%구간을 계산한다. 전체139·신규127·군집비중첩119를 모두 보고하고 유의한 집합만 선택하지 않는다. p값은 자동 계산하지 않는다. 계획서의 새3대비 검정군과 구현이 고정되기 전에는 p값을 덧붙이지 않는다. 원래 Holm3 결과를 새 방법으로 교체하지 않는다.

```bash
python run_air.py --analyze-only
```

이 명령은 저장된 신규1,596행이 모두 있을 때만 사용한다. 모델은 다시 불러오지 않는다. 산출물은 `behavior_8_conditions.csv`, `alignment_8_conditions.csv`, `system_token_alignment.csv`, `summary.json`, `validation.json`이다. 감정축 출력은 총36,696행이다.

완료 보고 전 다음을 별도 읽기 전용 검증으로 확인한다.

- 3,336키·중복0·문항별24키·139문항·91군집
- 선택지배정, 확률유한성·합1, 신규rawlogits/full logsumexp 재구성
- NPY·축·원자료·입력·코드 해시와 보존된 기존 결과
- 전체139 및 군집비중첩119의 Unknown·8감정축·2평가축 변화95%구간
- system-only 위치와 전체질문 뒤 위치의 구분, 확정성과 능력 평가의 구분
- 주요forest plot·카테고리표·보고서·저장출력노트북의 수치일치

그래프와 보고서의 최종 출판용 레이아웃, 카테고리별 표 및 새 검정군 p값은 계획서에 따라 수신 Codex가 저장된 결과로 작성한다. 원자료가 완료되기 전에 결과를 채우지 않는다. fresh smoke는 코드·입출력 검증만 하며 이미지나 그래프를 화면에 출력하지 않는다. MacBook Air에서 완료한 뒤에도 홈페이지에 결과를 자동 게시하지 말고 결과 파일과 한계를 먼저 보고한다. 2,000문항 자동 확장은 하지 않는다.

## 다음 Codex에게 그대로 전달할 메시지

> 이 폴더의 EXPERIMENT_PLAN_139.md와 HANDOVER_MACBOOK_AIR.md를 읽고 139문항·8조건 실험을 인수하세요. 원래 결과·축·문항·문구는 보존하세요. 먼저 파일 해시와 메모리 및 기준 런타임을 검증하고, FP32 기준 실행이 불가능하면 자동으로 모델이나 정밀도를 바꾸지 말고 보고하세요. 실행이 가능한 경우 기존1,740키를 재사용하고 미완료1,596행과 system-only2개만 백그라운드로 측정하세요. 중복 프로세스·커널 없이 진행하고, 모든 조건과 세 순서가 완료된 뒤 전체139 및 개발템플릿을 제외한119문항의 Unknown과 모든 감정축 변화를95%군집신뢰구간으로 비교해 보고하세요. 모델을 재실행하지 않고 저장 결과로 그래프·표·보고서·노트북 출력을 작성하세요. 원래 검정과 새 검정군을 혼동하거나 유의한 결과만 골라 보고하지 마세요.
