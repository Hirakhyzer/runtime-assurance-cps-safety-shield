import numpy as np
from rtshield.domains.battery import make_spec
from rtshield.estimation.interval import IntervalStateEstimator
from rtshield.shields.reachability import ReachabilityShield
from rtshield.shields.barrier import BarrierGridShield
from rtshield.shields.composite import CompositeShield
from rtshield.core.types import ActionProposal

def test_composite_runs():
    s=make_spec(); e=IntervalStateEstimator(.02,.04).estimate(s.initial_state,s.initial_state)
    a=ReachabilityShield(s.model,s.property,s.action_lower,s.action_upper,s.fallback_action,horizon=2,grid_points=5)
    b=BarrierGridShield(s.model,s.property,s.action_lower,s.action_upper,s.fallback_action,grid_points=11)
    d=CompositeShield(a,b).filter(e,ActionProposal(np.array([6.]))); assert d.applied_action.shape==(1,)
