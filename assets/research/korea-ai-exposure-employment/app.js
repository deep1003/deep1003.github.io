'use strict';
const colors=['#0072B2','#E69F00','#009E73','#CC79A7','#D55E00','#6b7280'];
const sexNames={All:'전체',Male:'남성',Female:'여성'};
const charts={};
const byId=id=>document.getElementById(id);
function options(id,items,value){const s=byId(id);for(const [v,t] of items){const o=document.createElement('option');o.value=v;o.textContent=t;s.append(o);}s.value=value;}
function val(id){return byId(id).value;}
function render(id,rows,keys,labelFn){
 const holder=byId(id+'-chart'); if(charts[id])charts[id].destroy();holder.replaceChildren();const canvas=document.createElement('canvas');canvas.setAttribute('aria-label','고용지수 2022년 평균 100');canvas.setAttribute('role','img');holder.append(canvas);
 const times=[...new Set(rows.map(r=>r.time))].sort();const datasets=keys.map((k,i)=>({label:labelFn(k),data:times.map(t=>{const r=rows.find(r=>r.time===t&&r.series===k);return r&&r.index!==null?r.index:null;}),borderColor:colors[i%colors.length],backgroundColor:colors[i%colors.length],pointRadius:times.length>30?0:3,borderWidth:2,spanGaps:false}));
 datasets.push({label:'2022년 평균 100',data:times.map(()=>100),borderColor:'#99a7ae',borderDash:[5,5],pointRadius:0,borderWidth:1});
 charts[id]=new Chart(canvas,{type:'line',data:{labels:times,datasets},options:{animation:false,responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},plugins:{legend:{position:'bottom'},tooltip:{callbacks:{afterLabel:ctx=>{const r=rows.find(r=>r.time===times[ctx.dataIndex]&&labelFn(r.series)===ctx.dataset.label);return r&&r.employment!=null?'가중 취업자 '+Math.round(r.employment).toLocaleString()+'명':'';}}}},scales:{y:{title:{display:true,text:'고용지수 · 2022년 평균 = 100'}},x:{ticks:{maxTicksLimit:10,maxRotation:0},title:{display:true,text:times.length>30?'조사연월':'연도 또는 실제 조사연월'}}}}});
 const wrap=byId(id+'-table');wrap.replaceChildren();const table=document.createElement('table');const cap=document.createElement('caption');cap.textContent='지수 · 빈칸은 표본 또는 기준기간 부족으로 미표시';table.append(cap);const thead=table.createTHead();let tr=thead.insertRow();for(const text of ['시점',...keys.map(labelFn)]){const th=document.createElement('th');th.textContent=text;tr.append(th);}const body=table.createTBody();for(const t of times){tr=body.insertRow();tr.insertCell().textContent=t;for(const k of keys){const r=rows.find(r=>r.time===t&&r.series===k);tr.insertCell().textContent=r&&r.index!=null?r.index.toFixed(1):'';}}wrap.append(table);
}
Promise.all(['meta','res','monthly'].map(n=>fetch('data/'+n+'.json').then(r=>{if(!r.ok)throw Error('자료 로드 실패');return r.json();}))).then(([meta,res,monthly])=>{
 const ages=[['All','전체 15세 이상'],...meta.ages.map(a=>[a,a+'세'])],sexes=Object.entries(sexNames),freq=[['annual','연도별 · 4월·10월 평균'],['wave','실제 조사시점 · 4월·10월']];
 for(const id of ['exp-age','sex-age'])options(id,ages,id==='exp-age'?'All':'22–25');
 for(const id of ['exp-sex','occ-sex','ind-sex','mon-sex'])options(id,sexes,'All');
 for(const id of ['exp-freq','occ-freq','sex-freq','ind-freq'])options(id,freq,'annual');
 const inds=[['All','전체 산업'],...meta.industries.map(x=>['industry_'+x.id,x.id+' · '+x.name])];options('exp-ind',inds,'All');options('sex-ind',inds,'All');
 options('ind-id',meta.industries.map(x=>[x.id,x.id+' · '+x.name]),'62');options('occ-id',meta.occupations.map(x=>[x.id,x.id+' · '+x.name]),'222');options('sex-q',[1,2,3,4,5].map(i=>['Q'+i,'Q'+i+(i===5?' · 가장 높음':i===1?' · 가장 낮음':'')]),'Q5');options('mon-freq',[['monthly','월별 · 관측치'],['annual','연도별 · 12개월 평균']],'monthly');
 byId('coverage').textContent='지역별고용조사 취업자 중 THAIE 점수가 연결된 비율은 조사시점별 '+meta.coverage_min.toFixed(2)+'–'+meta.coverage_max.toFixed(2)+'%입니다. 연결되지 않은 직업은 분위 비교에서 제외합니다.';
 const renderers={
 exp:()=>render('exp',res.filter(r=>r.kind==='exposure'&&r.scope===val('exp-ind')&&r.agegroup===val('exp-age')&&r.sex===val('exp-sex')&&r.frequency===val('exp-freq')).map(r=>({...r,series:r.line})),['Q1','Q2','Q3','Q4','Q5'],k=>k+(k==='Q5'?' · 높은 THAIE':k==='Q1'?' · 낮은 THAIE':'')),
 occ:()=>{const o=meta.occupations.find(x=>x.id===val('occ-id'));byId('occ-score').textContent=o.name+' · 고정 THAIE '+o.score.toFixed(3)+' · 전국 고정 분위 Q'+o.quintile+'. 직업 안에서 노출 분위는 바뀌지 않습니다.';render('occ',res.filter(r=>r.kind==='occupation'&&r.scope===o.id&&meta.ages.includes(r.agegroup)&&r.sex===val('occ-sex')&&r.frequency===val('occ-freq')).map(r=>({...r,series:r.agegroup})),meta.ages,k=>k+'세');},
 sex:()=>render('sex',res.filter(r=>r.kind==='exposure'&&r.scope===val('sex-ind')&&r.agegroup===val('sex-age')&&r.line===val('sex-q')&&r.sex!=='All'&&r.frequency===val('sex-freq')).map(r=>({...r,series:r.sex})),['Male','Female'],k=>sexNames[k]),
 ind:()=>{const i=meta.industries.find(x=>x.id===val('ind-id'));byId('ind-score').textContent=i.name+' · 2022년 직업 구성의 고용 가중 THAIE '+i.score.toFixed(3)+'. 특정 직업을 뜻하는 산업 분류가 아닙니다.';render('ind',res.filter(r=>r.kind==='industry'&&r.scope===i.id&&meta.ages.includes(r.agegroup)&&r.sex===val('ind-sex')&&r.frequency===val('ind-freq')).map(r=>({...r,series:r.agegroup})),meta.ages,k=>k+'세');},
 mon:()=>render('mon',monthly.filter(r=>meta.ages.includes(r.agegroup)&&r.sex===val('mon-sex')&&r.frequency===val('mon-freq')).map(r=>({...r,series:r.agegroup})),meta.ages,k=>k+'세')};
 for(const [id,fn] of Object.entries(renderers)){fn();document.querySelectorAll('select[id^="'+id+'-"]').forEach(s=>s.addEventListener('change',fn));}
 document.querySelectorAll('details').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)for(const c of Object.values(charts))c.resize();}));
}).catch(err=>{const p=document.createElement('p');p.className='note';p.textContent='인터랙티브 자료를 불러오지 못했습니다. 정적 그림과 CSV를 이용해 주세요. '+err.message;byId('results').prepend(p);console.error(err);});
