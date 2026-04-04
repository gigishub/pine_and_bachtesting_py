from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from .config import DatasetConfig


@dataclass(frozen=True)
class DatasetSplit:
    dataset: DatasetConfig
    in_sample: pd.DataFrame
    out_of_sample: pd.DataFrame


@dataclass
class OptimizationArtifacts:
    dataset_splits: dict[str, DatasetSplit] = field(default_factory=dict)
    dataset_results: pd.DataFrame = field(default_factory=pd.DataFrame)
    master_winners: pd.DataFrame = field(default_factory=pd.DataFrame)
    intersection_winners: pd.DataFrame = field(default_factory=pd.DataFrame)
    consistent_winners: pd.DataFrame = field(default_factory=pd.DataFrame)
    out_of_sample_results: pd.DataFrame = field(default_factory=pd.DataFrame)
    finalist_params: dict[str, Any] | None = None
    completed_step: str = "plan"
