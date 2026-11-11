const form = document.querySelector('.controls');
const search = document.querySelector('#search');
const domain = document.querySelector('#domain');
const domains = [...document.querySelectorAll('.domain')];
function filter() {
  const q = search.value.trim().toLocaleLowerCase();
  let count = 0;
  let categories = 0;
  domains.forEach(section => {
    const domainMatch = domain.value === 'all' || section.dataset.domain === domain.value;
    let visible = 0;
    section.querySelectorAll('.category').forEach(category => {
      let found = 0;
      category.querySelectorAll('.risk-card').forEach(card => {
        const show = domainMatch && (!q || card.dataset.search.includes(q));
        card.hidden = !show;
        if (show) found++;
      });
      category.hidden = !found;
      category.querySelector('.category-count').textContent = found;
      category.querySelector('details').open = Boolean(q && found);
      if (found) { categories++; visible += found; }
    });
    section.hidden = !visible;
    section.open = Boolean(visible && (q || domain.value !== 'all'));
    count += visible;
  });
  document.querySelector('#result').textContent = `${categories}개 범주 · ${count}개 리스크 카드`;
  document.querySelector('#empty').hidden = count !== 0;
}
form.addEventListener('submit', event => event.preventDefault());
form.addEventListener('input', filter);
form.addEventListener('change', filter);
form.addEventListener('reset', () => requestAnimationFrame(filter));
document.querySelectorAll('.risk-card code,.category-heading code').forEach(code => {
  const id = code.closest('[id]').id;
  const link = document.createElement('a');
  link.href = '#' + id;
  link.textContent = code.textContent;
  code.replaceChildren(link);
});
function revealHash() {
  const requested = decodeURIComponent(location.hash.slice(1));
  const aliases = {"G_INT_COPY_008": "G_INT_COPY_003", "A_INT_CASCADE_003": "A_INT_CASCADE_001", "A_INT_CASCADE_004": "A_INT_CASCADE_001", "A_INT_CASCADE_009": "A_INT_CASCADE_001", "G_INT_COPY_011": "G_INT_COPY_003", "G_SYS_EVAL_076": "G_SYS_EVAL_001", "G_INT_SEX_011": "G_INT_SEX_004", "A_SYS_AUTH_021": "A_SYS_AUTH_012", "A_SYS_GOAL_010": "A_SYS_GOAL_005", "G_SYS_EVAL_075": "G_SYS_EVAL_070"};
  const canonical = aliases[requested] || requested;
  const target = document.getElementById(canonical);
  if (requested !== canonical) history.replaceState(null, '', '#' + canonical);
  if (!target || !target.matches('.risk-card,.category,.domain')) return;
  if (target.matches('details')) target.open = true;
  let parent = target.parentElement;
  while (parent) {
    if (parent.matches('details')) parent.open = true;
    parent = parent.parentElement;
  }
  target.scrollIntoView();
}
window.addEventListener('hashchange', revealHash);
revealHash();

// HEART source-taxonomy crosswalk candidates and conservative selection rules.
{const script=document.createElement("script");script.src="mapping-tags.js?v=20261111-rules1";document.head.append(script);}
