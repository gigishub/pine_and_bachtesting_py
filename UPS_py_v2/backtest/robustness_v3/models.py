from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd


@dataclass
class RobustnessArtifactsV3:
    primary_results: pd.DataFrame = field(default_factory=pd.DataFrame)
    primary_candidates: pd.DataFrame = field(default_factory=pd.DataFrame)
    validation_results: pd.DataFrame = field(default_factory=pd.DataFrame)
    validation_summary: pd.DataFrame = field(default_factory=pd.DataFrame)
    completed_step: str = "plan"
    finalist_params: dict[str, Any] | None = None