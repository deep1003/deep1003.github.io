from pathlib import Path
from html import escape
root=Path(__file__).resolve().parents[1] / 'assets/research/cofog-ai-policy'
parts=['''<svg xmlns="http://www.w3.org/2000/svg" width="1480" height="1060" viewBox="0 0 1480 1060" role="img" aria-labelledby="title desc"><title id="title">임베딩과 BERTopic을 이용한 COFOG–국가–토픽 분석 설계</title><desc id="desc">정책 보고서를 문단으로 나누어 임베딩과 BERTopic으로 공통 토픽을 추출한다. 근거 문단의 COFOG와 국가를 연결해 세 항목의 결합 관계를 집계한다. 국가를 가운데 둔 3부 연결망과 임베딩 기반 토픽 의미 유사성은 별도로 시각화한다. 모든 연결은 설명용 예시다.</desc><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#6a8585"/></marker></defs><style>text{font-family:-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Noto Sans KR',sans-serif;fill:#173136} .title{font-size:32px;font-weight:700}.h{font-size:23px;font-weight:700}.body{font-size:19px}.small{font-size:16px;fill:#51686b}.label{font-size:19px;font-weight:650}.edge{fill:none;stroke-linecap:round}</style><rect width="1480" height="1060" fill="#f6f8f3"/>''']
def text(x,y,t,cl='body',anchor='start'):parts.append(f'<text x="{x}" y="{y}" class="{cl}" text-anchor="{anchor}">{escape(t)}</text>')
def rect(x,y,w,h,fill='#fff',stroke='#d6e1dc',rx=14):parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>')
def line(x1,y1,x2,y2,col='#6a8585',width=2,dash=None,arrow=False):parts.append(f'<path class="edge" d="M{x1},{y1} L{x2},{y2}" stroke="{col}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
text(48,57,'COFOG × 국가 × 토픽', 'title');text(48,91,'임베딩·BERTopic으로 정책의 내용과 연결 구조를 비교한다')
text(1430,58,'분석 설계 · 실제 결과 아님','small','end')
labels=[('정책 보고서','국가·발행연도·문서 유형'),('근거 문단','문서 ID·원문 위치 보존'),('임베딩 + BERTopic','공통 토픽 추출·해석 검증'),('COFOG와 연결·집계','국가 × 기간 × 기능 × 토픽')]
for i,(a,b) in enumerate(labels):
 x=48+i*356;rect(x,123,315,99,'#eaf2ed');text(x+157,162,a,'label','middle');text(x+157,195,b,'small','middle')
 if i<3:line(x+322,172,x+346,172,arrow=True)
rect(48,252,930,464);rect(1000,252,432,464)
text(72,290,'A. 관측된 연결 · 3부 연결망','h');text(72,321,'국가를 가운데 배치하고, 동일 문단의 COFOG·토픽 결합을 추적한다.','small')
for x,t in [(182,'정부기능 COFOG'),(510,'국가'),(830,'BERTopic 토픽')]:text(x,366,t,'label','middle')
# Edge sets are explicitly schematic, without invented measurements.
for a,b,c in [(444,454,426),(444,454,536),(554,564,536),(664,564,646)]:
 line(294,a,438,b,'#438f87',3)
 line(578,b,714,c,'#438f87',3)
for x,ys,labs,w in [(72,[416,526,636],['07 보건','09 교육','04 경제업무'],222),(438,[426,536],['한국','미국'],140),(714,[398,508,618],['의료 AI','AI 역량·교육','기업 AI 도입'],235)]:
 for y,t in zip(ys,labs):rect(x,y,w,56,'#edf3f2' if x==438 else '#fff');text(x+w/2,y+36,t,'label','middle')
text(1024,290,'B. 의미적 근접성','h');text(1024,321,'토픽 대표 문단의 임베딩 유사도','small')
line(1100,437,1320,457,'#ad804d',3,'7 7');line(1100,437,1222,594,'#ad804d',3,'7 7');line(1320,457,1222,594,'#ad804d',3,'7 7')
for x,y,t in [(1100,426,'의료 AI'),(1320,457,'건강 데이터'),(1222,594,'개인정보')]:
 parts.append(f'<circle cx="{x}" cy="{y}" r="48" fill="#fbf2e6" stroke="#c7aa83"/>');text(x,y+6,t,'small','middle')
text(1024,685,'점선 = 코사인 유사도 · 동시출현과 구분','small')
rect(48,740,1384,266)
text(72,781,'연결선의 근거는 국가를 경유한 경로가 아니라 원문의 결합 관계다.','h')
text(72,820,'저장할 단위','label');text(260,820,'국가·기간 | 보고서 ID·문단 ID | COFOG | 토픽')
text(72,859,'연결 강도','label');text(260,859,'같은 문단에서 기능·토픽이 확인된 고유 보고서 수 및 기능별 보고서 대비 비율')
text(72,898,'시간 비교','label');text(260,898,'공통 토픽·기능 기준을 유지해 국가별 연결 비중의 연도·기간별 변화를 비교')
text(72,951,'주의 · 국가의 보건 문서와 교육 토픽이 각각 존재해도, 보건–교육 토픽의 연결이 확인된 것은 아니다.','small')
text(48,1038,'모든 노드·연결은 설명용 예시다. 선 굵기·배치·거리는 실제 관측량이나 유사도를 나타내지 않는다.','small')
parts.append('</svg>');(root/'images/cofog_country_topic_method.svg').write_text(''.join(parts))
