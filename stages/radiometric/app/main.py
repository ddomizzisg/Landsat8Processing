import rasterio
from LS_ultils import read_metadata
import argparse
import os
#import shutil


def radiometric_corrections(path, name, output):
    for x in range(1,10):
        band_path = os.path.join(path, name + "_B%d.TIF" % x)
        with rasterio.open(band_path) as src:
            band = src.read(1)
            corrected_band = band * 0.1  # Apply the radiometric scale factor
            
            os.makedirs(os.path.join(output,name), exist_ok=True)
            #shutil.copyfile(os.path.join(path, name + "_MTL.txt"), os.path.join(output,name,name +  "_MTL.txt"))
            with rasterio.open(os.path.join(output,name,name +  "_B%d.TIF" % x) , 'w', **src.meta) as dst:
                dst.write(corrected_band, 1)


parser = argparse.ArgumentParser(
                    prog='LandSat8ToRGB',
                    description='Creates a PNG from the LandSat8 bands.')

parser.add_argument('path')           # positional argument
parser.add_argument('imagename')           # positional argument
parser.add_argument('-o', '--output') 

args = parser.parse_args()
radiometric_corrections(args.path, args.imagename, args.output)