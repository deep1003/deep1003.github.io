#!/usr/bin/env python3
"""Validate the published structural claims for a local v7.10 release."""

import argparse
import hashlib
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--master", type=Path, required=True)
    parser.add_argument("--pairs", type=Path, required=True)
    args = parser.parse_args()

    master = pd.read_parquet(args.master)
    pairs = pd.read_csv(args.pairs, dtype=str)
    schema = pq.read_schema(args.master)

    assert len(master) == 269_853
    assert master["record_id"].nunique(dropna=False) == 269_853
    assert len(schema.names) == 162
    assert len(pairs) == 182_010
    assert pairs["record_id"].nunique(dropna=False) == 182_010
    assert not pairs.duplicated(["record_id", "analysis_country"]).any()
    assert pairs["weight"].astype(int).eq(1).all()
    assert pairs["analysis_country"].nunique(dropna=False) == 135
    assert set(pairs["record_id"]) <= set(master["record_id"])

    print(f"master_rows={len(master)} columns={len(schema.names)} sha256={sha256(args.master)}")
    print(f"pair_rows={len(pairs)} countries={pairs.analysis_country.nunique()} sha256={sha256(args.pairs)}")
    print("release_structure=PASS")


if __name__ == "__main__":
    main()
