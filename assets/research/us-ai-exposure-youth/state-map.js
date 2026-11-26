(() => {
  "use strict";
  const root = document.getElementById("state-youth-map");
  if (!root) return;
  const ns = "http://www.w3.org/2000/svg";
  const make = (name, attrs = {}, text = "") => {
    const el = document.createElementNS(ns, name);
    Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
    if (text) el.textContent = text;
    return el;
  };
  const number = (n) => new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 }).format(n);
  const stops = ["#FFF7F5", "#F5CDD0", "#E79AA6", "#CF6479", "#AB3C56", "#7C2038"];
  const color = (v) => {
    const z = Math.max(0, Math.min(1, v / 25)) * (stops.length - 1);
    const i = Math.min(stops.length - 2, Math.floor(z));
    const rgb = (s) => [1, 3, 5].map((p) => parseInt(s.slice(p, p + 2), 16));
    const a = rgb(stops[i]), b = rgb(stops[i + 1]);
    return `rgb(${a.map((x, j) => Math.round(x + (b[j] - x) * (z - i))).join(",")})`;
  };
  fetch("data/state-youth-pooled-map.json?v=20261126")
    .then((r) => { if (!r.ok) throw new Error("Pooled state data unavailable"); return r.json(); })
    .then((data) => {
      let period = data.metadata.default_period;
      const svg = root.querySelector("svg");
      const info = root.querySelector(".state-map-info");
      const title = root.querySelector(".state-map-title");
      const stats = root.querySelector(".state-map-stats");
      const legend = root.querySelector(".state-map-legend");
      const small = ["VT", "NH", "MA", "RI", "CT", "NJ", "DE", "MD", "DC"];
      const ordered = data.states.filter((s) => small.includes(s.abbr)).sort((a, b) => a.label[1] - b.label[1]);
      const leaderY = new Map(ordered.map((s, i) => [s.abbr, 82 + i * 27]));
      function render() {
        const selected = data.periods.find((p) => p.id === period);
        const rates = new Map(data.rates.filter((r) => r.period === period).map((r) => [r.GESTFIPS, r]));
        const national = data.national.find((r) => r.period === period);
        root.querySelectorAll("button[data-period]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.period === period)));
        title.textContent = `Full-time employment in THAIE Q5 · ${selected.label}`;
        const sample = [...rates.values()].map((r) => r.numerator_records);
        stats.textContent = `U.S. rate ${national.estimate_pct.toFixed(2)}% of all residents aged 22–25 · ${number(national.average_monthly_numerator)} Q5 full-time workers, average month · ${selected.observed_months} observed months · All 50 states and DC · Smallest state/DC sample ${number(Math.min(...sample))} contributing person-month records`;
        info.textContent = `Among Q5 employed youth, ${national.FT_share_pct.toFixed(2)}% work full time nationally. This differs from the ${national.estimate_pct.toFixed(2)}% population rate. Hover, tap, or focus a state for its estimate and working uncertainty.`;
        svg.replaceChildren();
        svg.setAttribute("aria-label", `${title.textContent}. Denominator is all civilian noninstitutional state residents aged 22–25. Period averages, not causal effects.`);
        data.states.forEach((state) => {
          const r = rates.get(state.fips);
          if (!r || !Number.isFinite(r.estimate_pct)) throw new Error(`Missing estimate for ${state.name}`);
          const interval = r.CI_status === "working_household_cluster"
            ? `Working household-cluster 95% interval ${r.working_CI_low_pct.toFixed(2)}% to ${r.working_CI_high_pct.toFixed(2)}%; not full CPS survey-design or causal inference.`
            : "Working interval withheld because of sparse or degenerate support.";
          const summary = `${state.name}. ${selected.label}. Rate ${r.estimate_pct.toFixed(2)}%. ${interval} Estimated Q5 full-time workers ${number(r.average_monthly_numerator)} and all residents aged 22–25 ${number(r.average_monthly_denominator)}, average month. Sample ${number(r.numerator_records)} records with a positive Q5 full-time contribution across ${r.observed_months} observed months; these are not distinct people or the population worker count. Pre-2020 band contributions use a probabilistic occupation bridge. Full-time share among Q5 employed youth ${r.FT_share_pct.toFixed(2)}%.`;
          const path = make("path", { d: state.path, fill: color(r.estimate_pct), stroke: "white", "stroke-width": 1.1, "fill-rule": "evenodd", tabindex: 0, role: "button", "aria-label": summary, "data-state": state.abbr, "data-rate": r.estimate_pct, "data-period": period });
          path.append(make("title", {}, summary));
          ["mouseenter", "focus", "click"].forEach((event) => path.addEventListener(event, () => { info.textContent = summary; }));
          path.addEventListener("keydown", (event) => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); info.textContent = summary; } });
          svg.append(path);
          const [x, y] = state.label;
          if (leaderY.has(state.abbr)) {
            const ly = leaderY.get(state.abbr);
            svg.append(make("path", { d: `M${x},${y}L916,${ly}L927,${ly}`, fill: "none", stroke: "#A9ADB1", "stroke-width": .8, "pointer-events": "none" }));
            svg.append(make("text", { x: 932, y: ly + 4, class: "state-map-abbr", "pointer-events": "none" }, state.abbr));
          } else {
            svg.append(make("text", { x, y: y + 4, "text-anchor": "middle", class: "state-map-abbr", "pointer-events": "none" }, state.abbr));
          }
        });
        svg.append(make("text", { x: 45, y: 664, class: "state-map-inset" }, "Alaska and Hawaii shown as insets; scales differ."));
        legend.replaceChildren();
        const ramp = document.createElement("span"); ramp.className = "state-map-ramp";
        ramp.style.background = `linear-gradient(to right,${stops.join(",")})`;
        const text = document.createElement("span");
        text.textContent = "Fixed scale 0%–25% · darker red = higher Q5 full-time employment / same-age population · color is not significance";
        legend.append(ramp, text);
      }
      root.querySelectorAll("button[data-period]").forEach((b) => b.addEventListener("click", () => { period = b.dataset.period; render(); }));
      root.querySelector(".state-map-save").addEventListener("click", () => {
        const selected = data.periods.find((p) => p.id === period);
        const clone = svg.cloneNode(true);
        clone.setAttribute("xmlns", ns);
        clone.setAttribute("viewBox", "0 0 1000 795");
        const style = make("style", {}, ".state-map-abbr{font:600 14px Arial,sans-serif;fill:#39434b;paint-order:stroke;stroke:#fff;stroke-width:2px}.state-map-inset{font:13px Arial,sans-serif;fill:#66727b}");
        clone.prepend(make("rect", { width: 1000, height: 795, fill: "white" }), style);
        clone.append(make("text", { x: 40, y: 700, fill: "#39434b", "font-size": 15 }, title.textContent));
        clone.append(make("text", { x: 40, y: 725, fill: "#66727b", "font-size": 12 }, `${selected.observed_months} observed months; Q5 full-time / all civilian noninstitutional residents aged 22–25.`));
        clone.append(make("text", { x: 40, y: 748, fill: "#66727b", "font-size": 12 }, "Fixed 0%–25% red scale; period averages, not causal effects. October 2025 is not filled."));
        clone.append(make("text", { x: 40, y: 771, fill: "#66727b", "font-size": 12 }, "Working household-cluster intervals and sample support are available in the accompanying table."));
        const url = URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(clone)], { type: "image/svg+xml" }));
        const a = document.createElement("a"); a.href = url; a.download = `CPS_THAIE_Q5_youth_state_${period}.svg`; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
      });
      render();
    })
    .catch((error) => { root.querySelector(".state-map-info").textContent = `${error.message}. Please use the downloadable data table.`; root.querySelector(".state-map-stats").textContent = "Interactive map unavailable; static map and data remain available below."; });
})();
