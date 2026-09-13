"""External validation datasets — real cross-domain benchmarks (sklearn/OpenML).

The former synthetic-fallback entries in this file were replaced (2026-09-12)
by verified real-data sources in their own modules: german_credit.py,
credit_card.py, customer_churn.py, climate_weather.py, air_quality_uci.py,
electricity.py, olympics.py.

Domains (NOT in development corpus):
- Biomedical/Clinical (2)
- Real Estate (1)
- Health (1)

Same BRF config as dev corpus:
  n_splits=30, n_permutations=200, Ridge(alpha=1.0), seed=42, scale=True
  tau_s=0.0, tau_e=0.5
"""
import numpy as np
import pandas as pd
from . import DatasetSource, register_source


def _sklearn_cache(name, df):
    from pathlib import Path
    cache = Path(__file__).resolve().parent.parent / "cache" / name
    cache.mkdir(parents=True, exist_ok=True)
    p = cache / f"{name}.csv"
    if not p.exists():
        df.to_csv(str(p), index=False)
    return p


# ===== Breast Cancer (sklearn) — Biomedical =====
@register_source
class BreastCancerSource(DatasetSource):
    name = "breast_cancer"
    display_name = "Breast Cancer — Survival"
    version = "1.0"
    source_url = "sklearn.datasets.load_breast_cancer"
    license_info = "sklearn (public domain)"
    reference = "sklearn; UCI Breast Cancer Wisconsin"
    task = "regression"
    n_samples = 569
    n_features = 29   # 30 measured attributes minus the target (mean radius)
    n_groups = 2
    grouping_description = "Diagnosis (2: malignant/benign)"
    notes = "Biomedical: tumor size as regression. Group: diagnosis class."

    def download(self):
        from sklearn.datasets import load_breast_cancer
        d = load_breast_cancer()
        df = pd.DataFrame(d.data, columns=d.feature_names)
        df["target"] = d.target
        return _sklearn_cache(self.name, df)

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = np.asarray(df["mean radius"]).astype(float).ravel()
        groups = np.asarray(df["target"]).astype(int).astype(str).ravel()
        feat_cols = [c for c in df.columns if c not in ("target", "mean radius")]
        X = df[feat_cols].apply(pd.to_numeric, errors="coerce").fillna(0).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": 2, "source": "sklearn load_breast_cancer",
                "features": feat_cols}
        return X, y, groups, card


# ===== Linnerud (sklearn) — Health =====
@register_source
class LinnerudSource(DatasetSource):
    name = "linnerud"
    display_name = "Linnerud — Fitness"
    version = "1.0"
    source_url = "sklearn.datasets.load_linnerud"
    license_info = "sklearn (public domain)"
    reference = "Linnerud (1968); sklearn"
    task = "regression"
    n_samples = 20
    n_features = 5
    n_groups = 2
    grouping_description = "Pulse (2: above/below median)"
    notes = "Health: body-weight prediction from fitness tests. Group: pulse category."

    def download(self):
        # sklearn>=1.8 Linnerud: data = [Chins, Situps, Jumps],
        # target = [Weight, Waist, Pulse]. Pin column names from the loader.
        from sklearn.datasets import load_linnerud
        d = load_linnerud()
        X = pd.DataFrame(d.data, columns=[str(n) for n in d.feature_names])
        y = pd.DataFrame(d.target, columns=[str(n) for n in d.target_names])
        df = pd.concat([X, y], axis=1)
        return _sklearn_cache(self.name, df)

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["Weight"].astype(float).values
        groups = (df["Pulse"] > df["Pulse"].median()).astype(int).astype(str).values
        feat_cols = [c for c in df.columns if c not in ("Weight",)]
        X = df[feat_cols].astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": 2, "source": "sklearn load_linnerud",
                "features": feat_cols}
        return X, y, groups, card


# ===== California Housing (sklearn) — Real Estate =====
@register_source
class CaliforniaHousingSource(DatasetSource):
    name = "california_housing"
    display_name = "California Housing — Median Value"
    version = "1.0"
    source_url = "sklearn.datasets.fetch_california_housing"
    license_info = "sklearn (public domain)"
    reference = "sklearn; California Census 1990"
    task = "regression"
    n_samples = 20640
    n_features = 8
    n_groups = 71
    grouping_description = "Region (71 lat/lon bins)"
    notes = "Real Estate: median house value. Group: geographic region."

    def download(self):
        from sklearn.datasets import fetch_california_housing
        d = fetch_california_housing()
        df = pd.DataFrame(d.data, columns=d.feature_names)
        df["target"] = d.target
        return _sklearn_cache(self.name, df)

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = np.asarray(df["target"]).astype(float).ravel()
        lat = np.asarray(df["Latitude"]).astype(float).ravel()
        lon = np.asarray(df["Longitude"]).astype(float).ravel()
        lat_bin = np.floor((lat - 32) / 0.8).astype(int)
        lon_bin = np.floor((lon + 125) / 1.0).astype(int)
        groups = (lat_bin * 100 + lon_bin).astype(str).ravel()
        feat_cols = [c for c in df.columns if c != "target"]
        X = df[feat_cols].apply(pd.to_numeric, errors="coerce").fillna(0).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "sklearn fetch_california_housing",
                "features": feat_cols}
        return X, y, groups, card


# ===== Diabetes (sklearn) — Biomedical =====
@register_source
class DiabetesSource(DatasetSource):
    name = "diabetes"
    display_name = "Diabetes — Disease Progression"
    version = "1.0"
    source_url = "sklearn.datasets.load_diabetes"
    license_info = "sklearn (public domain)"
    reference = "sklearn; SLC26A9 cohort"
    task = "regression"
    n_samples = 442
    n_features = 10
    n_groups = 3
    grouping_description = "BMI bins (3: normal/overweight/obese)"
    notes = "Metabolic: disease progression rate. Group: BMI category."

    def download(self):
        from sklearn.datasets import load_diabetes
        d = load_diabetes(scaled=False)  # sklearn>=1.8 defaults to scaled=True; raw values needed for BMI bins
        df = pd.DataFrame(d.data, columns=d.feature_names)
        df["target"] = d.target
        return _sklearn_cache(self.name, df)

    def prepare(self):
        path = self.download()
        df = pd.read_csv(str(path))
        y = df["target"].astype(float).values
        bmi = df["bmi"].astype(float).values
        groups = np.where(bmi < 25, "normal", np.where(bmi <= 30, "overweight", "obese"))
        X = df.drop(columns=["target"]).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": 3, "source": "sklearn load_diabetes",
                "features": list(df.columns[:-1])}
        return X, y, groups, card
