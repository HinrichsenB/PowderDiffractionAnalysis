import os
import numpy as np

def loadReferenceData(path_of_the_directory='dIs'):

    numberOfFiles = len(os.listdir(path_of_the_directory))
    referencePatterns = np.zeros((numberOfFiles,1000,2))
    patternID = []
    i=0
    for filename in os.listdir(path_of_the_directory):
        f = os.path.join(path_of_the_directory,filename)
        if os.path.isfile(f):
            pattern = np.loadtxt(f, max_rows=1000)
            if len(pattern) > 2:
                intensities = pattern[:,1]
                maxIntensity = np.max(intensities)
                pattern[:,1] = intensities/maxIntensity
                referencePatterns[i,0:len(pattern),:] = pattern
                patternID.append(filename)
            i+=1
    return referencePatterns, patternID