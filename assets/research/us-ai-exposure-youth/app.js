/* Native-SVG explorer for frozen, aggregate CPS data. No microdata or network APIs. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const palette = ['#65758B', '#258F83', '#3977A4', '#8A62AC', '#BB3D43'];
  const dashes = ['7 4', '2 4', '9 3 2 3', '10 4', ''];
  const cache = new Map();
  let metadata, regions, generation = 0, csvURL, currentPanels = [];

  async function getJSON(path) {
    const response = await fetch(path);
    if (!response.ok) throw new Error(`Unable to load ${path} (${response.status})`);
    return response.json();
  }
  async function getState(state) {
    if (cache.has(state)) return cache.get(state);
    const data = await getJSON(`data/state-${state}.json`);
    if (cache.size >= 5) cache.delete(cache.keys().next().value);
    cache.set(state, data);
    return data;
  }
  function element(name, attrs = {}, text) {
    const node = document.createElementNS('http://www.w3.org/2000/svg', name);
    for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function numeric(value) { return value !== null && Number.isFinite(value); }
  function format(value) { return numeric(value) ? value.toLocaleString('en-GB', {maximumFractionDigits: 2}) : ''; }
  function niceStep(range) {
    const raw = range / 4, power = 10 ** Math.floor(Math.log10(raw));
    const fraction = raw / power;
    return (fraction <= 1 ? 1 : fraction <= 2 ? 2 : fraction <= 5 ? 5 : 10) * power;
  }
  function drawChart(index, panel) {
    $(`title-${index}`).textContent = `${panel.title} (${panel.unit})`;
    const host = $(`chart-${index}`);
    const width = Math.max(260, host.clientWidth || 500), height = 315;
    const margin = {left: 58, right: 18, top: 25, bottom: 45};
    const innerW = width - margin.left - margin.right;
    const innerH = height - margin.top - margin.bottom;
    const values = panel.series.flatMap(s => s.y.filter(numeric));
    host.classList.remove('loading');
    if (!values.length) {
      host.textContent = 'No values meet the sample threshold for this selection.';
      return;
    }
    let low = Math.min(...values), high = Math.max(...values);
    const pad = Math.max((high - low) * .12, Math.abs(high) * .015, .2);
    low = Math.max(0, low - pad); high += pad;
    const step = niceStep(high - low);
    low = Math.floor(low / step) * step; high = Math.ceil(high / step) * step;
    const x = year => margin.left + (year - 2010) / 16 * innerW;
    const y = value => margin.top + (high - value) / (high - low) * innerH;
    const svg = element('svg', {viewBox: `0 0 ${width} ${height}`, role: 'img', 'aria-labelledby': `svg-title-${index} svg-desc-${index}`});
    svg.append(element('title', {id: `svg-title-${index}`}, panel.title));
    svg.append(element('desc', {id: `svg-desc-${index}`}, `Annual January–September observations, 2010–2026. Unit ${panel.unit}. Highest exposure is Q5. Numeric values are available in the table below.`));
    svg.append(element('rect', {x: x(2019.7), y: margin.top, width: x(2020.3) - x(2019.7), height: innerH, fill: '#65758B', opacity: '.09'}));
    for (let tick = low; tick <= high + step / 100; tick += step) {
      svg.append(element('line', {x1: margin.left, x2: width - margin.right, y1: y(tick), y2: y(tick), stroke: '#ded8c9', 'stroke-width': '.7'}));
      svg.append(element('text', {x: margin.left - 9, y: y(tick) + 5, 'text-anchor': 'end', fill: '#565953', 'font-size': 14}, format(tick)));
    }
    const ticks = width < 420 ? [2010, 2018, 2026] : [2010, 2014, 2018, 2022, 2026];
    for (const tick of ticks) svg.append(element('text', {x: x(tick), y: height - 17, 'text-anchor': 'middle', fill: '#565953', 'font-size': 14}, tick));
    svg.append(element('line', {x1: x(2022.5), x2: x(2022.5), y1: margin.top, y2: margin.top + innerH, stroke: '#596778', 'stroke-dasharray': '3 4'}));
    for (const series of panel.series) {
      let path = '', connected = false;
      series.x.forEach((year, i) => {
        const value = series.y[i];
        if (!numeric(value)) { connected = false; return; }
        path += `${connected ? 'L' : 'M'}${x(year).toFixed(2)},${y(value).toFixed(2)} `;
        connected = true;
      });
      svg.append(element('path', {d: path.trim(), fill: 'none', 'aria-hidden': 'true', stroke: series.color, 'stroke-width': series.name === 'Q5' ? 3 : 1.8, 'stroke-dasharray': series.dash || ''}));
      series.x.forEach((year, i) => {
        if (!numeric(series.y[i])) return;
        const dot = element('circle', {cx: x(year), cy: y(series.y[i]), r: year === 2026 ? 3.8 : 2.2, fill: series.color, 'aria-hidden': 'true'});
        dot.append(element('title', {}, `${series.name}, ${year}, ${format(series.y[i])} ${panel.unit}`));
        svg.append(dot);
      });
    }
    host.replaceChildren(svg);
  }
  function series(rows, column, name, color, dash = '', index = false, yearColumn = 1) {
    rows = rows.slice().sort((a, b) => a[yearColumn] - b[yearColumn]);
    const baseline = index ? rows.find(row => row[yearColumn] === 2022)?.[column] : 1;
    const byYear = new Map(rows.map(row => [row[yearColumn], row]));
    return {name, color, dash, x: metadata.years,
      y: metadata.years.map(year => {
        const row = byYear.get(year);
        return !row || !numeric(row[column]) || (index && !(baseline > 0)) ? null : row[column] * (index ? 100 / baseline : 100);
      })};
  }
  function renderLegend(allSeries) {
    $('legend').replaceChildren(...allSeries.map(item => {
      const span = document.createElement('span'), line = document.createElement('i');
      line.className = 'swatch'; line.style.color = item.color; span.append(line, document.createTextNode(item.name === 'Q5' ? 'Q5 highest' : item.name === 'Q1' ? 'Q1 lowest' : item.name));
      return span;
    }));
  }
  function tableAndCSV(panels, state, age, measure, view) {
    const headers = ['Year'];
    const all = [];
    for (const panel of panels) for (const item of panel.series) {
      headers.push(`${panel.title} ${item.name} (${panel.unit})`); all.push(item);
    }
    const rows = metadata.years.map(year => [year, ...all.map(item => {
      const index = item.x.indexOf(year); return index < 0 ? null : item.y[index];
    })]);
    const table = document.createElement('table'), head = document.createElement('thead'), tr = document.createElement('tr');
    headers.forEach(label => { const th = document.createElement('th'); th.scope = 'col'; th.textContent = label; tr.append(th); });
    head.append(tr); table.append(head);
    const body = document.createElement('tbody');
    rows.forEach(row => { const tr = document.createElement('tr'); row.forEach(value => { const td = document.createElement('td'); td.textContent = format(value); tr.append(td); }); body.append(tr); });
    table.append(body); $('chart-table').replaceChildren(table);
    const quote = value => value === null ? '' : `"${String(value).replaceAll('"', '""')}"`;
    const csv = [headers, ...rows].map(row => row.map(quote).join(',')).join('\r\n');
    if (csvURL) URL.revokeObjectURL(csvURL);
    csvURL = URL.createObjectURL(new Blob([csv], {type: 'text/csv;charset=utf-8'}));
    $('download-chart').href = csvURL;
    $('download-chart').download = `${view}-${state}-${age}-${measure}-2010-2026.csv`;
  }
  async function update() {
    const token = ++generation;
    let state = $('geography').value, age = $('age').value;
    const measure = $('measure').value, view = $('view').value;
    $('geography').disabled = view === 'region';
    $('age').disabled = view === 'quality';
    $('measure').disabled = view === 'overall';
    if (view === 'region') {state = '0'; $('geography').value = state;}
    if (view === 'quality') {age = 'age22_25'; $('age').value = age;}
    const data = view === 'region' ? null : await getState(state);
    if (token !== generation) return;
    let panels, note;
    if (view === 'overall') {
      const rows = data.overall.filter(row => row[0] === age);
      panels = [{title: 'Employment-to-population ratio', unit: '%', series: [series(rows, 2, 'All workers', palette[2])]},
                {title: 'Unemployment rate', unit: '%', series: [series(rows, 3, 'All workers', palette[4])]}];
      note = 'All people in the selected age group are included. National rates use summed survey-weighted numerators and denominators. These are observed rates, not adjusted DID estimates.';
    } else {
      const rows = (view === 'region' ? regions : data.occupation).filter(row => row[0] === age && row[2] === measure && row[3] > 0);
      const make = (column, index) => [1,2,3,4,5].map(q => series(rows.filter(row => row[3] === q), column, `Q${q}`, palette[q-1], dashes[q-1], index));
      if (view === 'quality') {
        panels = [{title: 'Full-time employment', unit: '2022 = 100', series: make(7, true)},
                  {title: 'Part-time employment', unit: '2022 = 100', series: make(8, true)},
                  {title: 'Real median weekly earnings', unit: 'September 2026 USD', series: [1,2,3,4,5].map(q => {
                    const w = data.wages.filter(row => row[1] === measure && row[2] === q).sort((a,b) => a[0]-b[0]);
                    const byYear = new Map(w.map(row => [row[0], row[3]]));
                    return {name: `Q${q}`, color: palette[q-1], dash: dashes[q-1], x: metadata.years, y: metadata.years.map(year => byYear.get(year) ?? null)};
                  })}];
        note = 'Ages 22–25 only. Employment indices use each quintile’s 2022 value. Earnings medians are suppressed below 30 ORG person-months; gaps are not interpolated. Full-time and part-time do not identify contract permanence.';
      } else {
        panels = [{title: view === 'region' ? 'Employment-to-population ratio' : 'Occupational employment / age-group population', unit: '%', series: make(4, false)},
                  {title: view === 'region' ? 'Unemployment rate' : 'Previous-occupation conditional unemployment rate', unit: '%', series: make(5, false)}];
        if (view === 'region') note = 'The five regional groups use fixed 2019 state/DC scores. Each curve pools all people in those regions. Select another view to inspect a single state. Quintiles contain roughly equal numbers of regions, not equal populations.';
        else {
          note = 'Occupational employment contribution is not an occupation-specific employment rate. Conditional unemployment excludes new entrants and other people without a linked previous occupation. Unmatched Q0 is excluded from these five curves, but retained in overall regional rates.';
        }
      }
    }
    currentPanels = panels;
    const geoName = metadata.states.find(item => String(item.id) === state)?.name || 'United States';
    const ageName = metadata.ages.find(item => item.id === age)?.label || age;
    $('trend-status').textContent = `${view === 'region' ? 'United States regional quintiles' : geoName} · ages ${ageName}${view === 'overall' ? '' : ' · '+measure}. ${note}`;
    for (let i = 1; i <= 3; i++) {
      $(`panel-${i}`).hidden = i > panels.length;
      if (i <= panels.length) drawChart(i, panels[i-1]);
    }
    renderLegend(panels[0].series);
    tableAndCSV(panels, state, age, measure, view);
  }
  function showError(error) {
    $('trend-status').textContent = `The explorer could not load the selected data. ${error.message}. CSV downloads and the figures PDF remain available below.`;
    console.error(error);
  }
  async function init() {
    [metadata, regions] = await Promise.all([getJSON('data/metadata.json'), getJSON('data/regions.json')]);
    $('geography').replaceChildren(...metadata.states.map(item => new Option(item.name, String(item.id))));
    $('age').replaceChildren(...metadata.ages.map(item => new Option(item.label, item.id)));
    $('age').value = 'age22_25';
    for (const id of ['geography','age','measure','view']) $(id).addEventListener('change', () => update().catch(showError));
    let resize;
    window.addEventListener('resize', () => {clearTimeout(resize); resize = setTimeout(() => currentPanels.forEach((panel, i) => drawChart(i+1, panel)), 120);});
    await update();
  }
  init().catch(showError);
})();
