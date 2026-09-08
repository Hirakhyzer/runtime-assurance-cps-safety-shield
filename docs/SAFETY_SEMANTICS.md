# Safety Semantics

`ACCEPT` means the nominal action passed the configured finite-horizon box-reachability check. `MODIFY` means a nearby action passed. `FALLBACK` means the candidate grid did not produce a certified-safe action; the configured fallback is applied, but it is **not automatically certified**.

These statuses are conditional on model fidelity, uncertainty bounds, discrete-time abstraction, horizon, and numerical implementation. They are not deployment certificates.
