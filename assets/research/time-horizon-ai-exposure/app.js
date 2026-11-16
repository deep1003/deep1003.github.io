'use strict';
(() => {
  const $ = id => document.getElementById(id);
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const fmt = n => Number(n).toLocaleString('en-GB', {maximumFractionDigits:0});
  const models = ['gpt4_2023','claude37_2025','gpt5_2025','opus46_2026'];
  const names = ['GPT-4 (2023)','Claude 3.7 Sonnet (2025)','GPT-5 (2025)','Claude Opus 4.6 (2026)'];
  const pageSize = 10;
  const plot = {left:78, top:20, width:990, height:375, xMax:210, yMax:0.72};
  let occupations = [], tasks = [], columns = [], meta = {}, byOcc = {}, filtered = [], page = 0;
  let tasksReady = false, colourMax = 1, maxEmployment = 1;
  let zoom = {k:1, x:0, y:0}, drag = null, dragged = false;
  const model = () => $('model').value;
  const modelIndex = () => models.indexOf(model());
  const isTasks = () => $('unit').value === 'tasks';
  const groupName = g => ({short:'Short-task, high exposure',long:'Long-task, high exposure',other:'Other occupations'}[g] || 'Unmapped');
  const ranks = o => ({content:o.rankContent, horizon:o['rank_' + model()], gain:o.rankContent-o['rank_' + model()]});
  const taskScore = r => r[7 + modelIndex()];
  const areaRadius = employment => 28 * Math.sqrt(employment/maxEmployment);

  function colour(value) {
    const stops = [[15,10,38],[85,32,109],[181,54,79],[245,135,48],[252,246,164]];
    const t = Math.max(0, Math.min(1, value/colourMax))*4;
    const i = Math.min(3, Math.floor(t)), f = t-i;
    return `rgb(${stops[i].map((c,j)=>Math.round(c+(stops[i+1][j]-c)*f)).join(',')})`;
  }
  function download(file, headers, rows) {
    const quote = x => '"'+String(x??'').replace(/"/g,'""')+'"';
    const data = '\ufeff'+[headers,...rows].map(row=>row.map(quote).join(',')).join('\r\n');
    const url = URL.createObjectURL(new Blob([data],{type:'text/csv;charset=utf-8'}));
    const a = document.createElement('a'); a.href=url; a.download=file; a.click();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  function occupationRows(list) {
    return list.map(o=>[o.code,o.name,o.content,o[model()],o.minutes,o.employment,o.rankContent,o['rank_'+model()],o.group,model()]);
  }
  const occupationHeaders = ['ksco8_3','occupation_author_translation','content_bge','horizon_bge','predicted_human_minutes','employment_mean_2023_2025','content_rank_all162','horizon_rank_all162','group','model_snapshot'];

  const representativeLabels = [
    ['531','Telecom sales'], ['224','Data professionals'],
    ['222','Software professionals'], ['269','Other education professionals'],
    ['261','University lecturers'], ['331','Accounting clerks'],
    ['510','Sales representatives'], ['244','Nurses'],
    ['262','School teachers'], ['263','Kindergarten teachers'],
    ['611','Crop growers'], ['872','Drivers'],
    ['941','Cleaners'], ['922','Delivery workers'], ['451','Cooks']
  ];

  function mapLabels(sx, sy) {
    const nodes = occupations.map(o => ({x:sx(o.minutes),y:sy(o.content),r:areaRadius(o.employment)}));
    const placed = [];
    const overlaps = (a,b) => a.x < b.x+b.w+5 && a.x+a.w+5 > b.x && a.y < b.y+b.h+4 && a.y+a.h+4 > b.y;
    const marks = [];
    for (const [code,label] of representativeLabels) {
      const o = byOcc[code];
      if (!o) continue;
      const x=sx(o.minutes),y=sy(o.content),radius=areaRadius(o.employment);
      if (x < plot.left || x > plot.left+plot.width || y < plot.top || y > plot.top+plot.height) continue;
      const w=label.length*6.1+10,h=19;
      let best=null;
      // Score nearby, straight-line placements, excluding previous label boxes.
      for (const distance of [radius+10,radius+27,radius+47,radius+72,radius+105,radius+140]) {
        for (const [dx,dy] of [[0,-1],[1,-0.65],[-1,-0.65],[1,0],[-1,0],[0,1],[1,0.75],[-1,0.75]]) {
          const box={x:x+dx*distance-w/2,y:y+dy*distance-h/2,w,h};
          if (box.x < plot.left+3 || box.x+w > plot.left+plot.width-3 || box.y < plot.top+2 || box.y+h > plot.top+plot.height-2 || placed.some(b=>overlaps(box,b))) continue;
          let obstruction=0;
          for (const n of nodes) {
            const nearX=Math.max(box.x,Math.min(n.x,box.x+w));
            const nearY=Math.max(box.y,Math.min(n.y,box.y+h));
            const separation=Math.hypot(n.x-nearX,n.y-nearY);
            if (separation < n.r+3) obstruction += (n.r+3-separation)*20;
          }
          const cost=distance+obstruction+(dy>0?8:0);
          if (!best || cost < best.cost) best={...box,cost};
        }
      }
      if (!best) continue;
      placed.push(best);
      const endX=Math.max(best.x,Math.min(x,best.x+best.w));
      const endY=Math.max(best.y,Math.min(y,best.y+best.h));
      const length=Math.hypot(endX-x,endY-y);
      const startX=x+(endX-x)*Math.min(1,radius/Math.max(length,1));
      const startY=y+(endY-y)*Math.min(1,radius/Math.max(length,1));
      const line=length>radius+4?`<line x1="${startX}" y1="${startY}" x2="${endX}" y2="${endY}" class="label-leader"/>`:'';
      marks.push(`<g data-label="${code}" class="occupation-label">${line}<text x="${best.x+best.w/2}" y="${best.y+13}" text-anchor="middle">${esc(label)}</text></g>`);
    }
    return marks.join('');
  }

  function renderMap() {
    const sx = v => plot.left + zoom.x + v/plot.xMax*plot.width*zoom.k;
    const sy = v => plot.top + zoom.y + (1-v/plot.yMax)*plot.height*zoom.k;
    const grid = [];
    for(let i=0;i<=5;i++) {
      const x = plot.left+i*plot.width/5;
      const v = ((i*plot.width/5-zoom.x)/(plot.width*zoom.k))*plot.xMax;
      grid.push(`<line x1="${x}" x2="${x}" y1="${plot.top}" y2="${plot.top+plot.height}" stroke="#e2e7e2"/><text x="${x}" y="${plot.top+plot.height+25}" text-anchor="middle">${v.toFixed(zoom.k>3?1:0)}</text>`);
      const y = plot.top+i*plot.height/5;
      const e = (1-(i*plot.height/5-zoom.y)/(plot.height*zoom.k))*plot.yMax;
      grid.push(`<line x1="${plot.left}" x2="${plot.left+plot.width}" y1="${y}" y2="${y}" stroke="#e2e7e2"/><text x="${plot.left-12}" y="${y+4}" text-anchor="end">${e.toFixed(2)}</text>`);
    }
    const dots = [...occupations].sort((a,b)=>b.employment-a.employment).map(o=>`<circle data-occ="${o.code}" cx="${sx(o.minutes)}" cy="${sy(o.content)}" r="${areaRadius(o.employment)}" fill="${colour(o[model()])}" fill-opacity="0.9" stroke="#53505a" stroke-width="0.7" tabindex="0" role="button" aria-label="${esc(o.name)}, content ${o.content.toFixed(3)}, horizon ${o[model()].toFixed(3)}, human minutes ${o.minutes.toFixed(1)}, employment ${fmt(o.employment)}"></circle>`).join('');
    $('occupation-map').innerHTML = `<desc>Task duration and AI exposure across 162 occupations. Hover details are provided by the custom information panel.</desc><defs><clipPath id="plot-clip"><rect x="${plot.left}" y="${plot.top}" width="${plot.width}" height="${plot.height}"/></clipPath></defs><rect x="${plot.left}" y="${plot.top}" width="${plot.width}" height="${plot.height}" fill="#fafbf8"/>${grid.join('')}<g clip-path="url(#plot-clip)">${dots}${mapLabels(sx,sy)}</g><text x="${plot.left+plot.width/2}" y="460" text-anchor="middle" class="axis-label">Predicted human task duration (minutes)</text><text transform="translate(20 ${plot.top+plot.height/2}) rotate(-90)" text-anchor="middle" class="axis-label">Content AI exposure (BGE-M3)</text>`;
    $('zoom-level').textContent = Math.round(zoom.k*100)+'%';
    $('map-status').textContent = `${occupations.length} occupations · ${names[modelIndex()]}`;
    $('colour-max').textContent = colourMax.toFixed(3)+' · higher';
    $('size-legend').innerHTML = `<span>Employment · proportional area</span><svg viewBox="0 0 250 65" aria-label="Node area proportional to employment">${[10000,100000,1000000].map((v,i)=>`<circle cx="${35+i*85}" cy="22" r="${areaRadius(v)}" fill="none" stroke="#69767b"/><text x="${35+i*85}" y="58" text-anchor="middle" font-size="11">${fmt(v)}</text>`).join('')}</svg>`;
  }
  function zoomAt(factor, px=plot.width/2, py=plot.height/2) {
    const k = Math.min(10,Math.max(1,zoom.k*factor));
    const ratio = k/zoom.k;
    zoom.x = Math.max(plot.width*(1-k), Math.min(0,px-(px-zoom.x)*ratio));
    zoom.y = Math.max(plot.height*(1-k), Math.min(0,py-(py-zoom.y)*ratio));
    zoom.k=k; $('map-tooltip').hidden=true; renderMap();
  }
  function point(event) {
    const p = $('occupation-map').createSVGPoint(); p.x=event.clientX; p.y=event.clientY;
    return p.matrixTransform($('occupation-map').getScreenCTM().inverse());
  }
  function tooltip(event) {
    const circle = event.target.closest('[data-occ]');
    if(!circle || drag) { $('map-tooltip').hidden=true; return; }
    const o=byOcc[circle.dataset.occ], tip=$('map-tooltip');
    tip.innerHTML=`<strong>${esc(o.name)}</strong><br>KSCO ${o.code}<br>Human duration ${o.minutes.toFixed(1)} min<br>Content exposure ${o.content.toFixed(3)}<br>Time-horizon exposure ${o[model()].toFixed(3)}<br>Employment ${fmt(o.employment)} persons<br><span>Select to inspect the occupation.</span>`;
    const box=circle.getBoundingClientRect();
    tip.style.left=Math.max(8,Math.min(innerWidth-300,(event.clientX||box.x)+14))+'px';
    tip.style.top=Math.max(8,Math.min(innerHeight-210,(event.clientY||box.y)+14))+'px'; tip.hidden=false;
  }
  function selectOccupation(code) {
    const o=byOcc[code], r=ranks(o); $('selected-occupation').hidden=false;
    $('selected-occupation').innerHTML=`<div><strong>${esc(o.name)}</strong><span>KSCO ${o.code} · ${esc(groupName(o.group))}</span></div><p>Content ${o.content.toFixed(3)} (rank ${r.content}) · Horizon ${o[model()].toFixed(3)} (rank ${r.horizon}) · Human duration ${o.minutes.toFixed(1)} min · Employment ${fmt(o.employment)}</p><button id="view-selected-tasks" data-code="${o.code}">View this occupation’s tasks</button>`;
  }
  function filterRecords() {
    const term=$('search').value.trim().toLocaleLowerCase(), code=$('occupation').value, scope=$('coverage').value;
    const accepted=(g,mapped)=>scope==='all'||scope==='unmapped'&&!mapped||scope==='high'&&(g==='short'||g==='long')||scope===g;
    filtered = isTasks() ? tasks.filter(r=>(!code||r[2]===code)&&(!term||r.searchText.includes(term))&&accepted(byOcc[r[2]]?.group,!!r[2])) : occupations.filter(o=>(!code||o.code===code)&&(!term||o.searchText.includes(term))&&accepted(o.group,true));
    const order=$('sort').value;
    filtered.sort((a,b)=> {
      if(order==='id') return isTasks()?a[0].localeCompare(b[0])||a[1]-b[1]:a.code.localeCompare(b.code);
      if(isTasks()) return order==='content'?b[5]-a[5]:order==='minutes'?b[6]-a[6]:taskScore(b)-taskScore(a);
      return order==='content'?b.content-a.content:order==='minutes'?b.minutes-a.minutes:order==='employment'?b.employment-a.employment:order==='gap'?Math.abs(ranks(b).gain)-Math.abs(ranks(a).gain)||b[model()]-a[model()]:b[model()]-a[model()];
    });
    page=0; renderRecords();
  }
  function renderRecords() {
    const unit=isTasks()?'tasks':'occupations',total=isTasks()?tasks.length:occupations.length,start=page*pageSize;
    $('count').textContent=`${fmt(filtered.length)} of ${fmt(total)} ${unit}`;
    $('download').textContent=`Download filtered ${unit} as CSV`;
    $('download').disabled=isTasks()&&!tasksReady;
    $('scenario').textContent=`${names[modelIndex()]} · ${meta.curves?.[model()]?.h50_min ?? 718.8} human-minute 50% horizon · showing ${unit} · ten per page`;
    $('records-head').innerHTML=isTasks()?'<tr><th>Source task / occupation</th><th>Original task statement</th><th>Content exposure</th><th>Human minutes</th><th>Horizon exposure</th><th>Details</th></tr>':'<tr><th>KSCO / occupation</th><th>Human minutes</th><th>Content exposure</th><th>Horizon exposure</th><th>Horizon rank</th><th>Employment</th><th>Details</th></tr>';
    $('records-body').innerHTML=filtered.slice(start,start+pageSize).map(r=>isTasks()?`<tr><td class="task-meta"><code>${esc(r[0])}/${r[1]}</code><span>${esc(byOcc[r[2]]?.name||'Unmapped occupation')}</span><span lang="ko">${esc(r[3])}</span></td><td class="task-text" lang="ko">${esc(r[4])}</td><td class="num">${r[5].toFixed(3)}</td><td class="num">${r[6].toFixed(1)}</td><td class="num">${taskScore(r).toFixed(3)}</td><td><button class="row-button" data-task="${r.index}" aria-label="Open task ${esc(r[0])} sentence ${r[1]}">Open</button></td></tr>`:`<tr><td><code>${r.code}</code><strong class="occupation-name">${esc(r.name)}</strong><span class="small">${r.tasks} tasks · ${esc(groupName(r.group))}</span></td><td class="num">${r.minutes.toFixed(1)}</td><td class="num">${r.content.toFixed(3)}</td><td class="num"><strong>${r[model()].toFixed(3)}</strong></td><td class="num">${r['rank_'+model()]}</td><td class="num">${fmt(r.employment)}</td><td><button class="row-button" data-occupation="${r.code}" aria-label="Open occupation ${r.code}">Open</button></td></tr>`).join('') || `<tr><td colspan="7">${isTasks()&&!tasksReady?'Task records are still loading…':'No records match these filters. Try a shorter search or reset the filters.'}</td></tr>`;
    $('page-info').textContent=filtered.length?`${fmt(start+1)}–${fmt(Math.min(start+pageSize,filtered.length))} · page ${page+1} of ${Math.ceil(filtered.length/pageSize)}`:'No matching records';
    $('prev').disabled=page===0; $('next').disabled=start+pageSize>=filtered.length;
  }
  function showTask(index) {
    const r=tasks[index],o=byOcc[r[2]];
    $('record-detail').innerHTML=`<h2>${esc(o?.name||'Unmapped occupation')}</h2><p><code>${esc(r[0])}/${r[1]}</code> · ${esc(r[3])}</p><blockquote class="source-quote" lang="ko">${esc(r[4])}</blockquote><p>Predicted human completion time <strong>${r[6].toFixed(2)} minutes</strong>. BGE content exposure <strong>${r[5].toFixed(6)}</strong>.</p><table><thead><tr><th>Model</th><th>Transferred weight</th><th>Horizon exposure</th></tr></thead><tbody>${models.map((m,i)=>`<tr><td>${names[i]}</td><td>${r[11+i].toFixed(6)}</td><td>${r[7+i].toFixed(6)}</td></tr>`).join('')}</tbody></table><p class="small">Human duration and completion weights are transferred estimates, not observed Korean task completion or agent success. Source IDs use analytical entry numbering and zero-based sentence indices.</p>`;
    $('task-dialog').showModal();
  }
  function showOccupation(code) {
    const o=byOcc[code];
    $('record-detail').innerHTML=`<h2>${esc(o.name)}</h2><p>KSCO ${o.code} · <span lang="ko">${esc(o.sourceName)}</span></p><p>${fmt(o.employment)} employed persons, mean of six 2023–2025 survey waves. Predicted human duration ${o.minutes.toFixed(2)} minutes. Content exposure ${o.content.toFixed(6)}.</p><table><thead><tr><th>Model</th><th>Horizon exposure</th><th>Rank / 162</th></tr></thead><tbody>${models.map((m,i)=>`<tr><td>${names[i]}</td><td>${o[m].toFixed(6)}</td><td>${o['rank_'+m]}</td></tr>`).join('')}</tbody></table><p>${o.tasks} task statements in ${o.entries} dictionary entries. Occupation scores average tasks within entry, then entries within occupation.</p><button class="occupation-tasks" data-code="${o.code}">View ${o.tasks} tasks</button>`;
    $('task-dialog').showModal();
  }
  function renderComparison() {
    const changed=[...occupations].sort((a,b)=>Math.abs(ranks(b).gain)-Math.abs(ranks(a).gain)||b[model()]-a[model()]).slice(0,10);
    const x=r=>410+(r-1)/161*650;
    $('gap-caption').textContent=`Ten largest rank changes · ${names[modelIndex()]}`;
    $('gap-chart').innerHTML=`<title>Ten largest absolute rank changes among 162 occupations</title>${[1,40,80,120,162].map(r=>`<line x1="${x(r)}" x2="${x(r)}" y1="20" y2="445" stroke="#e1e7e2"/><text x="${x(r)}" y="470" text-anchor="middle" font-size="12">${r}</text>`).join('')}<text x="740" y="503" text-anchor="middle" font-size="14">Occupation rank (1 = highest exposure)</text>${changed.map((o,i)=>{const r=ranks(o),y=40+i*42;return `<text x="390" y="${y+4}" text-anchor="end" font-size="12">${esc(o.name.length>48?o.name.slice(0,46)+'…':o.name)}</text><line x1="${x(r.content)}" x2="${x(r.horizon)}" y1="${y}" y2="${y}" stroke="#a0acac" stroke-width="3"/><circle cx="${x(r.content)}" cy="${y}" r="6" fill="#8b959a"/><circle cx="${x(r.horizon)}" cy="${y}" r="6" fill="#087b78"/><text x="${Math.max(x(r.content),x(r.horizon))+10}" y="${y+4}" font-size="11">${Math.abs(r.gain)}</text><title>${esc(o.name)} · ${r.content} → ${r.horizon}</title>`}).join('')}`;
    $('gap-body').innerHTML=changed.map(o=>{const r=ranks(o);return `<tr><td>${esc(o.name)}</td><td class="num">${o.content.toFixed(3)}</td><td class="num">${o[model()].toFixed(3)}</td><td class="num">${r.content}</td><td class="num">${r.horizon}</td><td class="num">${Math.abs(r.gain)}</td></tr>`}).join('');
    const topContent=[...occupations].sort((a,b)=>b.content-a.content).slice(0,10),topHorizon=[...occupations].sort((a,b)=>b[model()]-a[model()]).slice(0,10);
    for(const [id,list,key] of [['content',topContent,'content'],['horizon',topHorizon,model()]]) {
      $(id+'-top-chart').innerHTML=`<title>Top ten occupations by ${id} exposure</title>${list.map((o,i)=>{const y=20+i*36;return `<text x="235" y="${y+12}" text-anchor="end" font-size="11">${esc(o.name.length>32?o.name.slice(0,30)+'…':o.name)}</text><rect x="245" y="${y}" width="${o[key]*380}" height="19" fill="${id==='content'?'#8b959a':'#087b78'}"/><text x="${250+o[key]*380}" y="${y+13}" font-size="11">${o[key].toFixed(3)}</text>`}).join('')}<text x="330" y="403" text-anchor="middle" font-size="12">Exposure score · common scale</text>`;
      $(id+'-top-list').innerHTML=list.map(o=>`<li>${esc(o.name)} <strong>${o[key].toFixed(3)}</strong></li>`).join('');
    }
  }
  function viewTasks(code) {
    $('task-dialog').close(); $('unit').value='tasks';$('occupation').value=code;$('search').value='';$('coverage').value='all';filterRecords();$('search-section').scrollIntoView({behavior:'smooth'});
  }
  async function init() {
    const taskPromise=fetch('tasks.json').then(r=>{if(!r.ok)throw Error('Task data unavailable');return r.json()});
    try {
      [occupations,meta]=await Promise.all(['occupations.json','metadata.json'].map(f=>fetch(f).then(r=>{if(!r.ok)throw Error('Occupation data unavailable');return r.json()})));
      byOcc=Object.fromEntries(occupations.map(o=>[o.code,o]));
      occupations.forEach(o=>o.searchText=[o.code,o.name,o.sourceName].join(' ').toLocaleLowerCase());
      maxEmployment=Math.max(...occupations.map(o=>o.employment));colourMax=Math.max(...occupations.flatMap(o=>models.map(m=>o[m])));
      $('occupation').innerHTML='<option value="">All occupations</option>'+[...occupations].sort((a,b)=>a.name.localeCompare(b.name)).map(o=>`<option value="${o.code}">${esc(o.code+' · '+o.name)}</option>`).join('');
      $('search').disabled=false;$('occupation').disabled=false;renderMap();filterRecords();renderComparison();
      const payload=await taskPromise;tasks=payload.rows;columns=payload.columns;
      tasks.forEach((r,i)=>{r.index=i;r.searchText=[r[0],r[2],r[3],r[4],byOcc[r[2]]?.name].join(' ').toLocaleLowerCase()});tasksReady=true;$('loading').textContent='';if(isTasks())filterRecords();
    } catch(e) {$('loading').textContent='Some data could not be loaded. Please reload the page.';console.error(e);}
  }
  let timer;
  $('search').addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(filterRecords,140)});
  ['unit','occupation','coverage','sort'].forEach(id=>$(id).addEventListener('change',filterRecords));
  $('model').addEventListener('change',()=>{renderMap();filterRecords();renderComparison();$('selected-occupation').hidden=true});
  $('reset').onclick=()=>{$('search').value='';$('occupation').value='';$('coverage').value='all';$('sort').value='horizon';filterRecords()};
  $('prev').onclick=()=>{if(page){page--;renderRecords()}};
  $('next').onclick=()=>{if((page+1)*pageSize<filtered.length){page++;renderRecords()}};
  $('records-body').onclick=e=>{const task=e.target.closest('[data-task]'),occ=e.target.closest('[data-occupation]');if(task)showTask(Number(task.dataset.task));if(occ)showOccupation(occ.dataset.occupation)};
  $('close-dialog').onclick=()=>$('task-dialog').close();
  $('record-detail').onclick=e=>{const b=e.target.closest('[data-code]');if(b)viewTasks(b.dataset.code)};
  $('selected-occupation').onclick=e=>{const b=e.target.closest('[data-code]');if(b)viewTasks(b.dataset.code)};
  $('download').onclick=()=>isTasks()?download('time_horizon_tasks.csv',[...columns,'human_time_status'],filtered.map(r=>[...r,'Transferred prediction, not measured Korean time'])):download('time_horizon_occupations.csv',occupationHeaders,occupationRows(filtered));
  $('comparison-download').onclick=()=>download('occupation_index_comparison.csv',occupationHeaders,occupationRows([...occupations].sort((a,b)=>Math.abs(ranks(b).gain)-Math.abs(ranks(a).gain))));
  $('comparison-mode').onchange=()=>{const top=$('comparison-mode').value==='top';$('gap-view').hidden=top;$('top-view').hidden=!top};
  $('zoom-in').onclick=()=>zoomAt(1.4);$('zoom-out').onclick=()=>zoomAt(1/1.4);$('zoom-reset').onclick=()=>{zoom={k:1,x:0,y:0};renderMap()};
  const svg=$('occupation-map');
  svg.addEventListener('wheel',e=>{e.preventDefault();const p=point(e);zoomAt(e.deltaY<0?1.15:1/1.15,p.x-plot.left,p.y-plot.top)},{passive:false});
  svg.addEventListener('pointerdown',e=>{const p=point(e);drag={id:e.pointerId,x:p.x,y:p.y,tx:zoom.x,ty:zoom.y,code:e.target.closest('[data-occ]')?.dataset.occ};dragged=false;svg.setPointerCapture(e.pointerId)});
  svg.addEventListener('pointermove',e=>{if(drag){const p=point(e);if(Math.abs(p.x-drag.x)+Math.abs(p.y-drag.y)>3)dragged=true;zoom.x=Math.max(plot.width*(1-zoom.k),Math.min(0,drag.tx+p.x-drag.x));zoom.y=Math.max(plot.height*(1-zoom.k),Math.min(0,drag.ty+p.y-drag.y));if(dragged)renderMap()}else tooltip(e)});
  svg.addEventListener('pointerup',e=>{const selected=drag?.code,wasDrag=dragged;drag=null;svg.releasePointerCapture(e.pointerId);if(!wasDrag&&selected)selectOccupation(selected)});
  svg.addEventListener('pointercancel',()=>{drag=null});svg.addEventListener('pointerleave',()=>{$('map-tooltip').hidden=true});svg.addEventListener('focusin',tooltip);
  svg.addEventListener('keydown',e=>{const c=e.target.closest('[data-occ]');if(c&&(e.key==='Enter'||e.key===' ')){e.preventDefault();selectOccupation(c.dataset.occ)}});
  init();
})();
