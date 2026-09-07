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

def mean_pertinence(base_pertinence, alternative_a, alternative_b):
    """
    Calculate the mean pertinence used in a pairwise comparison.
    """
    return float(
        (base_pertinence + alternative_a + alternative_b) / 3
    )


def performance_difference(a, b):
    """
    Calculate the performance difference between two alternatives.
    """
    return a - b

def build_pairwise_vectors(
    performance_a,
    performance_b,
    base_pertinences,
    pertinences_a,
    pertinences_b,
    preference_thresholds,
    indifference_thresholds,
):
    """
    Build the THOR2 pairwise comparison vectors for two alternatives.

    Returns
    -------
    tuple
        relations_ab,
        differences_ab,
        pertinences_ab,
        relations_ba,
        differences_ba,
        pertinences_ba
    """

    relations_ab = []
    differences_ab = []
    pertinences_ab = []

    relations_ba = []
    differences_ba = []
    pertinences_ba = []

    for i in range(len(performance_a)):
        relations_ab.append(
            preference_relation(
                performance_a[i],
                performance_b[i],
                preference_thresholds[i],
                indifference_thresholds[i],
            )
        )

        differences_ab.append(
            performance_difference(
                performance_a[i],
                performance_b[i],
            )
        )

        pertinences_ab.append(
            mean_pertinence(
                base_pertinences[i],
                pertinences_a[i],
                pertinences_b[i],
            )
        )

        relations_ba.append(
            preference_relation(
                performance_b[i],
                performance_a[i],
                preference_thresholds[i],
                indifference_thresholds[i],
            )
        )

        differences_ba.append(
            performance_difference(
                performance_b[i],
                performance_a[i],
            )
        )

        pertinences_ba.append(
            mean_pertinence(
                base_pertinences[i],
                pertinences_b[i],
                pertinences_a[i],
            )
        )

    return (
        relations_ab,
        differences_ab,
        pertinences_ab,
        relations_ba,
        differences_ba,
        pertinences_ba,
    )

def evaluate_pair(
    relations_ab,
    differences_ab,
    pertinences_ab,
    relations_ba,
    differences_ba,
    pertinences_ba,
    weights,
    preference_thresholds,
    indifference_thresholds,
    discordance_thresholds,
    scenario,
):
    """
    Avalia um par de alternativas segundo um dos cenários THOR2.

    Retorna os valores de dominância de A sobre B e de B sobre A,
    preservando a lógica da implementação original.
    """

    scenario_functions = {
        "s1": scenario_s1,
        "s2": scenario_s2,
        "s3": scenario_s3,
    }

    discordance_functions = {
        "s1": discordance_s1,
        "s2": discordance_s2,
        "s3": discordance_s3,
    }

    if scenario not in scenario_functions:
        raise ValueError(
            "Scenario must be 's1', 's2' or 's3'."
        )

    scenario_function = scenario_functions[scenario]
    discordance_function = discordance_functions[scenario]

    dominates_ab = scenario_function(
        relations_ab,
        differences_ab,
        pertinences_ab,
        weights,
        preference_thresholds,
        indifference_thresholds,
    )

    dominates_ba = scenario_function(
        relations_ba,
        differences_ba,
        pertinences_ba,
        weights,
        preference_thresholds,
        indifference_thresholds,
    )

    if (
        dominates_ab == "dominates"
        and dominates_ba == "dominates"
    ):
        discordance_ab = discordance_function(
            differences_ab,
            relations_ab,
            pertinences_ab,
            weights,
            preference_thresholds,
            indifference_thresholds,
            discordance_thresholds,
        )

        # Mantém o curto-circuito da implementação original.
        if discordance_ab == 0.5:
            return 0.5, 0.5

        discordance_ba = discordance_function(
            differences_ba,
            relations_ba,
            pertinences_ba,
            weights,
            preference_thresholds,
            indifference_thresholds,
            discordance_thresholds,
        )

        if discordance_ba == 0.5:
            return 0.5, 0.5

        return (
            round(discordance_ab, 3),
            round(discordance_ba, 3),
        )

    if (
        dominates_ab == "dominates"
        and dominates_ba != "dominates"
    ):
        discordance_ab = discordance_function(
            differences_ab,
            relations_ab,
            pertinences_ab,
            weights,
            preference_thresholds,
            indifference_thresholds,
            discordance_thresholds,
        )

        if discordance_ab != 0.5:
            return round(discordance_ab, 3), 0

        return 0.5, 0.5

    if (
        dominates_ab != "dominates"
        and dominates_ba == "dominates"
    ):
        discordance_ba = discordance_function(
            differences_ba,
            relations_ba,
            pertinences_ba,
            weights,
            preference_thresholds,
            indifference_thresholds,
            discordance_thresholds,
        )

        if discordance_ba != 0.5:
            return 0, round(discordance_ba, 3)

        return 0.5, 0.5

    return 0.5, 0.5