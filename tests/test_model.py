import numpy as np
from rtshield.models.affine import AffineDiscreteModel
from rtshield.sets.box import Box

def test_step_box_contains_nominal():
    m=AffineDiscreteModel(np.eye(2),np.eye(2),np.zeros(2),Box(np.array([-.1,-.1]),np.array([.1,.1])))
    xb=Box.around([1,2],[.2,.2]); ub=Box.point([.5,-.5]); r=m.step_box(xb,ub)
    assert r.contains_point(m.step_point([1,2],[.5,-.5]))
