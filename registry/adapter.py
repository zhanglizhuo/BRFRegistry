from typing import Optional, Tuple

import numpy as np

from .known_datasets import REGISTRY

# Import BehaviorAudit adapters (they must be importable from the SR repo)
import sys
from pathlib import Path

BA_ROOT = Path(__file__).resolve().parent.parent.parent / "AutoResearchClaw" / "BehaviorAudit"
if BA_ROOT.exists():
    sys.path.insert(0, str(BA_ROOT))
else:
    raise ImportError(
        f"BehaviorAudit repo not found at {BA_ROOT}. "
        "Please set BA_ROOT or clone the repo."
    )

from framework.adapters import (
    MMTBAAdapter,
    OULADAdapter,
    UCIStudentAdapter,
    XAPIEduAdapter,
    StudentDropoutAdapter,
    EntranceExamAdapter,
    HigherEdAdapter,
)

_REGISTRY_DIR = Path(__file__).resolve().parent
_BRF_DATA_DIR = _REGISTRY_DIR.parent / "data"


class TAEAdapter:
    """Teaching Assistant Evaluation (UCI ID 100).

    Columns: English speaker, Instructor, Course, Semester, Class size, Target.
    Group by Instructor (25 categories); predict Class (1=Low, 2=Medium, 3=High).
    """

    name = "tae"

    def load(self, dataset_root: Optional[str] = None) -> object:
        data_path = _BRF_DATA_DIR / "tae.data"
        if not data_path.exists():
            return _error_bundle(f"Missing file: {data_path}")

        raw = np.loadtxt(str(data_path), delimiter=",")
        # Columns: 0=English speaker, 1=Instructor, 2=Course, 3=Semester, 4=Class size, 5=Target
        X = raw[:, [0, 2, 3, 4]]  # features: English speaker, Course, Semester, Class size
        y = raw[:, 5].astype(int)  # target: 1=Low, 2=Medium, 3=High
        group_ids = raw[:, 1].astype(int).astype(str).tolist()  # Instructor

        data_card = {
            "n_samples": len(y),
            "n_features": X.shape[1],
            "n_groups": len(np.unique(group_ids)),
            "source": "UCI ID 100",
            "features": ["english_speaker", "course", "semester", "class_size"],
        }
        return _bundle(X, y, group_ids, data_card)


class TurkiyeAdapter:
    """Turkiye Student Evaluation (UCI ID 262).

    Columns: instr (1-3), class (1-13), nb.repeat, attendance, difficulty, Q1-Q28.
    Group by class (13 course categories); predict difficulty (1-5).
    """

    name = "turkiye"

    def load(self, dataset_root: Optional[str] = None) -> object:
        data_path = _BRF_DATA_DIR / "turkiye-student-evaluation_generic.csv"
        if not data_path.exists():
            return _error_bundle(f"Missing file: {data_path}")

        import pandas as pd
        df = pd.read_csv(str(data_path))
        # Use Q1-Q28 as features
        q_cols = [f"Q{i}" for i in range(1, 29)]
        X = df[q_cols].values.astype(float)
        y = df["difficulty"].values.astype(int)
        group_ids = df["class"].astype(str).tolist()

        data_card = {
            "n_samples": len(y),
            "n_features": X.shape[1],
            "n_groups": df["class"].nunique(),
            "source": "UCI ID 262",
            "features": q_cols,
        }
        return _bundle(X, y, group_ids, data_card)


class ASSISTmentsAdapter:
    """ASSISTments 2009-2010 Skill Builder (corrected).

    Transaction-level student tutoring data. Aggregated to student level.
    Target: overall accuracy per student.
    Group: teacher_id (153 teachers).
    """

    name = "assistments"

    def load(self, dataset_root: Optional[str] = None) -> object:
        import pandas as pd

        data_path = _BRF_DATA_DIR / "skill_builder_data_corrected.csv"
        if not data_path.exists():
            return _error_bundle(f"Missing file: {data_path}")

        df = pd.read_csv(str(data_path), encoding="ISO-8859-15", low_memory=False)

        # Keep only main problems (not scaffolding)
        df = df[df["original"] == 1].copy()

        # Aggregate to student level
        agg = df.groupby("user_id").agg(
            n_problems=("correct", "count"),
            mean_correct=("correct", "mean"),
            mean_attempt=("attempt_count", "mean"),
            mean_hint=("hint_count", "mean"),
            median_response_ms=("ms_first_response", "median"),
            n_skills=("skill_id", "nunique"),
            n_teachers=("teacher_id", "nunique"),
            n_schools=("school_id", "nunique"),
            teacher_id=("teacher_id", "first"),
            school_id=("school_id", "first"),
        ).reset_index()

        # Filter students with >= 5 problems
        agg = agg[agg["n_problems"] >= 5].copy()

        # Features
        feat_cols = ["n_problems", "mean_attempt", "mean_hint", "median_response_ms", "n_skills"]
        X = agg[feat_cols].values.astype(float)
        # Log-transform response time
        X[:, 3] = np.log1p(X[:, 3])

        y = agg["mean_correct"].values  # target: overall accuracy

        group_ids = agg["teacher_id"].astype(str).tolist()

        data_card = {
            "n_samples": len(y),
            "n_features": len(feat_cols),
            "n_groups": agg["teacher_id"].nunique(),
            "n_schools": agg["school_id"].nunique(),
            "n_transactions": len(df),
            "source": "ASSISTments 2009-2010 (corrected)",
            "features": feat_cols + ["log_response_ms"],
        }
        return _bundle(X, y, group_ids, data_card)


def _bundle(X, y, group_ids, data_card):
    class _Bundle:
        pass
    b = _Bundle()
    b.X = X
    b.y = y
    b.group_ids = group_ids
    b.data_card = data_card
    return b


def _error_bundle(msg):
    b = _bundle(None, None, None, {"error": msg})
    return b


_ADAPTERS = {
    "mm_tba": MMTBAAdapter(),
    "oulad": OULADAdapter(),
    "uci_student": UCIStudentAdapter(),
    "xapi_edu": XAPIEduAdapter(),
    "student_dropout": StudentDropoutAdapter(),
    "entrance_exam": EntranceExamAdapter(),
    "higher_ed": HigherEdAdapter(),
    "tae": TAEAdapter(),
    "turkiye": TurkiyeAdapter(),
    "assistments": ASSISTmentsAdapter(),
}


def load_dataset(key: str) -> Optional[Tuple[np.ndarray, np.ndarray, Optional[np.ndarray], dict]]:
    """Load a dataset from the registry.

    Returns (X, y, groups, metadata) or None if loading fails.
    groups is None if the dataset has no grouping variable.
    """
    if key not in REGISTRY:
        raise KeyError(f"Unknown dataset: {key}")

    info = REGISTRY[key]
    adapter = _ADAPTERS.get(key)
    if adapter is None:
        return None

    dataset_root = str(BA_ROOT / info["dataset_root"])
    bundle = adapter.load(dataset_root=dataset_root)
    if bundle.X is None:
        return None

    groups = np.array(bundle.group_ids) if bundle.group_ids else None
    return bundle.X, bundle.y, groups, bundle.data_card
