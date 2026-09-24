from __future__ import annotations

from dataclasses import dataclass, asdict
from statistics import mean
from typing import Iterable, Mapping


@dataclass(frozen=True)
class PairedSafetyComparison:
    """Summary of shielded versus unshielded runs on matched seeds."""

    runs: int
    unsafe_states_unshielded_mean: float
    unsafe_states_shielded_mean: float
    unsafe_states_reduction_mean: float
    intervention_rate_mean: float
    fallback_rate_mean: float
    intervention_cost_mean: float
    minimum_margin_mean: float
    shield_improved_runs: int
    shield_worsened_runs: int
    shield_tied_runs: int

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def summarize_paired_runs(
    unshielded: Iterable[Mapping[str, float | int]],
    shielded: Iterable[Mapping[str, float | int]],
) -> PairedSafetyComparison:
    """Compare matched unshielded/shielded simulations.

    Pairing is important because both conditions should share the same random
    seed and scenario configuration. Positive unsafe-state reduction means the
    shielded condition visited fewer unsafe states than its matched baseline.
    """
    baseline = list(unshielded)
    protected = list(shielded)
    if not baseline or not protected:
        raise ValueError("at least one matched run is required")
    if len(baseline) != len(protected):
        raise ValueError("unshielded and shielded runs must have equal length")

    reductions = [
        float(b["unsafe_states"]) - float(s["unsafe_states"])
        for b, s in zip(baseline, protected)
    ]

    return PairedSafetyComparison(
        runs=len(reductions),
        unsafe_states_unshielded_mean=mean(float(v["unsafe_states"]) for v in baseline),
        unsafe_states_shielded_mean=mean(float(v["unsafe_states"]) for v in protected),
        unsafe_states_reduction_mean=mean(reductions),
        intervention_rate_mean=mean(float(v["intervention_rate"]) for v in protected),
        fallback_rate_mean=mean(float(v["fallback_rate"]) for v in protected),
        intervention_cost_mean=mean(float(v["mean_intervention_cost"]) for v in protected),
        minimum_margin_mean=mean(float(v["min_margin"]) for v in protected),
        shield_improved_runs=sum(delta > 0 for delta in reductions),
        shield_worsened_runs=sum(delta < 0 for delta in reductions),
        shield_tied_runs=sum(delta == 0 for delta in reductions),
    )
