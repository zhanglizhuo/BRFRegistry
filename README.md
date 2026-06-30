# BRF Benchmark Registry

Versioned, DOI-tracked collection of group-aware educational benchmark datasets
audited under the Benchmark Reliability Framework (BRF).

Dataset-as-Code architecture: each dataset is a Python module with
download -> verify -> prepare pipeline for full reproducibility.

## Quick Start

```bash
# Install BRF
pip install benchmark-reliability

# List all datasets
python -m registry.cli list

# Download and verify a dataset
python -m registry.cli download tae
python -m registry.cli verify tae

# Sync all (download + verify all datasets)
python -m registry.cli sync

# Show metadata
python -m registry.cli info oulad

# Run BRF on all registered datasets
python run_registry.py
```

## Structure

```
BRFRegistry/
|-- registry/
|   |-- sources/          # One .py per dataset (DatasetSource subclass)
|   |-- cache/            # Downloaded data (gitignored)
|   |-- manifest.yaml     # Registry version + dataset index
|   |-- cli.py            # CLI: list, download, verify, sync, info
|   |-- verify.py         # SHA-256 verification
|   `-- known_datasets.py # Legacy metadata registry
|-- results/              # BRF audit results (JSON)
|-- run_registry.py       # Run BRF on all registered datasets
`-- ROADMAP.md            # Project roadmap & paper definitions
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

| Version | Date | Datasets | Reliable | Void | Fragile |
|---------|------|----------|----------|------|---------|
| v1.0 | 2026-06-28 | 7 | 4 | 3 | 0 |
| v1.5 | 2026-07-01 | 25 | 20 | 5 | 0 |

### v1.5 (current) -- 25 datasets

| Dataset                                   | N      | p  | G   | B     | I    | Stab | M    | S     | E     | Class    |
|-------------------------------------------|--------|----|-----|-------|------|------|------|-------|-------|----------|
| ASSISTments 2009-2010                     | 3729   | 5  | 124 | 0.51  | 0.05 | 1.00 | 0.44 | 0.95  | 0.95  | Reliable |
| ASSISTments 2009-2010 (by school)         | 3729   | 5  | 58  | 0.51  | 0.05 | 1.00 | 0.39 | 0.95  | 0.90  | Reliable |
| US College Scorecard                      | 2220   | 30 | 55  | 0.24  | 0.18 | 1.00 | 0.45 | 0.82  | 0.69  | Reliable |
| US College Scorecard (by Carnegie)        | 1902   | 27 | 22  | 0.30  | 0.19 | 1.00 | 0.42 | 0.81  | 0.71  | Reliable |
| US College Scorecard (by ownership)       | 2220   | 27 | 3   | 0.24  | 0.18 | 1.00 | 0.74 | 0.82  | 0.98  | Reliable |
| US College Scorecard (by region)          | 2220   | 27 | 9   | 0.24  | 0.18 | 1.00 | 0.63 | 0.82  | 0.87  | Reliable |
| Colleges AAUP                             | 1161   | 9  | 52  | 0.48  | 0.10 | 1.00 | 0.54 | 0.90  | 1.03  | Reliable |
| Colleges AAUP (by type)                   | 1161   | 9  | 4   | 0.48  | 0.10 | 1.00 | 0.47 | 0.90  | 0.95  | Reliable |
| Colleges US News                          | 1204   | 31 | 51  | 0.50  | 0.12 | 1.00 | 0.54 | 0.88  | 1.04  | Reliable |
| Entrance Exam                             | 666    | 49 | 3   | 0.46  | 0.12 | 1.00 | 0.51 | 0.88  | 0.97  | Reliable |
| Higher Ed                                 | 145    | 31 | 9   | 0.17  | 2.00 | 0.97 | 0.39 | -1.03 | 0.56  | Void     |
| Law School Admission                      | 20800  | 10 | 6   | 0.18  | 0.04 | 1.00 | 0.55 | 0.96  | 0.73  | Reliable |
| MathE                                     | 833    | 26 | 14  | 0.03  | 2.47 | 0.83 | 0.60 | -1.64 | 0.63  | Void     |
| MM-TBA                                    | 186    | 13 | 0   | -0.03 | 1.44 | 0.67 | 0.00 | -0.77 | -0.03 | Void     |
| OLI Engineering Statics 2011              | 194947 | 2  | 19  | 0.04  | 0.04 | 1.00 | 0.67 | 0.96  | 0.71  | Reliable |
| OULAD                                     | 32593  | 44 | 22  | 0.47  | 0.02 | 1.00 | 0.77 | 0.98  | 1.24  | Reliable |
| PISA 2015 Science                         | 519334 | 2  | 73  | 0.00  | 0.13 | 0.03 | 0.66 | -0.10 | 0.66  | Void     |
| Student Depression Survey                 | 27875  | 21 | 30  | 0.52  | 0.02 | 1.00 | 0.85 | 0.98  | 1.37  | Reliable |
| Student Depression Survey (by degree)     | 27901  | 21 | 28  | 0.52  | 0.02 | 1.00 | 0.45 | 0.98  | 0.97  | Reliable |
| Student Depression Survey (by profession) | 27884  | 21 | 3   | 0.52  | 0.02 | 1.00 | 0.00 | 0.98  | 0.52  | Reliable |
| Student Dropout                           | 3630   | 36 | 17  | 0.66  | 0.03 | 1.00 | 0.65 | 0.97  | 1.30  | Reliable |
| Teaching Assistant Evaluation             | 151    | 4  | 25  | 0.12  | 1.36 | 0.93 | 0.63 | -0.42 | 0.75  | Void     |
| Turkiye Student Evaluation                | 5820   | 28 | 13  | 0.02  | 0.44 | 1.00 | 0.68 | 0.56  | 0.70  | Reliable |
| UCI Student                               | 649    | 56 | 2   | 0.24  | 0.38 | 1.00 | 0.81 | 0.62  | 1.06  | Reliable |
| xAPI-Edu-Data                             | 480    | 72 | 12  | 0.66  | 0.11 | 1.00 | 0.69 | 0.89  | 1.34  | Reliable |

### BRF Metric Definitions

| Metric | Formula | Meaning |
|--------|---------|---------|
| B | mean(Delta(R^2) vs mean baseline) | Predictive signal strength |
| I | std(R^2) / max(|mean(R^2)|, 1e-4) + 1e-8 | Intrinsic instability |
| N | fraction of folds where R^2_real > median(R^2_perm) | Null separation |
| M | 0.5 * norm_group_entropy + 0.5 * group_balance | Metadata adequacy |
| S | N - I | Stability (signal - noise) |
| E | B + M | Evidence (predictive + structural) |

Classification: Void if S <= 0, Fragile if S > 0 and E <= 0.5, Reliable otherwise.

## Key Findings (v1.5, N=25)

- **Fragile regime unobserved**: The condition S>0 and E<=0.5 has not appeared
  in any dataset. The closest case is Student Depression by Profession (E=0.52).
- **Grouping sensitivity**: Identical data with different grouping levels yields
  vastly different M and E values while S stays constant.
- **Void causes are diverse**: small N (Higher Ed), low feature density (TAE),
  no grouping metadata (MM-TBA), cross-domain transfer failure (MathE),
  zero predictive signal (PISA).

## License

Code: MIT. Individual datasets have their own licenses (see registry metadata).
