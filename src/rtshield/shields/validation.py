"""Input checks shared by model-based shield implementations."""
from __future__ import annotations

import numpy as np

from rtshield.core.types import ActionProposal, StateEstimate
from rtshield.models.affine import AffineDiscreteModel
from rtshield.sets.box import Box


def validate_action_space(model: AffineDiscreteModel, lower, upper, fallback,
                          uncertainty, grid_points: int):
    if isinstance(grid_points, bool) or not isinstance(grid_points, int) or grid_points < 2:
        raise ValueError("grid_points must be an integer >= 2")
    vectors = tuple(np.array(value, dtype=float, copy=True)
                    for value in (lower, upper, fallback))
    if any(v.shape != (model.action_dim,) or not np.all(np.isfinite(v)) for v in vectors):
        raise ValueError("action bounds and fallback must be finite action-dimensional vectors")
    lo, hi, fb = vectors
    if np.any(lo > hi):
        raise ValueError("action bounds must be ordered")
    radius = np.asarray(uncertainty, dtype=float)
    try:
        radius = np.broadcast_to(radius, (model.action_dim,)).copy()
    except ValueError as exc:
        raise ValueError("action_uncertainty must match action dimension") from exc
    if not np.all(np.isfinite(radius)) or np.any(radius < 0):
        raise ValueError("action_uncertainty must be finite and nonnegative")
    for v in (lo, hi, fb, radius):
        v.flags.writeable = False
    return lo, hi, fb, radius


def validate_filter_inputs(model: AffineDiscreteModel, estimate: StateEstimate,
                           proposal: ActionProposal) -> np.ndarray:
    center = np.asarray(estimate.center, dtype=float)
    if (not isinstance(estimate.uncertainty, Box)
            or estimate.uncertainty.dim != model.state_dim
            or center.shape != (model.state_dim,)
            or not np.all(np.isfinite(center))):
        raise ValueError("state estimate must match model dimensions and be finite")
    nominal = np.asarray(proposal.nominal, dtype=float)
    if nominal.shape != (model.action_dim,) or not np.all(np.isfinite(nominal)):
        raise ValueError("nominal action must be a finite action-dimensional vector")
    return nominal
