
import sys

import matplotlib.pyplot as plt
import numpy as np

from background import background
from computeFOM import get_FOM_array
from loadReferencePatterns import loadReferenceData
from XRDTools import cleanup_convert_dIs, get_peak_details


if __name__ == "__main__":

    # Get some sample data
    DiffractionPattern = np.loadtxt(sys.argv[1], delimiter="\t")

    # Get the reference patterns
    referencePatterns, referenceIDs = loadReferenceData('./data/testdIs')
    print(f"Using {len(referencePatterns)} reference patterns")

    # Set the experimental wavelegth
    Wavelength = 0.17714286
    maxPositionalDifference = 0.1

    Intensities = DiffractionPattern[:,1]
    TwoThetaValues = DiffractionPattern[:,0]
    maxExperimentalIntensity = np.max(Intensities)

    # Determine Background
    BackgroundIntensities = background(
        Intensities,
        TwoThetaValues,
        iterations=20,
        sec_iterations=20,
        curvature=0.0001,
        perc_anchor_pnts=20
    )

    # Determine the background subtracted signal
    BackgroudSubtractedIntensities = Intensities - BackgroundIntensities

    # Get the peak indices from the pattern
    peakDetails = get_peak_details(TwoThetaValues, BackgroudSubtractedIntensities, maxHeightOfPeaks=0.01, peakWidthInDataPoints=7)

    peak2ThetaList = peakDetails[0]
    peakIntensities = peakDetails[1]

    # normalize the peak intensities
    maxPeakIntensity = np.max(peakIntensities)
    peakIntensities = peakIntensities / maxPeakIntensity

    samplePattern = np.array([peak2ThetaList, peakIntensities])

    FOMs = get_FOM_array(
        samplePattern,
        referencePatterns,
        Wavelength,
        maxPositionalDifference=0.05,
        weightingAngle=1,
        weightingIntensity=0.2,
        weightingPhases=0.5
    )
    FOMs[np.isnan(FOMs)] = 0
    sortedFOMIndices = np.flip(np.argsort(FOMs))

    for i in range(9):

        plt.figure(i + 1) # to let the index start at 1

        indexOfBestMatch = sortedFOMIndices[i]
        FOMOfBestMatch = FOMs[indexOfBestMatch]
        patternOfBestMatch = referencePatterns[indexOfBestMatch,:,:]
        IDofBestMatch = referenceIDs[indexOfBestMatch]
        convertedPatternOfBestMatch = cleanup_convert_dIs(patternOfBestMatch, Wavelength)

        plt.xlim([0, 10])
        plt.plot(TwoThetaValues, Intensities)
        plt.plot(TwoThetaValues, BackgroundIntensities)
        plt.plot(TwoThetaValues, BackgroudSubtractedIntensities)
        plt.plot(peak2ThetaList, peakIntensities * maxExperimentalIntensity, "x")
        plt.stem(convertedPatternOfBestMatch[0], (convertedPatternOfBestMatch[1] * maxExperimentalIntensity))

        plt.title(f"ID: {IDofBestMatch} FOM: {FOMOfBestMatch}")
        plt.show(block=True)

    print("Example completed")
