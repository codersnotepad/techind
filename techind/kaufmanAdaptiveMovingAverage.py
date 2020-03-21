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
    # change vs data point `period` in past
    change = np.zeros(len(data))
    # change since last data point
    prev_cur = np.zeros(len(data))
    # sum of last `period` prev_cur values
    volatility = np.zeros(len(data))
    # efficiency ratio
    er = np.zeros(len(data))
    # smoothing constant
    sc = np.zeros(len(data))
    # kama
    kama = np.zeros(len(data))

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
            volatility[i] = np.nan
            er[i] = np.nan
            sc[i] = np.nan
            # --- first kama value is the sma
            kama[i] = sum(data[i : i + period]) / period

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
