
from scipy.signal import find_peaks
import numpy as np


def returnPeakPositionsAndIntensities(pattern, maxHeightOfPeaks, peakWidthInDataPoints):
    peakIndices = returnPeakIndices(pattern, maxHeightOfPeaks, peakWidthInDataPoints)
    peakIntensities = pattern[peakIndices]

    return(np.array([peakIndices, peakIntensities]))


def returnPeakIndices(intensities, maxHeightOfPeaks=0.01, peakWidthInDataPoints=7):

    peaks, _ = find_peaks(
        intensities,
        height=maxHeightOfPeaks * np.max(intensities),
        distance=peakWidthInDataPoints
    )

    return peaks
