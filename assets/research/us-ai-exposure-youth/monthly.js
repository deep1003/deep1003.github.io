/* Monthly aggregate indices. No person-level data, interpolation or external chart service. */
(() => {
  "use strict";
  const $ = (id) => document.getElementById(id),
    NS = "http://www.w3.org/2000/svg";
  const palette = ["#9b171c", "#527d9e", "#f05234", "#d89900", "#401417"];
  const ageColors = [
    "#a9171c",
    "#527d9e",
    "#f05234",
    "#d89900",
    "#62363a",
    "#aa9a89",
  ];
  let data,
    latestSeries = [];
  const node = (tag, attrs = {}, text) => {
    const n = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([k, v]) => n.setAttribute(k, v));
    if (text !== undefined) n.textContent = text;
    return n;
  };
  const keyOut = () => ({ E: 1, FT: 2, PT: 3 })[$("outcome").value];
  function series(rows, labels, colors) {
    return rows.map((r, i) => ({
      ...r,
      label: labels(r),
      color: colors(r, i),
    }));
  }
  function filteredPoints(r) {
    const pos = keyOut();
    return r.points.map((p) => ({
      date: p[0],
      value:
        p[pos] !== null && ($("source").value === "adp" || p[3 + pos] >= 30)
          ? p[pos]
          : null,
      n: p[3 + pos],
    }));
  }
  function chart(id, rows, title, commonY) {
    const box = $(id);
    box.replaceChildren();
    const width = 920,
      height = 405,
      m = { l: 68, r: 24, t: 24, b: 46 };
    const all = rows.flatMap(filteredPoints),
      good = all.filter((p) => p.value !== null && Number.isFinite(p.value));
    const wrapper = document.createElement("div");
    wrapper.className = "chart-title";
    wrapper.textContent = title;
    box.append(wrapper);
    if (!good.length) {
      const p = document.createElement("p");
      p.className = "note";
      p.textContent =
        "No monthly cells meet the display threshold. This is unavailable evidence, not zero employment.";
      box.append(p);
      return;
    }
    const dates = rows.flatMap((r) => r.points.map((p) => Date.parse(p[0]))),
      xmin = Math.min(...dates),
      xmax = Math.max(...dates);
    let low = commonY ? commonY[0] : Math.min(100, ...good.map((p) => p.value)),
      high = commonY ? commonY[1] : Math.max(100, ...good.map((p) => p.value));
    const pad = Math.max(3, (high - low) * 0.12);
    low -= pad;
    high += pad;
    const x = (d) =>
        m.l + ((Date.parse(d) - xmin) / (xmax - xmin)) * (width - m.l - m.r),
      y = (v) =>
        height - m.b - ((v - low) / (high - low)) * (height - m.t - m.b);
    const svg = node("svg", {
      viewBox: `0 0 ${width} ${height}`,
      role: "img",
      "aria-label": title,
    });
    svg.append(node("title", {}, title));
    for (let i = 0; i < 6; i++) {
      const v = low + ((high - low) * i) / 5;
      svg.append(
        node("line", {
          x1: m.l,
          x2: width - m.r,
          y1: y(v),
          y2: y(v),
          stroke: "#e3e5e7",
        }),
      );
      svg.append(
        node(
          "text",
          {
            x: m.l - 10,
            y: y(v) + 5,
            "text-anchor": "end",
            fill: "#4d5660",
            "font-size": 14,
          },
          v.toFixed(0),
        ),
      );
    }
    if (low <= 100 && high >= 100)
      svg.append(
        node("line", {
          x1: m.l,
          x2: width - m.r,
          y1: y(100),
          y2: y(100),
          stroke: "#838991",
          "stroke-width": 1,
        }),
      );
    for (let year = 2020; year <= 2026; year++) {
      const d = `${year}-01-01`;
      if (Date.parse(d) >= xmin && Date.parse(d) <= xmax) {
        svg.append(
          node(
            "text",
            {
              x: x(d),
              y: height - 15,
              "text-anchor": "middle",
              fill: "#4d5660",
              "font-size": 14,
            },
            year,
          ),
        );
      }
    }
    const event = "2022-11-30";
    if (Date.parse(event) >= xmin) {
      svg.append(
        node("line", {
          x1: x(event),
          x2: x(event),
          y1: m.t,
          y2: height - m.b,
          stroke: "#777",
          "stroke-dasharray": "3 4",
        }),
      );
      svg.append(
        node(
          "text",
          { x: x(event) + 6, y: m.t + 10, fill: "#666", "font-size": 12 },
          "ChatGPT launch",
        ),
      );
    }
    if ($("source").value === "cps") {
      const gapx = x("2025-10-01");
      svg.append(
        node("rect", {
          x: gapx - 3,
          y: m.t,
          width: 6,
          height: height - m.b - m.t,
          fill: "#e5e7eb",
          opacity: 0.7,
        }),
      );
    }
    rows.forEach((r) => {
      let path = "",
        active = false;
      for (const p of filteredPoints(r)) {
        if (p.value === null) {
          active = false;
          continue;
        }
        path += `${active ? "L" : "M"}${x(p.date).toFixed(2)},${y(p.value).toFixed(2)} `;
        active = true;
      }
      svg.append(
        node("path", {
          d: path,
          fill: "none",
          stroke: r.color,
          "stroke-width": r.quintile === 5 ? 3 : 1.8,
        }),
      );
      filteredPoints(r)
        .filter((p) => p.value !== null)
        .forEach((p) => {
          const circle = node("circle", {
            cx: x(p.date),
            cy: y(p.value),
            r: 4.5,
            fill: "transparent",
            tabindex: "0",
            "aria-label": `${r.label}, ${p.date.slice(0, 7)}, ${p.value.toFixed(2)}`,
          });
          circle.append(
            node(
              "title",
              {},
              `${r.label} · ${p.date.slice(0, 7)} · ${p.value.toFixed(2)}${p.n === null || p.n === undefined ? "" : ` · unweighted n=${Math.round(p.n)}`}`,
            ),
          );
          svg.append(circle);
        });
    });
    box.append(svg);
    const legend = document.createElement("div");
    legend.className = "legend";
    rows.forEach((r) => {
      const span = document.createElement("span");
      const dot = document.createElement("i");
      dot.style.backgroundColor = r.color;
      span.append(dot, document.createTextNode(r.label));
      legend.append(span);
    });
    box.append(legend);
    latestSeries.push(...rows.map((r) => ({ ...r, chart: title })));
  }
  function exposureRows(source, age, sex) {
    if (source === "adp") {
      const product =
        sex === "All"
          ? age === "All ages (16+)"
            ? "by_exposure"
            : "age_by_exposure"
          : "gender_by_exposure";
      const a = age === "All ages (16+)" ? "All ages (source definition)" : age;
      return data.stanford.filter(
        (r) =>
          r.product === product &&
          r.age === a &&
          r.sex === sex &&
          r.quintile > 0,
      );
    }
    return data.cps_exposure.filter(
      (r) => r.measure === $("measure").value && r.age === age && r.sex === sex,
    );
  }
  function update() {
    latestSeries = [];
    const source = $("source").value,
      age = $("age").value,
      measure = $("measure").value,
      scope = $("occupation").value;
    $("measure").disabled = source === "adp";
    $("outcome").disabled = source === "adp";
    $("occupation").disabled = source === "adp";
    if (source === "adp") $("outcome").value = "E";
    const norm = "2022 monthly mean = 100",
      labelQ = (r) =>
        `Q${r.quintile}${r.quintile === 5 ? " (highest)" : r.quintile === 1 ? " (lowest)" : ""}`,
      colorQ = (r) => palette[r.quintile - 1];
    chart(
      "chart-overall",
      series(exposureRows(source, "All ages (16+)", "All"), labelQ, colorQ),
      `All-worker employment by ${source === "adp" ? "Stanford exposure" : measure} quintile`,
    );
    chart(
      "chart-age",
      series(exposureRows(source, age, "All"), labelQ, colorQ),
      `Ages ${age} by exposure quintile`,
    );
    let occRows;
    if (source === "adp")
      occRows = data.stanford.filter(
        (r) => r.product === "software_developers",
      );
    else
      occRows = data.cps_occupation.filter(
        (r) =>
          r.scope === scope &&
          r.sex === "All" &&
          data.metadata.ages.includes(r.age),
      );
    const name =
      source === "adp"
        ? "Software developers"
        : scope === "computer_math"
          ? "Computer and mathematical occupations"
          : data.metadata.occupations[scope];
    chart(
      "chart-occupation",
      series(
        occRows,
        (r) => `Ages ${r.age}`,
        (r) => ageColors[data.metadata.ages.indexOf(r.age)],
      ),
      `${name} by age`,
    );
    const qRecord = data.metadata.occupation_quintiles.find(
      (r) => String(r.occ) === scope,
    );
    $("occupation-note").textContent =
      source === "adp"
        ? "Stanford classifies software developers in its highest-exposure group. Its public download provides age-specific indices, not five exposure strata within software developers."
        : scope === "computer_math"
          ? "This broad occupational family contains several detailed occupations. Its quintile comparisons reflect differences across those occupations."
          : `${name} is a single detailed occupation, assigned to ${measure} Q${qRecord[measure + "_q"]}. Occupational exposure is fixed, so five within-occupation exposure groups cannot be identified.`;
    const within = source === "cps" && scope === "computer_math";
    $("computer-wrap").hidden = !within;
    if (within)
      chart(
        "chart-computer",
        series(
          data.cps_computer.filter(
            (r) => r.measure === measure && r.age === age && r.sex === "All",
          ),
          labelQ,
          colorQ,
        ),
        `${name}, ages ${age}, by exposure`,
      );
    const women = series(exposureRows(source, age, "Women"), labelQ, colorQ),
      men = series(exposureRows(source, age, "Men"), labelQ, colorQ),
      vals = [...women, ...men]
        .flatMap(filteredPoints)
        .filter((p) => p.value !== null)
        .map((p) => p.value),
      common = vals.length
        ? [Math.min(100, ...vals), Math.max(100, ...vals)]
        : undefined;
    chart("chart-women", women, `Women, ages ${age}`, common);
    chart("chart-men", men, `Men, ages ${age}`, common);
    $("chart-status").textContent =
      source === "cps"
        ? `CPS · January 2020–October 2026 · ${measure} · ${$("outcome").selectedOptions[0].textContent} · ${norm} · not seasonally adjusted. Gaps include unavailable October 2025 and cells with fewer than 30 observations.`
        : `Stanford / ADP · November 2021–October 2026 · source vintage November 15, 2026 · rebased to ${norm}. No ADP values are available for 2020.`;
  }
  function download() {
    const rows = ["chart,series,date,index,unweighted_n"];
    latestSeries.forEach((r) =>
      filteredPoints(r).forEach((p) =>
        rows.push(
          [r.chart, r.label, p.date, p.value ?? "", p.n ?? ""]
            .map((v) => '"' + String(v).replaceAll('"', '""') + '"')
            .join(","),
        ),
      ),
    );
    const a = document.createElement("a"),
      url = URL.createObjectURL(
        new Blob([rows.join("\n")], { type: "text/csv" }),
      );
    a.href = url;
    a.download = "monthly-selected-series.csv";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  fetch("data/monthly.json")
    .then((r) => {
      if (!r.ok) throw new Error(`Data response ${r.status}`);
      return r.json();
    })
    .then((d) => {
      data = d;
      for (const id of ["source", "measure", "age", "outcome", "occupation"])
        $(id).addEventListener("change", update);
      $("download-selected").addEventListener("click", download);
      update();
      $("explorer-loading").hidden = true;
      $("explorer-content").hidden = false;
    })
    .catch((e) => {
      $("explorer-loading").textContent =
        "The monthly data could not be loaded. Download the CSV files below to inspect the results. " +
        e.message;
    });
})();
