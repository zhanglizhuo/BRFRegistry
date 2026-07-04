"""UCI Student Absences (Kaggle mirror, UCI ID 320).

Same student data as uci_student, but with full 33-feature set.
Target: absences (number of school absences, 0-93).
Group: school (GP/MS, 2 groups).
Differs from uci_student (G3 grade target) and uci_student_math (math G3).
"""

import numpy as np
import shutil

from . import DatasetSource, register_source


@register_source
class StudentAbsencesSource(DatasetSource):
    name = "student_absences"
    display_name = "UCI Student Absences (Kaggle)"
    version = "1.0"
    source_url = "https://www.kaggle.com/datasets/uciml/student-alcohol-consumption"
    license_info = "CC BY 4.0"
    reference = "Cortez & Silva (2008); UCI ID 320 (Kaggle mirror)"
    task = "regression"
    n_samples = 395
    n_features = 37
    n_groups = 2
    sha256 = "659f3984643c2def53ba5e49f551c6ce3657039f9c25306cacb8f43b818a5190"
    grouping_description = "School (2: GP/MS)"

    def download(self):
        import kagglehub
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "student-mat.csv"
        if csv_path.exists():
            return csv_path
        path = kagglehub.dataset_download("uciml/student-alcohol-consumption")
        src_csv = f"{path}/student-mat.csv"
        if __import__('os').path.exists(src_csv):
            shutil.copy(src_csv, str(csv_path))
        return csv_path

    def prepare(self):
        import pandas as pd

        path = self.download()
        df = pd.read_csv(str(path))
        
        # Target: absences (0-93, highly skewed, represents dropout risk proxy)
        y = df["absences"].values.astype(float)
        groups = df["school"].astype(str).values
        
        # Features: all columns except absences and highly correlated G1/G2/G3
        feat_df = df.drop(columns=["absences", "G1", "G2", "G3"])
        cat_cols = feat_df.select_dtypes(include=["object"]).columns.tolist()
        X_df = pd.get_dummies(feat_df, columns=cat_cols, dummy_na=False)
        X = X_df.fillna(0).astype(float).values
        
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": df["school"].nunique(),
                "source": "UCI ID 320 (Kaggle mirror, absences target)",
                "features": list(X_df.columns)[:8] + [f"... ({X.shape[1]} total)"]}
        return X, y, groups, card
