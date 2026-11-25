/* Independent CPS + own THAIE. Quantile colors and white halos never alter the data. */
(() => {
  "use strict";
  const $ = (id) => document.getElementById(id),
    NS = "http://www.w3.org/2000/svg";
  const colors = ["#B8B8B8", "#DDDDDD", "#F3D4D7", "#E5A2AA", "#C64F5A"];
  const ageColors = [
    "#769A98",
    "#8DA4B4",
    "#A393AE",
    "#B8A180",
    "#8D9D85",
    "#9E8C99",
  ];
  const state = {
    age: "22–25",
    outcome: "FT",
    occupation: "1021",
    comparison: "quintiles",
  };
  const axes = ["E", "FT", "PT"],
    names = {
      E: "employment",
      FT: "full-time employment",
      PT: "part-time employment",
    };
  let data;
  const plotted = new Map();
  const el = (tag, attrs = {}, text) => {
    const n = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([k, v]) => n.setAttribute(k, v));
    if (text !== undefined) n.textContent = text;
    return n;
  };
  function points(row) {
    const i = axes.indexOf(state.outcome) + 1;
    const result = row.points.map((p, j, source) => {
      const observed = p[i] !== null && p[i+3] >= 30;
      if (!observed && p[0] === "2025-10-01") {
        const before = source.find(v => v[0] === "2025-09-01"), after = source.find(v => v[0] === "2025-11-01");
        if (before && after && before[i] !== null && after[i] !== null && before[i+3] >= 30 && after[i+3] >= 30)
          return {date:p[0], value:(before[i]+after[i])/2, n:null, estimated:true};
      }
      return {date:p[0], value:observed ? p[i] : null, n:p[i+3], estimated:false};
    });
    {
      const base = result.find(p => p.date === "2022-11-01");
      return result.filter(p => p.date >= "2022-11-01").map(p => ({...p, value:base && base.value > 0 && p.value !== null ? p.value/base.value*100 : null}));
    }
    return result;
  }

  function rawRows(age, sex = "All") {
    const family =
      state.comparison === "quintiles" ? data.cps_exposure : data.cps_contrast;
    return family
      .filter((r) => r.age === age && r.sex === sex)
      .map((r) => ({
        ...r,
        label: r.band || `Q${r.quintile}`,
        isQ5: r.band === "Q5" || r.quintile === 5,
        color: r.band
          ? r.band === "Q5"
            ? colors[4]
            : colors[1]
          : colors[r.quintile - 1],
      }));
  }
  function change(row) {
    if (!row) return null;
    const valid = points(row).filter(p => p.value !== null && !p.estimated);
    const base = valid.find(p => p.date === "2022-11-01"), last = valid.find(p => p.date === "2026-10-01");
    return base && last ? (last.value/base.value-1)*100 : null;
  }

  const pct = (v) =>
    v === null ? "unavailable" : `${v >= 0 ? "+" : ""}${v.toFixed(1)}%`;
  function narrative(age, sex = "All") {
    const rows = data.cps_contrast.filter(
        (r) => r.age === age && r.sex === sex,
      ),
      a = change(rows.find((r) => r.band === "Q5")),
      b = change(rows.find((r) => r.band === "Q1–Q4"));
    if (a === null || b === null)
      return "The selected monthly cells do not support a complete matched-period comparison. Missing values are not zero employment.";
    return `From November 2022 to October 2026, Q5 ${names[state.outcome]} changed ${pct(a)}, compared with ${pct(b)} in Q1–Q4. These are descriptive headcounts, not a causal estimate.`;
  }
  function legend(box, rows) {
    const leg = document.createElement("div");
    leg.className = "story-legend";
    rows.forEach((r) => {
      const s = document.createElement("span");
      s.className = r.isQ5 ? "is-q5" : "";
      const i = document.createElement("i");
      i.style.background = r.color;
      i.style.height = "3px";
      s.append(
        i,
        document.createTextNode(r.isQ5 ? "Q5 · highest THAIE" : r.label),
      );
      leg.append(s);
    });
    box.append(leg);
  }
  function chart(id, rows, title, commonDomain) {
    const box = $(id);
    box.replaceChildren();
    plotted.set(id, { rows, title });
    const all = rows.flatMap(points),
      good = all.filter((p) => p.value !== null && Number.isFinite(p.value));
    if (!good.length) {
      const p = document.createElement("p");
      p.className = "empty-chart";
      p.textContent =
        "No monthly cells meet the support threshold for this selection. Download the support audit for details.";
      box.append(p);
      return;
    }
    const twin = box.closest(".gender-panels") !== null;
    const width = Math.max(
        twin ? 420 : 720,
        Math.round(box.getBoundingClientRect().width) || 1000,
      ),
      height = 450,
      m = { l: 64, r: twin ? 95 : 175, t: 65, b: 65 };
    const dates = rows.flatMap((r) => points(r).map((p) => Date.parse(p.date))),
      xmin = Math.min(...dates),
      xmax = Math.max(...dates),
      values = good.map((p) => p.value);
    let low = commonDomain ? commonDomain[0] : Math.min(100, ...values),
      high = commonDomain ? commonDomain[1] : Math.max(100, ...values);
    const pad = Math.max(4, (high - low) * 0.12);
    low -= pad;
    high += pad;
    const x = (d) =>
        m.l + ((Date.parse(d) - xmin) / (xmax - xmin)) * (width - m.l - m.r),
      y = (v) =>
        height - m.b - ((v - low) / (high - low)) * (height - m.t - m.b);
    const svg = el("svg", {
      xmlns: NS,
      viewBox: `0 0 ${width} ${height}`,
      role: "img",
      "aria-label": title,
    });
    svg.append(el("title", {}, title));
    svg.append(
      el(
        "desc",
        {},
        rows.some((r) => r.isQ5)
          ? "Our CPS reconstruction. Each curve uses its own November 2022 baseline of 100. Q5 is the warm-red line; all quintile lines have equal width; other exposure groups use muted colors. Gaps are unavailable or low-support months."
          : "Our CPS reconstruction. Exposure is held fixed in this view; muted colors identify age groups. Each curve uses its own November 2022 baseline of 100.",
      ),
    );
    svg.append(el("rect", { x: 0, y: 0, width, height, fill: "white" }));
    for (let j = 0; j < 5; j++) {
      const v = low + ((high - low) * j) / 4;
      svg.append(
        el("line", {
          x1: m.l,
          x2: width - m.r,
          y1: y(v),
          y2: y(v),
          stroke: "#e8ebee",
          "stroke-width": 0.75,
        }),
      );
      svg.append(
        el(
          "text",
          {
            x: m.l - 12,
            y: y(v) + 5,
            "text-anchor": "end",
            fill: "#58626b",
            "font-size": 14,
            "font-family": "Arial,sans-serif",
          },
          v.toFixed(0),
        ),
      );
    }
    if (low < 100 && high > 100)
      svg.append(
        el("line", {
          x1: m.l,
          x2: width - m.r,
          y1: y(100),
          y2: y(100),
          stroke: "#acb1b7",
          "stroke-width": 0.9,
        }),
      );
    const months = [...new Set(rows.flatMap(r => points(r).map(p => p.date)))].sort();
    const labelStep = Math.max(1, Math.ceil(months.length / Math.max(2, Math.floor((width-m.l-m.r)/65))));
    months.forEach((date, i) => {
      const tick = el("line", {x1:x(date), x2:x(date), y1:height-m.b, y2:height-m.b+4, stroke:"#aeb4b9", "stroke-width":0.7});
      tick.append(el("title", {}, date.slice(0,7)));
      svg.append(tick);
      if (i % labelStep === 0 || i === months.length-1) {
        if (i === months.length-1 && months.length > 1 && i % labelStep < labelStep/2) return;
        svg.append(el("text", {x:x(date), y:height-m.b+23, "text-anchor":"middle", fill:"#58626b", "font-size":11, "font-family":"Arial,sans-serif"}, date.slice(0,7)));
      }
    });
    const event = "2022-11-30";
    svg.append(
      el("line", {
        x1: x(event),
        x2: x(event),
        y1: m.t,
        y2: height - m.b,
        stroke: "#8d959d",
        "stroke-width": 0.9,
        "stroke-dasharray": "3 5",
      }),
    );
    svg.append(
      el(
        "text",
        {
          x: x(event) + 8,
          y: m.t - 12,
          fill: "#6e757d",
          "font-size": 12,
          "font-family": "Arial,sans-serif",
        },
        "Nov 30, 2022",
      ),
    );
    const gap = x("2025-10-01");
    svg.append(
      el("rect", {
        x: gap - 3,
        y: m.t,
        width: 6,
        height: height - m.t - m.b,
        fill: "#e9ecef",
        opacity: 0.65,
      }),
    );
    svg.append(
      el(
        "text",
        {
          x: m.l,
          y: 20,
          fill: "#263039",
          "font-size": 15,
          "font-weight": 600,
          "font-family": "Arial,sans-serif",
        },
        title,
      ),
    );
    svg.append(
      el(
        "text",
        {
          x: m.l,
          y: 40,
          fill: "#58626b",
          "font-size": 12,
          "font-family": "Arial,sans-serif",
        },
        "Employment index · November 2022 = 100",
      ),
    );
    // Shade only matched, supported months; preserve all missing-month gaps.
    if (rows.length === 2 && rows.every(r => r.sexLabel)) {
      const left = points(rows[0]);
      const right = new Map(points(rows[1]).map(p => [p.date, p]));
      let segment = [];
      const drawBand = () => {
        if (segment.length > 1) {
          const upper = segment.map(([a]) => `${x(a.date)},${y(a.value)}`);
          const lower = [...segment].reverse().map(([, b]) => `${x(b.date)},${y(b.value)}`);
          svg.append(el("path", {d: "M"+upper.join(" L")+" L"+lower.join(" L")+" Z", fill: "#DADADA", "fill-opacity": 0.48, stroke: "none", "data-role": "sex-gap-band"}));
        }
        segment = [];
      };
      for (const a of left) {
        const b = right.get(a.date);
        if (a.value === null || a.estimated || !b || b.value === null || b.estimated) { drawBand(); continue; }
        if (segment.length) {
          const prior = new Date(segment.at(-1)[0].date), now = new Date(a.date);
          if ((now.getUTCFullYear()-prior.getUTCFullYear())*12+now.getUTCMonth()-prior.getUTCMonth() !== 1) drawBand();
        }
        segment.push([a,b]);
      }
      drawBand();
    }
    const sorted = [...rows].sort((a, b) => Number(a.isQ5) - Number(b.isQ5)),
      labels = [];
    for (const r of sorted) {
      const ps = points(r);
      let d = "",
        active = false;
      for (const p of ps) {
        if (p.value === null || p.estimated) {
          active = false;
          continue;
        }
        d += `${active ? "L" : "M"}${x(p.date).toFixed(2)},${y(p.value).toFixed(2)} `;
        active = true;
      }
      const lw = 3.1;
      svg.append(
        el("path", {
          d,
          fill: "none",
          stroke: "white",
          "stroke-width": lw + 1.9,
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
        }),
      );
      svg.append(
        el("path", {
          d,
          fill: "none",
          stroke: r.color,
          "stroke-width": lw,
          "stroke-opacity": r.isQ5 ? 1 : 0.86,
          "stroke-linecap": "round",
          "stroke-linejoin": "round",
          ...(r.context ? { "stroke-dasharray": "4 5" } : {}),
        }),
      );
      const estimate = ps.find(p => p.estimated);
      if (estimate) {
        const before = ps.find(p => p.date === "2025-09-01"), after = ps.find(p => p.date === "2025-11-01");
        const bridge = `M${x(before.date)},${y(before.value)} L${x(estimate.date)},${y(estimate.value)} L${x(after.date)},${y(after.value)}`;
        svg.append(el("path", {d:bridge, fill:"none", stroke:"white", "stroke-width":lw+1.9}));
        svg.append(el("path", {d:bridge, fill:"none", stroke:r.color, "stroke-width":lw, "stroke-dasharray":"6 5", "data-role":"interpolated-October-2025"}));
      }
      const valid = ps.filter((p) => p.value !== null);
      if (valid.length) {
        const last = valid.at(-1);
        labels.push({
          row: r,
          point: last,
          target: y(last.value),
          actual: y(last.value),
        });
      }
      ps.filter((p) => p.value !== null).forEach((p) => {
        const c = el("circle", {
          cx: x(p.date),
          cy: y(p.value),
          r: 5,
          fill: "transparent",
        });
        c.append(
          el(
            "title",
            {},
            `${r.label} · ${p.date.slice(0, 7)} · ${p.value.toFixed(2)} · ${p.estimated ? "interpolated estimate; no observed sample" : "unweighted n="+Math.round(p.n)}`,
          ),
        );
        svg.append(c);
      });
    }
    labels.sort((a, b) => a.target - b.target);
    for (let j = 1; j < labels.length; j++)
      labels[j].target = Math.max(labels[j].target, labels[j - 1].target + 38);
    if (labels.length && labels.at(-1).target > height - m.b - 3) {
      const excess = labels.at(-1).target - (height - m.b - 3);
      labels.forEach((l) => (l.target -= excess));
    }
    for (const item of labels) {
      const r = item.row,
        x0 = x(item.point.date);
      svg.append(
        el("path", {
          d: `M${x0},${item.actual} L${width - m.r + 11},${item.target} L${width - m.r + 19},${item.target}`,
          stroke: r.color,
          fill: "none",
          "stroke-width": 1.4,
          "stroke-opacity": 0.7,
        }),
      );
      const txt = el(
        "text",
        {
          x: width - m.r + 24,
          y: item.target + 4,
          fill: r.color,
          "font-size": 14,
          "font-weight": 600,
          "font-family": "Arial,sans-serif",
        },
        "",
      );
      const q = r.sexLabel ? null : r.quintile || (r.band === "Q5" ? 5 : null);
      const name = q ? `Quintile ${q}` : r.context ? "All Occupations" : r.band === "Q1–Q4" ? "Quintiles 1–4" : r.label;
      txt.append(el("tspan", {x: width - m.r + 24, dy: 0}, name));
      if (q === 1 || q === 5) txt.append(el("tspan", {x: width - m.r + 24, dy: 16}, q === 1 ? "(least exposed)" : "(most exposed)"));
      svg.append(txt);
    }
    svg.append(
      el(
        "text",
        {
          x: m.l,
          y: height - 10,
          fill: "#777f86",
          "font-size": 11,
          "font-family": "Arial,sans-serif",
        },
        "Monthly observations · YYYY-MM · Basic Monthly CPS · not seasonally adjusted",
      ),
    );
    box.append(svg);
    legend(box, rows);
  }
  function render(name) {
    if (!data) return;
    if (name === "overall") {
      chart(
        "chart-overall",
        rawRows(state.age),
        `${state.age === "All ages (16+)" ? "All ages (16+)" : "Ages " + state.age} · ${names[state.outcome]} by THAIE`,
      );
      $("overview-reading").textContent = narrative(state.age);
      $("overview-scope").textContent = `${state.age === "All ages (16+)" ? "All workers aged 16 and older" : "Workers aged " + state.age}, grouped by occupational THAIE. Changes with the selected age group.`;
    }
    if (name === "age") {
      chart(
        "chart-age",
        rawRows(state.age),
        `Ages ${state.age} · ${names[state.outcome]} by THAIE`,
      );
      $("age-reading").textContent = narrative(state.age);
    }
    if (name === "occupation") {
      const scope = state.occupation,
        family = scope === "computer_math",
        label = family
          ? "Computer and mathematical occupations"
          : data.metadata.occupations[scope];
      const rows = data.cps_occupation
        .filter(
          (r) =>
            r.scope === scope &&
            r.sex === "All" &&
            data.metadata.ages.includes(r.age),
        )
        .map((r) => ({
          ...r,
          label: "Ages " + r.age,
          color: ageColors[data.metadata.ages.indexOf(r.age)],
          isQ5: false,
        }));
      chart("chart-occupation", rows, label + " by age");
      const record = data.metadata.occupation_quintiles.find(
        (r) => String(r.occ) === scope,
      );
      $("occupation-classification").textContent = family
        ? "Mixed THAIE exposure"
        : "THAIE Q" + record.THAIE_q;
      $("occupation-reading").textContent = family
        ? "This broad family contains multiple detailed occupations. The age chart holds the family fixed; the optional panel below compares its available exposure groups."
        : `${label} is assigned to THAIE Q${record.THAIE_q} in our method. This chart holds the occupation fixed, so color identifies age rather than five within-occupation exposure groups.`;
      $("computer-wrap").hidden = !family;
      if (family) {
        const source =
          state.comparison === "quintiles"
            ? data.cps_computer
            : data.cps_computer_contrast;
        chart(
          "chart-computer",
          source
            .filter((r) => r.age === state.age && r.sex === "All")
            .map((r) => ({
              ...r,
              label: r.band || "Q" + r.quintile,
              isQ5: r.band === "Q5" || r.quintile === 5,
              color: r.band
                ? r.band === "Q5"
                  ? colors[4]
                  : colors[1]
                : colors[r.quintile - 1],
            })),
          `Computer/mathematical occupations · ages ${state.age}`,
        );
      }
    }
    if (name === "sex") {
      const panels = [1, 2, 3, 4, 5, 6].map(q => {
        const rows = ["Women", "Men"].map(sex => {
          const r = q === 6
            ? data.cps_allmapped.find(r => r.age === state.age && r.sex === sex)
            : data.cps_exposure.find(r => r.age === state.age && r.sex === sex && r.quintile === q);
          return r ? {...r, label: sex, sexLabel: sex, color: sex === "Women" ? "#969696" : "#C64F5A", isQ5: false} : null;
        }).filter(Boolean);
        return {q, rows};
      });
      const values = panels.flatMap(p => p.rows).flatMap(points).filter(p => p.value !== null).map(p => p.value);
      const domain = values.length ? [Math.min(100, ...values), Math.max(100, ...values)] : undefined;
      for (const {q, rows} of panels) chart("chart-sex-"+q, rows, q === 6 ? "All mapped occupations" : "Quintile "+q+(q === 1 ? " · least exposed" : q === 5 ? " · most exposed" : ""), domain);
      const a = change(
          data.cps_contrast.find(
            (r) => r.age === state.age && r.sex === "Women" && r.band === "Q5",
          ),
        ),
        b = change(
          data.cps_contrast.find(
            (r) => r.age === state.age && r.sex === "Men" && r.band === "Q5",
          ),
        );
      $("sex-reading").textContent =
        a !== null && b !== null
          ? `Within Q5, ${names[state.outcome]} changed ${pct(a)} for women and ${pct(b)} for men from November 2022 to October 2026. The plotted series use November 2022 = 100 and start in November 2022; this comparison does not establish a causal sex difference.`
          : "The selected cells do not support a complete matched-period comparison. All six panels use the same vertical scale.";
    }
  }
  function update() {
    state.outcome = $("outcome").value;
    state.occupation = $("occupation").value;
    state.comparison = $("comparison").value;
    document
      .querySelectorAll("[data-age]")
      .forEach((b) =>
        b.setAttribute("aria-pressed", String(b.dataset.age === state.age)),
      );
    document
      .querySelectorAll(".story-card[open][data-story]")
      .forEach((card) => render(card.dataset.story));
    $("story-status").textContent =
      `Our CPS reconstruction · THAIE only · ${state.outcome === "FT" ? "Full-time" : state.outcome === "PT" ? "Part-time" : "Total employment"} · November 2022–October 2026. October 2025 is interpolated between September and November and shown as dashed lines; regressions use observed months.`;
  }
  function csv(id) {
    const plottedChart = plotted.get(id);
    if (!plottedChart) return;
    const lines = ["series,date,index,unweighted_n,status"];
    for (const r of plottedChart.rows)
      for (const p of points(r))
        lines.push(
          [r.label, p.date, p.value ?? "", p.n ?? "", p.estimated ? "interpolated" : "observed"]
            .map((v) => '"' + String(v).replaceAll('"', '""') + '"')
            .join(","),
        );
    save(new Blob([lines.join("\n")], { type: "text/csv" }), id + ".csv");
  }
  function save(blob, name) {
    const a = document.createElement("a"),
      url = URL.createObjectURL(blob);
    a.href = url;
    a.download = name;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  function svg(id) {
    const n = $(id).querySelector("svg");
    if (n)
      save(
        new Blob([new XMLSerializer().serializeToString(n)], {
          type: "image/svg+xml",
        }),
        id + ".svg",
      );
  }
  fetch("data/monthly.json?v=all-nov2022-base-20261125")
    .then((r) => {
      if (!r.ok) throw new Error("CPS data unavailable");
      return r.json();
    })
    .then((d) => {
      data = d;
      for (const id of [
        "outcome",
        "occupation",
        "comparison",
      ])
        $(id).addEventListener("change", update);
      document.querySelectorAll("[data-age]").forEach((button) =>
        button.addEventListener("click", () => {
          state.age = button.dataset.age;
          update();
        }),
      );
      document.querySelectorAll(".story-card[data-story]").forEach((card) =>
        card.addEventListener("toggle", () => {
          if (card.open) render(card.dataset.story);
        }),
      );
      document
        .querySelectorAll("[data-csv]")
        .forEach((button) =>
          button.addEventListener("click", () => csv(button.dataset.csv)),
        );
      document
        .querySelectorAll("[data-svg]")
        .forEach((button) =>
          button.addEventListener("click", () => svg(button.dataset.svg)),
        );
      $("expand-stories").addEventListener("click", () => {
        document
          .querySelectorAll(".story-card[data-story]")
          .forEach((card) => (card.open = true));
      });
      $("story-loading").hidden = true;
      $("story-controls").hidden = false;
      update();
      let timer;
      window.addEventListener("resize", () => {
        clearTimeout(timer);
        timer = setTimeout(update, 200);
      });
    })
    .catch((e) => {
      $("story-loading").textContent =
        "The CPS chart data could not be loaded. The downloadable data and model results remain available below. " +
        e.message;
    });
})();
