#!/usr/bin/env python3
"""Backfill verified CSV companions beside every canonical raw RIS page."""

from __future__ import annotations

import importlib.util
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright


BASE = Path(
    "/Users/deep1003/Library/Mobile Documents/com~apple~CloudDocs/data3/"
    "policy_commons_ai_full_collection_20260910"
)
CANON = BASE / "artificial_intelligence_1950_2026_by_module"
LOG_ROOT = BASE / "output/csv_companion_backfill_20260920"
HELPER = Path("/Users/deep1003/data3/policy_commons_collect_csv_2026_all_modules.py")
CDP = "http://127.0.0.1:9223"

spec = importlib.util.spec_from_file_location("csv_helper", HELPER)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load helper: {HELPER}")
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
common = helper.common


def append(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_page_metadata(ris: Path, module: str, year: int) -> dict:
    page_number = int(ris.stem.rsplit("_", 1)[-1])
    manifest = ris.parent / "manifest.jsonl"
    rows = []
    if manifest.exists():
        for line in manifest.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    exact = [row for row in rows if int(row.get("page", -1)) == page_number]
    source = exact[-1] if exact else (rows[-1] if rows else {})
    partition = source.get("partition") or {}
    query = partition.get("query", common.QUERY)
    artifact_type = partition.get("artifact_type")
    sort = source.get("sort") or partition.get("sort")
    if not sort:
        sort = "date_asc" if "date_asc" in ris.parent.name else "date_desc"
    return {
        "module": source.get("module", module),
        "year": int(source.get("year", year)),
        "page": page_number,
        "query": query,
        "artifact_type": artifact_type,
        "sort": sort,
        "manifest": str(manifest),
    }


def tasks() -> list[tuple[str, int, Path]]:
    found = []
    seen_roots: set[Path] = set()
    for status_path in sorted(CANON.glob("*/[0-9][0-9][0-9][0-9]/STATUS.json")):
        status = json.loads(status_path.read_text(encoding="utf-8"))
        module = status["module_code"]
        year = int(status["year"])
        links = status_path.parent / "_raw_sources"
        if not links.exists():
            continue
        for link in sorted(links.iterdir()):
            if not link.is_symlink():
                continue
            root = link.resolve()
            if root in seen_roots or not root.exists():
                continue
            seen_roots.add(root)
            found.extend((module, year, ris) for ris in sorted(root.rglob("page_*.ris")))
    return sorted(found, key=lambda item: (-item[1], item[0], str(item[2])))


def main() -> None:
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    queue = tasks()
    (LOG_ROOT / "queue_summary.json").write_text(
        json.dumps({"created_at": utc_now(), "ris_pages": len(queue)}, indent=2) + "\n",
        encoding="utf-8",
    )
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = next((p for p in context.pages if "policycommons.net" in p.url), None)
        if page is None:
            page = context.new_page()
        for index, (module, year, ris) in enumerate(queue, 1):
            target = ris.with_suffix(".csv")
            try:
                expected_ids = helper.ris_artifact_ids(ris)
                ris_info = common.inspect_ris(ris)
                if len(expected_ids) != ris_info["records"]:
                    raise RuntimeError(
                        f"RIS artifact IDs {len(expected_ids)} != records {ris_info['records']}"
                    )
                if target.exists():
                    info = helper.inspect_csv(target)
                    if info["artifact_ids"] == expected_ids:
                        print(f"[{index}/{len(queue)}] skip {module} {year} {target.name} {info['records']}", flush=True)
                        continue
                    quarantine = LOG_ROOT / "quarantine" / target.relative_to(BASE)
                    quarantine.parent.mkdir(parents=True, exist_ok=True)
                    target.replace(quarantine)
                meta = load_page_metadata(ris, module, year)
                success = False
                for attempt in range(1, 6):
                    try:
                        url = common.search_url(
                            meta["module"], meta["year"], page_number=meta["page"],
                            sort=meta["sort"], artifact_type=meta["artifact_type"],
                            query=meta["query"],
                        )
                        page.goto(url, wait_until="domcontentloaded", timeout=120_000)
                        page.wait_for_selector(".search-item", timeout=120_000)
                        info = helper.export_csv(page, target, expected_ids)
                        clean_info = {k: v for k, v in info.items() if k != "artifact_ids"}
                        append(LOG_ROOT / "manifest.jsonl", {
                            "module": module, "year": year, "ris": str(ris),
                            "csv": str(target), "join_key": "Policy Commons artifact ID parsed from URL",
                            **clean_info, "at": utc_now(),
                        })
                        print(f"[{index}/{len(queue)}] saved {module} {year} {target.name} {info['records']}", flush=True)
                        success = True
                        break
                    except Exception as exc:
                        target.with_suffix(".csv.part").unlink(missing_ok=True)
                        append(LOG_ROOT / "errors.jsonl", {
                            "module": module, "year": year, "ris": str(ris),
                            "page": meta["page"], "attempt": attempt,
                            "error": repr(exc), "at": utc_now(),
                        })
                        if attempt < 5:
                            time.sleep(10 * attempt)
                if not success:
                    append(LOG_ROOT / "unresolved.jsonl", {
                        "module": module, "year": year, "ris": str(ris),
                        "reason": "five CSV attempts exhausted", "at": utc_now(),
                    })
            except Exception as exc:
                append(LOG_ROOT / "unresolved.jsonl", {
                    "module": module, "year": year, "ris": str(ris),
                    "reason": repr(exc), "at": utc_now(),
                })
                print(f"[{index}/{len(queue)}] unresolved {module} {year} {ris.name}: {exc!r}", flush=True)
            (LOG_ROOT / "checkpoint.json").write_text(
                json.dumps({"index": index, "total": len(queue), "module": module, "year": year, "ris": str(ris), "status": "running", "updated_at": utc_now()}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        (LOG_ROOT / "checkpoint.json").write_text(
            json.dumps({"index": len(queue), "total": len(queue), "status": "complete", "updated_at": utc_now()}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        browser.close()


if __name__ == "__main__":
    main()
