# -*- coding: utf-8 -*-

import os
import Functions as funcs


#Take the annual rasters and give output of statistical time series trends
inFol = '.../AnnualRas/'
outFol = '/OutStats/'

inArrays = funcs.tiffToarray(inFol)
outTuple = funcs.linReg(inArrays)

# Use the first raster as a blueprint, to recreate GEoTiffs from arrays later on
for allRasters in os.listdir(inFol):
        if allRasters[-3:] == "tif":
            firstRasStr = inFol + allRasters
            break

outNames = ("An_slope.tif", "An_intcp.tif", "An_rval.tif", "An_pval.tif", "An_stderr.tif",
            "An_mkP.tif")

for fname, i in zip(outNames, range(len(outNames))):
    funcs.array_to_raster(firstRasStr,outTuple[i],outFol+fname)


#Take monthly rasters from respective folders and give output of statistical time series trends
#Rasters MUST be in their own folders within inFol2 grouped by their month
#Does nothing if all rasters are within one folder

monthNum = ['01', '02', '03', '04', '05', '06', 
            '07', '08', '09', '10', '11', '12']
            
inFol2 = '.../inFol/'

for foldr in os.listdir(inFol2):
    if os.path.isdir(inFol2+foldr):
        inFol = inFol2 + foldr + "/"

        # convert all rasters in the subfolder to arrays, use arrays for linear regression      
        inArrays = funcs.tiffToarray(inFol)
        outTuple = funcs.linReg(inArrays)
        
        for allRasters in os.listdir(inFol):
                if allRasters[-3:] == "tif":
                    firstRasStr = inFol + allRasters
                    break
        
        iName = inFol[-7:-5]
        outNames = (iName + "_slope.tif",iName +  "_intcp.tif",iName +  "_rval.tif", 
                    iName + "_pval.tif",iName +  "_stderr.tif", iName +  "_mkP.tif")
        
        for fname, i in zip(outNames, range(len(outNames))):
            funcs.array_to_raster(firstRasStr,outTuple[i],outFol+fname)
          
            
            
















'''
inFol = "D:/Test/NDVI_SPOT_MONGOLIA/Test/"
inFile = inFol + "NDVI_19990103__Extract.tif"

#Start and End Year


dataset = gdal.Open(inFol + "NDVI_19990103__Extract.tif", GA_ReadOnly)
dataset2 = gdal.Open(inFol + "NDVI_19990113__Extract.tif", GA_ReadOnly)
dataset3 = gdal.Open(inFol + "NDVI_19990124__Extract.tif", GA_ReadOnly)

cols = dataset.RasterXSize
rows = dataset.RasterYSize
bands = dataset.RasterCount


data = dataset.ReadAsArray(0, 0, cols, rows)
data2 = dataset2.ReadAsArray(0, 0, cols, rows)
data3 = dataset3.ReadAsArray(0, 0, cols, rows)
'''


#Collection

#create a random integer array
#c = np.random.randint(50, size=12).reshape(3,4)
#stack = np.dstack((a,b,c))


#use the larger value of 2 arrays in a new array, if both are the same,
#use the value from a (else result would be 0)
#condlist = [a>b, b>a]
#choicelist = [a, b]
#np.select(condlist, choicelist,a)

#monthName = ["Jan", "Feb","Mar","Apr","May","Jun","Jul","Aug", "Sep", "Oct", "Nov", "Dec"]

