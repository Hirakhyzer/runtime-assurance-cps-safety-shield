from dataclasses import dataclass
from rtshield.models.affine import AffineDiscreteModel
from rtshield.sets.box import Box

@dataclass
class ReachabilityPredictor:
    model: AffineDiscreteModel
    horizon: int = 1

    def predict_hold(self,state:Box,action:Box,extra_disturbance:Box|None=None)->list[Box]:
        out=[]; cur=state
        for _ in range(self.horizon):
            cur=self.model.step_box(cur,action,extra_disturbance)
            out.append(cur)
        return out
