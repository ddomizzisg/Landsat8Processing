# -*- coding: utf-8 -*-

#create GeoTiffs from nc file

# Change inFol and inFile
# Further below from line 45 change definitions of input nc File
# Naming is a continuously enumeration of the files

import os

from netCDF4 import Dataset
import Functions as funcs

inFol = '.../Original/'
inFile = "Sunshine_Europe_MonthlyMean_1990-2005.nc"

#create an output folder in the same the input file is in
outFol = '.../Sunshine_Tiffs/'

ncFile = inFol+inFile
rootgrp = Dataset(ncFile, 'r')

numVars = len(rootgrp.variables) #Number of variables in ncFile

#Extract name of variables and write in in a list
varList = []
for key in rootgrp.variables.keys():
    varList.append(key)
    
#Extract name of dimensions and write in in a list
dimList = []
for key in rootgrp.dimensions.keys():
    dimList.append(key)


#Get a list of only variables and no dimensions
varListnoDim = []
for var in varList:
    if var not in  dimList:
        varListnoDim.append(var)

#Define needed input variables
xdim = len(rootgrp.dimensions[dimList[0]]) #if first dimension entry is lon
ydim = len(rootgrp.dimensions[dimList[1]]) #if second dimension entry is lat
pixSize = 0.125
x_min = -27.0625 #top left corner of pixel, often x-min from dl site minus pixSize/2
y_max = 73.625 #top left corner of pixel, often y-max from dl site minus pixSize/2
proj = 'WGS84' #projection      
        
#Create Tiffs only for selected variable, iterate over varListnoDim if there are
#several and it should be done for each
var = varListnoDim[0]

#iterate through all variable steps
numSteps = len(rootgrp.variables[var])

for i in range(numSteps):
    timestep_ar = rootgrp.variables[var][i][:][:]
    outFile = outFol + str(i+1) + ".tif"

    funcs.array_to_raster_noTi(xdim,ydim,pixSize,x_min,y_max,proj,timestep_ar,outFile)
      
