# Runtime Assurance CPS Safety Shield

**Reachability-Guided Runtime Assurance and Safety Shields for Cyber-Physical Systems Under Cyberattacks and Uncertainty**

This repository is a simulation-first research framework for **online safety enforcement** in cyber-physical systems (CPS). A nominal controller proposes an action; a runtime safety shield predicts a conservative reachable set under bounded state, action, disturbance, fault, and cyber-effect uncertainty; the action is accepted only when the predicted set remains inside a declared safe region. Otherwise the shield minimally modifies the action or falls back to a conservative command.

> **Research boundary:** this is not production safety software, a certified control system, or an operational attack toolkit. All domains and cyber effects are reduced-order, synthetic abstractions.

## Core question

> Can reachability-guided runtime assurance prevent unsafe controller actions under uncertainty and bounded cyber/fault effects while minimizing unnecessary intervention and preserving service?

## Architecture

```text
Physical CPS → Sensors / Digital Twin → Interval State Estimate
                                      ↓
Nominal Controller → proposed action → Runtime Safety Shield
                                      │
                         Reachability / Barrier Check
                             ↙                  ↘
                         safe                    unsafe
                          │                        │
                       accept             minimally modify
                                                   │
                                            fallback if needed
                                                   ↓
                                             Applied Action
```

## v0.2 capabilities

- affine discrete-time CPS models;
- outward-expanded interval/box uncertainty;
- finite-horizon hold-action reachability screening;
- one-step barrier-margin grid filter;
- composite shield fallback;
- interval measurement/twin fusion with disagreement inflation;
- bounded synthetic cyber/fault effects;
- minimal intervention objective via nearest safe action search;
- four domain adapters: battery, water, robot, railway;
- intervention, fallback, unsafe-state, margin, and service-cost metrics;
- **paired shielded-vs-unshielded benchmark evaluation on matched seeds**;
- explicit unsafe-state reduction and safety/service trade-off reporting;
- configurable benchmark artifacts with experiment metadata;
- deterministic tests and multi-version CI.

## Safety semantics

For a state estimate set \(X_t\), candidate action set \(U\), disturbance set \(W\), and discrete affine model

\[
x_{t+1}=Ax_t+Bu_t+c+w_t,
\]

the shield computes an over-approximated successor box

\[
\widehat{\mathcal R}_{t+1}=AX_t\oplus BU\oplus c\oplus W.
\]

A candidate is declared **certified safe by this v0.1 shield** only when each predicted box over the configured finite horizon is contained in the configured safe box. The claim is therefore conditional on the stated model, horizon, discretization, uncertainty bounds, and box over-approximation. It is **not** a universal safety proof.

## Quick start

```bash
pip install -e ".[dev]"
pytest -q
python scripts/run_demo.py
python scripts/run_benchmark.py
rtshield --domain battery --steps 40 --attack-scale 1.0
```

Run a larger paired benchmark with explicit experiment settings:

```bash
python scripts/run_benchmark.py \
  --steps 100 \
  --horizon 3 \
  --seeds 0 1 2 3 4 5 6 7 8 9 \
  --attack-scales 0 0.5 1 2 3 \
  --output results/paired-study.json
```

## Paired safety-versus-service evaluation

The benchmark now evaluates runtime assurance using **matched random seeds**. For every domain, attack scale, and seed, the same stochastic scenario is run once without the shield and once with the shield. This avoids comparing averages from unrelated random trials.

The paired summary reports:

- mean unsafe states without the shield;
- mean unsafe states with the shield;
- mean paired unsafe-state reduction;
- number of matched runs improved, worsened, or tied;
- intervention rate;
- fallback rate;
- mean intervention cost;
- minimum safety margin.

This design deliberately treats runtime assurance as a **safety-versus-service trade-off**. A shield should not be considered useful merely because it intervenes frequently; safety improvement must be interpreted together with the amount of control authority consumed.

See [`docs/paired-benchmark-protocol.md`](docs/paired-benchmark-protocol.md) for the experimental protocol, interpretation rules, statistical extension plan, and threats to validity.

## Domains

| Domain | State | Safety objective | Shielded action |
|---|---|---|---|
| Battery | SOC, temperature | SOC/thermal envelope | charge/discharge current command |
| Water | two tank levels | overflow/underflow envelope | pump commands |
| Robot | 2-D position/velocity | workspace/velocity envelope | acceleration |
| Railway | separation, closing speed | minimum separation envelope | abstract braking command |

## Research directions

1. Couple this framework directly to `automatic-formal-verification-cps` so offline reachable-set certificates parameterize online shields.
2. Replace finite action grids with convex/QP safety filters where assumptions permit.
3. Add nonlinear validated reachability and hybrid-mode shields.
4. Incorporate calibrated digital-twin uncertainty instead of fixed radii.
5. Evaluate attack-vs-fault-aware intervention policies.
6. Verify learning-enabled controllers and runtime-assurance wrappers.
7. Measure worst-case computation time and real-time feasibility.
8. Add bootstrap confidence intervals and preregistered sensitivity sweeps for the paired benchmark.

See `docs/` for semantics, assumptions, benchmark methodology, limitations, and the PhD research roadmap.
