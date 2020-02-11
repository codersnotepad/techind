def weightedMovingAverage(period, data):

    #--- Weighted Moving Average
    # data: array, time series data e.g. daily close prices
    # period: integer, number of periods from time series array to include in calculation

    import numpy as np

    #--- based on period value calculate the 'weighting factor' or denominator
    d = period*(period/2+.5)

    #--- generate weights list
    weights = np.zeros(period)
    for i in range(period):
        weights[i] = (i+1)/d

    #--- calculate WMA
    a = np.zeros(period)
    out = np.zeros(len(data))

    for i in range(len(data)):
        if i < period-1:
            out[i] = np.nan
        else:
            for m in range(period):
                a[(period-1)-m] = data[i-m,]
            out[i] = np.sum(a * weights)

    return out
