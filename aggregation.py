"""Weight aggregation functions for group decision-making."""

import numpy as np


def aggregate_weights(all_weights):
    """
    Aggregate criteria weights from multiple decision makers.

    The individual weight vectors are aggregated using the geometric
    mean for each criterion and subsequently normalized.

    Parameters
    ----------
    all_weights : list[list[float]]
        Individual criteria-weight vectors, one for each decision maker.

    Returns
    -------
    numpy.ndarray
        Normalized aggregated criteria weights.
    """

    weights_array = np.array(all_weights).T

    geometric_means = (
        np.prod(weights_array, axis=1)
        ** (1 / weights_array.shape[1])
    )

    geometric_means /= np.sum(geometric_means)

    return geometric_means