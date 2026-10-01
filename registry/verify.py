"""SHA-256 verification for downloaded datasets and prepare() output."""

import hashlib
import json
import io
from pathlib import Path

import numpy as np

from .sources import REGISTRY_SOURCES, list_sources

_PREPARE_HASHES_PATH = Path(__file__).resolve().parent / "prepare_hashes.json"


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


def compute_sha256(path):
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()


def verify_dataset(key):
    source = REGISTRY_SOURCES.get(key)
    if source is None:
        print(f"Dataset '{key}' not found.")
        return None
    if not source.sha256:
        print(f"Dataset '{key}' has no SHA-256 checksum defined.")
        return None
    path = source.download()
    if isinstance(path, Path) and path.is_dir():
        actual = compute_directory_sha256(path)
        if actual == source.sha256:
            print(f"  OK: {key} directory sha256={actual[:16]}...")
            return True
        else:
            print(f"  MISMATCH: {key}")
            print(f"    expected: {source.sha256[:32]}...")
            print(f"    actual:   {actual[:32]}...")
            return False
    actual = compute_sha256(path)
    if actual == source.sha256:
        print(f"  OK: {key} sha256={actual[:16]}...")
        return True
    else:
        print(f"  MISMATCH: {key}")
        print(f"    expected: {source.sha256[:32]}...")
        print(f"    actual:   {actual[:32]}...")
        return False


def compute_directory_sha256(path):
    sha = hashlib.sha256()
    for fpath in sorted(path.rglob("*")):
        if fpath.is_file():
            rel = fpath.relative_to(path)
            sha.update(str(rel).encode())
            file_sha = compute_sha256(fpath)
            sha.update(file_sha.encode())
    return sha.hexdigest()


def verify_all():
    results = {}
    for key in list_sources():
        results[key] = verify_dataset(key)
    return results


def verify_prepare(key):
    source = REGISTRY_SOURCES.get(key)
    if source is None:
        print(f"Dataset '{key}' not found.")
        return None
    if not _PREPARE_HASHES_PATH.exists():
        print(f"prepare_hashes.json not found. Run scripts/compute_prepare_hashes.py first.")
        return None
    with open(_PREPARE_HASHES_PATH) as f:
        expected = json.load(f)
    exp_hash = expected.get(key)
    if not exp_hash:
        print(f"  {key}: no prepare hash defined in prepare_hashes.json")
        return None
    try:
        X, y, groups, _ = source.prepare()
        actual = compute_prepare_sha256(X, y, groups)
        if actual == exp_hash:
            print(f"  OK: {key} prepare_sha256={actual[:16]}...")
            return True
        else:
            print(f"  MISMATCH: {key}")
            print(f"    expected: {exp_hash[:32]}...")
            print(f"    actual:   {actual[:32]}...")
            return False
    except Exception as e:
        print(f"  ERROR: {key}: {e}")
        return False


def verify_prepare_all():
    results = {}
    for key in list_sources():
        results[key] = verify_prepare(key)
    return results
