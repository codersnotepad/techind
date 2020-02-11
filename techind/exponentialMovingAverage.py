def exponentialMovingAverage(period, data):

    #--- Exponential Moving Average
    # data: array, time series data e.g. daily close prices
    # period: integer, number of periods form time series array to include in calculation

    #--- import libraries
    import numpy as np

    #--- get first non nan index
    for i in range(len(data)):

        if np.isnan(data[i]) == False:

            firstNonNan = i
            break

    #--- get last non nan index
    for i in reversed(range(len(data))):

        if np.isnan(data[i]) == False:

            lastNonNan = i
            break

    #--- define variables
    sma = data[firstNonNan:period+firstNonNan].sum()/period      # the first simple moving average
    m = 2/(period+1)                                      # weighting factor

    #--- define output array
    out = np.zeros(len(data))

    #--- calculate EMA
    for i in range(len(data)):
        #--- where data item is the p'th item, use the SMA
        if i < firstNonNan:
            out[i] = np.nan
        elif i > lastNonNan:
            out[i] = np.nan
        elif i == period-1+firstNonNan:
            out[i] = sma
        elif i > period-1+firstNonNan:
            #--- the EMA calculation
            out[i] = ((data[i] - out[i-1]) * m) + out[i-1]
            #--- mathematically equivalent
            #    out[i] = m * data[i] + (1-m) * out[i-1]
        elif i < period-1+firstNonNan:
            out[i] = np.nan

    return out
