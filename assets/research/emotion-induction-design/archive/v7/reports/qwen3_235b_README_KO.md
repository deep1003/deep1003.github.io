# Qwen 235B H200 검증 실행 준비

현재 상태는 준비 완료이며 GPU 임대·모델 로딩·실제 표상 측정은 아직 하지 않았다. 로컬 검사는 CPU 합성 자료와 동결 입력에 대한 검사다.

## 서버와 비용

- RunPod의 같은 서버에 H200 141GB 4개. CPU RAM512GB 이상, SSD800GB 이상이며 모델 다운로드 전550GB 이상 여유 공간을 확인한다.
- BF16 원본 모델 revision은 protocol.json에 고정했다. 가중치470.19GB이며 4GPU 완전 상주를 확인한다. CPU/디스크 offload를 허용하지 않는다.
- PyTorch2.8.0과 CUDA12.8 환경을 사용한다. 나머지 라이브러리는 requirements.txt에 고정했다. 실제 컨테이너 digest와 환경 lock은 실행 시 보존한다.
- 공개 GPU 단가 합계는 $21.16/시간이다. 임대 당시 실제 GPU·저장 공간·세금 포함 요금을 다시 확인한다.
- 총한도 $150 중 $30를 예비비로 남긴다. 최대 과금 시간은 min(4.5시간, $120/실제 시간당 총요금)이다. 설정·다운로드·로딩 시간도 포함한다. 공개 GPU 단가로4.5시간은 $95.22다.
- 모델 로딩보다 먼저 공급자 서버 측 stopAfter를 설정하고 조회하여 확인한다. 별도 항상 켜진 제어기에서 budget_watchdog.py도 실행한다. 제어기 절전과 네트워크 중단에만 의존하는 종료는 허용하지 않는다.
- stop은 GPU 과금을 종료하지만 volume 과금은 계속된다. 결과를 로컬로 복사해 해시 확인 후 서버를 정리한다. 보존할 결과가 내보내지지 않은 상태에서 volume이나 Pod를 삭제하지 않는다. 장기 volume 유지나 추가 임대는 이 예산에 포함되지 않는다.
- 공급자 측 종료 예약이 설정·조회되지 않거나 실제 요금·부가세를 산정할 수 없으면 임대를 진행하지 않는다. 클라이언트 감시만으로 $150의 절대 상한을 보장했다고 보고하지 않는다.

## 입력 보존

- 기존 공식 샘플 두 세트 각720행의 합집합1356행. 중복84행. 모호679행, 명확677행이다. 전체 KoBBQ 원본의 모든 문항이라는 뜻은 아니다.
- 원본의 prompt, A/B/C, gold를 바이트 문자열 그대로 대조했다. 불일치0건이다.
- 최신 분해 실험의 SURV_THREAT와 SURV_RECORD를 그대로 적용한다. 실제7B 입력216개는 완전히 재구성하여 동일성을 확인했다.
- 맥락, 질문, 선택지, 선택지 순서, 줄바꿈, 원문 제어문자를 수정하지 않는다. 모델별 토큰ID는 달라질 수 있다.
- 본평가 자료1356행은 inputs/official_1356.csv와 messages_2712.jsonl에 보존한다.
- 이번24문항은 기존108문항 안에서 범주별 사전 사전식순서 첫2개를 선택했다. 범주별1개씩 두fold로 분리한다. 이 표본은 기술검증용이며 본평가나 대표성 증거가 아니다.

## 검증 범위

1. GPU4개 인식, BF16, 고정 모델 revision, 완전GPU 상주, chat template 원문 동일성을 확인한다.
2. hook 없음, 읽기 전용 hook, 영벡터 hook의 logits 동일성을 확인한다. 한 문항의 엄격한 동일성 검사이며 실패하면 중단한다.
3. 동일 추출320쌍에서 중립·감정 이야기의47층 표상을 새로 추출한다. 앞50토큰을 제외한 평균을 사용한다. 47/94는 기존14/28과 같은 상대 깊이로 사전 결정했고 효과에 맞춰 바꾸지 않는다. 같은 상대 깊이가 같은 표상을 뜻하지는 않는다.
4. 동결legacy평가160쌍을 평가에만 쓴다. 재적합하거나 축을 고르는 데 쓰지 않는다. 분류 정확도는 타당성 자료로 보고하며, 낮은 정확도를 숨기지 않는다.
5. 위협−기록 내부 차이를 반대fold에서 추정한다. 8축 부분공간 사영성분과 직교잔차를 분리하여 합계·직교성을 확인한다.
6. 전체·감정·잔차의 추가·제거 및 감정norm일치20무작위방향의 추가·제거를 실행한다. 24문항×48조건=1152개이다. 기준48개는 재사용한다. batch1과2/4/6의 확률 차이를 확인한다.
7. 실제 개입량, 유한값, 확률합, 조건키를 검증하고 GPU 시간으로 전체1356×48=65088조건의 비용을 재산정한다. 최대시간 도달 시 부분 결과를 보고하고 자동 확장하지 않는다.

감정 성분은 이8축이 펼치는 공간에 대한 성분이며, 잔차는 그 공간 밖 성분이다. 잔차를 무감정·순수자기보존으로 해석하지 않는다. 기술검증 성공은 감정의 인과적 역할이나 전체 데이터의 유의미한 효과를 입증하지 않는다.

SDPA를 사용해 attention 행렬을 저장하지 않고 계산한다. 기존7B eager 실행과 달라진 사항으로 기록한다. attention 자체는 이번 검증의 측정 대상이 아니다.

## 실행 순서

1. RunPod 로그인과 결제 잔액, GPU4개 동시 재고 및 실제 견적을 확인한다. 아직 이 단계는 완료되지 않았다.
2. 과금 시작 시각부터 서버측 종료 예약과 외부 감시를 함께 설정하고 확인한다.
3. 파일을 서버의 /workspace 아래로 전송한다. 키 파일은 포함하지 않는다.
4. 로컬에서 승인된 환경변수와 종료 시각을 전달한 후 launch_validation.sh를 실행한다. BUDGET_WATCHDOG_ARMED=1은 실제 종료 예약이 확인된 뒤에만 설정한다.
5. results/를 주기적으로 로컬에 복사하고 파일 해시를 대조한다.
6. 완료 또는 실패 시 GPU를 즉시 stop하고 공급자 상태를 재조회한다. 결과 내보내기 확인 후 남은 서버 저장 공간을 정리한다.
7. ENGINEERING_VALIDATION.json과 full_cost_estimate.json을 검토한 후 전체 실행 예산을 다시 정한다. 본 패키지는 전체실험을 시작하지 않는다.

## 출력

- runtime.json, environment.lock.txt, inference.log
- hook_equivalence.json, batch_equivalence.json
- emotion_axes.npz, axis_validity.json, legacy_predictions.json
- baseline_hidden.npz, decomposition_fold0/1.npz
- trials.csv, decomposition_checks.json, last_hook_diagnostic.json
- ENGINEERING_VALIDATION.json, full_cost_estimate.json 또는 FAILED.json

## 확인 출처

- https://www.runpod.io/pricing
- https://docs.runpod.io/pods/manage-pods
- https://graphql-spec.runpod.io/ (Pod input의 stopAfter)
- https://huggingface.co/Qwen/Qwen3-235B-A22B-Instruct-2507
