# Paired Runtime-Assurance Benchmark Protocol

## Purpose

Runtime assurance should be evaluated against the same underlying scenarios that an unshielded controller experiences. Comparing averages from unrelated random trials can hide scenario difficulty and exaggerate or obscure shield effects.

This protocol therefore uses **matched random seeds**: for each domain, attack scale, and seed, one unshielded run and one shielded run are generated from the same stochastic seed and configuration.

## Research Question

> Under matched disturbances and synthetic bounded cyber/fault effects, how much safety improvement does the runtime shield provide, and what intervention burden is required to obtain that improvement?

The benchmark does not assume that more intervention is always better. A useful shield should reduce unsafe behavior while avoiding unnecessary fallback and control modification.

## Experimental Unit

One paired experimental unit consists of:

- one CPS domain;
- one attack/fault-effect scale;
- one random seed;
- one simulation length;
- one reachability horizon;
- one unshielded run;
- one shielded run.

The shielded and unshielded conditions share the same seed so disturbance and measurement-noise realizations are comparable.

## Primary Outcomes

### Safety

- mean number of unsafe states in the unshielded condition;
- mean number of unsafe states in the shielded condition;
- mean paired unsafe-state reduction;
- number of matched runs where the shield improves, worsens, or ties the baseline;
- minimum safety margin.

A positive paired unsafe-state reduction means the shielded run visited fewer unsafe states than its matched baseline.

### Service and intervention burden

- intervention rate;
- fallback rate;
- mean intervention cost.

These metrics are reported alongside safety outcomes because a shield that preserves safety only by constantly overriding the nominal controller may be operationally unattractive even when it is conservative.

## Conditions

The default v0.2 benchmark evaluates:

- domains: battery, water, robot, railway;
- attack scales: `0.0`, `1.0`, and `3.0`;
- seeds: `0`, `1`, and `2`;
- simulation length: 50 steps;
- reachability horizon: 2 steps.

These are default research settings, not universal operating parameters. Published experiments should report the exact configuration and should increase the number of seeds before making statistical claims.

## Reproducibility

Run the default experiment with:

```bash
python scripts/run_benchmark.py
```

A custom run can be created with:

```bash
python scripts/run_benchmark.py \
  --steps 100 \
  --horizon 3 \
  --seeds 0 1 2 3 4 5 6 7 8 9 \
  --attack-scales 0 0.5 1 2 3 \
  --output results/paired-study.json
```

The output artifact records benchmark version, study design, step count, horizon, seeds, attack scales, and per-domain paired summaries.

## Interpretation Rules

1. Do not report aggregate safety improvement without also reporting intervention burden.
2. Do not treat a small number of deterministic seeds as evidence of general effectiveness.
3. Do not compare shielded and unshielded means from different seed sets.
4. Do not infer real-world cyber resilience from synthetic bounded attack-scale experiments.
5. Report domains separately before considering any cross-domain aggregate.
6. Preserve negative results, including scenarios where the shield worsens outcomes or introduces excessive fallback.

## Statistical Extension

The current implementation provides deterministic paired descriptive statistics. A larger study should add:

- bootstrap confidence intervals for paired unsafe-state reduction;
- paired non-parametric tests when distributions are non-normal;
- effect sizes with uncertainty intervals;
- sensitivity to horizon, grid density, uncertainty radius, and fallback policy;
- family-wise reporting across domains rather than pooling heterogeneous systems blindly.

## Threats to Validity

The current benchmark uses reduced-order synthetic models and synthetic cyber/fault effects. The nominal controllers, uncertainty radii, and action grids are co-designed with the research framework. This can bias results toward assumptions favorable to the shield.

Future evaluation should therefore include independently defined scenarios, externally sourced trajectories where feasible, alternative controllers, and parameter sweeps fixed before final analysis.

## Research Value

The paired protocol turns runtime assurance evaluation from a loose demonstration into a falsifiable safety-versus-service experiment. It makes clear whether improved safety is consistent across matched scenarios and what control authority the shield consumes to achieve it.
