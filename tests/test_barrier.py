import numpy as np
from rtshield.sets.box import Box
from rtshield.models.affine import AffineDiscreteModel
from rtshield.safety.properties import SafeBoxProperty
from rtshield.shields.barrier import BarrierGridShield
from rtshield.core.types import StateEstimate,ActionProposal

def test_barrier_filter_returns_safe_candidate():
    m=AffineDiscreteModel(np.eye(1),np.ones((1,1)),np.zeros(1),Box.point([0.])); p=SafeBoxProperty(Box(np.array([-1.]),np.array([1.])))
    s=BarrierGridShield(m,p,np.array([-1.]),np.array([1.]),np.array([0.]),grid_points=21)
    d=s.filter(StateEstimate(np.array([.95]),Box.around([.95],[.01])),ActionProposal(np.array([.5])))
    assert p.satisfied_by(d.predicted_reachable)
