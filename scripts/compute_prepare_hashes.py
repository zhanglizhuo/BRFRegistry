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


def _canonical_array_bytes(arr):
    """Return (dtype_tag, payload) for an array in an interpreter-stable form."""
    a = np.asarray(arr)
    if a.dtype.kind in "OUS":
        return "str", "\n".join("" if v is None else str(v) for v in a.ravel()).encode("utf-8")
    kind = {"i": "int64", "u": "uint64", "b": "bool",
            "f": "float64", "c": "complex128"}.get(a.dtype.kind)
    if kind is None:
        raise TypeError(f"unsupported dtype kind {a.dtype.kind!r} for canonical hashing")
    return kind, np.ascontiguousarray(a, dtype=kind).tobytes()


def compute_prepare_sha256(X, y, groups):
    """SHA-256 over a canonical encoding of the prepared data.

    This hashes the data, not a serialisation of it. Hashing the bytes that
    numpy.save() emits is not equivalent: object-dtype arrays are pickled, and
    that byte stream is not stable across interpreters. Measured on this
    registry, identical data hashed differently on CPython 3.8 and 3.13 for 26
    of 51 datasets, because the pickled form of the object-dtype `groups` array
    differed in length (8663 vs 8646 bytes for abalone) while its values were
    element-for-element equal.

    Each array is therefore reduced to an explicitly declared dtype, its shape,
    and its raw bytes, so the digest depends only on the values.
    """
    sha = hashlib.sha256()
    for name, arr in (("X", X), ("y", y), ("groups", groups)):
        dtype_tag, payload = _canonical_array_bytes(arr)
        sha.update(f"{name}|{dtype_tag}|{np.asarray(arr).shape}|".encode("utf-8"))
        sha.update(payload)
        sha.update(b"\x00")
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
