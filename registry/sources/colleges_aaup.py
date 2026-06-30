"""Colleges AAUP -- Faculty Salary Survey (OpenML ID 488)."""

import numpy as np

from . import DatasetSource, register_source


@register_source
class CollegesAAUPSource(DatasetSource):
    name = "colleges_aaup"
    display_name = "AAUP College Faculty Salary"
    version = "1.0"
    source_url = "https://www.openml.org/data/download/22101656/colleges_aaup.arff"
    license_info = "Public Domain (OpenML)"
    reference = "AAUP Faculty Salary Survey (OpenML ID 488)"
    task = "regression"
    n_samples = 1161
    n_features = 9
    n_groups = 52
    grouping_description = "US State (52 groups)"
    notes = "1161 US colleges. Institutional-level prediction."

    def download(self):
        import urllib.request
        dest_dir = self._ensure_cache_dir()
        arff_path = dest_dir / "colleges_aaup.arff"
        if not arff_path.exists():
            urllib.request.urlretrieve(self.source_url, str(arff_path))
        return arff_path

    def prepare(self):
        from scipy.io import arff
        import pandas as pd

        path = self.download()
        data, meta = arff.loadarff(str(path))
        df = pd.DataFrame(data)
        for col in df.select_dtypes([object]).columns:
            df[col] = df[col].str.decode("utf-8") if hasattr(df[col], "str") else df[col]

        target_col = "Average_salary-all_ranks"
        y = df[target_col].values.astype(float)

        type_d = pd.get_dummies(df["Type"], prefix="type", dtype=float)
        faculty_cols = [c for c in df.columns if c.startswith("Number_of")]
        X = np.hstack([type_d.values.astype(float), df[faculty_cols].values.astype(float)])
        groups = df["State"].astype(str).values

        card = {
            "n_samples": len(y),
            "n_features": X.shape[1],
            "n_groups": df["State"].nunique(),
            "source": "OpenML ID 488 (AAUP)",
            "features": list(type_d.columns) + faculty_cols,
        }
        return X, y, groups, card
