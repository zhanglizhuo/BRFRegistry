from .known_datasets import REGISTRY, register_dataset
from .adapter import load_dataset

__all__ = ["REGISTRY", "register_dataset", "load_dataset"]
