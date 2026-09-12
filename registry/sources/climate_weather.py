"""Global Historical Weather (OpenML d/40918, NOAA 'Climate'). 577,462 raw station-years (544,811 with complete temperature).
Target: average temperature (regression). Group: country (243)."""
import pandas as pd

from . import DatasetSource, register_source


@register_source
class ClimateWeatherSource(DatasetSource):
    name = "climate_weather"
    display_name = "Global Weather — Temperature (NOAA)"
    version = "2.0"
    source_url = "https://www.openml.org/d/40918"
    license_info = "OpenML (public domain)"
    reference = "OpenML ID 40918 (Climate); NOAA Global Historical Weather Summary"
    task = "regression"
    n_samples = 544811  # rows with non-missing temperature (577,462 raw station-years)
    n_features = 3
    n_groups = 242
    grouping_description = "Country (242 countries)"
    sha256 = "c83f266cf7b96dc90d8c10e271220078008d9a92b4d2fc73d7bcf77722d5b2e1"
    notes = "Climate: average temperature. Group: country of origin."

    def download(self):
        from sklearn.datasets import fetch_openml
        dest_dir = self._ensure_cache_dir()
        p = dest_dir / "climate.csv"
        if p.exists():
            return p
        ds = fetch_openml(data_id=40918, as_frame=True)
        df = ds.data.copy()
        df.to_csv(str(p), index=False)
        return p

    def prepare(self):
        df = pd.read_csv(str(self.download()))
        dt = pd.to_datetime(df["dt"], errors="coerce")
        y = pd.to_numeric(df["AverageTemperature"], errors="coerce").astype(float).values
        groups = df["Country"].astype(str).values
        X = pd.DataFrame({
            "year": dt.dt.year.astype(float),
            "month": dt.dt.month.astype(float),
            "uncertainty": pd.to_numeric(df["AverageTemperatureUncertainty"], errors="coerce"),
        }).fillna(0).astype(float).values
        keep = ~pd.isna(y)
        X, y, groups = X[keep], y[keep], groups[keep]
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "OpenML ID 40918 (Climate, NOAA)"}
        return X, y, groups, card
