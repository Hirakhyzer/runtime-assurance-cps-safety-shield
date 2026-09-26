import numpy as np

from rtshield.audit import build_decision_audit_record
from rtshield.core.types import DecisionStatus, ShieldDecision, StateEstimate
from rtshield.domains import battery
from rtshield.sets.box import Box
from rtshield.simulation import run_domain


def test_decision_audit_record_is_json_serializable_shape() -> None:
    estimate = StateEstimate(
        center=np.array([0.5, 25.0]),
        uncertainty=Box(np.array([0.49, 24.9]), np.array([0.51, 25.1])),
        source="unit-test",
    )
    decision = ShieldDecision(
        status=DecisionStatus.MODIFY,
        nominal_action=np.array([1.0]),
        applied_action=np.array([0.5]),
        predicted_reachable=Box(np.array([0.4, 24.0]), np.array([0.6, 26.0])),
        reason="test intervention",
        intervention_norm=0.5,
        metadata={"candidate_rank": 2, "margin": 1.5},
    )

    record = build_decision_audit_record(3, estimate, decision).to_dict()

    assert record["step"] == 3
    assert record["status"] == "MODIFY"
    assert record["estimate_source"] == "unit-test"
    assert record["nominal_action"] == [1.0]
    assert record["applied_action"] == [0.5]
    assert record["metadata"]["candidate_rank"] == 2


def test_simulation_records_include_shield_audit_evidence() -> None:
    _, records = run_domain(battery.make_spec(), steps=3, seed=0, shielded=True)

    assert len(records) == 3
    for index, record in enumerate(records):
        audit = record["shield_audit"]
        assert audit["step"] == index
        assert audit["status"] in {"ACCEPT", "MODIFY", "FALLBACK"}
        assert audit["reason"]
        assert audit["predicted_reachable_lower"]
        assert audit["predicted_reachable_upper"]
