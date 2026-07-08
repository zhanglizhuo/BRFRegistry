"""SHA-256 verification for downloaded datasets and prepare() output."""

import hashlib
import json
import io
from pathlib import Path

import numpy as np

from .sources import REGISTRY_SOURCES, list_sources

_PREPARE_HASHES_PATH = Path(__file__).resolve().parent / "prepare_hashes.json"


def compute_prepare_sha256(X, y, groups):
    sha = hashlib.sha256()
    for arr in (X, y, groups):
        buf = io.BytesIO()
        np.save(buf, np.asarray(arr))
        sha.update(buf.getvalue())
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
