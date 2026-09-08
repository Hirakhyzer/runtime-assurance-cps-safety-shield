from dataclasses import dataclass
import numpy as np
from rtshield.sets.box import Box

@dataclass(frozen=True)
class BoundedCyberEffect:
    name: str
    lower: np.ndarray
    upper: np.ndarray
    target: str = "state"
    def as_box(self): return Box(np.asarray(self.lower,float),np.asarray(self.upper,float))

def compose_effects(effects:list[BoundedCyberEffect],dim:int,target:str)->Box:
    lo=np.zeros(dim); hi=np.zeros(dim)
    for e in effects:
        if e.target==target:
            lo+=e.as_box().lower; hi+=e.as_box().upper
    return Box(lo,hi)
