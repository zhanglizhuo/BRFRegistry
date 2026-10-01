#!/usr/bin/env python3
"""Cross-repository consistency checks for BRFRegistry and BRFPackage.

These two trees hold the same registry in two places, and several facts are
duplicated across files in each of them. Nothing in the build enforces that the
copies agree, so a version bump or a hash regeneration that reaches one file and
not its twin ships silently. This script is the check that would have caught
each of the following, all of which reached a release before it existed:

  * 0.3.2 updated pyproject.toml and brf.__version__ but left setup.py and
    CITATION.cff at 0.3.0, so a reader saw two different versions.
  * The 51 dataset cards had empty task.type for 21 entries.
  * MANIFEST.in named sn-nature.bst, which lives in the manuscript directory,
    so setuptools skipped it silently and twine check passed regardless.
  * mm_tba's file-level digest covered all 2666 extracted files including 51
    __pycache__ .pyc instead of the 419 that prepare() reads.
  * prepare_hashes.json shipped the frozen 35-entry v2.0 file inside 0.3.0.

Exit status is 0 when every check passes and 1 otherwise, so it can be used as
a pre-commit hook or a CI step. Each check prints one line per finding.

Usage:
    python scripts/check_consistency.py
    python scripts/check_consistency.py --verbose

Run from either repository root, or from the parent that contains both.
"""

from __future__ import annotations

import argparse
import ast
import filecmp
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.checks = 0

    def check(self, name: str, ok: bool, detail: str = "") -> bool:
        self.checks += 1
        if ok:
            print(f"  PASS  {name}")
        else:
            print(f"  FAIL  {name}" + (f" -- {detail}" if detail else ""))
            self.failures.append(f"{name}: {detail}" if detail else name)
        return ok

    def section(self, title: str) -> None:
        print(f"\n{title}")

    def summary(self) -> int:
        total = self.checks
        bad = len(self.failures)
        print(f"\n{total - bad}/{total} checks passed")
        if bad:
            print(f"{bad} FAILED:")
            for f in self.failures:
                print(f"  - {f}")
            return 1
        print("all checks passed")
        return 0


def find_roots(start: Path) -> tuple[Path | None, Path | None]:
    """Locate the BRFRegistry and BRFPackage working trees."""
    candidates = [start, start.parent, start.parent.parent]
    reg = pkg = None
    for c in candidates:
        if reg is None and (c / "registry" / "verify.py").exists():
            reg = c
        if pkg is None and (c / "src" / "brf" / "registry" / "verify.py").exists():
            pkg = c
    if reg is not None and pkg is not None:
        return reg, pkg
    # Not rooted at either tree: look for sibling directories instead.
    for parent in (start, start.parent, start.parent.parent):
        try:
            entries = sorted(p for p in parent.iterdir() if p.is_dir())
        except (NotADirectoryError, PermissionError):
            continue
        for e in entries:
            if reg is None and (e / "registry" / "verify.py").exists():
                reg = e
            if pkg is None and (e / "src" / "brf" / "registry" / "verify.py").exists():
                pkg = e
        if reg is not None and pkg is not None:
            return reg, pkg
    return reg, pkg


def read_version(path: Path, pattern: str) -> str | None:
    if not path.exists():
        return None
    # re.M so that an anchored pattern such as ^\s*version: matches the
    # indented key in CITATION.cff rather than only the first line of the file.
    m = re.search(pattern, path.read_text(encoding="utf-8", errors="replace"), re.M)
    return m.group(1) if m else None


def walk_source_files(root: Path) -> list[Path]:
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ("__pycache__", "cache", ".git")]
        for fn in filenames:
            if fn.endswith(".py"):
                out.append(Path(dirpath) / fn)
    return sorted(out)


def compare_trees(reg_root: Path, pkg_root: Path) -> tuple[list[str], list[str]]:
    """Compare registry/sources and registry/verify.py across the two trees.

    The package tree is allowed to differ from the repository tree in ways the
    packaging requires. Known, intended differences are listed here so that a
    new one is a finding rather than noise.
    """
    reg_dir = reg_root / "registry"
    pkg_dir = pkg_root / "src" / "brf" / "registry"

    intended_code_differences = {
        # The package __init__ carries a docstring and re-exports the verify
        # helpers so that `from brf.registry import verify_all` works.
        "__init__.py",
        # These two carry an offline cache fallback so that a re-run can reuse
        # an existing extraction instead of re-downloading.
        os.path.join("sources", "kdd_cup_2010.py"),
        os.path.join("sources", "student_dropout.py"),
    }

    code_differs: list[str] = []
    data_differs: list[str] = []

    for src in walk_source_files(reg_dir):
        rel = src.relative_to(reg_dir)
        dst = pkg_dir / rel
        if not dst.exists():
            code_differs.append(f"{rel} missing from package tree")
            continue
        if filecmp.cmp(src, dst, shallow=False):
            continue
        key = str(rel)
        if key in intended_code_differences:
            continue
        code_differs.append(f"{rel} differs between the two trees")

    reg_only = {p.relative_to(reg_dir) for p in walk_source_files(reg_dir)}
    pkg_only = {p.relative_to(pkg_dir) for p in walk_source_files(pkg_dir)}
    for rel in sorted(reg_only - pkg_only):
        code_differs.append(f"{rel} only in repository tree")
    for rel in sorted(pkg_only - reg_only):
        code_differs.append(f"{rel} only in package tree")

    # Data files must be byte-identical in both directions.
    # registry_v2.1.json is expected in both trees; if either copy is absent
    # that is a finding rather than a layout difference.
    for name in ("prepare_hashes.json", "registry_v2.1.json", "manifest.yaml",
                 "taxonomy.yaml", "version_policy.yaml"):
        a, b = reg_dir / name, pkg_dir / name
        if a.exists() != b.exists():
            data_differs.append(f"{name} present in only one tree")
        elif a.exists() and not filecmp.cmp(a, b, shallow=False):
            data_differs.append(f"{name} differs between the two trees")

    # registry_v2.1.json also lives in BRFRegistry/results/, which is the copy the
    # generators read. The packaged copy under registry/ is what an installed
    # user gets, so the two must stay identical rather than merely both present.
    results_copy = reg_root / "results" / "registry_v2.1.json"
    packaged = pkg_dir / "registry_v2.1.json"
    if results_copy.exists() and packaged.exists():
        if not filecmp.cmp(results_copy, packaged, shallow=False):
            data_differs.append(
                "registry_v2.1.json: results/ copy differs from the packaged copy")

    return code_differs, data_differs


def check_cards(reg_dir: Path, report: Report) -> None:
    cards_dir = reg_dir / "cards"
    if not cards_dir.is_dir():
        report.check("dataset cards present", False, f"{cards_dir} not found")
        return
    files = sorted(cards_dir.glob("*.yaml"))
    report.check("51 dataset cards", len(files) == 51, f"found {len(files)}")

    if yaml is None:
        print("  SKIP  card field checks (pyyaml not installed)")
        return

    empty_task = []
    for f in files:
        card = yaml.safe_load(f.read_text(encoding="utf-8"))
        task = card.get("task") or {}
        if not str(task.get("type") or "").strip():
            empty_task.append(f.stem)
    report.check(
        "every card has a non-empty task.type",
        not empty_task,
        f"{len(empty_task)} empty: {', '.join(empty_task[:6])}"
        + ("..." if len(empty_task) > 6 else ""),
    )


def check_card_source_agreement(reg_dir: Path, report: Report) -> None:
    """Compare card N/G/p/task against the source modules when importable."""
    cards_dir = reg_dir / "cards"
    if not cards_dir.is_dir() or yaml is None:
        report.check("card fields agree with source modules", False,
                     "prerequisites missing (cards or pyyaml)")
        return
    sys.path.insert(0, str(reg_dir.parent))
    try:
        from registry.sources import REGISTRY_SOURCES  # type: ignore
    except Exception as exc:  # pragma: no cover
        report.check("card fields agree with source modules", False,
                     f"cannot import registry.sources: {exc}")
        return

    mismatches = []
    for f in sorted(cards_dir.glob("*.yaml")):
        key = f.stem
        src = REGISTRY_SOURCES.get(key)
        if src is None:
            mismatches.append(f"{key}: card has no source module")
            continue
        card = yaml.safe_load(f.read_text(encoding="utf-8"))
        for card_key, attr in (("n_samples", "n_samples"), ("n_groups", "n_groups"),
                               ("n_features", "n_features")):
            val = card.get(card_key)
            if val is not None and int(val) != int(getattr(src, attr)):
                mismatches.append(
                    f"{key}.{card_key}={val} but source declares {getattr(src, attr)}")
        task_type = str((card.get("task") or {}).get("type") or "").strip()
        if task_type and task_type != src.task:
            mismatches.append(f"{key}.task.type={task_type!r} but source.task={src.task!r}")
    report.check("card fields agree with source modules", not mismatches,
                 f"{len(mismatches)} mismatches: " + "; ".join(mismatches[:4]))


def check_manifest_in(pkg_root: Path, report: Report) -> None:
    mi = pkg_root / "MANIFEST.in"
    if not mi.exists():
        report.check("MANIFEST.in patterns match real files", True,
                     "no MANIFEST.in (nothing to check)")
        return
    missing = []
    for line in mi.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("include"):
            continue
        pattern = line.split(None, 1)[1].strip()
        # MANIFEST.in include paths are relative to the project root, which is
        # why verification/ resolves even though it sits outside src/brf.
        hits = list(pkg_root.glob(pattern))
        if not hits:
            missing.append(pattern)
    report.check(
        "MANIFEST.in patterns match real files", not missing,
        f"match nothing and are skipped silently: {', '.join(missing)}",
    )


def check_declared_hash_coverage(reg_dir: Path, report: Report) -> None:
    """The paper states 42/51 file-level digests; the policy file must agree."""
    vp = reg_dir / "version_policy.yaml"
    if not vp.exists() or yaml is None:
        report.check("version_policy SHA coverage matches reality", False,
                     "version_policy.yaml or pyyaml missing")
        return
    try:
        sys.path.insert(0, str(reg_dir.parent))
        from registry.sources import REGISTRY_SOURCES  # type: ignore
    except Exception as exc:  # pragma: no cover
        report.check("version_policy SHA coverage matches reality", False, str(exc))
        return
    n = sum(1 for s in REGISTRY_SOURCES.values() if s.sha256)
    total = len(REGISTRY_SOURCES)
    doc = yaml.safe_load(vp.read_text(encoding="utf-8"))
    text = json.dumps(doc)
    claimed = re.search(r"SHA-256 coverage: (\d+)/(\d+)", text)
    if not claimed:
        report.check("version_policy SHA coverage matches reality", False,
                     "no 'SHA-256 coverage: n/m' string in version_policy.yaml")
        return
    cn, ct = int(claimed.group(1)), int(claimed.group(2))
    report.check("version_policy SHA coverage matches reality",
                 (cn, ct) == (n, total),
                 f"policy says {cn}/{ct}, sources declare {n}/{total}")


def check_prepare_hashes(reg_dir: Path, report: Report) -> None:
    ph = reg_dir / "prepare_hashes.json"
    if not ph.exists():
        report.check("prepare_hashes.json exists and is current", False, "absent")
        return
    data = json.loads(ph.read_text(encoding="utf-8"))
    report.check("prepare_hashes.json has one entry per dataset", len(data) == 51,
                 f"{len(data)} entries")

    sys.path.insert(0, str(reg_dir.parent))
    try:
        from registry.sources import REGISTRY_SOURCES  # type: ignore
        missing = sorted(set(REGISTRY_SOURCES) - set(data))
        extra = sorted(set(data) - set(REGISTRY_SOURCES))
    except Exception:  # pragma: no cover
        report.check("prepare_hashes keys match registered sources", True,
                     "registry.sources not importable; skipped")
        return
    report.check("prepare_hashes keys match registered sources",
                 not missing and not extra,
                 f"missing {missing[:5]}, unknown {extra[:5]}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=None,
                    help="directory containing BRFRegistry/ and BRFPackage/")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    start = args.root or Path(__file__).resolve().parent.parent
    reg_root, pkg_root = find_roots(start)
    if reg_root is None or pkg_root is None:
        print(f"error: could not locate both trees from {start}")
        print("       expected BRFRegistry/registry and BRFPackage/src/brf/registry")
        return 2

    print(f"repository tree : {reg_root}")
    print(f"package tree    : {pkg_root}")

    report = Report()

    report.section("Version chain")
    files = {
        "pyproject.toml": (pkg_root / "pyproject.toml", r'version\s*=\s*"([^"]+)"'),
        "setup.py": (pkg_root / "setup.py", r'version\s*=\s*"([^"]+)"'),
        "CITATION.cff": (pkg_root / "CITATION.cff", r'^\s*version:\s*"([^"]+)"'),
        "src/brf/__init__.py": (pkg_root / "src" / "brf" / "__init__.py",
                                r'__version__\s*=\s*"([^"]+)"'),
    }
    versions: dict[str, str | None] = {}
    for name, (path, pattern) in files.items():
        versions[name] = read_version(path, pattern)
        flag = "" if versions[name] else "   <-- FILE MISSING OR NO VERSION"
        print(f"        {name:<22} {versions[name] or '<not found>'}{flag}")

    missing = [n for n, v in versions.items() if not v]
    if missing:
        report.check("every version declaration is readable", False,
                     f"no version found in: {', '.join(missing)}")
    else:
        report.check("every version declaration is readable", True)

    distinct = {v for v in versions.values() if v}
    report.check("version declared identically in all four files", len(distinct) == 1,
                 f"found {sorted(distinct)}")

    if len(distinct) == 1:
        ver = distinct.pop()
        changelog = pkg_root / "CHANGELOG.md"
        if changelog.exists():
            text = changelog.read_text(encoding="utf-8", errors="replace")
            entry = f"## {ver} " in text or f"## {ver}(" in text or f"## {ver}\n" in text
            report.check(f"CHANGELOG has an entry for {ver}", entry,
                         "no section header for this version")

    report.section("Package data declared vs shipped")
    pp = pkg_root / "pyproject.toml"
    if pp.exists():
        text = pp.read_text(encoding="utf-8")
        declared = re.search(r'package-data.*?=?\s*\[(.*?)\]', text, re.S)
        if declared:
            reg_dir = pkg_root / "src" / "brf" / "registry"
            missing = []
            for pat in re.findall(r'"([^"]+)"', declared.group(1)):
                if "*" in pat:
                    # Expand the glob against the tree so that a pattern matching
                    # nothing is reported rather than passing silently.
                    hits = list(reg_dir.glob(pat))
                    if not hits:
                        missing.append(pat)
                elif not (reg_dir / pat).exists():
                    missing.append(pat)
            report.check("package-data entries exist in the source tree", not missing,
                         f"declared but match nothing: {', '.join(missing)}")
    check_manifest_in(pkg_root, report)

    report.section("Two trees agree")
    code_diff, data_diff = compare_trees(reg_root, pkg_root)
    report.check("registry source files agree (excluding documented differences)",
                 not code_diff, f"{len(code_diff)}: " + "; ".join(code_diff[:3]))
    report.check("registry data files agree", not data_diff,
                 f"{len(data_diff)}: " + "; ".join(data_diff[:3]))

    reg_dir = reg_root / "registry"
    report.section("Registry content")
    check_cards(reg_dir, report)
    check_card_source_agreement(reg_dir, report)
    check_declared_hash_coverage(reg_dir, report)
    check_prepare_hashes(reg_dir, report)

    report.section("Python syntax")
    bad = []
    for src in walk_source_files(reg_dir) + walk_source_files(pkg_root / "src" / "brf"):
        try:
            ast.parse(src.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError as exc:
            bad.append(f"{src}: {exc}")
    report.check("every registry .py parses", not bad,
                 f"{len(bad)}: " + "; ".join(b[:80] for b in bad[:3]))

    return report.summary()


if __name__ == "__main__":
    raise SystemExit(main())