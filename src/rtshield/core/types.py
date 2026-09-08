from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from rtshield.sets.box import Box

class DecisionStatus(str, Enum):
    ACCEPT = "ACCEPT"
    MODIFY = "MODIFY"
    FALLBACK = "FALLBACK"

@dataclass(frozen=True)
class StateEstimate:
    center: np.ndarray
    uncertainty: Box
    source: str = "estimator"

@dataclass(frozen=True)
class ActionProposal:
    nominal: np.ndarray
    controller: str = "nominal"

@dataclass
class ShieldDecision:
    status: DecisionStatus
    nominal_action: np.ndarray
    applied_action: np.ndarray
    predicted_reachable: Box
    reason: str
    intervention_norm: float
    metadata: dict = field(default_factory=dict)
