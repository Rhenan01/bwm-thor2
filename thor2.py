"""Core computational functions for the THOR2 method."""


def preference_relation(a, b, preference_threshold, indifference_threshold):
    """
    Determine the preference relation between two alternative performances.

    Parameters
    ----------
    a : float
        Performance of alternative a.
    b : float
        Performance of alternative b.
    preference_threshold : float
        Preference threshold p.
    indifference_threshold : float
        Indifference threshold q.

    Returns
    -------
    str
        One of the THOR2 preference relations:
        aPb, aQb, aIb, bIa, bQa or bPa.
    """

    difference = a - b

    if difference > preference_threshold:
        return "aPb"

    if difference > indifference_threshold:
        return "aQb"

    if difference >= 0:
        return "aIb"

    if difference >= -indifference_threshold:
        return "bIa"

    if difference >= -preference_threshold:
        return "bQa"

    return "bPa"