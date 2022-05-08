# -*- coding: utf-8 -*-

# Calculate pixel-based linear regressions for many different month/season combinations
# Process can be restarted any time, as the script checks for existing files in the outFol

import Functions as funcs
import numpy, itertools, os, datetime

#Input Folder containing monthly tifs in form year_monthnumber as in 1999_03.tif
inFol = ".../inFol/"
outFol = ".../outFol/"

startYear = 1999
endYear = 2013


startTime = datetime.datetime.now()

# Months to be used, min:1 max:12
monthInt = [1,2,3,4,5,6,7,8,9,10,11,12]

monthNum = ['01', '02', '03', '04', '05', '06', 
            '07', '08', '09', '10', '11', '12']

monthNameList = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
 
                
# from https://docs.python.org/3/library/itertools.html
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    #s = list(iterable)
    #return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))
    psList = []
    for L in range(0, len(iterable)+1):
        for subset in itertools.combinations(iterable, L):
            psList.append(subset)
    return psList

# Create a Powerset of all months
monthPS = powerset(monthInt)
maxLen = len(monthInt)

# Determine first raster, used for conversion from arrays to tif
for allRasters in os.listdir(inFol):
        if allRasters[-3:] == "tif":
            firstRasStr = inFol + allRasters
            break

# Create a list of all combinations with >2 elements and only consecutive months
combList = []
for i in monthPS:
    x = 0
    setLen = len(i)
    
    for j in range(setLen-1):
        #Test if months are consecutive... 
        if abs(i[j] - i[j+1]) == 1:
            x = x + 1
    #if x is the same length as current set, all months are consecutive
    #at least 2 months should be in set
    if x == setLen-1 and setLen != 1 and setLen != 0:
        combList.append(i)
    

# now combinations are still missing that go over the Dec-Jan line  
# therefore combList entries are shifted by 1, entries that are >maxLen are
#  subtracted by maxLen... this is repeated by a shift by 2 etc.
# only resulting non-existent combinations are then appended to combList  


combList2 = []    
for j in range(12): #value to add to comblist
   
    for k in combList:
        kList = list(k) 
        newList1 = [x2+j for x2 in kList] #new sets with j added
 
        newTuple = tuple(newList1)
        
        if newTuple not in combList: #only if set is not already exisiting it gets in
            combList2.append(newTuple)
        
combList3 = list(set(combList2))
combList = combList[:] + combList3[:]

#delete all entries that have only values > 12 i.e. are in a new year entirely
for ii in range(len(combList)-1,-1,-1):
    if all(jj > 12 for jj in combList[ii]):
        del combList[ii]

#check if files already exist, so no double calculations are done
#only the existence of Mann-Kendall files is tested
for i in range(len(combList)-1,-1,-1):
                   
        chkName = ""
        for elements in combList[i]:  
            chkName = chkName + str(elements)
        for files in os.listdir(outFol):
            if files == chkName + "_mkP.tif":
                del combList[i]
            
    
 

# Use combList to create a list of files 
for i in combList:
    
    # calculate process when all months in the same year
    if all(jj < 13 for jj in i):    
    
        startTime2 = datetime.datetime.now()
    
        #Define file output name, basically number series of months
        outName = ""
        for elements in i:  
            outName = outName + str(elements)
            
        statsList = []  # will contain the arrays for the linear regression
        for year in range(startYear,endYear+1):
            
            pathList = [] # will contain paths for all months in current set
            for setPart in i:
                fileName = str(year) + "_" + monthNum[setPart-1] + ".tif"
                pathList.append(inFol + fileName)
            print("pathList created with ", len(pathList), " elements for: ", year, " set: ", i)
            
            arrayList = [] # will contain all pathList entries as numpy arrays
            for rasPath in pathList:
                newArray = funcs.singleTifToArray(rasPath)
                arrayList.append(newArray)
            
            #calculate the mean of all arrays
            zeroArray = numpy.zeros(arrayList[0].shape)
            for inArray in arrayList:
                zeroArray = zeroArray + inArray
            meanArray = zeroArray / len(arrayList)
            
            statsList.append(meanArray)
            


    
    # calcluate process when months span over 2 years    
    else:   
        startTime2 = datetime.datetime.now()
    
        #Define file output name, basically number series of months
        outName = ""
        for elements in i:  
            outName = outName + str(elements)
    
        statsList = []  # will contain the arrays for the linear regression    
        for year in range(startYear,endYear):            
            pathList = [] # will contain paths for all months in current set
            for setPart in i:
                
                if setPart < 13:
                    fileName = str(year) + "_" + monthNum[setPart-1] + ".tif"
                    pathList.append(inFol + fileName)
                else:
                    fileName = str(year+1) + "_" + monthNum[setPart-13] + ".tif"
                    pathList.append(inFol + fileName)
            print("pathList created with ", len(pathList), " elements for: ", year, " set: ", i)
            
            arrayList = [] # will contain all pathList entries as numpy arrays
            for rasPath in pathList:
                newArray = funcs.singleTifToArray(rasPath)
                arrayList.append(newArray)
            
            #calculate the mean of all arrays
            zeroArray = numpy.zeros(arrayList[0].shape)
            for inArray in arrayList:
                zeroArray = zeroArray + inArray
            meanArray = zeroArray / len(arrayList)
            
            statsList.append(meanArray)
        
    
    #calcluate linear regression
    statsTuple = funcs.linReg(statsList)
        
    #Assign names and convert linear regression output into tiff
    outNames = (outName+"_slope.tif", outName+"_intcp.tif", outName+"_rval.tif", 
                outName+"_pval.tif", outName+"_stderr.tif", outName+"_mkP.tif")
    for fname, i in zip(outNames, range(len(outNames))):
        funcs.array_to_raster(firstRasStr,statsTuple[i],outFol+fname)
    
    print("\ntime: ", (datetime.datetime.now()-startTime).seconds, " seconds")
        
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
