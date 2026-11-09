// The generated deployment includes HEART_COMMENT_RISK_IDS from risk-ids.json.
function heartCommentResponse(data, status, origin, env) {
  return new Response(status === 204 ? null : JSON.stringify(data), { status, headers: {
    'content-type': 'application/json; charset=utf-8',
    'access-control-allow-origin': origin === env.ALLOWED_ORIGIN ? origin : env.ALLOWED_ORIGIN,
    'access-control-allow-methods': 'GET, POST, OPTIONS',
    'access-control-allow-headers': 'content-type',
    'cache-control': 'no-store', vary: 'Origin',
  } });
}

async function heartCommentHash(secret) {
  const bytes = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(secret));
  return Array.from(new Uint8Array(bytes), value => value.toString(16).padStart(2, '0')).join('');
}

function heartPublicComment(row) {
  return { id: row.id, risk_id: row.risk_id, body: row.body, created_at: row.created_at, updated_at: row.updated_at };
}

function heartCommentHeaders(env) {
  return { authorization: `Bearer ${env.GH_TOKEN}`, accept: 'application/vnd.github+json',
    'content-type': 'application/json', 'user-agent': 'heart-anonymous-comments',
    'x-github-api-version': '2022-11-28' };
}

async function heartCommentDocument(riskId, env) {
  const path = `heart-comments/risks/${riskId}.json`;
  const endpoint = `https://api.github.com/repos/${env.GH_OWNER}/${env.GH_REPO}/contents/${path}`;
  const result = await fetch(endpoint, { headers: heartCommentHeaders(env), cache: 'no-store' });
  if (result.status === 404) return { endpoint, sha: null, comments: [] };
  if (!result.ok) throw new Error(`Comment store read ${result.status}`);
  const file = await result.json();
  const bytes = Uint8Array.from(atob(file.content.replace(/\s/g, '')), char => char.charCodeAt(0));
  const document = JSON.parse(new TextDecoder().decode(bytes));
  if (document.risk_id !== riskId || !Array.isArray(document.comments)) throw new Error('Invalid stored thread');
  return { endpoint, sha: file.sha, comments: document.comments };
}

async function heartCommentsFetch(request, env) {
  const origin = request.headers.get('origin') || '';
  const respond = (data, status = 200) => heartCommentResponse(data, status, origin, env);
  const url = new URL(request.url);
  if (request.method === 'OPTIONS') return respond(null, 204);
  const riskId = url.pathname.slice('/comments/'.length);
  if (!Object.hasOwn(HEART_COMMENT_RISK_IDS, riskId)) return respond({ error: 'Unknown risk ID' }, 404);
  if (!['GET', 'POST'].includes(request.method)) return respond({ error: 'Method not allowed' }, 405);
  if (request.method === 'POST' && origin !== env.ALLOWED_ORIGIN) return respond({ error: 'Origin not allowed' }, 403);
  try {
    if (request.method === 'GET') {
      const document = await heartCommentDocument(riskId, env);
      const offset = Math.max(0, Math.min(100000, Number.parseInt(url.searchParams.get('offset') || '0', 10) || 0));
      const rows = [...document.comments].sort((a, b) => b.created_at.localeCompare(a.created_at) || b.id.localeCompare(a.id));
      return respond({ comments: rows.slice(offset, offset + 30).map(heartPublicComment) });
    }
    if (!request.headers.get('content-type')?.startsWith('application/json')) return respond({ error: 'JSON required' }, 400);
    if (Number(request.headers.get('content-length')) > 16000) return respond({ error: 'Request too large' }, 413);
    const text = await request.text();
    if (new TextEncoder().encode(text).length > 16000) return respond({ error: 'Request too large' }, 413);
    let input;
    try { input = JSON.parse(text); } catch { return respond({ error: 'Invalid JSON' }, 400); }
    if (!/^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/i.test(input.id || '')
        || !/^[a-f0-9]{64}$/.test(input.edit_key || '') || typeof input.body !== 'string') {
      return respond({ error: 'Invalid comment' }, 400);
    }
    const body = input.body.trim();
    if (!body || Array.from(body).length > 2000) return respond({ error: 'Comment must contain 1 to 2000 characters' }, 400);
    const hash = await heartCommentHash(input.edit_key);
    for (let attempt = 0; attempt < 6; attempt++) {
      const document = await heartCommentDocument(riskId, env);
      const index = document.comments.findIndex(row => row.id === input.id);
      if (index >= 0 && document.comments[index].edit_hash !== hash) return respond({ error: 'Not the author' }, 403);
      if (index >= 0 && document.comments[index].body === body) return respond({ comment: heartPublicComment(document.comments[index]) });
      const now = new Date().toISOString();
      const row = { id: input.id, risk_id: riskId, body, edit_hash: hash,
        created_at: index >= 0 ? document.comments[index].created_at : now, updated_at: now };
      const comments = [...document.comments];
      if (index >= 0) comments[index] = row; else comments.push(row);
      const content = JSON.stringify({ schema_version: 1, risk_id: riskId, comments }, null, 2) + '\n';
      if (new TextEncoder().encode(content).length > 900000) return respond({ error: 'Thread capacity reached' }, 409);
      const result = await fetch(document.endpoint, { method: 'PUT', headers: heartCommentHeaders(env), body: JSON.stringify({
        message: `${index >= 0 ? 'Update' : 'Add'} anonymous HEART comment ${riskId}`,
        content: btoa(unescape(encodeURIComponent(content))), ...(document.sha ? { sha: document.sha } : {}),
      }) });
      if (result.ok) return respond({ comment: heartPublicComment(row) }, index >= 0 ? 200 : 201);
      if (![409, 422].includes(result.status)) throw new Error(`Comment store write ${result.status}`);
      await new Promise(resolve => setTimeout(resolve, 75 * (attempt + 1) + Math.random() * 100));
    }
    return respond({ error: 'Concurrent save, please retry' }, 409);
  } catch {
    return respond({ error: 'Comment store unavailable' }, 503);
  }
}
