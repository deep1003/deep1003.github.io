'use strict';
(async()=>{
 const el=document.getElementById('major-time-chart'),select=document.getElementById('major-time-select');if(!el||!select)return;
 const response=await fetch('full_outcomes/major_groups.json');if(!response.ok)return;const data=await response.json();
 function draw(){
  const rows=data.filter(r=>r.major===Number(select.value)),base=rows.find(r=>r.year===2022);
  const defs=[['employed_persons','Employment change'],['linked_rate_pct','Linked unemployment rate change']];
  const series=defs.map(([key,title])=>({key,title,rows:rows.filter(r=>r[key]!==null).map(r=>({...r,value:100*(r[key]/base[key]-1)}))}));
  const values=series.flatMap(s=>s.rows.map(r=>r.value));const lo=10*Math.floor(Math.min(...values)/10)-10,hi=10*Math.ceil(Math.max(...values)/10)+10;
  let html='';
  series.forEach((s,i)=>{
   const left=70+i*550,x=year=>left+(year-2013)/12*420,y=value=>350-(value-lo)/(hi-lo)*270;
   html+=`<text x="${left+210}" y="25" text-anchor="middle" font-size="18" font-weight="bold">${s.title}</text><rect x="${x(2023)}" y="80" width="${x(2025)-x(2023)}" height="270" fill="#e9eeeb"/><path d="M${x(2023)} 80V350" stroke="#657577" stroke-dasharray="5 5"/>`;
   for(let j=0;j<=4;j++){const v=lo+(hi-lo)*j/4;html+=`<path d="M${left} ${y(v)}h420" stroke="#d8dfdd"/><text x="${left-10}" y="${y(v)+4}" text-anchor="end" font-size="13">${v.toFixed(0)}%</text>`;}
   html+=`<path d="M${left} ${y(0)}h420" stroke="#8a9697" stroke-dasharray="3 4"/><polyline points="${s.rows.map(r=>`${x(r.year)},${y(r.value)}`).join(' ')}" fill="none" stroke="#234d64" stroke-width="3"/>`;
   for(const r of s.rows)html+=`<circle cx="${x(r.year)}" cy="${y(r.value)}" r="4" fill="#234d64"><title>${r.year} · relative change ${r.value.toFixed(1)}% · underlying ${s.key==='employed_persons'?r[s.key].toLocaleString('en-GB')+' persons':r[s.key].toFixed(2)+'%'}</title></circle>`;
   for(const yr of [2013,2016,2019,2022,2023,2025])html+=`<text x="${x(yr)}" y="378" text-anchor="middle" font-size="12">${yr}</text>`;
   html+=`<text x="${left+210}" y="55" text-anchor="middle" font-size="14">Relative change (%) · May 2022 = 0</text>`;
  });
  el.innerHTML=html+'<text x="550" y="430" text-anchor="middle" font-size="14">May observations · Ages 15+ · Linked unemployment unavailable in 2013–2014</text>';
 }
 select.addEventListener('change',draw);draw();
})();
