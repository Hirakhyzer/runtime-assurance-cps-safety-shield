import numpy as np
from rtshield.sets.box import Box
from rtshield.models.affine import AffineDiscreteModel
from rtshield.safety.properties import SafeBoxProperty
from rtshield.domains.common import DomainSpec

def make_spec():
    dt=0.2
    A=np.array([[1,0,dt,0],[0,1,0,dt],[0,0,0.92,0],[0,0,0,0.92]],float)
    B=np.array([[0,0],[0,0],[dt,0],[0,dt]],float)
    model=AffineDiscreteModel(A,B,np.zeros(4),Box(np.array([-0.01,-0.01,-0.04,-0.04]),np.array([0.01,0.01,0.04,0.04])),dt=dt,name="robot")
    # workspace and velocity envelope; obstacle handled by controller/shield benchmark as additional corridor constraint
    safe=SafeBoxProperty(Box(np.array([-1,-2,-2,-2]),np.array([10,2,2,2])),"workspace_velocity")
    def ctrl(x):
        target=np.array([8.0,0.0]); pos=x[:2]; vel=x[2:]; return np.clip(0.45*(target-pos)-0.7*vel,-1.5,1.5)
    return DomainSpec("robot",model,safe,np.array([0.,0.,0.,0.]),np.ones(2)*-1.5,np.ones(2)*1.5,np.zeros(2),ctrl,("x","y","vx","vy"),("ax","ay"),np.array([1.0,0.6]))
