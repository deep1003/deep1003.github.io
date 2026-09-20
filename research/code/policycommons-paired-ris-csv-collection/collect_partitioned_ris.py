#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
import re
import string
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

from playwright.sync_api import sync_playwright


ROOT = (
    Path.home()
    / "Library/Mobile Documents/com~apple~CloudDocs/data3"
    / "policy_commons_ai_full_collection_20260910/output"
    / "artificial_intelligence_other_modules_1950_2025_20260917"
)
CDP = "http://127.0.0.1:9223"
QUERY = "artificial intelligence"
MODULES = (
    "POCO_POHE",  # Public Health and Social Care
    "POCO_PSPL",  # N.A. State, Provincial, and Territorial Governments
    "POCO_ALL",   # Global Think Tanks
)
MODULE_NAMES = {
    "POCO_POHE": "Public Health and Social Care",
    "POCO_PSPL": "N.A. State, Provincial, and Territorial Governments",
    "POCO_ALL": "Global Think Tanks",
}
YEARS = (2025, *range(2023, 1949, -1))
MAX_RESULTS = 10_000
PREFIX_ALPHABET = string.ascii_lowercase + string.digits


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def inspect_ris(path: Path) -> dict:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig", errors="replace")
    ty = len(re.findall(r"(?m)^TY  - ", text))
    er = len(re.findall(r"(?m)^ER  -\s*$", text))
    if not ty or ty != er:
        raise RuntimeError(f"invalid RIS TY={ty} ER={er}")
    return {
        "records": ty,
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def search_url(
    module: str,
    year: int,
    page_number: int = 1,
    sort: str = "date_desc",
    artifact_type: str | None = None,
    query: str = QUERY,
) -> str:
    params: list[tuple[str, str | int]] = [
        ("q", query),
        ("searchType", "logical"),
        ("advanced", "yes"),
        ("limit", 100),
        ("sort", sort),
        ("modules", module),
        ("year", year),
        ("page", page_number),
    ]
    if artifact_type:
        params.append(("artifact_type", artifact_type))
    return "https://policycommons.net/search/?" + urlencode(params)


def count_results(page, url: str) -> int:
    last_error: Exception | None = None
    for attempt in range(1, 6):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=120_000)
            body = page.locator("body").inner_text(timeout=30_000)
            if "Search timed out" in body:
                raise RuntimeError("Policy Commons search timed out")
            capped = re.search(r"([\d,]+)\+\s+results?", body)
            if capped:
                # The UI deliberately hides the exact total above the export cap.
                # A sentinel above MAX_RESULTS is sufficient to trigger splitting.
                return MAX_RESULTS + 1
            match = re.search(r"([\d,]+)\s+results?", body)
            if match:
                return int(match.group(1).replace(",", ""))
            if "We couldn't find anything matching your search query" in body:
                return 0
            raise RuntimeError("result count unavailable")
        except Exception as exc:
            last_error = exc
            if attempt < 5:
                time.sleep(5 * attempt)
    raise RuntimeError(f"count failed after retries: {last_error!r}")


def facet_values(context, url: str, facet_type: str) -> list[dict]:
    facet_url = url.replace("/search/?", "/api/search/facet/?")
    facet_url += "&facet_type=" + facet_type
    response = context.request.get(facet_url, timeout=120_000)
    if not response.ok:
        raise RuntimeError(f"facet request failed HTTP {response.status}")
    return response.json()


def safe_slug(value: str, limit: int = 90) -> str:
    clean = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_")
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:10]
    return f"{clean[:limit]}_{digest}" if clean else digest


def prefixed_query(prefix: str, parent_query: str = QUERY) -> str:
    return f"({parent_query}) AND title:{prefix}*"


def residual_query(prefix: str, parent_query: str = QUERY) -> str:
    children = " OR ".join(f"title:{prefix}{char}*" for char in PREFIX_ALPHABET)
    required = f" AND title:{prefix}*" if prefix else ""
    return f"({parent_query}){required} AND NOT ({children})"


def existing_cutoff_date(module: str, year: int, artifact_type: str) -> str | None:
    label = safe_slug(artifact_type)
    page_100 = ROOT / module / str(year) / label / "page_0100.ris"
    if not page_100.exists():
        return None
    text = page_100.read_text(encoding="utf-8-sig", errors="replace")
    dates = re.findall(r"(?m)^DA  - (\d{4}-\d{2}-\d{2})\s*$", text)
    return min(dates) if dates else None


def split_by_publication_date(
    page, module: str, year: int, artifact_type: str, parent_query: str
) -> list[dict]:
    cutoff = existing_cutoff_date(module, year, artifact_type)
    cutoff_month = int(cutoff[5:7]) if cutoff else 13
    month_numbers = list(range(1, cutoff_month))
    queries: list[tuple[str, str]] = []
    for month in month_numbers:
        queries.append(
            (f"{year}-{month:02d}", f"({parent_query}) AND published:{year}-{month:02d}*")
        )
    if cutoff:
        queries.append((cutoff, f"({parent_query}) AND published:{cutoff}*"))

    partitions: list[dict] = []
    for label, query in queries:
        count = count_results(
            page,
            search_url(module, year, artifact_type=artifact_type, query=query),
        )
        if not count:
            continue
        if count <= MAX_RESULTS:
            partitions.append({"query": query, "count": count, "date_label": label})
            continue
        for day in range(1, 32):
            day_label = f"{label}-{day:02d}"
            day_query = f"({parent_query}) AND published:{day_label}*"
            day_count = count_results(
                page,
                search_url(
                    module, year, artifact_type=artifact_type, query=day_query
                ),
            )
            if day_count:
                if day_count > 2 * MAX_RESULTS:
                    raise RuntimeError(
                        f"daily partition above two-sided limit: {module} {day_label} "
                        f"{artifact_type} count={day_count}"
                    )
                if day_count > MAX_RESULTS:
                    partitions.append(
                        {
                            "query": day_query,
                            "count": MAX_RESULTS,
                            "date_label": day_label + "_newest",
                            "sort": "date_desc",
                        }
                    )
                    partitions.append(
                        {
                            "query": day_query,
                            "count": day_count - MAX_RESULTS,
                            "date_label": day_label + "_oldest",
                            "sort": "date_asc",
                        }
                    )
                    continue
                partitions.append(
                    {"query": day_query, "count": day_count, "date_label": day_label}
                )
    if not partitions:
        raise RuntimeError(
            f"no date partitions generated: {module} {year} {artifact_type}"
        )
    return partitions


def split_large_partition(
    page,
    module: str,
    year: int,
    artifact_type: str,
    parent_query: str,
    prefix: str = "",
    depth: int = 0,
) -> list[dict]:
    if depth > 5:
        raise RuntimeError(
            f"title-prefix partition remained above {MAX_RESULTS}: "
            f"{module} {year} {artifact_type} {prefix!r}"
        )
    partitions: list[dict] = []
    previous_siblings: list[str] = []
    for char in PREFIX_ALPHABET:
        child_prefix = prefix + char
        child_clause = f"title:{child_prefix}*"
        if previous_siblings:
            excluded = " OR ".join(previous_siblings)
            child_query = f"({parent_query}) AND {child_clause} AND NOT ({excluded})"
        else:
            child_query = f"({parent_query}) AND {child_clause}"
        url = search_url(module, year, artifact_type=artifact_type, query=child_query)
        count = count_results(page, url)
        if not count:
            continue
        if count <= MAX_RESULTS:
            partitions.append(
                {"query": child_query, "count": count, "prefix": child_prefix}
            )
        else:
            partitions.extend(
                split_large_partition(
                    page,
                    module,
                    year,
                    artifact_type,
                    child_query,
                    child_prefix,
                    depth + 1,
                )
            )
        previous_siblings.append(child_clause)
    children = " OR ".join(f"title:{prefix}{char}*" for char in PREFIX_ALPHABET)
    remainder = f"({parent_query}) AND NOT ({children})"
    remainder_count = count_results(
        page,
        search_url(module, year, artifact_type=artifact_type, query=remainder),
    )
    if remainder_count:
        if remainder_count > MAX_RESULTS:
            if remainder_count > 2 * MAX_RESULTS:
                raise RuntimeError(
                    f"unpartitioned title residual above two-sided limit: "
                    f"{module} {year} {artifact_type} {prefix!r} "
                    f"count={remainder_count}"
                )
            partitions.extend(
                [
                    {
                        "query": remainder,
                        "count": MAX_RESULTS,
                        "prefix": prefix + "_residual_newest",
                        "sort": "date_desc",
                    },
                    {
                        "query": remainder,
                        "count": remainder_count - MAX_RESULTS,
                        "prefix": prefix + "_residual_oldest",
                        "sort": "date_asc",
                    },
                ]
            )
        else:
            partitions.append(
                {
                    "query": remainder,
                    "count": remainder_count,
                    "prefix": prefix + "_residual",
                }
            )
    return partitions


def plan_year(page, context, module: str, year: int) -> list[dict]:
    artifact_type = "document:Document"
    base_url = search_url(module, year, artifact_type=artifact_type)
    total = count_results(page, base_url)
    if total == 0:
        return []
    if total <= MAX_RESULTS:
        return [
            {
                "query": QUERY,
                "artifact_type": artifact_type,
                "count": total,
                "label": safe_slug(artifact_type),
            }
        ]

    plan: list[dict] = []
    for part in split_large_partition(page, module, year, artifact_type, QUERY):
        plan.append(
            {
                "query": part["query"],
                "artifact_type": artifact_type,
                "count": part["count"],
                "sort": part.get("sort", "date_desc"),
                "label": safe_slug(
                    artifact_type + "_title_partition_" + part["prefix"]
                ),
            }
        )
    return plan


def download_partition(page, module: str, year: int, partition: dict) -> None:
    partition_dir = ROOT / module / str(year) / partition["label"]
    partition_dir.mkdir(parents=True, exist_ok=True)
    manifest = partition_dir / "manifest.jsonl"
    errors = partition_dir / "errors.jsonl"
    pages = math.ceil(int(partition["count"]) / 100)
    for number in range(1, pages + 1):
        target = partition_dir / f"page_{number:04d}.ris"
        partial = target.with_suffix(".ris.part")
        non_exportable = partition_dir / f"page_{number:04d}.non_exportable.json"
        if target.exists():
            try:
                info = inspect_ris(target)
                print(
                    f"[{module} {year} {partition['label']} {number}/{pages}] "
                    f"skip {info['records']}",
                    flush=True,
                )
                continue
            except Exception as exc:
                append_jsonl(
                    errors,
                    {
                        "module": module,
                        "year": year,
                        "partition": partition,
                        "page": number,
                        "error": f"invalid existing file removed: {exc!r}",
                        "at": now(),
                    },
                )
                target.unlink(missing_ok=True)
        if non_exportable.exists():
            print(
                f"[{module} {year} {partition['label']} {number}/{pages}] "
                "skip previously verified non-exportable page",
                flush=True,
            )
            continue
        success = False
        for attempt in range(1, 6):
            try:
                partial.unlink(missing_ok=True)
                url = search_url(
                    module,
                    year,
                    page_number=number,
                    sort=partition.get("sort", "date_desc"),
                    artifact_type=partition["artifact_type"],
                    query=partition["query"],
                )
                response = page.goto(
                    url, wait_until="domcontentloaded", timeout=120_000
                )
                page.wait_for_selector(".search-item", timeout=120_000)
                item_types = page.locator(".search-item").evaluate_all(
                    """items => items.reduce((counts, item) => {
                        const type = item.dataset.type || 'unknown';
                        counts[type] = (counts[type] || 0) + 1;
                        return counts;
                    }, {})"""
                )
                exportable_count = sum(
                    int(item_types.get(kind, 0))
                    for kind in ("file", "artifact", "topic", "organization")
                )
                if exportable_count == 0:
                    payload = {
                        "module": module,
                        "module_name": MODULE_NAMES[module],
                        "year": year,
                        "partition_label": partition["label"],
                        "partition": partition,
                        "page": number,
                        "item_types": item_types,
                        "reason": "page contains no RIS-supported item types",
                        "http": response.status if response else None,
                        "at": now(),
                    }
                    non_exportable.write_text(
                        json.dumps(payload, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )
                    append_jsonl(ROOT / "non_exportable_pages.jsonl", payload)
                    print(
                        f"[{module} {year} {partition['label']} {number}/{pages}] "
                        f"no RIS-supported records {item_types}; skipped",
                        flush=True,
                    )
                    success = True
                    break
                export_result = page.evaluate(
                    """async () => {
                        const results = Array.from(document.querySelectorAll('.search-item'))
                            .map(item => ({
                                object_id: item.dataset.id,
                                content_type: item.dataset.type,
                            }))
                            .filter(item => ['file', 'artifact', 'topic', 'organization']
                                .includes(item.content_type));
                        const csrf = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
                        const response = await fetch('/api/export/many/', {
                            method: 'POST',
                            credentials: 'include',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrf,
                            },
                            body: JSON.stringify({
                                export_type: 'ris',
                                content_type: 'search',
                                object_id: 0,
                                results,
                            }),
                        });
                        const text = await response.text();
                        return {status: response.status, text, count: results.length};
                    }"""
                )
                if int(export_result["status"]) != 200:
                    raise RuntimeError(
                        f"export API HTTP {export_result['status']}: "
                        f"{export_result['text'][:500]}"
                    )
                export_payload = json.loads(export_result["text"])
                export_url = export_payload.get("url")
                if not export_url:
                    raise RuntimeError("export API returned no download URL")
                file_response = page.context.request.get(export_url, timeout=120_000)
                if not file_response.ok:
                    raise RuntimeError(
                        f"RIS object download HTTP {file_response.status}"
                    )
                partial.write_bytes(file_response.body())
                info = inspect_ris(partial)
                if info["records"] != exportable_count:
                    raise RuntimeError(
                        f"RIS record mismatch expected={exportable_count} "
                        f"actual={info['records']}"
                    )
                partial.replace(target)
                append_jsonl(
                    manifest,
                    {
                        "module": module,
                        "module_name": MODULE_NAMES[module],
                        "year": year,
                        "partition": partition,
                        "page": number,
                        **info,
                        "http": response.status if response else None,
                        "at": now(),
                    },
                )
                print(
                    f"[{module} {year} {partition['label']} {number}/{pages}] "
                    f"saved {info['records']}",
                    flush=True,
                )
                success = True
                break
            except Exception as exc:
                partial.unlink(missing_ok=True)
                append_jsonl(
                    errors,
                    {
                        "module": module,
                        "year": year,
                        "partition": partition,
                        "page": number,
                        "attempt": attempt,
                        "error": repr(exc),
                        "at": now(),
                    },
                )
                if attempt < 5:
                    time.sleep(10 * attempt)
        if not success:
            append_jsonl(
                ROOT / "unresolved_pages.jsonl",
                {
                    "module": module,
                    "module_name": MODULE_NAMES[module],
                    "year": year,
                    "partition_label": partition["label"],
                    "partition": partition,
                    "page": number,
                    "status": "needs_separate_retry",
                    "reason": "RIS download did not start after 5 attempts",
                    "at": now(),
                },
            )
            print(
                f"[{module} {year} {partition['label']} {number}/{pages}] "
                "recorded as unresolved; continuing main sweep",
                flush=True,
            )
            continue
        time.sleep(4)


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    plan_log = ROOT / "partition_plan.jsonl"
    checkpoint = ROOT / "checkpoint.json"
    completed_module: str | None = None
    completed_year: int | None = None
    if checkpoint.exists():
        try:
            state = json.loads(checkpoint.read_text(encoding="utf-8"))
            completed_module = state.get("last_completed_module")
            completed_year = int(state["last_completed_year"])
            if state.get("status") == "complete":
                print("Collection already complete", flush=True)
                return
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            completed_module = None
            completed_year = None
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = next(
            (candidate for candidate in context.pages if "policycommons.net" in candidate.url),
            None,
        )
        if page is None:
            page = context.new_page()
        for candidate in list(context.pages):
            if candidate is not page and candidate.url == "about:blank":
                candidate.close()

        for module in MODULES:
            for year in YEARS:
                if completed_module in MODULES and completed_year is not None:
                    module_index = MODULES.index(module)
                    completed_index = MODULES.index(completed_module)
                    if module_index < completed_index:
                        continue
                    if module_index == completed_index and year >= completed_year:
                        continue
                try:
                    partitions = plan_year(page, context, module, year)
                    append_jsonl(
                        plan_log,
                        {
                            "module": module,
                            "module_name": MODULE_NAMES[module],
                            "year": year,
                            "partition_count": len(partitions),
                            "partitions": partitions,
                            "planned_at": now(),
                        },
                    )
                    print(
                        f"PLAN {module} {year} partitions={len(partitions)} "
                        f"counts={sum(int(p['count']) for p in partitions)}",
                        flush=True,
                    )
                    for partition in partitions:
                        try:
                            download_partition(page, module, year, partition)
                        except Exception as exc:
                            append_jsonl(
                                ROOT / "skipped_partitions.jsonl",
                                {
                                    "module": module,
                                    "year": year,
                                    "partition": partition,
                                    "error": repr(exc),
                                    "at": now(),
                                },
                            )
                            print(
                                f"SKIP PARTITION {module} {year} "
                                f"{partition.get('label')} error={exc!r}",
                                flush=True,
                            )
                except Exception as exc:
                    append_jsonl(
                        ROOT / "skipped_years.jsonl",
                        {
                            "module": module,
                            "year": year,
                            "error": repr(exc),
                            "at": now(),
                        },
                    )
                    print(
                        f"SKIP YEAR {module} {year} error={exc!r}", flush=True
                    )
                checkpoint.write_text(
                    json.dumps(
                        {
                            "last_completed_module": module,
                            "last_completed_year": year,
                            "status": "running",
                            "updated_at": now(),
                        },
                        ensure_ascii=False,
                        indent=2,
                    ),
                    encoding="utf-8",
                )
        checkpoint.write_text(
            json.dumps(
                {
                    "last_completed_module": MODULES[-1],
                    "last_completed_year": YEARS[-1],
                    "status": "complete",
                    "updated_at": now(),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        browser.close()


if __name__ == "__main__":
    main()
