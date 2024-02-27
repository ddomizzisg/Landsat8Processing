import os
import numpy as np
import os
import Functions as funcs
import argparse

from LS_ultils import read_metadata

"""
  Arg: 
      data_array= (array of masked images path )
      band = band number 
  Returns:
      new_data_array = array of the radiance value of single masked image
  
  Function working:
      First it get the 'B' and 'G' value from the dictionary that we created 
      for landsat7. Then  by looping through the each pixel it converted the 
      pixel value to the radiance. and the return this value as an array
"""


def dn_to_radiance(path, band, metaDict)  :
    # getting the G value 
    #print(metaDict)
    channel_gain = float(metaDict['radiance_mult_B'+str(band)])

    # Getting the B value
    channel_offset = float(metaDict['radiance_mult_B'+str(band)])
    
    data = funcs.singleTifToArray(path)

    # creating a temp array to store the radiance value
    new_data = np.empty_like(data)
    new_data = data * channel_gain +channel_offset
    #loooping through the image
    # for i,row in enumerate(data):
    #     for j, col in enumerate(row):

    #         # checking if the pixel value is not nan, to avoid background correction 
    #         if data[i][j] != np.nan:
    #             new_data[i][j] = data[i][j] * channel_gain +channel_offset
    
    print(f'Radiance calculated for band {band}')
    return new_data

def make_corrections(folder, image_name, output="."):
    metaDict = read_metadata(folder,image_name)
    paths = []
    for x in range(1,10):
        band_path = os.path.join(folder, image_name + "_B%d.TIF" % x)
        new_data = dn_to_radiance(band_path, x, metaDict)
        os.makedirs( os.path.join(output, image_name), exist_ok=True)
        funcs.array_to_raster(band_path, new_data, os.path.join(output, image_name, image_name + "_B%d.TIF" % x))
        #paths.append(band_path)

    #masked_paths = apply_mask(paths, folder)
    #outputs = radiance_to_reflectance(masked_paths, 1, metaDict)
    
parser = argparse.ArgumentParser(
                    prog='LandSat8ToRGB',
                    description='Creates a PNG from the LandSat8 bands.')


parser.add_argument('path')           # positional argument
parser.add_argument('imagename')           # positional argument
parser.add_argument('-o', '--output') 

args = parser.parse_args()
    
make_corrections(args.path, args.imagename, output=args.output)