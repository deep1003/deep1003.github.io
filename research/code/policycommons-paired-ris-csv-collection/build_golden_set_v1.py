#!/usr/bin/env python3
"""Build the identifier-exact PCGS AIGOV5 Golden Set candidate."""
from __future__ import annotations

import glob, hashlib, json, re
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "golden_set_v1"
RIS_MASTER = ROOT / "analysis_steps5_8_v4/07_all_classified_records.csv.gz"
SEED = 20260920
REQUIRED = {"type", "title", "url", "publisher", "year", "topics", "country"}

def normalise_coi(value):
    text = str(value).strip().lower()
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", text)
    return re.sub(r"^doi:\s*", "", text).rstrip("/")

def artifact_id(value):
    match = re.search(r"/artifacts/(\d+)/", str(value))
    return match.group(1) if match else ""

def split_country(value):
    code, sep, name = str(value).strip().partition(":")
    return (code.strip(), name.strip()) if sep else ("", code.strip())

def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ris = pd.read_csv(RIS_MASTER, dtype=str).fillna("")
    ris["join_coi"] = ris.policy_commons_id.map(normalise_coi)
    ris["join_artifact_id"] = ris.url.map(artifact_id)

    frames, manifest = [], []
    for filename in sorted(glob.glob(str(ROOT / "raw_csv/*/*.csv"))):
        path = Path(filename)
        frame = pd.read_csv(path, dtype=str).fillna("")
        if not REQUIRED.issubset(frame.columns):
            raise ValueError(f"Required CSV columns missing: {path}")
        frame["csv_source_file"] = str(path.relative_to(ROOT))
        frame["csv_source_row"] = range(1, len(frame) + 1)
        frames.append(frame)
        manifest.append({"file": str(path.relative_to(ROOT)), "rows": len(frame),
                         "bytes": path.stat().st_size, "sha256": sha256(path)})

    observations = pd.concat(frames, ignore_index=True)
    observations["join_coi"] = observations.coi.map(normalise_coi)
    observations["join_artifact_id"] = observations.url.map(artifact_id)
    observations["join_key"] = observations.join_coi + "|" + observations.join_artifact_id

    value_columns = ["type", "title", "url", "publisher", "people", "year",
                     "coi", "language", "topics", "issn", "isbn", "country"]
    conflicts = []
    for key, group in observations.groupby("join_key", sort=False):
        values = {column: sorted(set(group.loc[group[column].ne(""), column]))
                  for column in value_columns}
        values = {column: items for column, items in values.items() if len(items) > 1}
        if values:
            conflicts.append({"join_key": key, "observation_count": len(group),
                              "conflicting_fields_json": json.dumps(values, ensure_ascii=False)})

    canonical = observations.sort_values(
        ["join_key", "csv_source_file", "csv_source_row"], kind="stable"
    ).drop_duplicates("join_key", keep="first").copy()
    groups = observations.groupby("join_key")
    canonical["csv_observation_count"] = canonical.join_key.map(groups.size()).astype(int)
    canonical["csv_source_files"] = canonical.join_key.map(
        groups.csv_source_file.apply(lambda values: ";".join(sorted(set(values))))
    )
    canonical[["published_in_country_code", "published_in_country_name"]] = (
        canonical.country.apply(lambda value: pd.Series(split_country(value)))
    )

    ris_keys = set(zip(ris.join_coi, ris.join_artifact_id))
    csv_keys = set(zip(canonical.join_coi, canonical.join_artifact_id))
    canonical["exact_ris_pair"] = [(coi, aid) in ris_keys for coi, aid in zip(
        canonical.join_coi, canonical.join_artifact_id)]
    keep = ["join_coi", "join_artifact_id", "type", "people", "topics", "issn",
            "isbn", "country", "published_in_country_code",
            "published_in_country_name", "csv_observation_count", "csv_source_files"]
    paired = ris.merge(canonical.loc[canonical.exact_ris_pair, keep],
                       on=["join_coi", "join_artifact_id"], how="inner",
                       validate="one_to_one")
    paired["pairing_status"] = "exact_coi_and_artifact_id"
    paired["human_validation_status"] = "pending"
    paired["golden_set_version"] = "pcgs-aigov5-golden-v1"

    ris_index = pd.MultiIndex.from_frame(ris[["join_coi", "join_artifact_id"]])
    csv_index = pd.MultiIndex.from_tuples(csv_keys)
    unmatched_ris = ris.loc[~ris_index.isin(csv_index)].copy()
    unmatched_csv = canonical.loc[~canonical.exact_ris_pair].copy()
    eligible = paired.loc[paired.ai_include.astype(str).eq("1") &
                          paired.document_eligible.astype(str).str.lower().eq("true")].copy()

    paired.to_parquet(OUT / "golden_set_master.parquet", index=False, compression="zstd")
    paired.to_csv(OUT / "golden_set_master.csv.gz", index=False, compression="gzip")
    eligible.to_csv(OUT / "golden_set_document_eligible.csv.gz", index=False, compression="gzip")
    observations.to_csv(OUT / "csv_source_observations.csv.gz", index=False, compression="gzip")
    pd.DataFrame(manifest).to_csv(OUT / "input_csv_manifest.csv", index=False)
    pd.DataFrame(conflicts).to_csv(OUT / "csv_field_conflicts.csv", index=False)
    unmatched_ris.to_csv(OUT / "unmatched_ris_records.csv.gz", index=False, compression="gzip")
    unmatched_csv.to_csv(OUT / "unmatched_csv_records.csv", index=False)

    sample = paired.sample(n=min(100, len(paired)), random_state=SEED).copy()
    for column in ["review_ai", "review_document_type", "review_published_country",
                   "review_issuer_country", "review_pairing", "adjudication_notes"]:
        sample[column] = ""
    sample.to_csv(OUT / "validation_sample_100.csv", index=False)

    summary = {
        "version": "pcgs-aigov5-golden-v1", "created_at": datetime.now(timezone.utc).isoformat(),
        "csv_files": len(manifest), "csv_observations": len(observations),
        "csv_unique_join_keys": len(canonical), "ris_canonical_records": len(ris),
        "exact_ris_csv_pairs": len(paired), "ris_pair_coverage": round(len(paired)/len(ris), 6),
        "unmatched_ris_records": len(unmatched_ris), "unmatched_csv_records": len(unmatched_csv),
        "csv_join_keys_with_field_conflicts": len(conflicts),
        "published_country_nonblank": int(paired.published_in_country_name.ne("").sum()),
        "topics_nonblank": int(paired.topics.ne("").sum()),
        "document_eligible": len(eligible), "human_validation_status": "pending",
        "deletion_performed": False,
    }
    (OUT / "SUMMARY.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
