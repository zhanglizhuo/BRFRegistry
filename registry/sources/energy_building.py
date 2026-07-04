"""Energy Efficiency (UCI ID 242).

Building energy simulation. 768 rows, 8 features.
Target: heating load (Y1). Group: orientation (X6, 4 categories).
Non-educational cross-domain benchmark.
"""

import numpy as np
import pandas as pd

from . import DatasetSource, register_source


@register_source
class EnergyBuildingSource(DatasetSource):
    name = "energy_building"
    display_name = "Energy Building (Orientation)"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/242/energy+efficiency.zip"
    license_info = "CC BY 4.0"
    reference = "Tsanas & Xifara (2012); UCI ID 242"
    task = "regression"
    n_samples = 768
    n_features = 8
    n_groups = 4
    grouping_description = "Orientation (X6, 4 categories: 2/3/4/5)"
    sha256 = "c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c"

    def download(self):
        import urllib.request
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "energy_building.csv"
        if csv_path.exists():
            return csv_path
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00242/ENB2012_data.xlsx"
        import io
        resp = urllib.request.urlopen(url, timeout=30)
        df = pd.read_excel(io.BytesIO(resp.read()))
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["Y1"].values.astype(float)
        groups = df["X6"].astype(int).astype(str).values  # Orientation
        feat_df = df.drop(columns=["Y1", "Y2", "X6"])
        X = feat_df.fillna(0).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": df["X6"].nunique(), "source": "UCI ID 242",
                "features": list(feat_df.columns)}
        return X, y, groups, card
