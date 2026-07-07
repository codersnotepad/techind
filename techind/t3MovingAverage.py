# References
# https://www.tradingview.com/script/UI3EYBCr/

import numpy as np
from techind.exponentialMovingAverage import (
    exponentialMovingAverage as exponentialMovingAverage,
)


def t3MovingAverage(period: int, volumeFactor: float, data: np.ndarray) -> int:
    """
    Calculate the triple exponential moving average (T3) of a given data array.

    Parameters:
    ----------
    period : int
        The number of periods to use for the moving average. Single integer value.
    volumeFactor : float
        The volume factor to adjust the sensitivity of the moving average between 0 and 1. Single float value.
    data : NDArray[np.float64 | np.integer]
        The input data array for which the triple exponential moving average is to be calculated. Single-dimensional array.

    Returns:
    -------
    NDArray[np.float64 | np.integer]
        An array containing the triple exponential moving average of the input data. Single-dimensional array of the same length as the input data, with NaN values for indices where the moving average cannot be computed due to insufficient data points.

    Notes:
    -----
    - This analysis indicator applies triple exponential smoothing to filter out market noise while reacting faster than traditional moving averages.
    - Developed by Tim Tillson, T3 recursively applies a Generalized Double Exponential Moving Average (GDEMA) three times. It also incorporates a Volume Factor (often set between 0 and 1) that fine-tunes the indicator's responsiveness.
    """
    # calculate EMA's
    e1: np.ndarray = exponentialMovingAverage(period, data)
    e2: np.ndarray = exponentialMovingAverage(period, e1)
    e3: np.ndarray = exponentialMovingAverage(period, e2)
    e4: np.ndarray = exponentialMovingAverage(period, e3)
    e5: np.ndarray = exponentialMovingAverage(period, e4)
    e6: np.ndarray = exponentialMovingAverage(period, e5)

    # calculate the c's
    c1 = volumeFactor**3
    c2 = 3 * volumeFactor**2 + 3 * volumeFactor**3
    c3 = 6 * volumeFactor**2 - 3 * volumeFactor - 3 * volumeFactor**3
    c4 = 1 + 3 * volumeFactor + volumeFactor**3 + 3 * volumeFactor**2

    return c1 * e6 + c2 * e5 + c3 * e4 + c4 * e3
