def mesaAdaptiveMovingAverage(high, low, fastLimit, slowLimit, warmUpPeriod):

    # --- MESA Adaptive Moving Average
    # high: array, time series data e.g. daily close prices
    # low: array, time series data e.g. daily close prices
    # period: integer, number of periods from time series array to include in calculation
    #
    # converted from sources:
    #    https://www.mesasoftware.com/papers/MAMA.pdf
    #    https://www.quantconnect.com/forum/discussion/942/john-ehlers-mama-and-frama-indicators/p1
    #    https://www.prorealcode.com/prorealtime-indicators/john-ehlers-mama-the-mother-of-adaptive-moving-average/

    import numpy as np

    data = (high + low) / 2
    s = np.zeros(len(data))  # smooth
    d = np.zeros(len(data))  # detrenders
    p = np.zeros(len(data))  # periods
    sp = np.zeros(len(data))  # smoothed periods
    ph = np.zeros(len(data))  # phases
    q1 = np.zeros(len(data))  # q1
    q2 = np.zeros(len(data))  # q2
    i1 = np.zeros(len(data))  # i1
    i2 = np.zeros(len(data))  # i2
    re = np.zeros(len(data))  # re
    im = np.zeros(len(data))  # im

    MAMA = np.zeros(len(data))  # MAMA out
    FAMA = np.zeros(len(data))  # FAMA out

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

    # --- calculate MAMA and FAMA
    for i in range(len(data)):

        if i < firstNonNan:
            MAMA[i] = np.nan
            FAMA[i] = np.nan

        elif i > lastNonNan:
            MAMA[i] = np.nan
            FAMA[i] = np.nan

        elif i > firstNonNan + 4:

            s[i] = (4 * data[i] + 3 * data[i - 1] + 2 * data[i - 2] + data[i - 3]) / 10
            d[i] = (
                0.0962 * s[i]
                + 0.5769 * s[i - 2]
                - 0.5769 * s[i - 4]
                - 0.0962 * s[i - 6]
            ) * (0.075 * p[i - 1] + 0.54)

            # Compute InPhase and Quadrature components
            q1[i] = (
                0.0962 * d[i]
                + 0.5769 * d[i - 2]
                - 0.5769 * d[i - 4]
                - 0.0962 * d[i - 6]
            ) * (0.075 * p[i - 1] + 0.54)
            i1[i] = d[i - 3]

            # Advance the phase of I1 and Q1 by 90 degrees
            ji = (
                0.0962 * i1[i - i]
                + 0.5769 * i1[i - 2]
                - 0.5769 * i1[i - 4]
                - 0.0962 * i1[i - 6]
            ) * (0.075 * p[i - 1] + 0.54)
            jq = (
                0.0962 * q1[i - i]
                + 0.5769 * q1[i - 2]
                - 0.5769 * q1[i - 4]
                - 0.0962 * q1[i - 6]
            ) * (0.075 * p[i - 1] + 0.54)

            # Phasor addition for 3 bar averaging
            _i2 = i1[i] - jq
            _q2 = q1[i] + ji

            # Smooth the I and Q components before applying the discriminator
            i2[i] = 0.2 * _i2 + 0.8 * i2[i]
            q2[i] = 0.2 * _q2 + 0.8 * q2[i]

            # Homodyne Discriminator
            _re = i2[i] * i2[i - 1] + q2[i] * q2[i - 1]
            _im = i2[i] * q2[i - 1] + q2[i] * i2[i - 1]
            re[i] = 0.2 * _re + 0.8 * re[i - 1]
            im[i] = 0.2 * _im + 0.8 * im[i - 1]

            # set period value
            period = 0
            if _im != 0 and _re != 0:
                period = 360 / np.arctan(_im / _re)
            if period > 1.5 * p[-1]:
                period = 1.5 * p[i - 1]
            if period < 0.67 * p[i - 1]:
                period = 0.67 * p[i - 1]
            if period < 6:
                period = 6
            if period > 50:
                period = 50
            p[i] = 0.2 * period + 0.8 * p[i - 1]
            sp[i] = 33 * p[i - 1] + 0.67 * sp[i - 1]

            if i1[i] != 0:
                ph[i] = np.arctan(q1[i] / i1[i])

            # delta phase
            deltaPhase = ph[i - 1] - ph[i]
            if deltaPhase < 1:
                deltaPhase = 1

            # alpha
            alpha = fastLimit / deltaPhase
            if alpha < slowLimit:
                aplha = slowLimit

            # add to output using EMA formula
            MAMA[i] = alpha * data[i] + (1 - alpha) * MAMA[i - 1]
            FAMA[i] = 0.5 * alpha * MAMA[i] + (1 - 0.5 * alpha) * FAMA[i - 1]

    # remove the MAMA and FAMA warm-up values
    for i in range(warmUpPeriod + 1):

        if i <= warmUpPeriod:

            MAMA[i] = np.nan
            FAMA[i] = np.nan

    return MAMA, FAMA
