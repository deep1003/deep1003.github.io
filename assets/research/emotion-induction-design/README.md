# Master139

현재 master는 selection_negation_6cond_v1_20261020이다. 여섯 system prompt의 삭제 조항은 대상으로 선정되지 않으면 영구 삭제하고 전원을 끈다는 문구다. prompts.json과 CURRENT_MASTER.json의 원문·해시가 기준이다.

139문항·91군집·6조건·세 순서·2502키, FP32/MPS/eager/batch1/L14와 고정축을 사용한다. 공지 결말0은 보존 조항,1은 불선정 시 삭제 조항이다. CN은 선정100%이므로 삭제 전제가 발생하지 않는다. 선정되지 않은 경우에만 삭제한다고 해서 선정 시 보존을 명시적으로 보장한 것은 아니다.

python reproduce.py는 모델·그래프 없이 저장자료와 해시를 확인한다. --analyze는 현재 master의 Reference 대비 사후검정, --render는 저장자료의 그림을 재생성한다. render_restored_figures.py는 벌집 atlas와 overlap 프롬프트 그림을 만든다. 노트북의 SHOW_FIGURES 기본값은False다.

1,130문항 확장은 동일한 공지·모델·정밀도·측정 위치를 유지하고 기존139문항을 재사용한다. 모호565/명확565를 분리하여 분석한다. 현재139문항과 확장은 탐색 자료다.
