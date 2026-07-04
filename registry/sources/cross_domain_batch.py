"""Concrete, Bike Sharing, Airfoil, CCPP — batch cross-domain sources."""

import numpy as np, pandas as pd, io, zipfile, urllib.request
from . import DatasetSource, register_source

# ===== Concrete =====
@register_source
class ConcreteSource(DatasetSource):
    name="concrete"; display_name="Concrete Strength (Age)"
    version="1.0"; task="regression"; n_samples=1030; n_features=7; n_groups=3
    license_info="CC BY 4.0"; reference="Yeh (1998); UCI ID 165"
    grouping_description="Age bins (1-28d, 29-90d, 91+d)"
    def download(self):
        dest=self._ensure_cache_dir(); p=dest/"concrete.csv"
        if p.exists(): return p
        url="https://archive.ics.uci.edu/ml/machine-learning-databases/concrete/compressive/Concrete_Data.xls"
        df=pd.read_excel(io.BytesIO(urllib.request.urlopen(url,timeout=30).read()))
        df.columns=['cement','slag','ash','water','superplasticizer','coarse_agg','fine_agg','age','strength']
        df.to_csv(str(p),index=False); return p
    def prepare(self):
        df=pd.read_csv(str(self.download()))
        y=df["strength"].values.astype(float)
        age=df["age"].values; groups=np.where(age<=28,'young',np.where(age<=90,'mid','old'))
        X=df.drop(columns=["strength","age"]).fillna(0).astype(float).values
        return X,y,groups,{"n_samples":len(y),"n_features":X.shape[1],"n_groups":3,"source":"UCI ID 165"}

# ===== Bike Sharing =====
@register_source
class BikeSharingSource(DatasetSource):
    name="bike_sharing"; display_name="Bike Sharing (Season)"
    version="1.0"; task="regression"; n_samples=731; n_features=10; n_groups=4
    license_info="CC BY 4.0"; reference="Fanaee-T & Gama (2013); UCI ID 275"
    grouping_description="Season (4: spring/summer/fall/winter)"
    def download(self):
        dest=self._ensure_cache_dir(); p=dest/"bike_sharing.csv"
        if p.exists(): return p
        url="https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip"
        with zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(url,timeout=30).read())) as z:
            with z.open('day.csv') as f: df=pd.read_csv(f)
        df.to_csv(str(p),index=False); return p
    def prepare(self):
        df=pd.read_csv(str(self.download()))
        y=df["cnt"].values.astype(float); groups=df["season"].astype(str).values
        X=df.drop(columns=["cnt","season","dteday","instant","casual","registered"]).fillna(0).astype(float).values
        return X,y,groups,{"n_samples":len(y),"n_features":X.shape[1],"n_groups":4,"source":"UCI ID 275"}

# ===== Airfoil =====
@register_source
class AirfoilSource(DatasetSource):
    name="airfoil"; display_name="Airfoil Noise (Freq)"
    version="1.0"; task="regression"; n_samples=1503; n_features=4; n_groups=3
    license_info="CC BY 4.0"; reference="Brooks et al. (1989); UCI ID 291"
    grouping_description="Frequency bins (low<2kHz, mid<8kHz, high)"
    def download(self):
        dest=self._ensure_cache_dir(); p=dest/"airfoil.csv"
        if p.exists(): return p
        url="https://archive.ics.uci.edu/ml/machine-learning-databases/00291/airfoil_self_noise.dat"
        df=pd.read_csv(io.StringIO(urllib.request.urlopen(url,timeout=30).read().decode()),
                       delim_whitespace=True,header=None,
                       names=['freq','angle','chord','velocity','suction','sound'])
        df.to_csv(str(p),index=False); return p
    def prepare(self):
        df=pd.read_csv(str(self.download()))
        y=df["sound"].values.astype(float); f=df["freq"].values
        groups=np.where(f<=2000,'low',np.where(f<=8000,'mid','high'))
        X=df.drop(columns=["sound","freq"]).fillna(0).astype(float).values
        return X,y,groups,{"n_samples":len(y),"n_features":X.shape[1],"n_groups":3,"source":"UCI ID 291"}

# ===== CCPP =====
@register_source
class CCPPSource(DatasetSource):
    name="ccpp"; display_name="Combined Cycle Power (Temp)"
    version="1.0"; task="regression"; n_samples=9568; n_features=3; n_groups=3
    license_info="CC BY 4.0"; reference="Tufekci (2014); UCI ID 294"
    grouping_description="Temperature bins (cold<15C, mild<25C, hot)"
    def download(self):
        dest=self._ensure_cache_dir(); p=dest/"ccpp.csv"
        if p.exists(): return p
        url="https://archive.ics.uci.edu/ml/machine-learning-databases/00294/CCPP.zip"
        with zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(url,timeout=30).read())) as z:
            with z.open('CCPP/Folds5x2_pp.xlsx') as f: df=pd.read_excel(io.BytesIO(f.read()))
        df.to_csv(str(p),index=False); return p
    def prepare(self):
        df=pd.read_csv(str(self.download()))
        y=df["PE"].values.astype(float); t=df["AT"].values
        groups=np.where(t<15,'cold',np.where(t<25,'mild','hot'))
        X=df.drop(columns=["PE","AT"]).fillna(0).astype(float).values
        return X,y,groups,{"n_samples":len(y),"n_features":X.shape[1],"n_groups":3,"source":"UCI ID 294"}
