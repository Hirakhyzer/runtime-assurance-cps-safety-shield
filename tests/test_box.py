import numpy as np
from rtshield.sets.box import Box

def test_box_contains_and_intersects():
    a=Box(np.array([0.,0.]),np.array([2.,2.])); b=Box(np.array([.5,.5]),np.array([1.,1.]))
    assert a.contains_box(b) and a.intersects(b) and a.contains_point([1,1])

def test_affine_map_encloses_corners():
    b=Box(np.array([-1.,2.]),np.array([2.,3.])); A=np.array([[2.,-1.],[.5,1.]])
    m=b.affine_map(A)
    for x in ([i,j] for i in (-1,2) for j in (2,3)): assert m.contains_point(A@np.array(x,float))


import pytest


@pytest.mark.parametrize(("lower", "upper"), [
    ([0.0], [float("nan")]),
    ([float("-inf")], [1.0]),
    ([1.0], [0.0]),
    ([], []),
    ([[0.0, 1.0]], [[1.0, 2.0]]),
    ([0.0, 1.0], [1.0]),
])
def test_invalid_box_bounds_rejected(lower, upper):
    with pytest.raises(ValueError, match="box bounds"):
        Box(lower, upper)


@pytest.mark.parametrize("radius", [-0.1, float("inf"), float("nan")])
def test_invalid_uncertainty_radius_rejected(radius):
    with pytest.raises(ValueError, match="radius"):
        Box.around([0.0], radius)


def test_invalid_center_rejected():
    with pytest.raises(ValueError, match="center"):
        Box.around([float("nan")], 0.1)


def test_box_bounds_are_independent_of_caller_mutation():
    values = np.array([0.0, 1.0])
    interval = Box.point(values)
    values[0] = 99.0
    assert interval.lower.tolist() == [0.0, 1.0]
    with pytest.raises(ValueError):
        interval.lower[0] = 5.0


def test_dimension_mismatches_rejected_or_return_false():
    one = Box.point([0.0])
    two = Box.point([0.0, 0.0])
    assert not one.contains_box(two)
    assert not one.intersects(two)
    assert not one.contains_point([0.0, 0.0])
    with pytest.raises(ValueError, match="dimensions"):
        one.hull(two)
    with pytest.raises(ValueError, match="dimensions"):
        one.affine_map(np.eye(2))


def test_affine_map_nonfinite_coefficients_rejected():
    with pytest.raises(ValueError, match="coefficients"):
        Box.point([0.0]).affine_map([[float("inf")]])
