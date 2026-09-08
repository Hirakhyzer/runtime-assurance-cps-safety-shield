import numpy as np
from rtshield.sets.box import Box
from rtshield.models.affine import AffineDiscreteModel
from rtshield.safety.properties import SafeBoxProperty
from rtshield.domains.common import DomainSpec

def make_spec():
    A=np.array([[1.0,0.0],[0.0,0.985]])
    B=np.array([[0.0018],[0.10]])
    c=np.array([0.0,0.38])
    model=AffineDiscreteModel(A,B,c,Box(np.array([-0.0005,-0.08]),np.array([0.0005,0.08])),dt=1.0,name="battery")
    safe=SafeBoxProperty(Box(np.array([0.10,15.0]),np.array([0.95,55.0])),"soc_temperature")
    def ctrl(x): return np.array([4.0 if x[0]<0.75 else 0.5])
    return DomainSpec("battery",model,safe,np.array([0.60,28.0]),np.array([-3.0]),np.array([6.0]),np.array([0.0]),ctrl,("soc","temperature_c"),("current_cmd",),np.array([1.0]))
