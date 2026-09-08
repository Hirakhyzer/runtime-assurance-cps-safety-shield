from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Box:
    lower: np.ndarray
    upper: np.ndarray

    def __post_init__(self):
        lo=np.asarray(self.lower,dtype=float); hi=np.asarray(self.upper,dtype=float)
        if lo.shape != hi.shape or np.any(lo>hi): raise ValueError("invalid box")
        object.__setattr__(self,"lower",lo); object.__setattr__(self,"upper",hi)

    @classmethod
    def around(cls, center, radius):
        c=np.asarray(center,float); r=np.broadcast_to(np.asarray(radius,float),c.shape)
        return cls(np.nextafter(c-r,-np.inf), np.nextafter(c+r,np.inf))

    @classmethod
    def point(cls, x):
        x=np.asarray(x,float); return cls(x.copy(),x.copy())

    @property
    def center(self): return (self.lower+self.upper)/2.0
    @property
    def radius(self): return (self.upper-self.lower)/2.0
    @property
    def dim(self): return int(self.lower.size)

    def contains_point(self,x):
        x=np.asarray(x,float); return bool(np.all(x>=self.lower) and np.all(x<=self.upper))
    def contains_box(self,other:'Box'):
        return bool(np.all(other.lower>=self.lower) and np.all(other.upper<=self.upper))
    def intersects(self,other:'Box'):
        return bool(np.all(self.lower<=other.upper) and np.all(other.lower<=self.upper))
    def inflate(self,radius):
        r=np.broadcast_to(np.asarray(radius,float),self.lower.shape)
        return Box(np.nextafter(self.lower-r,-np.inf),np.nextafter(self.upper+r,np.inf))
    def hull(self,other:'Box'):
        return Box(np.minimum(self.lower,other.lower),np.maximum(self.upper,other.upper))
    def affine_map(self,A,b=None):
        A=np.asarray(A,float); b=np.zeros(A.shape[0]) if b is None else np.asarray(b,float)
        c=A@self.center+b; r=np.abs(A)@self.radius
        return Box(np.nextafter(c-r,-np.inf),np.nextafter(c+r,np.inf))
