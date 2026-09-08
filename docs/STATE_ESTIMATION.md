# State Estimation

The interval estimator builds a measurement box and, when available, a twin-prediction box. Consistent boxes are intersected. If they disagree, their hull is used and the source is explicitly marked as a disagreement. This is deliberately conservative and creates a useful hook for future calibrated probabilistic/twin uncertainty.
