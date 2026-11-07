"""Build a public aggregate inventory without exporting source records."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path


def build(source, destination):
    destination.mkdir(parents=True, exist_ok=True)
    groups = collections.defaultdict(collections.Counter)
    identifiers = set()
    rows = 0
    with source.open(encoding='utf-8-sig', newline='') as handle:
        for record in csv.DictReader(handle):
            rows += 1
            identifiers.add(record['id'])
            group = groups[record['country'].strip() or '(missing)']
            group['records'] += 1
            unit = record['integration_observation_unit'].strip()
            group[unit if unit in {'document', 'event', 'initiative'} else 'unspecified'] += 1
            year = record['year'].strip()
            if year.isdigit():
                group['min_year'] = min(group.get('min_year', int(year)), int(year))
                group['max_year'] = max(group.get('max_year', int(year)), int(year))
            else:
                group['missing_year'] += 1
    fields = ['country_label', 'records', 'document', 'event', 'initiative', 'unspecified', 'min_year', 'max_year', 'missing_year']
    inventory = [dict(country_label=label, **{key: counts.get(key, 0) for key in fields[1:]})
                 for label, counts in sorted(groups.items(), key=lambda item: (-item[1]['records'], item[0]))]
    assert sum(row['records'] for row in inventory) == rows
    assert all(row['records'] == sum(row[key] for key in ['document', 'event', 'initiative', 'unspecified']) for row in inventory)
    with (destination / 'country_inventory_20261107.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(inventory)
    with source.open('rb') as handle:
        digest = hashlib.file_digest(handle, 'sha256').hexdigest()
    manifest = {'generated_on': '2026-11-07', 'input_snapshot': 'output/korea_expanded_reanalysis_20260907/approved_input.csv',
                'input_sha256': digest, 'rows': rows, 'unique_ids': len(identifiers),
                'country_field': 'country', 'country_labels_not_harmonized': True,
                'observation_unit_field': 'integration_observation_unit',
                'filters': 'none; inventory of the historical candidate input, not a final AI policy document set',
                'totals': {key: sum(row[key] for row in inventory) for key in ['records', 'document', 'event', 'initiative', 'unspecified', 'missing_year']},
                'country_inventory': inventory}
    (destination / 'country_inventory_20261107.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: manifest[key] for key in ['rows', 'unique_ids', 'totals']}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    build(args.source, args.destination)
