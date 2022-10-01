
import matplotlib.pyplot as plt
import numpy as np

from background import background
from ReturnPeaks import returnPeakDetails
from computeFOM import returnFOMArray
from loadReferencePatterns import loadReferenceData
from XRDTools import returnTwoThetaFromDspacingAndWavelength


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
    TwoTheta = returnTwoThetaFromDspacingAndWavelength(DSpacing, Wavelength)

    return ([TwoTheta, Intensities])


if __name__ == "__main__":

    # Get some sample data
    DiffractionPattern = np.loadtxt("./data/Rack4_Sample2_Qz_PDF.xy", delimiter="\t")

    # Get the reference patterns
    referencePatterns, referenceIDs = loadReferenceData('./data/testdIs')

    # Set the experimental wavelegth
    Wavelength = 0.17714286
    maxPositionalDifference = 0.1

    Intensities = DiffractionPattern[:,1]
    TwoThetaValues = DiffractionPattern[:,0]

    # Determine Background
    BackgroundIntensities = background(
        Intensities,
        TwoThetaValues,
        iterations=50,
        sec_iterations=50,
        curvature=0.000001,
        perc_anchor_pnts=25
    )

    # Determine the background subtracted signal
    BackgroudSubtractedIntensities = Intensities - BackgroundIntensities

    # Get the peak indices from the pattern
    peakDetails = returnPeakDetails(TwoThetaValues, BackgroudSubtractedIntensities, maxHeightOfPeaks=0.01, peakWidthInDataPoints=7)

    peak2ThetaList = peakDetails[0] 
    peakIntensities = peakDetails[1]

    # normalize the peak intensities
    maxPeakIntensity = np.max(peakIntensities)
    peakIntensities = peakIntensities / maxPeakIntensity

    samplePattern = np.array([peak2ThetaList,peakIntensities])

    FOMs = returnFOMArray(
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
        
        plt.plot(TwoThetaValues, Intensities)
        plt.xlim([0, 10])
        plt.plot(TwoThetaValues, BackgroundIntensities)
        plt.plot(TwoThetaValues, BackgroudSubtractedIntensities)
        plt.plot(peak2ThetaList, peakIntensities * maxPeakIntensity, "x")
        plt.stem(convertedPatternOfBestMatch[0], (convertedPatternOfBestMatch[1] * maxPeakIntensity))
        Title = str(IDofBestMatch)  + ", FOM: " + str(FOMOfBestMatch)
        plt.title(Title)
        plt.show(block=True)

    print("Example completed")
