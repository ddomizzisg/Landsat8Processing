import rasterio
from rasterio.mask import mask
import geopandas as gpd
from shapely.geometry import box
import argparse
import os

# 20.076776, -101.306667
#19.871558, -100.839748

def crop_bands(path, image_name, min_lat, min_lon, max_lat, max_lon, output=None):
    os.makedirs(os.path.join(output, image_name), exist_ok=True)
    bbox = box(min_lon, min_lat, max_lon, max_lat)
    print(bbox)
    print(min_lon, min_lat, max_lon, max_lat)
    #Patzcuaro
    #min_lon, min_lat = -101.723135, 19.538797
    #max_lon, max_lat = -101.540980, 19.695493
    #min_lon, min_lat = -101.315881, 19.870015
    #max_lon, max_lat = -100.827868, 20.084173
    
    print(min_lon, min_lat, max_lon, max_lat)

    # Create a bounding box geometry
    bbox = box(min_lon, min_lat, max_lon, max_lat)
    print(bbox)
    geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs='EPSG:4326')

    # Read the list of bands
    bands = [f'{path}/{image_name}_B{i}.TIF' for i in range(1, 10)]

    # Open the Landsat 8 image
    for i,b in enumerate(bands):
        with rasterio.open(b) as src:
            # Reproject the bounding box to the image's CRS
            geo = geo.to_crs(src.crs)

            # Crop the image using the bounding box
            out_image, out_transform = mask(src, geo.geometry, crop=True)
            out_meta = src.meta.copy()

            # Update the metadata with new dimensions and transform
            out_meta.update({
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform
            })

            # Save the cropped image
            with rasterio.open(f'{output}/{image_name}/{image_name}_B{i+1}.TIF', 'w', **out_meta) as dest:
                dest.write(out_image)


parser = argparse.ArgumentParser(
                    prog='LandSat8ToRGB',
                    description='Creates a PNG from the LandSat8 bands.')

parser.add_argument('path')           # positional argument
parser.add_argument('imagename')           # positional argument
parser.add_argument('min_lon', type=float)      
parser.add_argument('min_lat', type=float) 
parser.add_argument('max_lon', type=float) 
parser.add_argument('max_lat', type=float)      
parser.add_argument('-o', '--output') 

args = parser.parse_args()
crop_bands(args.path, args.imagename, args.min_lat, args.min_lon, args.max_lat, args.max_lon, output=args.output) 
