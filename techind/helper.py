import numpy as np
import numpy.typing as npt


def get_valid_data_range(data: npt.NDArray[np.float64 | np.integer]) -> tuple[int | None, int | None]:
    """
    Find the first and last non-NaN indices in a data array.

    Parameters:
    ----------
    data : NDArray[np.float64 | np.integer]
        The input data array.

    Returns:
    -------
    tuple[int | None, int | None]
        A tuple containing (firstNonNan, lastNonNan) indices, or (None, None) if no valid data exists.
    """
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

    return firstNonNan, lastNonNan
