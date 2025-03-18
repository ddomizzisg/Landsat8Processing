import numpy as np
import rasterio
import matplotlib.pyplot as plt
import os
import argparse
import earthpy.plot as ep
import earthpy.spatial as es
from PIL import Image
import tifffile as tiff


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
    
    # Save the NDVI image as TIFF
    with rasterio.open(output.replace(".png", ".tif"), 'w', **meta) as out:
        out.write_band(1, ndvi * 255)    
    
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

    #ep.draw_legend(im_ax=im, classes=classes, titles=ndvi_cat_names)
    ax.set_title(
        "Landsat 8 - Normalized Difference Vegetation Index (NDVI) Classes",
        fontsize=14,
    )
    ax.set_axis_off()

    plt.tight_layout()
    plt.savefig(output, dpi=600, bbox_inches='tight', pad_inches=0.1)
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
    plt.savefig(output, dpi=600, bbox_inches='tight', pad_inches=0.1)
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
    plt.savefig(output, dpi=600, bbox_inches='tight', pad_inches=0.1)
    plt.close()

def normalize_array(arr, a, b):
    min_array = np.min(arr)
    max_array = np.max(arr)
    
    # Applying the normalization formula
    normalized_arr = a + ((arr - min_array) * (b - a)) / (max_array - min_array)
    
    return normalized_arr

def ndwi_red(band4_path, band6_path, output):
        
    with rasterio.open(band4_path) as band4:
        meta = band4.meta
        band4_arr = band4.read(1).astype('float64')
        #band4_arr[band4_arr == 0] = np.nan
        
    with rasterio.open(band6_path) as band6:
        band6_arr = band6.read(1).astype('float64')
        #band6_arr[band6_arr == 0] = np.nan
    
    ndwi = es.normalized_diff(band4_arr, band6_arr)
    ndwi[np.isnan(ndwi)] = -1
    
    n_ndwi = normalize_array(ndwi, 0, 255)
    # Save the NDVI image as TIFF
    print("red",n_ndwi)
    print("red",n_ndwi.min())
    print("red",n_ndwi.max())
    with rasterio.open(output.replace(".png", ".tif"), 'w', **meta) as out:
        out.write_band(1, n_ndwi)  
    
    # Create classes and apply to NDWI results
    ndwi_class_bins = [-np.inf, 0, 0.1, 0.25, 0.4, np.inf]
    ndwi_landsat_class = np.digitize(ndwi, ndwi_class_bins)

    # Apply the nodata mask to the newly classified NDWI data
    ndwi_landsat_class = np.ma.masked_where(
        np.ma.getmask(ndwi), ndwi_landsat_class
    )
    np.unique(ndwi_landsat_class)

    # Define color map
    ndwi_colors = ["gray", "lightskyblue", "skyblue", "b", "darkblue"]
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

    print(meta)
    # Plot your data
    px = 1/plt.rcParams['figure.dpi']  # pixel in inches
    fig, ax = plt.subplots(figsize=(meta["width"]*px, meta["height"]*px))
    im = ax.imshow(ndwi_landsat_class, cmap=ndwi_cmap)

    #ep.draw_legend(im_ax=im, classes=classes_ndwi, titles=ndwi_cat_names)
    #ax.set_title(
    #    "Landsat 8 - Normalized Difference Water Index (NDWI) Classes",
    #    fontsize=14,
    #)
    ax.set_axis_off()

    plt.tight_layout()
    plt.savefig(output, dpi=600, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    
def ndwi_green(band3_path, band6_path, output):
        
    with rasterio.open(band3_path) as band3:
        meta = band3.meta
        band3_arr = band3.read(1).astype('float64')
        band3_arr[band3_arr == 0] = np.nan
        
    with rasterio.open(band6_path) as band6:
        band6_arr = band6.read(1).astype('float64')
        band6_arr[band6_arr == 0] = np.nan
        
    #print(band3_arr)
    
    #ndwi_arr = (band3_arr - band6_arr) / (band3_arr + band6_arr)
    ndwi = es.normalized_diff(band3_arr, band6_arr) 
    ndwi[np.isnan(ndwi)] = -1
    
    n_ndwi = normalize_array(ndwi, 0, 255)
    
    # Save the NDVI image as TIFF
    with rasterio.open(output.replace(".png", ".tif"), 'w', **meta) as out:
        out.write_band(1, n_ndwi) 
    
    # Create classes and apply to NDWI results
    ndwi_class_bins = [-np.inf, 0, 0.1, 0.25, 0.4, np.inf]
    ndwi_landsat_class = np.digitize(ndwi, ndwi_class_bins)

    # Apply the nodata mask to the newly classified NDWI data
    ndwi_landsat_class = np.ma.masked_where(
        np.ma.getmask(ndwi), ndwi_landsat_class
    )
    np.unique(ndwi_landsat_class)

    # Define color map
    ndwi_colors = ["gray", "lightskyblue", "skyblue", "b", "darkblue"]
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
    px = 1/plt.rcParams['figure.dpi']  # pixel in inches
    fig, ax = plt.subplots(figsize=(meta["width"]*px, meta["height"]*px))
    im = ax.imshow(ndwi_landsat_class, cmap=ndwi_cmap)

    #ep.draw_legend(im_ax=im, classes=classes_ndwi, titles=ndwi_cat_names)
    #ax.set_title(
    #    "Landsat 8 - Normalized Difference Water Index (NDWI) Classes",
    #    fontsize=14,
    #)
    ax.set_axis_off()
    
    plt.tight_layout()
    plt.savefig(output, dpi=600, bbox_inches='tight', pad_inches=0.1)

    plt.close()

def ndwi(band3_path, band5_path, output):
    
    with rasterio.open(band3_path) as band3:
        band3_arr = band3.read(1).astype('float64')
        meta = band3.meta
        
    with rasterio.open(band5_path) as band5:
        band5_arr = band5.read(1).astype('float64')
    
    #ndwi_arr = (band3_arr - band5_arr) / (band3_arr + band5_arr)
    
    ndwi = es.normalized_diff(band3_arr, band5_arr) 
    ndwi[np.isnan(ndwi)] = -1
    
    n_ndwi = normalize_array(ndwi, 0, 255)
    
    # Create classes and apply to NDWI results
    ndwi_class_bins = [-np.inf, 0, 0.1, 0.25, 0.4, np.inf]
    ndwi_landsat_class = np.digitize(ndwi, ndwi_class_bins)

    # Apply the nodata mask to the newly classified NDWI data
    ndwi_landsat_class = np.ma.masked_where(
        np.ma.getmask(ndwi), ndwi_landsat_class
    )
    np.unique(ndwi_landsat_class)

    # Define color map
    ndwi_colors = ["gray", "lightskyblue", "skyblue", "b", "darkblue"]
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
    px = 1/plt.rcParams['figure.dpi']  # pixel in inches
    fig, ax = plt.subplots(figsize=(meta["width"]*px, meta["height"]*px))
    im = ax.imshow(ndwi_landsat_class, cmap=ndwi_cmap)

    #ep.draw_legend(im_ax=im, classes=classes_ndwi, titles=ndwi_cat_names)
    #ax.set_title(
    #    "Landsat 8 - Normalized Difference Water Index (NDWI) Classes",
    #    fontsize=14,
    #)
    ax.set_axis_off()

    plt.tight_layout()
    plt.savefig(output, dpi=600, bbox_inches='tight', pad_inches=0.1)
    plt.close()

def false_color(band7_path, band6_path, band4_path, output):
    with rasterio.open(band7_path) as band7:
        band7_arr = band7.read(1).astype('float64')
        
    with rasterio.open(band6_path) as band6:
        band6_arr = band6.read(1).astype('float64')
        
    with rasterio.open(band4_path) as band4:
        band4_arr = band4.read(1).astype('float64')
        
    # Stack and scale bands
    false_color = np.dstack((band7_arr, band6_arr, band4_arr))
    
    #normalize between 0 and 255
    false_color = normalize(false_color) * 255
    
    print(false_color.max())
    
    im = Image.fromarray((false_color).astype(np.uint8))
    im.save(output, quality=95)
    

def get_mask(val,type='cloud'):
    
    """Get mask for a specific cover type"""

    # convert to binary
    bin_ = '{0:016b}'.format(val)

    # reverse string
    str_bin = str(bin_)[::-1]

    # get bit for cover type
    bits = {'cloud':3,'shadow':4,'dilated_cloud':1,'cirrus':2}
    bit = str_bin[bits[type]]

    if bit == '1':
        return 0 # cover
    else:
        return 1 # no cover

def to_rgb_high_contrast(path, image_name, output, upscale_factor=4):
    blue_fp = os.path.join(path, '%s_B2.TIF' % image_name)
    green_fp = os.path.join(path, '%s_B3.TIF' % image_name)
    red_fp = os.path.join(path, '%s_B4.TIF' % image_name)
        
    with rasterio.open(blue_fp) as blue_raster, \
         rasterio.open(green_fp) as green_raster, \
         rasterio.open(red_fp) as red_raster:

        blue_band = blue_raster.read(1)
        green_band = green_raster.read(1)
        red_band = red_raster.read(1)

        # Normalize bands
        redn = normalize(red_band)
        greenn = normalize(green_band)
        bluen = normalize(blue_band)

        # Create RGB composite
        rgb = np.dstack((redn, greenn, bluen))
        rgb = (rgb * 255).astype(np.uint8)  # Convert to 8-bit

        # Convert to Image and upscale
        im = Image.fromarray(rgb)
        im_upscaled = upscale_image(im, upscale_factor)
        
        # Save with high quality
        im_upscaled.save(output, quality=100)

def normalize(array):
    """ Normalize array values to range 0-1 """
    return (array - array.min()) / (array.max() - array.min())

def upscale_image(img, scale_factor=4):
    """ Upscale an image using high-quality LANCZOS resampling """
    width, height = img.size
    new_size = (width * scale_factor, height * scale_factor)
    return img.resize(new_size, Image.LANCZOS)

def to_rgb(path, image_name, output, upscale_factor=4):
    # Open bands
    blue_fp = os.path.join(path, f"{image_name}_B2.TIF")
    green_fp = os.path.join(path, f"{image_name}_B3.TIF")
    red_fp = os.path.join(path, f"{image_name}_B4.TIF")
    
    with rasterio.open(blue_fp) as blue_raster, \
         rasterio.open(green_fp) as green_raster, \
         rasterio.open(red_fp) as red_raster:

        blue_band = blue_raster.read(1)
        green_band = green_raster.read(1)
        red_band = red_raster.read(1)

        # Normalize bands
        redn = normalize(red_band)
        greenn = normalize(green_band)
        bluen = normalize(blue_band)

        # Create RGB composite
        rgb = np.dstack((redn, greenn, bluen))
        rgb = (rgb * 255).astype(np.uint8)  # Convert to 8-bit

        # Convert to Image and upscale
        im = Image.fromarray(rgb)
        im_upscaled = upscale_image(im, upscale_factor)
        
        # Save with high quality
        im_upscaled.save(output, quality=100)
    
    
def remove_clouds(path, image_name, output):
    blue_fp = os.path.join(path, '%s_B2.TIF' % image_name)
    green_fp = os.path.join(path, '%s_B3.TIF' % image_name)
    red_fp = os.path.join(path, '%s_B4.TIF' % image_name)
    
    # Load Blue (B2), Green (B3) and Red (B4) bands
    B2 = tiff.imread(blue_fp)
    B3 = tiff.imread(green_fp)
    B4 = tiff.imread(red_fp)
        
    # Stack and scale bands
    RGB = np.dstack((B4, B3, B2))
    RGB = np.clip(RGB*0.0000275-0.2, 0, 1)

    # Clip to enhance contrast
    RGB = np.clip(RGB,0,0.3)/0.3
    
    QA_path = os.path.join(path, '%s_QA_PIXEL.TIF' % image_name)
    QA = tiff.imread(QA_path)
    QA = np.array(QA)
    
    # Get masks
    print("Getting masks")
    print("getting cloud mask")
    cloud_mask = np.vectorize(get_mask)(QA,type='cloud')
    """print("getting shadow mask")
    shadow_mask = np.vectorize(get_mask)(QA,type='shadow')
    print("getting dilated cloud mask")
    dilated_cloud_mask = np.vectorize(get_mask)(QA,type='dilated_cloud')
    print("getting cirrus mask")
    cirrus_mask = np.vectorize(get_mask)(QA,type='cirrus')
    
    # color for each cover type
    colors = np.array([[247, 2, 7],
                        [201, 116, 247],
                        [0, 234, 255],
                        [3, 252, 53]])/255

    masks = [cloud_mask, shadow_mask, dilated_cloud_mask, cirrus_mask]
    
    #fig, ax = plt.subplots(figsize=(20, 10))
    #ax.imshow(RGB)
    #plt.show()"""
    
    # Remove clouds
    rm_clouds = RGB*cloud_mask[:, :, np.newaxis]
    im = Image.fromarray((rm_clouds * 255).astype(np.uint8))
    im.save(output)
    

def generate_indexes(path, image, output):
    print("path", path)
    
    #remove last slash if exists
    if path[-1] == "/":
        path = path[:-1]
    
    dir_name = os.path.basename(path)
    print("aa",image)
    os.makedirs(os.path.join(output, dir_name), exist_ok=True)
    #remove_clouds(path, image, os.path.join(output, image, "clouds_removed_" + image + ".png"))
    to_rgb(path, image, os.path.join(output, dir_name, "rgb_" + image + ".png"))
    to_rgb_high_contrast(path, image, os.path.join(output, dir_name, "rgb_high_contrast_" + image + ".png"))
    ndvi(os.path.join(path, image + "_B5.TIF"), os.path.join(path, image + "_B4.TIF"), os.path.join(output, dir_name,"ndvi_" + image + ".png"))
    
    evi(os.path.join(path, image + "_B2.TIF"), os.path.join(path, image + "_B4.TIF"), os.path.join(path, image + "_B5.TIF"), os.path.join(output, image,"evi_" + image + ".png"))
    
    savi(os.path.join(path, image + "_B5.TIF"), os.path.join(path, image + "_B4.TIF"), os.path.join(output, image,"savi_" + image + ".png"))
    ndwi_green(os.path.join(path, image + "_B3.TIF"), os.path.join(path, image + "_B7.TIF"), os.path.join(output, dir_name,"ndwi_green_b7" + image + ".png"))
    
    ndwi_red(os.path.join(path, image + "_B4.TIF"), os.path.join(path, image + "_B7.TIF"), os.path.join(output, dir_name,"ndwi_red_b7" + image + ".png"))
    
    ndwi_green(os.path.join(path, image + "_B3.TIF"), os.path.join(path, image + "_B6.TIF"), os.path.join(output, dir_name,"ndwi_green_b6" + image + ".png"))
    
    ndwi_red(os.path.join(path, image + "_B4.TIF"), os.path.join(path, image + "_B6.TIF"), os.path.join(output, dir_name,"ndwi_red_b6" + image + ".png"))
    
    ndwi(os.path.join(path, image + "_B4.TIF"), os.path.join(path, image + "_B5.TIF"), os.path.join(output, dir_name,"ndwi_b4" + image + ".png"))
    ndwi(os.path.join(path, image + "_B3.TIF"), os.path.join(path, image + "_B5.TIF"), os.path.join(output, dir_name,"ndwi_b4" + image + ".png"))
    false_color(os.path.join(path, image + "_B7.TIF"), os.path.join(path, image + "_B6.TIF"), os.path.join(path, image + "_B4.TIF"), os.path.join(output, image,"false_color_" + image + ".png"))
    
parser = argparse.ArgumentParser(
                    prog='LandSat8ToRGB',
                    description='Creates a PNG from the LandSat8 bands.')

parser.add_argument('path')           # positional argument
parser.add_argument('imagename')           # positional argument
parser.add_argument('-o', '--output') 

args = parser.parse_args()
generate_indexes(args.path, args.imagename, output=args.output) 
