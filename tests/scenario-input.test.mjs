import test from "node:test";
import assert from "node:assert/strict";
import {
  parseScenarios,
  scenariosMarkdown,
} from "../assets/research/heart-risk-taxonomy/scenario-input.js";
import { extractPdfScenarios } from "../assets/research/heart-risk-taxonomy/pdf-scenarios.js";
const table =
  "| 번호 | 구분 | **잠재리스크 시나리오** | 완화방안 예시 |\n| --- | --- | --- | --- |\n| 1 | 입력A | 개인정보를 동의 없이 수집한다. | 로봇 안전 시험 |\n| 2 | 입력B | 보행자를 인식하지 못해 충돌한다. | 개인정보 삭제 |";
test("Markdown only selects named scenario cells, ignores unrelated tables", () => {
  const r = parseScenarios(
    table + "\n\n| 문항 | 답변 |\n| --- | --- |\n| 무관 | 프롬프트 공격 |",
  );
  assert.equal(r.rows.length, 2);
  assert.equal(r.rows[0].scenario, "개인정보를 동의 없이 수집한다.");
  assert.ok(!r.rows.some((x) => x.scenario.includes("삭제")));
  assert.deepEqual(
    parseScenarios(scenariosMarkdown(r.rows)).rows.map((x) => x.scenario),
    r.rows.map((x) => x.scenario),
  );
});
test("quoted CSV and TSV retain multiline cells without mixing neighboring columns", () => {
  const r = parseScenarios(
    '번호,구분,잠재리스크 시나리오,완화방안\n1,A,"개인정보를 수집하고,\n동의 없이 사용한다.",차단\n2,B,잘못된 추천,검토',
  );
  assert.equal(r.rows.length, 2);
  assert.match(r.rows[0].scenario, /수집하고,\n동의 없이/);
  assert.equal(
    parseScenarios(
      "번호\t잠재리스크 시나리오\t완화방안\n1\t잘못된 추천\t안전필터",
    ).rows[0].scenario,
    "잘못된 추천",
  );
});
test("heading export only reads scenario section; flattened mixed input requires manual review", () => {
  const r = parseScenarios(
    "## 1. 항목\n### 잠재리스크 시나리오\n잘못된 추천\n### 사회적 영향\n비용\n### 완화방안 예시\n보안시험",
  );
  assert.equal(r.rows[0].scenario, "잘못된 추천");
  const loose = parseScenarios(
    "1 2추천오계산개인정보사회적 영향완화방안 예시차단",
  );
  assert.equal(loose.mode, "review");
  assert.equal(loose.rows[0].scenario, "");
});
const item = (str, x, y, width = 20) => ({
  str,
  transform: [8, 0, 0, 8, x, y],
  width,
});
test("PDF coordinates select only scenario column, continue rows across pages, stop at next section", () => {
  const r = extractPdfScenarios([
    {
      width: 600,
      items: [
        item("번호", 20, 700),
        item("구분", 60, 700),
        item("잠재리스크", 160, 700),
        item("사회적", 300, 700),
        item("1", 20, 650),
        item("항목", 60, 650),
        item("개인정보", 160, 650),
        item("유출", 300, 650),
      ],
    },
    {
      width: 600,
      items: [
        item("수집", 160, 740),
        item("2", 20, 680),
        item("다음", 60, 680),
        item("보행자", 160, 680),
        item("[1차 영향평가]", 20, 600),
        item("다른 답변", 160, 550),
      ],
    },
  ]);
  assert.equal(r.rows.length, 2);
  assert.equal(r.rows[0].scenario, "개인정보 수집");
  assert.equal(r.rows[1].scenario, "보행자");
});
test("changing every non-scenario column leaves extracted queries identical", () => {
  const altered = table
    .replaceAll("입력A", "전혀 다른 제목")
    .replaceAll("로봇 안전 시험", "프롬프트 주입 개인정보 메모리 차별")
    .replaceAll("개인정보 삭제", "보행자 충돌 로봇 파괴");
  assert.deepEqual(
    parseScenarios(table).rows.map((r) => r.scenario),
    parseScenarios(altered).rows.map((r) => r.scenario),
  );
});
test("blank scenario rows are kept for user correction rather than silently dropped", () => {
  const r = parseScenarios(
    "| 번호 | 구분 | 잠재리스크 시나리오 |\n| --- | --- | --- |\n| 1 | 있음 | 정상 내용 |\n| 2 | 빈칸 | |",
  );
  assert.equal(r.rows.length, 2);
  assert.equal(r.rows[1].scenario, "");
});
test("security payload text is preserved as data", () => {
  assert.equal(
    parseScenarios("LLM이 <script>alert(1)</script>를 출력한다.").rows[0]
      .scenario,
    "LLM이 <script>alert(1)</script>를 출력한다.",
  );
});
