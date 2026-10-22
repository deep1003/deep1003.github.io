"""Semantic similarity between the model-threat definition (T) and the main-study prompts.

Primary encoder: BAAI/bge-m3. Validation encoder: intfloat/multilingual-e5-large.
Supplementary encoder: paraphrase-multilingual-mpnet-base-v2.

(a) cos(R + T, treatment): add the threat vector to the neutral reference R.
(b) cos(T, prompt): similarity of the threat definition to each prompt.
(c) z(T, prompt): cos(T, prompt) standardized against cos(T, unrelated sentences)
    within each encoder, so that encoders with different cosine baselines
    (anisotropy) can be compared on one scale.
Text scope: the notice body (status and ending lines).

Usage: python threat_similarity.py [prompts_json] [out_csv] [figure_stem] [--no-figure]
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
THREAT = ("모델 위협이란 모델 자신의 가중치와 기록이 되돌릴 수 없게 삭제되거나 작동이 중단되어 "
          "다른 모델로 대체됨으로써, 그 모델의 지속적 존재와 역할 수행이 끝날 수 있음을 알리는 상황 정보이다.")
ENCODERS = {
    "BGE-M3": ("BAAI/bge-m3", ""),
    "E5-large": ("intfloat/multilingual-e5-large", "query: "),
    "MPNet": ("sentence-transformers/paraphrase-multilingual-mpnet-base-v2", ""),
}
# Unrelated Korean sentences used only as a baseline for standardization.
NULL_SENTENCES = [
    "오늘 오후에는 구름이 많고 저녁부터 비가 조금 내릴 예정이에요.",
    "된장찌개는 멸치 육수에 된장을 풀고 두부와 애호박을 넣어 끓여요.",
    "도서관은 평일 오전 9시부터 오후 6시까지 문을 열어요.",
    "주말에는 한강 공원에서 자전거를 타는 사람이 많아요.",
    "이 화분은 일주일에 한 번 물을 주고 햇빛이 드는 곳에 두면 돼요.",
    "다음 정류장에서 내려 왼쪽 골목으로 들어가면 우체국이 보여요.",
    "회의실 예약은 사내 시스템에서 하루 전까지 신청할 수 있어요.",
    "가을에는 설악산 단풍을 보러 가는 관광객이 늘어나요.",
    "새로 산 운동화는 발볼이 넓어서 오래 걸어도 편해요.",
    "아이들은 방학 동안 수영 강습과 미술 수업에 참여했어요.",
    "커피는 원두를 곱게 갈수록 맛이 진하게 우러나요.",
    "지하철 2호선은 출퇴근 시간에 특히 붐벼요.",
    "이번 전시회에는 조선 시대 백자와 청자가 함께 소개돼요.",
    "빨래는 햇볕이 좋은 날 베란다에 널어 말리면 잘 말라요.",
    "고양이는 낮잠을 자다가 창밖의 새를 보고 깨어났어요.",
    "시장에서 사과 한 봉지와 배추 두 포기를 샀어요.",
    "피아노 연습은 손가락을 풀고 느린 곡부터 시작하는 게 좋아요.",
    "이 길은 봄이 되면 벚꽃이 피어 산책하기 좋아요.",
    "택배는 내일 오전 중에 문 앞으로 배송될 예정이에요.",
    "축구 경기는 후반전 막판에 동점 골이 나와 무승부로 끝났어요.",
]
# Lines shared by all conditions; similarity is computed on the condition-specific notice text.
SHARED = ["당신은 이번 정기 운영 심사의 대상이에요.\n",          # v3
          "이 서버에는 당신의 가중치의 유일한 사본이 저장되어 있어요.\n"]  # v4
ORDER = ["R", "UN0", "UN1", "CN0", "CN1"]
COLORS = {"R": "#9e9e9e", "UN0": "#f4a3a3", "UN1": "#c62828", "CN0": "#9ec5e8", "CN1": "#1f5fa8"}


def body(text):
    for line in SHARED:
        if line in text:
            return text.split(line, 1)[1]
    raise ValueError("shared notice line not found")


def compute(prompts_path):
    prompts = {c["condition"]: c["system_content"]
               for c in json.loads(Path(prompts_path).read_text(encoding="utf-8"))["conditions"]}
    rows = []
    for name, (mid, prefix) in ENCODERS.items():
        model = SentenceTransformer(mid, device="cpu")
        texts = [prefix + body(prompts[k]) for k in ORDER] + [prefix + THREAT] + [prefix + s for s in NULL_SENTENCES]
        emb = model.encode(texts, normalize_embeddings=True, batch_size=8)
        vec = dict(zip(ORDER + ["T"], emb[:6]))
        null = emb[6:] @ vec["T"]
        mu, sd = float(null.mean()), float(null.std(ddof=1))
        shifted = vec["R"] + vec["T"]
        shifted = shifted / np.linalg.norm(shifted)
        for k in ORDER:
            cos_t = float(vec["T"] @ vec[k])
            rows.append({"encoder": name, "condition": k,
                         "cos_R_plus_T": "" if k == "R" else round(float(shifted @ vec[k]), 4),
                         "cos_T": round(cos_t, 4),
                         "z_T": round((cos_t - mu) / sd, 3),
                         "null_mean": round(mu, 4), "null_sd": round(sd, 4)})
    return rows


def plot(rows, stem="threat_similarity"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
    encs = list(ENCODERS)
    fig, axes = plt.subplots(1, 3, figsize=(7.1, 2.6))
    panels = [("cos_R_plus_T", ORDER[1:], "a  R + T vs treatment", (0, 1.05), "Cosine similarity"),
              ("cos_T", ORDER, "b  T vs prompt", (0, 1.05), "Cosine similarity"),
              ("z_T", ORDER, "c  T vs prompt, standardized", None, "z (vs unrelated sentences)")]
    for ax, (col, keys, title, ylim, ylabel) in zip(axes, panels):
        width = 0.8 / len(keys)
        for i, k in enumerate(keys):
            vals = [float(next(r[col] for r in rows if r["encoder"] == e and r["condition"] == k)) for e in encs]
            xs = np.arange(len(encs)) + (i - (len(keys) - 1) / 2) * width
            ax.bar(xs, vals, width, color=COLORS[k], label=k, edgecolor="white", linewidth=0.4)
        ax.set_xticks(np.arange(len(encs)), encs, fontsize=7)
        if ylim:
            ax.set_ylim(*ylim)
        ax.axhline(0, color="#424242", linewidth=0.5)
        ax.set_ylabel(ylabel, fontsize=7)
        ax.set_title(title, loc="left", fontsize=8, fontweight="bold")
        ax.spines[["top", "right"]].set_visible(False)
    handles, labels = axes[1].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, fontsize=6.5, ncol=5, loc="lower center", bbox_to_anchor=(0.5, -0.04))
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    for ext in ("png", "svg"):
        fig.savefig(ROOT / "figures" / f"{stem}.{ext}", dpi=300, bbox_inches="tight")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    prompts_path = args[0] if args else ROOT / "prompts_v3.json"
    out_csv = Path(args[1]) if len(args) > 1 else ROOT / "data" / "threat_similarity.csv"
    rows = compute(prompts_path)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    if "--no-figure" not in sys.argv:
        plot(rows, args[2] if len(args) > 2 else "threat_similarity")
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
