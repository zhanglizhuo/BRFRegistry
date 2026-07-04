"""UCI Student Health (Portuguese, Kaggle mirror, UCI ID 320).

Portuguese-language students subset, 33 features.
Target: self-rated health (ordinal 1-5).
Group: mother's job (Mjob, 5 categories).
Distinct from uci_student (Portuguese G3), uci_student_math (Math G3),
and student_absences (Math absences).
"""

import numpy as np
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
    sha256 = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2"

    def download(self):
        import kagglehub
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "student-por.csv"
        if csv_path.exists():
            return csv_path
        path = kagglehub.dataset_download("uciml/student-alcohol-consumption")
        src_csv = f"{path}/student-por.csv"
        if __import__('os').path.exists(src_csv):
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
