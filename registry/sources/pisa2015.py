"""PISA 2015 Science (OECD PUF). Predict science achievement from student background. Group: Country (73 groups)."""
import numpy as np

from . import DatasetSource, register_source

@register_source
class PISA2015Source(DatasetSource):
    name = "pisa2015"
    display_name = "PISA 2015 Science"
    version = "2.0"
    source_url = "https://webfs.oecd.org/pisa/PUF_SPSS_COMBINED_CMB_STU_QQQ.zip"
    license_info = "OECD Public Use File"
    reference = "OECD PISA 2015 (Results Volume III / Technical Report)"
    task = "regression"
    n_samples = 519334
    n_features = 3
    n_groups = 73
    grouping_description = "Country (73 groups)"
    sha256 = "4c89fbf6cb6c3f5b008422999256b7adffbb5cf45271e0fb9261b698fd7c374d"
    notes = ("519K students, 73 countries (official OECD PISA 2015 PUF, STU_QQQ). "
             "Features: ESCS, WEALTH, HOMEPOS (median-imputed). "
             "Target: mean of science plausible values PV1SCIE-PV5SCIE. "
             "v1.0 (USTC mirror, near-constant features + string-match target) superseded "
             "2026-09-14 after verification against the official PUF.")

    def download(self):
        import urllib.request, zipfile
        oecd_dir = self._ensure_cache_dir() / "oecd_puf"
        sav_path = oecd_dir / "CY6_MS_CMB_STU_QQQ.sav"
        if sav_path.exists():
            return sav_path
        zpath = oecd_dir / "PUF_SPSS_COMBINED_CMB_STU_QQQ.zip"
        if not zpath.exists():
            oecd_dir.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(self.source_url, str(zpath))
        with zipfile.ZipFile(zpath) as z:
            z.extractall(str(oecd_dir))
        return sav_path

    def prepare(self):
        try:
            import pyreadstat
        except ImportError as exc:
            raise ImportError(
                "pyreadstat is required for this dataset but is not installed. "
                "Install the optional extra with: "
                "pip install 'benchmark-reliability[full]'"
            ) from exc
        pvt_cols = [f"PV{i}SCIE" for i in range(1, 6)]
        usecols = ["CNT", "ESCS", "WEALTH", "HOMEPOS"] + pvt_cols
        df, _ = pyreadstat.read_sav(str(self.download()), usecols=usecols)

        X = df[["ESCS", "WEALTH", "HOMEPOS"]].copy()
        for c in X.columns:
            X[c] = X[c].fillna(X[c].median())
        X = X.to_numpy(dtype=float)

        y = df[pvt_cols].mean(axis=1).to_numpy(dtype=float)
        groups = df["CNT"].to_numpy()

        card = {
            "n_samples": len(y),
            "n_features": X.shape[1],
            "n_groups": len(set(groups)),
            "source": "OECD PISA 2015 PUF (STU_QQQ, SPSS)",
            "features": ["ESCS", "WEALTH", "HOMEPOS"],
            "target": "mean(PV1SCIE..PV5SCIE)",
        }
        return X, y, groups, card
