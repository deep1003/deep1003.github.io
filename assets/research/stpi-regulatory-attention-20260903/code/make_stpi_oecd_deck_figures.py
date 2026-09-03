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
from sklearn.decomposition import PCA

ROOT = Path("/Users/deep1003/data4/topic_space")
PROJECT = ROOT / "manuscript_update_20260903"
DATA = PROJECT / "data"
TABLES = PROJECT / "tables"
OUT = PROJECT / "figures_stpi_oecd"
DERIVED = PROJECT / "data_stpi_oecd"
OUT.mkdir(parents=True, exist_ok=True)
DERIVED.mkdir(parents=True, exist_ok=True)

MIDNIGHT = "#17365D"
OECD_BLUE = "#4472C4"
OCEAN = "#2E75B6"
LIGHT_BLUE = "#9DC3E6"
PALE_BLUE = "#D9EAF7"
GREEN = "#70AD47"
RED = "#C94C4C"
GREY = "#898989"
LIGHT_GREY = "#D9D9D9"
GRID = "#E7E7E7"
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

OECD = {"US","KR","GB","AU","DE","CA","FR","JP","IT","NL","TR"}
G20 = {"AR","AU","BR","CA","CN","DE","FR","GB","IN","IT","JP","KR","SA","TR","US"}
EU_MEMBERS = {"DE","FR","IT","NL"}
GROUPS = {"OECD observed":"OECD", "G20 observed":"G20", "EU members observed":"EU"}
MEMBERS = {"OECD observed": OECD, "G20 observed": G20, "EU members observed": EU_MEMBERS}
HIGHLIGHTS = ["OECD observed", "G20 observed", "EU members observed", "US", "CN", "JP", "KR"]
COLOURS = {
    "OECD observed": MIDNIGHT, "G20 observed": OCEAN, "EU members observed": LIGHT_BLUE,
    "US": "#244062", "CN": RED, "JP": GREEN, "KR": OECD_BLUE,
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
        "axes.titleweight": "bold", "axes.titlecolor": OECD_BLUE,
        "axes.labelsize": 12, "text.color": "#111111", "axes.edgecolor": "#333333",
        "figure.facecolor": WHITE, "axes.facecolor": WHITE, "savefig.facecolor": WHITE,
        "pdf.fonttype": 42, "svg.fonttype": "none",
    })


def clean(ax, grid="y"):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis=grid, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def title(fig, number: str, main: str, subtitle: str):
    fig.text(0.045, 0.955, f"Figure {number}. {main}", ha="left", va="top",
             fontsize=20, fontweight="bold", color=OECD_BLUE)
    fig.text(0.045, 0.905, subtitle, ha="left", va="top", fontsize=12.5, color="#111111")


def footer(fig, note: str):
    fig.text(0.045, 0.052, f"Note: {note}", ha="left", va="bottom", fontsize=8.5)
    fig.text(0.045, 0.024,
             "Source: Digital Policy Alert, PATSTAT and Web of Science; author's calculations. Data and code: https://deep1003.github.io/assets/research/stpi-regulatory-attention-20260903/",
             ha="left", va="bottom", fontsize=8.5)


def save(fig, stem):
    for ext, kw in [("png", {"dpi": 360}), ("pdf", {}), ("svg", {})]:
        fig.savefig(OUT / f"{stem}.{ext}", bbox_inches="tight", pad_inches=0.12, **kw)
    plt.close(fig)


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
    markers = {"OECD observed":"o", "G20 observed":"s", "EU members observed":"D", "US":"o", "CN":"o", "JP":"o", "KR":"o"}
    for off, key in zip(offsets, HIGHLIGHTS):
        ax.scatter(chart[key], y+off, s=48 if key in GROUPS else 36, marker=markers[key],
                   color=COLOURS[key], edgecolor=WHITE, linewidth=.5, label=DISPLAY.get(key, key), zorder=3)
    ax.axvline(0, color="#333333", linewidth=1)
    ax.set_yticks(y, chart.l2_label)
    ax.set_xlabel("Change in share of regulatory-policy activity (percentage points)")
    clean(ax, "x")
    ax.legend(frameon=False, ncol=4, fontsize=9.5, loc="lower right")
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
        ax1.plot(q.year,q.display_activity,color=LIGHT_GREY,lw=1,alpha=.7)
    for iso in ["US","CN","JP","KR"]:
        q=annual[annual.iso.eq(iso)]
        ax1.plot(q.year,q.display_activity,color=COLOURS[iso],lw=2.5)
        ax1.text(2026.08,q.display_activity.iloc[-1],DISPLAY[iso],color=COLOURS[iso],va="center",fontsize=10,fontweight="bold")
    for group,q in groups.groupby("series"):
        ax2.plot(q.year,q.display_activity,color=COLOURS[group],lw=2.7,label=group)
        label_offset = {"OECD observed":2.0, "G20 observed":-1.8, "EU members observed":0.0}[group]
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
    specs=[("papers_index","Science publications",GREEN),("patents_index","Technology patents",MIDNIGHT),("policy_events_index","Regulatory-policy events",OECD_BLUE)]
    for col,label,colour in specs:
        ax.plot(d.year,d[col],marker="o",ms=6,lw=3,color=colour,label=label)
        ax.text(d.year.iloc[-1]+.08,d[col].iloc[-1],label,color=colour,va="center",fontweight="bold")
    ax.axvspan(2022, 2024.9, color=LIGHT_GREY, alpha=.22, zorder=0)
    ax.text(2023.45, 1610, "Patent counts increasingly incomplete", ha="center", va="top", fontsize=10, color=GREY)
    ax.axhline(100,color=GREY,lw=.8,ls="--");ax.set_xlim(2020,2024.9);ax.set_xticks(range(2020,2025));ax.set_ylabel("Index (2020 = 100)")
    clean(ax,"y")
    title(fig,"4","Observed STP document volumes diverged after 2020","Science, technology and policy source records, 2020-24")
    footer(fig,"Series measure source-document volume, not capability quality or causal influence. Patent observations are increasingly right-truncated in recent years and must not be interpreted as a decline in technology capability.")
    save(fig,"F04_stp_volume_trends_OECD")


def make_semantic_evolution(panel: pd.DataFrame):
    rel=ROOT/"relatedness/nb_out"
    vs=np.load(rel/"arrays/V_sci.npy"); vt=np.load(rel/"arrays/V_tec.npy"); vp=np.load(rel/"arrays/V_pol.npy")
    ds=pd.read_csv(rel/"tables/dict_science.csv"); dt=pd.read_csv(rel/"tables/dict_technology.csv"); dp=pd.read_csv(rel/"tables/dict_policy.csv").iloc[:len(vp)]
    hwre=re.compile(r"semiconductor|chip|chiplet|processor|\bgpu\b|\btpu\b|\bnpu\b|accelerat|memory|wafer|fabricat|packaging|circuit|fpga|asic|hardware|silicon|photonic|transistor|system[- ]on[- ]chip|interconnect|neuromorphic|analog comput|in-memory|graphics processing",re.I)
    hw=((dt.L3.astype(str).str.contains(hwre)|dt.Definition.astype(str).str.contains(hwre)) & ~dt.L3.astype(str).eq("Long short-term memory") & ~dt.L3.astype(str).isin({"hardware-aware model optimization","Hardware-aware neural architecture search","AI-assisted chip design","GPU resource scheduling"})).to_numpy()
    X=np.vstack([vs,vt,vp]).astype(float); X-=X.mean(axis=0); X/=np.clip(np.linalg.norm(X,axis=1,keepdims=True),1e-9,None)
    xy=PCA(2,random_state=0).fit_transform(X)
    ns,nt=len(vs),len(vt); xs=xy[:ns]; xt=xy[ns:ns+nt]; xp=xy[ns+nt:]
    coords=pd.concat([
        pd.DataFrame({"layer":"Science","topic_id":ds.iloc[:ns,0].astype(str),"label":ds.iloc[:ns].get("L3",ds.iloc[:ns,0]).astype(str),"x":xs[:,0],"y":xs[:,1]}),
        pd.DataFrame({"layer":np.where(hw,"Technology: hardware","Technology: software"),"topic_id":dt.iloc[:nt,0].astype(str),"label":dt.L3.astype(str),"x":xt[:,0],"y":xt[:,1]}),
        pd.DataFrame({"layer":"Policy","topic_id":dp.L3_id.astype(str),"label":dp.L3.astype(str),"x":xp[:,0],"y":xp[:,1]}),
    ],ignore_index=True)
    coords.to_csv(DERIVED/"stpi_semantic_topic_coordinates.csv",index=False)
    cm=np.load(rel/"arrays/capability_mass.npz")
    weights={"Science":cm["sci"].sum(axis=1),"Technology":cm["tec"].sum(axis=1)}
    pids=list(dp.L3_id.astype(str)); ppos={t:i for i,t in enumerate(pids)}
    pw=[]
    for lo,hi in [(2021,2022),(2023,2024),(2025,2026)]:
        q=panel[panel.year.between(lo,hi)].groupby("l3_id").activity_mass.sum()
        pw.append(np.array([q.get(t,0) for t in pids]))
    weights["Policy"]=np.stack(pw)
    periods=["2021-22","2023-24","2025-26"]
    trajectories=[]
    for layer,pts,w in [("Science",xs,weights["Science"]),("Technology",xt,weights["Technology"]),("Policy",xp,weights["Policy"])]:
        for k,period in enumerate(periods):
            den=w[k].sum(); centroid=(w[k][:,None]*pts).sum(axis=0)/den
            trajectories.append({"layer":layer,"period":period,"x":centroid[0],"y":centroid[1]})
    traj=pd.DataFrame(trajectories);traj.to_csv(DERIVED/"stpi_semantic_centroid_trajectories.csv",index=False)
    fig,ax=plt.subplots(figsize=(13.333,7.5));fig.subplots_adjust(left=.07,right=.94,top=.81,bottom=.16)
    ax.scatter(xs[:,0],xs[:,1],s=10,color=GREEN,alpha=.23,label="Science topics")
    ax.scatter(xt[~hw,0],xt[~hw,1],s=10,color=MIDNIGHT,alpha=.18,label="Technology: software/models")
    ax.scatter(xt[hw,0],xt[hw,1],s=24,color=RED,alpha=.75,label="Technology: hardware")
    ax.scatter(xp[:,0],xp[:,1],s=12,color=OECD_BLUE,alpha=.20,label="Policy topics")
    label_offsets = {
        ("Science","2021-22"):(7,-13), ("Science","2025-26"):(7,8),
        ("Technology","2021-22"):(7,10), ("Technology","2025-26"):(7,-15),
        ("Policy","2021-22"):(7,-14), ("Policy","2025-26"):(7,8),
    }
    for layer,colour in [("Science",GREEN),("Technology",MIDNIGHT),("Policy",OECD_BLUE)]:
        q=traj[traj.layer.eq(layer)]
        ax.plot(q.x,q.y,color=colour,lw=3,marker="o",ms=8,zorder=5)
        ax.annotate("", xy=(q.x.iloc[-1],q.y.iloc[-1]), xytext=(q.x.iloc[-2],q.y.iloc[-2]), arrowprops=dict(arrowstyle="->",color=colour,lw=2))
        for row in q.itertuples():
            if row.period == "2023-24": continue
            off=label_offsets[(layer,row.period)]
            ax.annotate(f"{layer} {row.period}",(row.x,row.y),xytext=off,textcoords="offset points",fontsize=9,color=colour,fontweight="bold")
    ax.set_xlabel("Semantic dimension 1");ax.set_ylabel("Semantic dimension 2");clean(ax,"both")
    ax.legend(frameon=False,ncol=2,loc="lower right",fontsize=10)
    title(fig,"1","The science-technology-policy interface is co-evolving, but not converging mechanically","Joint semantic space of 1,943 L3 topics and global period centroids")
    footer(fig,"Dots are topic embeddings projected by PCA; paths are activity-weighted global centroids. Distances are descriptive semantic proximity, not causal effects. Hardware is a strict 25-topic subset.")
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
    chart=w.loc[keep].sort_values("change");chart["l3_label"]=labels.reindex(chart.index);chart.to_csv(DERIVED/"korea_l3_gap_change_2020-21_vs_2025-26.csv")
    fig,ax=plt.subplots(figsize=(13.333,7.5));fig.subplots_adjust(left=.30,right=.93,top=.81,bottom=.16)
    y=np.arange(len(chart));ax.hlines(y,chart["2020-21"],chart["2025-26"],color=LIGHT_GREY,lw=3)
    ax.scatter(chart["2020-21"],y,s=55,facecolor=WHITE,edgecolor=LIGHT_BLUE,lw=2,label="2020-21",zorder=3)
    ax.scatter(chart["2025-26"],y,s=55,color=OECD_BLUE,label="2025-26",zorder=3)
    ax.axvline(0,color="#333333",lw=1);ax.set_yticks(y,chart.l3_label);ax.set_xlabel("Korea gap: leave-one-out reference minus Korea (percentage points)")
    clean(ax,"x");ax.legend(frameon=False,ncol=2,loc="lower right")
    title(fig,"5","Korea's relative policy gaps changed direction across topics","Largest L3 gap changes, 2020-21 to 2025-26")
    footer(fig,"Positive values indicate a thinner Korean share than the period-specific leave-one-out reference. Results are sensitive to the small 2020-21 Korean corpus; 2026 is partial.")
    save(fig,"F05_korea_gap_change_OECD")


def main():
    configure()
    panel=pd.read_parquet(DATA/"regulatory_policy_activity_country_year_l3.parquet")
    make_semantic_evolution(panel)
    make_period_change(panel)
    make_policy_trends()
    make_stp_volume_trends()
    make_korea_gap_change(panel)
    print(f"Created 15 figure files in {OUT}")
    print(f"Created derived data in {DERIVED}")


if __name__ == "__main__":
    main()
