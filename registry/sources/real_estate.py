"""Real Estate Valuation (UCI ID 477). house price per unit area. Group: convenience stores binned (0-2, 3-5, 6+)."""
import numpy as np
import pandas as pd
import io

from . import DatasetSource, register_source

@register_source
class RealEstateSource(DatasetSource):
    name = "real_estate"
    display_name = "Real Estate Valuation (Stores)"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/477/real+estate+valuation+data+set.zip"
    license_info = "CC BY 4.0"
    reference = "Yeh & Hsu (2018); UCI ID 477"
    task = "regression"
    n_samples = 414
    n_features = 4
    n_groups = 3
    grouping_description = "Convenience stores binned (0-2, 3-5, 6+)"
    sha256 = "e0074220e235164e8fe010e055a94a4aed8bf484e0e33d7f8efc65e1b6a48b5e"

    def download(self):
        import urllib.request
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "real_estate.csv"
        if csv_path.exists():
            return csv_path
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00477/Real%20estate%20valuation%20data%20set.xlsx"
        resp = urllib.request.urlopen(url, timeout=30)
        df = pd.read_excel(io.BytesIO(resp.read()))
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["Y house price of unit area"].values.astype(float)
        stores = df["X4 number of convenience stores"].values
        groups = np.where(stores <= 2, 'low', np.where(stores <= 5, 'mid', 'high'))
        drop_cols = ["No", "Y house price of unit area", "X4 number of convenience stores",
                     "X1 transaction date"]
        feat_df = df.drop(columns=[c for c in drop_cols if c in df.columns])
        X = feat_df.fillna(0).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(np.unique(groups)), "source": "UCI ID 477",
                "features": list(feat_df.columns)}
        return X, y, groups, card
