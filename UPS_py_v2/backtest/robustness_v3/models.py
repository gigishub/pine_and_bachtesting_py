from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass
class RobustnessArtifactsV3:
    dataset_results: pd.DataFrame = field(default_factory=pd.DataFrame)
    parameter_grid_size: int = 0
    completed_step: str = "plan"