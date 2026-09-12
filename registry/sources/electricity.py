"""Electricity (OpenML d/151, AIFB). 45,312 half-hourly NSW/VIC market records.
Target: price band (UP/DOWN, peak/off-peak). Group: day of week (7)."""
import pandas as pd

from . import DatasetSource, register_source


@register_source
class ElectricitySource(DatasetSource):
    name = "electricity"
    display_name = "Electricity — Peak/Off-Peak (AIFB)"
    version = "2.0"
    source_url = "https://www.openml.org/d/151"
    license_info = "OpenML (public domain)"
    reference = "OpenML ID 151 (AIFB Electricity); AIFB (2014)"
    task = "classification"
    n_samples = 45312
    n_features = 6
    n_groups = 7
    grouping_description = "Day of week (7)"
    sha256 = "01db54b7c46202b5bd2458d8c31efabbe9661233af8e3d7077b06e903053808c"
    notes = "Energy: peak/off-peak price band. Group: day of week."

    def download(self):
        from sklearn.datasets import fetch_openml
        dest_dir = self._ensure_cache_dir()
        p = dest_dir / "electricity.csv"
        if p.exists():
            return p
        ds = fetch_openml(data_id=151, as_frame=True)
        df = ds.data.copy()
        df["target"] = ds.target
        df.to_csv(str(p), index=False)
        return p

    def prepare(self):
        df = pd.read_csv(str(self.download()))
        y = (df["target"].astype(str) == "UP").astype(int).values
        groups = df["day"].astype(str).values
        feat_cols = ["period", "nswprice", "nswdemand", "vicprice", "vicdemand", "transfer"]
        X = df[feat_cols].apply(pd.to_numeric, errors="coerce").fillna(0).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "OpenML ID 151 (Electricity, AIFB)"}
        return X, y, groups, card
