# Limitations

- v0.1 uses affine discrete-time models and box over-approximations.
- the reachability shield assumes a held action over its prediction horizon.
- action search is grid-based and does not scale well with action dimension.
- the robot example currently verifies a workspace/velocity envelope, not nonconvex obstacle avoidance.
- `FALLBACK` does not mean the fallback action was formally certified.
- fixed interval radii are illustrative, not statistically calibrated.
- no hard real-time timing guarantee is provided.
- no production certification or standards compliance is claimed.
