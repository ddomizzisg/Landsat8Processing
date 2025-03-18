import rasterio
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import os
from os.path import isdir, join
import pandas as pd
from sklearn.linear_model import LinearRegression
import argparse


# in order to display the rgb image the array values need to be normalized 
def normalize(array):
    '''normalizes numpy arrays into scale 0.0 - 1.0'''
    array_min, array_max = array.min(), array.max()
    return((array-array_min)/(array_max - array_min))


def get_summary(input_path, output):
    
    output = join(input_path,output)
    
    os.makedirs(output, exist_ok=True)
    
    # Get dirs to images
    images_dirs = [join(input_path,d) for d in os.listdir(input_path) if isdir(join(input_path, d))]

    data_frame = pd.DataFrame(columns=["path","row","year", "month", "day", "water_area"])

    for d in images_dirs:
        print(d, output)
        if d == output:
            continue
        
        # get dir name
        dir_name = os.path.basename(d)
        
        #get year from dir name
        date_acq = dir_name.split("_")[3]
        year = int(date_acq[0:4])
        month = int(date_acq[4:6])
        day = int(date_acq[6:8])
        
        # get path and row
        path_row = dir_name.split("_")[2]
        path = int(path_row[0:3])
        row = int(path_row[3:6])

        # open the images
        path_to_image = join(d, f"ndwi_red_b7{dir_name}.tif")
        
        if os.path.exists(path_to_image):
        
            with rasterio.open(path_to_image) as src:
                image = src.read(1)
                meta = src.meta
            
            # show image
            water_threshold = 0.65
            image = normalize(image)
            #print("Uniques",np.unique(image))
            water_mask = image > water_threshold
            #print(water_mask)
            n_rows, n_cols = water_mask.shape
            #print(year, np.sum(water_mask), n_rows * n_cols)
            # Calculate the pixel area (in square meters)
            pixel_area = src.res[0] * src.res[1]
            print(path_to_image, len(water_mask[water_mask == True]))
            print(np.sum(water_mask), n_rows * n_cols)
            water_area = np.sum(water_mask) * 100 / (n_rows * n_cols) #* pixel_area #* 100 / (n_rows * n_cols)
            
            #convert to km^2
            #water_area = water_area / 1000000
            
            
            #data_frame = data_frame.append({"year": year, "month": month, "day": day, "water_area": np.sum(water_mask_2013) * pixel_area}, ignore_index=True)
            data_frame.loc[len(data_frame.index)] = [path, row, year, month, day, water_area]
        else:
            print("Not exists", path_to_image)
        
    data_frame.sort_values(by=["year", "month", "day"], inplace=True, ascending=[True, True, True])
    paths = data_frame["path"].unique()
    res = data_frame.groupby(["path","row",'year'], as_index=False)['water_area'].mean()

    for path in paths:
        res2 = res.loc[res['path'] == path]
        X = res2["year"].values.reshape(-1, 1)  # iloc[:, 1] is the column of X
        Y = res2["water_area"].values.reshape(-1, 1)  # df.iloc[:, 4] is the column of Y
        print(X)
        print(Y)
        linear_regressor = LinearRegression()
        linear_regressor.fit(X, Y)
        Y_pred = linear_regressor.predict(X)
        
        fig_width_cm = 29.7                               # A4 page
        fig_height_cm = 21  
        inches_per_cm = 1 / 2.54                         # Convert cm to inches
        fig_width = fig_width_cm * inches_per_cm         # width in inches
        fig_height = fig_height_cm * inches_per_cm       # height in inches
        fig_size = [fig_width, fig_height]
            
        plt.clf()

        
        fig = plt.figure()
        fig.set_size_inches(fig_size)
        #plt.rcParams.update({'font.size': 20})  # Adjust the font size as needed
        plt.scatter(X, Y,  label="Real Data")
        
        # Set the x and y ranges
        plt.xlim(min(X) - 1, max(X) + 1)  # Set x-axis range dynamically
        plt.ylim(min(Y) - 5, max(Y) + 5)  # Set y-axis range dynamically


        plt.plot(X, Y_pred, color='red', label="Linear Regression")
        plt.legend(loc="lower left", fontsize=20)
        plt.xlabel("Year", fontsize=24)
        plt.ylabel("Approximate Percentage of Water Area", fontsize=24)
        # Set tick parameters
        plt.tick_params(axis='both', which='major', labelsize=20)  # Tick labels font size

        #plt.show()
        fig.savefig(join(output,f"{path}_water_area.pdf"), bbox_inches='tight')

parser = argparse.ArgumentParser(
                    prog='LandSat8ToRGB',
                    description='Creates a summary from derivatives.')

parser.add_argument('path')           # positional argument
parser.add_argument('-o', '--output') 

args = parser.parse_args()
get_summary(args.path, args.output)