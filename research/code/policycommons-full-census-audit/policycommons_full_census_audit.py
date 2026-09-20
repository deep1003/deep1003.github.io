#!/usr/bin/env python3
"""Vectorised full-census audit for the Policy Commons Golden Set.

The program never changes the input release. It writes candidates, summaries,
regression-test results and proposed labels to a new timestamped run directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pycountry


DEFAULT_INPUT = Path(
    "/Users/deep1003/Downloads/pcgs_aigov5_20260920/"
    "final_release_v5/policycommons_ai_master_final_v5.parquet"
)
DEFAULT_OUTPUT_ROOT = Path(
    "/Users/deep1003/Downloads/pcgs_aigov5_20260920/full_census_audit/runs"
)

AI_EXPLICIT = re.compile(
    r"artificial intelligence|machine learning|deep learning|reinforcement learning|"
    r"neural networks?|natural language processing|computer vision|generative ai|"
    r"large language models?|\bllms?\b|\bgpt(?:-?\d+)?\b|인공지능|기계학습|머신러닝|"
    r"人工智能|人工智慧|人工知能",
    re.I,
)
AI_GOVERNANCE = re.compile(
    r"\bai\s+(?:governance|risk|system|policy|ethics|regulation|safety|technology|"
    r"strategy|standard)s?\b",
    re.I,
)
AI_AMBIGUOUS = re.compile(
    r"expert systems?|knowledge[- ]based systems?|machine intelligence|"
    r"intelligent systems?|지능형|\bml\b|\bai\b",
    re.I,
)
AI_ALTERNATIVE = re.compile(
    r"avian influenza|bird flu|biological neural|neural tissue|artificial insemination",
    re.I,
)
MEETING_TRIGGER = re.compile(
    r"(?=.*\bagenda\b)(?=.*\b(?:meeting|council|committee|board|parliament)\b)|"
    r"notice of .*meeting|meeting notice",
    re.I,
)
BUNDLE_OVERRIDE = re.compile(
    r"minutes|supporting documents?|supporting materials?|related documents?|"
    r"business papers?|\bpapers\b|presentations?|\breports?\b|interim report|"
    r"substantive summary|\bsummary\b|strategy|assessment|recommendations?|briefing|"
    r"submissions?|transcript|official record|digital government agenda",
    re.I,
)
RECRUITMENT_TRIGGER = re.compile(
    r"job profile|job and traineeship opportunities|position vacancy announcement|"
    r"position description|job description|vacancy notice|career opportunit",
    re.I,
)
RECRUITMENT_OVERRIDE = re.compile(
    r"policy|manual|compliance|evaluation|impact|security|memorandum|report|study|"
    r"assessment|labou?r market|workforce strategy",
    re.I,
)
ARCHIVE_FINDING_AID = re.compile(
    r"indexed list of files|file index|archival catalogue|finding aid",
    re.I,
)
ACADEMIC_OR_PATENT = re.compile(
    r"\bthesis\b|\bdissertation\b|\bconference paper\b|\bpatent application\b",
    re.I,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def text_field(frame: pd.DataFrame) -> pd.Series:
    fields = ["title", "abstract", "keywords", "topics_combined"]
    return frame[fields].fillna("").astype(str).agg(" ".join, axis=1)


def iso3(value: object) -> str:
    code = str(value or "").strip().upper()
    if len(code) == 3:
        return code
    country = pycountry.countries.get(alpha_2=code) if len(code) == 2 else None
    return country.alpha_3 if country else ""


def add_flag(frame: pd.DataFrame, name: str, mask: pd.Series, severity: str,
             action: str, evidence: str) -> None:
    frame[name] = mask.fillna(False).astype(bool)
    frame.attrs.setdefault("rules", []).append({
        "rule_id": name,
        "severity": severity,
        "recommended_action": action,
        "evidence_requirement": evidence,
    })


def build_audit(
    frame: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    data = frame.copy()
    title = data["title"].fillna("").astype(str)
    publisher = data["publisher"].fillna("").astype(str)
    combined = text_field(data)
    eligible = data["document_eligible_v2"].astype(bool)
    analysis_country = data["analysis_country_v3"].fillna("").astype(str)
    published = data["published_in_country_code"].map(iso3)
    issuer = data["issuer_country_v3"].fillna("").astype(str).str.upper()

    add_flag(data, "E001_duplicate_record_id", data["record_id"].duplicated(False),
             "critical", "block_release", "record_id must be unique")
    add_flag(data, "E002_pairing_not_exact",
             data["pairing_status"].fillna("").ne("exact_coi_and_artifact_id"),
             "critical", "quarantine", "normalised coi and URL artefact ID must agree")
    add_flag(data, "E003_missing_stable_identifier",
             data["policy_commons_id"].fillna("").eq("") | data["url"].fillna("").eq(""),
             "high", "review_identity", "retain both provider ID and URL")
    add_flag(data, "E004_missing_title", title.str.strip().eq(""),
             "high", "review_metadata", "title must be present")
    add_flag(data, "E005_invalid_year",
             pd.to_numeric(data["year"], errors="coerce").notna()
             & ~pd.to_numeric(data["year"], errors="coerce").between(1600, 2026),
             "medium", "review_date", "distinguish publication, revision and retrieval date")

    explicit = combined.str.contains(AI_EXPLICIT) | combined.str.contains(AI_GOVERNANCE)
    alternative = combined.str.contains(AI_ALTERNATIVE)
    ambiguous = combined.str.contains(AI_AMBIGUOUS)
    add_flag(data, "A001_metadata_negative_ai_provenance",
             ~explicit & data["ai_include"].astype(str).eq("1"),
             "information", "retain_without_additional_ai_review",
             "documented AI-oriented collection provenance is sufficient for retention")
    add_flag(data, "A002_probable_alternative_ai_meaning",
             alternative & ~explicit,
             "high", "review_for_non_ai", "positive alternative meaning and no independent AI evidence")
    add_flag(data, "A003_ambiguous_ai_only", ambiguous & ~explicit & ~alternative,
             "information", "retain_under_collection_provenance",
             "do not exclude unless positive non-AI evidence is independently established")

    meeting = title.str.contains(MEETING_TRIGGER)
    bundle = title.str.contains(BUNDLE_OVERRIDE)
    recruitment = title.str.contains(RECRUITMENT_TRIGGER)
    recruitment_override = title.str.contains(RECRUITMENT_OVERRIDE)
    archival = title.str.contains(ARCHIVE_FINDING_AID)
    academic = title.str.contains(ACADEMIC_OR_PATENT)
    add_flag(data, "D001_eligible_standalone_meeting_document", eligible & meeting & ~bundle,
             "high", "propose_exclude", "meeting trigger without a substantive bundle signal")
    add_flag(data, "D002_excluded_substantive_meeting_bundle", ~eligible & meeting & bundle,
             "high", "propose_restore", "bundle signal overrides logistical meeting exclusion")
    add_flag(data, "D003_eligible_standalone_recruitment", eligible & recruitment & ~recruitment_override,
             "high", "propose_exclude", "standalone recruitment material")
    add_flag(data, "D004_excluded_recruitment_policy_or_analysis",
             ~eligible & recruitment & recruitment_override,
             "high", "propose_restore", "policy, evaluation or labour-market content")
    add_flag(data, "D005_eligible_archival_finding_aid", eligible & archival,
             "high", "propose_exclude", "pure catalogue, file list or finding aid")
    add_flag(data, "D006_eligible_academic_or_patent_candidate", eligible & academic,
             "medium", "review_document_form", "exclude only a standalone academic work or patent")

    add_flag(data, "C001_eligible_country_unresolved", eligible & analysis_country.eq(""),
             "high", "review_country", "retain unresolved rather than invent attribution")
    add_flag(data, "C002_provider_issuer_country_conflict",
             published.ne("") & issuer.ne("") & published.ne(issuer),
             "high", "review_country_conflict", "explicit issuer jurisdiction may override publication place")
    add_flag(data, "C003_british_columbia_false_uk",
             publisher.str.contains("British Columbia", case=False, regex=False)
             & analysis_country.str.contains("GBR", regex=False),
             "critical", "correct_to_canada", "boundary-aware institution alias")
    add_flag(data, "C004_nz_productivity_false_australia",
             publisher.eq("New Zealand Productivity Commission")
             & analysis_country.str.contains("AUS", regex=False),
             "critical", "correct_to_new_zealand", "longest-specific-name alias")
    add_flag(data, "C005_kosovo_not_xkx",
             publisher.eq("Government of Kosovo") & analysis_country.ne("XKX"),
             "critical", "correct_to_kosovo", "explicit issuer jurisdiction")
    add_flag(data, "C006_public_issuer_library_unresolved",
             publisher.isin({"Alberta Legislature Library", "Institute of Museum and Library Services",
                             "New Zealand Parliamentary Library", "National Library of Australia"})
             & analysis_country.eq(""),
             "high", "review_public_issuer", "distinguish issuing public body from passive repository")
    add_flag(data, "C007_national_commission_unresolved",
             publisher.eq("Canadian Commission for Unesco") & analysis_country.ne("CAN"),
             "high", "correct_to_canada", "official national commission")
    add_flag(data, "C008_multiple_country_codes",
             analysis_country.str.split(";").map(lambda values: len([v for v in values if v.strip()]) > 1),
             "review", "verify_each_country", "each supported country receives one unit-weight row")

    rule_rows = []
    for rule in data.attrs["rules"]:
        count = int(data[rule["rule_id"]].sum())
        rule_rows.append({**rule, "candidate_count": count})
    summary = pd.DataFrame(rule_rows).sort_values(["severity", "rule_id"])

    rule_cols = [r["rule_id"] for r in data.attrs["rules"]]
    candidate_cols = [
        r["rule_id"] for r in data.attrs["rules"] if r["severity"] != "information"
    ]
    data["audit_information_count"] = data[rule_cols].sum(axis=1) - data[candidate_cols].sum(axis=1)
    data["audit_flag_count"] = data[candidate_cols].sum(axis=1)
    data["audit_rule_ids"] = data[candidate_cols].apply(
        lambda row: ";".join(row.index[row.astype(bool)]), axis=1
    )
    candidates = data.loc[data["audit_flag_count"].gt(0)].copy()

    regressions = pd.DataFrame([
        {"test": "unique_record_id", "passed": not data["E001_duplicate_record_id"].any()},
        {"test": "exact_pairing", "passed": not data["E002_pairing_not_exact"].any()},
        {"test": "british_columbia_not_gbr", "passed": not data["C003_british_columbia_false_uk"].any()},
        {"test": "nz_productivity_not_aus", "passed": not data["C004_nz_productivity_false_australia"].any()},
        {"test": "government_kosovo_xkx", "passed": not data["C005_kosovo_not_xkx"].any()},
        {"test": "public_issuer_libraries_resolved", "passed": not data["C006_public_issuer_library_unresolved"].any()},
        {"test": "national_commission_resolved", "passed": not data["C007_national_commission_unresolved"].any()},
        {"test": "no_eligible_standalone_meeting", "passed": not data["D001_eligible_standalone_meeting_document"].any()},
        {"test": "no_excluded_substantive_bundle", "passed": not data["D002_excluded_substantive_meeting_bundle"].any()},
        {"test": "no_eligible_standalone_recruitment", "passed": not data["D003_eligible_standalone_recruitment"].any()},
        {"test": "no_excluded_recruitment_analysis", "passed": not data["D004_excluded_recruitment_policy_or_analysis"].any()},
        {"test": "no_eligible_archival_finding_aid", "passed": not data["D005_eligible_archival_finding_aid"].any()},
    ])
    return data, candidates, summary, regressions


def run(input_path: Path = DEFAULT_INPUT, output_root: Path = DEFAULT_OUTPUT_ROOT) -> dict:
    started = datetime.now(timezone.utc)
    stamp = started.strftime("%Y%m%dT%H%M%SZ")
    output = output_root / f"audit_{stamp}"
    output.mkdir(parents=True, exist_ok=False)
    source = pd.read_parquet(input_path)
    audited, candidates, rule_summary, regressions = build_audit(source)

    keep = [
        "record_id", "year", "title", "publisher", "url", "policy_commons_id",
        "document_genre_v2", "document_eligible_v2", "institution_type_v2",
        "published_in_country_code", "issuer_country_v3", "analysis_country_v3",
        "country_decision_source_v3", "audit_flag_count", "audit_rule_ids",
    ]
    candidates[keep].to_csv(output / "audit_candidates.csv.gz", index=False, compression="gzip")
    rule_summary.to_csv(output / "rule_summary.csv", index=False, encoding="utf-8-sig")
    regressions.to_csv(output / "regression_results.csv", index=False, encoding="utf-8-sig")
    audited[["record_id", "audit_information_count", "audit_flag_count", "audit_rule_ids"]].to_parquet(
        output / "record_audit_flags.parquet", index=False, compression="zstd"
    )

    metrics = {
        "audit_version": "full-census-1.0",
        "created_at": started.isoformat(),
        "input": str(input_path),
        "input_sha256": sha256(input_path),
        "records": len(source),
        "records_with_flags": len(candidates),
        "rules": len(rule_summary),
        "regression_tests": len(regressions),
        "regression_tests_passed": int(regressions["passed"].sum()),
        "regression_tests_failed": int((~regressions["passed"]).sum()),
        "automatic_input_changes": 0,
        "output": str(output),
    }
    (output / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    manifest = []
    for path in sorted(output.iterdir()):
        if path.is_file() and path.name != "SHA256SUMS.txt":
            manifest.append(f"{sha256(path)}  {path.name}")
    (output / "SHA256SUMS.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    args = parser.parse_args()
    print(json.dumps(run(args.input, args.output_root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
