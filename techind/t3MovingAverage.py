# References
# https://www.tradingview.com/script/UI3EYBCr/

import numpy as np
from techind.exponentialMovingAverage import (
    exponentialMovingAverage as exponentialMovingAverage,
)


def t3MovingAverage(period: int, volumeFactor: float, data: np.ndarray) -> int:

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
