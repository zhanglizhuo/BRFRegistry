"""Build BRF Benchmark Registry: run BRF on all known datasets and save results.

Uses the Dataset-as-Code architecture (registry/sources/).
"""

import json
import time
from pathlib import Path

import numpy as np
from sklearn.preprocessing import StandardScaler

from brf import BRFAnalyzer
from registry import REGISTRY_SOURCES, list_sources

RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def run_brf_on_source(source):
    """Run BRF on a single DatasetSource instance."""
    info = source.metadata()

    print(f"\n{'='*60}")
    print(f"  {info['display_name']} ({source.name})")
    print(f"{'='*60}")

    t0 = time.time()

    try:
        X_raw, y, groups_raw, data_card = source.prepare()
    except Exception as e:
        print(f"  ERROR: could not prepare -- {e}")
        return {**info, "brf_error": f"prepare_failed: {e}", "brf_result": None}

    scaler = StandardScaler()
    X = scaler.fit_transform(X_raw)

    if groups_raw is not None:
        groups = np.array(groups_raw)
    else:
        groups = None

    n_grp = len(np.unique(groups)) if groups is not None else 0
    print(f"  N={len(y)}, features={X.shape[1]}, groups={n_grp}")

    try:
        analyzer = BRFAnalyzer(n_splits=30, n_permutations=200).fit(X, y, groups=groups)
    except Exception as e:
        print(f"  ERROR: BRF failed -- {e}")
        return {**info, "brf_error": f"brf_failed: {e}", "brf_result": None}

    bv = analyzer.brf_vector
    elapsed = time.time() - t0

    print(f"  B={bv['B']:.4f}, I={bv['I']:.4f}, N={bv['N']:.4f}, M={bv['M']:.4f}")
    print(f"  S={bv['S']:.4f}, E={bv['E']:.4f}, class={bv['class']}")
    print(f"  elapsed={elapsed:.1f}s")

    return {
        **info,
        "brf_result": {
            "B": round(bv["B"], 4),
            "I": round(bv["I"], 4),
            "N": round(bv["N"], 4),
            "M": round(bv["M"], 4),
            "S": round(bv["S"], 4),
            "E": round(bv["E"], 4),
            "class": bv["class"],
            "n_splits": 30,
            "n_permutations": 200,
            "model": "Ridge(alpha=1.0)",
            "seed": 42,
            "scale": True,
            "elapsed_seconds": round(elapsed, 1),
        },
        "brf_error": None,
    }


def main(subset=None):
    """Run BRF on all (or a *subset* of) registered datasets.

    Args:
        subset: Optional list of dataset keys to run. If None, runs all.
    """
    keys = subset if subset is not None else list_sources()
    results = {}

    successes = 0
    failures = 0

    for key in keys:
        source = REGISTRY_SOURCES.get(key)
        if source is None:
            print(f"\n  SKIP {key}: not registered")
            continue

        result = run_brf_on_source(source)
        results[key] = result
        if result["brf_result"] and result["brf_error"] is None:
            successes += 1
        else:
            failures += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"  SUMMARY: {successes} succeeded, {failures} failed")
    print(f"{'='*60}")
    for key, r in sorted(results.items()):
        cls = r["brf_result"]["class"] if r["brf_result"] else "ERROR"
        print(f"  {key:<20} -> {cls}")

    # Save
    out_path = RESULTS_DIR / "registry_v1.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n  Saved to {out_path}")

    return results


if __name__ == "__main__":
    main()
