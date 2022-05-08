# Define functions for spectral indices
def NDVI(R,NIR):
    #LS8 = B4,B5    LS57 = B3,B4
    ndvi = (NIR - R) / (NIR + R)
    ndvi = ndvi.astype(np.float32)
    return ndvi

def EVI(B,R,NIR,L=1):
    #LS8 = B2,B4,B5    LS57 = B1,B3,B4
    evi = (NIR - R) / (NIR + 6*R - 7.5 * B + L)
    evi = evi.astype(np.float32)
    return evi

def SAVI(R,NIR,L=0.5):
    #LS8 = B4,B5    LS57 = B3,B4
    savi = ((NIR-R) / (NIR + R + L)) * (1+L)
    savi = savi.astype(np.float32)
    return savi

def MSAVI(R,NIR):
    #LS8 = B4,B5    LS57 = B3,B4
    msavi = (2 * NIR + 1 - np.sqrt((2*NIR+1)**2 - 8 * (NIR - R))) / 2
    msavi = msavi.astype(np.float32)
    return msavi

def NDMI(NIR,SWIR):
    #LS8 = B5,B6    LS57 = B4,B5
    ndmi = (NIR-SWIR) / (NIR+SWIR)
    ndmi = ndmi.astype(np.float32)
    return ndmi

def NBR(NIR,SWIR):
    #LS8 = B5,B7    LS57 = B4,B7
    nbr = (NIR - SWIR) / (NIR+SWIR)
    nbr = nbr.astype(np.float32)
    return nbr

def NBR2(SWIR1,SWIR2):
    #LS8 = B6,B7      LS57 = B5,B7
    nbr2 = (SWIR1 - SWIR2) / (SWIR1 + SWIR2)
    nbr2 = nbr2.astype(np.float32)
    return nbr2

def NDSI(G,SWIR):
    #LS8 = B3,B6      LS57 = B2,B5
    ndsi = (G-SWIR) / (G+SWIR)
    ndsi  = ndsi.astype(np.float32)
    return ndsi

############################################################################
