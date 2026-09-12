"""Air Quality (UCI, Smola et al. 2011; mirror: asharvi1/UCI-Air-Quality-Data).
Cross-pollutant sensor calibration: predict the reference (GT) reading of each
pollutant from its PT08 sensor reading plus meteorological features (T, RH, AH).
Group: pollutant (4: CO, NMHC, NOx, NO2)."""
import numpy as np
import pandas as pd

from . import DatasetSource, register_source

# (GT reference column, PT08 sensor column, pollutant label)
PAIRS = [
    ("CO(GT)", "PT08.S1(CO)", "CO"),
    ("NMHC(GT)", "PT08.S2(NMHC)", "NMHC"),
    ("NOx(GT)", "PT08.S3(NOx)", "NOx"),
    ("NO2(GT)", "PT08.S4(NO2)", "NO2"),
]
METEO = ["T", "RH", "AH"]


@register_source
class AirQualityUciSource(DatasetSource):
    name = "air_quality"
    display_name = "Air Quality UCI — Sensor Calibration"
    version = "2.0"
    source_url = "https://github.com/Gauhar1107/AirQualityUCI/blob/master/AirQualityUCI.csv"
    license_info = "UCI ML Repository (CC BY 4.0)"
    reference = "UCI 'Air Quality' (Smola et al. 2011); github.com/Gauhar1107/AirQualityUCI"
    task = "regression"
    n_samples = 37424   # 4 pollutants x 9,356 complete rows
    n_features = 4
    n_groups = 4
    grouping_description = "Pollutant (4: CO, NMHC, NOx, NO2)"
    sha256 = "b0aad84a1f735f2e98359a0ac6f7e6730d0d7dccd27db1fa6ae3e07388159a97"
    notes = "Environmental: cross-pollutant sensor calibration (GT from PT08 + meteorology)."

    def download(self):
        dest_dir = self._ensure_cache_dir()
        p = dest_dir / "air_quality.csv"
        if p.exists():
            return p
        url = ("https://github.com/Gauhar1107/AirQualityUCI/raw/master/AirQualityUCI.csv")
        self._download_url_ua(url, p)
        return p

    @staticmethod
    def _download_url_ua(url, dest, timeout=300):
        # GitHub rejects python-urllib's default User-Agent.
        from urllib.request import Request, urlopen
        dest.parent.mkdir(parents=True, exist_ok=True)
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (BRFRegistry)"})
        with urlopen(req, timeout=timeout) as resp:
            dest.write_bytes(resp.read())
        return dest

    def prepare(self):
        df = pd.read_csv(str(self.download()))
        df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
        Xs, ys, gs = [], [], []
        for gt_col, sensor_col, label in PAIRS:
            need = [gt_col, sensor_col] + METEO
            sub = df[need].apply(pd.to_numeric, errors="coerce").dropna()
            Xs.append(pd.DataFrame({
                "sensor": sub[sensor_col].values,
                "T": sub["T"].values, "RH": sub["RH"].values, "AH": sub["AH"].values,
            }).values)
            ys.append(sub[gt_col].values.astype(float))
            gs.append(np.full(len(sub), label))
        X = np.vstack(Xs)
        y = np.concatenate(ys)
        groups = np.concatenate(gs)
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "UCI Air Quality (Smola et al. 2011)"}
        return X, y, groups, card
