export function cleanCell(value) {
  return String(value ?? "")
    .replace(/<br\s*\/?\s*>/gi, "\n")
    .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1")
    .replace(/\\([|*_()[\].])/g, "$1")
    .replace(/\*\*|__/g, "")
    .replace(/&nbsp;|&#160;/g, " ")
    .replace(/&amp;/g, "&")
    .trim();
}
const key = (s) =>
  cleanCell(s)
    .normalize("NFKC")
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]/gu, "");
const isScenario = (s) =>
  [
    "잠재리스크시나리오",
    "잠재위험시나리오",
    "potentialriskscenario",
    "riskscenario",
  ].includes(key(s));
function header(cells) {
  const scenario = cells.findIndex(isScenario);
  return scenario < 0
    ? null
    : {
        scenario,
        number: cells.findIndex((c) =>
          ["번호", "no", "number"].includes(key(c)),
        ),
        title: cells.findIndex((c) =>
          ["구분", "항목", "명칭", "title"].includes(key(c)),
        ),
      };
}
function row(cells, h, source) {
  return {
    number: cleanCell(cells[h.number]) || "",
    title: cleanCell(cells[h.title]) || "",
    scenario: cleanCell(cells[h.scenario]),
    source,
  };
}
export function parseDelimited(text, delimiter = ",") {
  const rows = [];
  let cells = [],
    cell = "",
    quoted = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (ch === '"') {
      if (quoted && text[i + 1] === '"') {
        cell += '"';
        i++;
      } else if (quoted || !cell) quoted = !quoted;
      else cell += ch;
    } else if (ch === delimiter && !quoted) {
      cells.push(cell);
      cell = "";
    } else if ((ch === "\n" || ch === "\r") && !quoted) {
      if (ch === "\r" && text[i + 1] === "\n") i++;
      cells.push(cell);
      rows.push(cells);
      cells = [];
      cell = "";
    } else cell += ch;
  }
  if (cell || cells.length) {
    cells.push(cell);
    rows.push(cells);
  }
  return rows;
}
function markdownCells(line) {
  let s = line.trim();
  if (s.startsWith("|")) s = s.slice(1);
  if (s.endsWith("|") && !s.endsWith("\\|")) s = s.slice(0, -1);
  const cells = [];
  let value = "";
  for (let i = 0; i < s.length; i++) {
    if (s[i] === "\\" && s[i + 1] === "|") {
      value += "|";
      i++;
    } else if (s[i] === "|") {
      cells.push(value);
      value = "";
    } else value += s[i];
  }
  cells.push(value);
  return cells;
}
export function parseScenarios(text) {
  const lines = String(text)
    .replace(/^\uFEFF/, "")
    .split(/\r?\n/);
  let rows = [],
    h = null;
  for (const line of lines) {
    if (!line.trim().startsWith("|")) {
      h = null;
      continue;
    }
    const cells = markdownCells(line),
      found = header(cells);
    if (found) {
      h = found;
      continue;
    }
    if (!h || cells.every((c) => /^\s*:?-+:?\s*$/.test(c))) continue;
    const r = row(cells, h, "Markdown 표");
    if (r.scenario || r.number || r.title) rows.push(r);
  }
  if (rows.length)
    return {
      rows: numberRows(rows),
      mode: "table",
      message: `잠재리스크 시나리오 ${rows.length}개 행을 추출했습니다.`,
    };
  for (const delimiter of ["\t", ","]) {
    h = null;
    const parsed = parseDelimited(String(text), delimiter);
    for (const cells of parsed) {
      const found = header(cells);
      if (found) {
        h = found;
        continue;
      }
      if (cells.length < 2) {
        h = null;
        continue;
      }
      if (h) {
        const r = row(cells, h, "표");
        if (r.scenario || r.number || r.title) rows.push(r);
      }
    }
    if (rows.length)
      return {
        rows: numberRows(rows),
        mode: "table",
        message: "잠재리스크 시나리오 컬럼만 추출했습니다.",
      };
  }
  // Also accept the previous heading-based Markdown export, without its mitigation sections.
  let item = null,
    collect = false;
  for (const line of lines) {
    const title = line.match(/^##\s+(\d+)[.)]\s*(.+)/);
    if (title) {
      if (item?.hasScenario) rows.push(item);
      item = {
        number: title[1],
        title: cleanCell(title[2]),
        scenario: "",
        source: "Markdown",
      };
      collect = false;
      continue;
    }
    if (/^#{1,6}\s/.test(line)) {
      collect = Boolean(item && isScenario(line.replace(/^#+\s*/, "")));
      if (collect) item.hasScenario = true;
      continue;
    }
    if (collect && item) item.scenario += line + "\n";
  }
  if (item?.hasScenario) rows.push(item);
  if (rows.length)
    return {
      rows: numberRows(
        rows.map((r) => ({ ...r, scenario: cleanCell(r.scenario) })),
      ),
      mode: "sections",
      message: "잠재리스크 시나리오 항목만 추출했습니다.",
    };
  const mixed =
    /(잠재\s*리스크\s*시나리오|사회적\s*영향|영향받는\s*자|완화\s*방안|사업\s*[/·]?\s*개발\s*검토|Requirements)/i.test(
      text,
    );
  if (mixed)
    return {
      rows: [{ number: "1", title: "", scenario: "", source: "직접 입력" }],
      mode: "review",
      message:
        "행·열 경계를 확인할 수 없습니다. 원문에서 잠재리스크 시나리오만 아래 행에 옮겨 주세요. 여러 항목이면 행을 추가해 각각 입력해 주세요.",
    };
  return {
    rows: [
      {
        number: "1",
        title: "",
        scenario: cleanCell(text),
        source: "직접 입력",
      },
    ],
    mode: "plain",
    message:
      "한 개의 시나리오로 읽었습니다. 검색할 내용만 포함됐는지 확인해 주세요.",
  };
}
function numberRows(rows) {
  return rows.map((r, i) => ({ ...r, number: r.number || String(i + 1) }));
}
export function scenariosMarkdown(rows) {
  const esc = (s) => String(s).replace(/\|/g, "\\|").replace(/\n/g, "<br>");
  return (
    "| 번호 | 구분 | 잠재리스크 시나리오 |\n| --- | --- | --- |\n" +
    rows
      .map(
        (r, i) =>
          `| ${esc(r.number || i + 1)} | ${esc(r.title || "")} | ${esc(r.scenario)} |`,
      )
      .join("\n")
  );
}
