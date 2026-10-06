"""Boston Housing (OpenML 531). 506 samples, 13 features, target: median value.
Group: quartile bins of feature f5 (4 groups)."""
import pandas as pd
import numpy as np

from . import DatasetSource, register_source

@register_source
class BostonHousingSource(DatasetSource):
    name = "boston_housing"
    display_name = "Boston Housing (Quartile groups)"
    version = "1.0"
    source_url = "https://www.openml.org/d/531"
    license_info = "Public domain"
    reference = "OpenML 531"
    task = "regression"
    n_samples = 506
    n_features = 13
    n_groups = 4
    grouping_description = "Quartile bins of feature f5 (4 groups)"

    def download(self):
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "boston_housing.csv"
        if csv_path.exists():
            return csv_path
        from sklearn.datasets import fetch_openml
        ds = fetch_openml(data_id=531, as_frame=False, parser='auto')
        df = pd.DataFrame(ds.data.astype(float), columns=[f'f{i}' for i in range(ds.data.shape[1])])
        df['y'] = ds.target.astype(float)
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["y"].values.astype(float)
        X = df[[f'f{i}' for i in range(13)]].values.astype(float)
        groups = pd.qcut(df["f5"], 4, labels=False, duplicates='drop').values
        meta = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "OpenML 531"}
        return X, y, groups, meta
