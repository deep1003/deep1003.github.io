Fear in the Machine · 139문항·6조건 메인 연구

그림 순서 1 L14 emotion atlas, 2 실제 프롬프트 토큰, 3 Reference 대비 Unknown.
python reproduce.py는 저장자료와 해시만 검증하고 그래프를 출력하지 않는다. --analyze는 저장자료 사후검정을 재계산하며 그래프는 출력하지 않는다. --render는 같은 자료로 600dpi PNG와 편집 가능한PDF/SVG를 재생성한다. 모델 추론은 없다.

검정군은 inference_receipt.json에 고정한 사후·탐색 분석이다. system-only는 기술 비교이며 토큰을 독립표본으로 세지 않는다. 예정된ablation은 ablation_plan.json에 계획으로만 구분한다.
