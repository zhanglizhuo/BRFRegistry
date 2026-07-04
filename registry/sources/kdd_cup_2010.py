"""KDD Cup 2010 Algebra I 2005-2006 (Development Set).

Student-step logs from Carnegie Learning Cognitive Tutor,
aggregated to student level. Data sourced from USTC mirror.
"""

import numpy as np

from . import DatasetSource, register_source


@register_source
class KDDCup2010Source(DatasetSource):
    name = "kdd_cup_2010"
    display_name = "KDD Cup 2010 (Algebra I 2005-2006)"
    version = "1.0"
    source_url = "http://base.ustc.edu.cn/data/KDD_Cup_2010/algebra_2005_2006.zip"
    fallback_urls = ["https://pslcdatashop.web.cmu.edu/KDDCup/downloads.jsp"]
    license_info = "Public research data (PSLC DataShop)"
    reference = "Stamper, Niculescu-Mizil, Ritter, Gordon & Koedinger (2010)"
    task = "regression"
    n_samples = 574
    n_features = 5
    n_groups = 22
    grouping_description = "Curriculum Unit (22 categories)"
    sha256 = ""
    notes = "Student-level aggregation of 809K step logs from Algebra I 2005-2006."

    def download(self):
        import urllib.request, zipfile, io, os
        dest_dir = self._ensure_cache_dir()
        train_file = dest_dir / "algebra_2005_2006_train.txt"
        if train_file.exists():
            return train_file

        urls = [self.source_url] + self.fallback_urls
        for url in urls:
            try:
                resp = urllib.request.urlopen(url, timeout=120)
                with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
                    z.extractall(str(dest_dir))
                # Find the train file
                for root, dirs, files in os.walk(str(dest_dir)):
                    for f in files:
                        if f == "algebra_2005_2006_train.txt":
                            return dest_dir / root / f
                break
            except Exception:
                continue
        return train_file

    def prepare(self):
        import pandas as pd

        path = self.download()
        df = pd.read_csv(str(path), sep="\t")

        agg = (
            df.groupby("Anon Student Id")
            .agg(
                n_steps=("Correct First Attempt", "count"),
                mean_correct=("Correct First Attempt", "mean"),
                mean_step_duration=("Step Duration (sec)", "mean"),
                total_incorrects=("Incorrects", "sum"),
                total_hints=("Hints", "sum"),
                n_problems=("Problem Name", "nunique"),
            )
            .reset_index()
        )

        agg["log_duration"] = np.log1p(agg["mean_step_duration"].clip(lower=0))
        agg["hint_rate"] = agg["total_hints"] / agg["n_steps"]
        agg["incorrect_rate"] = agg["total_incorrects"] / agg["n_steps"]

        # Grouping: first Unit per student
        hier = df.groupby("Anon Student Id")["Problem Hierarchy"].first()
        agg["unit"] = hier.str.split(", ").str[0].values

        feat_cols = ["log_duration", "hint_rate", "incorrect_rate", "n_problems", "n_steps"]
        X = agg[feat_cols].values.astype(float)
        y = agg["mean_correct"].values
        groups = agg["unit"].astype(str).values

        card = {
            "n_samples": len(y),
            "n_features": len(feat_cols),
            "n_groups": agg["unit"].nunique(),
            "source": "KDD Cup 2010 Algebra I 2005-2006 (USTC mirror)",
            "features": feat_cols,
        }
        return X, y, groups, card
