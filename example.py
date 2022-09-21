import matplotlib.pyplot as plt
from background import *
from ReturnPeaks import *
from computeFOM import *
from loadReferencePatterns import *
from XRDTools import *



# Get some sample data

DiffractionPattern = np.loadtxt("Rack4_Sample2_Qz_PDF.xy", delimiter="\t")

# Get the reference patterns
referencePatterns, referenceIDs = loadReferenceData('testdIs')

# Set the experimental wavelegth
Wavelength = 0.17714286
maxPositionalDifference = 0.1

Intensities=DiffractionPattern[:,1]
TwoThetaValues=DiffractionPattern[:,0]

# Determine Background 
BackgroundIntensities = background(Intensities, TwoThetaValues, iterations=50, sec_iterations=50, curvature=0.000001, perc_anchor_pnts=50) 

# Determine the background subtracted signal
BackgroudSubtractedIntensities = Intensities - BackgroundIntensities

# Get the peak indices from the pattern
PeakIndicesAndIntensities = returnPeakPositionsAndIntensities(BackgroudSubtractedIntensities, maxHeightOfPeaks=0.01, peakWidthInDataPoints=7)
peakIndices = PeakIndicesAndIntensities[0,:]
peakIndices =  peakIndices.astype(int)
peak2ThetaList = TwoThetaValues[peakIndices]
peakIntensities = PeakIndicesAndIntensities[1,:]

# normalize the peak intensities
maxPeakIntensity = np.max(peakIntensities)
peakIntensities = peakIntensities / maxPeakIntensity

samplePattern = np.array([peak2ThetaList,peakIntensities])

FOMs = returnFOMArray(samplePattern, referencePatterns, Wavelength, maxPositionalDifference, weightingAngle=0.5, weightingIntensity=0.5, weightingPhases=0.5)
FOMs[np.isnan(FOMs)] = 0
sortedFOMIndices = np.argsort(FOMs)

plt.plot(TwoThetaValues, Intensities)
plt.plot(TwoThetaValues, BackgroundIntensities)
plt.plot(TwoThetaValues, BackgroudSubtractedIntensities)
plt.plot(TwoThetaValues[peakIndices], BackgroudSubtractedIntensities[peakIndices], "x")
plt.show(block=True)