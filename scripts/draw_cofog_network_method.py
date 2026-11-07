from pathlib import Path
from html import escape

root = Path(__file__).resolve().parents[1] / 'assets/research/cofog-ai-policy'
parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1480" height="1050" viewBox="0 0 1480 1050" role="img" aria-labelledby="title desc"><title id="title">재정·정책 관심 연결망과 원문 근거 연결망</title><desc id="desc">상단은 COFOG와 국가를 재정지출 비중으로, 국가와 토픽을 보고서 포함률로 연결한다. 하단은 같은 근거 문단에서 확인된 COFOG와 토픽의 실제 연결을 별도로 나타낸다. 2023년을 경계로 3년 구간을 비교하며 불완전 재정 자료는 관측 비중을 유지하는 단순 추정으로 구분한다. 연결은 설명용 예시다.</desc><style>text{font-family:-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Noto Sans KR',sans-serif;fill:#173136}.title{font-size:32px;font-weight:700}.h{font-size:24px;font-weight:700}.body{font-size:20px}.small{font-size:17px;fill:#51686b}.label{font-size:20px;font-weight:650}.edge{fill:none;stroke-linecap:round}</style><rect width="1480" height="1050" fill="#f6f8f3"/>''']

def text(x,y,value,kind='body',anchor='start'):
    parts.append(f'<text x="{x}" y="{y}" class="{kind}" text-anchor="{anchor}">{escape(value)}</text>')

def rect(x,y,w,h,fill='#fff'):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="#d6e1dc"/>')

def edge(x1,y1,x2,y2,color,width=3):
    parts.append(f'<path class="edge" d="M{x1},{y1} L{x2},{y2}" stroke="{color}" stroke-width="{width}"/>')

def node(x,y,w,label,fill='#fff'):
    rect(x,y,w,54,fill);text(x+w/2,y+35,label,'label','middle')

text(48,56,'재정 배분과 AI 정책 관심을 연결하고, 실제 논의 내용과 구분한다','title')
text(48,91,'국가·기간별 비교 설계 · 노드와 연결은 설명용이며 실제 분석 결과가 아니다.','small')
rect(48,118,1384,435)
text(72,157,'A. 재정–국가–토픽 · 서로 다른 두 지표를 연결','h')
text(190,209,'정부기능 COFOG','label','middle');text(730,209,'국가','label','middle');text(1240,209,'BERTopic 토픽','label','middle')
text(438,247,'재정지출 비중','label','middle');text(1005,247,'보고서 포함률','label','middle')
for a,b in [(307,332),(387,332),(467,427)]:edge(300,a,640,b,'#287f77',5)
for a,b in [(332,307),(332,387),(427,387),(427,467)]:edge(820,a,1130,b,'#b77831',5)
for y,label in [(280,'07 보건'),(360,'09 교육'),(440,'04 경제업무')]:node(80,y,220,label)
for y,label in [(305,'한국'),(400,'미국')]:node(640,y,180,label,'#eaf2ed')
for y,label in [(280,'의료 AI'),(360,'AI 역량·교육'),(440,'개인정보 보호')]:node(1130,y,260,label)
text(72,528,'청록선 = 기능 지출 / 전체 정부지출','small');text(760,528,'갈색선 = 토픽 포함 고유 보고서 / 전체 분석 보고서','small')
rect(48,575,1384,253)
text(72,615,'B. 실제 COFOG–토픽 연결 · 동일 근거 문단에서 확인','h')
edge(300,687,710,687,'#438f87',4);edge(300,767,710,767,'#438f87',4)
node(80,660,220,'07 보건');node(80,740,220,'09 교육')
node(710,660,240,'의료 AI');node(710,740,240,'AI 역량·교육')
text(1000,674,'국가·기간별로 따로 집계','label');text(1000,711,'선 = 해당 결합을 확인한 보고서의','small');text(1000,738,'해당 기능 보고서 대비 비율','small');text(1000,786,'국가별 결합을 합산하면 전체 2부망','small')
rect(48,850,1384,144,'#eaf2ed')
text(72,889,'기간 · 2020–2022년 ↔ 2023–2025년 · 3년 구간 우선, 5년 구간은 보조 비교','label')
text(72,929,'재정 비중이 1년만 있으면 그 값을 3년 대표 추정값으로 사용 · 관측 1/3년 표시','body')
text(72,966,'A의 국가 경유 경로는 B의 연결을 입증하지 않는다. 기능 전체 재정은 AI 예산이 아니다.','small')
text(48,1027,'의미적 근접성은 별도 분석 · 토픽 대표 문단 임베딩의 코사인 유사도이며 위 연결선의 가중치가 아니다.','small')
parts.append('</svg>')
(root/'images/cofog_country_topic_method.svg').write_text(''.join(parts))
