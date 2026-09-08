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
