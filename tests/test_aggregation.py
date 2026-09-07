import pytest

from aggregation import aggregate_weights


def test_aggregate_weights_reference_case():
    """Verify geometric aggregation for two decision makers."""

    all_weights = [
        [0.6, 0.3, 0.1],
        [0.3, 0.4, 0.3],
    ]

    aggregated_weights = aggregate_weights(all_weights)

    expected_weights = [
        0.4494897427831781,
        0.36700683814454793,
        0.18350341907227397,
    ]

    assert aggregated_weights == pytest.approx(
        expected_weights,
        abs=1e-9,
    )


def test_aggregated_weights_sum_to_one():
    """Verify that aggregated weights are normalized."""

    all_weights = [
        [0.6, 0.3, 0.1],
        [0.3, 0.4, 0.3],
    ]

    aggregated_weights = aggregate_weights(all_weights)

    assert sum(aggregated_weights) == pytest.approx(
        1.0,
        abs=1e-9,
    )


def test_single_decision_maker_preserves_weights():
    """Verify aggregation behavior with only one decision maker."""

    all_weights = [
        [0.5, 0.3, 0.2],
    ]

    aggregated_weights = aggregate_weights(all_weights)

    assert aggregated_weights == pytest.approx(
        [0.5, 0.3, 0.2],
        abs=1e-9,
    )


def test_aggregated_weights_are_non_negative():
    """Verify that aggregated weights are non-negative."""

    all_weights = [
        [0.6, 0.3, 0.1],
        [0.3, 0.4, 0.3],
    ]

    aggregated_weights = aggregate_weights(all_weights)

    assert all(weight >= 0 for weight in aggregated_weights)