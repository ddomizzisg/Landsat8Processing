############################################################################
#All of the follwing are used to calculate earth-sun distance, adapted from
#ttp://davit.ece.vt.edu/davitpy/_modules/utils/calcSun.html#calcSunRadVector
def calcGeomMeanAnomalySun( t ):
    """ Calculate the Geometric Mean Anomaly of the Sun (in degrees)     """
    M = 357.52911 + t * ( 35999.05029 - 0.0001537 * t)
    return M # in degrees

def calcEccentricityEarthOrbit( t ):
    """ Calculate the eccentricity of earth's orbit (unitless)   """
    e = 0.016708634 - t * ( 0.000042037 + 0.0000001267 * t)
    return e # unitless

def calcSunEqOfCenter( t ):
    """Calculate the equation of center for the sun (in degrees) """
    mrad = np.radians(calcGeomMeanAnomalySun(t))
    sinm = np.sin(mrad)
    sin2m = np.sin(mrad+mrad)
    sin3m = np.sin(mrad+mrad+mrad)
    C = (sinm * (1.914602 - t * (0.004817 + 0.000014 * t)) +
         sin2m * (0.019993 - 0.000101 * t) + sin3m * 0.000289)
    return C # in degrees

def calcSunTrueAnomaly( t ):
    m = calcGeomMeanAnomalySun(t)
    c = calcSunEqOfCenter(t)
    v = m + c
    return v # in degrees

def ES_dist(t):

   #eccent = 0.01672592        # Eccentricity of Earth orbit
   #axsmaj = 1.4957            # Semi-major axis of Earth orbit (km)
   #solyr  = 365.2563855       # Number of days in a solar year

    v = calcSunTrueAnomaly(t)
    e = calcEccentricityEarthOrbit(t)
    R = (1.000001018 * (1. - e * e)) / ( 1. + e * np.cos( np.radians(v) ) )
    return R
############################################################################
