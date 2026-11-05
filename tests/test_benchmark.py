from rtshield.benchmark import run_suite


def test_benchmark_has_all_domains_and_attack_scales():
    out = run_suite(seeds=(0,))
    assert set(out) == {"battery", "water", "robot", "railway"}

    # Each row is a paired shielded/unshielded comparison for one attack scale.
    for rows in out.values():
        assert len(rows) == 3
        assert {row["attack_scale"] for row in rows} == {0.0, 1.0, 3.0}
        assert all(row["seeds"] == [0] for row in rows)
