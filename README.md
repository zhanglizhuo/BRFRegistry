# BRF Benchmark Registry

Versioned, DOI-tracked collection of benchmark datasets audited under the
Benchmark Reliability Framework (BRF).

## Structure

```
BRFRegistry/
|-- registry/            # Python package: dataset metadata + adapters
|-- results/             # BRF audit results (JSON)
|-- data/                # (optional) processed dataset snapshots
|-- run_registry.py      # Run BRF on all registered datasets
```

## Usage

```bash
pip install benchmark-reliability
python run_registry.py
```

## Registry Contents

| Version | Date | Datasets | Reliable | Fragile | Void |
|---------|------|----------|----------|---------|------|
| v1.0 | 2026-06-28 | 7 | 4 | 0 | 3 |
| v1.5 | 2026-06-30 | 9 | 6 | 0 | 3 |

### v1.5 (current) -- 9 datasets

| Dataset | N | Features | Groups | Target | B | I | N | M | S | E | Class |
|---------|---|---|---------|--------|---|---|---|---|---|---|---|
| OULAD | 32593 | 44 | 22 | binary | 0.468 | 0.020 | 1.000 | 0.768 | 0.980 | 1.236 | Reliable |
| Student Dropout | 3630 | 36 | 17 | binary | 0.656 | 0.029 | 1.000 | 0.646 | 0.971 | 1.302 | Reliable |
| xAPI-Edu-Data | 480 | 72 | 12 | ordinal 3 | 0.655 | 0.110 | 1.000 | 0.689 | 0.890 | 1.344 | Reliable |
| Entrance Exam | 666 | 49 | 3 | ordinal 4 | 0.456 | 0.116 | 1.000 | 0.510 | 0.884 | 0.966 | Reliable |
| UCI Student | 649 | 56 | 2 | continuous | 0.243 | 0.377 | 1.000 | 0.815 | 0.623 | 1.058 | Reliable |
| Turkiye Student Eval | 5820 | 28 | 13 | ordinal 5 | 0.021 | 0.445 | 1.000 | 0.678 | 0.556 | 0.699 | Reliable |
| Higher Ed | 145 | 31 | 9 | continuous | 0.169 | 2.000 | 0.967 | 0.392 | -1.034 | 0.561 | Void |
| Teaching Assistant Eval | 151 | 4 | 25 | ordinal 3 | 0.117 | 1.356 | 0.933 | 0.629 | -0.423 | 0.746 | Void |
| MM-TBA | 186 | 13 | 0 | continuous | -0.034 | 1.436 | 0.667 | 0.000 | -0.769 | -0.034 | Void |

See `results/registry_v1.5.json` for full BRF audit results (v1.0 in `results/registry_v1.json`).

## Adding a Dataset

1. Add the adapter class in `registry/adapter.py` (see `TAEAdapter` or `TurkiyeAdapter` for examples)
2. Register metadata in `registry/known_datasets.py`
3. Run `python run_registry.py` to regenerate results

## License

The code in this repository is MIT. Individual datasets have their own
licenses (see registry metadata).
