from html import escape
from pathlib import Path

import pyarrow.parquet as pq


SOURCE = Path("/Users/deep1003/Downloads/policycommons_local_enrichment_20260920_r1/final_augmented_release_v7_10_fulltext_ai_corrections/policycommons_augmented_master_final_v7_10.parquet")
OUTPUT = Path(__file__).resolve().parents[2] / "policy-commons-ris-data-dictionary.html"


EXACT = {
    "record_id": ("Identity", "Internal canonical document-version identifier."),
    "policy_commons_id": ("Identity", "Persistent Policy Commons content identifier exported in RIS."),
    "ris_record_id": ("Identity", "Identifier retained from the canonical RIS record."),
    "join_coi": ("Identity", "Normalised persistent content identifier used for conservative RIS–CSV linkage."),
    "join_artifact_id": ("Identity", "Numeric Policy Commons artefact identifier parsed from the artefact URL."),
    "url": ("Bibliographic metadata", "Canonical or best available Policy Commons artefact-page URL."),
    "coilink_url": ("Bibliographic metadata", "COI resolver URL associated with the Policy Commons identifier."),
    "title": ("Bibliographic metadata", "Canonical document title."),
    "abstract": ("Bibliographic metadata", "Provider-supplied or provider-generated abstract or summary."),
    "abstract_hash": ("Identity", "Hash of the normalised abstract used for integrity and contamination checks."),
    "year": ("Bibliographic metadata", "Best normalised publication year retained by the release."),
    "year_type": ("Bibliographic metadata", "Evidence class or derivation method for the year value."),
    "year_band": ("Audit and sampling", "Year stratum used for diagnostics and stratified validation."),
    "year_in_scope": ("Eligibility", "Whether the year falls within the analysis period."),
    "publisher": ("Bibliographic metadata", "Recorded publisher or issuing organisation string."),
    "publisher_key": ("Institution", "Normalised publisher key used for authority matching."),
    "authors": ("Bibliographic metadata", "Authors or organisational contributors retained from RIS."),
    "people": ("Bibliographic metadata", "Contributor values supplied by the CSV export."),
    "affiliations": ("Bibliographic metadata", "Author or contributor affiliation values when available."),
    "language": ("Bibliographic metadata", "Exported document language or languages."),
    "keywords": ("Bibliographic metadata", "RIS keywords, kept separate from Policy Commons Topics."),
    "topics": ("CSV enrichment", "Policy Commons Topics supplied by the CSV export."),
    "topics_combined": ("CSV enrichment", "Order-preserving union of RIS keywords and CSV Topics."),
    "doi": ("Bibliographic metadata", "External DOI when supplied; distinct from the Policy Commons identifier."),
    "isbn": ("Bibliographic metadata", "ISBN supplied by RIS or CSV."),
    "issn": ("Bibliographic metadata", "ISSN supplied by RIS or CSV."),
    "type": ("Bibliographic metadata", "Provider CSV object class."),
    "ris_type": ("Bibliographic metadata", "Original RIS reference type from TY."),
    "publication_type": ("Bibliographic metadata", "Normalised publication-type value when available."),
    "content_type": ("Bibliographic metadata", "Normalised content-type value when available."),
    "place_published": ("Country evidence", "Exported publication place; not automatically the issuer country."),
    "country": ("Country evidence", "Raw provider country value, normally code plus country name."),
    "published_in_country_code": ("Country evidence", "Country code parsed from the provider Published in field."),
    "published_in_country_name": ("Country evidence", "Country name parsed from the provider Published in field."),
    "issuer_country": ("Country attribution", "Country or countries attributed to the issuing institution in the base classification."),
    "target_country": ("Country attribution", "Country discussed, targeted or covered by the document; not issuer provenance."),
    "CTRY": ("Country attribution", "Single analytical issuer-country code where one eligible jurisdiction is resolved."),
    "analysis_country": ("Country attribution", "Base whole-count analytical country assignment."),
    "analysis_country_count": ("Country attribution", "Number of distinct countries in the base analytical assignment."),
    "country": ("Country evidence", "Raw country value from the paired CSV or inherited Golden Set record."),
    "institution_type": ("Institution", "Base normalised class of the issuer or publisher."),
    "collection_categories": ("Provenance", "All collection categories linked to the canonical record."),
    "collection_provenance": ("Provenance", "Search and collection history supporting inclusion."),
    "query": ("Provenance", "Exact or representative search expression associated with the record."),
    "query_id": ("Provenance", "Short identifier for the search contract."),
    "source_file": ("Provenance", "Representative source file selected for the canonical record."),
    "source_ordinal": ("Provenance", "Record position within the representative source file."),
    "observation_id": ("Provenance", "Stable identifier for the representative source observation."),
    "observation_count": ("Provenance", "Number of observations linked to the canonical record."),
    "source_observation_count": ("Provenance", "Count of source observations represented by the row."),
    "csv_observation_count": ("RIS–CSV linkage", "Number of CSV observations sharing the accepted linkage key."),
    "csv_source_files": ("RIS–CSV linkage", "CSV files contributing fields to the canonical record."),
    "csv_source_category": ("RIS–CSV linkage", "Collection category attached to the CSV source."),
    "pairing_status": ("RIS–CSV linkage", "RIS–CSV linkage outcome, including paired and format-only states."),
    "raw_fields_json": ("Provenance", "Loss-preserving JSON representation of original repeated RIS fields."),
    "master_origin": ("Release", "Whether the record originated in the Golden Set or local augmentation."),
    "augmentation_status": ("Release", "Status assigned during Golden Set augmentation."),
    "golden_membership": ("Release", "Whether the record is a preserved Golden Set member."),
    "golden_record_id": ("Release", "Matched Golden Set record identifier when present."),
    "golden_match_status": ("Release", "Outcome of matching the local record to the Golden Set."),
    "golden_set_version": ("Release", "Golden Set version from which the record or schema originated."),
    "release_version": ("Release", "Version label of the augmented release."),
    "identity_status": ("Identity", "Canonicalisation, duplicate or identity-review status."),
    "classification_status": ("Classification", "Overall classification completion or review state."),
    "format_status": ("Document form", "Availability and structural status of RIS, CSV or paired metadata."),
    "document_genre": ("Document form", "Base normalised document genre."),
    "document_eligible": ("Document form", "Base eligibility flag for substantive document analysis."),
    "genre_reason": ("Document form", "Rule or evidence supporting the base genre decision."),
    "human_validation_status": ("Review", "Original-source or human-adjudication status."),
    "original_source_verified": ("Review", "Whether the original page or document was directly checked."),
    "quality_review_required": ("Review", "Flag indicating that a record needs quality review."),
    "quality_reason": ("Review", "Reason a record entered the quality-review queue."),
    "risk_band": ("Audit and sampling", "Risk stratum used for review and validation."),
    "audit_stratum": ("Audit and sampling", "Frozen sampling stratum assigned for audit."),
}


def describe(name: str):
    if name in EXACT:
        return EXACT[name]
    if name.startswith("ai_"):
        if "evidence" in name:
            return "AI relevance", f"AI evidence field retained by the {name.removeprefix('ai_').replace('_', ' ')} step."
        if "include" in name:
            return "AI relevance", "Versioned high-recall inclusion flag; metadata absence alone is not a negative decision."
        if "decision" in name or "label" in name or "relevance" in name or "scope" in name:
            return "AI relevance", "Versioned AI-relevance classification or scope value."
        if "reason" in name:
            return "AI relevance", "Rule or evidence explanation for the corresponding AI decision."
        return "AI relevance", "Versioned AI-screening output preserved for audit."
    if name.startswith("analysis_country_before_") or name.startswith("issuer_country_before_"):
        return "Country history", "Country value preserved immediately before the named correction or exclusion stage."
    if name.startswith("analysis_country_count"):
        return "Country attribution", "Number of distinct analytical countries at the named release stage."
    if name.startswith("analysis_country"):
        return "Country attribution", "Whole-count analytical country assignment at the named release stage."
    if name.startswith("issuer_country"):
        return "Country attribution", "Issuer-country value or automated normalisation at the named release stage."
    if name.startswith("country_analysis_eligible"):
        return "Eligibility", "Versioned flag for inclusion in national country-level analysis."
    if name.startswith("country_") or name.startswith("provider_country") or name.startswith("publisher_rule_country"):
        return "Country attribution", "Evidence, rule, confidence or status used in country resolution."
    if name.startswith("policycommons_live_country"):
        return "Live-page verification", "Value, field, URL or timestamp captured from direct Policy Commons page verification."
    if name.startswith("document_genre") or name.startswith("document_eligible") or name.startswith("genre_reason"):
        return "Document form", "Versioned document-genre, eligibility or supporting-reason field."
    if name.startswith("document_form_review") or name.startswith("human_form_review"):
        return "Document-form review", "Human-review outcome or rule from the document-form validation release."
    if name.startswith("institution_type"):
        return "Institution", "Versioned issuer or publisher institution classification or applied rule."
    if name.startswith("precision_"):
        return "Precision cleaning", "Status, rule or exclusion class from a precision-cleaning round."
    if name.startswith("round2_"):
        return "Country review", "Rule or classification outcome from the second live-review round."
    if name.startswith("changed_") or name == "v1_error_corrected":
        return "Change audit", "Flag recording whether the value changed between named release versions."
    if name.startswith("national_policy_interest"):
        return "Policy eligibility", "National policy-interest scope or the rule supporting that decision."
    if name.startswith("live_validation"):
        return "Live-page verification", "Rule or exclusion class recorded during live-page validation."
    if name.startswith("precision_round"):
        return "Precision cleaning", "Status or rule from the named precision review round."
    return "Other audit field", "Versioned field retained by the augmented-master pipeline for reproducibility and audit."


schema = pq.read_schema(SOURCE)
groups = {}
for field in schema:
    group, definition = describe(field.name)
    groups.setdefault(group, []).append((field.name, str(field.type), definition))

tables = []
for group, rows in groups.items():
    body = "".join(
        f"<tr><td><code>{escape(name)}</code></td><td>{escape(dtype)}</td><td>{escape(definition)}</td></tr>"
        for name, dtype, definition in rows
    )
    tables.append(f"<details><summary><strong>{escape(group)}</strong> ({len(rows)} variables)</summary><div class='table-scroll'><table class='audit'><thead><tr><th>Variable</th><th>Stored type</th><th>Definition</th></tr></thead><tbody>{body}</tbody></table></div></details>")

html = f"""<!DOCTYPE html><html lang='en-GB'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1.0'>
<title>Policy Commons Augmented Master v7.10 Data Dictionary | Youngsam Chun</title><meta name='description' content='Complete 162-variable dictionary for the Policy Commons augmented master v7.10.'>
<link rel='stylesheet' href='assets/style.css?v=4'><style>.dictionary-wrap{{max-width:1260px;margin:0 auto;padding:42px 28px 80px}}.dictionary-wrap h1{{font-size:28px}}.notice{{background:var(--accent-dim);border-left:4px solid var(--accent);padding:13px 16px;margin:20px 0}}details{{margin:12px 0;border:1px solid var(--rule);padding:10px 12px}}summary{{cursor:pointer}}.table-scroll{{overflow-x:auto;margin-top:10px}}table.audit{{width:100%;border-collapse:collapse;font-size:13px}}table.audit th,table.audit td{{padding:8px 9px;border-bottom:1px solid var(--rule);text-align:left;vertical-align:top}}table.audit th{{background:#f6f7f9}}code{{white-space:nowrap}}</style></head><body>
<nav class='topbar'><div class='topbar-inner'><span class='brand'>Youngsam Chun</span><a class='nav' href='index.html'>About</a><a class='nav active' href='research.html'>Research</a></div></nav>
<main class='dictionary-wrap'><p class='small'><a href='research/policycommons-ris-collection.html'>Collection and cleaning workflow</a> / Data dictionary</p>
<h1>Policy Commons augmented master v7.10 data dictionary</h1>
<p>The dictionary is generated from the physical Parquet schema of <code>policycommons_augmented_master_final_v7_10.parquet</code>. It describes all {len(schema.names)} stored columns. The master grain is one canonical document version; country-level analysis uses the separate document-country file and unique <code>(record_id, analysis_country)</code> rows.</p>
<div class='notice'><strong>Interpretation.</strong> Base, intermediate and final fields coexist deliberately. Historical fields preserve the effect of each correction round. For current analysis, use the fields marked <code>final</code> together with the release-specific eligibility variables and retain raw provider evidence separately.</div>
{''.join(tables)}
<p class='small'>Generated directly from the v7.10 Parquet schema. Schema order is preserved within each semantic group.</p>
<footer>© 2026 Youngsam Chun · <a href='research.html'>Return to Research</a></footer></main></body></html>"""
OUTPUT.write_text(html, encoding="utf-8")
print(f"wrote {OUTPUT} with {len(schema.names)} variables in {len(groups)} groups")
