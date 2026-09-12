"""Olympics Country Medals (teams.csv; mirror: nderitugichuki/Olympics-Medal-Prediction).
2,144 raw country-years (2,014 complete) of Olympic participation and medal counts since 1964.
Target: medals won (regression). Group: country (230)."""
import pandas as pd

from . import DatasetSource, register_source

FEAT_COLS = ["events", "athletes", "age", "height", "weight", "prev_medals", "prev_3_medals"]


@register_source
class OlympicsSource(DatasetSource):
    name = "olympics"
    display_name = "Olympics — Country Medals"
    version = "2.0"
    source_url = "https://github.com/nderitugichuki/Olympics-Medal-Prediction-Machine-Learning-Model/blob/main/teams.csv"
    license_info = "Public statistics (GitHub mirror)"
    reference = "Olympic participation & medal records; github.com/nderitugichuki/Olympics-Medal-Prediction-Machine-Learning-Model"
    task = "regression"
    n_samples = 2014   # rows complete on features + target (2,144 raw country-years)
    n_features = 7
    n_groups = 230
    grouping_description = "Country (230 countries)"
    sha256 = "b27b7dd6621567b550ab9b036b6d07b87a917c2b00292fa70eb8be358ee7ef53"
    notes = "Sports: medals won. Group: country of the Olympic team."

    def download(self):
        dest_dir = self._ensure_cache_dir()
        p = dest_dir / "olympics.csv"
        if p.exists():
            return p
        url = ("https://github.com/nderitugichuki/Olympics-Medal-Prediction-"
               "Machine-Learning-Model/raw/main/teams.csv")
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
        df = df.dropna(subset=FEAT_COLS + ["medals"])
        y = pd.to_numeric(df["medals"], errors="coerce").fillna(0).astype(float).values
        groups = df["country"].astype(str).values
        X = df[FEAT_COLS].apply(pd.to_numeric, errors="coerce").fillna(0).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": len(set(groups)), "source": "Olympic records (teams.csv)"}
        return X, y, groups, card
