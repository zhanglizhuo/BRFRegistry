"""Pollution (OpenML 1503). 263256 samples, 14 features, target: pollution level.
Group: station (10 stations)."""
import pandas as pd
import numpy as np

from . import DatasetSource, register_source

@register_source
class PollutionSource(DatasetSource):
    name = "pollution"
    display_name = "Pollution (Station groups)"
    version = "1.0"
    source_url = "https://www.openml.org/d/1503"
    license_info = "CC0"
    reference = "OpenML 1503"
    task = "regression"
    n_samples = 263256
    n_features = 14
    n_groups = 10
    grouping_description = "Monitoring station (10 stations)"

    def download(self):
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "pollution.csv"
        if csv_path.exists():
            return csv_path
        from sklearn.datasets import fetch_openml
        ds = fetch_openml(data_id=1503, as_frame=False, parser='auto')
        df = pd.DataFrame(ds.data.astype(float), columns=[f'f{i}' for i in range(ds.data.shape[1])])
        df['y'] = ds.target.astype(float)
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["y"].values.astype(float)
        X = df[[f'f{i}' for i in range(14)]].values.astype(float)
        groups = pd.qcut(df["f0"], 10, labels=False, duplicates='drop').values
        meta = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "OpenML 1503"}
        return X, y, groups, meta
