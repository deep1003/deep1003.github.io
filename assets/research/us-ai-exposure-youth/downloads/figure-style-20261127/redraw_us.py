"""Original plotting implementation informed by Chen Liu's figures4papers design examples.
Reference commit daa2833f03878454cb9b6ad3f9ecb68acad36ade (CC BY-NC 4.0).
Empirical estimates retain their existing source files and interpretation.
"""

from pathlib import Path
import hashlib, json
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = Path(__file__).resolve().parents[2]
S = R / "outputs/US_Figure_Style_20261127"
(S / "figures").mkdir(parents=True, exist_ok=True)
D = S / "downloads/figure-style-20261127"
D.mkdir(parents=True, exist_ok=True)
RED = "#C64F5A"
INK = "#28343D"
GRAY = "#A8AFB5"
plt.rcParams.update(
    {
        "font.family": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 13,
        "axes.labelsize": 13,
        "axes.linewidth": 1.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "savefig.facecolor": "white",
    }
)
manifest = []


def draw(name, title, subtitle, labels, point, lo, hi, xlabel, source):
    assert np.isfinite(np.r_[point, lo, hi]).all()
    assert np.all(lo <= point) and np.all(point <= hi)
    fig = plt.figure(figsize=(12.6, 5.8))
    ax = fig.add_axes([0.29, 0.22, 0.45, 0.58])
    text = fig.add_axes([0.77, 0.22, 0.21, 0.58])
    text.set_axis_off()
    y = np.arange(len(point))
    ax.set_ylim(len(y) - 0.55, -0.55)
    text.set_ylim(ax.get_ylim())
    ax.axvline(0, color=GRAY, linewidth=1, linestyle=(0, (3, 3)), zorder=0)
    ax.errorbar(
        point,
        y,
        xerr=np.vstack([point - lo, hi - point]),
        fmt="s",
        markersize=8,
        color=RED,
        markeredgecolor="white",
        markeredgewidth=1.1,
        elinewidth=2.2,
        capsize=4,
        capthick=1.5,
        zorder=3,
    )
    ax.set_yticks(y, labels)
    ax.tick_params(axis="y", length=0, pad=12)
    ax.tick_params(axis="x", length=5, color=INK)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(INK)
    ax.set_xlabel(xlabel, labelpad=12)
    ax.set_xlim(min(lo.min(), 0) - 0.6, max(hi.max(), 0) + 0.6)
    for i, (v, l, h) in enumerate(zip(point, lo, hi)):
        text.text(
            0, i, f"{v:+.2f}  [{l:+.2f}, {h:+.2f}]", va="center", fontsize=12, color=INK
        )
    text.text(
        0,
        1.045,
        "Estimate [diagnostic range]",
        transform=text.transAxes,
        fontsize=11,
        fontweight="bold",
        color=INK,
    )
    fig.text(0.035, 0.93, title, fontsize=18, fontweight="bold", color=INK)
    fig.text(0.035, 0.875, subtitle, fontsize=12, color="#66717A")
    fig.text(
        0.035,
        0.075,
        "Central 95% state-resampling ranges are geographic diagnostics, not CPS sampling confidence intervals.",
        fontsize=10,
        color="#66717A",
    )
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    from matplotlib.text import Text

    for obj in fig.findobj(Text):
        if obj.get_visible() and obj.get_text():
            box = obj.get_window_extent(renderer)
            assert box.x0 >= -1 and box.x1 <= fig.bbox.width + 1, obj.get_text()
            assert box.y0 >= -1 and box.y1 <= fig.bbox.height + 1, obj.get_text()
    for ext in ["png", "pdf", "svg"]:
        path = S / "figures" / f"{name}.{ext}"
        fig.savefig(path, dpi=300)
        assert path.stat().st_size > 1000
    plt.close(fig)
    manifest.append(
        dict(
            figure=name,
            source=str(source.relative_to(R)),
            source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            values=point.tolist(),
            low=lo.tolist(),
            high=hi.tolist(),
        )
    )


p = R / "outputs/US_Residual_Audit_20261126/STOCK_SENSITIVITIES.csv"
d = pd.read_csv(p)
draw(
    "STOCK_RESIDUAL_SENSITIVITY",
    "Relative full-time employment under alternative specifications",
    "Recorded ages 22–25 · THAIE Q5 relative to Q1–Q4 · own CPS reconstruction",
    [
        "Original long window",
        "Equal rotation-group mix",
        "Unambiguous code links",
        "2020-start reference",
        "Matched 22-month windows",
    ],
    d.relative_percent.to_numpy(),
    d.ci_low.to_numpy(),
    d.ci_high.to_numpy(),
    "Relative headcount change (%)",
    p,
)
p = R / "outputs/US_Stock_Flow_20261126/SEASON_BALANCED_FLOW_INTENSITIES.csv"
d = pd.read_csv(p)
names = [
    "Nonemployment entry",
    "Nonemployment exit",
    "Full-/part-time balance",
    "Recorded occupation balance",
    "Age-boundary balance",
]
d = (
    d[d.period.eq("DID_calendar") & d.component.isin(names)]
    .set_index("component")
    .loc[names]
)
draw(
    "FLOW_CHANNEL_COMPARISON",
    "Descriptive worker-transition contrasts",
    "Recorded ages 22–25 · equal calendar-month weights · per 100 origin full-time workers",
    [
        "Nonemployment entry",
        "Nonemployment exit",
        "Full-/part-time balance",
        "Recorded occupation balance",
        "Recorded age-bin balance",
    ],
    d.relative_change_pp.to_numpy(),
    d.working_ci_low.to_numpy(),
    d.working_ci_high.to_numpy(),
    "Q5 minus Q1–Q4 post–pre change (pp)",
    p,
)
(D / "STYLE_AND_DATA_CHECKS.json").write_text(
    json.dumps(
        dict(
            reference="https://github.com/ChenLiu-1996/figures4papers",
            commit="daa2833f03878454cb9b6ad3f9ecb68acad36ade",
            license="CC BY-NC 4.0",
            implementation="Original code using design references; existing data and numerical ranges unchanged",
            figures=manifest,
            figures_emitted_during_smokes=0,
        ),
        indent=2,
    )
)
print(
    "Two figures exported as PNG/PDF/editable SVG. Source values and ranges retained; no images emitted."
)
