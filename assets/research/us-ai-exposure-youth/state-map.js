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
  const signed = (n) => `${n >= 0 ? "+" : "−"}${Math.abs(n).toFixed(2)}`;
  const mix = (a, b, t) => {
    const rgb = (s) => [1, 3, 5].map((i) => parseInt(s.slice(i, i + 2), 16));
    const x = rgb(a), y = rgb(b);
    return `rgb(${x.map((v, i) => Math.round(v + (y[i] - v) * Math.max(0, Math.min(1, t)))).join(",")})`;
  };
  const rateStops = ["#FFF7F5", "#F5CDD0", "#E79AA6", "#CF6479", "#AB3C56", "#7C2038"];
  const rateColor = (t) => {
    const z = Math.max(0, Math.min(1, t)) * (rateStops.length - 1);
    const i = Math.min(rateStops.length - 2, Math.floor(z));
    return mix(rateStops[i], rateStops[i + 1], z - i);
  };
  fetch("data/state-youth-map.json?v=20261126")
    .then((r) => { if (!r.ok) throw new Error("Map data unavailable"); return r.json(); })
    .then((data) => {
      let year = 2026, mode = "rate", coverage = "all";
      const svg = root.querySelector("svg");
      const info = root.querySelector(".state-map-info");
      const label = root.querySelector(".state-map-title");
      const stats = root.querySelector(".state-map-stats");
      const legend = root.querySelector(".state-map-legend");
      const valid = data.rates.filter((r) => Number.isFinite(r.rate_pct));
      const maxRate = Math.ceil(Math.max(...valid.map((r) => r.rate_pct)) / 5) * 5;
      const maxChange = Math.ceil(Math.max(...data.rates.filter((r) => Number.isFinite(r.change_pp)).map((r) => Math.abs(r.change_pp))));
      const color = (v) => mode === "rate"
        ? rateColor(v / maxRate)
        : mix("#F4F2F0", v < 0 ? "#9B2946" : "#557974", Math.abs(v) / maxChange);
      const small = ["VT", "NH", "MA", "RI", "CT", "NJ", "DE", "MD", "DC"];
      const ordered = data.states.filter((s) => small.includes(s.abbr)).sort((a, b) => a.label[1] - b.label[1]);
      const leaderY = new Map(ordered.map((s, i) => [s.abbr, 82 + i * 27]));

      function render() {
        const rates = new Map(data.rates.filter((r) => r.year === year).map((r) => [r.GESTFIPS, r]));
        const nat = data.national.find((r) => r.year === year);
        const base = data.national.find((r) => r.year === 2022);
        const supported = mode === "rate" ? nat.supported_states : nat.supported_changes;
        root.querySelectorAll("[data-year]").forEach((b) => b.setAttribute("aria-pressed", String(Number(b.dataset.year) === year)));
        root.querySelectorAll("[data-mode]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.mode === mode)));
        root.querySelectorAll("[data-coverage]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.coverage === coverage)));
        label.textContent = mode === "rate"
          ? `Full-time employment in THAIE Q5 · ages 22–25 · ${year}`
          : `Change in Q5 full-time employment rate · 2022 to ${year}`;
        stats.textContent = `U.S. rate ${nat.rate_pct.toFixed(2)}% · ${signed(nat.rate_pct - base.rate_pct)} percentage points from 2022 · ${number(nat.Q5_FT_average)} estimated full-time Q5 workers, monthly average · ${coverage === "all" ? "All 50 states and DC shown" : `${supported} higher-support estimates colored`} · ${51 - supported} smaller-sample estimates marked †`;
        info.textContent = "Hover over a state, tap it, or use the keyboard to inspect its rate and sample support.";
        svg.replaceChildren();
        svg.setAttribute("aria-label", `${label.textContent}. January–September. Denominator is all state residents aged 22–25, not only employed people.`);
        const defs = make("defs");
        const pattern = make("pattern", { id: "state-map-missing", width: 7, height: 7, patternUnits: "userSpaceOnUse" });
        pattern.append(make("rect", { width: 7, height: 7, fill: "#ECEDEF" }), make("path", { d: "M-1,1L1,-1M0,7L7,0M6,8L8,6", stroke: "#C1C5CA", "stroke-width": 1 }));
        defs.append(pattern); svg.append(defs);
        data.states.forEach((state) => {
          const r = rates.get(state.fips);
          const higherSupport = mode === "rate" ? r.supported : r.change_supported;
          const value = mode === "rate" ? r.rate_pct : r.change_pp;
          const ok = Number.isFinite(value) && (coverage === "all" || higherSupport);
          const changeText = `${signed(r.change_pp)} percentage points${r.change_supported ? "" : " (smaller-sample endpoint; interpret cautiously)"}`;
          const summary = `${state.name}. Estimated full-time Q5 workers ${number(r.Q5_FT_average)} people, monthly average. ${year} rate ${r.rate_pct.toFixed(2)}%; change since 2022 ${changeText}. Estimated population aged 22–25 ${number(r.population_average)} people. Survey sample ${r.nQ5_FT} Q5 full-time person-month records across nine months, NOT ${r.nQ5_FT} workers in the state. ${higherSupport ? "Passes the research sample-size flag rule; precision is not guaranteed." : "Smaller sample: estimate shown with a caution flag, not statistically validated."}`;
          const path = make("path", { d: state.path, fill: ok ? color(value) : "url(#state-map-missing)", stroke: higherSupport ? "white" : "#606974", "stroke-width": higherSupport ? 1.1 : 1.3, "stroke-dasharray": higherSupport ? "none" : "4 2", "fill-rule": "evenodd", tabindex: 0, role: "button", "aria-label": summary, "data-state": state.abbr, "data-low-sample": String(!higherSupport) });
          path.append(make("title", {}, summary));
          ["mouseenter", "focus", "click"].forEach((event) => path.addEventListener(event, () => { info.textContent = summary; }));
          path.addEventListener("keydown", (event) => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); info.textContent = summary; } });
          svg.append(path);
          const [x, y] = state.label;
          if (leaderY.has(state.abbr)) {
            const ly = leaderY.get(state.abbr);
            svg.append(make("path", { d: `M${x},${y}L916,${ly}L927,${ly}`, fill: "none", stroke: "#A9ADB1", "stroke-width": 0.8, "pointer-events": "none" }));
            svg.append(make("text", { x: 932, y: ly + 4, class: "state-map-abbr", "pointer-events": "none" }, state.abbr + (higherSupport ? "" : "†")));
          } else {
            svg.append(make("text", { x, y: y + 4, "text-anchor": "middle", class: "state-map-abbr", "pointer-events": "none" }, state.abbr + (higherSupport ? "" : "†")));
          }
        });
        svg.append(make("text", { x: 45, y: 664, class: "state-map-inset" }, "Alaska and Hawaii shown as insets; scales differ."));
        const gradient = mode === "rate"
          ? `linear-gradient(to right,${rateStops.join(",")})`
          : "linear-gradient(to right,#9B2946,#F4F2F0,#557974)";
        legend.replaceChildren();
        const ramp = document.createElement("span"); ramp.className = "state-map-ramp"; ramp.style.background = gradient;
        const text = document.createElement("span");
        text.textContent = mode === "rate" ? `0% to ${maxRate}% · darker red = higher employment rate` : `−${maxChange} to +${maxChange} percentage points · red = decline, green-gray = increase`;
        legend.append(ramp, text);
        const missing = document.createElement("span"); missing.textContent = coverage === "all" ? "† / dashed border = smaller sample; estimate shown" : "▧ Smaller-sample estimates hidden by optional filter"; legend.append(missing);
      }
      root.querySelectorAll("[data-year]").forEach((b) => b.addEventListener("click", () => { year = Number(b.dataset.year); render(); }));
      root.querySelectorAll("[data-mode]").forEach((b) => b.addEventListener("click", () => { mode = b.dataset.mode; render(); }));
      root.querySelectorAll("[data-coverage]").forEach((b) => b.addEventListener("click", () => { coverage = b.dataset.coverage; render(); }));
      root.querySelector(".state-map-save").addEventListener("click", () => {
        const clone = svg.cloneNode(true);
        clone.setAttribute("xmlns", ns);
        clone.setAttribute("viewBox", "0 0 1000 770");
        const style = make("style", {}, ".state-map-abbr{font:600 14px Arial,sans-serif;fill:#39434b;paint-order:stroke;stroke:#fff;stroke-width:2px}.state-map-inset{font:13px Arial,sans-serif;fill:#66727b}");
        clone.prepend(make("rect", { x: 0, y: 0, width: 1000, height: 770, fill: "white" }), style);
        clone.append(make("text", { x: 40, y: 700, fill: "#39434b", "font-size": 15 }, label.textContent));
        clone.append(make("text", { x: 40, y: 725, fill: "#66727b", "font-size": 12 }, "January–September; Q5 full-time employment / all residents aged 22–25. † / dashed border: smaller sample."));
        clone.append(make("text", { x: 40, y: 748, fill: "#66727b", "font-size": 12 }, legend.textContent));
        const url = URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(clone)], { type: "image/svg+xml" }));
        const a = document.createElement("a"); a.href = url; a.download = `CPS_THAIE_Q5_youth_state_${mode}_${year}.svg`; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
      });
      render();
    })
    .catch((error) => { root.querySelector(".state-map-info").textContent = `${error.message}. Please use the downloadable data table.`; });
})();
