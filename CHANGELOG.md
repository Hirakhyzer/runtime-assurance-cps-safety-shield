# Changelog

## v0.1.1 — 2026-11-22

- Reject non-finite, inverted, empty, or non-vector state/action interval bounds and negative uncertainty radii.
- Copy interval bounds and affine model coefficients so external array mutations cannot silently change validated research inputs.
- Validate affine state and action dimensions, finite model matrices, and positive time steps; reject malformed propagation inputs.
- Reject invalid reachability horizons, grid densities, action bounds, action uncertainties, fallback dimensions, and state estimates in reachability/barrier filters.
- Validate simulation and paired-benchmark seed sets, step counts, horizons, and finite nonnegative synthetic attack scales.
- Add regression coverage for all the input-integrity checks; preserve valid-input behavior and existing synthetic model assumptions.

These checks improve integrity of the *model-conditioned* calculations. They are not a formal proof of implementation correctness or safety of a deployed CPS.

## Previous baseline — v0.1.0

- Runtime-assurance research package, finite-horizon reachability and barrier shields, synthetic CPS domains, deterministic paired benchmark, and decision audits.

Note: The benchmark artifact's `benchmark_version: "0.2"` names its experimental report format. It is separate from the Python package version.
