from rtshield.benchmark import run_suite


def test_benchmark_has_all_domains_and_attack_scales():
    out = run_suite(seeds=(0,))
    assert set(out) == {"battery", "water", "robot", "railway"}

    # Each row is a paired shielded/unshielded comparison for one attack scale.
    for rows in out.values():
        assert len(rows) == 3
        assert {row["attack_scale"] for row in rows} == {0.0, 1.0, 3.0}
        assert all(row["seeds"] == [0] for row in rows)


import pytest


@pytest.mark.parametrize(("field", "value"), [
    ("seeds", ()),
    ("seeds", (-1,)),
    ("seeds", (0, 0)),
    ("seeds", (True,)),
    ("seeds", (1.5,)),
    ("steps", 0),
    ("steps", 2.5),
    ("horizon", 0),
    ("horizon", True),
    ("attack_scales", ()),
    ("attack_scales", (-1.0,)),
    ("attack_scales", (float("nan"),)),
    ("attack_scales", (float("inf"),)),
    ("attack_scales", (0.0, 0.0)),
])
def test_invalid_benchmark_configuration_fails_before_running(field, value):
    with pytest.raises(ValueError):
        run_suite(**{field: value})
