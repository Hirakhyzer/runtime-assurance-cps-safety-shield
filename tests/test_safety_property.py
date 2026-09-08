import numpy as np
from rtshield.sets.box import Box
from rtshield.safety.properties import SafeBoxProperty

def test_margin_sign():
    p=SafeBoxProperty(Box(np.array([0.]),np.array([1.])))
    assert p.margin(Box(np.array([.2]),np.array([.8])))>0
    assert p.margin(Box(np.array([-.1]),np.array([.8])))<0
