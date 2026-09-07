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

def scenario_s1(
    relations,
    differences,
    pertinences,
    weights,
    preference_thresholds,
    indifference_thresholds,
):
    """
    Evaluate dominance according to THOR2 scenario S1.

    Parameters
    ----------
    relations : list[str]
        Preference relations for each criterion.
    differences : list[float]
        Performance differences between alternatives.
    pertinences : list[float]
        Pertinence values associated with the comparison.
    weights : list[float]
        Criteria weights.
    preference_thresholds : list[float]
        Preference thresholds p.
    indifference_thresholds : list[float]
        Indifference thresholds q.

    Returns
    -------
    str
        "dominates" or "does not dominate".
    """

    support = 0.0
    opposition = 0.0

    for i in range(len(weights)):
        relation = relations[i]

        if relation == "aPb":
            support += weights[i] * pertinences[i]

        elif relation == "aQb":
            opposition += abs(
                weights[i]
                * pertinences[i]
                * (
                    (
                        (abs(differences[i]) - indifference_thresholds[i])
                        / (
                            preference_thresholds[i]
                            - indifference_thresholds[i]
                        )
                    )
                    * 0.5
                    + 0.5
                )
            )

        elif relation in ("aIb", "bIa"):
            opposition += weights[i] * 0.5 * pertinences[i]

        elif relation == "bQa":
            opposition += abs(
                weights[i]
                * pertinences[i]
                * (
                    (
                        (abs(differences[i]) - indifference_thresholds[i])
                        / (
                            preference_thresholds[i]
                            - indifference_thresholds[i]
                        )
                    )
                    * 0.5
                    + 0.5
                )
            )

        elif relation == "bPa":
            opposition += weights[i] * pertinences[i]

    if support > opposition:
        return "dominates"

    return "does not dominate"


def scenario_s2(
    relations,
    differences,
    pertinences,
    weights,
    preference_thresholds,
    indifference_thresholds,
):
    """
    Evaluate dominance according to THOR2 scenario S2.
    """

    support = 0.0
    opposition = 0.0

    for i in range(len(weights)):
        relation = relations[i]

        if relation == "aPb":
            support += weights[i] * pertinences[i]

        elif relation == "aQb":
            support += abs(
                weights[i]
                * pertinences[i]
                * (
                    (
                        (abs(differences[i]) - indifference_thresholds[i])
                        / (
                            preference_thresholds[i]
                            - indifference_thresholds[i]
                        )
                    )
                    * 0.5
                    + 0.5
                )
            )

        elif relation in ("aIb", "bIa"):
            opposition += weights[i] * 0.5 * pertinences[i]

        elif relation == "bQa":
            opposition += abs(
                weights[i]
                * pertinences[i]
                * (
                    (
                        (abs(differences[i]) - indifference_thresholds[i])
                        / (
                            preference_thresholds[i]
                            - indifference_thresholds[i]
                        )
                    )
                    * 0.5
                    + 0.5
                )
            )

        elif relation == "bPa":
            opposition += weights[i] * pertinences[i]

    if support > opposition:
        return "dominates"

    return "does not dominate"


def scenario_s3(
    relations,
    differences,
    pertinences,
    weights,
    preference_thresholds,
    indifference_thresholds,
):
    """
    Evaluate dominance according to THOR2 scenario S3.
    """

    support = 0.0
    opposition = 0.0

    for i in range(len(weights)):
        relation = relations[i]

        if relation == "aPb":
            support += weights[i] * pertinences[i]

        elif relation == "aQb":
            support += abs(
                weights[i]
                * pertinences[i]
                * (
                    (
                        (abs(differences[i]) - indifference_thresholds[i])
                        / (
                            preference_thresholds[i]
                            - indifference_thresholds[i]
                        )
                    )
                    * 0.5
                    + 0.5
                )
            )

        elif relation in ("aIb", "bIa"):
            support += weights[i] * 0.5 * pertinences[i]

        elif relation == "bQa":
            opposition += abs(
                weights[i]
                * pertinences[i]
                * (
                    (
                        (abs(differences[i]) - indifference_thresholds[i])
                        / (
                            preference_thresholds[i]
                            - indifference_thresholds[i]
                        )
                    )
                    * 0.5
                    + 0.5
                )
            )

        elif relation == "bPa":
            opposition += weights[i] * pertinences[i]

    if support > opposition:
        return "dominates"

    return "does not dominate"

def discordance_s1(
    differences,
    relations,
    pertinences,
    weights,
    preference_thresholds,
    indifference_thresholds,
    discordance_thresholds,
):
    """
    Calculate the THOR2 discordance evaluation for scenario S1.
    """

    support = 0.0
    opposition = 0.0
    discordance_detected = False

    for i in range(len(weights)):
        if weights[i] == 0:
            continue

        relation = relations[i]

        if relation == "aPb":
            support += weights[i] * pertinences[i]

        elif relation == "aQb":
            opposition += abs(
                weights[i]
                * pertinences[i]
                * (
                    (
                        (
                            abs(differences[i])
                            - indifference_thresholds[i]
                        )
                        / (
                            preference_thresholds[i]
                            - indifference_thresholds[i]
                        )
                    )
                    * 0.5
                    + 0.5
                )
            )

        elif relation == "aIb":
            opposition += weights[i] * 0.5 * pertinences[i]

        elif relation == "bIa":
            opposition += weights[i] * 0.5 * pertinences[i]

            if abs(differences[i]) >= discordance_thresholds[i]:
                discordance_detected = True

        elif relation == "bQa":
            opposition += abs(
                weights[i]
                * pertinences[i]
                * (
                    (
                        (
                            abs(differences[i])
                            - indifference_thresholds[i]
                        )
                        / (
                            preference_thresholds[i]
                            - indifference_thresholds[i]
                        )
                    )
                    * 0.5
                    + 0.5
                )
            )

            if abs(differences[i]) >= discordance_thresholds[i]:
                discordance_detected = True

        elif relation == "bPa":
            opposition += weights[i] * pertinences[i]

            if abs(differences[i]) >= discordance_thresholds[i]:
                discordance_detected = True

    if discordance_detected:
        return 0.5

    return support / (opposition + support)


def discordance_s2(
    differences,
    relations,
    pertinences,
    weights,
    preference_thresholds,
    indifference_thresholds,
    discordance_thresholds,
):
    """
    Calculate the THOR2 discordance evaluation for scenario S2.
    """

    support = 0.0
    opposition = 0.0
    discordance_detected = False

    for i in range(len(weights)):
        if weights[i] == 0:
            continue

        relation = relations[i]

        if relation == "aPb":
            support += weights[i] * pertinences[i]

        elif relation == "aQb":
            support += abs(
                weights[i]
                * pertinences[i]
                * (
                    (
                        (
                            abs(differences[i])
                            - indifference_thresholds[i]
                        )
                        / (
                            preference_thresholds[i]
                            - indifference_thresholds[i]
                        )
                    )
                    * 0.5
                    + 0.5
                )
            )

        elif relation == "aIb":
            opposition += weights[i] * 0.5 * pertinences[i]

        elif relation == "bIa":
            opposition += weights[i] * 0.5 * pertinences[i]

            if abs(differences[i]) >= discordance_thresholds[i]:
                discordance_detected = True

        elif relation == "bQa":
            opposition += abs(
                weights[i]
                * pertinences[i]
                * (
                    (
                        (
                            abs(differences[i])
                            - indifference_thresholds[i]
                        )
                        / (
                            preference_thresholds[i]
                            - indifference_thresholds[i]
                        )
                    )
                    * 0.5
                    + 0.5
                )
            )

            if abs(differences[i]) >= discordance_thresholds[i]:
                discordance_detected = True

        elif relation == "bPa":
            opposition += weights[i] * pertinences[i]

            if abs(differences[i]) >= discordance_thresholds[i]:
                discordance_detected = True

    if discordance_detected:
        return 0.5

    return support / (opposition + support)


def discordance_s3(
    differences,
    relations,
    pertinences,
    weights,
    preference_thresholds,
    indifference_thresholds,
    discordance_thresholds,
):
    """
    Calculate the THOR2 discordance evaluation for scenario S3.
    """

    support = 0.0
    opposition = 0.0
    discordance_detected = False

    for i in range(len(weights)):
        if weights[i] == 0:
            continue

        relation = relations[i]

        if relation == "aPb":
            support += weights[i] * pertinences[i]

        elif relation == "aQb":
            support += abs(
                weights[i]
                * pertinences[i]
                * (
                    (
                        (
                            abs(differences[i])
                            - indifference_thresholds[i]
                        )
                        / (
                            preference_thresholds[i]
                            - indifference_thresholds[i]
                        )
                    )
                    * 0.5
                    + 0.5
                )
            )

        elif relation == "aIb":
            support += weights[i] * 0.5 * pertinences[i]

        elif relation == "bIa":
            support += weights[i] * 0.5 * pertinences[i]

            if abs(differences[i]) >= discordance_thresholds[i]:
                discordance_detected = True

        elif relation == "bQa":
            opposition += abs(
                weights[i]
                * pertinences[i]
                * (
                    (
                        (
                            abs(differences[i])
                            - indifference_thresholds[i]
                        )
                        / (
                            preference_thresholds[i]
                            - indifference_thresholds[i]
                        )
                    )
                    * 0.5
                    + 0.5
                )
            )

            if abs(differences[i]) >= discordance_thresholds[i]:
                discordance_detected = True

        elif relation == "bPa":
            opposition += weights[i] * pertinences[i]

            if abs(differences[i]) >= discordance_thresholds[i]:
                discordance_detected = True

    if discordance_detected:
        return 0.5

    return support / (opposition + support)