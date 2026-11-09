// Text coordinates are used only for the table with the scenario column.
export function extractPdfScenarios(pages) {
  const result = [];
  let columns = null,
    current = null,
    foundHeader = false,
    active = false;
  for (const page of pages) {
    const lines = [];
    for (const item of page.items
      .filter((i) => i.str?.trim())
      .sort(
        (a, b) =>
          b.transform[5] - a.transform[5] || a.transform[4] - b.transform[4],
      )) {
      let line = lines.find((l) => Math.abs(l.y - item.transform[5]) < 2);
      if (!line) {
        line = { y: item.transform[5], items: [] };
        lines.push(line);
      }
      line.items.push(item);
    }
    for (const line of lines.sort((a, b) => b.y - a.y)) {
      const items = line.items.sort((a, b) => a.transform[4] - b.transform[4]);
      const joined = items
        .map((i) => i.str)
        .join("")
        .replace(/\s/g, "");
      const scenario = items.find(
        (i) =>
          i.str.replace(/\s/g, "").includes("잠재리스크") ||
          i.str.replace(/\s/g, "").includes("잠재위험"),
      );
      const number = items.find((i) => i.str.trim() === "번호"),
        title = items.find((i) => i.str.trim() === "구분"),
        impact = items.find((i) =>
          i.str.replace(/\s/g, "").startsWith("사회적"),
        );
      if (scenario && number && title && impact) {
        columns = {
          number: (number.transform[4] - 3) / page.width,
          title: (title.transform[4] - 3) / page.width,
          scenario: (scenario.transform[4] - 3) / page.width,
          end: (impact.transform[4] - 3) / page.width,
        };
        foundHeader = true;
        active = true;
        continue;
      }
      if (!active || !columns) continue;
      if (/(?:[12]차영향평가|Requirements|Requirements번호)/i.test(joined)) {
        active = false;
        columns = null;
        continue;
      }
      const inCol = (from, to) => {
        const selected = items.filter(
          (i) =>
            i.transform[4] / page.width >= from &&
            i.transform[4] / page.width < to,
        );
        let text = "",
          last = null;
        for (const i of selected) {
          if (last && i.transform[4] - (last.transform[4] + last.width) > 0.7)
            text += " ";
          text += i.str;
          last = i;
        }
        return text;
      };
      const nr = inCol(columns.number, columns.title).trim();
      if (/^\d{1,3}$/.test(nr)) {
        if (current) result.push(current);
        current = { number: nr, title: "", scenario: "", source: "PDF 표" };
      }
      if (!current) continue;
      const titlePart = inCol(columns.title, columns.scenario),
        part = inCol(columns.scenario, columns.end);
      // Skip repeated, wrapped header fragments and page footers.
      if (/^(오|시나리오|잠재리스크시나리오)$/.test(part.replace(/\s/g, "")))
        continue;
      if (titlePart) current.title += (current.title ? " " : "") + titlePart;
      if (part) current.scenario += (current.scenario ? " " : "") + part;
    }
  }
  if (current) result.push(current);
  return { rows: result, foundHeader };
}
