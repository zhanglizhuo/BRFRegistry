"""California Housing (OpenML 574). 22784 samples, 16 features, target: median value.
Group: ocean proximity (5 categories)."""
import pandas as pd
import numpy as np

from . import DatasetSource, register_source

@register_source
class CaliforniaHousingSource(DatasetSource):
    name = "california_housing"
    display_name = "California Housing (Ocean proximity groups)"
    version = "1.0"
    source_url = "https://www.openml.org/d/574"
    license_info = "Public domain"
    reference = "OpenML 574"
    task = "regression"
    n_samples = 22784
    n_features = 16
    n_groups = 5
    grouping_description = "Ocean proximity (5 categories)"

    def download(self):
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "california_housing.csv"
        if csv_path.exists():
            return csv_path
        from sklearn.datasets import fetch_openml
        ds = fetch_openml(data_id=574, as_frame=False, parser='auto')
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
        groups = pd.qcut(df["f0"], 5, labels=False, duplicates='drop').values
        meta = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "OpenML 574"}
        return X, y, groups, meta
