#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from rtshield.benchmark import run_suite


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run paired runtime-assurance benchmark experiments."
    )
    parser.add_argument("--steps", type=int, default=50)
    parser.add_argument("--horizon", type=int, default=2)
    parser.add_argument(
        "--seeds",
        type=int,
        nargs="+",
        default=[0, 1, 2],
        help="Matched random seeds used for shielded and unshielded runs.",
    )
    parser.add_argument(
        "--attack-scales",
        type=float,
        nargs="+",
        default=[0.0, 1.0, 3.0],
        help="Synthetic bounded cyber/fault-effect scales to evaluate.",
    )
    parser.add_argument(
        "--output",
        default="results/v0_2_paired_benchmark.json",
        help="JSON output path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = run_suite(
        tuple(args.seeds),
        steps=args.steps,
        attack_scales=tuple(args.attack_scales),
        horizon=args.horizon,
    )

    artifact = {
        "benchmark_version": "0.2",
        "design": "paired shielded-vs-unshielded matched-seed comparison",
        "steps": args.steps,
        "horizon": args.horizon,
        "seeds": args.seeds,
        "attack_scales": args.attack_scales,
        "results": results,
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(artifact, indent=2))


if __name__ == "__main__":
    main()
