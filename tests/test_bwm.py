import pytest

from bwm import solve_bwm


def test_solve_bwm_reference_case():
    """Verify BWM results for a fixed regression case."""

    best_index = 0
    worst_index = 2

    best_to_others = [1, 3, 5]
    others_to_worst = [5, 2, 1]

    weights, xi = solve_bwm(
        best_index,
        worst_index,
        best_to_others,
        others_to_worst,
    )

    expected_weights = [0.650, 0.225, 0.125]
    expected_xi = 0.025

    assert weights == pytest.approx(expected_weights, abs=1e-9)
    assert xi == pytest.approx(expected_xi, abs=1e-9)


def test_bwm_weights_sum_to_one():
    """Verify that the BWM weights are normalized."""

    best_index = 0
    worst_index = 2

    best_to_others = [1, 3, 5]
    others_to_worst = [5, 2, 1]

    weights, _ = solve_bwm(
        best_index,
        worst_index,
        best_to_others,
        others_to_worst,
    )

    assert sum(weights) == pytest.approx(1.0, abs=1e-9)


def test_bwm_weights_are_non_negative():
    """Verify that all BWM weights are non-negative."""

    weights, _ = solve_bwm(
        best_index=0,
        worst_index=2,
        best_to_others=[1, 3, 5],
        others_to_worst=[5, 2, 1],
    )

    assert all(weight >= 0 for weight in weights)