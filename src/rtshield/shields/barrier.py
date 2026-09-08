from __future__ import annotations
from dataclasses import dataclass
import itertools, numpy as np
from rtshield.core.types import StateEstimate, ActionProposal, ShieldDecision, DecisionStatus
from rtshield.models.affine import AffineDiscreteModel
from rtshield.safety.properties import SafeBoxProperty
from rtshield.sets.box import Box

@dataclass
class BarrierGridShield:
    """Grid-search safety filter using a one-step box-margin barrier surrogate."""
    model: AffineDiscreteModel
    property: SafeBoxProperty
    action_lower: np.ndarray
    action_upper: np.ndarray
    fallback_action: np.ndarray
    grid_points: int = 21
    action_uncertainty: float|np.ndarray = 0.0

    def __post_init__(self):
        self.action_lower=np.asarray(self.action_lower,float); self.action_upper=np.asarray(self.action_upper,float); self.fallback_action=np.asarray(self.fallback_action,float)

    def filter(self,estimate:StateEstimate,proposal:ActionProposal)->ShieldDecision:
        n=np.asarray(proposal.nominal,float)
        axes=[np.unique(np.r_[np.linspace(lo,hi,self.grid_points),np.clip(ni,lo,hi)]) for lo,hi,ni in zip(self.action_lower,self.action_upper,n)]
        best=None
        for combo in itertools.product(*axes):
            u=np.asarray(combo,float); reach=self.model.step_box(estimate.uncertainty,Box.around(u,self.action_uncertainty))
            m=self.property.margin(reach)
            if m>=0:
                cost=float(np.linalg.norm(u-n))
                if best is None or cost<best[0]: best=(cost,u,reach,m)
        if best is not None:
            cost,u,reach,m=best
            st=DecisionStatus.ACCEPT if cost<=1e-12 else DecisionStatus.MODIFY
            return ShieldDecision(st,n,u,reach,"one-step barrier margin nonnegative",cost,{"barrier_margin":m})
        fb=np.clip(self.fallback_action,self.action_lower,self.action_upper); reach=self.model.step_box(estimate.uncertainty,Box.around(fb,self.action_uncertainty))
        return ShieldDecision(DecisionStatus.FALLBACK,n,fb,reach,"no action on barrier grid satisfies one-step safety margin",float(np.linalg.norm(fb-n)),{"barrier_margin":self.property.margin(reach)})
