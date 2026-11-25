'use strict';

function novemberIndex(rows) {
 const bases=new Map();
 for(const r of rows) if(String(r.time).slice(0,7)==='2022-11') {
  const v=Number.isFinite(r.employment)?r.employment:Number.isFinite(r.count)?r.count:r.index;
  if(Number.isFinite(v)&&v>0) bases.set(r.series,v);
 }
 return rows.filter(r=>/^202[2-9]-\d{2}/.test(String(r.time))).map(r=>{
  const v=Number.isFinite(r.employment)?r.employment:Number.isFinite(r.count)?r.count:r.index;
  const b=bases.get(r.series);
  return {...r,index:b&&Number.isFinite(v)?100*v/b:null};
 });
}

const colors=['#B7BABE','#D9DBDE','#F2D9DC','#DF9DA4','#C34E58','#7C8397'];
const ageColors=['#6F62A3','#3C929D','#7F9C73','#B19264','#6685AF','#89939A'];
const focusColor='#C34E58';
const lineDashes=[[],[7,3],[2,3],[9,3,2,3],[4,2],[12,3]];
const sexNames={All:'전체',Male:'남성',Female:'여성'};
const charts={};
const whiteOutline={id:'whiteOutline',beforeDatasetDraw(chart,args){
 const d=chart.data.datasets[args.index],line=args.meta.dataset;
 if(!line||d.label==='2022년 11월 100')return;
 const o=line.options,colour=o.borderColor,width=o.borderWidth;
 try{o.borderColor='#ffffff';o.borderWidth=width+2.0;line.draw(chart.ctx,chart.chartArea,0,line.points.length);}finally{o.borderColor=colour;o.borderWidth=width;}
}};
const endLabels={id:'endLabels',afterDatasetsDraw(chart){
 const ctx=chart.ctx,area=chart.chartArea,labels=[];
 chart.data.datasets.forEach((d,i)=>{if(d.label==='2022년 11월 100'||!chart.isDatasetVisible(i))return;
 let n=d.data.length-1;while(n>=0&&d.data[n]==null)n--;if(n<0)return;
 const p=chart.getDatasetMeta(i).data[n];if(p&&!p.skip)labels.push({x:p.x,y:p.y,target:p.y,text:d.label,colour:d.borderColor,focus:d.borderWidth>3});});
 labels.sort((a,b)=>a.y-b.y);const gap=23;
 labels.forEach((p,i)=>{p.y=Math.max(area.top+7,p.y,i?labels[i-1].y+gap:area.top+7);});
 for(let i=labels.length-1;i>=0;i--)labels[i].y=Math.min(labels[i].y,i<labels.length-1?labels[i+1].y-gap:area.bottom-6);
 ctx.save();ctx.textBaseline='middle';labels.forEach(p=>{ctx.font='bold 13px Arial, sans-serif';ctx.strokeStyle='#fff';ctx.lineWidth=3.5;ctx.lineJoin='round';const raw=p.text.replace(' · 높은 THAIE','').replace(' · 낮은 THAIE','');const text=raw==='Q1'?'Q1 · 가장 낮음':raw==='Q5'?'Q5 · 가장 높음':raw;
 if(Math.abs(p.y-p.target)>5){ctx.beginPath();ctx.moveTo(p.x+3,p.target);ctx.lineTo(area.right+7,p.y);ctx.strokeStyle=p.colour;ctx.lineWidth=.7;ctx.stroke();}
 ctx.strokeText(text,area.right+10,p.y);ctx.fillStyle=p.colour;ctx.fillText(text,area.right+10,p.y);});ctx.restore();
}};

const byId=id=>document.getElementById(id);
function options(id,items,value){const s=byId(id);for(const [v,t] of items){const o=document.createElement('option');o.value=v;o.textContent=t;s.append(o);}s.value=value;}
function val(id){return byId(id).value;}
function render(id,rows,keys,labelFn,focusGroup=false,yRange=null,sexComparison=false){
 rows=novemberIndex(rows);
 const holder=byId(id+'-chart'); if(charts[id])charts[id].destroy();holder.replaceChildren();const canvas=document.createElement('canvas');canvas.setAttribute('aria-label','고용지수 2022년 11월 100');canvas.setAttribute('role','img');holder.append(canvas);
 const times=[...new Set(rows.map(r=>r.time))].sort();const datasets=keys.map((k,i)=>({label:labelFn(k),data:times.map(t=>{const r=rows.find(r=>r.time===t&&r.series===k);return r&&r.index!==null?r.index:null;}),borderColor:sexComparison?(k==='Male'?'#C64F5A':'#577C96'):(k==='Q5'||focusGroup?focusColor:(String(k).startsWith('Q')?colors[i%colors.length]:ageColors[i%ageColors.length])),backgroundColor:sexComparison?(k==='Male'?'#C64F5A':'#577C96'):(k==='Q5'||focusGroup?focusColor:(String(k).startsWith('Q')?colors[i%colors.length]:ageColors[i%ageColors.length])),pointRadius:0,pointHoverRadius:0,pointHitRadius:8,borderWidth:3.4,borderDash:focusGroup?lineDashes[i%lineDashes.length]:[],order:sexComparison?0:(k==='Q5'||focusGroup?0:2),fill:sexComparison&&i===1?{target:0,above:"#71818b16",below:"#71818b16"}:false,spanGaps:false}));
 datasets.push({label:'2022년 11월 100',data:times.map(()=>100),borderColor:'#99a7ae',borderDash:[4,4],pointRadius:0,borderWidth:0.8,order:4});
 charts[id]=new Chart(canvas,{type:'line',data:{labels:times,datasets},plugins:[whiteOutline,endLabels],options:{layout:{padding:{right:sexComparison?65:155,top:16}},animation:false,responsive:true,maintainAspectRatio:false,interaction:{mode:'nearest',intersect:false},plugins:{legend:{display:false},tooltip:{mode:'nearest',intersect:false,filter:ctx=>ctx.dataset.label!=='2022년 11월 100',backgroundColor:'rgba(255,255,255,0.96)',titleColor:'#667580',bodyColor:'#263b47',borderColor:'#dce3e7',borderWidth:1,cornerRadius:4,padding:7,displayColors:false,caretSize:3,caretPadding:9,titleFont:{size:10,weight:'normal'},bodyFont:{size:11},callbacks:{label:ctx=>ctx.dataset.label+' · '+Number(ctx.parsed.y).toFixed(1)}}},scales:{y:{...(yRange||{}),grid:{color:'#e9edf0'},title:{display:true,text:'고용지수 · 2022년 11월 = 100'}},x:{grid:{display:false},ticks:{autoSkip:times.length!==12,maxTicksLimit:times.length===12?12:10,maxRotation:times.length===12?(sexComparison?65:30):0,minRotation:times.length===12?(sexComparison?65:30):0,font:{size:sexComparison?8:11}},title:{display:true,text:String(times[0]||'').length===7?'실제 조사연월':'연도'}}}}});
 if(!rows.some(r=>r.index!=null)){charts[id].destroy();delete charts[id];holder.replaceChildren();const message=document.createElement('p');message.className='note';message.textContent='실제 2022년 11월 기준값이 없어 이 그래프는 표시하지 않습니다.';holder.append(message);}
 const wrap=byId(id+'-table');wrap.replaceChildren();const table=document.createElement('table');const cap=document.createElement('caption');cap.textContent='지수 · 빈칸은 표본 또는 기준기간 부족으로 미표시';table.append(cap);const thead=table.createTHead();let tr=thead.insertRow();for(const text of ['시점',...keys.map(labelFn)]){const th=document.createElement('th');th.textContent=text;tr.append(th);}const body=table.createTBody();for(const t of times){tr=body.insertRow();tr.insertCell().textContent=t;for(const k of keys){const r=rows.find(r=>r.time===t&&r.series===k);tr.insertCell().textContent=r&&r.index!=null?r.index.toFixed(1):'';}}wrap.append(table);
}
Promise.all(['meta','res','monthly','administrative','gender-totals'].map(n=>fetch('data/'+n+'.json').then(r=>{if(!r.ok)throw Error('자료 로드 실패');return r.json();}))).then(([meta,res,monthly,administrative,genderTotals])=>{
 const ages=[['All','전체 15세 이상'],...meta.ages.map(a=>[a,a+'세'])],sexes=Object.entries(sexNames),freq=[['annual','연도별 · 4월·10월 평균'],['wave','실제 조사시점 · 4월·10월']];
 for(const id of ['exp-age','sex-age'])options(id,ages,'22–25');
 for(const id of ['exp-sex','occ-sex','ind-sex','mon-sex'])options(id,sexes,'All');
 for(const id of ['exp-freq','occ-freq','sex-freq','ind-freq'])options(id,freq,'wave');
 const inds=[['All','전체 산업'],...meta.industries.map(x=>['industry_'+x.id,x.id+' · '+x.name])];options('exp-ind',inds,'All');options('sex-ind',inds,'All');
 options('ind-id',meta.industries.map(x=>[x.id,x.id+' · '+x.name]),'62');options('occ-id',meta.occupations.map(x=>[x.id,x.id+' · '+x.name]),'222');options('sex-q',[1,2,3,4,5].map(i=>['Q'+i,'Q'+i+(i===5?' · 가장 높음':i===1?' · 가장 낮음':'')]),'Q5');options('mon-freq',[['monthly','월별 · 관측치'],['annual','연도별 · 12개월 평균']],'monthly');

 options('gender-age',ages,'22–25');options('gender-ind',inds,'All');options('gender-freq',freq,'wave');
 for(const kind of ['software','industry62']){options(kind+'-sex',sexes,'All');options(kind+'-freq',[['monthly','월별 · 실제 관측'],['annual','연도별 · 완료연도 12개월 평균']],'monthly');}
 const Q=['Q1','Q2','Q3','Q4','Q5'];
 function genderPanels(){const slug=val('gender-age').replaceAll('–','-').replace('+','plus').toLowerCase();byId('gender-figure-downloads').hidden=true;byId('gender-png').href='figures/sex-by-quintile-'+slug+'.png';byId('gender-pdf').href='figures/sex-by-quintile-'+slug+'.pdf';const filter=r=>r.scope===val('gender-ind')&&r.agegroup===val('gender-age')&&r.frequency===val('gender-freq')&&r.sex!=='All';const rows=res.filter(r=>r.kind==='exposure'&&filter(r));const totals=genderTotals.filter(filter);const q5=rows.filter(r=>r.line==='Q5'&&r.index!=null),times=[...new Set(q5.map(r=>r.time))].sort().reverse();const latest=times.find(t=>['Male','Female'].every(sex=>q5.some(r=>r.time===t&&r.sex===sex)));byId('gender-reading').textContent=latest?`${latest} Q5의 고용지수는 남성 ${q5.find(r=>r.time===latest&&r.sex==='Male').index.toFixed(1)}, 여성 ${q5.find(r=>r.time===latest&&r.sex==='Female').index.toFixed(1)}입니다. 각각 자기 집단의 2022년 11월과 비교한 값이며, 인구·직업 구성을 통제한 성별 효과는 아닙니다.`:'선택한 조건에서 Q5의 남녀를 같은 시점에 비교할 표시 요건이 충족되지 않습니다. 각 패널의 결측과 수치 보기를 확인해 주세요.';const ys=[...rows,...totals].filter(r=>r.index!=null).map(r=>r.index);const range=ys.length?{min:Math.floor((Math.min(...ys)-2)/5)*5,max:Math.ceil((Math.max(...ys)+2)/5)*5}:null;for(const q of [...Q,'all']){const data=(q==='all'?totals:rows.filter(r=>r.line===q)).map(r=>({...r,series:r.sex}));render('gender-q'+(q==='all'?'all':q.slice(1)),data,['Male','Female'],k=>sexNames[k],false,range,true);}}
 function administrativePanel(kind){const sourceKind=kind==='industry62'?'software':kind;const all=administrative.filter(r=>r.kind===sourceKind&&r.sex===val(kind+'-sex')&&r.frequency===val(kind+'-freq'));const allowed=val(kind+'-range')==='young'?['20~24세 이하','25~29세 이하','30~34세 이하','35~39세 이하','40~44세 이하','45~49세 이하']:['50~54세 이하','55~59세 이하','60~64세 이하','65~69세 이하','70세 이상'];render(kind,all.filter(r=>allowed.includes(r.age_group)).map(r=>({...r,series:r.age_group})),allowed,k=>k.replace('세 이하','세'));}
 render('overall',res.filter(r=>r.kind==='exposure'&&r.scope==='All'&&r.agegroup==='All'&&r.sex==='All'&&r.frequency==='wave').map(r=>({...r,series:r.line})),Q,k=>k);
 genderPanels();document.querySelectorAll('select[id^="gender-"]').forEach(s=>s.addEventListener('change',genderPanels));
 for(const kind of ['software','industry62']){administrativePanel(kind);document.querySelectorAll('select[id^="'+kind+'-"]').forEach(s=>s.addEventListener('change',()=>administrativePanel(kind)));}

 byId('coverage').textContent='지역별고용조사 취업자 중 THAIE 점수가 연결된 비율은 조사시점별 '+meta.coverage_min.toFixed(2)+'–'+meta.coverage_max.toFixed(2)+'%입니다. 연결되지 않은 직업은 분위 비교에서 제외합니다.';
 const renderers={
 exp:()=>{const rows=res.filter(r=>r.kind==='exposure'&&r.scope===val('exp-ind')&&r.agegroup===val('exp-age')&&r.sex===val('exp-sex')&&r.frequency===val('exp-freq')).map(r=>({...r,series:r.line}));render('exp',rows,['Q1','Q2','Q3','Q4','Q5'],k=>k+(k==='Q5'?' · 높은 THAIE':k==='Q1'?' · 낮은 THAIE':''));if(val('exp-ind')==='industry_62'&&!rows.some(r=>r.index!=null)){const holder=byId('exp-chart');holder.replaceChildren();const p=document.createElement('p');p.className='note';p.textContent='산업 62의 원자료는 수집되어 있습니다. 선택한 연령·성별·THAIE 분위에서 2022년 기준기간 또는 해당 조사시점의 표본이 표시 기준에 미달해 그래프를 숨겼습니다. 현재 기준은 각 조사시점 표본 30명 이상이며, 공식 공표 기준을 뜻하지 않습니다.';holder.append(p);if(val('exp-age')!=='All'){const b=document.createElement('button');b.type='button';b.textContent='전체 연령으로 가용 분위 보기';b.style.cssText='background:none;border:0;color:#176c80;text-decoration:underline;cursor:pointer;padding:8px 0;font:inherit';b.addEventListener('click',()=>{byId('exp-age').value='All';byId('exp-age').dispatchEvent(new Event('change',{bubbles:true}));});holder.append(b);}}},
 occ:()=>{const o=meta.occupations.find(x=>x.id===val('occ-id'));byId('occ-score').textContent=o.name+' · 고정 THAIE '+o.score.toFixed(3)+' · 전국 고정 분위 Q'+o.quintile+'. 직업 안에서 노출 분위는 바뀌지 않습니다.';render('occ',res.filter(r=>r.kind==='occupation'&&r.scope===o.id&&meta.ages.includes(r.agegroup)&&r.sex===val('occ-sex')&&r.frequency===val('occ-freq')).map(r=>({...r,series:r.agegroup})),meta.ages,k=>k+'세',Number(o.quintile)===5);},
 sex:()=>render('sex',res.filter(r=>r.kind==='exposure'&&r.scope===val('sex-ind')&&r.agegroup===val('sex-age')&&r.line===val('sex-q')&&r.sex!=='All'&&r.frequency===val('sex-freq')).map(r=>({...r,series:r.sex})),['Male','Female'],k=>sexNames[k],val('sex-q')==='Q5'),
 ind:()=>{const i=meta.industries.find(x=>x.id===val('ind-id'));byId('ind-score').textContent=i.name+' · 2022년 직업 구성의 고용 가중 THAIE '+i.score.toFixed(3)+'. 특정 직업을 뜻하는 산업 분류가 아닙니다.';render('ind',res.filter(r=>r.kind==='industry'&&r.scope===i.id&&meta.ages.includes(r.agegroup)&&r.sex===val('ind-sex')&&r.frequency===val('ind-freq')).map(r=>({...r,series:r.agegroup})),meta.ages,k=>k+'세');},
 mon:()=>render('mon',monthly.filter(r=>meta.ages.includes(r.agegroup)&&r.sex===val('mon-sex')&&r.frequency===val('mon-freq')).map(r=>({...r,series:r.agegroup})),meta.ages,k=>k+'세')};
 for(const [id,fn] of Object.entries(renderers)){fn();document.querySelectorAll('select[id^="'+id+'-"]').forEach(s=>s.addEventListener('change',fn));}
 document.querySelectorAll('details').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)for(const c of Object.values(charts))c.resize();}));
}).catch(err=>{const p=document.createElement('p');p.className='note';p.textContent='인터랙티브 자료를 불러오지 못했습니다. 정적 그림과 CSV를 이용해 주세요. '+err.message;byId('results').prepend(p);console.error(err);});

// Monthly administrative stocks. No occupation-to-THAIE assignment is inferred here.
(async()=>{
 const response=await fetch('data/monthly-occupations/manifest.json');if(!response.ok)throw Error('월별 직종 목록을 불러오지 못했습니다.');const manifest=await response.json();
 const software=manifest.find(o=>o.label==='소프트웨어 개발자');const cache=new Map();
 const allOptions=manifest.map(o=>[o.id,o.label==='총계'?'전체 피보험자':o.label]);const crossOptions=manifest.filter(o=>o.cross_end).map(o=>[o.id,o.label]);
 options('m-total-occ',allOptions,software.id);options('m-age-occ',crossOptions,software.id);options('m-sex-occ',crossOptions,software.id);
 const young=['20~24세 이하','25~29세 이하','30~34세 이하','35~39세 이하','40~44세 이하','45~49세 이하'];const older=['50~54세 이하','55~59세 이하','60~64세 이하','65~69세 이하','70세 이상'];
 options('m-sex-age',[...young,...older].map(a=>[a,a.replace('세 이하','세')]),young[0]);
 async function load(id){if(!cache.has(id))cache.set(id,fetch('data/monthly-occupations/'+id+'.json').then(r=>{if(!r.ok)throw Error('월별 직종 자료 로드 실패');return r.json();}).then(a=>a.map(r=>({time:r[0],age:r[1],sex:r[2],index:r[3],employment:r[4]}))));return cache.get(id);}
 function fillMonths(rows,keys,start,end){if(!start||!end)return rows;const periods=[];let y=Number(start.slice(0,4)),m=Number(start.slice(5));while(y+'-'+String(m).padStart(2,'0')<=end){periods.push(y+'-'+String(m).padStart(2,'0'));if(++m===13){m=1;y++;}}const lookup=new Map(rows.map(r=>[r.time+'|'+r.series,r]));return periods.flatMap(time=>keys.map(series=>lookup.get(time+'|'+series)||{time,series,index:null,employment:null}));}
 const runs={};async function panel(id){const token=(runs[id]||0)+1;runs[id]=token;const selected=val(id+'-occ'),meta=manifest.find(o=>o.id===selected),data=await load(selected);if(runs[id]!==token)return;let rows,keys,start,end;
 if(id==='m-total'){keys=['전체 연령'];rows=data.filter(r=>r.age==='All'&&r.sex==='All').map(r=>({...r,series:keys[0]}));start=meta.all_start;end=meta.all_end;}
 else if(id==='m-age'){keys=val(id+'-range')==='young'?young:older;rows=data.filter(r=>keys.includes(r.age)&&r.sex===val(id+'-sex')).map(r=>({...r,series:r.age}));start=meta.cross_start;end=meta.cross_end;}
 else{keys=['Female','Male'];rows=data.filter(r=>r.age===val('m-sex-age')&&keys.includes(r.sex)).map(r=>({...r,series:r.sex}));start=meta.cross_start;end=meta.cross_end;}
 byId(id+'-info').textContent='고용행정통계 · '+meta.label+' · '+(start<'2022-01'?'2022-01':start)+'–'+end+' · 월말 피보험자 · 2022년 11월 = 100 · 계절조정 전';
 render(id,fillMonths(rows,keys,start,end),keys,k=>sexNames[k]||k.replace('세 이하','세'));
 }
 for(const id of ['m-total','m-age','m-sex']){await panel(id);document.querySelectorAll('select[id^="'+id+'-"]').forEach(s=>s.addEventListener('change',()=>panel(id).catch(showError)));}
 function showError(e){byId('monthly-paths').insertAdjacentText('afterbegin','월별 자료를 불러오지 못했습니다. '+e.message);}
})().catch(e=>{byId('monthly-paths').insertAdjacentText('afterbegin','월별 자료를 불러오지 못했습니다. '+e.message);});
