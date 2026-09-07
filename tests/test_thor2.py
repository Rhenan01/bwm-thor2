import pytest

from thor2 import (
    discordance_s1,
    discordance_s2,
    discordance_s3,
    mean_pertinence,
    performance_difference,
    preference_relation,
    scenario_s1,
    scenario_s2,
    scenario_s3,
)


def test_strict_preference_a_over_b():
    assert preference_relation(
        a=10,
        b=5,
        preference_threshold=3,
        indifference_threshold=1,
    ) == "aPb"


def test_weak_preference_a_over_b():
    assert preference_relation(
        a=8,
        b=6,
        preference_threshold=3,
        indifference_threshold=1,
    ) == "aQb"


def test_indifference_a_over_b():
    assert preference_relation(
        a=7,
        b=6.5,
        preference_threshold=3,
        indifference_threshold=1,
    ) == "aIb"


def test_indifference_b_over_a():
    assert preference_relation(
        a=6.5,
        b=7,
        preference_threshold=3,
        indifference_threshold=1,
    ) == "bIa"


def test_weak_preference_b_over_a():
    assert preference_relation(
        a=6,
        b=8,
        preference_threshold=3,
        indifference_threshold=1,
    ) == "bQa"


def test_strict_preference_b_over_a():
    assert preference_relation(
        a=5,
        b=10,
        preference_threshold=3,
        indifference_threshold=1,
    ) == "bPa"

def test_preference_threshold_boundary():
    """
    At exactly p, the current implementation classifies the
    relation as weak preference, not strict preference.
    """

    assert preference_relation(
        a=8,
        b=5,
        preference_threshold=3,
        indifference_threshold=1,
    ) == "aQb"


def test_indifference_threshold_boundary():
    """
    At exactly q, the current implementation classifies the
    relation as indifference.
    """

    assert preference_relation(
        a=6,
        b=5,
        preference_threshold=3,
        indifference_threshold=1,
    ) == "aIb"


def test_negative_indifference_threshold_boundary():
    assert preference_relation(
        a=5,
        b=6,
        preference_threshold=3,
        indifference_threshold=1,
    ) == "bIa"


def test_negative_preference_threshold_boundary():
    assert preference_relation(
        a=5,
        b=8,
        preference_threshold=3,
        indifference_threshold=1,
    ) == "bQa"

def test_thor2_scenario_s1_reference_case():
    relations = [
        "aPb",
        "aQb",
        "aIb",
        "bIa",
        "bQa",
        "bPa",
    ]

    differences = [
        5.0,
        2.0,
        0.5,
        -0.5,
        -2.0,
        -5.0,
    ]

    pertinences = [1.0] * 6

    weights = [
        0.30,
        0.20,
        0.15,
        0.10,
        0.10,
        0.15,
    ]

    preference_thresholds = [3.0] * 6
    indifference_thresholds = [1.0] * 6

    result = scenario_s1(
        relations,
        differences,
        pertinences,
        weights,
        preference_thresholds,
        indifference_thresholds,
    )

    assert result == "does not dominate"


def test_thor2_scenario_s2_reference_case():
    relations = [
        "aPb",
        "aQb",
        "aIb",
        "bIa",
        "bQa",
        "bPa",
    ]

    differences = [
        5.0,
        2.0,
        0.5,
        -0.5,
        -2.0,
        -5.0,
    ]

    pertinences = [1.0] * 6

    weights = [
        0.30,
        0.20,
        0.15,
        0.10,
        0.10,
        0.15,
    ]

    preference_thresholds = [3.0] * 6
    indifference_thresholds = [1.0] * 6

    result = scenario_s2(
        relations,
        differences,
        pertinences,
        weights,
        preference_thresholds,
        indifference_thresholds,
    )

    assert result == "dominates"


def test_thor2_scenario_s3_reference_case():
    relations = [
        "aPb",
        "aQb",
        "aIb",
        "bIa",
        "bQa",
        "bPa",
    ]

    differences = [
        5.0,
        2.0,
        0.5,
        -0.5,
        -2.0,
        -5.0,
    ]

    pertinences = [1.0] * 6

    weights = [
        0.30,
        0.20,
        0.15,
        0.10,
        0.10,
        0.15,
    ]

    preference_thresholds = [3.0] * 6
    indifference_thresholds = [1.0] * 6

    result = scenario_s3(
        relations,
        differences,
        pertinences,
        weights,
        preference_thresholds,
        indifference_thresholds,
    )

    assert result == "dominates"

def test_discordance_s1_reference_case():
    differences = [5.0, 2.0, 0.5, -0.5, -2.0, -5.0]

    relations = [
        "aPb",
        "aQb",
        "aIb",
        "bIa",
        "bQa",
        "bPa",
    ]

    pertinences = [1.0] * 6

    weights = [
        0.30,
        0.20,
        0.15,
        0.10,
        0.10,
        0.15,
    ]

    preference_thresholds = [3.0] * 6
    indifference_thresholds = [1.0] * 6
    discordance_thresholds = [10.0] * 6

    result = discordance_s1(
        differences,
        relations,
        pertinences,
        weights,
        preference_thresholds,
        indifference_thresholds,
        discordance_thresholds,
    )

    assert result == pytest.approx(0.375, abs=1e-9)


def test_discordance_s2_reference_case():
    differences = [5.0, 2.0, 0.5, -0.5, -2.0, -5.0]

    relations = [
        "aPb",
        "aQb",
        "aIb",
        "bIa",
        "bQa",
        "bPa",
    ]

    pertinences = [1.0] * 6

    weights = [
        0.30,
        0.20,
        0.15,
        0.10,
        0.10,
        0.15,
    ]

    preference_thresholds = [3.0] * 6
    indifference_thresholds = [1.0] * 6
    discordance_thresholds = [10.0] * 6

    result = discordance_s2(
        differences,
        relations,
        pertinences,
        weights,
        preference_thresholds,
        indifference_thresholds,
        discordance_thresholds,
    )

    assert result == pytest.approx(0.5625, abs=1e-9)


def test_discordance_s3_reference_case():
    differences = [5.0, 2.0, 0.5, -0.5, -2.0, -5.0]

    relations = [
        "aPb",
        "aQb",
        "aIb",
        "bIa",
        "bQa",
        "bPa",
    ]

    pertinences = [1.0] * 6

    weights = [
        0.30,
        0.20,
        0.15,
        0.10,
        0.10,
        0.15,
    ]

    preference_thresholds = [3.0] * 6
    indifference_thresholds = [1.0] * 6
    discordance_thresholds = [10.0] * 6

    result = discordance_s3(
        differences,
        relations,
        pertinences,
        weights,
        preference_thresholds,
        indifference_thresholds,
        discordance_thresholds,
    )

    assert result == pytest.approx(0.71875, abs=1e-9)

def test_discordance_s1_returns_half_when_threshold_is_reached():
    result = discordance_s1(
        differences=[5.0, -2.0],
        relations=["aPb", "bQa"],
        pertinences=[1.0, 1.0],
        weights=[0.6, 0.4],
        preference_thresholds=[3.0, 3.0],
        indifference_thresholds=[1.0, 1.0],
        discordance_thresholds=[10.0, 2.0],
    )

    assert result == pytest.approx(0.5, abs=1e-9)


def test_discordance_s2_returns_half_when_threshold_is_reached():
    result = discordance_s2(
        differences=[5.0, -2.0],
        relations=["aPb", "bQa"],
        pertinences=[1.0, 1.0],
        weights=[0.6, 0.4],
        preference_thresholds=[3.0, 3.0],
        indifference_thresholds=[1.0, 1.0],
        discordance_thresholds=[10.0, 2.0],
    )

    assert result == pytest.approx(0.5, abs=1e-9)


def test_discordance_s3_returns_half_when_threshold_is_reached():
    result = discordance_s3(
        differences=[5.0, -2.0],
        relations=["aPb", "bQa"],
        pertinences=[1.0, 1.0],
        weights=[0.6, 0.4],
        preference_thresholds=[3.0, 3.0],
        indifference_thresholds=[1.0, 1.0],
        discordance_thresholds=[10.0, 2.0],
    )

    assert result == pytest.approx(0.5, abs=1e-9)

def test_mean_pertinence_reference_case():
    result = mean_pertinence(
        base_pertinence=1.0,
        alternative_a=0.8,
        alternative_b=0.6,
    )

    assert result == pytest.approx(0.8, abs=1e-9)


def test_performance_difference_positive():
    result = performance_difference(10.0, 6.0)

    assert result == pytest.approx(4.0, abs=1e-9)


def test_performance_difference_negative():
    result = performance_difference(6.0, 10.0)

    assert result == pytest.approx(-4.0, abs=1e-9)