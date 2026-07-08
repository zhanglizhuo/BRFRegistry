"""Compute prepare() SHA-256 for all datasets and save to JSON.

Usage:
    python scripts/compute_prepare_hashes.py
    python scripts/compute_prepare_hashes.py --verify   # check existing hashes only

Output: registry/prepare_hashes.json
"""

import argparse
import hashlib
import io
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from registry.sources import REGISTRY_SOURCES, list_sources


def compute_prepare_sha256(X, y, groups):
    sha = hashlib.sha256()
    for arr in (X, y, groups):
        buf = io.BytesIO()
        np.save(buf, np.asarray(arr))
        sha.update(buf.getvalue())
    return sha.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true", help="Compare against existing hashes without recomputing")
    args = parser.parse_args()

    hashes_path = Path(__file__).resolve().parent.parent / "registry" / "prepare_hashes.json"

    if args.verify:
        with open(hashes_path) as f:
            expected = json.load(f)
    else:
        expected = {}

    results = {}
    all_ok = True

    for key in list_sources():
        source = REGISTRY_SOURCES[key]
        print(f"  {key}...", end=" ", flush=True)
        try:
            X, y, groups, _ = source.prepare()
            actual = compute_prepare_sha256(X, y, groups)
            results[key] = actual

            if args.verify:
                exp = expected.get(key, "")
                if not exp:
                    print(f"NO EXPECTED HASH")
                    all_ok = False
                elif actual == exp:
                    print(f"OK ({actual[:16]}...)")
                else:
                    print(f"MISMATCH")
                    print(f"    expected: {exp[:32]}...")
                    print(f"    actual:   {actual[:32]}...")
                    all_ok = False
            else:
                print(f"{actual[:16]}...")
        except Exception as e:
            print(f"ERROR: {e}")
            results[key] = None
            all_ok = False

    if not args.verify:
        with open(hashes_path, "w") as f:
            json.dump(results, f, indent=2, sort_keys=True)
            f.write("\n")
        print(f"\nWrote {len(results)} hashes to {hashes_path}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
