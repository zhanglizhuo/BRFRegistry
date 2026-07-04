"""Seoul Bike Sharing (UCI ID 560). rented bike count. Group: season (4: Spring/Summer/Autumn/Winter)."""
import pandas as pd

from . import DatasetSource, register_source

@register_source
class SeoulBikeSource(DatasetSource):
    name = "seoul_bike"
    display_name = "Seoul Bike Sharing (Season)"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/560/seoul+bike+sharing+demand.zip"
    license_info = "CC BY 4.0"
    reference = "Sathishkumar et al. (2020); UCI ID 560"
    task = "regression"
    n_samples = 8760
    n_features = 11
    n_groups = 4
    grouping_description = "Season (4: Spring/Summer/Autumn/Winter)"
    sha256 = "827e5d046b09f52c546646a1a492ddf8c71ff61edd9b032894f846e37b2f9576"

    def download(self):
        import urllib.request
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "seoul_bike.csv"
        if csv_path.exists():
            return csv_path
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00560/SeoulBikeData.csv"
        df = pd.read_csv(url, encoding='latin-1')
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["Rented Bike Count"].values.astype(float)
        groups = df["Seasons"].astype(str).values
        drop_cols = ["Rented Bike Count", "Seasons", "Date", "Holiday", "Functioning Day"]
        feat_df = df.drop(columns=[c for c in drop_cols if c in df.columns])
        X = feat_df.fillna(0).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": df["Seasons"].nunique(), "source": "UCI ID 560",
                "features": list(feat_df.columns)}
        return X, y, groups, card
