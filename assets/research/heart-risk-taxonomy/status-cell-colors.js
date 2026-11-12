(() => {
  'use strict';
  const selector = '.myai-type-table';
  const root = document.querySelector('main');
  if (!root) return;

  function paint(table) {
    const headers = Array.from(table.tHead?.rows[0]?.cells || [], cell => cell.textContent.trim());
    const rows = [...Array.from(table.tBodies).flatMap(body => Array.from(body.rows)), ...Array.from(table.tFoot?.rows || [])];
    for (const row of rows) {
      Array.from(row.cells).forEach((cell, index) => {
        const header = headers[index] || '';
        const value = Number(cell.textContent.replaceAll(',', '').trim());
        const positive = Number.isFinite(value) && value > 0;
        cell.classList.toggle('review-count', positive && header.includes('휴먼 검토'));
        cell.classList.toggle('unmapped-count', positive && header.includes('미매핑'));
      });
    }
  }

  const pending = new Set();
  let frame = 0;
  function enqueue(table) {
    if (!table) return;
    pending.add(table);
    if (frame) return;
    frame = requestAnimationFrame(() => {
      frame = 0;
      for (const item of pending) if (item.isConnected) paint(item);
      pending.clear();
    });
  }

  root.querySelectorAll(selector).forEach(paint);
  new MutationObserver(records => {
    for (const record of records) {
      const element = record.target.nodeType === Node.ELEMENT_NODE ? record.target : record.target.parentElement;
      enqueue(element?.closest(selector));
      for (const node of record.addedNodes) {
        if (node.nodeType !== Node.ELEMENT_NODE) continue;
        if (node.matches(selector)) enqueue(node);
        node.querySelectorAll(selector).forEach(enqueue);
      }
    }
  }).observe(root, { childList: true, characterData: true, subtree: true });
})();
