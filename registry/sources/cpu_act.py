"""CPU Activity (UCI). 852 samples, 27 features, target: cpu time.
Group: cpu type (4 types)."""
import pandas as pd
import numpy as np
import io

from . import DatasetSource, register_source

@register_source
class CpuActSource(DatasetSource):
    name = "cpu_act"
    display_name = "CPU Activity (Type groups)"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/11/cpu+activity.zip"
    license_info = "UCI Open Data Policy"
    reference = "UCI ID 11"
    task = "regression"
    n_samples = 852
    n_features = 27
    n_groups = 4
    grouping_description = "CPU type (4 types)"

    def download(self):
        import urllib.request
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "cpu_act.csv"
        if csv_path.exists():
            return csv_path
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/cpu_activity/cpu_act.data"
        resp = urllib.request.urlopen(url, timeout=30)
        lines = resp.read().decode().strip().split('\n')
        # First line is CPU types
        cpu_types = lines[0].strip().split()
        # Data starts from line 2
        cols = ['cpu'] + [f'f{i}' for i in range(1, 28)]
        data_lines = [l for l in lines[1:] if not l.startswith('#')]
        df = pd.read_csv(io.StringIO('\n'.join(data_lines)), sep='\s+', header=None, names=cols)
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["f28"].values.astype(float)
        feature_cols = [f'f{i}' for i in range(1, 28)]
        X = df[feature_cols].values.astype(float)
        groups = df["cpu"].astype("category").cat.codes.values
        meta = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "UCI CPU Activity"}
        return X, y, groups, meta
