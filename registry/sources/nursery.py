"""UCI Nursery School Applications (UCI ID 76).

Pre-primary education level. 12,960 rows, 8 categorical features.
Target: application decision (ordinal: not_recom/recommend/very_recom/priority/spec_prior).
Group: parents' occupation (3 groups: usual/pretentious/great_pret).
"""

import numpy as np

from . import DatasetSource, register_source


@register_source
class NurserySource(DatasetSource):
    name = "nursery"
    display_name = "UCI Nursery School Applications"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/76/nursery.zip"
    license_info = "CC BY 4.0"
    reference = "Olave, Rajkovic & Bohanec (1989); UCI ID 76"
    task = "regression"
    n_samples = 12960
    n_features = 24
    n_groups = 3
    sha256 = "8e0389c3dd37590248a921c2726d869ee96b817761a35eb8416afa24f31f931d"
    grouping_description = "Parents occupation (3: usual, pretentious, great_pret)"

    def download(self):
        import urllib.request, zipfile, io, shutil
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "nursery.csv"
        if csv_path.exists():
            return csv_path
        resp = urllib.request.urlopen(self.source_url, timeout=60)
        with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
            z.extractall(str(dest_dir))
        for f in dest_dir.glob("**/*.data"):
            shutil.copy(str(f), str(csv_path))
            return csv_path
        return dest_dir

    def prepare(self):
        import pandas as pd

        path = self.download()
        colnames = ["parents", "has_nurs", "form", "children", "housing",
                    "finance", "social", "health", "class"]
        df = pd.read_csv(str(path), names=colnames)
        
        # Ordinal target: not_recom=0, recommend=1, very_recom=2, priority=3, spec_prior=4
        order = {"not_recom": 0, "recommend": 1, "very_recom": 2,
                 "priority": 3, "spec_prior": 4}
        y = df["class"].map(order).values.astype(float)
        
        groups = df["parents"].astype(str).values
        feat_df = df.drop(columns=["class", "parents"])
        cat_cols = feat_df.select_dtypes(include=["object"]).columns.tolist()
        X_df = pd.get_dummies(feat_df, columns=cat_cols, dummy_na=False)
        X = X_df.fillna(0).astype(float).values
        
        # Ensure groups is not included in features to avoid leakage
        # (parents is excluded from feat_df above)
        
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": df["parents"].nunique(),
                "source": "UCI ID 76",
                "features": list(X_df.columns)[:8] + [f"... ({X.shape[1]} total)"]}
        return X, y, groups, card
