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
            return True
        return self._check_sha256(path)

    @abstractmethod
    def prepare(self):
        """Return (X, y, groups, metadata_card)."""

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
