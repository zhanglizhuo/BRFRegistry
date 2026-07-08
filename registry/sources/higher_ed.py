"""Higher Education Students Performance (UCI ID 856)."""
from . import DatasetSource, register_source

@register_source
class HigherEdSource(DatasetSource):
    name = "higher_ed"
    display_name = "Higher Education Students Performance"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/856/higher+education+students+performance+evaluation.zip"
    license_info = "CC BY 4.0"
    reference = "Yilmaz & Sekeroglu (2020); UCI ID 856"
    task = "regression"
    n_samples = 145
    n_features = 30
    n_groups = 9
    sha256 = "d5905d231bedd7e4cdcf708fab55fc65b79dfe12012e846eccad3e88b5ecb019"
    grouping_description = "Course ID (9 courses)"

    def download(self):
        import urllib.request, zipfile, io, shutil
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "higher_ed_856.csv"
        if csv_path.exists():
            return csv_path
        resp = urllib.request.urlopen(self.source_url, timeout=60)
        with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
            z.extractall(str(dest_dir))
        # Save the first CSV found to the canonical path
        for f in dest_dir.glob("**/*.csv"):
            if f.name != csv_path.name:
                shutil.copy(str(f), str(csv_path))
                return csv_path
            return csv_path
        # Fallback: save any file as CSV
        for f in dest_dir.glob("**/*"):
            if f.is_file() and f.name != csv_path.name:
                shutil.copy(str(f), str(csv_path))
                return csv_path
        return dest_dir

    def prepare(self):
        import pandas as pd

        path = self.download()
        df = pd.read_csv(str(path))
        # Expected columns from UCI ID 856: GRADE (target), COURSE ID (group)
        y_col = "GRADE"
        g_col = "COURSE ID"
        if y_col not in df.columns:
            y_col = [c for c in df.columns if 'grade' in str(c).lower()][0]
        if g_col not in df.columns:
            g_col = [c for c in df.columns if 'course' in str(c).lower()][0]
        y = df[y_col].values.astype(float)
        groups = df[g_col].astype(str).values
        
        drop_cols = [c for c in [y_col, g_col, 'STUDENT ID'] if c in df.columns]
        feat_df = df.drop(columns=drop_cols)
        X = feat_df.fillna(0).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": df[g_col].nunique(), "source": "UCI ID 856",
                "features": list(feat_df.columns)[:8] + [f"... ({X.shape[1]} total)"]}
        return X, y, groups, card
