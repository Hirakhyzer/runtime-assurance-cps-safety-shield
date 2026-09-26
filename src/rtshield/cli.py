from __future__ import annotations

import argparse
import json
from pathlib import Path

from rtshield.domains import battery, railway, robot, water
from rtshield.simulation import run_domain


MODS = {
    "battery": battery,
    "water": water,
    "robot": robot,
    "railway": railway,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reachability-guided runtime assurance simulator"
    )
    parser.add_argument("--domain", choices=MODS, default="battery")
    parser.add_argument("--steps", type=int, default=40)
    parser.add_argument("--attack-scale", type=float, default=0.0)
    parser.add_argument("--horizon", type=int, default=2)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--unshielded", action="store_true")
    parser.add_argument(
        "--trace-output",
        help="write step-level shield audit evidence to a JSON file",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    metrics, records = run_domain(
        MODS[args.domain].make_spec(),
        steps=args.steps,
        seed=args.seed,
        attack_scale=args.attack_scale,
        shielded=not args.unshielded,
        horizon=args.horizon,
    )
    print(json.dumps(metrics, indent=2))

    if args.trace_output:
        path = Path(args.trace_output)
        path.parent.mkdir(parents=True, exist_ok=True)
        artifact = {
            "domain": args.domain,
            "steps": args.steps,
            "seed": args.seed,
            "attack_scale": args.attack_scale,
            "horizon": args.horizon,
            "shielded": not args.unshielded,
            "metrics": metrics,
            "records": records,
        }
        path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
