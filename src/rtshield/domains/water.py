import numpy as np
from rtshield.sets.box import Box
from rtshield.models.affine import AffineDiscreteModel
from rtshield.safety.properties import SafeBoxProperty
from rtshield.domains.common import DomainSpec

def make_spec():
    A=np.array([[0.995,0.002],[0.002,0.994]])
    B=np.array([[0.06,0.0],[-0.01,0.05]])
    c=np.array([-0.01,-0.015])
    model=AffineDiscreteModel(A,B,c,Box(np.array([-0.015,-0.015]),np.array([0.015,0.015])),name="water")
    safe=SafeBoxProperty(Box(np.array([0.5,0.5]),np.array([9.2,9.2])),"tank_levels")
    def ctrl(x): return np.clip(np.array([(5.0-x[0])*0.35,(5.0-x[1])*0.35]),0,2)
    return DomainSpec("water",model,safe,np.array([5.0,5.0]),np.zeros(2),np.ones(2)*2,np.zeros(2),ctrl,("tank1","tank2"),("pump1","pump2"),np.array([1.0,1.0]))
