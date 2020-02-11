def simpleMovingAverage(period, data):

    #--- Simple Moving Average
    # data: array, time series data e.g. daily close prices
    # period: integer, number of periods from time series array to include in calculation

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

    #--- calculate SMA
    out = np.nancumsum(data, dtype=float)
    out[period:] = out[period:] - out[:-period]
    out = out[period - 1:] / period

    #--- return array the same length as the input
    out =  np.append(np.zeros(period-1) + np.nan, out)

    #--- update zeros with nan
    for i in range(len(data)):

        if i < firstNonNan+period:

            np.put(out,i,np.nan)

        elif i >= lastNonNan:

            np.put(out,i,np.nan)

    return out
