"""Dataset-as-Code framework for BRF Registry.

Each dataset is a Python module with a DatasetSource subclass decorated
with @register_source. Modules are auto-discovered on import.
"""

import hashlib
import importlib
import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np

_CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"
_CACHE_DIR.mkdir(parents=True, exist_ok=True)


class DatasetSource(ABC):

    name = ""
    display_name = ""
    version = "1.0"
    source_url = ""
    fallback_urls = []
    license_info = "TBD"
    reference = ""
    task = "regression"
    n_samples = 0
    n_features = 0
    n_groups = 0
    sha256 = ""
    prepare_sha256 = ""
    grouping_description = ""
    notes = ""

    def _cache_path(self, filename):
        return _CACHE_DIR / self.name / filename

    def _ensure_cache_dir(self):
        p = _CACHE_DIR / self.name
        p.mkdir(parents=True, exist_ok=True)
        return p

    @staticmethod
    def _download_url(url, dest, timeout=120):
        from urllib.request import urlretrieve
        dest.parent.mkdir(parents=True, exist_ok=True)
        urlretrieve(url, str(dest))
        return dest

    @staticmethod
    def _compute_sha256(path):
        sha = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha.update(chunk)
        return sha.hexdigest()

    def _check_sha256(self, path):
        if not self.sha256:
            return True
        actual = self._compute_sha256(path)
        return actual == self.sha256

    @abstractmethod
    def download(self):
        """Download raw data, return path to file or directory."""

    def verify(self, path=None):
        if path is None:
            path = self.download()
        if isinstance(path, Path) and path.is_dir():
            return self._check_directory_sha256(path)
        return self._check_sha256(path)

    def _compute_directory_sha256(self, path):
        sha = hashlib.sha256()
        for fpath in sorted(path.rglob("*")):
            if fpath.is_file():
                rel = fpath.relative_to(path)
                sha.update(str(rel).encode())
                file_sha = self._compute_sha256(fpath)
                sha.update(file_sha.encode())
        return sha.hexdigest()

    def _check_directory_sha256(self, path):
        if not self.sha256:
            return True
        actual = self._compute_directory_sha256(path)
        return actual == self.sha256

    @abstractmethod
    def prepare(self):
        """Return (X, y, groups, metadata_card)."""

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
    def verify_prepare(self):
        if not self.prepare_sha256:
            return True
        X, y, groups, _ = self.prepare()
        actual = self._compute_prepare_sha256(X, y, groups)
        return actual == self.prepare_sha256

    def metadata(self):
        return {
            "name": self.name,
            "display_name": self.display_name,
            "version": self.version,
            "source_url": self.source_url,
            "license": self.license_info,
            "reference": self.reference,
            "task": self.task,
            "n_samples": self.n_samples,
            "n_features": self.n_features,
            "n_groups": self.n_groups,
            "sha256": self.sha256,
            "prepare_sha256": self.prepare_sha256,
            "grouping": self.grouping_description,
            "notes": self.notes,
        }


REGISTRY_SOURCES = {}


def register_source(source_cls_or_instance):
    if isinstance(source_cls_or_instance, type):
        instance = source_cls_or_instance()
    else:
        instance = source_cls_or_instance
    REGISTRY_SOURCES[instance.name] = instance
    return instance


def list_sources():
    return sorted(REGISTRY_SOURCES.keys())


# auto-discover all .py modules in this directory
_MODULE_DIR = os.path.dirname(__file__)
for _fn in sorted(os.listdir(_MODULE_DIR)):
    if _fn.startswith("_") or not _fn.endswith(".py"):
        continue
    _modname = _fn[:-3]
    importlib.import_module(f".{_modname}", package=__package__ if __package__ else "registry.sources")
