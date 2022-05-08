# -*- coding: utf-8 -*-

import os
import Functions as funcs
import numpy as np

# uses the output from the monthly combinations (best_Reg.py) and returns the best
# combation at each pixel location

#Input Folder containing monthly combinations as in 12345.tif for Jan-Feb-Mar-Apr-May
inFol = ".../inFol/"
outFol = ".../outFol/"



def getBestVal(inFol,outFol,combDct):
    endings = ("_slope.tif", "_intcp.tif", "_rval.tif", "_pval.tif", "_stderr.tif", "_mkP.tif")
    
    # Determine first raster, used for conversion from arrays to tif
    for allRasters in os.listdir(inFol):
            if allRasters[-3:] == "tif":
                firstRasStr = inFol + allRasters
                break
               
    for ending in endings:
        rasLst = [] #stores the rasterPaths to be tested for largest value later
        for file in os.listdir(inFol):
            if file[-len(ending):] == ending:
                rasLst.append(file)
        
        # For p-values, MKP-values and r-values one wants to know the smallest value
        if ending == "_pval.tif" or ending == "_mkP.tif" or ending == "_rval.tif":
            for rasNum in range(len(rasLst)):  
                ras = rasLst[rasNum]
                curComb = ras[:-len(ending)]   #number-month combination
                curKey = combDct[curComb]       #associated simple number in the dictionary
    
                if rasNum == 0: 
                    #create the array that will store the number of the month combination
                    nameArray = funcs.singleTifToArray(inFol+rasLst[0]) * 0 + curKey
                    #create the array that will store the actual smallest value
                    valueArray = funcs.singleTifToArray(inFol+rasLst[0])
                    
                    #same but for next raster in list
                    curComb2 = rasLst[1][:-len(ending)]
                    curKey2 = combDct[curComb2]
                    nameArray2 = funcs.singleTifToArray(inFol+rasLst[1]) * 0 + curKey2
                    valueArray2 = funcs.singleTifToArray(inFol+rasLst[1])
                    
                    
                    condlist = [ valueArray < valueArray2 ]
                    
                    choicelist  = [ nameArray ]
                    resultName = np.select(condlist, choicelist, nameArray2)
                    
                    choicelist  = [ valueArray ]
                    resultValue = np.select(condlist, choicelist, valueArray2)
                elif i == 1:
                    continue
                else:
                    nameArray = funcs.singleTifToArray(inFol+rasLst[rasNum]) * 0 + curKey 
                    valueArray = funcs.singleTifToArray(inFol+rasLst[rasNum])
                    
                    condlist = [ resultValue < valueArray ]
                    
                    choicelist  = [ resultName ]
                    resultName = np.select(condlist, choicelist, nameArray)   
                    
                    choicelist  = [ resultValue ]
                    resultValue = np.select(condlist, choicelist, valueArray)
        
            if ending == "_rval.tif":      
                funcs.array_to_raster(firstRasStr,resultName,outFol+ "name_small"+ending)
                funcs.array_to_raster(firstRasStr,resultValue,outFol+ "value_small"+ending)
            else:
                funcs.array_to_raster(firstRasStr,resultName,outFol+ "name_"+ending)
                funcs.array_to_raster(firstRasStr,resultValue,outFol+ "value_"+ending)
            
        # all others, including r-values, biggest values are interesting
        if (ending == "_slope.tif" or ending == "_intcp.tif" or ending == "_stderr.tif" 
            or ending == "_rval.tif"):        
            for rasNum in range(len(rasLst)):  
                ras = rasLst[rasNum]
                curComb = ras[:-len(ending)]   #number-month combination
                curKey = combDct[curComb]       #associated simple number in the dictionary
    
                if rasNum == 0: 
                    #create the array that will store the number of the month combination
                    nameArray = funcs.singleTifToArray(inFol+rasLst[0]) * 0 + curKey
                    #create the array that will store the actual biggest value
                    valueArray = funcs.singleTifToArray(inFol+rasLst[0])
                    
                    #same but for next raster in list
                    curComb2 = rasLst[1][:-len(ending)]
                    curKey2 = combDct[curComb2]
                    nameArray2 = funcs.singleTifToArray(inFol+rasLst[1]) * 0 + curKey2
                    valueArray2 = funcs.singleTifToArray(inFol+rasLst[1])
                    
                    
                    condlist = [ valueArray > valueArray2 ]
                    
                    choicelist  = [ nameArray ]
                    resultName = np.select(condlist, choicelist, nameArray2)
                    
                    choicelist  = [ valueArray ]
                    resultValue = np.select(condlist, choicelist, valueArray2)
                elif i == 1:
                    continue
                else:
                    nameArray = funcs.singleTifToArray(inFol+rasLst[rasNum]) * 0 + curKey 
                    valueArray = funcs.singleTifToArray(inFol+rasLst[rasNum])
                    
                    condlist = [ resultValue > valueArray ]
                    
                    choicelist  = [ resultName ]
                    resultName = np.select(condlist, choicelist, nameArray)   
                    
                    choicelist  = [ resultValue ]
                    resultValue = np.select(condlist, choicelist, valueArray)

    
            if ending == "_rval.tif":      
                funcs.array_to_raster(firstRasStr,resultName,outFol+ "name_big_"+ending)
                funcs.array_to_raster(firstRasStr,resultValue,outFol+ "value_big_"+ending)
            else:
                funcs.array_to_raster(firstRasStr,resultName,outFol+ "name_"+ending)
                funcs.array_to_raster(firstRasStr,resultValue,outFol+ "value_"+ending)
        
        print(ending, " done")



#diction should be a dictioniary where long numbers are the keys
def atLoc(mkNameFile,diction,inFol,outFol):
            mkArray = funcs.singleTifToArray(mkNameFile)
            outArray= np.zeros(mkArray.shape)
            
            for key in diction:
                dictVal = diction[key]
                keyArray = funcs.singleTifToArray(inFol + str(key) + "_rval.tif")
                
                condlist = [ mkArray == dictVal ]
                choicelist = [ keyArray ]
                outArray = np.select(condlist, choicelist, outArray)
                
            funcs.array_to_raster(mkNameFile,outArray, outFol+"rval_MK_name_sig2.tif")
                
            
#VERY INEFFICIENT -> deprecated:
#iterate over the best_pix Names of Mann Kendall and extract the rvals... of this combination
#return as own raster
#mkNameFile is the Mann-Kendall file to iterate over, inFol contains the rval rasters, 
# diction is a dictionary with short numbers as keys  (the ones in mkNameFile)
#    and long numbers as values
# noData is the value to be skipped as it does not indicate a real combination
def atLoc2(mkNameFile,diction,inFol,outFol,noData):
    
    mkArray = funcs.singleTifToArray(mkNameFile)
    newArray = np.zeros(mkArray.shape) #rvals are written into this array

    
    for yCo in range(mkArray.shape[0]):
        for xCo in range(mkArray.shape[1]):

            mkValue = mkArray[yCo][xCo] #check the short number at each location in mkarray            
 
            try:
                longNum = diction[mkValue] #extract long number from dictionary
            
                #read value at rval file of the large number
                readArray = funcs.singleTifToArray(inFol + str(longNum)+"_rval.tif") 
                
                newArray[yCo][xCo] = readArray[yCo][xCo]
            
            except:
                newArray[yCo][xCo] = noData
                
    funcs.array_to_raster(mkNameFile,newArray,outFol+"rval_MK_name_sig.tif")            
            
          

#rval files are used to create the month combinations contained in the filename
combLst = []
for i in os.listdir(inFol):
    if i[-9:] == "_rval.tif":
        comb = i[:-9]
        combLst.append(comb)

#create a dictionary that assigns single numbers as identifiers of (too long) month combinations
#beginning with 1 and skipping 0
#also write key-value pairs into a file
combDct = {}
infoTxt = open(outFol + "_Info.txt", "a")
infoTxt.write("Files beginning with \"name\" contain the name of the monthly combination. \
                This is the number in the left column displayed below. \n \
                Files beginning with \"value\" contain the actual value of \
                the biggest/smallest pixel existing. \n For the r-value biggest and \
                smallest pixels are stored in separate files. pval and mkp store \
                only the smallest, all other only the largest value. \n\n")
for x,y in zip(combLst, range(1,len(combLst)+1)):
    combDct[x] = y
    infoTxt.write(str(y) + "    " + str(x) + "\n")
infoTxt.close()

getBestVal(inFol,outFol,combDct)


# The following can be used independently of the steps above
# It looks at the month combination of best MK and saves the corresponding rvals in a raster
# Like combDct but keys and values are switched
invcombDct = {}
for y,x in zip(combLst, range(1,len(combLst)+1)):
    invcombDct[x] = y


mkNameFile = ".../name__mkP.tif"
inFol2 = ".../inFol/"
outFol2 = "/outFol/"
noData = -3.4028231e+38
test = atLoc(mkNameFile,combDct,inFol2,outFol2) 

