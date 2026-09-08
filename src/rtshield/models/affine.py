from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from rtshield.sets.box import Box

@dataclass(frozen=True)
class AffineDiscreteModel:
    A: np.ndarray
    B: np.ndarray
    c: np.ndarray
    disturbance: Box
    dt: float = 1.0
    name: str = "affine"

    def __post_init__(self):
        A=np.asarray(self.A,float); B=np.asarray(self.B,float); c=np.asarray(self.c,float)
        if A.ndim!=2 or A.shape[0]!=A.shape[1]: raise ValueError("A square")
        if B.ndim!=2 or B.shape[0]!=A.shape[0]: raise ValueError("B shape")
        if c.shape!=(A.shape[0],) or self.disturbance.dim!=A.shape[0]: raise ValueError("state shape")
        object.__setattr__(self,'A',A); object.__setattr__(self,'B',B); object.__setattr__(self,'c',c)

    @property
    def state_dim(self): return self.A.shape[0]
    @property
    def action_dim(self): return self.B.shape[1]

    def step_point(self,x,u,w=None):
        w=np.zeros(self.state_dim) if w is None else np.asarray(w,float)
        return self.A@np.asarray(x,float)+self.B@np.asarray(u,float)+self.c+w

    def step_box(self,x_box:Box,u_box:Box,extra_disturbance:Box|None=None):
        xb=x_box.affine_map(self.A,self.c)
        ub=u_box.affine_map(self.B)
        lo=xb.lower+ub.lower+self.disturbance.lower
        hi=xb.upper+ub.upper+self.disturbance.upper
        if extra_disturbance is not None:
            lo=lo+extra_disturbance.lower; hi=hi+extra_disturbance.upper
        return Box(np.nextafter(lo,-np.inf),np.nextafter(hi,np.inf))
