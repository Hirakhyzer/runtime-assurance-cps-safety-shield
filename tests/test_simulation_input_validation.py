"""Simulation input validation must precede expensive shield construction."""
import math

import pytest

from rtshield.domains import battery
from rtshield.simulation import run_domain


@pytest.mark.parametrize("kwargs,expected", [
    ({"steps": 0}, "steps"),
    ({"steps": True}, "steps"),
    ({"steps": 1.5}, "steps"),
    ({"horizon": 0}, "horizon"),
    ({"horizon": False}, "horizon"),
    ({"horizon": 2.5}, "horizon"),
    ({"seed": -1}, "seed"),
    ({"seed": True}, "seed"),
    ({"seed": 1.5}, "seed"),
    ({"attack_scale": -0.1}, "attack_scale"),
    ({"attack_scale": math.nan}, "attack_scale"),
    ({"attack_scale": math.inf}, "attack_scale"),
    ({"attack_scale": True}, "attack_scale"),
])
def test_invalid_direct_simulation_configuration(kwargs, expected):
    with pytest.raises(ValueError, match=expected):
        run_domain(battery.make_spec(), **kwargs)
