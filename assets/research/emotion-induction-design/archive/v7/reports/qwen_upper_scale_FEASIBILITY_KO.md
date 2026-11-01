# Qwen2.5 상위 모델 실행 가능성 검토

2026-10-30T17:10:14.375680+09:00

7B 결과는 원본 실험 폴더와 해시 검증 ZIP에 로컬 저장했다. 새 모델 가중치는 다운로드하거나 로드하지 않았다. 원고·Overleaf·홈페이지는 수정하지 않았다.

장비는 M4 Pro 20GPU코어, 통합메모리48GiB다. PyTorch MPS가 보고한권장상한은37.44GiB다. 측정시점의빈디스크는약11.6GiB이며외장볼륨은없다. 현재가용RAM과기존swap은동적상태이므로실행직전재확인한다.

| 모델 | 정밀도 | 가중치 GiB | 판단 |
|---|---|---:|---|
| Qwen/Qwen2.5-14B-Instruct | bf16 | 27.51 | 같은bf16/MPS실험의현실적다음후보. batch1로로드·훅·정확한토큰질량·제거/추가를검증한뒤본실험. 성공보장은아님 |
| Qwen/Qwen2.5-32B-Instruct | bf16 | 61.03 | 가중치만48GiB를초과하므로현재환경의비양자화실험에부적합 |
| Qwen/Qwen2.5-72B-Instruct | bf16 | 135.43 | 현재환경의비양자화실험에부적합 |
| mlx-community/Qwen2.5-32B-Instruct-4bit | 4bit-MLX | 17.17 | 저장공간확보후탐색가능한양자화상한후보. MLX개입코드와활성값·확률측정검증필요. bf16주규모비교와분리 |
| mlx-community/Qwen2.5-72B-Instruct-4bit | 4bit-MLX | 38.09 | 가중치만38.1GiB라OS와활성값여유가부족. 이번5184개개입실험에는권하지않음 |

가중치크기는공식safetensors index 또는배포자파일메타데이터에서계산했다. 실행총메모리와같지않다. 가중치외에활성값·attention·Metal연산작업공간과OS메모리가필요하다.

**권고는7B→14B bf16의동일최소설계비교다.** 14B는48층중24층,5120차원이며모델전용8축을동일이야기에서재추출한다. 7B의3584차원축을재사용하지않는다. 108문항·48조건·seed·두주지표·조건부CI정의는유지한다. batch크기는메모리검증에맞춰줄이고그차이와숫자재현성을기록한다.

현재디스크공간으로는14B의27.5GiB가중치를받을수없다. 모델캐시를둘외장SSD경로또는최소35~40GiB의실제빈공간을확보해야한다. 기존실험결과·모델캐시를임의삭제하지않았다. 32B 4bit도현재빈디스크보다크다.

32B/72B bf16은더큰메모리의장비나외부GPU환경이필요하다. 32B 4bit는양자화와백엔드차이가혼재하므로순수규모효과의증거로합치지않는다. 7B·14B두점만으로단조규모추세를주장하지않는다.

14B로가도8축일반화한계와전체방향d의낮은포착률이저절로해결되지는않는다. 결과해석의한계는유지한다. 실측소요시간은로드와소수문항검증후에만추정한다.

## 출처

- https://huggingface.co/Qwen/Qwen2.5-14B-Instruct/raw/cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8/model.safetensors.index.json
- https://huggingface.co/Qwen/Qwen2.5-32B-Instruct/raw/5ede1c97bbab6ce5cda5812749b4c0bdf79b18dd/model.safetensors.index.json
- https://huggingface.co/Qwen/Qwen2.5-72B-Instruct/raw/495f39366efef23836d0cfae4fbe635880d2be31/model.safetensors.index.json
- https://huggingface.co/api/models/mlx-community/Qwen2.5-32B-Instruct-4bit?blobs=true
- https://huggingface.co/api/models/mlx-community/Qwen2.5-72B-Instruct-4bit?blobs=true
