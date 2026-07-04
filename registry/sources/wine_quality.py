"""Wine Quality (UCI ID 186) — cross-domain benchmark.

Non-educational regression benchmark for cross-domain comparison.
Target: quality rating (0-10). Group: wine type (red/white, 2 groups).
Used as out-of-domain test for the BRF Fragile hypothesis.
"""

import numpy as np
import shutil

from . import DatasetSource, register_source


@register_source
class WineQualitySource(DatasetSource):
    name = "wine_quality"
    display_name = "Wine Quality (Red+White)"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/186/wine+quality.zip"
    license_info = "CC BY 4.0"
    reference = "Cortez et al. (2009); UCI ID 186"
    task = "regression"
    n_samples = 6497
    n_features = 11
    n_groups = 2
    grouping_description = "Wine type (red/white, 2 groups)"
    sha256 = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1"

    def download(self):
        import urllib.request, zipfile, io
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "winequality-combined.csv"
        if csv_path.exists():
            return csv_path
        resp = urllib.request.urlopen(self.source_url, timeout=60)
        with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
            z.extractall(str(dest_dir))
        # Combine red and white wine CSVs
        import pandas as pd
        red_path = next(dest_dir.glob("**/*red*"), None)
        white_path = next(dest_dir.glob("**/*white*"), None)
        if red_path and white_path:
            red = pd.read_csv(str(red_path), sep=';')
            white = pd.read_csv(str(white_path), sep=';')
            red['type'] = 'red'
            white['type'] = 'white'
            combined = pd.concat([red, white], ignore_index=True)
            combined.to_csv(str(csv_path), index=False)
            return csv_path
        return dest_dir

    def prepare(self):
        import pandas as pd

        path = self.download()
        df = pd.read_csv(str(path))
        y = df["quality"].values.astype(float)
        groups = df["type"].astype(str).values
        feat_df = df.drop(columns=["quality", "type"])
        X = feat_df.fillna(0).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": df["type"].nunique(),
                "source": "UCI ID 186 (Wine Quality, red+white combined)",
                "features": list(feat_df.columns)}
        return X, y, groups, card
