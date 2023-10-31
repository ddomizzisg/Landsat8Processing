# GDAL_Python3
Open Source (geographic) data handling scripts, written in Python 3.4 and 3.5 with a focus on time series analysis

Last tested (March 2016) with [GDAL 2.0.2](http://www.gisinternals.com/query.html?content=filelist&file=release-1800-x64-gdal-1-11-3-mapserver-6-4-2.zip)

Functions.py is needed by many of these scripts, as it contains basic functions repeatedly required


### best_Comb.py

Uses the files created by best_Reg.py and returns a value for each pixel that represents the *best* monthly combination

Largest values are returned for linear regression p-Value, r-Value and Mann-Kendall p-Value.   
Smallest values are returned for linear regression slope, intercept, standard error and additionally r-value

The script assigns a shorter integer (i) to each month combination (e.g. 101112 for Oct,Nov,Dec is value 23). This assignment depends on the number of
month combinations used and may vary as such. Therefore an *_Info.txt* files is created, storing the relation between each i and original month combination.

The i is the value that represents the best month combination in the output rasters.

### best_Reg.py

Calculate pixel-based linear regressions for many different month/season combinations

Input is a folder containing monthly rasters potentially spanning over several years (file naming scheme: 1999_03.tif)
Script calculates pixel-based linear regressions for many different month/season combinations. 
The script physically saves the output of each combinatio to HDD. If it is re-run, it will check for existing files, so already exisiting combinations are
ignored in following runs

This is done within one year and also spanning into the next year (e.g. for winter)

This allows to handle seasons not as static entities, but can help to find better combinations (e.g. winter is often represented as DJF, but may show
better results as NDJF or NDJFM)

### Functions.py

Crucial file as many of the other scripts call functions from within, so be sure to put it in the *PYTHONPATH*   

Includes:
* **chkdir** and **chkdir2** handle directory checking, deletion and creation
* **getLargVal** multiple same dimension arrays are the input - output is one array with the largest respective value at each data point
* **array_to_raster** and **array_to_raster_noTi** create GeoTiffs from numpy arrays, either using an exisiting GeoTiff as a blueprint or with manual attirbute input
* **linReg** caluclates linear regression parameters and the Mann-Kendall trend test for each pixel in a stack of rasters (regression between values an time)
* **linReg2** similar to linReg, but instead of Y-axis being time steps, two different rasters stacks are correlated on a pixel by pixel basis. 
	This script is flexible, works with arrays or GeoTiffs as input, and should work even for stacks that differ in extent, resolution or coordinate system
* **tiffToarray** converts a folder of raster files into arrays and returns a list of arrays (inverse function to *array_to_raster*)
* **singleTifToArray** converts only one raster file into an array and returns the array
* **mk_test** calculates the Mann-Kendall trend test and returns h and p value (originally adopted from http://www.ambhas.com/codes/statlib.py but changed 
	to use numpy matrices and other minor changes -> script is now about 35x faster than the original)
* **hdfTOtif** convert HDF files to GeoTiff format, quite specific to certain NDVI data, as DN values are converted to NDVI in the process
* **BILtoTIF** convert BIL files to GeoTiff format
* **extXLS** read rows from Excel file and return it as a list
* **get_spatialref** small tool to import the Spatial Reference from an EPSG Code
* **my_intersect** calculate new extent from intersect of two rasters
* **reproject_dataset** creates a physical copy of the reprojected raster and return its path as a string
* **addCS** assign a coordinate system to a TIFF file
* **histo** creates a histogram of a raster dataset


### MiniScripts.py


A collection of small scripts. In contrast to Functions.py these are mostly run on their own and are not called from other scripts.

Includes:
* conversion of a folder of HDF files to the GeoTiff format
* handling of nested zip files (specific for data from www.vito-eodata.be)
* copy the content of many folders into one (useful when data is packed in folder by month, though all monthly files are required to be in one folder)
* inverse case, copy content of one folder to many (here specifically monthly folders)
* rename files (first to last) to fit the *Year_Month.tif* format used in some of the other scripts
* convert BIL files in ZIP archives to GeoTiffs
* Text file merging
* change a number string representing months into month names (number strings may be a result of *best_Comb.py*)


### netCDFtoTiff.py

Converts 3D netCDF files (X,Y,Z = lon, lat, value) into multiple single GeoTiff rasters. Requires Functions.py and the [netCDF4](https://netcdf4-python.googlecode.com/svn/trunk/docs/netCDF4-module.html) module

Extent and pixel size must be manually changed, all else is extracted automatically.   
The script returns files that are numbered in continuous order (*1.tif, 2.tif, 3.tif...*)


### trend_stats.py

Uses the input of annual rasters (inFol) and monthly rasters stored in sub-folders by month in inFol2. Returns pixel based coefficients from the 
linear regression on a monthly and annual basis



