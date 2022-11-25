
import math

import numpy as np

from XRDTools import get_dspacing


def get_FOM_array(samplePattern, referencePatterns, Wavelength, maxPositionalDifference=0.05, weightingAngle=0.5, weightingIntensity=0.5, weightingPhases=0.5):

    # create an array of maximal positional differences which takes into account wavelength dispersion effects: tan(theta)
    numberOfPeaksInSamplePattern = round(np.size(samplePattern) / 2)
    maxPositionalDifferenceArray = np.ndarray(numberOfPeaksInSamplePattern)
    maxPositionalDifferenceArray[:] = maxPositionalDifference

    peak2ThetaList = samplePattern[0, :]
    peakDSpacingList = get_dspacing(peak2ThetaList, Wavelength)
    peakIntensities = samplePattern[1, :]

    i = 0
    for maxPositionalDifferenceValue in maxPositionalDifferenceArray:
        # maxPositionalDifferenceArray[i] = maxPositionalDifferenceArray[i] / ( ( math.cos( np.deg2rad( peak2ThetaList[i]/2 ))) ** 2 )
        # maxPositionalDifferenceArray[i] = maxPositionalDifferenceArray[i] * (Wavelength/2) * (math.cos( np.deg2rad( peak2ThetaList[i] ) ) )/( math.sin( np.deg2rad( peak2ThetaList[i] ) ) ** 2 )
        maxPositionalDifferenceArray[i] = maxPositionalDifference * peakDSpacingList[i]
        i += 1

    # Build the array for getting FOMs
    sampleDIerrors = np.array([peakDSpacingList, peakIntensities, maxPositionalDifferenceArray ])

    numberOfReferencePatterns = len(referencePatterns)
    FOMs = np.zeros(numberOfReferencePatterns)
    i = 0
    while i < numberOfReferencePatterns - 1:
        FOMs[i] = get_patterns_FOM(sampleDIerrors, referencePatterns[i, :, :])
        i += 1

    return FOMs


def get_patterns_FOM(sampleDIerrors, referenceDIs, weightingAngle=0.5, weightingIntensity=0.5, weightingPhases=0.5):

    numberOfPeaksInReferencePattern = round(np.shape((np.nonzero(referenceDIs)))[1] / 2)
    referenceDIs = referenceDIs[0:numberOfPeaksInReferencePattern, :]
    numberOfPeaksInSamplePattern = np.size(sampleDIerrors, 0)

    # Create an array to hold the individual peak FOMs
    FOM = np.zeros((numberOfPeaksInReferencePattern + numberOfPeaksInSamplePattern, 4))

    # run through all experimental peaks and compute the FOM contribution of each peak
    if numberOfPeaksInReferencePattern > 0:
        i = 0

        while i < numberOfPeaksInSamplePattern - 1:
            positionDifference = np.abs(referenceDIs[:,0] - sampleDIerrors[0,i])
            minDifference = np.argmin(positionDifference)

            if positionDifference[minDifference] < sampleDIerrors[2,i]:
                FOM[i,0:4] = get_peak_FOMs(sampleDIerrors[0:2, i], referenceDIs[minDifference, :])

            i += 1

    maxPositionalDifference = sampleDIerrors.mean(axis=0)[2]
    numberOfAssignedPeaks = np.count_nonzero(FOM, axis=0)[0]

    FOMTheta = 1 - (FOM.sum(axis=0)[0]) / (numberOfAssignedPeaks * maxPositionalDifference)
    FOMIntensity = 1 - (FOM.sum(axis=0)[1]) / numberOfAssignedPeaks
    FOMph = math.sqrt(
        (FOM.sum(axis=0)[2]) * numberOfAssignedPeaks /
        ((sampleDIerrors.sum(axis=0)[1]) * numberOfPeaksInSamplePattern)
    )
    FOMdb = math.sqrt(
        (FOM.sum(axis=0)[3]) * numberOfAssignedPeaks /
        ((referenceDIs.sum(axis=0)[1]) * numberOfPeaksInReferencePattern)
    )
    finalFOM = math.sqrt(
        FOMdb *
        (weightingAngle * FOMTheta + weightingIntensity * FOMIntensity + weightingPhases * FOMph) /
        (weightingAngle + weightingIntensity + weightingPhases)
    )
    return finalFOM


def get_peak_FOMs(sampleDI, referenceDI):
    FOMtheta = abs(sampleDI[0] - referenceDI[0])
    FOMintensity = abs(sampleDI[1] - referenceDI[1])
    return np.array([FOMtheta, FOMintensity, sampleDI[1], referenceDI[1]])
