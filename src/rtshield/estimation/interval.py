from dataclasses import dataclass
import numpy as np
from rtshield.core.types import StateEstimate
from rtshield.sets.box import Box

@dataclass
class IntervalStateEstimator:
    measurement_radius: np.ndarray|float
    twin_radius: np.ndarray|float

    def estimate(self,measurement,twin_prediction=None)->StateEstimate:
        m=np.asarray(measurement,float); mb=Box.around(m,self.measurement_radius)
        if twin_prediction is None: return StateEstimate(m,mb,"measurement")
        t=np.asarray(twin_prediction,float); tb=Box.around(t,self.twin_radius)
        lo=np.maximum(mb.lower,tb.lower); hi=np.minimum(mb.upper,tb.upper)
        if np.all(lo<=hi):
            b=Box(lo,hi); return StateEstimate(b.center,b,"measurement∩twin")
        b=mb.hull(tb); return StateEstimate(b.center,b,"measurement∪twin(disagreement)")
