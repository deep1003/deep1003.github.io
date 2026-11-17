'use strict';
(async()=>{
 const chart=document.getElementById('degree-chart');if(!chart)return;
 const response=await fetch('degree_2025/degree_results.json');if(!response.ok){chart.outerHTML='<p>Downloadable degree figures remain available.</p>';return;}
 const data=await response.json(),degree=document.getElementById('degree-population'),unit=document.getElementById('degree-unit');
 function draw(){
  const rows=data.trends.filter(r=>r.ed===degree.value),indexed=unit.value==='index';
  const bases=Object.fromEntries(rows.filter(r=>r.year===2022).map(r=>[r.group,r.emp]));
  const value=r=>indexed?100*r.emp/bases[r.group]:r.emp/1000,max=Math.max(...rows.map(value))*1.1,x=year=>90+(year-2013)/12*850,y=v=>355-v/max*290;
  let svg='<rect x="90" y="65" width="850" height="290" fill="#fcfbf7"/>';
  svg+=`<rect x="${x(2020)}" y="65" width="${x(2023)-x(2020)}" height="290" fill="#dfe4df" opacity="0.6"/>`;
  for(let i=0;i<=4;i++){const v=max*i/4;svg+=`<path d="M90 ${y(v)}H940" stroke="#d8dfdd"/><text x="76" y="${y(v)+5}" text-anchor="end" font-size="16">${v.toLocaleString('en-GB',{maximumFractionDigits:1})}</text>`;}
  for(const year of [2013,2016,2019,2022,2025])svg+=`<text x="${x(year)}" y="383" text-anchor="middle" font-size="16">${year}</text>`;
  svg+=`<path d="M${x(2023)} 65V355" stroke="#6f7778" stroke-dasharray="5 5"/>`;
  for(const [group,colour,offset] of [['High','#bf454e',0],['Low','#257daf',260]]){
   const series=rows.filter(r=>r.group===group).sort((a,b)=>a.year-b.year);
   svg+=`<polyline points="${series.map(r=>`${x(r.year)},${y(value(r))}`).join(' ')}" fill="none" stroke="${colour}" stroke-width="3"/>`;
   for(const r of series)svg+=`<circle cx="${x(r.year)}" cy="${y(value(r))}" r="4" fill="${colour}"><title>${data.labels[r.ed]} | ${group} exposure | ${r.year} | ${Math.round(r.emp).toLocaleString('en-GB')} employed persons</title></circle>`;
   svg+=`<path d="M${100+offset} 25h35" stroke="${colour}" stroke-width="3"/><text x="${145+offset}" y="31" font-size="17">${group} exposure</text>`;
  }
  chart.innerHTML=svg+`<text x="515" y="425" text-anchor="middle" font-size="17">${data.labels[degree.value]} · ${indexed?'Employment index, 2022 = 100':'Employed persons, thousands'}</text>`;
  const s=data.summary.find(r=>r.degree===degree.value);
  document.getElementById('degree-summary').textContent=`2022–2025. High exposure +${s.high_growth.toFixed(1)}% (${Math.round(s.high_2022).toLocaleString('en-GB')} to ${Math.round(s.high_2025).toLocaleString('en-GB')}); low exposure +${s.low_growth.toFixed(1)}% (${Math.round(s.low_2022).toLocaleString('en-GB')} to ${Math.round(s.low_2025).toLocaleString('en-GB')}). All-age employment stocks.`;
 }
 degree.addEventListener('change',draw);unit.addEventListener('change',draw);draw();
})();
