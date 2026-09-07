"""Best-Worst Method (BWM) computational functions."""

from scipy.optimize import linprog


def solve_bwm(best_index, worst_index, best_to_others, others_to_worst):
    """
    Solve the linear Best-Worst Method (BWM) optimization model.

    Parameters
    ----------
    best_index : int
        Index of the criterion selected as Best.
    worst_index : int
        Index of the criterion selected as Worst.
    best_to_others : list[float]
        Best-to-Others preference vector.
    others_to_worst : list[float]
        Others-to-Worst preference vector.

    Returns
    -------
    weights : numpy.ndarray
        Optimal normalized criteria weights.
    xi : float
        Optimal inconsistency value of the BWM model.

    Raises
    ------
    ValueError
        If the optimization problem cannot be solved.
    """

    n = len(best_to_others)

    # Objective function: minimize xi
    objective = [0] * n + [1]

    inequality_matrix = []
    inequality_bounds = []

    # Best-to-Others constraints
    for j in range(n):
        if j == best_index:
            continue

        positive_constraint = [0] * (n + 1)
        negative_constraint = [0] * (n + 1)

        positive_constraint[best_index] = 1
        positive_constraint[j] = -best_to_others[j]
        positive_constraint[-1] = -1

        inequality_matrix.append(positive_constraint)
        inequality_bounds.append(0)

        negative_constraint[best_index] = -1
        negative_constraint[j] = best_to_others[j]
        negative_constraint[-1] = -1

        inequality_matrix.append(negative_constraint)
        inequality_bounds.append(0)

    # Others-to-Worst constraints
    for j in range(n):
        if j == worst_index:
            continue

        positive_constraint = [0] * (n + 1)
        negative_constraint = [0] * (n + 1)

        positive_constraint[j] = 1
        positive_constraint[worst_index] = -others_to_worst[j]
        positive_constraint[-1] = -1

        inequality_matrix.append(positive_constraint)
        inequality_bounds.append(0)

        negative_constraint[j] = -1
        negative_constraint[worst_index] = others_to_worst[j]
        negative_constraint[-1] = -1

        inequality_matrix.append(negative_constraint)
        inequality_bounds.append(0)

    # Sum of weights must be equal to 1
    equality_matrix = [[1] * n + [0]]
    equality_bounds = [1]

    # All weights and xi must be non-negative
    bounds = [(0, None)] * (n + 1)

    result = linprog(
        c=objective,
        A_ub=inequality_matrix,
        b_ub=inequality_bounds,
        A_eq=equality_matrix,
        b_eq=equality_bounds,
        bounds=bounds,
        method="highs",
    )

    if not result.success:
        raise ValueError(f"BWM optimization failed: {result.message}")

    weights = result.x[:-1]
    xi = result.x[-1]

    return weights, xi