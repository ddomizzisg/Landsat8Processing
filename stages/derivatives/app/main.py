import numpy as np
import rasterio
import matplotlib.pyplot as plt
import os
import argparse
import earthpy.plot as ep
import earthpy.spatial as es
from matplotlib.colors import ListedColormap



def ndvi(nir_path, red_path, output):
    
    with rasterio.open(red_path) as red_band:
        meta = red_band.meta
        red = red_band.read(1).astype('float64')
        #ed[red == 0] = np.nan
        
    with rasterio.open(nir_path) as nir_band:
        nir = nir_band.read(1).astype('float64')
        #nir[nir == 0] = np.nan
    
    ndvi = es.normalized_diff(nir, red)
    titles = ["Landsat 8 - Normalized Difference Vegetation Index (NDVI)"]
    
    # Create classes and apply to NDVI results
    ndvi_class_bins = [-np.inf, 0, 0.1, 0.25, 0.4, np.inf]
    ndvi_landsat_class = np.digitize(ndvi, ndvi_class_bins)

    # Apply the nodata mask to the newly classified NDVI data
    ndvi_landsat_class = np.ma.masked_where(
        np.ma.getmask(ndvi), ndvi_landsat_class
    )
    np.unique(ndvi_landsat_class)
    
    # Define color map
    nbr_colors = ["gray", "y", "yellowgreen", "g", "darkgreen"]
    nbr_cmap = ListedColormap(nbr_colors)

    # Define class names
    ndvi_cat_names = [
        "No Vegetation",
        "Bare Area",
        "Low Vegetation",
        "Moderate Vegetation",
        "High Vegetation",
    ]

    # Get list of classes
    #classes = np.unique(ndvi_landsat_class)
    #classes = classes.tolist()
    # The mask returns a value of none in the classes. remove that
    classes = range(1, 6)

    # Plot your data
    fig, ax = plt.subplots(figsize=(12, 12))
    im = ax.imshow(ndvi_landsat_class, cmap=nbr_cmap)
    
    print(classes)

    ep.draw_legend(im_ax=im, classes=classes, titles=ndvi_cat_names)
    ax.set_title(
        "Landsat 8 - Normalized Difference Vegetation Index (NDVI) Classes",
        fontsize=14,
    )
    ax.set_axis_off()

    plt.tight_layout()
    plt.savefig(output)
    plt.close()
    
    #with rasterio.open(output, 'w', **meta) as out:
    #    out.write_band(1, ndvi_arr)
    
def evi(blue_path, red_path, nir_path, output, L=1):
    
    with rasterio.open(blue_path) as blue_band:
        blue = blue_band.read(1).astype('float32')
        blue[blue == 0] = np.nan
        
    with rasterio.open(red_path) as red_band:
        red = red_band.read(1).astype('float32')
        red[red == 0] = np.nan
                
    with rasterio.open(nir_path) as nir_band:
        nir = nir_band.read(1).astype('float32')
        nir[nir == 0] = np.nan
    
    arr_1 = (nir + 6*red - 7.5 * blue + L)
    arr_1[arr_1 == 0] = np.nan
    evi_arr = (nir - red) / arr_1
    evi_arr = (evi_arr + 1) * (2**15 - 1)
    
    # Plot the NDVI with a color scale
    plt.clf()
    plt.imshow(evi_arr, cmap='RdYlGn')
    plt.colorbar()
    #plt.show()
    plt.savefig(output)
    plt.close()
    
def savi(nir_path, red_path, output, L=0.5):
    
    with rasterio.open(red_path) as red_band:
        red = red_band.read(1).astype('float32')
        red[red == 0] = np.nan
        
    with rasterio.open(nir_path) as nir_band:
        nir = nir_band.read(1).astype('float32')
        nir[nir == 0] = np.nan
    
    #savi_arr = ((nir-red) / (nir + red + L)) * (1+L)
    #savi_arr = (savi_arr + 1) * (2**15 - 1)
    
    savi_arr =  (((nir - red) / (nir + red + 0.5)) * 1.5)
    
    # Plot the NDVI with a color scale
    plt.clf()
    plt.imshow(savi_arr, cmap='RdYlGn')
    plt.colorbar()
    #plt.show()
    plt.savefig(output)
    plt.close()

def ndwi(band3_path, band5_path, output):
    
    with rasterio.open(band3_path) as band3:
        band3_arr = band3.read(1).astype('float64')
        
    with rasterio.open(band5_path) as band5:
        band5_arr = band5.read(1).astype('float64')
    
    #ndwi_arr = (band3_arr - band5_arr) / (band3_arr + band5_arr)
    
    ndwi = es.normalized_diff(band3_arr, band5_arr) 
    # Create classes and apply to NDWI results
    ndwi_class_bins = [-np.inf, 0, 0.1, 0.25, 0.4, np.inf]
    ndwi_landsat_class = np.digitize(ndwi, ndwi_class_bins)

    # Apply the nodata mask to the newly classified NDWI data
    ndwi_landsat_class = np.ma.masked_where(
        np.ma.getmask(ndwi), ndwi_landsat_class
    )
    np.unique(ndwi_landsat_class)

    # Define color map
    ndwi_colors = ["gray", "lightgreen", "seagreen", "b", "darkblue"]
    ndwi_cmap = ListedColormap(ndwi_colors)

    # Define class names
    ndwi_cat_names = [
        "No Water",
        "Shallow Water",
        "Moderate Water",
        "Deep Water",
        "Very Deep Water",
    ]

    # Get list of classes
    #classes_ndwi = np.unique(ndwi_landsat_class)
    #classes_ndwi = classes_ndwi.tolist()
    # The mask returns a value of none in the classes. remove that
    classes_ndwi = range(1,6) #classes_ndwi[0:5]

    # Plot your data
    fig, ax = plt.subplots(figsize=(12, 12))
    im = ax.imshow(ndwi_landsat_class, cmap=ndwi_cmap)

    ep.draw_legend(im_ax=im, classes=classes_ndwi, titles=ndwi_cat_names)
    ax.set_title(
        "Landsat 8 - Normalized Difference Water Index (NDWI) Classes",
        fontsize=14,
    )
    ax.set_axis_off()

    plt.tight_layout()
    plt.savefig(output)
    plt.close()
    
    
# in order to display the rgb image the array values need to be normalized 
def normalize(array):
    '''normalizes numpy arrays into scale 0.0 - 1.0'''
    array_min, array_max = array.min(), array.max()
    return((array-array_min)/(array_max - array_min))

def to_rgb(path, image_name, output):
    
    blue_fp = os.path.join(path, '%s_B2.TIF' % image_name)
    green_fp = os.path.join(path, '%s_B3.TIF' % image_name)
    red_fp = os.path.join(path, '%s_B4.TIF' % image_name)

    blue_raster = rasterio.open(blue_fp)
    green_raster = rasterio.open(green_fp)
    red_raster = rasterio.open(red_fp)

    green_band = green_raster.read(1)
    blue_band = blue_raster.read(1)
    red_band = red_raster.read(1)

    # normalize the bands
    redn = normalize(red_band)
    greenn = normalize(green_band)
    bluen = normalize(blue_band)

    # create RGB natural color composite
    rgb = np.dstack((redn, greenn, bluen))
    
    #os.makedirs(output, exist_ok=True)

    # display the assembled true-color image
    fig, ax = plt.subplots(figsize = (60,60))
    # check out the color composite
    plt.imshow(rgb)
    plt.savefig(output)
     

def generate_indexes(path, image, output):
    os.makedirs(os.path.join(output, image), exist_ok=True)
    to_rgb(path, image, os.path.join(output, image, "rgb_" + image + ".png"))
    ndvi(os.path.join(path, image + "_B5.TIF"), os.path.join(path, image + "_B4.TIF"), os.path.join(output, image,"ndvi_" + image + ".png"))
    
    #evi(os.path.join(path, image + "_B2.TIF"), os.path.join(path, image + "_B4.TIF"), os.path.join(path, image + "_B5.TIF"), os.path.join(output, image,"evi_" + image + ".png"))
    
    #savi(os.path.join(path, image + "_B5.TIF"), os.path.join(path, image + "_B4.TIF"), os.path.join(output, image,"savi_" + image + ".png"))
    
    ndwi(os.path.join(path, image + "_B3.TIF"), os.path.join(path, image + "_B5.TIF"), os.path.join(output, image,"ndwi_" + image + ".png"))
    
    
parser = argparse.ArgumentParser(
                    prog='LandSat8ToRGB',
                    description='Creates a PNG from the LandSat8 bands.')

parser.add_argument('path')           # positional argument
parser.add_argument('imagename')           # positional argument
parser.add_argument('-o', '--output') 

args = parser.parse_args()
generate_indexes(args.path, args.imagename, output=args.output) 
