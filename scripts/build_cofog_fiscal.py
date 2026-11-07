"""Fetch and normalise OECD COFOG actual expenditure, preserving source flags."""
import argparse
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import urllib.request

DATAFLOW = 'OECD.SDD.NAD,DSD_NASEC10@DF_TABLE11,1.1'
KEYS = ['A', '', 'S13', '_Z', 'D', 'OTE', '_Z', '_T+' + '+'.join(f'GF{i:02}' for i in range(1, 11)), 'XDC', 'S', 'V', 'N', 'T1100']
URL = 'https://sdmx.oecd.org/public/rest/v1/data/' + DATAFLOW + '/' + '.'.join(KEYS) + '?startPeriod=2000&endPeriod=2025'
FUNCTIONS = ['일반 공공행정', '국방', '공공질서 및 안전', '경제업무', '환경보호', '주택 및 지역사회 편의시설', '보건', '휴양·문화·종교', '교육', '사회보호']
KOREAN = dict(KOR='한국', USA='미국', GBR='영국', DEU='독일', FRA='프랑스', JPN='일본', AUS='호주', CAN='캐나다', ITA='이탈리아', ESP='스페인', SWE='스웨덴', NOR='노르웨이', DNK='덴마크', FIN='핀란드', NLD='네덜란드', CHE='스위스', AUT='오스트리아', BEL='벨기에', POL='폴란드', CZE='체코', HUN='헝가리', PRT='포르투갈', GRC='그리스', IRL='아일랜드', ISL='아이슬란드', ISR='이스라엘', LUX='룩셈부르크', EST='에스토니아', LVA='라트비아', LTU='리투아니아', SVK='슬로바키아', SVN='슬로베니아', COL='콜롬비아', CRI='코스타리카', CHL='칠레', ROU='루마니아', BGR='불가리아', HRV='크로아티아')
AGGREGATES = {'EU', 'EU27_2020', 'EA20'}


def code(value):
    return value.split(': ', 1)[0]


def build(destination, fetch):
    destination.mkdir(parents=True, exist_ok=True)
    raw_path = destination / 'oecd_cofog_source_20261107.csv'
    if fetch:
        request = urllib.request.Request(URL, headers={'Accept': 'text/csv;labels=both'})
        with urllib.request.urlopen(request, timeout=120) as response:
            raw_path.write_bytes(response.read())
    raw = raw_path.read_bytes()
    records = []
    countries = {}
    unique_keys = set()
    totals = {}
    for source in csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))):
        row = {key.split(':')[0]: value for key, value in source.items()}
        country = code(row['REF_AREA'])
        if country in AGGREGATES:
            continue
        year = int(code(row['TIME_PERIOD']))
        function = code(row['EXPENDITURE'])
        key = (country, year, function)
        assert key not in unique_keys, key
        unique_keys.add(key)
        assert code(row['SECTOR']) == 'S13'
        assert code(row['TRANSACTION']) == 'OTE'
        assert code(row['PRICE_BASE']) == 'V'
        amount = float(row['OBS_VALUE']) * 10 ** (int(code(row['UNIT_MULT'])) - 6)
        item = dict(country=country, year=year, function=function, amount=amount,
                    currency=code(row['CURRENCY']), status=code(row['OBS_STATUS']))
        records.append(item)
        countries[country] = dict(code=country, name=KOREAN.get(country, row['REF_AREA'].split(': ', 1)[-1]),
                                  english=row['REF_AREA'].split(': ', 1)[-1])
        if function == '_T':
            totals[country, year] = item
    observations = []
    missing_denominators = []
    for item in records:
        if item['function'] == '_T':
            continue
        total = totals.get((item['country'], item['year']))
        item['share'] = item['amount'] / total['amount'] * 100 if total and total['amount'] > 0 else None
        item['total_status'] = total['status'] if total else None
        if item['share'] is None:
            missing_denominators.append([item['country'], item['year'], item['function']])
        observations.append(item)
    grouped = collections.defaultdict(list)
    for item in observations:
        grouped[item['country'], item['year']].append(item)
    reconciliations = []
    for key, values in grouped.items():
        if len(values) == 10 and key in totals:
            difference = sum(item['amount'] for item in values) - totals[key]['amount']
            relative = abs(difference) / totals[key]['amount'] if totals[key]['amount'] else 0
            reconciliations.append(dict(country=key[0], year=key[1], difference_millions=difference, relative_difference=relative))
    assert not missing_denominators
    assert all(item['relative_difference'] < 0.0001 for item in reconciliations)
    for country in countries.values():
        country['years'] = sorted({item['year'] for item in observations if item['country'] == country['code']})
        country['currency'] = next(item['currency'] for item in observations if item['country'] == country['code'])
    data = dict(retrieved_on='2026-11-07', source='OECD Annual government expenditure by function (COFOG)',
                source_api=URL, source_sha256=hashlib.sha256(raw).hexdigest(),
                sector='S13 general government', transaction='OTE total government expenditure',
                amount_unit='millions of national currency, current prices',
                share_definition='100 * function expenditure / total general government expenditure, same country and year',
                exclusions=sorted(AGGREGATES), countries=sorted(countries.values(), key=lambda value: (value['code'] != 'KOR', value['english'])),
                functions=[dict(code=f'GF{i:02}', name=name) for i, name in enumerate(FUNCTIONS, 1)],
                rows=sorted(observations, key=lambda item: (item['country'], item['year'], item['function'])),
                status_labels={'A':'정상 관측값', 'P':'잠정값', 'B':'시계열 단절', 'E':'추정값'})
    (destination / 'cofog_expenditure_20261107.json').write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n')
    with (destination / 'cofog_expenditure_20261107.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(observations[0]))
        writer.writeheader()
        writer.writerows(data['rows'])
    coverage = [dict(country=country['code'], name=country['name'], first_year=min(country['years']), last_year=max(country['years']), years=len(country['years'])) for country in data['countries']]
    validation = dict(countries=len(countries), observations=len(observations), years=sorted({item['year'] for item in observations}),
                      unique_country_year_function=True, missing_denominators=missing_denominators,
                      full_ten_function_country_years=len(reconciliations), max_relative_reconciliation_error=max(item['relative_difference'] for item in reconciliations),
                      flags=dict(collections.Counter(item['status'] for item in observations)), coverage=coverage)
    (destination / 'validation_20261107.json').write_text(json.dumps(validation, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(validation, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--fetch', action='store_true')
    args = parser.parse_args()
    build(args.destination, args.fetch)
