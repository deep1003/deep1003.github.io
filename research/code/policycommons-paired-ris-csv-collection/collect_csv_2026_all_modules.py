#!/usr/bin/env python3
"""Download CSV companions beside the verified 2026 RIS page exports."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import math
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


BASE = Path(
    "/Users/deep1003/Library/Mobile Documents/com~apple~CloudDocs/data3/"
    "policy_commons_ai_full_collection_20260910/output"
)
SOURCE = BASE / "jupyter-notebook/collect_artificial_intelligence_other_modules_1950_2025.py"
ROOT = BASE / "artificial_intelligence_all_modules_2026_20260920"
CDP = "http://127.0.0.1:9223"
MODULES = ("POCO_POGO", "POCO_PCWL", "POCO_POHE", "POCO_PSPL", "POCO_ALL")
MODULE_NAMES = {
    "POCO_POGO": "World Governments",
    "POCO_PCWL": "World Cities",
    "POCO_POHE": "Public Health and Social Care",
    "POCO_PSPL": "N.A. State, Provincial, and Territorial Governments",
    "POCO_ALL": "Global Think Tanks",
}
YEAR = 2026
REQUIRED_COLUMNS = {"type", "title", "url", "publisher", "year", "topics", "country"}

spec = importlib.util.spec_from_file_location("policy_commons_ris_collector", SOURCE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load collector: {SOURCE}")
common = importlib.util.module_from_spec(spec)
spec.loader.exec_module(common)


def inspect_csv(path: Path) -> dict:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig", errors="strict")
    reader = csv.DictReader(io.StringIO(text))
    columns = reader.fieldnames or []
    missing = REQUIRED_COLUMNS.difference(columns)
    if missing:
        raise RuntimeError(f"CSV missing required columns: {sorted(missing)}")
    data = list(reader)
    rows = len(data)
    if rows < 1:
        raise RuntimeError("CSV contains no records")
    artifact_ids = []
    for row in data:
        match = re.search(r"/artifacts/(\d+)/", row.get("url", ""))
        artifact_ids.append(match.group(1) if match else "")
    return {
        "records": rows,
        "columns": columns,
        "artifact_ids": artifact_ids,
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def ris_artifact_ids(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    return re.findall(
        r"(?m)^UR  - https://policycommons\.net/artifacts/(\d+)/", text
    )


def export_csv(page, target: Path, expected_ids: list[str]) -> dict:
    expected = len(expected_ids)
    result = page.evaluate(
        """async () => {
            const results = Array.from(document.querySelectorAll('.search-item'))
                .map(item => ({object_id: item.dataset.id, content_type: item.dataset.type}))
                .filter(item => ['file', 'artifact', 'topic', 'organization']
                    .includes(item.content_type));
            const csrf = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
            const response = await fetch('/api/export/many/', {
                method: 'POST', credentials: 'include',
                headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrf},
                body: JSON.stringify({
                    export_type: 'csv', content_type: 'search', object_id: 0, results,
                }),
            });
            return {status: response.status, text: await response.text(), count: results.length};
        }"""
    )
    if int(result["status"]) != 200:
        raise RuntimeError(f"CSV export HTTP {result['status']}: {result['text'][:500]}")
    rendered_items = int(result["count"])
    url = json.loads(result["text"]).get("url")
    if not url:
        raise RuntimeError("CSV export returned no URL")
    response = page.context.request.get(url, timeout=120_000)
    if not response.ok:
        raise RuntimeError(f"CSV object download HTTP {response.status}")
    partial = target.with_suffix(".csv.part")
    partial.write_bytes(response.body())
    info = inspect_csv(partial)
    if info["records"] != rendered_items:
        raise RuntimeError(
            f"CSV export mismatch rendered={rendered_items} CSV={info['records']}"
        )
    ordered_matches = sum(
        a == b for a, b in zip(info["artifact_ids"], expected_ids)
    )
    overlap = len(set(info["artifact_ids"]) & set(expected_ids))
    if info["artifact_ids"] == expected_ids:
        pair_status = "exact_page_match"
    elif overlap:
        pair_status = "partial_page_overlap"
    else:
        pair_status = "no_page_overlap"
    info.update(
        {
            "pair_status": pair_status,
            "ordered_matches": ordered_matches,
            "set_overlap": overlap,
            "expected_ris_records": expected,
            "rendered_export_items": rendered_items,
        }
    )
    partial.replace(target)
    return info


def main() -> None:
    checkpoint = ROOT / "csv_checkpoint.json"
    errors = ROOT / "csv_errors.jsonl"
    manifest = ROOT / "csv_manifest.jsonl"
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = next((p for p in context.pages if "policycommons.net" in p.url), None)
        if page is None:
            page = context.new_page()
        for candidate in list(context.pages):
            if candidate is not page and candidate.url == "about:blank":
                candidate.close()

        for module in MODULES:
            partitions = common.plan_year(page, context, module, YEAR)
            for partition in partitions:
                folder = ROOT / module / str(YEAR) / partition["label"]
                pages = math.ceil(int(partition["count"]) / 100)
                for number in range(1, pages + 1):
                    ris = folder / f"page_{number:04d}.ris"
                    csv_path = folder / f"page_{number:04d}.csv"
                    if not ris.exists():
                        common.append_jsonl(errors, {"module": module, "year": YEAR, "page": number, "error": "paired RIS missing", "at": common.now()})
                        continue
                    ris_info = common.inspect_ris(ris)
                    expected_ids = ris_artifact_ids(ris)
                    if len(expected_ids) != ris_info["records"]:
                        common.append_jsonl(errors, {"module": module, "year": YEAR, "page": number, "error": f"RIS artifact IDs {len(expected_ids)} != records {ris_info['records']}", "at": common.now()})
                        continue
                    if csv_path.exists():
                        try:
                            info = inspect_csv(csv_path)
                            if info["records"] == ris_info["records"] and info["artifact_ids"] == expected_ids:
                                print(f"[{module} {YEAR} {partition['label']} {number}/{pages}] skip CSV {info['records']}", flush=True)
                                continue
                        except Exception:
                            csv_path.unlink(missing_ok=True)
                    success = False
                    for attempt in range(1, 6):
                        try:
                            url = common.search_url(
                                module, YEAR, page_number=number,
                                sort=partition.get("sort", "date_desc"),
                                artifact_type=partition["artifact_type"],
                                query=partition["query"],
                            )
                            page.goto(url, wait_until="domcontentloaded", timeout=120_000)
                            page.wait_for_selector(".search-item", timeout=120_000)
                            info = export_csv(page, csv_path, expected_ids)
                            manifest_info = {key: value for key, value in info.items() if key != "artifact_ids"}
                            common.append_jsonl(manifest, {"module": module, "module_name": MODULE_NAMES[module], "year": YEAR, "partition": partition, "page": number, **manifest_info, "join_key": "Policy Commons artifact ID parsed from URL", "paired_ris": str(ris.relative_to(ROOT)), "at": common.now()})
                            print(f"[{module} {YEAR} {partition['label']} {number}/{pages}] saved CSV {info['records']}", flush=True)
                            success = True
                            break
                        except Exception as exc:
                            csv_path.with_suffix(".csv.part").unlink(missing_ok=True)
                            common.append_jsonl(errors, {"module": module, "year": YEAR, "partition": partition, "page": number, "attempt": attempt, "error": repr(exc), "at": common.now()})
                            if attempt < 5:
                                time.sleep(10 * attempt)
                    if not success:
                        print(f"[{module} {YEAR} {partition['label']} {number}/{pages}] unresolved CSV", flush=True)
                    checkpoint.write_text(json.dumps({"module": module, "year": YEAR, "partition": partition["label"], "page": number, "status": "running", "updated_at": common.now()}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        checkpoint.write_text(json.dumps({"module": MODULES[-1], "year": YEAR, "status": "complete", "updated_at": common.now()}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        browser.close()


if __name__ == "__main__":
    main()
