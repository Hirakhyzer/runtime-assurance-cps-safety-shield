import numpy as np
from rtshield.sets.box import Box
from rtshield.models.affine import AffineDiscreteModel
from rtshield.safety.properties import SafeBoxProperty
from rtshield.shields.reachability import ReachabilityShield
from rtshield.core.types import StateEstimate,ActionProposal,DecisionStatus

def fixture():
    m=AffineDiscreteModel(np.eye(1),np.ones((1,1)),np.zeros(1),Box(np.array([0.]),np.array([0.])))
    p=SafeBoxProperty(Box(np.array([-1.]),np.array([1.])))
    return m,p

def test_accepts_safe_nominal():
    m,p=fixture(); s=ReachabilityShield(m,p,np.array([-1.]),np.array([1.]),np.array([0.]),grid_points=5)
    d=s.filter(StateEstimate(np.array([0.]),Box.around([0.],[.1])),ActionProposal(np.array([.2]))); assert d.status==DecisionStatus.ACCEPT

def test_modifies_unsafe_nominal():
    m,p=fixture(); s=ReachabilityShield(m,p,np.array([-2.]),np.array([2.]),np.array([0.]),grid_points=9)
    d=s.filter(StateEstimate(np.array([.9]),Box.around([.9],[.05])),ActionProposal(np.array([1.]))); assert d.status in (DecisionStatus.MODIFY,DecisionStatus.FALLBACK); assert d.applied_action[0] < 1

def test_multistep_is_more_conservative():
    m,p=fixture(); e=StateEstimate(np.array([0.]),Box.around([0.],[.01])); q=ActionProposal(np.array([.6]))
    d1=ReachabilityShield(m,p,np.array([-1.]),np.array([1.]),np.array([0.]),horizon=1,grid_points=9).filter(e,q)
    d2=ReachabilityShield(m,p,np.array([-1.]),np.array([1.]),np.array([0.]),horizon=3,grid_points=9).filter(e,q)
    assert d1.status==DecisionStatus.ACCEPT and d2.status!=DecisionStatus.ACCEPT


import pytest


@pytest.mark.parametrize("settings", [
    {"horizon": 0},
    {"horizon": 1.5},
    {"grid_points": 1},
    {"grid_points": True},
    {"action_lower": np.array([0.0, 0.0])},
    {"action_upper": np.array([float("nan")])},
    {"action_lower": np.array([2.0])},
    {"action_uncertainty": -0.1},
    {"action_uncertainty": float("inf")},
    {"extra_disturbance": Box.point([0.0, 0.0])},
])
def test_invalid_reachability_configuration_rejected(settings):
    model, prop = fixture()
    base = dict(model=model, property=prop, action_lower=np.array([-1.0]),
                action_upper=np.array([1.0]), fallback_action=np.array([0.0]))
    base.update(settings)
    with pytest.raises(ValueError):
        ReachabilityShield(**base)


@pytest.mark.parametrize("action", [
    [float("nan")], [float("inf")], [0.0, 0.0],
])
def test_invalid_reachability_action_rejected(action):
    model, prop = fixture()
    shield = ReachabilityShield(model, prop, np.array([-1.0]), np.array([1.0]),
                                np.array([0.0]))
    estimate = StateEstimate(np.array([0.0]), Box.point([0.0]))
    with pytest.raises(ValueError, match="nominal action"):
        shield.filter(estimate, ActionProposal(np.asarray(action)))


def test_invalid_reachability_estimate_dimension_rejected():
    model, prop = fixture()
    shield = ReachabilityShield(model, prop, np.array([-1.0]), np.array([1.0]),
                                np.array([0.0]))
    with pytest.raises(ValueError, match="state estimate"):
        shield.filter(StateEstimate(np.array([0.0]), Box.point([0.0, 0.0])),
                      ActionProposal(np.array([0.0])))
