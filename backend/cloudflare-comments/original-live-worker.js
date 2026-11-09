var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// src/index.js
var JSON_HEADERS = { "content-type": "application/json; charset=utf-8" };
function cors(origin, allowedOrigin) {
  const accepted = origin === allowedOrigin || origin === "http://127.0.0.1:8765";
  return {
    "access-control-allow-origin": accepted ? origin : allowedOrigin,
    "access-control-allow-methods": "POST, OPTIONS",
    "access-control-allow-headers": "content-type",
    "access-control-max-age": "86400",
    vary: "Origin"
  };
}
__name(cors, "cors");
function response(body, status, origin, env) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...JSON_HEADERS, ...cors(origin, env.ALLOWED_ORIGIN) }
  });
}
__name(response, "response");
function validPayload(payload) {
  return payload && /^R-[a-f0-9]{12}$/.test(payload.respondent_id || "") && /^A(?:0[1-9]|1[0-9])$/.test(payload.assignment_block || "") && /^[a-f0-9-]{36}$/.test(payload.submission_id || "") && typeof payload.markdown === "string" && payload.markdown.length >= 500 && payload.markdown.length <= 2e5 && typeof payload.json === "string" && payload.json.length >= 500 && payload.json.length <= 3e5 && typeof payload.csv === "string" && payload.csv.length >= 500 && payload.csv.length <= 3e5;
}
__name(validPayload, "validPayload");
function partition(dateValue) {
  const date = new Date(dateValue || Date.now());
  if (Number.isNaN(date.getTime())) throw new Error("Invalid timestamp");
  return {
    year: String(date.getUTCFullYear()),
    month: String(date.getUTCMonth() + 1).padStart(2, "0")
  };
}
__name(partition, "partition");
async function putGitHubFile(repo, path, content, message, env) {
  const endpoint = `https://api.github.com/repos/${env.GH_OWNER}/${repo}/contents/${path}`;
  const githubResponse = await fetch(endpoint, {
    method: "PUT",
    headers: {
      authorization: `Bearer ${env.GH_TOKEN}`,
      accept: "application/vnd.github+json",
      "content-type": "application/json",
      "user-agent": "pai-risk-survey-worker",
      "x-github-api-version": "2022-11-28"
    },
    body: JSON.stringify({
      message,
      content: btoa(unescape(encodeURIComponent(content)))
    })
  });
  if (githubResponse.status === 422) return { duplicate: true };
  if (!githubResponse.ok) {
    const detail = await githubResponse.text();
    throw new Error(`GitHub ${githubResponse.status}: ${detail.slice(0, 300)}`);
  }
  return { duplicate: false, result: await githubResponse.json() };
}
__name(putGitHubFile, "putGitHubFile");
function yamlValue(value) {
  return JSON.stringify(value ?? null);
}
__name(yamlValue, "yamlValue");
function buildTelemetry(payload, request, receivedAt) {
  const cf = request.cf || {};
  const startedAt = new Date(payload.started_at || receivedAt);
  const completedAt = new Date(payload.submitted_at || receivedAt);
  const durationSeconds = Number.isFinite(payload.duration_seconds) ? Math.max(0, Math.round(payload.duration_seconds)) : Math.max(0, Math.round((completedAt - startedAt) / 1e3));
  const telemetry = {
    respondent_id: payload.respondent_id,
    submission_id: payload.submission_id,
    assignment_block: payload.assignment_block,
    started_at_client: payload.started_at || null,
    completed_at_client: payload.submitted_at || null,
    duration_seconds: durationSeconds,
    country: cf.country || null
  };
  const lines = ["---"];
  for (const [key, value] of Object.entries(telemetry)) {
    lines.push(`${key}: ${yamlValue(value)}`);
  }
  lines.push("---", "", "# Private Survey Administration Record", "");
  lines.push("This file contains access-restricted timing and country-level information separated from the public survey response.", "");
  return lines.join("\n");
}
__name(buildTelemetry, "buildTelemetry");
async function saveTelemetry(payload, request, receivedAt, env) {
  const { year, month } = partition(receivedAt);
  const filename = `${payload.respondent_id}_${payload.submission_id}.md`;
  const path = `telemetry/${year}/${month}/${filename}`;
  const content = buildTelemetry(payload, request, receivedAt);
  const stored = await putGitHubFile(
    env.GH_TELEMETRY_REPO,
    path,
    content,
    `Add private survey telemetry ${payload.respondent_id}`,
    env
  );
  return { path, duplicate: stored.duplicate };
}
__name(saveTelemetry, "saveTelemetry");
async function savePublicResponse(payload, env) {
  const { year, month } = partition(payload.submitted_at);
  const stem = `${payload.respondent_id}_${payload.submission_id}`;
  const path = `responses/${year}/${month}/${stem}.md`;
  const jsonPath = `responses/${year}/${month}/${stem}.json`;
  const csvPath = `responses/${year}/${month}/${stem}.csv`;
  const markdown = await putGitHubFile(
    env.GH_REPO,
    path,
    payload.markdown,
    `Add anonymous survey response ${payload.respondent_id}`,
    env
  );
  const json = await putGitHubFile(
    env.GH_REPO,
    jsonPath,
    payload.json,
    `Add anonymous survey JSON ${payload.respondent_id}`,
    env
  );
  const csv = await putGitHubFile(
    env.GH_REPO,
    csvPath,
    payload.csv,
    `Add anonymous survey CSV ${payload.respondent_id}`,
    env
  );
  return {
    path,
    json_path: jsonPath,
    csv_path: csvPath,
    url: `https://github.com/${env.GH_OWNER}/${env.GH_REPO}/blob/main/${path}`,
    json_url: `https://github.com/${env.GH_OWNER}/${env.GH_REPO}/blob/main/${jsonPath}`,
    csv_url: `https://github.com/${env.GH_OWNER}/${env.GH_REPO}/blob/main/${csvPath}`,
    duplicate: markdown.duplicate && json.duplicate && csv.duplicate
  };
}
__name(savePublicResponse, "savePublicResponse");
var index_default = {
  async fetch(request, env) {
    const origin = request.headers.get("origin") || "";
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors(origin, env.ALLOWED_ORIGIN) });
    }
    const url = new URL(request.url);
    if (request.method === "GET" && url.pathname === "/health") {
      return response({
        status: "ok",
        public_repository: `${env.GH_OWNER}/${env.GH_REPO}`,
        private_telemetry_repository: `${env.GH_OWNER}/${env.GH_TELEMETRY_REPO}`
      }, 200, origin, env);
    }
    if (request.method !== "POST" || url.pathname !== "/submit") {
      return response({ error: "Not found" }, 404, origin, env);
    }
    if (origin !== env.ALLOWED_ORIGIN && origin !== "http://127.0.0.1:8765") {
      return response({ error: "Origin not allowed" }, 403, origin, env);
    }
    let payload;
    try {
      payload = await request.json();
    } catch {
      return response({ error: "Invalid JSON" }, 400, origin, env);
    }
    if (!validPayload(payload)) return response({ error: "Invalid submission" }, 400, origin, env);
    try {
      const receivedAt = (/* @__PURE__ */ new Date()).toISOString();
      const telemetry = await saveTelemetry(payload, request, receivedAt, env);
      const publicResponse = await savePublicResponse(payload, env);
      return response({
        stored: true,
        ...publicResponse,
        telemetry_stored: true,
        telemetry_duplicate: telemetry.duplicate
      }, 201, origin, env);
    } catch (error) {
      console.error(error);
      return response({ error: "Storage failed" }, 502, origin, env);
    }
  }
};
export {
  index_default as default
};
//# sourceMappingURL=index.js.map
