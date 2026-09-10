"""Sulfate Ion (OpenML 411). 905 samples, 17 features, target: sulfate concentration.
Group: sampling station (4 stations)."""
import pandas as pd
import numpy as np

from . import DatasetSource, register_source

@register_source
class SulfateIonSource(DatasetSource):
    name = "sulfate_ion"
    display_name = "Sulfate Ion (Station groups)"
    version = "1.0"
    source_url = "https://www.openml.org/d/411"
    license_info = "CC0"
    reference = "OpenML 411"
    task = "regression"
    n_samples = 905
    n_features = 17
    n_groups = 4
    grouping_description = "Sampling station (4 locations)"

    def download(self):
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "sulfate_ion.csv"
        if csv_path.exists():
            return csv_path
        from sklearn.datasets import fetch_openml
        ds = fetch_openml(data_id=411, as_frame=False, parser='auto')
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
        groups = pd.qcut(df["f0"], 4, labels=False, duplicates='drop').values
        meta = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "OpenML 411"}
        return X, y, groups, meta
