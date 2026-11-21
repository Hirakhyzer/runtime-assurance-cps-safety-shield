import numpy as np
from rtshield.models.affine import AffineDiscreteModel
from rtshield.sets.box import Box

def test_step_box_contains_nominal():
    m=AffineDiscreteModel(np.eye(2),np.eye(2),np.zeros(2),Box(np.array([-.1,-.1]),np.array([.1,.1])))
    xb=Box.around([1,2],[.2,.2]); ub=Box.point([.5,-.5]); r=m.step_box(xb,ub)
    assert r.contains_point(m.step_point([1,2],[.5,-.5]))


import pytest


def _valid_model(**overrides):
    data = dict(A=np.eye(2), B=np.ones((2, 1)), c=np.zeros(2),
                disturbance=Box.point([0.0, 0.0]), dt=0.1)
    data.update(overrides)
    return AffineDiscreteModel(**data)


@pytest.mark.parametrize(("field", "value"), [
    ("A", np.array([[float("nan"), 0], [0, 1]])),
    ("B", np.array([[float("inf")], [1.0]])),
    ("c", np.array([0.0, float("-inf")])),
    ("dt", 0.0),
    ("dt", float("nan")),
    ("dt", float("inf")),
    ("dt", True),
])
def test_invalid_model_parameters_rejected(field, value):
    with pytest.raises(ValueError):
        _valid_model(**{field: value})


def test_model_rejects_inconsistent_dimensions():
    with pytest.raises(ValueError, match="B"):
        _valid_model(B=np.eye(3))
    with pytest.raises(ValueError, match="disturbance"):
        _valid_model(disturbance=Box.point([0.0]))


def test_affine_model_copies_its_coefficients():
    source = np.eye(2)
    model = _valid_model(A=source)
    source[0, 0] = 100.0
    assert model.A[0, 0] == 1.0
    with pytest.raises(ValueError):
        model.A[0, 0] = 5.0


def test_invalid_step_inputs_rejected():
    model = _valid_model()
    with pytest.raises(ValueError, match="matching dimensions"):
        model.step_point([0.0], [0.0])
    with pytest.raises(ValueError, match="finite"):
        model.step_point([0.0, float("nan")], [0.0])
    with pytest.raises(ValueError, match="dimensions"):
        model.step_box(Box.point([0.0]), Box.point([0.0]))
    with pytest.raises(ValueError, match="dimensions"):
        model.step_box(Box.point([0.0, 0.0]), Box.point([0.0, 0.0]))
