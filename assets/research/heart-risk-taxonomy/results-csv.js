const HEADERS = [
  "입력 순서",
  "원본 번호",
  "구분",
  "잠재리스크 시나리오",
  "검색 상태",
  "관련도 순위",
  "L3_ID",
  "L3_명칭_국문",
  "L3_명칭_영문",
  "L3_정의_국문",
  "L3_정의_영문",
  "L4_ID",
  "L4_명칭_국문",
  "L4_명칭_영문",
  "L4_정의_국문",
  "L4_정의_영문",
  "일치 표현",
];
function csvCell(value) {
  let text = String(value ?? "");
  // Spreadsheet applications must treat user-authored content as text, not formulas.
  if (/^[\s\uFEFF]*[=+@-]|^[\t\r]/.test(text)) text = "'" + text;
  return '"' + text.replaceAll('"', '""') + '"';
}
export function buildResultsCsv(groups) {
  const rows = [HEADERS];
  groups.forEach((group, index) => {
    const candidates = group.results.length ? group.results : [null];
    candidates.forEach((candidate, rank) => {
      const r = candidate?.row || {};
      rows.push([
        index + 1,
        group.number,
        group.title,
        group.scenario,
        candidate ? "연관 후보" : "관련 후보 없음",
        candidate ? rank + 1 : "",
        r.L3_ID,
        r.L3_Title_ko,
        r.L3_Title_en,
        r.L3_Description_ko,
        r.L3_Description_en,
        r.L4_ID,
        r.L4_Title_ko,
        r.L4_Title_en,
        r.L4_Description_ko,
        r.L4_Description_en,
        candidate?.matched?.join(" · ") || "",
      ]);
    });
  });
  return (
    "\uFEFF" +
    rows.map((row) => row.map(csvCell).join(",")).join("\r\n") +
    "\r\n"
  );
}
