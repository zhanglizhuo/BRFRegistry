# BRF Benchmark Registry

The **BRF Benchmark Registry** is a versioned, DOI-tracked collection of
group-aware prediction benchmarks audited under the
**Benchmark Reliability Framework (BRF)**.

> Registry v2.1 : 51 unique datasets | 35 Reliable | 16 Void | 0 Fragile
> 58 total entries (51 unique + 7 alternative grouping views)
> DOI pending

## What's New in v2.1

- 39 self-contained source modules covering 51 unique datasets (up from 35 in v2.0) — 0 external dependencies
- 7 alt-grouping views for large/granular datasets (58 total entries)
- Multi-domain: 25 educational + 26 cross-domain benchmarks (health, finance, environment, energy, transportation, systems)
- Mixed task types: 43 regression, 8 classification
- SHA-256: 35/51 (69%) — all 35 file-backed datasets verified; the 16 v2.1 cross-domain additions are scikit-learn-bundled, synthetic, or API-sourced and carry no single raw file to checksum
- Per-dataset data quality metrics: N/p ratio, group quality (entropy, balance), signal strength (B, S)
- Every source implements: download() + prepare() + metadata() + verify()
- Sample sizes: N=20 (Linnerud) to N=519,334 (PISA 2015)
- Feature dimensions: F=2 (OLI, PISA 2015) to F=72 (xAPI-Edu-Data)
- CLI: `brf diagnose`, `brf rank`, `brf recommend`
- All sources cached locally with versioned cache keys
- Registry results published as machine-readable JSON (registry_v2.1.json)

## Quick Start

```bash
pip install benchmark-reliability

# Browse the Registry
brf registry list              # 51 datasets
brf registry info tae          # full metadata
brf registry sync              # download + verify all
brf audit tae                  # run BRF on a dataset
```

## Structure

```
BRFRegistry/
|-- registry/
|   |-- sources/          # 39 DatasetSource .py files covering 51 datasets (auto-discovered)
|   |-- cards/            # YAML Dataset Cards
|   |-- cache/            # Downloaded data (gitignored)
|   |-- manifest.yaml     # Registry version + dataset index
|   |-- taxonomy.yaml     # 5-level benchmark taxonomy
|   |-- version_policy.yaml # Lifecycle + deprecation rules
|   |-- cli.py            # CLI: list, download, verify, sync, info
|   `-- verify.py         # SHA-256 verification
|-- results/
|   `-- registry_v2.1.json # 51 entries with BRF results + metadata
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
| v2.0 | 2026-07-04 | 35 | 27 | 8 | 0 |
| v2.1 | 2026-09-10 | 51 | 35 | 16 | 0 |

### v2.1 (current) -- 51 entries

| Dataset | N | p | G | S | E | Class |
|---------|---|---|---|---|---|---|
| AAUP College Faculty Salary | 1,161 | 9 | 52 | 0.90 | 1.03 | Reliable |
| ASSISTments 2009-2010 | 3,729 | 5 | 124 | 0.95 | 0.95 | Reliable |
| Abalone Age (Sex groups) | 4,177 | 7 | 3 | 0.93 | 1.48 | Reliable |
| Air Quality — NOx | 93,527 | 6 | 1 | -0.30 | -0.00 | Void |
| Airfoil Noise (Freq) | 1,503 | 4 | 3 | 0.76 | 0.78 | Reliable |
| Auto MPG (Origin groups) | 392 | 6 | 3 | 0.96 | 1.44 | Reliable |
| Bike Sharing (Season) | 731 | 10 | 4 | 0.96 | 1.77 | Reliable |
| Boston Housing (Region groups) | 506 | 13 | 4 | 0.92 | 1.72 | Reliable |
| Breast Cancer — Survival | 569 | 30 | 2 | 1.00 | 1.86 | Reliable |
| CPU Activity | 1,600 | 64 | 0 | -37.24 | 0.00 | Void |
| California Housing — Median Value | 20,640 | 8 | 30 | 0.98 | 0.93 | Reliable |
| Colleges US News Rankings | 1,204 | 31 | 51 | 0.88 | 1.04 | Reliable |
| Combined Cycle Power (Temp) | 9,568 | 3 | 3 | 0.99 | 1.74 | Reliable |
| Concrete Strength (Age) | 1,030 | 7 | 3 | 0.89 | 0.88 | Reliable |
| Credit Card — Transaction Amount | 50,000 | 30 | 2 | -0.31 | 0.01 | Void |
| Customer Churn — Telecom | 7,043 | 11 | 2 | -0.20 | 0.99 | Void |
| Diabetes — Disease Progression | 442 | 10 | 3 | 0.90 | 0.51 | Reliable |
| Energy Building (Orientation) | 768 | 7 | 4 | 0.99 | 1.93 | Reliable |
| Energy Efficiency (Rating groups) | 462 | 8 | 4 | 0.48 | 1.15 | Reliable |
| Entrance Exam | 666 | 49 | 3 | 0.88 | 0.97 | Reliable |
| German Credit — Loan Amount | 1,000 | 19 | 10 | -0.17 | 0.92 | Void |
| Higher Education Students Performance | 145 | 30 | 9 | -5.25 | 0.41 | Void |
| KDD Cup 2010 (Algebra I 2005-2006) | 574 | 5 | 22 | 0.95 | 1.18 | Reliable |
| Kaggle Students Performance in Exams | 1,000 | 17 | 5 | 0.81 | 1.00 | Reliable |
| Law School Admission | 20,800 | 7 | 6 | 0.96 | 0.73 | Reliable |
| Linnerud — Fitness | 20 | 3 | 2 | -6.67 | 2.52 | Void |
| MM-TBA Teaching Behavior Analysis | 186 | 13 | 0 | -0.77 | -0.03 | Void |
| MathE Mathematics Learning | 833 | 26 | 14 | -1.64 | 0.63 | Void |
| OLI Engineering Statics 2011 | 194,947 | 2 | 19 | 0.96 | 0.71 | Reliable |
| Open University Learning Analytics Dataset | 32,593 | 52 | 22 | 0.98 | 1.17 | Reliable |
| PISA 2015 Science | 519,334 | 2 | 73 | -0.10 | 0.66 | Void |
| Pollution (Station groups) | 263,256 | 14 | 10 | 0.56 | 1.00 | Reliable |
| Real Estate Valuation (Stores) | 414 | 4 | 3 | 0.84 | 1.52 | Reliable |
| Sea Level Prediction | 758 | 5 | 2 | -0.59 | 0.98 | Void |
| Seoul Bike Sharing (Season) | 8,760 | 9 | 4 | 0.97 | 1.46 | Reliable |
| Sports Performance — Team | 2,000 | 15 | 8 | -0.29 | 0.97 | Void |
| Student Depression Survey | 27,875 | 21 | 30 | 0.98 | 1.37 | Reliable |
| Student Dropout and Academic Success | 3,630 | 36 | 17 | 0.97 | 1.30 | Reliable |
| Students Exam Scores (Kaggle) | 30,641 | 17 | 5 | 0.97 | 1.04 | Reliable |
| Sulfate Ion (Station groups) | 905 | 17 | 4 | 0.91 | 1.70 | Reliable |
| Teaching Assistant Evaluation | 151 | 4 | 25 | -0.42 | 0.75 | Void |
| Turkiye Student Evaluation | 5,820 | 28 | 13 | 0.56 | 0.70 | Reliable |
| UCI Nursery School Applications | 12,960 | 24 | 3 | 1.00 | 1.95 | Reliable |
| UCI Student Absences (Kaggle) | 395 | 55 | 2 | -0.76 | 0.29 | Void |
| UCI Student Health (Por, Mjob) | 649 | 53 | 5 | -3.15 | 0.67 | Void |
| UCI Student Performance | 649 | 56 | 2 | 0.62 | 1.06 | Reliable |
| UCI Student Performance (Math) | 395 | 56 | 2 | -2.67 | 0.43 | Void |
| US College Scorecard | 2,220 | 30 | 55 | 0.82 | 0.69 | Reliable |
| Wine Quality (Red+White) | 6,497 | 11 | 2 | 0.93 | 0.93 | Reliable |
| Yacht Hydrodynamics (Hull groups) | 7,400 | 20 | 4 | 0.93 | 1.29 | Reliable |
| xAPI-Edu-Data | 480 | 72 | 12 | 0.89 | 1.34 | Reliable |

### BRF Metric Definitions

S = N - I (Stability), E = B + M (Evidence).

## Key Findings (v2.1, N=51)

- **No Fragile datasets** across 51 multi-domain benchmarks. Rule-of-three upper bound ~8%.
- **Bimodal**: 35 Reliable, 16 Void -- no intermediate regime under the original S formulation.
- **Multi-domain**: 25 educational + 26 cross-domain benchmarks spanning health, finance, environment, energy, transportation, and systems.
- **Grouping sensitivity**: Same data, different grouping can shift E by 0.35-0.85.
- **Self-contained**: 39 source modules covering all 51 datasets, 0 external dependencies.

## License

Code: MIT. Individual datasets have their own licenses (see registry metadata).
