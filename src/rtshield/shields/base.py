from typing import Protocol
from rtshield.core.types import StateEstimate, ActionProposal, ShieldDecision
class SafetyShield(Protocol):
    def filter(self, estimate:StateEstimate, proposal:ActionProposal)->ShieldDecision: ...
