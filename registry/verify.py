"""SHA-256 verification for downloaded datasets."""

import hashlib
from pathlib import Path

from .sources import REGISTRY_SOURCES, list_sources


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
        print(f"Dataset '{key}' is a directory; skipping hash check.")
        return True
    actual = compute_sha256(path)
    if actual == source.sha256:
        print(f"  OK: {key} sha256={actual[:16]}...")
        return True
    else:
        print(f"  MISMATCH: {key}")
        print(f"    expected: {source.sha256[:32]}...")
        print(f"    actual:   {actual[:32]}...")
        return False


def verify_all():
    results = {}
    for key in list_sources():
        results[key] = verify_dataset(key)
    return results
