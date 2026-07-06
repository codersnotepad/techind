import numpy as np
import numpy.typing as npt
from techind.helper import get_valid_data_range as get_valid_data_range


def trippleExponentialMovingAverage(period: int, data: npt.NDArray[np.float64 | np.integer]) -> npt.NDArray[np.float64 | np.integer]:
    """
    Calculate the tripple exponential moving average (TEMA) of a given data array.

    Parameters:
    ----------
    period : int
        The number of periods to use for the moving average. Single integer value.
    data : NDArray[np.float64 | np.integer]
        The input data array for which the tripple exponential moving average is to be calculated. Single-dimensional array.

    Returns:
    -------
    NDArray[np.float64 | np.integer]
        An array containing the tripple exponential moving average of the input data. Single-dimensional array of the same length as the input data, with NaN values for indices where the moving average cannot be computed due to insufficient data points.

    Notes:
    -----
    - The triple exponential moving average is a modified moving average designed to smooth large price fluctuations. This makes it easier to identify trends without the lag associated with traditional moving averages. It does this by taking multiple exponential moving averages (EMA) of the original EMA and subtracting out some of the lag.
    """
    # --- If the data contains nan values then this function will fail. So we need to find the first and last non nan values in the data array.
    firstNonNan: int | None
    lastNonNan: int | None
    firstNonNan, lastNonNan = get_valid_data_range(data)

    # --- we cooked if either is still None after the above.
    if firstNonNan is None or lastNonNan is None:
        return np.full(len(data), np.nan)

    s = (
        data[firstNonNan: period + firstNonNan].sum() / period
    )  # the first simple moving average
    k = 2 / (period + 1)  # weighting factor
    d = (2 * period) - 1  # start of the DEMA

    out = np.zeros(len(data))
    out_ee = np.zeros(len(data))
    out_eee = np.zeros(len(data))
    out_d = np.zeros(len(data))

    for i in range(len(data)):

        if i < firstNonNan + period - 1:
            out[i] = np.nan
            out_ee[i] = np.nan
            out_eee[i] = np.nan
            out_d[i] = np.nan

        elif i > lastNonNan:
            out[i] = np.nan
            out_ee[i] = np.nan
            out_eee[i] = np.nan
            out_d[i] = np.nan

        # --- where data item is the p'th item use the SMA
        if i == period - 1 + firstNonNan:
            out[i] = s
            out_ee[i] = s
            out_eee[i] = s
            out_d[i] = s

        elif i > period - 1 + firstNonNan:
            # --- calculate EMA
            out[i] = (k * data[i]) + (1 - k) * out[i - 1]
            # --- calcualte ema of ema
            out_ee[i] = (k * out[i]) + (1 - k) * out_ee[i - 1]
            # --- calcualte ema of ema of ema
            out_eee[i] = (k * out_ee[i]) + (1 - k) * out_eee[i - 1]
            # --- calculate tema
            out_d[i] = 3 * out[i] - 3 * out_ee[i] + out_eee[i]

    return out_d
