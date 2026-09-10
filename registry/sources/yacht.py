"""Yacht Hydrodynamics (OpenML 1496). 7400 samples, 20 features, target: drag force.
Group: hull length bins (4 groups)."""
import pandas as pd
import numpy as np

from . import DatasetSource, register_source

@register_source
class YachtSource(DatasetSource):
    name = "yacht"
    display_name = "Yacht Hydrodynamics (Hull groups)"
    version = "1.0"
    source_url = "https://www.openml.org/d/1496"
    license_info = "CC0"
    reference = "OpenML 1496"
    task = "regression"
    n_samples = 7400
    n_features = 20
    n_groups = 4
    grouping_description = "Hull length bins (4 groups)"

    def download(self):
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "yacht.csv"
        if csv_path.exists():
            return csv_path
        from sklearn.datasets import fetch_openml
        ds = fetch_openml(data_id=1496, as_frame=False, parser='auto')
        df = pd.DataFrame(ds.data.astype(float), columns=[f'f{i}' for i in range(ds.data.shape[1])])
        df['y'] = ds.target.astype(float)
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["y"].values.astype(float)
        X = df[[f'f{i}' for i in range(20)]].values.astype(float)
        groups = pd.qcut(df["f0"], 4, labels=False, duplicates='drop').values
        meta = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "OpenML 1496"}
        return X, y, groups, meta
