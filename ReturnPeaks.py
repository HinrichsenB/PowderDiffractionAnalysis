
from scipy.signal import find_peaks
import numpy as np

def returnPeakDetails(TwoThetaValues, intensities, maxHeightOfPeaks, peakWidthInDataPoints):
    
    peaks, properties = returnPeakIndices(intensities, maxHeightOfPeaks=0.01, peakWidthInDataPoints=7)
    
    TwoThetaStart = TwoThetaValues[0]
    TwoThetaStep = TwoThetaValues[1] - TwoThetaValues[0]
    peakPositionsInTwoTheta = TwoThetaStart + TwoThetaStep * (properties["widths"]/2 + properties["left_ips"])
    peakIntensities = properties["widths"] * properties["width_heights"]
    peakWidthsInTwoTheta = TwoThetaStep * properties["widths"]
    
    return([peakPositionsInTwoTheta, peakIntensities, peakWidthsInTwoTheta])

def returnPeakIndices(intensities, maxHeightOfPeaks=0.01, peakWidthInDataPoints=7):

    peaks, properties = find_peaks(
        intensities,
        height=maxHeightOfPeaks * np.max(intensities),
        distance=peakWidthInDataPoints,
        width=3,
        prominence=1
    )

    return peaks, properties 
