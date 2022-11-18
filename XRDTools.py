
import math

import numpy as np
from scipy.signal import find_peaks


def get_two_theta(dSpacings, Wavelength):
    TwoTheta = np.zeros(len(dSpacings))

    i = 0

    for dSpacing  in dSpacings:
        TwoTheta[i] = np.rad2deg( 2 * math.asin( Wavelength / ( 2 * dSpacing )))
        i += 1

    return TwoTheta


def get_dspacing(AngularValues, Wavelength):
    DSpacingList = np.zeros(len(AngularValues))

    i = 0

    for angularValue in AngularValues:
        DSpacingList[i] = Wavelength / (2 * math.sin( np.deg2rad( angularValue / 2 ) ))
        i += 1

    return DSpacingList


def get_non_zero_indices(data):
    res = []

    for i, datum in enumerate(data):
        if datum != 0:
            res.append(i)

    return res


def cleanup_convert_dIs(dIs, Wavelength):

    ValidIndices = get_non_zero_indices(dIs[:,1])
    Intensities = dIs[(ValidIndices), 1]
    DSpacing = dIs[(ValidIndices), 0]
    TwoTheta = get_two_theta(DSpacing, Wavelength)

    return ([TwoTheta, Intensities])


def get_peak_details(TwoThetaValues, intensities, maxHeightOfPeaks, peakWidthInDataPoints):

    peaks, properties = get_peak_indices(intensities, maxHeightOfPeaks=0.01, peakWidthInDataPoints=7)

    TwoThetaStart = TwoThetaValues[0]
    TwoThetaStep = TwoThetaValues[1] - TwoThetaValues[0]
    peakPositionsInTwoTheta = TwoThetaStart + TwoThetaStep * (properties["widths"]/2 + properties["left_ips"])
    peakIntensities = properties["widths"] * properties["width_heights"]
    peakWidthsInTwoTheta = TwoThetaStep * properties["widths"]

    return([peakPositionsInTwoTheta, peakIntensities, peakWidthsInTwoTheta])


def get_peak_indices(intensities, maxHeightOfPeaks=0.01, peakWidthInDataPoints=7):

    peaks, properties = find_peaks(
        intensities,
        height=maxHeightOfPeaks * np.max(intensities),
        distance=peakWidthInDataPoints,
        width=3,
        prominence=1
    )

    return peaks, properties
