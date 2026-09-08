import numpy as np
from rtshield.sets.box import Box

def test_box_contains_and_intersects():
    a=Box(np.array([0.,0.]),np.array([2.,2.])); b=Box(np.array([.5,.5]),np.array([1.,1.]))
    assert a.contains_box(b) and a.intersects(b) and a.contains_point([1,1])

def test_affine_map_encloses_corners():
    b=Box(np.array([-1.,2.]),np.array([2.,3.])); A=np.array([[2.,-1.],[.5,1.]])
    m=b.affine_map(A)
    for x in ([i,j] for i in (-1,2) for j in (2,3)): assert m.contains_point(A@np.array(x,float))
