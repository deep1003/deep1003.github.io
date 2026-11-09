import { buildResultsCsv } from "./results-csv.js";
import {
  createRiskIndex,
  searchRisks,
} from "./risk-search-engine.js?v=20261110-row-v3";
import {
  extractFileText,
  MAX_TEXT_LENGTH,
} from "./file-text.js?v=20261110-row-v3";
import { parseScenarios } from "./scenario-input.js";
const form = document.querySelector("#document-search-form"),
  input = document.querySelector("#document-text");
const upload = document.querySelector("#document-file"),
  status = document.querySelector("#document-status");
const output = document.querySelector("#document-results"),
  submit = document.querySelector("#document-submit");
const preview = document.createElement("details");
preview.id = "scenario-preview";
preview.hidden = false;
form.after(preview);
let indexPromise,
  reading = false,
  uploadVersion = 0,
  searchVersion = 0,
  savedGroups = null;
const node = (tag, text, cls) => {
  const el = document.createElement(tag);
  if (text) el.textContent = text;
  if (cls) el.className = cls;
  return el;
};
const saveButton = document.querySelector("#save-results-csv");
const saveStatus = document.querySelector("#save-status");
const resultHint = document.querySelector("#document-result-hint");
function resetPreview() {
  preview.replaceChildren(
    node("summary", "2. 자동 추출한 시나리오 확인"),
    node(
      "p",
      "1단계에서 파일을 불러오거나 텍스트를 입력하고 시나리오를 추출해 주세요.",
      "document-note",
    ),
  );
  preview.hidden = false;
  preview.open = false;
}
resetPreview();
function index() {
  return (indexPromise ??= (async () => {
    const r = await fetch("taxonomy.json?v=20261109-v10");
    if (!r.ok)
      throw Error("분류체계를 불러오지 못했습니다. 다시 시도해 주세요.");
    return createRiskIndex(await r.json());
  })().catch((e) => {
    indexPromise = null;
    throw e;
  }));
}
function link(id, text) {
  const a = node("a", text);
  a.href = "#" + id;
  return a;
}
function clearResults() {
  searchVersion++;
  output.replaceChildren();
  savedGroups = null;
  saveButton.disabled = true;
  saveStatus.textContent = "검색 결과를 출력하면 CSV로 저장할 수 있습니다.";
  resultHint.hidden = false;
}
function makePreviewRow(row = { number: "", title: "", scenario: "" }) {
  const el = node("article", "", "scenario-edit");
  const label = node("label", "원본 번호");
  const number = node("input");
  number.value = row.number;
  number.className = "scenario-number";
  number.setAttribute("aria-label", "원본 번호");
  label.append(number);
  const titleLabel = node("label", "구분");
  const title = node("input");
  title.value = row.title;
  title.className = "scenario-title";
  title.setAttribute("aria-label", "구분");
  titleLabel.append(title);
  const scenarioLabel = node("label", "검색할 잠재리스크 시나리오");
  const text = node("textarea");
  text.value = row.scenario;
  text.className = "scenario-value";
  text.rows = 4;
  text.maxLength = MAX_TEXT_LENGTH;
  text.setAttribute("aria-label", "검색할 잠재리스크 시나리오");
  scenarioLabel.append(text);
  const remove = node("button", "행 삭제");
  remove.type = "button";
  remove.addEventListener("click", () => {
    el.remove();
    clearResults();
  });
  el.append(label, titleLabel, scenarioLabel, remove);
  el.addEventListener("input", () => {
    clearResults();
    status.textContent = "수정한 시나리오로 다시 검색해 주세요.";
  });
  return el;
}
function prepare() {
  clearResults();
  resetPreview();
  const text = input.value.trim();
  if (!text) {
    preview.hidden = false;
    status.textContent = "파일을 불러오거나 시나리오를 붙여 넣어 주세요.";
    return;
  }
  if (text.length > MAX_TEXT_LENGTH) {
    status.textContent = "텍스트는 10만 자 이하로 나누어 입력해 주세요.";
    return;
  }
  const parsed = parseScenarios(text);
  if (parsed.rows.length > 100) {
    status.textContent = "한 번에 최대 100개 시나리오를 입력해 주세요.";
    return;
  }
  preview.replaceChildren();
  preview.hidden = false;
  preview.open = true;
  preview.append(
    node("summary", "2. 자동 추출한 시나리오 확인"),
    node("p", parsed.message, "scenario-extraction-status"),
    node(
      "p",
      "아래 시나리오 내용만 검색합니다. 번호와 구분은 행을 식별하는 데 사용합니다.",
      "document-note",
    ),
  );
  const list = node("div", "", "scenario-edit-list");
  for (const row of parsed.rows) list.append(makePreviewRow(row));
  preview.append(list);
  const add = node("button", "시나리오 추가");
  add.type = "button";
  add.addEventListener("click", () => {
    if (list.children.length >= 100) return;
    list.append(
      makePreviewRow({
        number: String(list.children.length + 1),
        title: "",
        scenario: "",
      }),
    );
    clearResults();
  });
  const search = node("button", "확인한 시나리오 검색", "document-primary");
  search.type = "button";
  search.id = "scenario-search";
  search.addEventListener("click", () => run(search));
  preview.append(add, search);
  status.textContent =
    parsed.mode === "review"
      ? "시나리오 추출 확인 필요"
      : `시나리오 ${parsed.rows.length}개 행을 확인한 뒤 검색해 주세요.`;
}
function render(groups) {
  output.replaceChildren();
  resultHint.hidden = true;
  savedGroups = groups;
  saveButton.disabled = false;
  saveStatus.textContent = "화면에 출력된 순서와 내용으로 저장합니다.";
  const summary = node("details", "", "document-summary");
  summary.open = true;
  const count = groups.reduce((n, g) => n + g.results.length, 0),
    heading = node("summary");
  heading.append(
    node("h3", `시나리오 ${groups.length}개 · L4 연관 결과 ${count}개`),
  );
  summary.append(
    heading,
    node(
      "p",
      "사전 정의된 리스크 정의와 사용자가 입력한 텍스트의 유사도에 따른 출력 결과입니다.",
      "muted",
    ),
  );
  output.append(summary);
  for (const group of groups) {
    const section = node("section", "", "scenario-result");
    section.append(
      node("h3", `${group.number}${group.title ? " · " + group.title : ""}`),
      node("blockquote", group.scenario, "scenario-source"),
    );
    if (!group.results.length) {
      section.append(
        node(
          "p",
          "충분히 연관된 후보를 찾지 못했습니다. 시나리오 내용을 구체적으로 확인해 주세요.",
        ),
      );
      summary.append(section);
      continue;
    }
    const table = node("table", "", "scenario-results-table"),
      head = node("thead"),
      tr = node("tr");
    for (const h of ["순위", "소속 L3", "연관 L4 잠재리스크", "연관 내용"])
      tr.append(node("th", h));
    head.append(tr);
    table.append(head);
    const body = node("tbody");
    group.results.forEach((candidate, i) => {
      const r = candidate.row,
        line = node("tr");
      line.dataset.riskId = r.L4_ID;
      line.dataset.score = String(candidate.score);
      const rank = node("td", String(i + 1));
      rank.dataset.label = "순위";
      const l3 = node("td");
      l3.dataset.label = "소속 L3";
      l3.append(link(r.L3_ID, r.L3_Title_ko), node("code", r.L3_ID));
      const l4 = node("td");
      l4.dataset.label = "연관 L4 잠재리스크";
      l4.append(link(r.L4_ID, r.L4_Title_ko), node("code", r.L4_ID));
      const details = node("details");
      details.append(
        node("summary", "정의 보기"),
        node("p", r.L4_Description_ko),
        node("p", r.L4_Description_en, "english"),
      );
      l4.append(details);
      const why = node("td");
      why.dataset.label = "연관 내용";
      why.append(
        node(
          "p",
          candidate.matched.length
            ? `일치 표현 · ${candidate.matched.join(" · ")}`
            : "시나리오와 리스크 정의의 관련 표현 비교",
        ),
      );
      line.append(rank, l3, l4, why);
      body.append(line);
    });
    table.append(body);
    section.append(table);
    summary.append(section);
  }
}
async function run(button) {
  if (reading) return;
  const rows = [...preview.querySelectorAll(".scenario-edit")].map((el, i) => ({
    number: el.querySelector(".scenario-number").value.trim() || String(i + 1),
    title: el.querySelector(".scenario-title").value.trim(),
    scenario: el.querySelector(".scenario-value").value.trim(),
  }));
  if (!rows.length || rows.some((r) => !r.scenario)) {
    status.textContent = "각 행에 검색할 잠재리스크 시나리오를 입력해 주세요.";
    return;
  }
  if (rows.reduce((n, r) => n + r.scenario.length, 0) > MAX_TEXT_LENGTH) {
    status.textContent = "시나리오 전체 길이는 10만 자 이하로 입력해 주세요.";
    return;
  }
  clearResults();
  const version = ++searchVersion;
  button.disabled = true;
  status.textContent = "시나리오별 연관 리스크를 비교하고 있습니다.";
  try {
    const idx = await index();
    if (version !== searchVersion) return;
    const groups = rows.map((row) => ({
      ...row,
      results: searchRisks(idx, row.scenario, {
        limit: Number(document.querySelector("#document-limit").value),
        domain: document.querySelector("#document-domain").value,
      }),
    }));
    render(groups);
    preview.open = false;
    output.scrollIntoView({ block: "start" });
    status.textContent = `검색결과 출력 · 시나리오 ${rows.length}개를 행별 관련도순 L3·L4 표로 표시했습니다.`;
  } catch (e) {
    status.textContent = e.message;
    output.replaceChildren();
  } finally {
    button.disabled = false;
  }
}
form.addEventListener("submit", (e) => {
  e.preventDefault();
  if (!reading) prepare();
});
form.addEventListener("reset", () => {
  uploadVersion++;
  reading = false;
  submit.disabled = false;
  clearResults();
  resetPreview();
  status.textContent = "";
});
input.addEventListener("input", () => {
  clearResults();
  resetPreview();
  status.textContent = "입력한 내용에서 시나리오를 다시 추출해 주세요.";
});
for (const id of ["#document-domain", "#document-limit"])
  document.querySelector(id).addEventListener("change", () => {
    clearResults();
    status.textContent = "변경한 조건으로 시나리오 검색을 눌러 주세요.";
  });
upload.addEventListener("change", async () => {
  const file = upload.files[0];
  if (!file) return;
  const version = ++uploadVersion;
  input.value = "";
  reading = true;
  submit.disabled = true;
  clearResults();
  resetPreview();
  status.textContent = `${file.name}에서 시나리오를 읽고 있습니다.`;
  try {
    const text = await extractFileText(file);
    if (version !== uploadVersion) return;
    input.value = text;
    prepare();
  } catch (e) {
    if (version === uploadVersion) {
      status.textContent = e.message;
      upload.value = "";
    }
  } finally {
    if (version === uploadVersion) {
      reading = false;
      submit.disabled = false;
    }
  }
});
document.querySelector("#document-example").addEventListener("click", () => {
  uploadVersion++;
  reading = false;
  submit.disabled = false;
  upload.value = "";
  input.value =
    "| 번호 | 구분 | 잠재리스크 시나리오 |\n| --- | --- | --- |\n| 1 | 로봇의 사람 인식 | 배달 로봇이 보행자를 인식하지 못해 충돌한다. |\n| 2 | 개인정보 동의 | 이용자의 동의 없이 개인정보를 수집하고 활용한다. |";
  prepare();
});

saveButton.addEventListener("click", () => {
  if (!savedGroups) return;
  const stamp = new Intl.DateTimeFormat("sv-SE", {
    timeZone: "Asia/Seoul",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  })
    .format(new Date())
    .replace(/[^0-9]/g, "");
  const blob = new Blob([buildResultsCsv(savedGroups)], {
    type: "text/csv;charset=utf-8",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `RAI_Risk_Explorer_results_${stamp}.csv`;
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  saveStatus.textContent = "CSV 파일 다운로드를 요청했습니다.";
});
