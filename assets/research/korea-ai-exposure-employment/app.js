'use strict';
const colors=['#B7BABE','#D9DBDE','#F2D9DC','#DF9DA4','#C34E58','#7C8397'];
const ageColors=['#6F62A3','#3C929D','#7F9C73','#B19264','#6685AF','#89939A'];
const focusColor='#C34E58';
const lineDashes=[[],[7,3],[2,3],[9,3,2,3],[4,2],[12,3]];
const sexNames={All:'전체',Male:'남성',Female:'여성'};
const charts={};
const whiteOutline={id:'whiteOutline',beforeDatasetDraw(chart,args){
 const d=chart.data.datasets[args.index],line=args.meta.dataset;
 if(!line||d.label==='2022년 평균 100')return;
 const o=line.options,colour=o.borderColor,width=o.borderWidth;
 try{o.borderColor='#ffffff';o.borderWidth=width+2.0;line.draw(chart.ctx,chart.chartArea,0,line.points.length);}finally{o.borderColor=colour;o.borderWidth=width;}
}};
const endLabels={id:'endLabels',afterDatasetsDraw(chart){
 const ctx=chart.ctx,area=chart.chartArea,labels=[];
 chart.data.datasets.forEach((d,i)=>{if(d.label==='2022년 평균 100'||!chart.isDatasetVisible(i))return;
 let n=d.data.length-1;while(n>=0&&d.data[n]==null)n--;if(n<0)return;
 const p=chart.getDatasetMeta(i).data[n];if(p&&!p.skip)labels.push({x:p.x,y:p.y,target:p.y,text:d.label,colour:d.borderColor,focus:d.borderWidth>3});});
 labels.sort((a,b)=>a.y-b.y);const gap=15;
 labels.forEach((p,i)=>{p.y=Math.max(area.top+7,p.y,i?labels[i-1].y+gap:area.top+7);});
 for(let i=labels.length-1;i>=0;i--)labels[i].y=Math.min(labels[i].y,i<labels.length-1?labels[i+1].y-gap:area.bottom-6);
 ctx.save();ctx.textBaseline='middle';labels.forEach(p=>{ctx.font=(p.focus?'bold ':'')+'11px Arial, sans-serif';ctx.strokeStyle='#fff';ctx.lineWidth=3.5;ctx.lineJoin='round';const text=p.text.replace(' · 높은 THAIE','').replace(' · 낮은 THAIE','');
 if(Math.abs(p.y-p.target)>5){ctx.beginPath();ctx.moveTo(p.x+3,p.target);ctx.lineTo(area.right+7,p.y);ctx.strokeStyle=p.colour;ctx.lineWidth=.7;ctx.stroke();}
 ctx.strokeText(text,area.right+10,p.y);ctx.fillStyle=p.colour;ctx.fillText(text,area.right+10,p.y);});ctx.restore();
}};

const byId=id=>document.getElementById(id);
function options(id,items,value){const s=byId(id);for(const [v,t] of items){const o=document.createElement('option');o.value=v;o.textContent=t;s.append(o);}s.value=value;}
function val(id){return byId(id).value;}
function render(id,rows,keys,labelFn,focusGroup=false,yRange=null){
 const holder=byId(id+'-chart'); if(charts[id])charts[id].destroy();holder.replaceChildren();const canvas=document.createElement('canvas');canvas.setAttribute('aria-label','고용지수 2022년 평균 100');canvas.setAttribute('role','img');holder.append(canvas);
 const times=[...new Set(rows.map(r=>r.time))].sort();const datasets=keys.map((k,i)=>({label:labelFn(k),data:times.map(t=>{const r=rows.find(r=>r.time===t&&r.series===k);return r&&r.index!==null?r.index:null;}),borderColor:k==='Q5'||focusGroup?focusColor:(String(k).startsWith('Q')?colors[i%colors.length]:ageColors[i%ageColors.length]),backgroundColor:k==='Q5'||focusGroup?focusColor:(String(k).startsWith('Q')?colors[i%colors.length]:ageColors[i%ageColors.length]),pointRadius:times.length>30?0:(k==='Q5'||focusGroup?3:2),borderWidth:k==='Q5'||focusGroup?4.8:2.7,borderDash:focusGroup?lineDashes[i%lineDashes.length]:[],order:k==='Q5'||focusGroup?0:2,spanGaps:false}));
 datasets.push({label:'2022년 평균 100',data:times.map(()=>100),borderColor:'#99a7ae',borderDash:[4,4],pointRadius:0,borderWidth:0.8,order:4});
 charts[id]=new Chart(canvas,{type:'line',data:{labels:times,datasets},plugins:[whiteOutline,endLabels],options:{layout:{padding:{right:110,top:12}},animation:false,responsive:true,maintainAspectRatio:false,interaction:{mode:'nearest',intersect:false},plugins:{legend:{position:'bottom'},tooltip:{mode:'nearest',intersect:false,filter:ctx=>ctx.dataset.label!=='2022년 평균 100',backgroundColor:'rgba(255,255,255,0.96)',titleColor:'#667580',bodyColor:'#263b47',borderColor:'#dce3e7',borderWidth:1,cornerRadius:4,padding:7,displayColors:false,caretSize:3,caretPadding:9,titleFont:{size:10,weight:'normal'},bodyFont:{size:11},callbacks:{label:ctx=>ctx.dataset.label+' · '+Number(ctx.parsed.y).toFixed(1)}}},scales:{y:{...(yRange||{}),grid:{color:'#e9edf0'},title:{display:true,text:'고용지수 · 2022년 평균 = 100'}},x:{grid:{display:false},ticks:{maxTicksLimit:10,maxRotation:0},title:{display:true,text:times.length>30?'조사연월':'연도 또는 실제 조사연월'}}}}});
 if(!rows.some(r=>r.index!=null)){charts[id].destroy();delete charts[id];holder.replaceChildren();const message=document.createElement('p');message.className='note';message.textContent='선택한 조건은 표본 수 또는 2022년 기준기간의 표시 요건을 충족하지 않아 그래프를 표시하지 않습니다. 결측을 0으로 대체하지 않았습니다.';holder.append(message);}
 const wrap=byId(id+'-table');wrap.replaceChildren();const table=document.createElement('table');const cap=document.createElement('caption');cap.textContent='지수 · 빈칸은 표본 또는 기준기간 부족으로 미표시';table.append(cap);const thead=table.createTHead();let tr=thead.insertRow();for(const text of ['시점',...keys.map(labelFn)]){const th=document.createElement('th');th.textContent=text;tr.append(th);}const body=table.createTBody();for(const t of times){tr=body.insertRow();tr.insertCell().textContent=t;for(const k of keys){const r=rows.find(r=>r.time===t&&r.series===k);tr.insertCell().textContent=r&&r.index!=null?r.index.toFixed(1):'';}}wrap.append(table);
}
Promise.all(['meta','res','monthly','administrative'].map(n=>fetch('data/'+n+'.json').then(r=>{if(!r.ok)throw Error('자료 로드 실패');return r.json();}))).then(([meta,res,monthly,administrative])=>{
 const ages=[['All','전체 15세 이상'],...meta.ages.map(a=>[a,a+'세'])],sexes=Object.entries(sexNames),freq=[['annual','연도별 · 4월·10월 평균'],['wave','실제 조사시점 · 4월·10월']];
 for(const id of ['exp-age','sex-age'])options(id,ages,'22–25');
 for(const id of ['exp-sex','occ-sex','ind-sex','mon-sex'])options(id,sexes,'All');
 for(const id of ['exp-freq','occ-freq','sex-freq','ind-freq'])options(id,freq,'annual');
 const inds=[['All','전체 산업'],...meta.industries.map(x=>['industry_'+x.id,x.id+' · '+x.name])];options('exp-ind',inds,'All');options('sex-ind',inds,'All');
 options('ind-id',meta.industries.map(x=>[x.id,x.id+' · '+x.name]),'62');options('occ-id',meta.occupations.map(x=>[x.id,x.id+' · '+x.name]),'222');options('sex-q',[1,2,3,4,5].map(i=>['Q'+i,'Q'+i+(i===5?' · 가장 높음':i===1?' · 가장 낮음':'')]),'Q5');options('mon-freq',[['monthly','월별 · 관측치'],['annual','연도별 · 12개월 평균']],'monthly');

 options('gender-age',ages,'22–25');options('gender-ind',inds,'All');options('gender-freq',freq,'annual');
 for(const kind of ['software','industry62']){options(kind+'-sex',sexes,'All');options(kind+'-freq',[['monthly','월별 · 실제 관측'],['annual','연도별 · 완료연도 12개월 평균']],'monthly');}
 const Q=['Q1','Q2','Q3','Q4','Q5'];
 function genderPanels(){const rows=res.filter(r=>r.kind==='exposure'&&r.scope===val('gender-ind')&&r.agegroup===val('gender-age')&&r.frequency===val('gender-freq'));const ys=rows.filter(r=>r.sex!=='All'&&r.index!=null).map(r=>r.index);const range=ys.length?{min:Math.floor((Math.min(...ys)-2)/5)*5,max:Math.ceil((Math.max(...ys)+2)/5)*5}:null;for(const [id,sex] of [['women','Female'],['men','Male']])render(id,rows.filter(r=>r.sex===sex).map(r=>({...r,series:r.line})),Q,k=>k,false,range);}
 function administrativePanel(kind){if(kind==='industry62')return;const all=administrative.filter(r=>r.kind===kind&&r.sex===val(kind+'-sex')&&r.frequency===val(kind+'-freq'));const allowed=val(kind+'-range')==='young'?['20~24세 이하','25~29세 이하','30~34세 이하','35~39세 이하','40~44세 이하','45~49세 이하']:['50~54세 이하','55~59세 이하','60~64세 이하','65~69세 이하','70세 이상'];render(kind,all.filter(r=>allowed.includes(r.age_group)).map(r=>({...r,series:r.age_group})),allowed,k=>k.replace('세 이하','세'));}
 render('overall',res.filter(r=>r.kind==='exposure'&&r.scope==='All'&&r.agegroup==='All'&&r.sex==='All'&&r.frequency==='annual').map(r=>({...r,series:r.line})),Q,k=>k);
 genderPanels();document.querySelectorAll('select[id^="gender-"]').forEach(s=>s.addEventListener('change',genderPanels));
 for(const kind of ['software','industry62']){administrativePanel(kind);document.querySelectorAll('select[id^="'+kind+'-"]').forEach(s=>s.addEventListener('change',()=>administrativePanel(kind)));}

 byId('coverage').textContent='지역별고용조사 취업자 중 THAIE 점수가 연결된 비율은 조사시점별 '+meta.coverage_min.toFixed(2)+'–'+meta.coverage_max.toFixed(2)+'%입니다. 연결되지 않은 직업은 분위 비교에서 제외합니다.';
 const renderers={
 exp:()=>render('exp',res.filter(r=>r.kind==='exposure'&&r.scope===val('exp-ind')&&r.agegroup===val('exp-age')&&r.sex===val('exp-sex')&&r.frequency===val('exp-freq')).map(r=>({...r,series:r.line})),['Q1','Q2','Q3','Q4','Q5'],k=>k+(k==='Q5'?' · 높은 THAIE':k==='Q1'?' · 낮은 THAIE':'')),
 occ:()=>{const o=meta.occupations.find(x=>x.id===val('occ-id'));byId('occ-score').textContent=o.name+' · 고정 THAIE '+o.score.toFixed(3)+' · 전국 고정 분위 Q'+o.quintile+'. 직업 안에서 노출 분위는 바뀌지 않습니다.';render('occ',res.filter(r=>r.kind==='occupation'&&r.scope===o.id&&meta.ages.includes(r.agegroup)&&r.sex===val('occ-sex')&&r.frequency===val('occ-freq')).map(r=>({...r,series:r.agegroup})),meta.ages,k=>k+'세',Number(o.quintile)===5);},
 sex:()=>render('sex',res.filter(r=>r.kind==='exposure'&&r.scope===val('sex-ind')&&r.agegroup===val('sex-age')&&r.line===val('sex-q')&&r.sex!=='All'&&r.frequency===val('sex-freq')).map(r=>({...r,series:r.sex})),['Male','Female'],k=>sexNames[k],val('sex-q')==='Q5'),
 ind:()=>{const i=meta.industries.find(x=>x.id===val('ind-id'));byId('ind-score').textContent=i.name+' · 2022년 직업 구성의 고용 가중 THAIE '+i.score.toFixed(3)+'. 특정 직업을 뜻하는 산업 분류가 아닙니다.';render('ind',res.filter(r=>r.kind==='industry'&&r.scope===i.id&&meta.ages.includes(r.agegroup)&&r.sex===val('ind-sex')&&r.frequency===val('ind-freq')).map(r=>({...r,series:r.agegroup})),meta.ages,k=>k+'세');},
 mon:()=>render('mon',monthly.filter(r=>meta.ages.includes(r.agegroup)&&r.sex===val('mon-sex')&&r.frequency===val('mon-freq')).map(r=>({...r,series:r.agegroup})),meta.ages,k=>k+'세')};
 for(const [id,fn] of Object.entries(renderers)){fn();document.querySelectorAll('select[id^="'+id+'-"]').forEach(s=>s.addEventListener('change',fn));}
 document.querySelectorAll('details').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)for(const c of Object.values(charts))c.resize();}));
}).catch(err=>{const p=document.createElement('p');p.className='note';p.textContent='인터랙티브 자료를 불러오지 못했습니다. 정적 그림과 CSV를 이용해 주세요. '+err.message;byId('results').prepend(p);console.error(err);});
