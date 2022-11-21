
import math

import numpy as np


def returnTwoThetaFromDspacingAndWavelength(dSpacings, Wavelength):
    TwoTheta = np.zeros(len(dSpacings))

    i = 0

    for dSpacing  in dSpacings:
        TwoTheta[i] = np.rad2deg( 2 * math.asin( Wavelength / ( 2 * dSpacing )))
        i += 1

    return TwoTheta


def returnDspacingFromTwoThetaAndWavelength(AngularValues, Wavelength):
    DSpacingList = np.zeros(len(AngularValues))

    i = 0

    for angularValue  in AngularValues:
        DSpacingList[i] = Wavelength / (2 * math.sin( np.deg2rad( angularValue / 2 ) ))
        i += 1

    return DSpacingList

def returnTwoThetaFromQAndWavelength(QVector, Wavelength):
    TwoTheta = np.zeros(len(QVector))

    i = 0

    for QValue  in QVector:
        TwoTheta[i] = np.rad2deg ( 2 * math.asin( Wavelength * QValue * 0.1 / ( 4 * math.pi )  ))
        i += 1

    return TwoTheta