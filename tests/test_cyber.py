import numpy as np
from rtshield.cyber.effects import BoundedCyberEffect, compose_effects

def test_compose_effects():
    e=[BoundedCyberEffect('a',np.array([-1.,0]),np.array([1.,.2]))]
    b=compose_effects(e,2,'state'); assert np.allclose(b.lower,[-1,0]) and np.allclose(b.upper,[1,.2])
