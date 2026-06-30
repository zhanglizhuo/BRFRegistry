"""Build BRF Benchmark Registry v1: run BRF on all known datasets and save results."""

import json
import sys
import time
from pathlib import Path

import numpy as np
from sklearn.preprocessing import StandardScaler

from brf import BRFAnalyzer
from registry import REGISTRY, load_dataset

RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def main():
    results = {}
    successes = 0
    failures = 0

    for key in sorted(REGISTRY.keys()):
        info = REGISTRY[key]
        print(f"\n{'='*60}")
        print(f"  {info['name']} ({key})")
        print(f"{'='*60}")

        t0 = time.time()

        loaded = load_dataset(key)
        if loaded is None:
            print(f"  ERROR: could not load")
            results[key] = {**info, "brf_error": "load_failed", "brf_result": None}
            failures += 1
            continue

        X_raw, y, groups, data_card = loaded

        scaler = StandardScaler()
        X = scaler.fit_transform(X_raw)

        print(f"  N={len(y)}, features={X.shape[1]}, groups={len(np.unique(groups)) if groups is not None else 'N/A'}")

        analyzer = BRFAnalyzer(n_splits=30, n_permutations=200).fit(X, y, groups=groups)

        bv = analyzer.brf_vector
        elapsed = time.time() - t0

        print(f"  B={bv['B']:.4f}, I={bv['I']:.4f}, N={bv['N']:.4f}, M={bv['M']:.4f}")
        print(f"  S={bv['S']:.4f}, E={bv['E']:.4f}, class={bv['class']}")
        print(f"  elapsed={elapsed:.1f}s")

        results[key] = {
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
        successes += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"  SUMMARY: {successes} succeeded, {failures} failed")
    print(f"{'='*60}")
    for key, r in results.items():
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
