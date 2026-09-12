"""Telecom Customer Churn (OpenML d/40701, Bell Atlantic-style telco records).
5,000 accounts. Target: churn (0/1). Group: state (51)."""
import pandas as pd

from . import DatasetSource, register_source


@register_source
class CustomerChurnSource(DatasetSource):
    name = "customer_churn"
    display_name = "Customer Churn — Telecom"
    version = "2.0"
    source_url = "https://www.openml.org/d/40701"
    license_info = "OpenML (public domain)"
    reference = "OpenML ID 40701 (churn)"
    task = "classification"
    n_samples = 5000
    n_features = 18
    n_groups = 51
    grouping_description = "State (51 states)"
    sha256 = "e07c3d31f8a0ccfde180158a04d83ef5ce46177e9738d8df8df028650a217be0"
    notes = "Business: churn prediction. Group: state."

    def download(self):
        from sklearn.datasets import fetch_openml
        dest_dir = self._ensure_cache_dir()
        p = dest_dir / "churn.csv"
        if p.exists():
            return p
        ds = fetch_openml(data_id=40701, as_frame=True)
        df = ds.data.copy()
        df["target"] = ds.target
        df.to_csv(str(p), index=False)
        return p

    def prepare(self):
        df = pd.read_csv(str(self.download()))
        y = pd.to_numeric(df["target"], errors="coerce").fillna(0).astype(int).values
        groups = df["state"].astype(str).values
        drop_cols = {"target", "state", "phone_number"}
        feat_cols = [c for c in df.columns if c not in drop_cols]
        X = (df[feat_cols]
             .apply(lambda c: pd.factorize(c)[0] if c.dtype == object else pd.to_numeric(c, errors="coerce").fillna(0))
             .astype(float).values)
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "OpenML ID 40701 (churn)"}
        return X, y, groups, card
