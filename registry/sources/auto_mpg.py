"""Auto MPG (UCI ID 9). mpg (miles per gallon). Group: origin (1=US, 2=Europe, 3=Japan)."""
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
    n_samples = 392
    n_features = 6
    n_groups = 3
    grouping_description = "Origin (1=US, 2=Europe, 3=Japan)"
    sha256 = "15f00c8a120c8a86ac9faa16d47115c3e103764549a8c3c2fd6d5de31063636a"

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
