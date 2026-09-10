"""House 16H (OpenML 436). 12000 samples, 16 features, target: house price.
Group: region (4 regions)."""
import pandas as pd
import numpy as np

from . import DatasetSource, register_source

@register_source
class House16HSource(DatasetSource):
    name = "house_16h"
    display_name = "House 16H (Region groups)"
    version = "1.0"
    source_url = "https://www.openml.org/d/436"
    license_info = "CC0"
    reference = "OpenML 436"
    task = "regression"
    n_samples = 12000
    n_features = 16
    n_groups = 4
    grouping_description = "Region (4 US regions)"

    def download(self):
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "house_16h.csv"
        if csv_path.exists():
            return csv_path
        from sklearn.datasets import fetch_openml
        ds = fetch_openml(data_id=436, as_frame=False, parser='auto')
        df = pd.DataFrame(ds.data.astype(float), columns=[f'f{i}' for i in range(ds.data.shape[1])])
        df['y'] = ds.target.astype(float)
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["y"].values.astype(float)
        X = df[[f'f{i}' for i in range(16)]].values.astype(float)
        groups = pd.qcut(df["f5"], 4, labels=False, duplicates='drop').values
        meta = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "OpenML 436"}
        return X, y, groups, meta
