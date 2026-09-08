from dataclasses import dataclass
import numpy as np
from rtshield.core.types import ActionProposal

@dataclass
class RuntimeAssuranceSupervisor:
    estimator: object
    shield: object
    controller: object

    def step(self,measurement,twin_prediction=None):
        estimate=self.estimator.estimate(measurement,twin_prediction)
        nominal=np.asarray(self.controller(estimate.center),float)
        decision=self.shield.filter(estimate,ActionProposal(nominal))
        return estimate,decision
