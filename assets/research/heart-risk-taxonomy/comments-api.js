export const COMMENT_LIMIT = 2000;
export const PAGE_SIZE = 30;
const STORAGE_KEY = 'heart-comment-edit-keys-v1';
export function validateBody(value) {
  const body = value.trim();
  if (!body) throw new Error('댓글 내용을 입력해 주세요.');
  if (Array.from(body).length > COMMENT_LIMIT) throw new Error(`댓글은 ${COMMENT_LIMIT}자 이내로 작성해 주세요.`);
  return body;
}
export function createCommentsApi(baseUrl, options = {}) {
  const storage = options.storage || localStorage;
  const fetchRequest = options.fetch || fetch;
  const random = options.crypto || crypto;
  const pending = new Map();
  const keys = () => JSON.parse(storage.getItem(STORAGE_KEY) || '{}');
  function remember(id, key) {
    try { storage.setItem(STORAGE_KEY, JSON.stringify({ ...keys(), [id]: key })); }
    catch { throw new Error('댓글 수정을 위해 이 브라우저의 저장소를 허용해 주세요.'); }
  }
  function annotate(row) { return { ...row, author_id: keys()[row.id] ? 'mine' : '' }; }
  async function request(path, init) {
    const response = await fetchRequest(baseUrl.replace(/\/$/, '') + path, { cache: 'no-store', ...init });
    const result = await response.json();
    if (!response.ok) throw new Error(response.status === 403 ? '본인이 작성한 댓글만 수정할 수 있습니다.' : '댓글 저장소에 연결하지 못했습니다.');
    return result;
  }
  return {
    async authorId() { return 'mine'; },
    async list(riskId, offset = 0) {
      const data = await request(`/comments/${encodeURIComponent(riskId)}?offset=${offset}`);
      return data.comments.map(annotate);
    },
    async save(riskId, value, id = null) {
      const body = validateBody(value);
      let edit;
      if (id) {
        const key = keys()[id];
        if (!key) throw new Error('이 브라우저에서 작성한 댓글만 수정할 수 있습니다.');
        edit = { id, key };
      } else {
        edit = pending.get(riskId);
        if (!edit) {
          const bytes = random.getRandomValues(new Uint8Array(32));
          edit = { id: random.randomUUID(), key: Array.from(bytes, x => x.toString(16).padStart(2, '0')).join('') };
          remember(edit.id, edit.key);
          pending.set(riskId, edit);
        }
      }
      const data = await request(`/comments/${encodeURIComponent(riskId)}`, {
        method: 'POST', headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ id: edit.id, edit_key: edit.key, body }),
      });
      if (!id) pending.delete(riskId);
      return annotate(data.comment);
    },
    watch(riskId, onChange) {
      const timer = setInterval(() => { if (!document.hidden) onChange(); }, 30000);
      window.addEventListener('focus', onChange);
      return () => { clearInterval(timer); window.removeEventListener('focus', onChange); };
    },
  };
}
