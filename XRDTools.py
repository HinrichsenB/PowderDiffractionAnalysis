# Some crystallographic tools
import numpy as np
import math


def returnTwoThetaFromDspacingAndWavelength(dSpacings, Wavelength):
    i=0
    for dSpacing  in dSpacings:
        dSpacings[i] = np.rad2deg( 2*math.asin( Wavelength/( 2*dSpacing )))
        i+=1
    return dSpacings

def returnDspacingFromTwoThetaAndWavelength(AngularValues, Wavelength):
    DSpacingList = AngularValues
    i=0
    for angularValue  in AngularValues:
        DSpacingList[i] = Wavelength/(2 * math.sin( np.deg2rad( angularValue/2 ) ))
        i+=1
    return DSpacingList