from __future__ import annotations

from math import isfinite

from rtshield.domains import battery, railway, robot, water
from rtshield.evaluation import summarize_paired_runs
from rtshield.simulation import run_domain


def run_suite(
    seeds: tuple[int, ...] = (0, 1, 2),
    *,
    steps: int = 50,
    attack_scales: tuple[float, ...] = (0.0, 1.0, 3.0),
    horizon: int = 2,
) -> dict:
    """Run paired shielded/unshielded experiments across domains.

    For each domain, attack scale, and seed, the shielded and unshielded
    conditions use the same stochastic seed. The returned comparison therefore
    measures within-scenario safety and service differences rather than mixing
    independent random trials.
    """
    if not seeds:
        raise ValueError("at least one benchmark seed is required")
    if any(isinstance(seed, bool) or not isinstance(seed, int) or seed < 0 for seed in seeds):
        raise ValueError("benchmark seeds must be nonnegative integers")
    if len(set(seeds)) != len(seeds):
        raise ValueError("benchmark seeds must be unique")
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1:
        raise ValueError("steps must be a positive integer")
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 1:
        raise ValueError("horizon must be a positive integer")
    if not attack_scales:
        raise ValueError("at least one attack scale is required")
    if any(isinstance(scale, bool) or not isinstance(scale, (int, float))
           or not isfinite(scale) or scale < 0 for scale in attack_scales):
        raise ValueError("attack scales must be finite and nonnegative")
    if len(set(attack_scales)) != len(attack_scales):
        raise ValueError("attack scales must be unique")

    output: dict[str, list[dict]] = {}
    for module in (battery, water, robot, railway):
        spec = module.make_spec()
        rows: list[dict] = []

        for attack_scale in attack_scales:
            unshielded_runs = []
            shielded_runs = []

            for seed in seeds:
                baseline_metrics, _ = run_domain(
                    spec,
                    steps=steps,
                    seed=seed,
                    shielded=False,
                    attack_scale=attack_scale,
                    horizon=horizon,
                )
                shield_metrics, _ = run_domain(
                    spec,
                    steps=steps,
                    seed=seed,
                    shielded=True,
                    attack_scale=attack_scale,
                    horizon=horizon,
                )
                unshielded_runs.append(baseline_metrics)
                shielded_runs.append(shield_metrics)

            comparison = summarize_paired_runs(unshielded_runs, shielded_runs)
            rows.append(
                {
                    "attack_scale": attack_scale,
                    "steps": steps,
                    "horizon": horizon,
                    "seeds": list(seeds),
                    **comparison.to_dict(),
                }
            )

        output[spec.name] = rows

    return output
