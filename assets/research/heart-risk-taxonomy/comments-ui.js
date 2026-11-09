import { COMMENT_LIMIT, PAGE_SIZE } from './comments-api.js';

function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text) node.textContent = text;
  if (className) node.className = className;
  return node;
}

export function mountComments(api, root = document) {
  const sections = [];
  root.querySelectorAll('.risk-card,.category-heading').forEach(host => {
    const riskId = host.closest('[id]').id;
    const section = element('section', '', 'risk-comments');
    section.setAttribute('aria-label', `${riskId} 익명 댓글`);
    const toggle = element('button', '익명 댓글', 'comments-toggle');
    toggle.type = 'button';
    toggle.setAttribute('aria-expanded', 'false');
    const panel = element('div', '', 'comments-panel');
    panel.id = `comments-${riskId}`;
    panel.hidden = true;
    toggle.setAttribute('aria-controls', panel.id);
    section.append(toggle, panel);
    host.append(section);
    let initialized = false;
    let stopWatching;
    let reload;
    let editing = null;
    let busy = false;
    let rows = [];
    let offset = 0;
    let mine = null;
    let loadVersion = 0;

    async function initialize() {
      const help = element('p', '익명으로 공개됩니다. 이 브라우저에서 작성한 댓글을 수정할 수 있습니다.', 'comments-help');
      const status = element('p', '', 'comments-status');
      status.setAttribute('role', 'status');
      const list = element('div', '', 'comments-list');
      const more = element('button', '댓글 더 보기');
      more.type = 'button';
      more.hidden = true;
      const refresh = element('button', '새로고침');
      refresh.type = 'button';
      const form = element('form', '', 'comment-form');
      const label = element('label', '댓글 작성');
      const input = element('textarea');
      input.id = `comment-body-${riskId}`;
      input.rows = 3;
      input.required = true;
      input.maxLength = COMMENT_LIMIT;
      label.htmlFor = input.id;
      const save = element('button', '저장');
      save.type = 'submit';
      const cancel = element('button', '수정 취소');
      cancel.type = 'button';
      cancel.hidden = true;
      const actions = element('div', '', 'comment-actions');
      actions.append(save, cancel, refresh);
      form.append(label, input, actions);
      panel.append(help, status, list, more, form);

      function render() {
        list.replaceChildren();
        if (!rows.length) list.append(element('p', '첫 댓글을 남겨 주세요.', 'comments-empty'));
        for (const row of rows) {
          const article = element('article', '', 'comment-item');
          const meta = element('p', '', 'comment-meta');
          const own = row.author_id === mine;
          const edited = row.updated_at !== row.created_at;
          const date = new Intl.DateTimeFormat('ko-KR', { dateStyle: 'short', timeStyle: 'short' })
            .format(new Date(row.updated_at));
          meta.textContent = `${own ? '익명 · 내 댓글' : '익명'} · ${date}${edited ? ' · 수정됨' : ''}`;
          article.append(meta, element('p', row.body, 'comment-body'));
          if (own) {
            const edit = element('button', '수정');
            edit.type = 'button';
            edit.disabled = busy;
            edit.addEventListener('click', () => {
              if (busy) return;
              editing = row.id;
              input.value = row.body;
              label.textContent = '댓글 수정';
              save.textContent = '수정 후 저장';
              cancel.hidden = false;
              input.focus();
            });
            article.append(edit);
          }
          list.append(article);
        }
      }
      function resetEditor() {
        editing = null;
        input.value = '';
        label.textContent = '댓글 작성';
        save.textContent = '저장';
        cancel.hidden = true;
      }
      reload = async (append = false) => {
        const version = ++loadVersion;
        status.textContent = '댓글을 불러오는 중입니다.';
        refresh.disabled = more.disabled = true;
        try {
          mine = await api.authorId();
          const page = await api.list(riskId, append ? offset : 0);
          if (version !== loadVersion || busy) return;
          rows = append ? [...rows, ...page] : page;
          offset = rows.length;
          more.hidden = page.length < PAGE_SIZE;
          render();
          status.textContent = '';
        } catch {
          status.textContent = '댓글을 불러오지 못했습니다. 새로고침해 주세요.';
        } finally {
          if (version === loadVersion && !busy) refresh.disabled = more.disabled = false;
        }
      };
      refresh.addEventListener('click', () => reload());
      more.addEventListener('click', () => reload(true));
      cancel.addEventListener('click', resetEditor);
      form.addEventListener('submit', async event => {
        event.preventDefault();
        if (busy) return;
        busy = true;
        loadVersion++;
        save.disabled = cancel.disabled = input.disabled = true;
        refresh.disabled = more.disabled = true;
        render();
        status.textContent = '저장 중입니다.';
        try {
          const saved = await api.save(riskId, input.value, editing);
          mine = await api.authorId();
          // Show only the row actually returned by the shared server.
          rows = [saved, ...rows.filter(row => row.id !== saved.id)];
          offset = rows.length;
          resetEditor();
          status.textContent = '저장되었습니다.';
        } catch (error) {
          status.textContent = /댓글 내용을|자 이내|브라우저|본인이/.test(error.message)
            ? error.message : '저장하지 못했습니다. 작성한 내용은 남아 있습니다. 다시 시도해 주세요.';
        } finally {
          busy = false;
          save.disabled = cancel.disabled = input.disabled = false;
          refresh.disabled = more.disabled = false;
          render();
        }
      });
      await reload();
    }
    toggle.addEventListener('click', async () => {
      panel.hidden = !panel.hidden;
      toggle.setAttribute('aria-expanded', String(!panel.hidden));
      if (panel.hidden) { stopWatching?.(); stopWatching = null; return; }
      if (!initialized) {
        initialized = true;
        await initialize();
      } else if (!busy && !editing) await reload();
      if (!panel.hidden && !stopWatching) {
        stopWatching = api.watch(riskId, () => {
          const rect = section.getBoundingClientRect();
          if (!busy && !editing && rect.bottom > 0 && rect.top < innerHeight) reload();
        });
      }
    });
    sections.push(section);
  });
  return sections;
}
