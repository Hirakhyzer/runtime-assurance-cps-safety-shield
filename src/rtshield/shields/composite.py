from dataclasses import dataclass
from rtshield.core.types import StateEstimate, ActionProposal, DecisionStatus

@dataclass
class CompositeShield:
    primary: object
    secondary: object
    def filter(self,estimate:StateEstimate,proposal:ActionProposal):
        d=self.primary.filter(estimate,proposal)
        if d.status != DecisionStatus.FALLBACK: return d
        d2=self.secondary.filter(estimate,proposal)
        d2.metadata["primary_failed"]=True
        return d2
