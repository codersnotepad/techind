import numpy as np
import numpy.typing as npt
from techind.helper import get_valid_data_range as get_valid_data_range


def triangularMovingAverage(period: int, data: npt.NDArray[np.float64 | np.integer]) -> npt.NDArray[np.float64 | np.integer]:
    """
    Calculate the triangular moving average (TMA) of a given data array.

    Parameters:
    ----------
    period : int
        The number of periods to use for the moving average. Single integer value.
    data : NDArray[np.float64 | np.integer]
        The input data array for which the triangular moving average is to be calculated. Single-dimensional array.

    Returns:
    -------
    NDArray[np.float64 | np.integer]
        An array containing the triangular moving average of the input data. Single-dimensional array of the same length as the input data, with NaN values for indices where the moving average cannot be computed due to insufficient data points.

    Notes:
    -----
    - This analysis indicator smooths out price data by averaging the data twice (averaging the average). It places greater weight on the central portion of the selected time period, which helps eliminate market noise and highlights overall trend direction.
    """
    # --- If the data contains nan values then this function will fail. So we need to find the first and last non nan values in the data array.
    firstNonNan: int | None
    lastNonNan: int | None
    firstNonNan, lastNonNan = get_valid_data_range(data)

    # --- we cooked if either is still None after the above.
    if firstNonNan is None or lastNonNan is None:
        return np.full(len(data), np.nan)

    # --- calculate SMA
    ret = np.nancumsum(data, dtype=float)
    ret[period:] = ret[period:] - ret[:-period]
    ret = ret[period - 1:] / period

    # --- calculate SMA of SMA
    ret_ss = np.nancumsum(ret, dtype=float)
    ret_ss[period:] = ret_ss[period:] - ret_ss[:-period]
    ret_ss = ret_ss[period - 1:] / period

    # --- return array of number the same length as the input
    ret = np.append(np.zeros(2 * period - 2) + np.nan, ret_ss)

    # --- update zeros with nan
    for i in range(len(data)):

        if i < firstNonNan + (period * 2):

            np.put(ret, i, np.nan)

        elif i >= lastNonNan:

            np.put(ret, i, np.nan)

    return ret
