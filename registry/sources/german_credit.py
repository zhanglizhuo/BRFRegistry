"""German Credit (OpenML d/31, credit-g / StatLog). 1000 loans, 20 attributes.
Target: credit risk (good/bad). Group: loan purpose (10 categories)."""
import pandas as pd

from . import DatasetSource, register_source


@register_source
class GermanCreditSource(DatasetSource):
    name = "german_credit"
    display_name = "German Credit — Loan Risk"
    version = "2.0"
    source_url = "https://www.openml.org/d/31"
    license_info = "OpenML (public domain)"
    reference = "OpenML ID 31 (StatLog German Credit); Michie & Spiegelhalter (1993)"
    task = "classification"
    n_samples = 1000
    n_features = 19
    n_groups = 10
    grouping_description = "Purpose of loan (10 categories)"
    sha256 = "d8bbc0b04fc9666ba137eed597e3fea84130071ff95c5f1b8037ea58553041f1"
    notes = "Finance: credit risk (good/bad). Group: loan purpose."

    def download(self):
        from sklearn.datasets import fetch_openml
        dest_dir = self._ensure_cache_dir()
        p = dest_dir / "german_credit.csv"
        if p.exists():
            return p
        ds = fetch_openml(data_id=31, as_frame=True)
        df = ds.data.copy()
        df["target"] = ds.target
        df.to_csv(str(p), index=False)
        return p

    def prepare(self):
        df = pd.read_csv(str(self.download()))
        y = (df["target"].astype(str) == "good").astype(int).values
        groups = df["purpose"].astype(str).values
        feat_cols = [c for c in df.columns if c not in ("target", "purpose")]
        X = (df[feat_cols]
             .apply(lambda c: pd.factorize(c)[0] if c.dtype == object else pd.to_numeric(c, errors="coerce").fillna(0))
             .astype(float).values)
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "OpenML ID 31 (credit-g)"}
        return X, y, groups, card
