import numpy as np
from rtshield.sets.box import Box
from rtshield.models.affine import AffineDiscreteModel
from rtshield.safety.properties import SafeBoxProperty
from rtshield.domains.common import DomainSpec

def make_spec():
    # state: separation (m), relative speed (m/s); positive relative speed closes gap
    dt=1.0
    A=np.array([[1.0,-dt],[0.0,0.96]])
    B=np.array([[0.0],[-0.8]])
    c=np.zeros(2)
    model=AffineDiscreteModel(A,B,c,Box(np.array([-0.5,-0.15]),np.array([0.5,0.15])),dt=dt,name="railway")
    safe=SafeBoxProperty(Box(np.array([25.0,-12.0]),np.array([500.0,12.0])),"minimum_separation")
    def ctrl(x): return np.array([max(0.0,min(1.0,(80.0-x[0])*0.03 + x[1]*0.10))])
    return DomainSpec("railway",model,safe,np.array([90.,5.]),np.array([0.]),np.array([1.]),np.array([1.]),ctrl,("separation_m","closing_speed"),("brake",),np.array([-1.0]))
