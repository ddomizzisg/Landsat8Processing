import os
import math
import Functions as funcs
import numpy as np


def read_metadata(curFol,LSname):
    
    metaDict = {}
    
    #Find the metafile and extract variables
    for x in os.listdir(curFol):

        if x[-7:].lower() == "mtl.txt":

            # Doesn't matter which Landsat, dictionary is only filled with exisiting keywords
            metaFile = open(curFol + "/" + x, "r")

            #Name of current Landsat file, extracted from first band name
            metaDict['julDay'] = int(LSname[29:34])
            metaDict['year'] = int(LSname[26:30])

            for lines in metaFile.readlines():
                #lines still contain whitespaces
                #strLine = lines.decode("utf-8").replace(" ", "")
                strLine = lines.replace(" ", "")
                #print strLine
                if strLine[:13] == 'SPACECRAFT_ID':
                    metaDict['spacecraft_ID'] = strLine[15:-2]
                if strLine[:8] == 'WRS_PATH':
                    metaDict['wrs_path'] = strLine[9:]
                if strLine[:7] == 'WRS_ROW':
                    metaDict['wrs_row'] = strLine[8:]
                if strLine[:11] == 'CLOUD_COVER':
                    try:
                        metaDict['cloud_cover'] = float(strLine[12:-1])
                    except:
                        pass
                if strLine[:13] == 'DATE_ACQUIRED':
                    metaDict['date_aquired_str'] = strLine[14:-1]
                if strLine[:17] == 'SCENE_CENTER_TIME':
                    metaDict['scene_center_time_str'] = strLine[18:-1]
                if strLine[:8] == 'UTM_ZONE':
                    metaDict['utm_zone'] = strLine[9:-1]

                if strLine[:11] == 'SUN_AZIMUTH':
                    metaDict['sun_azimuth'] = float(strLine[12:])
                if strLine[:13] == 'SUN_ELEVATION':
                    metaDict['sun_elevation'] = float(strLine[14:])
                if strLine[:18] == 'EARTH_SUN_DISTANCE':
                    metaDict['earth_sun_distance'] = float(strLine[19:])

                #Radiances, first ones need to make sure Band_10 or Band_11 are not chosen instead
                if strLine[:23] == 'RADIANCE_MAXIMUM_BAND_1' and strLine[23] == "=":
                    metaDict['radiance_max_B1'] = float(strLine[24:-2])
                if strLine[:23] == 'RADIANCE_MINIMUM_BAND_1' and strLine[23] == "=":
                    metaDict['radiance_min_B1'] = float(strLine[24:-2])
                if strLine[:23] == 'RADIANCE_MAXIMUM_BAND_2':
                    metaDict['radiance_max_B2'] = float(strLine[24:-2])
                if strLine[:23] == 'RADIANCE_MINIMUM_BAND_2':
                    metaDict['radiance_min_B2'] = float(strLine[24:-2])
                if strLine[:23] == 'RADIANCE_MAXIMUM_BAND_3':
                    metaDict['radiance_max_B3'] = float(strLine[24:-2])
                if strLine[:23] == 'RADIANCE_MINIMUM_BAND_3':
                    metaDict['radiance_min_B3'] = float(strLine[24:-2])
                if strLine[:23] == 'RADIANCE_MAXIMUM_BAND_4':
                    metaDict['radiance_max_B4'] = float(strLine[24:-2])
                if strLine[:23] == 'RADIANCE_MINIMUM_BAND_4':
                    metaDict['radiance_min_B4'] = float(strLine[24:-2])
                if strLine[:23] == 'RADIANCE_MAXIMUM_BAND_5':
                    metaDict['radiance_max_B5'] = float(strLine[24:-2])
                if strLine[:23] == 'RADIANCE_MINIMUM_BAND_5':
                    metaDict['radiance_min_B5'] = float(strLine[24:-2])

                if LSname[3] == '8':
                    if strLine[:23] == 'RADIANCE_MAXIMUM_BAND_6':
                        metaDict['radiance_max_B6'] = float(strLine[24:-2])
                    if strLine[:23] == 'RADIANCE_MINIMUM_BAND_6':
                        metaDict['radiance_min_B6'] = float(strLine[24:-2])
                if LSname[3] == '7':
                    if strLine[:30] == 'RADIANCE_MAXIMUM_BAND_6_VCID_1':
                        metaDict['radiance_max_B61'] = float(strLine[31:-2])
                    if strLine[:30] == 'RADIANCE_MINIMUM_BAND_6_VCID_1':
                        metaDict['radiance_min_B61'] = float(strLine[31:-2])
                    if strLine[:30] == 'RADIANCE_MAXIMUM_BAND_6_VCID_2':
                        metaDict['radiance_max_B62'] = float(strLine[31:-2])
                    if strLine[:30] == 'RADIANCE_MINIMUM_BAND_6_VCID_2':
                        metaDict['radiance_min_B62'] = float(strLine[31:-2])
                if LSname[3] == '5':
                    if strLine[:23] == 'RADIANCE_MAXIMUM_BAND_6':
                        metaDict['radiance_max_B6'] = float(strLine[24:-2])
                    if strLine[:23] == 'RADIANCE_MINIMUM_BAND_6':
                        metaDict['radiance_min_B6'] = float(strLine[24:-2])

                if strLine[:23] == 'RADIANCE_MAXIMUM_BAND_7':
                    metaDict['radiance_max_B7'] = float(strLine[24:-2])
                if strLine[:23] == 'RADIANCE_MINIMUM_BAND_7':
                    metaDict['radiance_min_B7'] = float(strLine[24:-2])
                if strLine[:23] == 'RADIANCE_MAXIMUM_BAND_8':
                    metaDict['radiance_max_B8'] = float(strLine[24:-2])
                if strLine[:23] == 'RADIANCE_MINIMUM_BAND_8':
                    metaDict['radiance_min_B8'] = float(strLine[24:-2])
                if strLine[:23] == 'RADIANCE_MAXIMUM_BAND_9':
                    metaDict['radiance_max_B9'] = float(strLine[24:-2])
                if strLine[:23] == 'RADIANCE_MINIMUM_BAND_9':
                    metaDict['radiance_min_B9'] = float(strLine[24:-2])

                if strLine[:24] == 'RADIANCE_MAXIMUM_BAND_10':
                    metaDict['radiance_max_B10'] = float(strLine[25:-2])
                if strLine[:24] == 'RADIANCE_MINIMUM_BAND_10':
                    metaDict['radiance_min_B10'] = float(strLine[25:-2])
                if strLine[:24] == 'RADIANCE_MAXIMUM_BAND_11':
                    metaDict['radiance_max_B11'] = float(strLine[25:-2])
                if strLine[:24] == 'RADIANCE_MINIMUM_BAND_11':
                    metaDict['radiance_min_B11'] = float(strLine[25:-2])



                #Reflectances, only 9 bands in metafile
                if strLine[:26] == 'REFLECTANCE_MAXIMUM_BAND_1':
                    metaDict['reflectance_max_B1'] = float(strLine[27:-2])
                if strLine[:26] == 'REFLECTANCE_MINIMUM_BAND_1':
                    metaDict['reflectance_min_B1'] = float(strLine[27:-2])
                if strLine[:26] == 'REFLECTANCE_MAXIMUM_BAND_2':
                    metaDict['reflectance_max_B2'] = float(strLine[27:-2])
                if strLine[:26] == 'REFLECTANCE_MINIMUM_BAND_2':
                    metaDict['reflectance_min_B2'] = float(strLine[27:-2])
                if strLine[:26] == 'REFLECTANCE_MAXIMUM_BAND_3':
                    metaDict['reflectance_max_B3'] = float(strLine[27:-2])
                if strLine[:26] == 'REFLECTANCE_MINIMUM_BAND_3':
                    metaDict['reflectance_min_B3'] = float(strLine[27:-2])
                if strLine[:26] == 'REFLECTANCE_MAXIMUM_BAND_4':
                    metaDict['reflectance_max_B4'] = float(strLine[27:-2])
                if strLine[:26] == 'REFLECTANCE_MINIMUM_BAND_4':
                    metaDict['reflectance_min_B4'] = float(strLine[27:-2])
                if strLine[:26] == 'REFLECTANCE_MAXIMUM_BAND_5':
                    metaDict['reflectance_max_B5'] = float(strLine[27:-2])
                if strLine[:26] == 'REFLECTANCE_MINIMUM_BAND_5':
                    metaDict['reflectance_min_B5'] = float(strLine[27:-2])
                if strLine[:26] == 'REFLECTANCE_MAXIMUM_BAND_6':
                    metaDict['reflectance_max_B6'] = float(strLine[27:-2])
                if strLine[:26] == 'REFLECTANCE_MINIMUM_BAND_6':
                    metaDict['reflectance_min_B6'] = float(strLine[27:-2])
                if strLine[:26] == 'REFLECTANCE_MAXIMUM_BAND_7':
                    metaDict['reflectance_max_B7'] = float(strLine[27:-2])
                if strLine[:26] == 'REFLECTANCE_MINIMUM_BAND_7':
                    metaDict['reflectance_min_B7'] = float(strLine[27:-2])
                if strLine[:26] == 'REFLECTANCE_MAXIMUM_BAND_8':
                    metaDict['reflectance_max_B8'] = float(strLine[27:-2])
                if strLine[:26] == 'REFLECTANCE_MINIMUM_BAND_8':
                    metaDict['reflectance_min_B8'] = float(strLine[27:-2])
                if strLine[:26] == 'REFLECTANCE_MAXIMUM_BAND_9':
                    metaDict['reflectance_max_B9'] = float(strLine[27:-2])
                if strLine[:26] == 'REFLECTANCE_MINIMUM_BAND_9':
                    metaDict['reflectance_min_B9'] = float(strLine[27:-2])

                # Min_Max pixel value
                if strLine[:23] == 'QUANTIZE_CAL_MAX_BAND_1' and strLine[23] == "=":
                    metaDict['quant_max_B1'] = int(strLine[24:])
                if strLine[:23] == 'QUANTIZE_CAL_MIN_BAND_1' and strLine[23] == "=":
                    metaDict['quant_min_B1'] = int(strLine[24:])
                if strLine[:23] == 'QUANTIZE_CAL_MAX_BAND_2':
                    metaDict['quant_max_B2'] = int(strLine[24:])
                if strLine[:23] == 'QUANTIZE_CAL_MIN_BAND_2':
                    metaDict['quant_min_B2'] = int(strLine[24:])
                if strLine[:23] == 'QUANTIZE_CAL_MAX_BAND_3':
                    metaDict['quant_max_B3'] = int(strLine[24:])
                if strLine[:23] == 'QUANTIZE_CAL_MIN_BAND_3' :
                    metaDict['quant_min_B3'] = int(strLine[24:])
                if strLine[:23] == 'QUANTIZE_CAL_MAX_BAND_4' :
                    metaDict['quant_max_B4'] = int(strLine[24:])
                if strLine[:23] == 'QUANTIZE_CAL_MIN_BAND_4' :
                    metaDict['quant_min_B4'] = int(strLine[24:])
                if strLine[:23] == 'QUANTIZE_CAL_MAX_BAND_5':
                    metaDict['quant_max_B5'] = int(strLine[24:])
                if strLine[:23] == 'QUANTIZE_CAL_MIN_BAND_5' :
                    metaDict['quant_min_B5'] = int(strLine[24:])

                if LSname[3] == '8' or LSname[3] == '5':
                    if strLine[:23] == 'QUANTIZE_CAL_MAX_BAND_6':
                        metaDict['quant_max_B6'] = int(strLine[24:])
                    if strLine[:23] == 'QUANTIZE_CAL_MIN_BAND_6' :
                        metaDict['quant_min_B6'] = int(strLine[24:])
                if LSname[3] == '7':
                    if strLine[:30] == 'QUANTIZE_CAL_MAX_BAND_6_VCID_1':
                        metaDict['quant_max_B61'] = int(strLine[31:])
                    if strLine[:30] == 'QUANTIZE_CAL_MIN_BAND_6_VCID_1':
                        metaDict['quant_min_B61'] = int(strLine[31:])
                    if strLine[:30] == 'QUANTIZE_CAL_MAX_BAND_6_VCID_2':
                        metaDict['quant_max_B62'] = int(strLine[31:])
                    if strLine[:30] == 'QUANTIZE_CAL_MIN_BAND_6_VCID_2':
                        metaDict['quant_min_B62'] = int(strLine[31:])

                if strLine[:23] == 'QUANTIZE_CAL_MAX_BAND_7':
                    metaDict['quant_max_B7'] = int(strLine[24:])
                if strLine[:23] == 'QUANTIZE_CAL_MIN_BAND_7':
                    metaDict['quant_min_B7'] = int(strLine[24:])
                if strLine[:23] == 'QUANTIZE_CAL_MAX_BAND_8' :
                    metaDict['quant_max_B8'] = int(strLine[24:])
                if strLine[:23] == 'QUANTIZE_CAL_MIN_BAND_8' :
                    metaDict['quant_min_B8'] = int(strLine[24:])
                if strLine[:23] == 'QUANTIZE_CAL_MAX_BAND_9' :
                    metaDict['quant_max_B9'] = int(strLine[24:])
                if strLine[:23] == 'QUANTIZE_CAL_MIN_BAND_9':
                    metaDict['quant_min_B9'] = int(strLine[24:])

                if strLine[:24] == 'QUANTIZE_CAL_MAX_BAND_10':
                    metaDict['quant_max_B10'] = int(strLine[25:])
                if strLine[:24] == 'QUANTIZE_CAL_MIN_BAND_10':
                    metaDict['quant_min_B10'] = int(strLine[25:])
                if strLine[:24] == 'QUANTIZE_CAL_MAX_BAND_11':
                    metaDict['quant_max_B11'] = int(strLine[25:])
                if strLine[:24] == 'QUANTIZE_CAL_MIN_BAND_11':
                    metaDict['quant_min_B11'] = int(strLine[25:])


                # Radiometric Rescaling
                if strLine[:20] == 'RADIANCE_MULT_BAND_1' and strLine[20] == "=":
                    metaDict['radiance_mult_B1'] = float(strLine[21:])
                if strLine[:20] == 'RADIANCE_MULT_BAND_2':
                    metaDict['radiance_mult_B2'] = float(strLine[21:])
                if strLine[:20] == 'RADIANCE_MULT_BAND_3':
                    metaDict['radiance_mult_B3'] = float(strLine[21:])
                if strLine[:20] == 'RADIANCE_MULT_BAND_4':
                    metaDict['radiance_mult_B4'] = float(strLine[21:])
                if strLine[:20] == 'RADIANCE_MULT_BAND_5':
                    metaDict['radiance_mult_B5'] = float(strLine[21:])

                if LSname[3] == '8' or LSname[3] == '5':
                    if strLine[:20] == 'RADIANCE_MULT_BAND_6':
                        metaDict['radiance_mult_B6'] = float(strLine[21:])
                if LSname[3] == '7':
                    if strLine[:27] == 'RADIANCE_MULT_BAND_6_VCID_1':
                        metaDict['radiance_mult_B61'] = float(strLine[28:])
                    if strLine[:27] == 'RADIANCE_MULT_BAND_6_VCID_2':
                        metaDict['radiance_mult_B62'] = float(strLine[28:])

                if strLine[:20] == 'RADIANCE_MULT_BAND_7':
                    metaDict['radiance_mult_B7'] = float(strLine[21:])
                if strLine[:20] == 'RADIANCE_MULT_BAND_8':
                    metaDict['radiance_mult_B8'] = float(strLine[21:])
                if strLine[:20] == 'RADIANCE_MULT_BAND_9':
                    metaDict['radiance_mult_B9'] = float(strLine[21:])
                if strLine[:21] == 'RADIANCE_MULT_BAND_10':
                    metaDict['radiance_mult_B10'] = float(strLine[22:])
                if strLine[:21] == 'RADIANCE_MULT_BAND_11':
                    metaDict['radiance_mult_B11'] = float(strLine[22:])

                if strLine[:19] == 'RADIANCE_ADD_BAND_1' and strLine[19] == "=":
                    metaDict['radiance_add_B1'] = float(strLine[20:])
                if strLine[:19] == 'RADIANCE_ADD_BAND_2':
                    metaDict['radiance_add_B2'] = float(strLine[20:])
                if strLine[:19] == 'RADIANCE_ADD_BAND_3':
                    metaDict['radiance_add_B3'] = float(strLine[20:])
                if strLine[:19] == 'RADIANCE_ADD_BAND_4':
                    metaDict['radiance_add_B4'] = float(strLine[20:])
                if strLine[:19] == 'RADIANCE_ADD_BAND_5':
                    metaDict['radiance_add_B5'] = float(strLine[20:])

                if LSname[3] == '8' or LSname[3] == '5':
                    if strLine[:19] == 'RADIANCE_ADD_BAND_6':
                        metaDict['radiance_add_B6'] = float(strLine[20:])
                if LSname[3] == '7':
                    if strLine[:26] == 'RADIANCE_ADD_BAND_6_VCID_1':
                        metaDict['radiance_add_B61'] = float(strLine[27:])
                    if strLine[:26] == 'RADIANCE_ADD_BAND_6_VCID_2':
                        metaDict['radiance_add_B62'] = float(strLine[27:])

                if strLine[:19] == 'RADIANCE_ADD_BAND_7':
                    metaDict['radiance_add_B7'] = float(strLine[20:])
                if strLine[:19] == 'RADIANCE_ADD_BAND_8':
                    metaDict['radiance_add_B8'] = float(strLine[20:])
                if strLine[:19] == 'RADIANCE_ADD_BAND_9':
                    metaDict['radiance_add_B9'] = float(strLine[20:])
                if strLine[:20] == 'RADIANCE_ADD_BAND_10':
                    metaDict['radiance_add_B10'] = float(strLine[21:])
                if strLine[:20] == 'RADIANCE_ADD_BAND_11':
                    metaDict['radiance_add_B11'] = float(strLine[21:])


                if strLine[:23] == 'REFLECTANCE_MULT_BAND_1' and strLine[23] == "=":
                    metaDict['reflectance_mult_B1'] = float(strLine[24:])
                if strLine[:23] == 'REFLECTANCE_MULT_BAND_2':
                    metaDict['reflectance_mult_B2'] = float(strLine[24:])
                if strLine[:23] == 'REFLECTANCE_MULT_BAND_3':
                    metaDict['reflectance_mult_B3'] = float(strLine[24:])
                if strLine[:23] == 'REFLECTANCE_MULT_BAND_4':
                    metaDict['reflectance_mult_B4'] = float(strLine[24:])
                if strLine[:23] == 'REFLECTANCE_MULT_BAND_5':
                    metaDict['reflectance_mult_B5'] = float(strLine[24:])
                if strLine[:23] == 'REFLECTANCE_MULT_BAND_6':
                    metaDict['reflectance_mult_B6'] = float(strLine[24:])
                if strLine[:23] == 'REFLECTANCE_MULT_BAND_7':
                    metaDict['reflectance_mult_B7'] = float(strLine[24:])
                if strLine[:23] == 'REFLECTANCE_MULT_BAND_8':
                    metaDict['reflectance_mult_B8'] = float(strLine[24:])
                if strLine[:23] == 'REFLECTANCE_MULT_BAND_9':
                    metaDict['reflectance_mult_B9'] = float(strLine[24:])

                if strLine[:22] == 'REFLECTANCE_ADD_BAND_1' and strLine[22] == "=":
                    metaDict['reflectance_add_B1'] = float(strLine[23:])
                if strLine[:22] == 'REFLECTANCE_ADD_BAND_2':
                    metaDict['reflectance_add_B2'] = float(strLine[23:])
                if strLine[:22] == 'REFLECTANCE_ADD_BAND_3':
                    metaDict['reflectance_add_B3'] = float(strLine[23:])
                if strLine[:22] == 'REFLECTANCE_ADD_BAND_4':
                    metaDict['reflectance_add_B4'] = float(strLine[23:])
                if strLine[:22] == 'REFLECTANCE_ADD_BAND_5':
                    metaDict['reflectance_add_B5'] = float(strLine[23:])
                if strLine[:22] == 'REFLECTANCE_ADD_BAND_6':
                    metaDict['reflectance_add_B6'] = float(strLine[23:])
                if strLine[:22] == 'REFLECTANCE_ADD_BAND_7':
                    metaDict['reflectance_add_B7'] = float(strLine[23:])
                if strLine[:22] == 'REFLECTANCE_ADD_BAND_8':
                    metaDict['reflectance_add_B8'] = float(strLine[23:])
                if strLine[:22] == 'REFLECTANCE_ADD_BAND_9':
                    metaDict['reflectance_add_B9'] = float(strLine[23:])

                #Thermal Constants
                if strLine[:19] == 'K1_CONSTANT_BAND_10':
                    metaDict['k1_const_B10'] = float(strLine[20:])
                if strLine[:19] == 'K1_CONSTANT_BAND_11':
                    metaDict['k1_const_B11'] = float(strLine[20:])
                if strLine[:19] == 'K2_CONSTANT_BAND_10':
                    metaDict['k2_const_B10'] = float(strLine[20:])
                if strLine[:19] == 'K2_CONSTANT_BAND_11':
                    metaDict['k2_const_B11'] = float(strLine[20:])

                metaFile.close()

    return metaDict

# Calculate radiation and toa_reflectance
def rad_toa(LSname,curFol,metaDict):

    #creates a dict that will hold each bands/rasters name and corresponding arrays
    # done beforw with eval(varName = create.array), this strangly didn't work for
    # all band in Python 3.5
    rrdict = {}

    #Handle Landsat 8 differently than 4,5 or 7
    if LSname[3] == '8':

        for x in range(1,10):
            xStr = str(x)
            print(curFol + LSname + "_B" + xStr + ".TIF")
            #read bands as arrays
            rrdict['arrayDN'+xStr] = funcs.singleTifToArray(curFol + LSname + "_B" + xStr + ".TIF")

            #convert to radiance and convert to 32-bit floating point for memory saving
            rrdict['lambda'+xStr] = metaDict['radiance_mult_B'+xStr] * rrdict['arrayDN'+xStr] + metaDict['radiance_add_B'+xStr]
            rrdict['lambda'+xStr] = rrdict['lambda'+xStr].astype(np.float32)

            #convert to reflectance and convert to 32-bit floating point for memory saving
            rrdict['reflectance'+xStr] = ( ( metaDict['reflectance_mult_B'+xStr] * rrdict['arrayDN'+xStr] + \
                                             metaDict['reflectance_add_B'+xStr] ) / \
                                             math.sin(math.radians(metaDict['sun_elevation'])) )

            rrdict['reflectance'+xStr] = rrdict['reflectance'+xStr].astype(np.float32)

            #del rrdict['arrayDN'+xStr]
    return rrdict

def rad_toa_band(LSname,curFol,metaDict,band):
    rrdict = {}
    if LSname[3] == '8':
        xStr = str(band)
        print(curFol + LSname + "_B" + xStr + ".TIF")
        #read bands as arrays
        rrdict['arrayDN'+xStr] = funcs.singleTifToArray(curFol + LSname + "_B" + xStr + ".TIF")

        #convert to radiance and convert to 32-bit floating point for memory saving
        rrdict['lambda'+xStr] = metaDict['radiance_mult_B'+xStr] * rrdict['arrayDN'+xStr] + metaDict['radiance_add_B'+xStr]
        rrdict['lambda'+xStr] = rrdict['lambda'+xStr].astype(np.float32)

        #convert to reflectance and convert to 32-bit floating point for memory saving
        rrdict['reflectance'+xStr] = ( ( metaDict['reflectance_mult_B'+xStr] * rrdict['arrayDN'+xStr] + \
                                         metaDict['reflectance_add_B'+xStr] ) / \
                                         math.sin(math.radians(metaDict['sun_elevation'])) )

        rrdict['reflectance'+xStr] = rrdict['reflectance'+xStr].astype(np.float32)

        del rrdict['arrayDN'+xStr]
    return rrdict

# save radiation rasters to disk
def saveRadFunc(LSname, curFol, metaDict, calcKelvin = 0):

    if LSname[3] == '8':

        endRange = 10

        for x in range(1,endRange):
            xStr = str(x)
            rrdict = rad_toa_band(LSname,curFol,metaDict,x)
            funcs.array_to_raster(curFol + LSname + "_B" +xStr+ ".TIF", rrdict['lambda'+xStr], \
            curFol + "Radiation_B"+xStr+".TIF")
            del rrdict['lambda'+xStr]

    elif LSname[3] == '7' or LSname[3] == '5' or LSname[3] == '4':

        if LSname[3] == '7':
            lastBand = 9
        else:
            lastBand = 8

        for x in range(1,lastBand):
                xStr = str(x)
                if LSname[3] == '7':
                    if x != 6:
                        funcs.array_to_raster(curFol + LSname + "_B" +xStr + ".TIF", rrdict['lambda'+xStr], \
                        curFol + "Radiation_B"+xStr+".TIF")
                        #del rrdict['lambda'+xStr]

                    else:
                        if calcKelvin != 0:
                            for y in range(1,3):
                                yStr = str(y)
                                try:
                                    funcs.array_to_raster(curFol + LSname +  \
                                    "_B"+xStr+"_VCID_"+yStr+".TIF", rrdict['lambda'+xStr+yStr], curFol + \
                                    "Radiation_B"+xStr+yStr+".TIF")
                                    #del  rrdict['lambda'+xStr+yStr]

                                except:
                                    pass

                if LSname[3] == '5' or LSname[3] == '4':
                    if calcKelvin != 0:
                        funcs.array_to_raster(curFol + LSname + "_B"+xStr+".TIF", rrdict['lambda'+xStr], \
                            curFol + "Radiation_B"+xStr+".TIF")
                    #del rrdict['lambda'+xStr]