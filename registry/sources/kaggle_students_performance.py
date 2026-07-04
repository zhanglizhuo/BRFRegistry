"""Kaggle Students Performance in Exams (K12). math score (0-100). Group: race/ethnicity (5 groups)."""
import pandas as pd

from . import DatasetSource, register_source

@register_source
class KaggleStudentsPerformanceSource(DatasetSource):
    name = "kaggle_students_performance"
    display_name = "Kaggle Students Performance in Exams"
    version = "1.0"
    source_url = "https://www.kaggle.com/datasets/spscientist/students-performance-in-exams"
    license_info = "CC0: Public Domain (Kaggle)"
    reference = "Kaggle (spscientist); originally from NCES"
    task = "regression"
    n_samples = 1000
    n_features = 14
    n_groups = 5
    sha256 = "ade5869dba8b2d3e2b96379359fb2f61cb0308e8394d9b1ba37e174cfe3bee69"
    grouping_description = "Race/Ethnicity (5 groups: A-E)"

    def download(self):
        import kagglehub
        import shutil
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "StudentsPerformance.csv"
        if csv_path.exists():
            return csv_path
        path = kagglehub.dataset_download("spscientist/students-performance-in-exams")
        src_csv = f"{path}/StudentsPerformance.csv"
        shutil.copy(src_csv, str(csv_path))
        return csv_path

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["math score"].values.astype(float)
        groups = df["race/ethnicity"].astype(str).values
        feat_df = df.drop(columns=["math score", "reading score", "writing score"])
        cat_cols = feat_df.select_dtypes(include=["object"]).columns.tolist()
        X_df = pd.get_dummies(feat_df, columns=cat_cols, dummy_na=False)
        X = X_df.fillna(0).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": df["race/ethnicity"].nunique(),
                "source": "Kaggle (spscientist)",
                "features": list(X_df.columns)[:8] + [f"... ({X.shape[1]} total)"]}
        return X, y, groups, card
