import test from "node:test";
import assert from "node:assert/strict";
import { buildResultsCsv } from "../assets/research/heart-risk-taxonomy/results-csv.js";
import { parseDelimited } from "../assets/research/heart-risk-taxonomy/scenario-input.js";
const candidate = (id) => ({
  row: {
    L3_ID: "G_SYS_CONTEXT",
    L3_Title_ko: "맥락 인식 실패",
    L3_Title_en: "Context",
    L3_Description_ko: "상위 정의",
    L3_Description_en: "Parent definition",
    L4_ID: id,
    L4_Title_ko: "한글 명칭",
    L4_Title_en: "English title",
    L4_Description_ko: '쉼표, 따옴표 "내용"\n다음 줄',
    L4_Description_en: "Definition",
  },
  matched: ["정보", "해석"],
});
test("CSV preserves Korean, commas, quotes, newlines and visible scenario/rank order", () => {
  const scenario = '고객 정보, 조건을 "잘못" 해석\n추천 오류';
  const csv = buildResultsCsv([
    {
      number: "7",
      title: "입력",
      scenario,
      results: [candidate("FIRST"), candidate("SECOND")],
    },
    { number: "8", title: "없음", scenario: "다음 입력", results: [] },
  ]);
  assert.ok(csv.startsWith("\uFEFF"));
  const rows = parseDelimited(csv.slice(1));
  assert.equal(rows.length, 4);
  assert.equal(rows[0].length, 17);
  assert.equal(rows[1][3], scenario);
  assert.equal(rows[1][11], "FIRST");
  assert.equal(rows[2][11], "SECOND");
  assert.equal(rows[1][14], '쉼표, 따옴표 "내용"\n다음 줄');
  assert.equal(rows[3][4], "관련 후보 없음");
  assert.equal(rows[3][1], "8");
  assert.ok(rows.every((row) => row.length === 17));
});
test("spreadsheet formula prefixes are saved as text", () => {
  const rows = parseDelimited(
    buildResultsCsv([
      {
        number: "=1+1",
        title: " @SUM(1,2)",
        scenario: "+COMMAND",
        results: [],
      },
    ]).slice(1),
  );
  assert.equal(rows[1][1], "'=1+1");
  assert.equal(rows[1][2], "' @SUM(1,2)");
  assert.equal(rows[1][3], "'+COMMAND");
});
