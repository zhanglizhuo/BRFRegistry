"""Abalone Age Prediction (UCI ID 1). rings (age proxy, 1-29). Group: sex (M/F/I, 3 groups)."""
import pandas as pd

from . import DatasetSource, register_source

@register_source
class AbaloneSource(DatasetSource):
    name = "abalone"
    display_name = "Abalone Age (Sex groups)"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/1/abalone.zip"
    license_info = "CC BY 4.0"
    reference = "Nash et al. (1995); UCI ID 1"
    task = "regression"
    n_samples = 4177
    n_features = 10
    n_groups = 3
    grouping_description = "Sex (M/F/I, 3 groups)"
    sha256 = "a2daaed9c48ef860360f6438a224a2fde2576f1ebcf4f821ffe23645c229b23e"

    def download(self):
        import urllib.request
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "abalone.csv"
        if csv_path.exists():
            return csv_path
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data"
        resp = urllib.request.urlopen(url, timeout=30)
        cols = ['sex','length','diameter','height','whole_weight','shucked_weight','viscera_weight','shell_weight','rings']
        df = pd.read_csv(resp, header=None, names=cols)
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["rings"].values.astype(float)
        groups = df["sex"].astype(str).values
        feat_df = df.drop(columns=["rings", "sex"])
        X = feat_df.fillna(0).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": df["sex"].nunique(), "source": "UCI ID 1",
                "features": list(feat_df.columns)}
        return X, y, groups, card
