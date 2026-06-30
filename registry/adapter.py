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

_ADAPTERS = {
    "mm_tba": MMTBAAdapter(),
    "oulad": OULADAdapter(),
    "uci_student": UCIStudentAdapter(),
    "xapi_edu": XAPIEduAdapter(),
    "student_dropout": StudentDropoutAdapter(),
    "entrance_exam": EntranceExamAdapter(),
    "higher_ed": HigherEdAdapter(),
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
