from __future__ import annotations
from dataclasses import dataclass
import itertools, numpy as np
from rtshield.core.types import StateEstimate, ActionProposal, ShieldDecision, DecisionStatus
from rtshield.models.affine import AffineDiscreteModel
from rtshield.safety.properties import SafeBoxProperty
from rtshield.sets.box import Box

@dataclass
class ReachabilityShield:
    model: AffineDiscreteModel
    property: SafeBoxProperty
    action_lower: np.ndarray
    action_upper: np.ndarray
    fallback_action: np.ndarray
    horizon: int = 1
    grid_points: int = 9
    action_uncertainty: np.ndarray | float = 0.0
    extra_disturbance: Box|None = None

    def __post_init__(self):
        self.action_lower=np.asarray(self.action_lower,float); self.action_upper=np.asarray(self.action_upper,float)
        self.fallback_action=np.asarray(self.fallback_action,float)

    def _rollout_safe(self,state:Box,u:np.ndarray):
        ub=Box.around(u,self.action_uncertainty); cur=state; last=state; margin=float('inf')
        for _ in range(self.horizon):
            last=self.model.step_box(cur,ub,self.extra_disturbance)
            margin=min(margin,self.property.margin(last))
            if not self.property.satisfied_by(last): return False,last,margin
            cur=last
        return True,last,margin

    def _candidates(self,nominal):
        n=np.clip(np.asarray(nominal,float),self.action_lower,self.action_upper)
        yield n
        axes=[]
        for lo,hi,ni in zip(self.action_lower,self.action_upper,n):
            vals=np.linspace(lo,hi,self.grid_points); vals=np.unique(np.r_[vals,ni])
            axes.append(vals)
        seen={tuple(n.tolist())}
        combos=[]
        for c in itertools.product(*axes):
            a=np.asarray(c,float); key=tuple(a.tolist())
            if key in seen: continue
            seen.add(key); combos.append(a)
        combos.sort(key=lambda a: float(np.linalg.norm(a-n)))
        yield from combos

    def filter(self,estimate:StateEstimate,proposal:ActionProposal)->ShieldDecision:
        n=np.asarray(proposal.nominal,float)
        for i,u in enumerate(self._candidates(n)):
            ok,reach,margin=self._rollout_safe(estimate.uncertainty,u)
            if ok:
                norm=float(np.linalg.norm(u-n))
                status=DecisionStatus.ACCEPT if norm<=1e-12 else DecisionStatus.MODIFY
                return ShieldDecision(status,n,u,reach,"reachable set remains inside safe set",norm,{"candidate_rank":i,"margin":margin,"horizon":self.horizon})
        fb=np.clip(self.fallback_action,self.action_lower,self.action_upper)
        ok,reach,margin=self._rollout_safe(estimate.uncertainty,fb)
        return ShieldDecision(DecisionStatus.FALLBACK,n,fb,reach,"no certified-safe candidate on action grid" if not ok else "fallback selected",float(np.linalg.norm(fb-n)),{"fallback_safe":ok,"margin":margin,"horizon":self.horizon})
