import numpy as np
import numpy.typing as npt


def weightedMovingAverage(period: int, data: npt.NDArray[np.float64 | np.integer]) -> npt.NDArray[np.float64 | np.integer]:
    """
    Calculate the weighted moving average of a given data array.

    Parameters:
    ----------
    period : int
        The number of periods to use for the moving average. Single integer value.
    data : NDArray[np.float64 | np.integer]
        The input data array for which the weighted moving average is to be calculated. Single-dimensional array.

    Returns:
    -------
    NDArray[np.float64 | np.integer]
        An array containing the weighted moving average of the input data. Single-dimensional array of the same length as the input data, with NaN values for indices where the moving average cannot be computed due to insufficient data points.

    Notes:
    -----
    - The weight moving average puts more weight on recent data points, making it more responsive to changes in the data compared to a simple moving average.
    """

    # --- If ther data contains nan values then this function will fail. So we need to find the first and last non nan values in the data array.
    firstNonNan: int | None = None
    for i in range(len(data)):

        if not np.isnan(data[i]):

            firstNonNan = i
            break
    lastNonNan: int | None = None
    for i in reversed(range(len(data))):

        if not np.isnan(data[i]):

            lastNonNan = i
            break

    # --- we cooked if either is still None after the above.
    if firstNonNan is None or lastNonNan is None:
        return np.full(len(data), np.nan)

    # --- based on period value calculate the 'weighting factor' or denominator
    d: float = period * (period / 2 + 0.5)

    # --- generate weights list
    weights: np.ndarray = np.zeros(period)
    for i in range(period):
        weights[i] = (i + 1) / d

    # --- calculate WMA
    a: np.ndarray = np.zeros(period)
    out: np.ndarray = np.zeros(len(data))

    for i in range(len(data)):

        if i < firstNonNan + period - 1:
            out[i] = np.nan

        elif i > lastNonNan:
            out[i] = np.nan

        else:
            for m in range(period):
                a[(period - 1) - m] = data[
                    i - m,
                ]
            out[i] = np.sum(a * weights)

    return out
