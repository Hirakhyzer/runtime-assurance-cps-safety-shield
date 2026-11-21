"""Validated discrete affine dynamics with bounded uncertainty."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from rtshield.sets.box import Box


@dataclass(frozen=True)
class AffineDiscreteModel:
    A: np.ndarray
    B: np.ndarray
    c: np.ndarray
    disturbance: Box
    dt: float = 1.0
    name: str = "affine"

    def __post_init__(self) -> None:
        A = np.array(self.A, dtype=float, copy=True)
        B = np.array(self.B, dtype=float, copy=True)
        c = np.array(self.c, dtype=float, copy=True)
        if A.ndim != 2 or A.shape[0] == 0 or A.shape[0] != A.shape[1]:
            raise ValueError("A must be a nonempty square state matrix")
        if B.ndim != 2 or B.shape[0] != A.shape[0] or B.shape[1] == 0:
            raise ValueError("B must have a row for each state and at least one action")
        if c.shape != (A.shape[0],):
            raise ValueError("c must match the state dimension")
        if not isinstance(self.disturbance, Box) or self.disturbance.dim != A.shape[0]:
            raise ValueError("disturbance box must match the state dimension")
        if not (np.all(np.isfinite(A)) and np.all(np.isfinite(B))
                and np.all(np.isfinite(c))):
            raise ValueError("model matrices and offset must be finite")
        if isinstance(self.dt, bool) or not np.isscalar(self.dt) or not np.isfinite(self.dt) or self.dt <= 0:
            raise ValueError("dt must be finite and positive")
        A.flags.writeable = False
        B.flags.writeable = False
        c.flags.writeable = False
        object.__setattr__(self, "A", A)
        object.__setattr__(self, "B", B)
        object.__setattr__(self, "c", c)

    @property
    def state_dim(self) -> int:
        return self.A.shape[0]

    @property
    def action_dim(self) -> int:
        return self.B.shape[1]

    def step_point(self, x, u, w=None):
        x = np.asarray(x, dtype=float)
        u = np.asarray(u, dtype=float)
        w = np.zeros(self.state_dim) if w is None else np.asarray(w, dtype=float)
        if (x.shape != (self.state_dim,) or u.shape != (self.action_dim,)
                or w.shape != (self.state_dim,)
                or not all(np.all(np.isfinite(v)) for v in (x, u, w))):
            raise ValueError("state, action, and disturbance must be finite vectors of matching dimensions")
        return self.A @ x + self.B @ u + self.c + w

    def step_box(self, x_box: Box, u_box: Box, extra_disturbance: Box | None = None) -> Box:
        if x_box.dim != self.state_dim or u_box.dim != self.action_dim:
            raise ValueError("state and action boxes must match model dimensions")
        if extra_disturbance is not None and extra_disturbance.dim != self.state_dim:
            raise ValueError("extra disturbance box must match state dimension")
        xb = x_box.affine_map(self.A, self.c)
        ub = u_box.affine_map(self.B)
        lo = xb.lower + ub.lower + self.disturbance.lower
        hi = xb.upper + ub.upper + self.disturbance.upper
        if extra_disturbance is not None:
            lo = lo + extra_disturbance.lower
            hi = hi + extra_disturbance.upper
        return Box(np.nextafter(lo, -np.inf), np.nextafter(hi, np.inf))
