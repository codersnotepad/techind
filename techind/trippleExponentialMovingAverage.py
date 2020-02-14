def trippleExponentialMovingAverage(period, data):

    # --- Tripple Exponential Moving Average
    # data: array, time series data e.g. daily close prices
    # period: integer, number of periods from time series array to include in calculation

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

    s = (
        data[firstNonNan : period + firstNonNan].sum() / period
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
