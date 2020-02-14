def triangularMovingAverage(period, data):

    # --- Triangular Moving Average
    # data: array, time series data e.g. daily close prices
    # period: integer, number of periods form time series array to include in calculation

    # --- import libraries
    import numpy as np

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

    # --- calculate SMA
    ret = np.nancumsum(data, dtype=float)
    ret[period:] = ret[period:] - ret[:-period]
    ret = ret[period - 1 :] / period

    # --- calculate SMA of SMA
    ret_ss = np.nancumsum(ret, dtype=float)
    ret_ss[period:] = ret_ss[period:] - ret_ss[:-period]
    ret_ss = ret_ss[period - 1 :] / period

    # --- return array of number the same length as the input
    ret = np.append(np.zeros(2 * period - 2) + np.nan, ret_ss)

    # --- update zeros with nan
    for i in range(len(data)):

        if i < firstNonNan + (period * 2):

            np.put(ret, i, np.nan)

        elif i >= lastNonNan:

            np.put(ret, i, np.nan)

    return ret
