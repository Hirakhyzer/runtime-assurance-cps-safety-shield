from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

from rtshield.core.types import ShieldDecision, StateEstimate


@dataclass(frozen=True)
class DecisionAuditRecord:
    step: int
    estimate_source: str
    estimate_center: list[float]
    estimate_lower: list[float]
    estimate_upper: list[float]
    nominal_action: list[float]
    applied_action: list[float]
    status: str
    reason: str
    intervention_norm: float
    predicted_reachable_lower: list[float]
    predicted_reachable_upper: list[float]
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_decision_audit_record(
    step: int,
    estimate: StateEstimate,
    decision: ShieldDecision,
) -> DecisionAuditRecord:
    """Convert one shield decision into a JSON-serializable audit record.

    The record deliberately captures both the state-estimation envelope and the
    applied control decision. This supports post-hoc inspection of *why* the
    shield intervened without changing the online safety logic itself.
    """

    def values(array: np.ndarray) -> list[float]:
        return [float(value) for value in np.asarray(array, dtype=float).tolist()]

    return DecisionAuditRecord(
        step=int(step),
        estimate_source=estimate.source,
        estimate_center=values(estimate.center),
        estimate_lower=values(estimate.uncertainty.lower),
        estimate_upper=values(estimate.uncertainty.upper),
        nominal_action=values(decision.nominal_action),
        applied_action=values(decision.applied_action),
        status=decision.status.value,
        reason=decision.reason,
        intervention_norm=float(decision.intervention_norm),
        predicted_reachable_lower=values(decision.predicted_reachable.lower),
        predicted_reachable_upper=values(decision.predicted_reachable.upper),
        metadata=dict(decision.metadata),
    )
