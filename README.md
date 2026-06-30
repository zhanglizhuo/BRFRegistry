# BRF Benchmark Registry v1

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

## Registry Contents (v1)

See `results/registry_v1.json` for full BRF audit results.

## License

The code in this repository is MIT. Individual datasets have their own
licenses (see registry metadata).
