/* Official OECD observations are loaded only when the fiscal-data details is opened. */
(() => {
  'use strict';
  const panel = document.getElementById('fiscal-data');
  if (!panel) return;
  const byId = id => document.getElementById(id);
  const escapeHtml = value => String(value).replace(/[&<>"']/g, character => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[character]));
  const number = (value, digits = 2) => value == null ? '결측' : Number(value).toLocaleString('ko-KR', {maximumFractionDigits: digits, minimumFractionDigits: digits});
  const state = {view: 'trend', country: 'KOR', year: 2023, function: 'GF07', metric: 'share'};
  let data;
  let loading;
  let displayedRows = [];
  let countryMap;
  let functionMap;
  let rowMap;
  const lookup = (country, year, functionCode) => rowMap.get(`${country}|${year}|${functionCode}`);
  const isFlagged = row => row && (row.status !== 'A' || row.total_status !== 'A');
  const statusText = row => row ? `${data.status_labels[row.status] || row.status} / ${data.status_labels[row.total_status] || row.total_status}` : '관측값 없음';

  function fillOptions(element, choices, selected) {
    element.innerHTML = choices.map(choice => `<option value="${escapeHtml(choice.value)}">${escapeHtml(choice.label)}</option>`).join('');
    element.value = String(selected);
  }

  function refreshYears() {
    const years = state.view === 'countries'
      ? [...new Set(data.rows.map(row => row.year))].sort((a, b) => a - b)
      : countryMap.get(state.country).years;
    if (!years.includes(state.year)) state.year = years[years.length - 1];
    fillOptions(byId('fiscal-year'), [...years].reverse().map(year => ({value: year, label: `${year}년`})), state.year);
  }

  function selectView(view) {
    state.view = view;
    document.querySelectorAll('[data-fiscal-view]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.fiscalView === view)));
    byId('fiscal-country-wrap').hidden = view === 'countries';
    byId('fiscal-year-wrap').hidden = view === 'trend';
    byId('fiscal-function-wrap').hidden = view === 'functions';
    byId('fiscal-metric-wrap').hidden = view === 'countries';
    refreshYears();
    render();
  }

  function rowsForView() {
    if (state.view === 'trend') {
      return countryMap.get(state.country).years.map(year => {
        const source = lookup(state.country, year, state.function);
        return {label: String(year), year, source};
      });
    }
    if (state.view === 'functions') {
      return data.functions.map(item => ({label: `${item.code.slice(2)} ${item.name}`, source: lookup(state.country, state.year, item.code)}));
    }
    return data.countries.map(country => ({label: country.name, source: lookup(country.code, state.year, state.function)}))
      .filter(row => row.source && row.source.share != null)
      .sort((a, b) => b.source.share - a.source.share);
  }

  function tooltip(index, event) {
    const row = displayedRows[index];
    if (!row || !row.source) return;
    const source = row.source;
    const element = byId('fiscal-tooltip');
    element.textContent = `${countryMap.get(source.country).name} · ${source.year}년 · ${functionMap.get(source.function).name} | 전체 지출 대비 ${number(source.share)}% | ${number(source.amount)} 백만 ${source.currency} | 원값 / 총지출 상태: ${statusText(source)}`;
    element.hidden = false;
    const box = event.currentTarget.getBoundingClientRect();
    const left = event.type === 'focus' ? box.left : event.clientX;
    const top = event.type === 'focus' ? box.top : event.clientY;
    element.style.left = `${Math.max(8, Math.min(window.innerWidth - element.offsetWidth - 8, left + 12))}px`;
    element.style.top = `${Math.max(8, Math.min(window.innerHeight - element.offsetHeight - 8, top + 12))}px`;
  }

  function bindMarks() {
    byId('fiscal-tooltip').hidden = true;
    byId('fiscal-chart').querySelectorAll('[data-row]').forEach(mark => {
      ['pointerenter', 'pointermove', 'focus'].forEach(type => mark.addEventListener(type, event => tooltip(Number(mark.dataset.row), event)));
      ['pointerleave', 'blur'].forEach(type => mark.addEventListener(type, () => { byId('fiscal-tooltip').hidden = true; }));
    });
  }

  function chart(rows, metric) {
    const values = rows.map(row => row.source && row.source[metric]).filter(value => value != null);
    if (!values.length) return '<p class="notice">이 조건의 관측값이 없습니다. 결측을 0으로 표시하지 않습니다.</p>';
    const width = 900;
    const left = state.view === 'trend' ? 100 : 210;
    const right = metric === 'amount' ? 150 : 100;
    const top = 36;
    const height = state.view === 'trend' ? 420 : Math.max(300, rows.length * 34 + 90);
    const bottom = 56;
    const plotWidth = width - left - right;
    const plotHeight = height - top - bottom;
    const minimum = Math.min(0, ...values);
    const maximum = Math.max(0, ...values) || 1;
    const roughStep = (maximum - minimum) / 4;
    const magnitude = 10 ** Math.floor(Math.log10(roughStep));
    const fraction = roughStep / magnitude;
    const step = (fraction <= 1 ? 1 : fraction <= 2 ? 2 : fraction <= 5 ? 5 : 10) * magnitude;
    const minimumTick = Math.floor(minimum / step) * step;
    const maximumTick = Math.ceil(maximum / step) * step;
    const tickCount = Math.round((maximumTick-minimumTick) / step);
    const scaleX = value => left + plotWidth * (value-minimumTick) / (maximumTick-minimumTick);
    const scaleY = value => height-bottom - plotHeight * (value-minimumTick) / (maximumTick-minimumTick);
    const zeroX = scaleX(0);
    const axisNumber = value => metric === 'share' ? number(value, Math.max(1, -Math.floor(Math.log10(step)))) : value.toLocaleString('ko-KR', {notation: 'compact', maximumFractionDigits: 1});
    const title = byId('fiscal-chart-title').textContent;
    let content = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="fiscal-svg-title fiscal-svg-description"><title id="fiscal-svg-title">${escapeHtml(title)}</title><desc id="fiscal-svg-description">${escapeHtml(byId('fiscal-chart-subtitle').textContent)}. 각 관측점은 키보드로 선택할 수 있으며 수치 표를 함께 제공합니다.</desc><rect width="${width}" height="${height}" fill="white"/>`;
    for (let tick = 0; tick <= tickCount; tick++) {
      const value = minimumTick + step * tick;
      if (state.view === 'trend') {
        const y = scaleY(value);
        content += `<line x1="${left}" x2="${width-right}" y1="${y}" y2="${y}" stroke="#d6e1dc"/><text x="${left-12}" y="${y+5}" text-anchor="end" fill="#51686b" font-size="14">${axisNumber(value)}</text>`;
      } else {
        const x = scaleX(value);
        content += `<line x1="${x}" x2="${x}" y1="${top}" y2="${height-bottom}" stroke="#d6e1dc"/><text x="${x}" y="${height-bottom+25}" text-anchor="middle" fill="#51686b" font-size="14">${axisNumber(value)}</text>`;
      }
    }
    if (state.view === 'trend') {
      const years = rows.map(row => row.year);
      const first = Math.min(...years);
      const last = Math.max(...years);
      const xFor = year => left + plotWidth * (year-first) / Math.max(1, last-first);
      const yFor = scaleY;
      let path = '';
      let previous;
      rows.forEach(row => {
        const value = row.source && row.source[metric];
        if (value == null) { previous = undefined; return; }
        const move = !previous || row.year !== previous.year + 1 || (row.source.status === 'B' || row.source.total_status === 'B');
        path += `${move ? 'M' : 'L'}${xFor(row.year)},${yFor(value)} `;
        previous = row;
      });
      content += `<path d="${path}" fill="none" stroke="#176b64" stroke-width="3"/>`;
      rows.forEach((row, index) => {
        if (row.source && row.source[metric] != null) {
          const flag = isFlagged(row.source);
          const description = `${row.label}년 ${number(row.source[metric])}${metric === 'share' ? '%' : ` 백만 ${row.source.currency}`}${flag ? ', 원자료 상태 확인 필요' : ''}`;
          content += `<circle class="chart-mark" data-row="${index}" tabindex="0" role="img" aria-label="${escapeHtml(description)}" cx="${xFor(row.year)}" cy="${yFor(row.source[metric])}" r="6" fill="${flag ? 'white' : '#176b64'}" stroke="${flag ? '#9c652d' : '#176b64'}" stroke-width="2"/>`;
        }
        if (row.year === first || row.year === last || (row.year-first) % 4 === 0) content += `<text x="${xFor(row.year)}" y="${height-bottom+28}" text-anchor="middle" fill="#51686b" font-size="14">${row.year}</text>`;
      });
      const lastRow = [...rows].reverse().find(row => row.source && row.source[metric] != null);
      content += `<text x="${width-right+12}" y="${yFor(lastRow.source[metric])+5}" fill="#173136" font-size="14">${number(lastRow.source[metric], metric === 'share' ? 2 : 0)}${metric === 'share' ? '%' : ''}</text>`;
    } else {
      const spacing = plotHeight / rows.length;
      rows.forEach((row, index) => {
        const y = top + spacing * index + spacing / 2;
        const value = row.source && row.source[metric];
        const flag = isFlagged(row.source);
        content += `<text x="${left-12}" y="${y+5}" text-anchor="end" fill="#173136" font-size="14">${escapeHtml(row.label)}</text>`;
        if (value == null) {
          content += `<text x="${left+12}" y="${y+5}" fill="#51686b" font-size="14">결측</text>`;
        } else {
          const barWidth = Math.abs(scaleX(value)-zeroX);
          const barLeft = Math.min(zeroX, scaleX(value));
          const label = `${number(value, metric === 'share' ? 2 : 0)}${metric === 'share' ? '%' : ''}${flag ? ' *' : ''}`;
          content += `<rect class="chart-mark" data-row="${index}" tabindex="0" role="img" aria-label="${escapeHtml(row.label+' '+label)}" x="${barLeft}" y="${y-9}" width="${barWidth}" height="18" fill="${flag ? '#edf3ee' : '#176b64'}" stroke="${flag ? '#9c652d' : '#176b64'}" stroke-width="1.5"/><text x="${Math.max(zeroX,scaleX(value))+9}" y="${y+5}" fill="#173136" font-size="14">${label}</text>`;
        }
      });
    }
    content += `<line x1="${state.view === 'trend' ? left : zeroX}" x2="${state.view === 'trend' ? left : zeroX}" y1="${top}" y2="${height-bottom}" stroke="#51686b"/><line x1="${left}" x2="${width-right}" y1="${height-bottom}" y2="${height-bottom}" stroke="#51686b"/></svg>`;
    return content;
  }

  function render() {
    const metric = state.view === 'countries' ? 'share' : state.metric;
    const country = countryMap.get(state.country);
    const functionInfo = functionMap.get(state.function);
    displayedRows = rowsForView();
    const available = displayedRows.filter(row => row.source && row.source[metric] != null);
    const unit = metric === 'share' ? '전체 일반정부 지출 대비 비중 (%)' : `명목 지출액 · 백만 ${country.currency}`;
    const titles = {
      trend: `${country.name} · ${functionInfo.name} · 연도별 재정지출`,
      countries: `${state.year}년 · ${functionInfo.name} · 국가별 재정 비중`,
      functions: `${country.name} · ${state.year}년 · 기능별 재정지출`
    };
    byId('fiscal-chart-title').textContent = titles[state.view];
    byId('fiscal-chart-subtitle').textContent = `${unit} · 일반정부 전체 · OECD 조회 2026-11-07`;
    byId('fiscal-chart').innerHTML = chart(displayedRows, metric);
    byId('fiscal-table-body').innerHTML = displayedRows.map(row => `<tr><td>${escapeHtml(row.label)}</td><td>${row.source ? number(row.source.share) : '결측'}</td><td>${row.source ? number(row.source.amount) : '결측'}</td><td>${row.source ? row.source.currency : '관측값 없음'}</td><td>${escapeHtml(statusText(row.source))}</td></tr>`).join('');
    const excluded = data.countries.filter(item => !lookup(item.code, state.year, state.function));
    byId('fiscal-coverage').textContent = state.view === 'countries'
      ? `${available.length}개국 관측값 표시. ${excluded.length ? `선택 연도·기능의 관측값이 없는 국가 ${excluded.length}개는 제외: ${excluded.map(item => item.name).join(', ')}.` : '수록 37개국 모두 관측됨.'} 국가 간 비교는 통화가 다른 금액 대신 비중으로 표시한다.`
      : state.view === 'trend'
        ? `${country.years[0]}~${country.years[country.years.length-1]}년 중 ${available.length}개 연도 관측. 결측 연도와 시계열 단절에서는 선을 잇지 않는다.`
        : `10개 기능 중 ${available.length}개 관측. 합계는 반올림·분류 범위에 따라 100%와 다를 수 있다.`;
    const flagged = available.filter(row => isFlagged(row.source));
    byId('fiscal-flags').textContent = `${flagged.length}개 관측에 원자료 또는 총지출 분모의 상태 표시가 있다. 빈 점·옅은 막대·별표(*)는 정상값 외 상태를 뜻한다. P 잠정값 · E 추정값 · B 시계열 단절. 수치 표와 관측점에서 양쪽 상태를 확인할 수 있다.`;
    if (available.some(row => row.source.amount < 0)) byId('fiscal-coverage').textContent += ' 원자료에 음수가 포함돼 있으며 그대로 표시했다. 해당 항목의 회계·분류 주석 확인이 필요하다.';
    bindMarks();
  }

  async function initialise() {
    byId('fiscal-loader').textContent = 'OECD 재정 데이터를 불러오는 중…';
    const response = await fetch('data/fiscal/cofog_expenditure_20261107.json');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    data = await response.json();
    countryMap = new Map(data.countries.map(item => [item.code, item]));
    functionMap = new Map(data.functions.map(item => [item.code, item]));
    rowMap = new Map(data.rows.map(row => [`${row.country}|${row.year}|${row.function}`, row]));
    fillOptions(byId('fiscal-country'), data.countries.map(country => ({value:country.code, label:`${country.name} (${country.english})`})), state.country);
    fillOptions(byId('fiscal-function'), data.functions.map(item => ({value:item.code, label:`${item.code.slice(2)} ${item.name}`})), state.function);
    byId('fiscal-country').addEventListener('change', event => {state.country = event.target.value; refreshYears(); render();});
    byId('fiscal-year').addEventListener('change', event => {state.year = Number(event.target.value); render();});
    byId('fiscal-function').addEventListener('change', event => {state.function = event.target.value; render();});
    byId('fiscal-metric').addEventListener('change', event => {state.metric = event.target.value; render();});
    document.querySelectorAll('[data-fiscal-view]').forEach(button => button.addEventListener('click', () => selectView(button.dataset.fiscalView)));
    byId('fiscal-loader').hidden = true;
    byId('fiscal-controls').hidden = false;
    selectView('trend');
  }

  panel.addEventListener('toggle', () => {
    if (!panel.open) { byId('fiscal-tooltip').hidden = true; return; }
    if (!loading) loading = initialise().catch(error => {
      byId('fiscal-loader').textContent = `데이터를 불러오지 못했습니다. 항목을 닫았다가 다시 열어주세요. (${error.message})`;
      byId('fiscal-loader').hidden = false;
      loading = undefined;
    });
  });
  document.addEventListener('keydown', event => {if (event.key === 'Escape') byId('fiscal-tooltip').hidden = true;});
  window.addEventListener('scroll', () => {byId('fiscal-tooltip').hidden = true;}, {passive:true});
})();
