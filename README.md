# BRF Benchmark Registry

The **BRF Benchmark Registry** is a versioned, DOI-tracked collection of
group-aware prediction benchmarks audited under the
**Benchmark Reliability Framework (BRF)**.

> Registry v2.0 : 35 unique datasets | 27 Reliable | 8 Void | 0 Fragile
> DOI pending

## What's New in v2.0

- 35 source modules (up from 20 in v1.6) — all self-contained, 0 external dependencies
- 7 alt-grouping views for large/granular datasets
- Multi-domain: education (17), engineering (6), energy (3), transportation (2), food (1), other (6)
- Mixed task types: 27 regression, 8 classification
- SHA-256: 35/35 (100%) — all source modules verified
- Per-dataset data quality metrics: N/p ratio, group quality (entropy, balance), signal strength (B, S)
- Every source implements: download() + prepare() + metadata() + verify()
- Sample sizes: N=145 (higher_ed) to N=519,334 (pisa2015)
- Feature dimensions: F=2 (oli, pisa2015) to F=72 (xapi_edu)
- CLI: `brf diagnose`, `brf rank`, `brf recommend`
- All sources cached locally with versioned cache keys
- Registry results published as machine-readable JSON (registry_v2.0.json)

## Quick Start

```bash
pip install benchmark-reliability

# Browse the Registry
brf registry list              # 35 datasets
brf registry info tae          # full metadata
brf registry sync              # download + verify all
brf audit tae                  # run BRF on a dataset
```

## Structure

```
BRFRegistry/
|-- registry/
|   |-- sources/          # 35 DatasetSource .py files (auto-discovered)
|   |-- cards/            # YAML Dataset Cards
|   |-- cache/            # Downloaded data (gitignored)
|   |-- manifest.yaml     # Registry version + dataset index
|   |-- taxonomy.yaml     # 5-level benchmark taxonomy
|   |-- version_policy.yaml # Lifecycle + deprecation rules
|   |-- cli.py            # CLI: list, download, verify, sync, info
|   |-- verify.py         # SHA-256 verification
|   `-- known_datasets.py # Metadata registry (35 entries)
|-- results/
|   `-- registry_v2.0.json # 35 entries with BRF results + metadata
`-- run_registry.py        # Run BRF on all registered datasets
```

## Adding a Dataset

Submit a PR with a `DatasetSource` subclass. See existing sources in
`registry/sources/` for examples. Datasets must satisfy the
[inclusion criteria](#) and pass BRF audit before merging.

## Registry Contents

| Version | Date | Entries | Reliable | Void | Fragile |
|---------|------|---------|----------|------|---------|
| v1.0 | 2026-03-28 | 7 | 4 | 3 | 0 |
| v1.6 | 2026-07-01 | 27 | 21 | 6 | 0 |
| v2.0 | 2026-07-04 | 35 | 26 | 8 | 0 |

### v2.0 (current) -- 35 entries

| Dataset | N | p | G | S | E | Class |
|---------|---|---|---|---|---|---|
| Abalone Age (Sex groups) | 4.2K | 10 | 3 | 0.93 | 1.48 | Reliable |
| Airfoil Noise (Freq) | 1.5K | 4 | 3 | 0.76 | 0.78 | Reliable |
| ASSISTments 2009-2010 | 3.7K | 5 | 124 | 0.95 | 0.95 | Reliable |
| Auto MPG (Origin groups) | 398 | 9 | 3 | 0.96 | 1.44 | Reliable |
| Bike Sharing (Season) | 731 | 10 | 4 | 0.96 | 1.77 | Reliable |
| Combined Cycle Power (Temp) | 9.6K | 3 | 3 | 0.99 | 1.74 | Reliable |
| Concrete Strength (Age) | 1K | 7 | 3 | 0.89 | 0.88 | Reliable |
| Energy Building (Orientation) | 768 | 8 | 4 | 0.99 | 1.93 | Reliable |
| Entrance Exam | 666 | 49 | 3 | 0.88 | 0.97 | Reliable |
| Higher Education Students Performance | 145 | 31 | 9 | -1.03 | 0.56 | Void |
| KDD Cup 2010 (Algebra I 2005-2006) | 574 | 5 | 22 | 0.95 | ? | ? |
| Kaggle Students Performance in Exams | 1K | 14 | 5 | 0.81 | 1.00 | Reliable |
| Law School Admission | 20.8K | 7 | 6 | 0.96 | 0.73 | Reliable |
| MathE Mathematics Learning | 833 | 26 | 14 | -1.64 | 0.63 | Void |
| MM-TBA Teaching Behavior Analysis | 186 | 13 | 0 | -0.77 | -0.03 | Void |
| UCI Nursery School Applications | 12K | 24 | 3 | 1.00 | 1.95 | Reliable |
| OLI Engineering Statics 2011 | 194.9K | 2 | 19 | 0.96 | 0.71 | Reliable |
| Open University Learning Analytics Dataset | 32.6K | 44 | 22 | 0.98 | 1.17 | Reliable |
| PISA 2015 Science | 519.3K | 2 | 73 | -0.10 | 0.66 | Void |
| Real Estate Valuation (Stores) | 414 | 6 | 3 | 0.84 | 1.52 | Reliable |
| Seoul Bike Sharing (Season) | 8.8K | 11 | 4 | 0.97 | 1.46 | Reliable |
| Student Depression Survey | 27.9K | 21 | 30 | 0.98 | 1.37 | Reliable |
| Student Dropout and Academic Success | 3.6K | 36 | 17 | 0.97 | 1.30 | Reliable |
| UCI Student Health (Por, Mjob) | 649 | 53 | 5 | -3.15 | 0.67 | Void |
| UCI Student Absences (Kaggle) | 395 | 37 | 2 | -0.76 | 0.29 | Void |
| Students Exam Scores (Kaggle) | 30.6K | 14 | 5 | 0.97 | 1.04 | Reliable |
| Teaching Assistant Evaluation | 151 | 4 | 25 | -0.42 | 0.75 | Void |
| Turkiye Student Evaluation | 5.8K | 28 | 13 | 0.56 | 0.70 | Reliable |
| UCI Student Performance | 649 | 56 | 2 | 0.62 | 1.06 | Reliable |
| UCI Student Performance (Math) | 395 | 56 | 2 | -2.67 | 0.43 | Void |
| US College Scorecard | 2.2K | 30 | 55 | 0.82 | 0.69 | Reliable |
| AAUP College Faculty Salary | 1.2K | 9 | 52 | 0.90 | 1.03 | Reliable |
| Colleges US News Rankings | 1.2K | 31 | 51 | 0.88 | 1.04 | Reliable |
| Wine Quality (Red+White) | 6.5K | 11 | 2 | 0.93 | 0.93 | Reliable |
| xAPI-Edu-Data | 480 | 72 | 12 | 0.89 | 1.34 | Reliable |

### BRF Metric Definitions

S = N - I (Stability), E = B + M (Evidence).

## Key Findings (v2.0, N=35)

- **No Fragile datasets** across 35 multi-domain benchmarks. Rule-of-three upper bound ~8%.
- **Bimodal**: 26 Reliable, 8 Void, 1 unknown -- no intermediate regime.
- **Multi-domain**: Expanded from education-only to include engineering, energy, transportation, and other domains.
- **Grouping sensitivity**: Same data, different grouping can shift E by 0.35-0.85.
- **Self-contained**: 35/35 source modules independent (0 BA dependencies).

## License

Code: MIT. Individual datasets have their own licenses (see registry metadata).
