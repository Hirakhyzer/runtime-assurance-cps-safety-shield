from rtshield.evaluation import summarize_paired_runs


def test_paired_summary_counts_improvement_and_service_cost() -> None:
    unshielded = [
        {
            "unsafe_states": 4,
            "intervention_rate": 0.0,
            "fallback_rate": 0.0,
            "mean_intervention_cost": 0.0,
            "min_margin": -0.2,
        },
        {
            "unsafe_states": 1,
            "intervention_rate": 0.0,
            "fallback_rate": 0.0,
            "mean_intervention_cost": 0.0,
            "min_margin": -0.1,
        },
    ]
    shielded = [
        {
            "unsafe_states": 1,
            "intervention_rate": 0.3,
            "fallback_rate": 0.1,
            "mean_intervention_cost": 0.2,
            "min_margin": 0.05,
        },
        {
            "unsafe_states": 1,
            "intervention_rate": 0.1,
            "fallback_rate": 0.0,
            "mean_intervention_cost": 0.1,
            "min_margin": 0.02,
        },
    ]

    result = summarize_paired_runs(unshielded, shielded)

    assert result.runs == 2
    assert result.unsafe_states_reduction_mean == 1.5
    assert result.shield_improved_runs == 1
    assert result.shield_tied_runs == 1
    assert result.shield_worsened_runs == 0
    assert result.intervention_rate_mean == 0.2


def test_paired_summary_rejects_unmatched_runs() -> None:
    sample = {
        "unsafe_states": 0,
        "intervention_rate": 0.0,
        "fallback_rate": 0.0,
        "mean_intervention_cost": 0.0,
        "min_margin": 1.0,
    }

    try:
        summarize_paired_runs([sample], [sample, sample])
    except ValueError as exc:
        assert "equal length" in str(exc)
    else:
        raise AssertionError("expected ValueError for unmatched paired runs")
