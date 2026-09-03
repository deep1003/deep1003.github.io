from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd
from adjustText import adjust_text

ROOT = Path("/Users/deep1003/data4/topic_space")
PROJECT = ROOT / "manuscript_update_20260903"
DATA = PROJECT / "data"
TABLES = PROJECT / "tables"
OUT = PROJECT / "figures_stpi_oecd"
DERIVED = PROJECT / "data_stpi_oecd"
OUT.mkdir(parents=True, exist_ok=True)
DERIVED.mkdir(parents=True, exist_ok=True)

# Canonical topic labels and ordering used by the 3 August final STPI report.
# The 20 EDU/LABOR branch anchors in the extended 495-row working file are
# intentionally excluded from the 475-topic core policy reference space.
STPI_REPORT_ROOT = Path(
    "/Users/deep1003/data3/kim_jongrip_ai_stpi_full_datasets_share_20260630"
)
TOPIC_MASTER = (
    STPI_REPORT_ROOT
    / "06_interactive_topic_space/github_pages_data/l0_l1_l2_l3_dictionary_for_appendix.csv"
)
UMAP_MASTER = (
    STPI_REPORT_ROOT
    / "05_analysis_statistics_and_figures/25_m3_cross_domain_gap_v3/02_data_outputs/"
      "m3_reference_l3_common_2d_coordinates_v3.csv"
)

# OECD report-chart palette matched to the supplied reference figures.
MIDNIGHT = "#08306B"
OECD_BLUE = "#0B3B75"
OCEAN = "#0877B9"
LIGHT_BLUE = "#7EA6D6"
CYAN = "#00A6C8"
ORANGE = "#F05A00"
PALE_BLUE = "#D8E6F3"
POLICY_RED = "#C95662"
SCIENCE_BLUE = "#2F6FAD"
TECH_GREEN = "#25864B"
GREEN = TECH_GREEN
RED = "#C9474D"
GREY = "#8C8C8C"
LIGHT_GREY = "#CFCFCF"
PLOT_GREY = "#EFEFEF"
GRID = "#FFFFFF"
WHITE = "#FFFFFF"

NAME_TO_ISO = {
    "United States of America":"US", "China":"CN", "Republic of Korea":"KR",
    "United Kingdom":"GB", "Australia":"AU", "Brazil":"BR", "Germany":"DE",
    "Saudi Arabia":"SA", "Canada":"CA", "France":"FR", "Singapore":"SG",
    "Argentina":"AR", "India":"IN", "Japan":"JP", "Italy":"IT", "Vietnam":"VN",
    "Philippines":"PH", "Netherlands":"NL", "Turkiye":"TR", "Thailand":"TH",
    "European Union":"EU", "Chinese Taipei":"TW",
}
DISPLAY = {"US":"United States", "CN":"China", "KR":"Korea", "JP":"Japan"}
COUNTRY_COLOURS = {"US":MIDNIGHT, "CN":POLICY_RED, "KR":SCIENCE_BLUE, "JP":CYAN, "OECD observed":ORANGE}

OECD = {"US","KR","GB","AU","DE","CA","FR","JP","IT","NL","TR"}
EU_MEMBERS = {"DE","FR","IT","NL"}
GROUPS = {"OECD observed":"OECD", "EU members observed":"EU"}
MEMBERS = {"OECD observed": OECD, "EU members observed": EU_MEMBERS}
HIGHLIGHTS = ["OECD observed", "EU members observed", "US", "CN", "JP", "KR"]
COLOURS = {
    "OECD observed": ORANGE, "EU members observed": LIGHT_BLUE,
    "US": MIDNIGHT, "CN": RED, "JP": OCEAN, "KR": OECD_BLUE,
}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def configure() -> None:
    installed = {f.name for f in font_manager.fontManager.ttflist}
    font = next((x for x in ["Arial", "Noto Sans", "Helvetica", "DejaVu Sans"] if x in installed), "DejaVu Sans")
    plt.rcParams.update({
        "font.family": font, "font.size": 12, "axes.titlesize": 19,
        "axes.titleweight": "bold", "axes.titlecolor": MIDNIGHT,
        "axes.labelsize": 12, "text.color": "#111111", "axes.edgecolor": "#333333",
        "figure.facecolor": WHITE, "axes.facecolor": WHITE, "savefig.facecolor": WHITE,
        "pdf.fonttype": 42, "svg.fonttype": "none",
    })


def clean(ax, grid="y"):
    ax.set_facecolor(PLOT_GREY)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis=grid, color=GRID, linewidth=1.0)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def title(fig, number: str, main: str, subtitle: str):
    fig.text(0.045, 0.955, f"Figure {number}. {main}", ha="left", va="top",
             fontsize=20, fontweight="bold", color=MIDNIGHT)
    fig.text(0.045, 0.905, subtitle, ha="left", va="top", fontsize=12.5, color="#111111")


def footer(fig, note: str):
    fig.text(0.045, 0.052, f"Notes: {note}", ha="left", va="bottom", fontsize=8.5)
    fig.text(0.045, 0.024,
             "Source: Digital Policy Alert, PATSTAT and Web of Science; author's calculations. Data and code: https://deep1003.github.io/assets/research/stpi-regulatory-attention-20260903/",
             ha="left", va="bottom", fontsize=8.5)


def save(fig, stem):
    for ext, kw in [("png", {"dpi": 360}), ("pdf", {}), ("svg", {})]:
        fig.savefig(OUT / f"{stem}.{ext}", bbox_inches="tight", pad_inches=0.12, **kw)
    plt.close(fig)


def report_legend(ax, **kwargs):
    legend = ax.legend(frameon=True, facecolor=PLOT_GREY, edgecolor=PLOT_GREY,
                       framealpha=1, borderpad=.8, **kwargs)
    return legend


def initial_upper(value: object) -> str:
    text = str(value).strip()
    return text[:1].upper() + text[1:] if text else text


def load_policy_master() -> pd.DataFrame:
    master = pd.read_csv(TOPIC_MASTER, low_memory=False)
    policy = master.loc[
        master["L3_id"].astype(str).str.startswith("POLICY-REF-"),
        ["L3_id", "L0", "L1", "L2", "L3", "Korean_label", "Definition"],
    ].copy()
    if len(policy) != 475 or policy["L2"].nunique() != 23 or policy["L3_id"].duplicated().any():
        raise ValueError("The final-report policy master must contain 475 unique L3 topics in 23 L2 groups.")
    policy.insert(0, "policy_order", np.arange(1, len(policy) + 1))
    policy.to_csv(DERIVED / "policy_l2_l3_master_final_report_order.csv", index=False)
    return policy


def align_panel_to_policy_master(panel: pd.DataFrame, policy: pd.DataFrame) -> pd.DataFrame:
    aligned = panel[panel["l3_id"].isin(policy["L3_id"])].copy()
    names = policy.set_index("L3_id")[["policy_order", "L2", "L3"]]
    aligned = aligned.drop(columns=[c for c in ["l2_label", "l3_label"] if c in aligned])
    aligned = aligned.join(names, on="l3_id")
    aligned = aligned.rename(columns={"L2": "l2_label", "L3": "l3_label"})
    aligned["l3_label"] = aligned["l3_label"].map(initial_upper)
    aligned = aligned.sort_values(["policy_order", "jurisdiction", "year"], kind="stable")
    return aligned


def period_profiles(panel: pd.DataFrame):
    panel = panel.copy()
    panel["iso"] = panel.jurisdiction.map(NAME_TO_ISO)
    out = {}
    for label, lo, hi in [("2020-21", 2020, 2021), ("2025-26", 2025, 2026)]:
        x = panel[panel.year.between(lo, hi)].groupby(["iso", "l2_label"], as_index=False).activity_mass.sum()
        x["share"] = x.activity_mass / x.groupby("iso").activity_mass.transform("sum")
        out[label] = x
    return out


def group_profile(frame: pd.DataFrame, members: set[str]) -> pd.Series:
    wide = frame.pivot(index="iso", columns="l2_label", values="share").fillna(0)
    fixed = sorted(members & set(wide.index))
    return wide.loc[fixed].mean(axis=0)


def make_period_change(panel: pd.DataFrame):
    pp = period_profiles(panel)
    all_iso = sorted(set(pp["2020-21"].iso) & set(pp["2025-26"].iso))
    early = pp["2020-21"].pivot(index="iso", columns="l2_label", values="share").fillna(0)
    late = pp["2025-26"].pivot(index="iso", columns="l2_label", values="share").fillna(0)
    topics = early.columns.union(late.columns)
    delta_country = 100 * (late.reindex(index=all_iso, columns=topics, fill_value=0) - early.reindex(index=all_iso, columns=topics, fill_value=0))
    series = {}
    coverage = []
    for group, members in MEMBERS.items():
        fixed = sorted(members & set(all_iso))
        series[group] = delta_country.loc[fixed].mean(axis=0)
        coverage.append({"series": group, "n_countries": len(fixed), "members": "|".join(fixed)})
    for iso in ["US", "CN", "JP", "KR"]:
        series[iso] = delta_country.loc[iso]
    highlights = pd.DataFrame(series).T
    importance = highlights.abs().mean(axis=0)
    keep = importance.nlargest(12).sort_values().index
    rows = []
    for topic in keep:
        vals = delta_country[topic]
        rows.append({"l2_label":topic, "p10":vals.quantile(.1), "p90":vals.quantile(.9),
                     "min_country":vals.idxmin(), "min_value":vals.min(),
                     "max_country":vals.idxmax(), "max_value":vals.max(), **{k: highlights.loc[k, topic] for k in HIGHLIGHTS}})
    chart = pd.DataFrame(rows)
    chart.to_csv(DERIVED / "period_change_l2_2020-21_vs_2025-26.csv", index=False)
    pd.DataFrame(coverage).to_csv(DERIVED / "group_coverage.csv", index=False)

    fig, ax = plt.subplots(figsize=(13.333, 7.5))
    fig.subplots_adjust(left=.30, right=.95, top=.82, bottom=.16)
    y = np.arange(len(chart))
    ax.hlines(y, chart.p10, chart.p90, color=LIGHT_GREY, linewidth=6, zorder=1, label="Country p10-p90")
    offsets = np.linspace(-.24, .24, len(HIGHLIGHTS))
    markers = {"OECD observed":"s", "EU members observed":"D", "US":"o", "CN":"o", "JP":"o", "KR":"o"}
    for off, key in zip(offsets, HIGHLIGHTS):
        ax.scatter(chart[key], y+off, s=48 if key in GROUPS else 36, marker=markers[key],
                   color=COLOURS[key], edgecolor=WHITE, linewidth=.5, label=DISPLAY.get(key, key), zorder=3)
    ax.axvline(0, color="#333333", linewidth=1)
    ax.set_yticks(y, chart.l2_label)
    ax.set_xlabel("Change in share of regulatory-policy activity (percentage points)")
    clean(ax, "x")
    report_legend(ax, ncol=4, fontsize=9.3, loc="lower right")
    title(fig, "2", "Policy attention shifted unevenly after the generative-AI turn",
          "Change in L2 topic shares, 2020-21 to 2025-26")
    footer(fig, "Grey bars show the 10th-90th percentile range across countries observed in both periods. Group values are unweighted means of fixed observed members. 2026 is partial through 3 September.")
    save(fig, "F02_policy_share_change_2020-21_2025-26_OECD")


def make_policy_trends():
    raw = pd.read_csv(ROOT / "event_attention_rebuild/outputs/ai_events_country_panel_raw_20260903.csv", low_memory=False)
    raw = raw[raw.year.between(2020, 2026)].copy()
    capped = raw.groupby(["intervention_id", "jurisdiction", "year"], as_index=False).scope_weight.first()
    capped["iso"] = capped.jurisdiction.map(NAME_TO_ISO)
    annual = capped.groupby(["iso", "year"], as_index=False).scope_weight.sum().rename(columns={"scope_weight":"effective_activity"})
    grid = pd.MultiIndex.from_product([sorted(annual.iso.dropna().unique()), range(2020, 2027)], names=["iso","year"]).to_frame(index=False)
    annual = grid.merge(annual, how="left").fillna({"effective_activity":0})
    # Annualise only the current partial year for the trend display.
    annual["display_activity"] = annual.effective_activity
    annual.loc[annual.year.eq(2026), "display_activity"] *= 365/246
    group_rows=[]
    for group,members in MEMBERS.items():
        fixed=sorted(members & set(annual.iso))
        q=annual[annual.iso.isin(fixed)].groupby("year",as_index=False).display_activity.mean()
        q["series"]=group; q["n_countries"]=len(fixed); group_rows.append(q)
    groups=pd.concat(group_rows,ignore_index=True)
    annual.to_csv(DERIVED/"annual_policy_activity_by_country.csv",index=False)
    groups.to_csv(DERIVED/"annual_policy_activity_group_means.csv",index=False)

    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(13.333,7.5),sharey=False)
    fig.subplots_adjust(left=.07,right=.95,top=.81,bottom=.16,wspace=.23)
    for iso,q in annual.groupby("iso"):
        ax1.plot(q.year,q.display_activity,color="#B7B7B7",lw=1,alpha=.62)
    for iso in ["US","CN","JP","KR"]:
        q=annual[annual.iso.eq(iso)]
        ax1.plot(q.year,q.display_activity,color=COLOURS[iso],lw=2.5)
        ax1.text(2026.08,q.display_activity.iloc[-1],DISPLAY[iso],color=COLOURS[iso],va="center",fontsize=10,fontweight="bold")
    for group,q in groups.groupby("series"):
        ax2.plot(q.year,q.display_activity,color=COLOURS[group],lw=2.7,label=group)
        label_offset = {"OECD observed":1.2, "EU members observed":0.0}[group]
        ax2.text(2026.08,q.display_activity.iloc[-1]+label_offset,group.replace(" observed",""),color=COLOURS[group],va="center",fontsize=10,fontweight="bold")
    for ax,panel_title in zip([ax1,ax2],["A. Selected countries","B. Observed group means"]):
        ax.set_title(panel_title,loc="left",fontsize=14,color="#111111")
        ax.set_xlim(2020,2026.8); ax.set_xticks(range(2020,2027)); ax.set_ylabel("Effective intervention-year activity")
        clean(ax,"y")
    title(fig,"3","Regulatory-policy activity accelerated after 2022","Annual event-based activity, 2020-26")
    footer(fig,"Each intervention counts at most once per jurisdiction-year and is scope-weighted. Grey lines are other observed jurisdictions. 2026 is annualised from activity observed through 3 September and is not a forecast.")
    save(fig,"F03_policy_activity_trends_groups_OECD")


def make_stp_volume_trends():
    docs=pd.read_csv(ROOT/"relatedness/nb_out/tables/T47_documents_by_year.csv")
    raw=pd.read_csv(ROOT/"event_attention_rebuild/outputs/ai_events_country_panel_raw_20260903.csv",low_memory=False)
    pol=raw[raw.year.between(2020,2026)].groupby(["intervention_id","year"]).size().reset_index().groupby("year").size().rename("policy_events").reset_index()
    d=docs.merge(pol,on="year",how="left").fillna({"policy_events":0})
    d=d[d.year.between(2020,2024)].copy()
    for col in ["papers","patents","policy_events"]: d[col+"_index"]=100*d[col]/d.loc[d.year.eq(2020),col].iloc[0]
    d.to_csv(DERIVED/"stp_document_volume_index_2020-2024.csv",index=False)
    fig,ax=plt.subplots(figsize=(13.333,7.5));fig.subplots_adjust(left=.09,right=.92,top=.80,bottom=.17)
    specs=[("papers_index","Science publications",SCIENCE_BLUE),("patents_index","Technology patents",TECH_GREEN),("policy_events_index","Regulatory-policy events",POLICY_RED)]
    for col,label,colour in specs:
        ax.plot(d.year,d[col],marker="o",ms=6,lw=3,color=colour,label=label)
        ax.text(d.year.iloc[-1]+.08,d[col].iloc[-1],label,color=colour,va="center",fontweight="bold")
    ax.axvspan(2022, 2024.9, color="#D8D8D8", alpha=.45, zorder=0)
    ax.text(2023.45, 1610, "Patent counts increasingly incomplete", ha="center", va="top", fontsize=10, color=GREY)
    ax.axhline(100,color=GREY,lw=.8,ls="--");ax.set_xlim(2020,2024.9);ax.set_xticks(range(2020,2025));ax.set_ylabel("Index (2020 = 100)")
    clean(ax,"y")
    title(fig,"4","Observed STP document volumes diverged after 2020","Science, technology and policy source records, 2020-24")
    footer(fig,"Series measure source-document volume, not capability quality or causal influence. Patent observations are increasingly right-truncated in recent years and must not be interpreted as a decline in technology capability.")
    save(fig,"F04_stp_volume_trends_OECD")


def make_semantic_evolution(panel: pd.DataFrame):
    rel=ROOT/"relatedness/nb_out"
    ds=pd.read_csv(rel/"tables/dict_science.csv"); dt=pd.read_csv(rel/"tables/dict_technology.csv")
    umap=pd.read_csv(UMAP_MASTER)
    hierarchy=pd.read_csv(TOPIC_MASTER,low_memory=False)[["L3_id","L1","L2","L3"]]
    umap=(umap.drop(columns=["l3_final_l1","l3_final_l2","l3_label_draft"])
          .merge(hierarchy,left_on="domain_reference_id",right_on="L3_id",how="left",validate="one_to_one")
          .rename(columns={"L1":"l3_final_l1","L2":"l3_final_l2","L3":"l3_label_draft"}))
    umap["layer"]=np.select(
        [umap.l3_final_l1.eq("AI science and research"),
         umap.l3_final_l1.eq("AI technology and invention"),
         umap.l3_final_l1.eq("AI policy and governance")],
        ["Science","Technology","Policy"], default="Unknown")
    if (umap.layer == "Unknown").any() or len(umap) != 1938:
        raise ValueError("Unexpected final-report UMAP master structure.")
    hwre=re.compile(r"semiconductor|chip|chiplet|processor|\bgpu\b|\btpu\b|\bnpu\b|accelerat|memory|wafer|fabricat|packaging|circuit|fpga|asic|hardware|silicon|photonic|transistor|system[- ]on[- ]chip|interconnect|neuromorphic|analog comput|in-memory|graphics processing",re.I)
    umap["is_hardware"]=(
        umap.layer.eq("Technology")
        & (umap.l3_label_draft.astype(str).str.contains(hwre)
           | umap.l3_final_l2.astype(str).str.contains(hwre))
        & ~umap.l3_label_draft.astype(str).eq("Long short-term memory")
        & ~umap.l3_label_draft.astype(str).isin({"hardware-aware model optimization","Hardware-aware neural architecture search","AI-assisted chip design","GPU resource scheduling"})
    )
    coords=umap.rename(columns={"domain_reference_id":"topic_id","l3_label_draft":"label"})[
        ["layer","topic_id","label","l3_final_l2","x","y","is_hardware"]]
    coords.to_csv(DERIVED/"stpi_semantic_topic_coordinates.csv",index=False)
    cm=np.load(rel/"arrays/capability_mass.npz")
    periods=["2021-22","2023-24","2025-26"]
    trajectories=[]
    dictionaries={"Science":ds,"Technology":dt}
    arrays={"Science":cm["sci"].sum(axis=1),"Technology":cm["tec"].sum(axis=1)}
    for layer in ["Science","Technology","Policy"]:
        pts=coords[coords.layer.eq(layer)].copy()
        for k,period in enumerate(periods):
            if layer == "Policy":
                lo,hi=[(2021,2022),(2023,2024),(2025,2026)][k]
                mass=panel[panel.year.between(lo,hi)].groupby("l3_id").activity_mass.sum()
            else:
                d=dictionaries[layer]
                mass=pd.Series(arrays[layer][k],index=d.L3_id.astype(str)).groupby(level=0).sum()
            w=pts.topic_id.map(mass).fillna(0).to_numpy()
            den=w.sum()
            centroid=(w[:,None]*pts[["x","y"]].to_numpy()).sum(axis=0)/den
            trajectories.append({"layer":layer,"period":period,"x":centroid[0],"y":centroid[1]})
    traj=pd.DataFrame(trajectories);traj.to_csv(DERIVED/"stpi_semantic_centroid_trajectories.csv",index=False)
    fig,ax=plt.subplots(figsize=(13.333,7.5));fig.subplots_adjust(left=.07,right=.94,top=.81,bottom=.16)
    sci=coords[coords.layer.eq("Science")];tech=coords[coords.layer.eq("Technology")]
    pol=coords[coords.layer.eq("Policy")];soft=tech[~tech.is_hardware];hard=tech[tech.is_hardware]
    ax.scatter(sci.x,sci.y,s=22,color=SCIENCE_BLUE,alpha=.72,edgecolor="#174A78",linewidth=.32,label="Science")
    ax.scatter(soft.x,soft.y,s=22,color=TECH_GREEN,alpha=.70,edgecolor="#145C34",linewidth=.32,label="Technology")
    ax.scatter(hard.x,hard.y,s=42,color="#70A83B",alpha=.94,edgecolor="#315F1D",linewidth=.65,label="AI hardware")
    ax.scatter(pol.x,pol.y,s=24,color=POLICY_RED,alpha=.75,edgecolor="#8C3440",linewidth=.38,label="Policy")

    representative = {
        "Policy": [
            "AI, rights, and biometrics",
            "Risk-based AI regulation and oversight",
            "Responsible AI and compliance",
        ],
        "Science": [
            "Optimization, inference, and evaluation methods",
            "Cognitive science and philosophy of mind",
            "Machine learning methods and tasks",
        ],
        "Technology": [
            "Machine learning and model training techniques",
            "Computer vision and image understanding",
            "Language and summarization technologies",
            "AI hardware and accelerators",
        ],
    }
    short = {
        "AI, rights, and biometrics":"AI rights and biometrics",
        "Risk-based AI regulation and oversight":"Risk-based AI regulation",
        "Responsible AI and compliance":"Responsible AI and compliance",
        "Optimization, inference, and evaluation methods":"Optimisation and evaluation",
        "Cognitive science and philosophy of mind":"Cognitive science",
        "Machine learning methods and tasks":"Machine learning methods",
        "Machine learning and model training techniques":"Model training technologies",
        "Computer vision and image understanding":"Computer vision",
        "Language and summarization technologies":"Language technologies",
        "AI hardware and accelerators":"AI hardware and accelerators",
    }
    colour_by_layer={"Policy":POLICY_RED,"Science":SCIENCE_BLUE,"Technology":TECH_GREEN}
    texts=[]; label_rows=[]
    for layer,topics in representative.items():
        for topic in topics:
            q=coords[(coords.layer.eq(layer)) & (coords.l3_final_l2.eq(topic))]
            if q.empty: continue
            x,y=q[["x","y"]].median()
            label_rows.append({"layer":layer,"l2_label":topic,"x":x,"y":y,"n_l3":len(q)})
            texts.append(ax.text(x,y,short[topic],fontsize=8.6,fontweight="bold",
                                 color=colour_by_layer[layer],zorder=8,
                                 bbox=dict(boxstyle="round,pad=.24",facecolor=WHITE,
                                           edgecolor=colour_by_layer[layer],linewidth=.75,alpha=.92)))
    adjust_text(texts,ax=ax,expand=(1.12,1.22),force_text=(.35,.50),force_static=(.12,.18),
                arrowprops=dict(arrowstyle="-",color="#666666",lw=.55,alpha=.8))
    pd.DataFrame(label_rows).to_csv(DERIVED/"stpi_umap_representative_l2_labels.csv",index=False)
    ax.set_xlabel("UMAP dimension 1");ax.set_ylabel("UMAP dimension 2");clean(ax,"both")
    report_legend(ax,ncol=4,loc="lower right",fontsize=9.5)
    title(fig,"1","Science, technology and policy occupy distinct but connected semantic regions","Final-report UMAP reference space, 1,938 L3 topics")
    footer(fig,"Nodes use the UMAP coordinates frozen for the 3 August final STPI report (Policy 475; Science 874; Technology 589). Labels identify selected high-coverage L2 topic families. Two-dimensional proximity is descriptive and is not used for statistical inference.")
    save(fig,"F01_STPI_semantic_evolution_OECD")


def make_korea_gap_change(panel: pd.DataFrame):
    panel=panel.copy(); panel["iso"]=panel.jurisdiction.map(NAME_TO_ISO)
    rows=[]
    for period,lo,hi in [("2020-21",2020,2021),("2025-26",2025,2026)]:
        x=panel[panel.year.between(lo,hi)].pivot_table(index="iso",columns="l3_id",values="activity_mass",aggfunc="sum",fill_value=0)
        if "KR" not in x.index: continue
        share=x.div(x.sum(axis=1),axis=0); loo=x.drop(index="KR").sum(axis=0);loo/=loo.sum()
        g=100*(loo-share.loc["KR"])
        for t,v in g.items(): rows.append({"period":period,"l3_id":t,"gap_pp":v})
    gap=pd.DataFrame(rows)
    labels=panel[["l3_id","l3_label"]].drop_duplicates().set_index("l3_id").l3_label
    w=gap.pivot(index="l3_id",columns="period",values="gap_pp").dropna()
    w["change"]=w["2025-26"]-w["2020-21"]
    keep=pd.concat([w.change.nlargest(6),w.change.nsmallest(6)]).index
    chart=w.loc[keep].sort_values("change")
    chart["l3_label_master"]=labels.reindex(chart.index).map(initial_upper)
    chart["l3_label"]=chart["l3_label_master"]
    chart.to_csv(DERIVED/"korea_l3_gap_change_2020-21_vs_2025-26.csv")
    fig,ax=plt.subplots(figsize=(13.333,7.5));fig.subplots_adjust(left=.30,right=.93,top=.81,bottom=.16)
    y=np.arange(len(chart),dtype=float)
    for yi,x0,x1 in zip(y,chart["2020-21"].to_numpy(),chart["2025-26"].to_numpy()):
        ax.plot([x0,x1],[yi,yi],color=LIGHT_GREY,lw=4.2,solid_capstyle="butt",zorder=1)
    ax.scatter(chart["2020-21"].to_numpy(),y,s=105,marker="D",facecolor=LIGHT_BLUE,
               edgecolor=WHITE,lw=1.1,label="2020-21",zorder=4)
    ax.scatter(chart["2025-26"].to_numpy(),y,s=92,marker="o",color=MIDNIGHT,
               edgecolor=WHITE,lw=1.1,label="2025-26",zorder=4)
    ax.axvline(0,color="#333333",lw=1);ax.set_yticks(y,chart.l3_label);ax.set_xlabel("Korea gap: leave-one-out reference minus Korea (percentage points)")
    clean(ax,"x");report_legend(ax,ncol=2,loc="upper right")
    title(fig,"5","Korea's relative policy gaps changed direction across topics","Largest L3 gap changes, 2020-21 to 2025-26")
    footer(fig,"Positive values indicate a thinner Korean share than the period-specific leave-one-out reference. Results are sensitive to the small 2020-21 Korean corpus; 2026 is partial.")
    save(fig,"F05_korea_gap_change_OECD")


def annual_domain_series():
    science=(pd.read_csv(ROOT/"relatedness/build/papers_country_field_year_v2.csv.gz",usecols=["country","year","count"])
             .groupby(["country","year"],as_index=False)["count"].sum().rename(columns={"country":"iso","count":"activity"}))
    technology=(pd.read_csv(ROOT/"relatedness/build/patents_country_tech_year.csv.gz",usecols=["country","year","count"])
                .groupby(["country","year"],as_index=False)["count"].sum().rename(columns={"country":"iso","count":"activity"}))
    raw=pd.read_csv(ROOT/"event_attention_rebuild/outputs/ai_events_country_panel_raw_20260903.csv",low_memory=False)
    capped=raw.groupby(["intervention_id","jurisdiction","year"],as_index=False).scope_weight.first()
    capped["iso"]=capped.jurisdiction.map(NAME_TO_ISO)
    policy=(capped.groupby(["iso","year"],as_index=False).scope_weight.sum()
            .rename(columns={"scope_weight":"activity"}))
    return {"Science":science,"Technology":technology,"Policy":policy}


def fixed_oecd_mean(frame: pd.DataFrame, years: range) -> pd.DataFrame:
    fixed=sorted(OECD & set(frame.iso.dropna()))
    grid=pd.MultiIndex.from_product([fixed,years],names=["iso","year"]).to_frame(index=False)
    x=grid.merge(frame,on=["iso","year"],how="left").fillna({"activity":0})
    q=x.groupby("year",as_index=False).activity.mean();q["iso"]="OECD observed"
    return q


def complete_domain_grid(frame: pd.DataFrame, years: range, countries: list[str]) -> pd.DataFrame:
    grid=pd.MultiIndex.from_product([countries,years],names=["iso","year"]).to_frame(index=False)
    return grid.merge(frame,on=["iso","year"],how="left").fillna({"activity":0})


def make_domain_country_trends():
    series=annual_domain_series()
    windows={"Science":range(2015,2022),"Technology":range(2015,2022),"Policy":range(2020,2027)}
    accents={"Science":SCIENCE_BLUE,"Technology":TECH_GREEN,"Policy":POLICY_RED}
    units={"Science":"Fractional AI publication count","Technology":"Fractional AI patent count","Policy":"Effective intervention-year activity"}
    stems={"Science":"F07_science_country_trends_OECD","Technology":"F08_technology_country_trends_OECD","Policy":"F09_policy_country_trends_OECD"}
    comparison=sorted({"US","CN","KR","JP","GB","AU","BR","DE","SA","CA","FR","SG","AR","IN","IT","VN","PH","NL","TR","TH"})
    combined={}
    for domain,frame in series.items():
        years=windows[domain]
        grid=complete_domain_grid(frame,years,comparison)
        oecd=fixed_oecd_mean(frame,years)
        export=pd.concat([grid,oecd],ignore_index=True);export["domain"]=domain
        export.to_csv(DERIVED/f"annual_{domain.lower()}_activity_selected_countries.csv",index=False)
        combined[domain]=export
        fig,ax=plt.subplots(figsize=(13.333,7.5));fig.subplots_adjust(left=.09,right=.88,top=.80,bottom=.17)
        for iso,q in grid.groupby("iso"):
            ax.plot(q.year,q.activity,color="#B9B9B9",lw=1,alpha=.65)
        for iso in ["US","CN","KR","JP"]:
            q=grid[grid.iso.eq(iso)];ax.plot(q.year,q.activity,color=COUNTRY_COLOURS[iso],lw=2.8)
            ax.text(max(years)+.08,q.activity.iloc[-1],DISPLAY[iso],color=COUNTRY_COLOURS[iso],va="center",fontweight="bold")
        ax.plot(oecd.year,oecd.activity,color=COUNTRY_COLOURS["OECD observed"],lw=3.0)
        ax.text(max(years)+.08,oecd.activity.iloc[-1],"OECD",color=COUNTRY_COLOURS["OECD observed"],va="center",fontweight="bold")
        ax.set_xlim(min(years),max(years)+.75);ax.set_xticks(list(years));ax.set_ylabel(units[domain]);clean(ax,"y")
        title(fig,{"Science":"7","Technology":"8","Policy":"9"}[domain],f"{domain} activity across selected countries",f"Annual activity, {min(years)}-{max(years)}")
        caveat="Grey lines show the other countries in the fixed comparison panel. OECD is the unweighted mean of 11 observed members."
        if domain=="Technology": caveat += " The window ends in 2021 to avoid severe recent-patent right truncation."
        if domain=="Policy": caveat += " The 2026 value is annualised from events observed through 3 September."
        footer(fig,caveat);save(fig,stems[domain])

    fig,axes=plt.subplots(1,3,figsize=(13.333,7.5));fig.subplots_adjust(left=.06,right=.96,top=.78,bottom=.18,wspace=.20)
    for ax,domain in zip(axes,["Science","Technology","Policy"]):
        q=combined[domain].copy();years=windows[domain]
        for iso,g in q.groupby("iso"):
            base=float(g.loc[g.year.eq(min(years)),"activity"].iloc[0])
            g=g.copy();g["index"]=100*g.activity/base if base>0 else np.nan
            if iso in COUNTRY_COLOURS:
                ax.plot(g.year,g["index"],color=COUNTRY_COLOURS[iso],lw=2.5)
            elif iso in comparison:
                ax.plot(g.year,g["index"],color="#B9B9B9",lw=.9,alpha=.58)
        ax.axhline(100,color="#777777",lw=.8,ls="--")
        ax.set_title(domain,loc="left",fontsize=16,color=accents[domain])
        ax.set_xticks([min(years),min(years)+2,min(years)+4,max(years)])
        ax.set_ylabel("Index (first year = 100)" if domain=="Science" else "")
        clean(ax,"y")
    handles=[plt.Line2D([0],[0],color=COUNTRY_COLOURS[k],lw=3,label=DISPLAY.get(k,"OECD")) for k in ["US","CN","KR","JP","OECD observed"]]
    legend=fig.legend(handles=handles,loc="upper center",bbox_to_anchor=(.53,.835),ncol=5,frameon=True,facecolor=PLOT_GREY,edgecolor=PLOT_GREY)
    title(fig,"6","Science and technology precede the observed policy acceleration","Lag-aligned analytical windows: capability activity, 2015-21; regulatory-policy activity, 2020-26")
    footer(fig,"All panels are indexed to their first displayed year. Science and technology use the five-year precursor window required by the lag design; policy begins when event coverage becomes usable. OECD is a fixed 11-country observed mean. 2026 policy is annualised.")
    save(fig,"F06_STP_country_trends_lag_aligned_OECD")


def main():
    configure()
    panel=pd.read_parquet(DATA/"regulatory_policy_activity_country_year_l3.parquet")
    policy_master=load_policy_master()
    panel=align_panel_to_policy_master(panel,policy_master)
    make_semantic_evolution(panel)
    make_period_change(panel)
    make_policy_trends()
    make_stp_volume_trends()
    make_korea_gap_change(panel)
    make_domain_country_trends()
    print(f"Created 27 figure files in {OUT}")
    print(f"Created derived data in {DERIVED}")


if __name__ == "__main__":
    main()
