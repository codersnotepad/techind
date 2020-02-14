def kaufmanAdaptiveMovingAverage(period, fastEMA, slowEMA, data):

    # --- import libraries
    import numpy as np
    import math

    # --- get first non nan index
    for i in range(len(data)):

        if np.isnan(data[i]) == False:

            firstNonNan = i
            break

    # --- get last non nan index
    for i in reversed(range(len(data))):

        if np.isnan(data[i]) == False:

            lastNonNan = i
            break

    # --- define variables
    dataLength = len(data)

    # --- define arrays
    change = np.zeros(dataLength)
    prev_cur = np.zeros(dataLength)
    volatility = np.zeros(dataLength)
    # --- efficiency ratio
    er = np.zeros(dataLength)
    # --- smoothing constant
    sc = np.zeros(dataLength)
    # --- kama
    kama = np.zeros(dataLength)

    # --- calculate efficiency ratio
    for i in range(0, dataLength):

        if i <= firstNonNan:
            prev_cur[i] = np.nan
            change[i] = np.nan
            volatility[i] = np.nan
            er[i] = np.nan
            sc[i] = np.nan
            kama[i] = np.nan

        elif i > lastNonNan:
            prev_cur[i] = np.nan
            change[i] = np.nan
            volatility[i] = np.nan
            er[i] = np.nan
            sc[i] = np.nan
            kama[i] = np.nan

        elif firstNonNan + period - 1 > i > firstNonNan:
            prev_cur[i] = math.sqrt((data[i] - data[i - 1]) ** 2)

            change[i] = np.nan
            volatility[i] = np.nan
            er[i] = np.nan
            sc[i] = np.nan
            kama[i] = np.nan

        elif i == firstNonNan + period - 1:
            prev_cur[i] = math.sqrt((data[i] - data[i - 1]) ** 2)

            change[i] = math.sqrt((data[i - 1] - data[i - period]) ** 2)

            # --- first kama value is the sma
            kama[i] = sum(data[i : i + period]) / period

            volatility[i] = np.nan
            er[i] = np.nan
            sc[i] = np.nan

        elif i > firstNonNan + period - 1:
            prev_cur[i] = math.sqrt((data[i] - data[i - 1]) ** 2)

            change[i] = math.sqrt((data[i] - data[i - period]) ** 2)

            volatility[i] = sum(prev_cur[i - period + 1 : i + 1])

            er[i] = change[i] / volatility[i]

            sc[i] = (
                er[i] * ((2 / (fastEMA + 1)) - (2 / (slowEMA + 1)))
                + (2 / (slowEMA + 1))
            ) ** 2

            kama[i] = kama[i - 1] + sc[i] * (data[i] - kama[i - 1])

    return kama
