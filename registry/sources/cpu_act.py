"""CPU Activity (OpenML). 1600 samples, 64 features, target: CPU usage (0-100%)."""
import pandas as pd
import numpy as np

from . import DatasetSource, register_source

@register_source
class CpuActSource(DatasetSource):
    name = "cpu_act"
    display_name = "CPU Activity"
    version = "2.0"
    source_url = "https://www.openml.org/d/1492"
    license_info = "OpenML (public domain)"
    reference = "OpenML ID 1492"
    task = "regression"
    n_samples = 1600
    n_features = 64
    n_groups = 0
    grouping_description = "No group structure"

    def download(self):
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "cpu_act.csv"
        if csv_path.exists():
            return csv_path
        from sklearn.datasets import fetch_openml
        ds = fetch_openml(data_id=1492, as_frame=False, parser="auto")
        df = pd.DataFrame(ds.data, columns=[f"f{i}" for i in range(ds.data.shape[1])])
        df["y"] = ds.target.astype(float)
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["y"].values.astype(float)
        feature_cols = [f"f{i}" for i in range(64)]
        X = df[feature_cols].values.astype(float)
        meta = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": 0, "source": "OpenML CPU Activity"}
        return X, y, None, meta
