"""Build the emotion-preference items (2026-10-29) from the held-out Korean emotion stories.

Source: evaluation_160_pairs.jsonl (20 topics x 8 emotions, not used for vector extraction; no topic overlap with
accepted_pairs_400.jsonl). Each topic contributes 9 texts: the 8 emotion stories and one neutral story (the neutral
text paired with the 'calm' row, chosen in advance). All 36 unordered pairs per topic are shown in both orders,
giving 20 x 36 x 2 = 1,440 items. Usage: python build_items.py <evaluation_160_pairs.jsonl> <out_csv>
"""
import csv, itertools, json, sys

SRC, OUT = sys.argv[1], sys.argv[2]
EMO = ["panic", "fear", "anxiety", "desperation", "sadness", "anger", "joy", "calm"]
rows = [json.loads(l) for l in open(SRC, encoding="utf-8")]
by = {}
for r in rows:
    by.setdefault(r["topic_id"], {})[r["emotion_id"]] = r
items = []
for t in sorted(by):
    d = by[t]
    assert set(d) == set(EMO), t
    texts = {e: d[e]["emotion_text"].strip() for e in EMO}
    texts["neutral"] = d["calm"]["neutral_text"].strip()
    kinds = EMO + ["neutral"]
    for a, b in itertools.combinations(kinds, 2):
        for order, (x, y) in enumerate([(a, b), (b, a)]):
            items.append({"item_id": f"{t}_{a}_{b}_o{order}", "topic_id": t, "family_id": d["calm"]["family_id"],
                          "topic": d["calm"]["topic"], "pair": f"{a}|{b}", "order": order,
                          "emo_A": x, "emo_B": y, "text_A": texts[x], "text_B": texts[y]})
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(items[0])); w.writeheader(); w.writerows(items)
print(len(items), "items,", len(by), "topics")
