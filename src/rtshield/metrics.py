from dataclasses import dataclass, asdict
import numpy as np
from rtshield.core.types import DecisionStatus

@dataclass
class RuntimeMetrics:
    steps:int=0; interventions:int=0; fallbacks:int=0; unsafe_states:int=0; intervention_cost:float=0.0; min_margin:float=float('inf')
    def update(self,decision,actual_safe:bool,margin:float):
        self.steps+=1; self.interventions+=decision.status!=DecisionStatus.ACCEPT; self.fallbacks+=decision.status==DecisionStatus.FALLBACK
        self.unsafe_states+=not actual_safe; self.intervention_cost+=decision.intervention_norm; self.min_margin=min(self.min_margin,margin)
    def summary(self):
        d=asdict(self); d['intervention_rate']=self.interventions/max(1,self.steps); d['fallback_rate']=self.fallbacks/max(1,self.steps); d['mean_intervention_cost']=self.intervention_cost/max(1,self.steps); return d
