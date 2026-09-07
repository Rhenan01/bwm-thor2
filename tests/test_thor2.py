from thor2 import preference_relation


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