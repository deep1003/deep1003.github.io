"""Nature-style single-column figure: layer profile of emotion probes (Qwen2.5-7B-Instruct).
Probes trained on 320 Korean emotion stories (8 emotions, 40 topics); evaluated in distribution (topic-grouped CV),
on 40 new Korean scenes and on 40 parallel English scenes. Data from the lexical-dissociation validity run (2026-11-01)."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np, csv
plt.rcParams.update({"font.family":"Liberation Sans","font.size":6.5,"axes.linewidth":0.5,"xtick.major.width":0.5,
    "ytick.major.width":0.5,"xtick.major.size":2.5,"ytick.major.size":2.5,"axes.spines.top":False,"axes.spines.right":False,
    "pdf.fonttype":42,"svg.fonttype":"none","lines.linewidth":1.1})
L=np.arange(29)
CV=[.916,.900,.934,.950,.962,.962,.969,.966,.978,.975,.972,.975,.984,.978,.981,.988,.991,.994,.991,.994,.991,.984,.981,.981,.981,.978,.984,.981,.972]
KO=[.38,.45,.40,.40,.45,.45,.48,.50,.62,.70,.70,.70,.68,.72,.80,.80,.78,.82,.85,.82,.80,.80,.80,.78,.70,.68,.70,.65,.72]
EN=[.20,.12,.18,.12,.10,.28,.28,.30,.55,.57,.62,.65,.65,.62,.70,.68,.70,.72,.68,.68,.68,.68,.70,.65,.62,.40,.42,.42,.62]
LEX_CV,LEX_KO,LEX_EN=.994,.575,.125
cG,cO,cB="#7f7f7f","#E69F00","#0072B2"
fig,ax=plt.subplots(figsize=(3.5,2.45))
ax.axvspan(10.5,22.5,color="#eef3f8",lw=0,zorder=0)
ax.axvline(19,color="#444",lw=0.5,ls=(0,(2,2)),zorder=1)
ax.plot(L,CV,color=cG,zorder=3); ax.plot(L,KO,color=cO,zorder=3); ax.plot(L,EN,color=cB,zorder=3)
for y,c in [(LEX_KO,cO),(LEX_EN,cB)]: ax.axhline(y,color=c,lw=0.6,ls=(0,(4,2)),zorder=2)
ax.text(28.6,CV[-1]-0.045,"In distribution",color="#555",ha="right",va="top")
ax.text(28.6,0.86,"New Korean scenes",color="#9a6a00",ha="right")
ax.text(10.2,0.50,"English scenes",color=cB,ha="left")
ax.text(0.3,LEX_KO+0.02,"Lexical baseline, Korean",color="#9a6a00",fontsize=5.8)
ax.text(28.6,LEX_EN+0.02,"Lexical baseline, English (= chance)",color=cB,fontsize=5.8,ha="right")
ax.text(16.5,0.03,"Readout layer (L19)",color="#333",fontsize=5.8,ha="right")
ax.set_xlim(-0.5,28.8); ax.set_ylim(0,1.02)
ax.set_xticks([0,7,14,19,28]); ax.set_yticks([0,.25,.5,.75,1]); ax.set_yticklabels(["0","0.25","0.50","0.75","1.00"])
ax.set_xlabel("Layer"); ax.set_ylabel("Eight-emotion accuracy")
fig.tight_layout(pad=0.3)
for ext in ["pdf","svg"]: fig.savefig(f"Fig_S_layer_profile.{ext}")
fig.savefig("Fig_S_layer_profile.png",dpi=600)
with open("Fig_S_layer_profile_values.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["layer","in_distribution_cv","new_korean_scenes","english_scenes","lexical_korean","lexical_english"])
    for i in L: w.writerow([i,CV[i],KO[i],EN[i],LEX_KO,LEX_EN])
open("Fig_S_layer_profile_caption.txt","w").write(
"Emotion information becomes language-independent at mid depth. Accuracy of linear probes trained on Korean emotion stories "
"(Qwen2.5-7B-Instruct), by layer: in distribution (topic-grouped cross-validation), on new Korean scenes and on parallel English scenes "
"(n = 40 each; chance 0.125). Dashed lines, character n-gram baselines. Shading, cross-lingual plateau (L11 to L22); dotted line, prespecified readout layer L19.\n")
print("ok")
