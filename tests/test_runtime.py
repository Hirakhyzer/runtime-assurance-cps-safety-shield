from rtshield.domains import battery,water,robot,railway
from rtshield.simulation import run_domain

def test_short_simulations_reproducible():
    for mod in (battery,water,robot,railway):
        s=mod.make_spec(); a,_=run_domain(s,steps=8,seed=4); b,_=run_domain(s,steps=8,seed=4); assert a==b

def test_metrics_fields():
    m,_=run_domain(battery.make_spec(),steps=5,seed=1); assert m['steps']==5 and 0<=m['intervention_rate']<=1


import pytest


@pytest.mark.parametrize(("field", "value"), [
    ("steps", 0),
    ("steps", 1.5),
    ("horizon", 0),
    ("horizon", 2.5),
    ("seed", -1),
    ("seed", True),
    ("attack_scale", -1.0),
    ("attack_scale", float("nan")),
    ("attack_scale", float("inf")),
])
def test_invalid_simulation_inputs_rejected(field, value):
    with pytest.raises(ValueError):
        run_domain(battery.make_spec(), **{field: value})
