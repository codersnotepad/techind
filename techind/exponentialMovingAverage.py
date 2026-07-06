import numpy as np
import numpy.typing as npt
from techind.helper import get_valid_data_range as get_valid_data_range


def exponentialMovingAverage(period: int, data: npt.NDArray[np.float64 | np.integer]) -> npt.NDArray[np.float64 | np.integer]:
    """
    Calculate the exponential moving average (EMA) of a given data array.

    Parameters:
    ----------
    period : int
        The number of periods to use for the moving average. Single integer value.
    data : NDArray[np.float64 | np.integer]
        The input data array for which the exponential moving average is to be calculated. Single-dimensional array.

    Returns:
    -------
    NDArray[np.float64 | np.integer]
        An array containing the exponential moving average of the input data. Single-dimensional array of the same length as the input data, with NaN values for indices where the moving average cannot be computed due to insufficient data points.

    Notes:
    -----
    - The exponential moving average is a type of moving average that places a greater weight and significance on the most recent data points. It reacts more significantly to recent price changes than a simple moving average (SMA), which applies an equal weight to all observations in the period.
    """
    # --- If the data contains nan values then this function will fail. So we need to find the first and last non nan values in the data array.
    firstNonNan: int | None
    lastNonNan: int | None
    firstNonNan, lastNonNan = get_valid_data_range(data)

    # --- we cooked if either is still None after the above.
    if firstNonNan is None or lastNonNan is None:
        return np.full(len(data), np.nan)

    # --- define variables
    # the first simple moving average
    sma = data[firstNonNan:period+firstNonNan].sum()/period
    m = 2/(period+1)                                      # weighting factor

    # --- define output array
    out = np.zeros(len(data))

    # --- calculate EMA
    for i in range(len(data)):
        # --- where data item is the p'th item, use the SMA
        if i < firstNonNan:
            out[i] = np.nan
        elif i > lastNonNan:
            out[i] = np.nan
        elif i == period-1+firstNonNan:
            out[i] = sma
        elif i > period-1+firstNonNan:
            # --- the EMA calculation
            out[i] = ((data[i] - out[i-1]) * m) + out[i-1]
            # --- mathematically equivalent
            #    out[i] = m * data[i] + (1-m) * out[i-1]
        elif i < period-1+firstNonNan:
            out[i] = np.nan

    return out
