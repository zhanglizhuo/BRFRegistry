"""Auto MPG (UCI ID 9).

Classic regression benchmark. 398 rows, 7 features.
Target: mpg (miles per gallon). Group: origin (1=US, 2=Europe, 3=Japan).
Non-educational cross-domain benchmark.
"""

import numpy as np
import pandas as pd
import io

from . import DatasetSource, register_source


@register_source
class AutoMPGSource(DatasetSource):
    name = "auto_mpg"
    display_name = "Auto MPG (Origin groups)"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/9/auto+mpg.zip"
    license_info = "CC BY 4.0"
    reference = "Quinlan (1993); UCI ID 9"
    task = "regression"
    n_samples = 398
    n_features = 9
    n_groups = 3
    grouping_description = "Origin (1=US, 2=Europe, 3=Japan)"
    sha256 = "b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b"

    def download(self):
        import urllib.request
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "auto-mpg.csv"
        if csv_path.exists():
            return csv_path
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
        resp = urllib.request.urlopen(url, timeout=30)
        cols = ['mpg','cylinders','displacement','horsepower','weight','acceleration','model_year','origin','car_name']
        df = pd.read_csv(io.StringIO(resp.read().decode()), delim_whitespace=True, header=None, names=cols)
        df['horsepower'] = pd.to_numeric(df['horsepower'], errors='coerce')
        df = df.dropna(subset=['horsepower'])
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["mpg"].values.astype(float)
        groups = df["origin"].astype(str).values
        feat_df = df.drop(columns=["mpg", "origin", "car_name"], errors='ignore')
        X = feat_df.fillna(0).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": df["origin"].nunique(), "source": "UCI ID 9",
                "features": list(feat_df.columns)}
        return X, y, groups, card
