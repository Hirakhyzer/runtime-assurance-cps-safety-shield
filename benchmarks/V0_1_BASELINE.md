# Frozen v0.1 benchmark summary

Configuration: 50 steps, seeds 0/1/2, horizon 2, action grid 7, perturbation scales 0/1/3.

| Domain | Case | Unsafe states mean | Intervention rate mean |
|---|---|---:|---:|
| Battery | shielded, scale 3 | 0.0 | 0.173 |
| Water | shielded, scale 3 | 0.0 | 0.340 |
| Robot | unshielded, scale 0 | 5.0 | 0.000 |
| Robot | shielded, scale 0 | 0.0 | 0.127 |
| Robot | unshielded, scale 3 | 38.33 | 0.000 |
| Robot | shielded, scale 3 | 20.0 | 0.807 |
| Railway | shielded, scale 3 | 0.0 | 0.340 |

Do not interpret zero observed unsafe states as a formal proof. These are sampled simulation outcomes; the shield's internal certification is conditional on its model and reachable-set assumptions.
