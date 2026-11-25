/* Present age filters as one-click buttons; retain native values and change handlers. */
(() => {
  'use strict';
  const fields = new WeakMap();
  const ageLabel = /\bages?\b|연령/i;
  function labelFor(select) {
    const wrapped = select.closest('label');
    if (wrapped) return Array.from(wrapped.childNodes).filter(n => n !== select && n.nodeType === Node.TEXT_NODE).map(n => n.textContent).join(' ').trim();
    if (select.getAttribute('aria-label')) return select.getAttribute('aria-label');
    const label = select.id && document.querySelector('label[for="' + CSS.escape(select.id) + '"]');
    return label ? label.textContent.trim() : '';
  }
  function update(select) {
    const label = labelFor(select);
    if (!fields.has(select) && !ageLabel.test(label)) return;
    const options = Array.from(select.options);
    if (!options.length) return;
    let field = fields.get(select);
    if (!field) {
      const group = document.createElement('div');
      group.className = 'age-filter-buttons';
      group.setAttribute('role', 'group');
      group.setAttribute('aria-label', label || 'Age group');
      let box = select.parentElement;
      if (box.tagName === 'LABEL') {
        const replacement = document.createElement('div');
        const heading = document.createElement('span');
        heading.className = 'age-filter-heading'; heading.textContent = label;
        box.replaceWith(replacement); replacement.append(heading, select); box = replacement;
      }
      box.classList.add('age-button-field');
      select.classList.add('age-select-source');
      select.hidden = true;
      select.after(group);
      field = { group, signature: '' }; fields.set(select, field);
      select.addEventListener('change', () => sync(select, field));
    }
    const signature = JSON.stringify(options.map(o => [o.value, o.textContent, o.disabled]));
    if (field.signature !== signature) {
      field.signature = signature; field.group.replaceChildren();
      for (const option of options) {
        const button = document.createElement('button');
        button.type = 'button'; button.textContent = option.textContent;
        button.dataset.ageValue = option.value;
        button.addEventListener('click', () => {
          if (select.value === option.value) return;
          select.value = option.value;
          select.dispatchEvent(new Event('change', { bubbles: true }));
          sync(select, field);
        });
        field.group.append(button);
      }
    }
    sync(select, field);
  }
  function sync(select, field) {
    Array.from(field.group.children).forEach((button, i) => {
      const selected = button.dataset.ageValue === select.value;
      button.setAttribute('aria-pressed', String(selected));
      button.disabled = select.disabled || !!select.options[i]?.disabled;
    });
  }
  let pending = false;
  function schedule() {
    if (pending) return; pending = true;
    queueMicrotask(() => { pending = false; document.querySelectorAll('select').forEach(update); });
  }
  const observer = new MutationObserver(schedule);
  observer.observe(document.body, { childList: true, subtree: true });
  schedule();
})();
