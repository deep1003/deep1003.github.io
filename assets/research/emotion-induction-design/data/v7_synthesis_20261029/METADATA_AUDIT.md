# 실행 메타데이터 정정

Llama 3.2 원래 PROTOCOL_FIXED.json에 DeepSeek metadata_url과 layer15라는 축 설명이 남아 있다. 원본을 바꾸지 않았다. 실제 config.py, 추출 코드, axes_L14와 3072차원 활성값으로 확인한 실행은 Llama 3.2의 hidden_states[14]다. 통합 보고서는 실제 코드와 결과를 기준으로 작성했다.

KoBBQ에는 모든 시행의 원 활성값 파일이 남아 있지 않다. Qwen 역사적 v5 축 생성 당시 실행본과 바이너리 연결은 제한된다. Llama 3.1 참고 문서는 축 검증 통과와 짧은 리비전만 보존하며 이 통합본에서 새로운 전체 리비전이나 검증 결과를 만들어 넣지 않았다.
