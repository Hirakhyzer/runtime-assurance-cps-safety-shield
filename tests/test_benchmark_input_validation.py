"""Input-contract regression tests for reproducible paired experiments."""
import math

import pytest

from rtshield.benchmark import run_suite


@pytest.mark.parametrize("seeds", [(), (1, 1), (True,), (1.5,), ("1",)])
def test_invalid_seed_sets_rejected(seeds):
    with pytest.raises(ValueError, match="seed"):
        run_suite(seeds=seeds)


@pytest.mark.parametrize("steps,horizon", [(0, 1), (True, 1), (1.5, 1), (1, 0), (1, True), (1, 1.5)])
def test_invalid_step_and_horizon_values_rejected(steps, horizon):
    with pytest.raises(ValueError, match="steps|horizon"):
        run_suite(steps=steps, horizon=horizon)


@pytest.mark.parametrize("scales", [(), (-1.0,), (math.nan,), (math.inf,), (-math.inf,), (True,), ("1",)])
def test_invalid_attack_scales_rejected(scales):
    with pytest.raises(ValueError, match="attack scale"):
        run_suite(attack_scales=scales)
