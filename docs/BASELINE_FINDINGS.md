# v0.1 Baseline Findings

The v0.1 benchmark uses three deterministic seeds, 50 steps per run, finite-horizon box reachability, and synthetic telemetry/controller-output perturbations. These results characterize **this reduced-order implementation only**.

## Key observations

- **Robot, nominal:** the unshielded controller leaves the configured workspace/velocity safe box for about 5 steps on average; the shielded controller records 0 unsafe states while intervening on about 12.7% of steps.
- **Robot, moderate synthetic corruption (scale 1):** shielded runs remain at 0 unsafe states with about 16.7% intervention.
- **Robot, severe synthetic corruption (scale 3):** the shield is not sufficient. Unsafe states average 20 steps even though the shield intervenes on about 80.7% of steps. The unshielded case is worse (about 38.3 unsafe steps), but this is **not** a safety guarantee.
- **Battery:** no unsafe state is observed in the short baseline. At the highest perturbation scale the shield intervenes on about 17.3% of steps, showing that the predictive enclosure becomes safety-relevant before the realized trajectory crosses the boundary.
- **Water:** no unsafe state is observed in the short baseline; the highest perturbation scale induces about 34% intervention.
- **Railway:** no realized minimum-separation violation is observed in this simplified baseline. Corrupted braking proposals increase shield intervention to about 34% of steps, illustrating a conservatism/service tradeoff rather than a demonstrated collision-prevention result.

## Research implication

A runtime shield should not be judged only by whether it intervenes. The severe robot scenario shows that high intervention can coexist with safety failure when the model, action set, fallback, or horizon is inadequate. The next research stage should therefore measure **shield feasibility**, distinguish `no safe action exists` from `search failed to find one`, and use offline reachable-set analysis to precompute invariant backup regions.
