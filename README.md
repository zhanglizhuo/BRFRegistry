# BRF Benchmark Registry

The **BRF Benchmark Registry** is a versioned, DOI-tracked collection of
group-aware educational prediction benchmarks audited under the
**Benchmark Reliability Framework (BRF)**.

> Registry v1.6 : 27 entries (20 unique + 7 alt views) | 21 Reliable | 6 Void | 0 Fragile

**Architecture**: Dataset-as-Code — each dataset is a self-contained Python
module with `download → verify → prepare` pipeline. 0 external dependencies.

## Quick Start

```bash
pip install benchmark-reliability

# Browse the Registry
brf registry list              # 20 datasets
brf registry info tae          # full metadata
brf registry sync              # download + verify all
brf audit tae                  # run BRF on a dataset
```

## Structure

```
BRFRegistry/
|-- registry/
|   |-- sources/          # 20 DatasetSource .py files (auto-discovered)
|   |-- cards/            # 20 machine-readable YAML Dataset Cards
|   |-- cache/            # Downloaded data (gitignored)
|   |-- manifest.yaml     # Registry version + dataset index
|   |-- taxonomy.yaml     # 5-level benchmark taxonomy
|   |-- version_policy.yaml # Lifecycle + deprecation rules
|   |-- cli.py            # CLI: list, download, verify, sync, info
|   |-- verify.py         # SHA-256 verification
|   `-- known_datasets.py # Legacy metadata registry
|-- results/
|   `-- registry_v1.5.json # 27 entries with BRF results + enriched metadata
`-- run_registry.py        # Run BRF on all registered datasets
```

## Adding a Dataset

Drop a `.py` file in `registry/sources/` implementing a `DatasetSource` subclass
decorated with `@register_source`. Auto-discovered on next import.

```python
from registry.sources import DatasetSource, register_source

@register_source
class MyDataset(DatasetSource):
    name = "my_dataset"
    display_name = "My Dataset"
    source_url = "https://..."
    license_info = "CC BY 4.0"
    task = "regression"
    n_samples = 1000
    n_features = 10
    n_groups = 20
    grouping_description = "School (20 schools)"

    def download(self):
        # Download from source_url, cache locally
        ...

    def prepare(self):
        # Return (X, y, groups, metadata_card)
        ...
```

## Registry Contents

| Version | Date | Entries | Unique | Alt Views | Reliable | Void | Fragile |
|---------|------|---------|--------|-----------|----------|------|---------|
| v1.0 | 2026-03-28 | 7 | 7 | 0 | 4 | 3 | 0 |
| v1.6 | 2026-07-01 | 27 | 20 | 7 | 21 | 6 | 0 |

### v1.5 (current) — 27 entries

| Dataset | N | p | G | S | E | Class |
|---------|---|---|---|---|---|---|-------|
| ASSISTments 2009-2010 | 3.7K | 5 | 124 | 0.95 | 0.95 | Reliable |
| ASSISTments 2009-2010 (by school) | 3.7K | 5 | 58 | 0.95 | 0.90 | Reliable |
| US College Scorecard | 2.2K | 30 | 55 | 0.82 | 0.69 | Reliable |
| US College Scorecard (by Carnegie) | 1.9K | 27 | 22 | 0.81 | 0.71 | Reliable |
| US College Scorecard (by ownership) | 2.2K | 27 | 3 | 0.82 | 0.98 | Reliable |
| US College Scorecard (by region) | 2.2K | 27 | 9 | 0.82 | 0.87 | Reliable |
| Colleges AAUP | 1.2K | 9 | 52 | 0.90 | 1.03 | Reliable |
| Colleges AAUP (by type) | 1.2K | 9 | 4 | 0.90 | 0.95 | Reliable |
| Colleges US News | 1.2K | 31 | 51 | 0.88 | 1.04 | Reliable |
| Entrance Exam | 666 | 49 | 3 | 0.88 | 0.97 | Reliable |
| Higher Ed | 145 | 31 | 9 | -1.03 | 0.56 | Void |
| Law School Admission | 20.8K | 7 | 6 | 0.96 | 0.73 | Reliable |
| MathE | 833 | 26 | 14 | -1.64 | 0.63 | Void |
| MM-TBA | 186 | 13 | 0 | -0.77 | -0.03 | Void |
| OLI Engineering Statics 2011 | 195K | 2 | 19 | 0.96 | 0.71 | Reliable |
| OULAD | 32.6K | 44 | 22 | 0.98 | 1.24 | Reliable |
| PISA 2015 Science | 519K | 2 | 73 | -0.10 | 0.66 | Void |
| Student Depression Survey | 27.9K | 21 | 30 | 0.98 | 1.37 | Reliable |
| Student Depression Survey (by degree) | 27.9K | 21 | 28 | 0.98 | 0.97 | Reliable |
| Student Depression Survey (by profession) | 27.9K | 21 | 3 | 0.98 | 0.52 | Reliable |
| Student Dropout | 3.6K | 36 | 17 | 0.97 | 1.30 | Reliable |
| Students Exam Scores (Kaggle) | 30.6K | 17 | 5 | 0.97 | 1.04 | Reliable |
| Teaching Assistant Evaluation | 151 | 4 | 25 | -0.42 | 0.75 | Void |
| Turkiye Student Evaluation | 5.8K | 28 | 13 | 0.56 | 0.70 | Reliable |
| UCI Student | 649 | 56 | 2 | 0.62 | 1.06 | Reliable |
| UCI Student (Math) | 395 | 56 | 2 | -2.67 | 0.43 | Void |
| xAPI-Edu-Data | 480 | 72 | 12 | 0.89 | 1.34 | Reliable |

### BRF Metric Definitions

S = N - I (Stability), E = B + M (Evidence).
See `results/registry_v1.5.json` for full B, I, N, M values.

## Key Findings (v1.5, N=27)

- **Fragile absent**: Across 27 entries, 0 Fragile. Rule-of-three upper bound ~11%.
- **Bimodal**: 21 Reliable, 6 Void — no intermediate regime.
- **Grouping sensitivity**: Same data, different grouping → E shifts by 0.35–0.85.
- **Self-contained**: 20/20 source modules independent (0 BA dependencies).
- **SHA-256**: 9/11 direct-download entries verified (82%).

## License

Code: MIT. Individual datasets have their own licenses (see registry metadata).
