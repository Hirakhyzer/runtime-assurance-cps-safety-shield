"""Finite axis-aligned intervals for conservative reachable-set calculations."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Box:
    lower: np.ndarray
    upper: np.ndarray

    def __post_init__(self) -> None:
        lo = np.array(self.lower, dtype=float, copy=True)
        hi = np.array(self.upper, dtype=float, copy=True)
        if (lo.ndim != 1 or not lo.size or lo.shape != hi.shape
                or not np.all(np.isfinite(lo)) or not np.all(np.isfinite(hi))
                or np.any(lo > hi)):
            raise ValueError("box bounds must be finite, ordered, nonempty 1D vectors")
        # Immutable arrays prevent accidental mutation of validated interval bounds.
        lo.flags.writeable = False
        hi.flags.writeable = False
        object.__setattr__(self, "lower", lo)
        object.__setattr__(self, "upper", hi)

    @staticmethod
    def _radius(radius: np.ndarray | float, shape: tuple[int, ...]) -> np.ndarray:
        r = np.broadcast_to(np.asarray(radius, dtype=float), shape)
        if not np.all(np.isfinite(r)) or np.any(r < 0):
            raise ValueError("box radius must be finite and nonnegative")
        return r

    @classmethod
    def around(cls, center, radius) -> Box:
        c = np.asarray(center, dtype=float)
        if c.ndim != 1 or not c.size or not np.all(np.isfinite(c)):
            raise ValueError("box center must be a finite nonempty 1D vector")
        r = cls._radius(radius, c.shape)
        return cls(np.nextafter(c - r, -np.inf), np.nextafter(c + r, np.inf))

    @classmethod
    def point(cls, x) -> Box:
        v = np.asarray(x, dtype=float)
        return cls(v, v)

    @property
    def center(self) -> np.ndarray:
        return self.lower + (self.upper - self.lower) / 2.0

    @property
    def radius(self) -> np.ndarray:
        return (self.upper - self.lower) / 2.0

    @property
    def dim(self) -> int:
        return int(self.lower.size)

    def contains_point(self, x) -> bool:
        point = np.asarray(x, dtype=float)
        return bool(point.shape == self.lower.shape
                    and np.all(np.isfinite(point))
                    and np.all(point >= self.lower)
                    and np.all(point <= self.upper))

    def contains_box(self, other: Box) -> bool:
        return bool(other.dim == self.dim and np.all(other.lower >= self.lower)
                    and np.all(other.upper <= self.upper))

    def intersects(self, other: Box) -> bool:
        return bool(other.dim == self.dim and np.all(self.lower <= other.upper)
                    and np.all(other.lower <= self.upper))

    def inflate(self, radius) -> Box:
        r = self._radius(radius, self.lower.shape)
        return Box(np.nextafter(self.lower - r, -np.inf),
                   np.nextafter(self.upper + r, np.inf))

    def hull(self, other: Box) -> Box:
        if other.dim != self.dim:
            raise ValueError("box dimensions must match")
        return Box(np.minimum(self.lower, other.lower),
                   np.maximum(self.upper, other.upper))

    def affine_map(self, A, b=None) -> Box:
        matrix = np.asarray(A, dtype=float)
        if matrix.ndim != 2 or matrix.shape[1] != self.dim or matrix.shape[0] < 1:
            raise ValueError("affine map dimensions must match the box")
        offset = np.zeros(matrix.shape[0]) if b is None else np.asarray(b, dtype=float)
        if (offset.shape != (matrix.shape[0],)
                or not np.all(np.isfinite(matrix))
                or not np.all(np.isfinite(offset))):
            raise ValueError("affine map coefficients must be finite and dimensionally valid")
        c = matrix @ self.center + offset
        r = np.abs(matrix) @ self.radius
        return Box(np.nextafter(c - r, -np.inf),
                   np.nextafter(c + r, np.inf))
