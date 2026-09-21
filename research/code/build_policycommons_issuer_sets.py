#!/usr/bin/env python3
"""Preserve identified non-national Policy Commons issuers outside national analysis."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


ROOT = Path('/Users/deep1003/Downloads/policycommons_local_enrichment_20260920_r1')
MASTER = ROOT / 'policycommons_current_master.parquet'
OUTPUT = ROOT / 'issuer_scope_sets_v8_3_20260921'
NEW_PREFIX = 'dl20260921_'

# These strings name national or private organisations, not the IGO/EU issuer.
FALSE_IGO_PUBLISHERS = {
    'Canadian Commission for Unesco',
    'Foreign Policy and United Nations Association of Austria',
    'United Nations Association of USA, Capital Area Division',
    'World Federation of United Nations Associations',
    'The Academic Council on the United Nations System',
}
FALSE_EU_PUBLISHERS = {
    'Ministry of Foreign Affairs, European Union and Cooperation',
    'Department for Exiting the European Union',
}

# Exact issuer names supplement missing institutional classifications. A word
# such as "international" in a title or topic is never enough for inclusion.
IGO_ISSUERS = {
    'Organisation for Economic Co-operation and Development',
    'International Telecommunications Union',
    'Inter-American Development Bank',
    'World Trade Organization',
    'International Energy Agency',
    'International Training Centre of the International Labour Organisation',
    'African Development Bank Group',
}
EU_ISSUERS = {
    'European Parliament',
    'European Commission',
    'European Parliamentary Research Service',
}
PRIVATE_ISSUERS = {
    'Deloitte',
    'KPMG International',
    'Boston Consulting Group',
    'Accenture',
    'Kearney',
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def classify(master: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    publisher = master.publisher.fillna('').astype(str).str.strip()
    previous = master.institution_type_final.fillna('').astype(str)
    recent = master.record_id.astype(str).str.startswith(NEW_PREFIX)

    false_igo = publisher.isin(FALSE_IGO_PUBLISHERS)
    false_eu = publisher.isin(FALSE_EU_PUBLISHERS)
    ambiguous = false_igo | false_eu

    known_igo = set(publisher[previous.eq('international_igo') & ~ambiguous])
    known_eu = set(publisher[previous.eq('supranational_eu') & ~ambiguous])
    igo = (previous.eq('international_igo') | publisher.isin(known_igo | IGO_ISSUERS)) & ~ambiguous
    eu = (previous.eq('supranational_eu') | publisher.isin(known_eu | EU_ISSUERS)) & ~ambiguous
    private = previous.eq('multinational_private') | publisher.isin(PRIVATE_ISSUERS)
    assert not (igo & eu).any()
    assert not ((igo | eu) & private).any()

    international = master.loc[igo | eu].copy()
    international['issuer_set'] = ['supranational_eu' if value else 'international_organisation' for value in eu[igo | eu]]
    international['issuer_set_evidence'] = [
        'exact_issuer_name' if recent.loc[index] or previous.loc[index] not in {'international_igo', 'supranational_eu'}
        else 'previously_classified_issuer'
        for index in international.index
    ]
    international['new_increment_review_required'] = recent.loc[international.index].to_numpy()

    multinational = master.loc[private].copy()
    multinational['issuer_set'] = 'multinational_private'
    multinational['issuer_set_evidence'] = [
        'exact_issuer_name' if recent.loc[index] or previous.loc[index] != 'multinational_private'
        else 'previously_classified_issuer'
        for index in multinational.index
    ]
    multinational['new_increment_review_required'] = recent.loc[multinational.index].to_numpy()

    review = master.loc[ambiguous, ['record_id', 'title', 'publisher', 'url', 'institution_type_final']].copy()
    review['review_reason'] = 'organisation_name_collision_with_international_body'

    assert international.record_id.is_unique and multinational.record_id.is_unique
    assert set(international.record_id).isdisjoint(multinational.record_id)
    assert set(review.record_id).isdisjoint(international.record_id)
    return international, multinational, review


def build() -> dict:
    master = pd.read_parquet(MASTER).fillna('')
    assert len(master) == 270_974 and master.record_id.is_unique
    international, multinational, review = classify(master)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    files = {
        'international_organisations': OUTPUT / 'international_organisations_v8_3.parquet',
        'multinational_private': OUTPUT / 'multinational_private_v8_3.parquet',
        'issuer_name_collision_review': OUTPUT / 'issuer_name_collision_review_v8_3.csv',
    }
    international.to_parquet(files['international_organisations'], index=False)
    multinational.to_parquet(files['multinational_private'], index=False)
    review.to_csv(files['issuer_name_collision_review'], index=False)
    summary = {
        'source_master_rows': len(master),
        'international_organisation_rows': int(international.issuer_set.eq('international_organisation').sum()),
        'supranational_eu_rows': int(international.issuer_set.eq('supranational_eu').sum()),
        'international_total_rows': len(international),
        'multinational_private_rows': len(multinational),
        'new_increment_international_review': int(international.new_increment_review_required.sum()),
        'new_increment_private_review': int(multinational.new_increment_review_required.sum()),
        'issuer_name_collisions_held_out': len(review),
        'master_sha256': digest(MASTER),
        'output_sha256': {name: digest(path) for name, path in files.items()},
        'selection_rule': 'previous institutional class or exact issuer allowlist, with named national/private collisions held out',
    }
    (OUTPUT / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    return summary


if __name__ == '__main__':
    print(json.dumps(build(), indent=2))
