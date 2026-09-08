import numpy as np
from rtshield.estimation.interval import IntervalStateEstimator

def test_estimator_intersection_when_consistent():
    e=IntervalStateEstimator(.2,.2).estimate(np.array([1.]),np.array([1.1])); assert e.uncertainty.lower[0] <= 1.0 <= e.uncertainty.upper[0]

def test_estimator_hull_on_disagreement():
    e=IntervalStateEstimator(.1,.1).estimate(np.array([0.]),np.array([2.])); assert 'disagreement' in e.source and e.uncertainty.contains_point([0]) and e.uncertainty.contains_point([2])
