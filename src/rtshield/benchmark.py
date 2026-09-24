from __future__ import annotations

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
    if steps < 1:
        raise ValueError("steps must be positive")
    if horizon < 1:
        raise ValueError("horizon must be positive")

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
