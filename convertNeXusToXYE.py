
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from XRDTools import returnTwoThetaFromQAndWavelength

from nexusformat.nexus import nxload


if __name__ == "__main__":

    # Loop through all the files in a directory
    p = Path("C:/Temp/ESRF/Downloads/2022Nov15/Streamline/processed_2th/")
    files = list(p.glob( '**/*.h5' ))
    for filename in files:
        DiffractionPattern = nxload(filename)
        Diffractogram = DiffractionPattern.get_default()
        TwoTheta = Diffractogram.nxaxes[0]
        Intensities = DiffractionPattern.results.integrate.diffractogram.data
        Errors =  DiffractionPattern.results.integrate.diffractogram.data_errors
        OutputFileName = str(filename) + ".xye"
        np.savetxt(OutputFileName, np.c_[TwoTheta, Intensities, Errors], delimiter='\t')



 

    print("Conversion completed")
