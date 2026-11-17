'use strict';
(async()=>{
 const chart=document.getElementById('labour-chart');if(!chart)return;
 const response=await fetch('labour_2025/manuscript_results.json');
 if(!response.ok){chart.outerHTML='<p>Employment data could not load. Downloadable figures remain available.</p>';return;}
 const data=await response.json(),pop=document.getElementById('labour-population'),unit=document.getElementById('labour-unit');
 function draw(){
  const rows=data.trends.filter(r=>r.stratum===pop.value),index=unit.value==='index',value=r=>index?r.index:r.emp/1e6,max=Math.max(...rows.map(value))*1.1,x=y=>90+(y-2013)/12*850,y=v=>355-v/max*290;
  let svg='<rect x="90" y="65" width="850" height="290" fill="#fcfbf7"/>';
  svg+=`<rect x="${x(2020)}" y="65" width="${x(2023)-x(2020)}" height="290" fill="#dfe4df" opacity="0.6"/>`;
  for(let i=0;i<=4;i++){const v=max*i/4;svg+=`<path d="M90 ${y(v)}H940" stroke="#d8dfdd"/><text x="76" y="${y(v)+5}" text-anchor="end" font-size="16">${v.toFixed(index?0:2)}</text>`;}
  for(const yr of [2013,2016,2019,2022,2025])svg+=`<text x="${x(yr)}" y="383" text-anchor="middle" font-size="16">${yr}</text>`;
  svg+=`<path d="M${x(2023)} 65V355" stroke="#6f7778" stroke-dasharray="5 5"/>`;
  for(const [group,colour,offset] of [['High','#bf454e',0],['Low','#257daf',260]]){
   const series=rows.filter(r=>r.group===group).sort((a,b)=>a.year-b.year);
   svg+=`<polyline points="${series.map(r=>`${x(r.year)},${y(value(r))}`).join(' ')}" fill="none" stroke="${colour}" stroke-width="3"/>`;
   for(const r of series)svg+=`<circle cx="${x(r.year)}" cy="${y(value(r))}" r="4" fill="${colour}"><title>${data.labels[r.stratum]} | ${group} exposure | ${r.year} | ${Math.round(r.emp).toLocaleString('en-GB')} employed persons | index ${r.index.toFixed(1)}</title></circle>`;
   svg+=`<path d="M${100+offset} 25h35" stroke="${colour}" stroke-width="3"/><text x="${145+offset}" y="31" font-size="17">${group} exposure</text>`;
  }
  chart.innerHTML=svg+`<text x="515" y="425" text-anchor="middle" font-size="17">${data.labels[pop.value]} · ${index?'Employment index, 2022 = 100':'Employed persons, millions'}</text>`;
  document.getElementById('labour-summary').textContent='2022–2025 annual-average change. '+data.growth.filter(r=>r.stratum===pop.value).map(r=>`${r.group} exposure ${r.growth_pct>=0?'+':''}${r.growth_pct.toFixed(1)}%`).join('; ')+'. Fixed 2025 quintiles. Hover over a point for the estimate.';
 }
 pop.addEventListener('change',draw);unit.addEventListener('change',draw);draw();
})();
