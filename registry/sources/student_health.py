"""UCI Student Health (Portuguese, Kaggle mirror, UCI ID 320). self-rated health (ordinal 1-5)."""
import shutil

from . import DatasetSource, register_source

@register_source
class StudentHealthSource(DatasetSource):
    name = "student_health"
    display_name = "UCI Student Health (Por, Mjob)"
    version = "1.0"
    source_url = "https://www.kaggle.com/datasets/uciml/student-alcohol-consumption"
    license_info = "CC BY 4.0"
    reference = "Cortez & Silva (2008); UCI ID 320 (Kaggle mirror, health target)"
    task = "regression"
    n_samples = 649
    n_features = 53
    n_groups = 5
    grouping_description = "Mother's Job (5: teacher, health, services, at_home, other)"
    sha256 = "3fb408fe4b66d4cdb90ad4ec5e3fb6de94ba662d0471a3d46c03da483069f76b"

    def download(self):
        import kagglehub
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "student-por.csv"
        if csv_path.exists():
            return csv_path
        path = kagglehub.dataset_download("uciml/student-alcohol-consumption")
        src_csv = f"{path}/student-por.csv"
        import os
        if os.path.exists(src_csv):
            shutil.copy(src_csv, str(csv_path))
        return csv_path

    def prepare(self):
        import pandas as pd

        path = self.download()
        df = pd.read_csv(str(path))

        y = df["health"].values.astype(float)
        groups = df["Mjob"].astype(str).values

        feat_df = df.drop(columns=["health", "G1", "G2", "G3", "school"])
        cat_cols = feat_df.select_dtypes(include=["object"]).columns.tolist()
        X_df = pd.get_dummies(feat_df, columns=cat_cols, dummy_na=False)
        X = X_df.fillna(0).astype(float).values

        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": df["Mjob"].nunique(),
                "source": "UCI ID 320 (Kaggle mirror, Portuguese, health target)",
                "features": list(X_df.columns)[:8] + [f"... ({X.shape[1]} total)"]}
        return X, y, groups, card
