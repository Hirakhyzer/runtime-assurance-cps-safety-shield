from dataclasses import dataclass
from rtshield.sets.box import Box

@dataclass(frozen=True)
class SafeBoxProperty:
    safe: Box
    name: str = "safe_region"
    def satisfied_by(self, reachable:Box)->bool: return self.safe.contains_box(reachable)
    def margin(self, reachable:Box)->float:
        import numpy as np
        return float(min(np.min(reachable.lower-self.safe.lower), np.min(self.safe.upper-reachable.upper)))
