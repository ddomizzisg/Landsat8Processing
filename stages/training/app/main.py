import argparse
import os
import numpy as np
import rasterio
from skimage import exposure
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt


# Function to load Landsat 8 bands
def load_landsat_bands(file_path, image_name, bands):
    data = []
    for b in bands:
        band_path = os.path.join(file_path, '%s_B%d.TIF' % (image_name, b))
        with rasterio.open(band_path) as src:
            data.append(src.read(1))
    return np.stack(data, axis=-1)


# Function to enhance contrast using histogram equalization
def enhance_contrast(image):
    for i in range(image.shape[-1]):
        image[:, :, i] = exposure.equalize_hist(image[:, :, i])
    return image

# Function to preprocess data for clustering
def preprocess_for_clustering(data):
    # Flatten the data
    flat_data = data.reshape((-1, data.shape[-1]))
    
    # Standardize the features
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(flat_data)
    
    return scaled_data

# Function to apply Principal Component Analysis (PCA)
def apply_pca(data, n_components=3):
    pca = PCA(n_components=n_components)
    reduced_data = pca.fit_transform(data)
    return reduced_data

# Function to perform K-Means clustering
def perform_kmeans(data, n_clusters=2):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(data)
    return labels.reshape((landsat_bands.shape[0], landsat_bands.shape[1]))

# Function to display an image
def display_image(image, ax, title):
    ax.imshow(image)
    ax.set_title(title)
    ax.axis('off')


parser = argparse.ArgumentParser()
parser.add_argument('path')           # positional argument
parser.add_argument('imagename')           # positional argument
parser.add_argument('-o', '--output') 

args = parser.parse_args()
file = args.path
image_name = args.imagename
outputfile = args.output

# Define the bands to use (for simplicity, using only a few bands)
bands_to_use = [2, 3, 4, 5, 6, 7]

# Load Landsat 8 bands and reference land cover data
landsat_bands = load_landsat_bands(file, image_name, bands_to_use)

landsat_bands = enhance_contrast(landsat_bands)

# Preprocess data for clustering
preprocessed_data = preprocess_for_clustering(landsat_bands)

# Apply PCA to reduce dimensionality
reduced_data = apply_pca(preprocessed_data)


# Perform K-Means clustering
#urban_mask = perform_kmeans(reduced_data)

# Plot the results
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

# Display Landsat 8 image (RGB)
#isplay_image(landsat_bands[:, :, [3, 2, 1]], ax1, 'Landsat 8 Image (RGB)')

# Display PCA components

#print(reduced_data)
display_image(reduced_data, ax2, 'PCA Components')

# Display Urban Mask
#display_image(urban_mask, ax3, 'Urban Mask')

plt.savefig(os.path.join(outputfile, image_name))