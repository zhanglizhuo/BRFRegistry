"""Credit Card Fraud (OpenML d/1597, Kaggle 'creditcard'). 284,807 transactions.
Target: transaction Amount (regression). Group: transaction class (normal/fraud, 2)."""
import numpy as np
import pandas as pd

from . import DatasetSource, register_source


@register_source
class CreditCardSource(DatasetSource):
    name = "credit_card"
    display_name = "Credit Card — Transaction Amount"
    version = "2.0"
    source_url = "https://www.openml.org/d/1597"
    license_info = "OpenML (public domain)"
    reference = "OpenML ID 1597 (Kaggle creditcard; PCA-obfuscated transactions)"
    task = "regression"
    n_samples = 284807
    n_features = 28
    n_groups = 2
    grouping_description = "Transaction class (2: normal/fraud)"
    sha256 = "7c29a13351d14ec5b70eafd28aa2281e66a7a8e1d5cfc753b774f0c835141111"
    notes = "Finance: transaction amount. Group: transaction class."

    def download(self):
        from sklearn.datasets import fetch_openml
        dest_dir = self._ensure_cache_dir()
        p = dest_dir / "credit_card.csv"
        if p.exists():
            return p
        ds = fetch_openml(data_id=1597, as_frame=True)
        df = ds.data.copy()
        df["target"] = ds.target
        df.to_csv(str(p), index=False)
        return p

    def prepare(self):
        df = pd.read_csv(str(self.download()))
        y = pd.to_numeric(df["Amount"], errors="coerce").fillna(0).astype(float).values
        groups = pd.to_numeric(df["target"], errors="coerce").fillna(0).astype(int).astype(str).values
        v_cols = [c for c in df.columns if c.startswith("V")]
        X = df[v_cols].apply(pd.to_numeric, errors="coerce").fillna(0).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "OpenML ID 1597 (creditcard)"}
        return X, y, groups, card
