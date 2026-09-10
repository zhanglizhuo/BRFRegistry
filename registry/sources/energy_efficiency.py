"""Energy Efficiency (OpenML 1498). 462 samples, 8 features, target: heating load.
Group: overall rating bins (4 groups)."""
import pandas as pd
import numpy as np

from . import DatasetSource, register_source

@register_source
class EnergyEfficiencySource(DatasetSource):
    name = "energy_efficiency"
    display_name = "Energy Efficiency (Rating groups)"
    version = "1.0"
    source_url = "https://www.openml.org/d/1498"
    license_info = "CC0"
    reference = "OpenML 1498"
    task = "regression"
    n_samples = 462
    n_features = 8
    n_groups = 4
    grouping_description = "Overall rating bins (4 groups)"

    def download(self):
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "energy_efficiency.csv"
        if csv_path.exists():
            return csv_path
        from sklearn.datasets import fetch_openml
        ds = fetch_openml(data_id=1498, as_frame=False, parser='auto')
        df = pd.DataFrame(ds.data.astype(float), columns=[f'f{i}' for i in range(ds.data.shape[1])])
        df['y'] = ds.target.astype(float)
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["y"].values.astype(float)
        X = df[[f'f{i}' for i in range(8)]].values.astype(float)
        groups = pd.qcut(df["f8"], 4, labels=False, duplicates='drop').values
        meta = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "OpenML 1498"}
        return X, y, groups, meta
