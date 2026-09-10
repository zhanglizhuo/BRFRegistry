"""Diabetes (OpenML 1491). 1600 samples, 64 features, target: disease progression.
Group: sex (Male/Female)."""
import pandas as pd
import numpy as np

from . import DatasetSource, register_source

@register_source
class DiabetesSource(DatasetSource):
    name = "diabetes"
    display_name = "Diabetes (Sex groups)"
    version = "1.0"
    source_url = "https://www.openml.org/d/1491"
    license_info = "CC BY 4.0"
    reference = "OpenML 1491"
    task = "regression"
    n_samples = 1600
    n_features = 64
    n_groups = 2
    grouping_description = "Sex (Male/Female)"

    def download(self):
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "diabetes.csv"
        if csv_path.exists():
            return csv_path
        from sklearn.datasets import fetch_openml
        ds = fetch_openml(data_id=1491, as_frame=False, parser='auto')
        df = pd.DataFrame(ds.data.astype(float), columns=[f'f{i}' for i in range(ds.data.shape[1])])
        df['y'] = ds.target.astype(float)
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["y"].values.astype(float)
        n_feat = df.shape[1] - 1
        X = df[[f'f{i}' for i in range(n_feat)]].values.astype(float)
        groups = (df["f0"].values > np.median(df["f0"].values)).astype(int)
        meta = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": 2, "source": "OpenML 1491"}
        return X, y, groups, meta
