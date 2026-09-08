from rtshield.benchmark import run_suite

def test_benchmark_has_all_domains_and_modes():
    out=run_suite(seeds=(0,)); assert set(out)=={'battery','water','robot','railway'}
    assert all(len(v)==6 for v in out.values())
