# Policy Commons 전수 분류 감사

## 웹에서 실행

Finder에서 `open_audit_notebook.command`를 더블클릭한다. JupyterLab이 로컬 웹 브라우저에서
열리면 `Run All Cells`를 실행한다. 입력 v5 마스터는 수정하지 않는다.

## 셸에서 전체 자동 실행

```bash
cd /Users/deep1003/Downloads/pcgs_aigov5_20260920/full_census_audit
./run_audit_notebook.sh
```

각 실행은 `runs/audit_UTC시각/`에 다음 파일을 새로 만든다.

- `audit_candidates.csv.gz`
- `rule_summary.csv`
- `regression_results.csv`
- `record_audit_flags.parquet`
- `metrics.json`
- `SHA256SUMS.txt`

그래프는 규칙별 후보 수, 심각도별 후보 수, 연도별 후보 비율을 표시한다. 후보 플래그는 자동
삭제나 자동 재분류가 아니다. 고위험 후보를 검토하고 오류와 반례를 회귀검사에 추가한 뒤 새
버전의 릴리스를 생성한다.
