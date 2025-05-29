import numpy as np
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import os
from PIL import Image
import tifffile as tiff
import earthpy.spatial as es
import argparse
import os
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable

plt.style.use("paper.mplstyle")

pt = 1./72.27
jour_sizes = {"PRD": {"onecol": 246.*pt, "twocol": 510.*pt},
              "CQG": {"onecol": 374.*pt}, }
my_width = jour_sizes["PRD"]["twocol"]
golden = (1 + 5 ** 0.5) / 2
# golden = (1 + 5 ** 0.5) / 2.4 # you can modify here for a higher height if needed
plt.rcParams.update({
    'axes.labelsize': 14,       # Axis label font size
    'legend.fontsize': 14,      # Legend font size
    'xtick.labelsize': 12,      # X-axis tick label font size
})

# === Generic helpers ===

def load_band(path, dtype='float32', replace_zeros=True):
    with rasterio.open(path) as band:
        arr = band.read(1).astype(dtype)
        meta = band.meta
    if replace_zeros:
        arr[arr == 0] = np.nan
    return arr, meta

def save_geotiff(path, array, meta):
    with rasterio.open(path, 'w', **meta) as dst:
        dst.write_band(1, array)

def normalize_array(arr, a=0, b=255):
    return a + ((arr - np.nanmin(arr)) * (b - a)) / (np.nanmax(arr) - np.nanmin(arr))

def normalize(array):
    return (array - np.nanmin(array)) / (np.nanmax(array) - np.nanmin(array))

def create_index(band_a, band_b, formula="nd", L=1.0):
    if formula == "nd":  # Normalized Difference
        return es.normalized_diff(band_a, band_b)
    elif formula == "evi":
        return (band_a - band_b) / (band_a + 6 * band_b - 7.5 * band_b + L)
    elif formula == "savi":
        return ((band_a - band_b) / (band_a + band_b + L)) * (1 + L)
    else:
        raise ValueError(f"Unknown formula {formula}")

def plot_index(index, output, meta, colormap, bins, class_names=None, overlay=None):
    index[np.isnan(index)] = -1
    classified = np.digitize(index, bins)
    masked = np.ma.masked_where(np.ma.getmask(index), classified)
    px = 1 / plt.rcParams['figure.dpi']
    fig, ax = plt.subplots(figsize=(my_width, my_width / golden))
    ax.imshow(masked, cmap=ListedColormap(colormap))
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(output)
    plt.close()
    return masked


# === Vegetation/Water Indices ===

def compute_index_and_save(band_paths, output, formula, bins, colormap, tif=True, L=1.0):
    bands = [load_band(p)[0] for p in band_paths]
    meta = load_band(band_paths[0])[1]

    index = create_index(*bands, formula=formula, L=L)
    norm_index = normalize_array(index)

    if tif:
        save_geotiff(output.replace(".png", ".tif"), norm_index, meta)

    masked = plot_index(index, output, meta, colormap, bins)
    

    return norm_index, masked


# === Specific Index Wrappers ===

def ndvi(nir_path, red_path, output):
    return compute_index_and_save(
        [nir_path, red_path],
        output,
        formula="nd",
        bins=[-np.inf, 0, 0.1, 0.25, 0.4, np.inf],
        colormap=["gray", "y", "yellowgreen", "g", "darkgreen"]
    )

def savi(nir_path, red_path, output, L=0.5):
    return compute_index_and_save(
        [nir_path, red_path],
        output,
        formula="savi",
        bins=[-np.inf, 0, 0.1, 0.25, 0.4, np.inf],
        colormap=["gray", "y", "yellowgreen", "g", "darkgreen"],
        L=L
    )

def evi(blue_path, red_path, nir_path, output, L=1.0):
    blue = load_band(blue_path)[0]
    red = load_band(red_path)[0]
    nir = load_band(nir_path)[0]
    evi_arr = (nir - red) / (nir + 6 * red - 7.5 * blue + L)
    evi_arr = normalize_array(evi_arr)

    plt.imshow(evi_arr, cmap='RdYlGn')
    plt.colorbar()
    plt.savefig(output)
    plt.close()

    return evi_arr

def ndwi(green_path, nir_path, output, colormap):
    return compute_index_and_save(
        [green_path, nir_path],
        output,
        formula="nd",
        bins=[-np.inf, 0, 0.1, 0.25, 0.4, np.inf],
        colormap=colormap
    )

def false_color(band_r_path, band_g_path, band_b_path, output):
    band_r = load_band(band_r_path, replace_zeros=False)[0]
    band_g = load_band(band_g_path, replace_zeros=False)[0]
    band_b = load_band(band_b_path, replace_zeros=False)[0]

    rgb_stack = np.dstack([band_r, band_g, band_b])
    rgb_norm = normalize(rgb_stack) * 255
    Image.fromarray(rgb_norm.astype(np.uint8)).save(output)


# === Miscellaneous ===

def overlay_index_on_rgb(index_array, rgb, masked, out_path, width, height, extent, alpha=0.6):
    """Overlays a single-band index (e.g., NDVI) on an RGB image using a light-to-strong blue colormap."""

    # Normalize RGB
    rgb = rgb / 255.0

    # Normalize index to 0–1 for colormap
    index_norm = (index_array - np.nanmin(index_array)) / (np.nanmax(index_array) - np.nanmin(index_array))

    # Create consistent colormap
    cmap = LinearSegmentedColormap.from_list("light_to_strong_blue", ["#add8e6", "#00008b"])  # #00008b = darkblue

    # Apply colormap to normalized index (with alpha manually)
    index_colored = cmap(index_norm)
    index_colored[..., 3] = alpha  # Add uniform alpha

    # Mask: where to overlay
    mask = masked >= 2

    # Create RGBA image from RGB
    rgba_img = np.zeros((*rgb.shape[:2], 4), dtype='float32')
    rgba_img[..., :3] = rgb  # Copy RGB
    rgba_img[..., 3] = 0.6    # More transparent background

    # Overlay colored index where mask is True
    for i in range(3):  # Only R, G, B channels
        rgba_img[..., i] = np.where(
            mask,
            (1 - alpha) * rgba_img[..., i] + alpha * index_colored[..., i],
            rgba_img[..., i]
        )

    # Set alpha channel: more opaque where mask is True
    rgba_img[..., 3] = np.where(mask, 1.0, rgba_img[..., 3])  # 1.0 = fully opaque in masked areas

    # Normalize index values for colorbar
    norm = Normalize(vmin=np.nanmin(index_array), vmax=np.nanmax(index_array))

    px = 1 / plt.rcParams['figure.dpi']
    fig, ax = plt.subplots(figsize=(my_width, my_width / golden))

    # Show the overlay image
    ax.imshow(rgba_img, extent=extent)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(True, linestyle='--', alpha=0.5)

    # Create colorbar
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # Required dummy array
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.03, pad=0.04)
    cbar.set_label("Index Value")

    plt.tight_layout()
    plt.savefig(out_path.replace(".png", "_with_colorbar.png"), bbox_inches='tight', pad_inches=0, dpi=800)
    plt.close()


def overlay_index_on_rgb2(index_array, rgb, masked, out_path, width, height, extent, alpha=0.6):
    """Overlays a single-band index (e.g., NDVI) on an RGB image using a light-to-strong blue colormap."""

    # Normalize RGB
    rgb = rgb / 255.0

    # Normalize index to 0–1 for colormap
    index_norm = (index_array - np.nanmin(index_array)) / (np.nanmax(index_array) - np.nanmin(index_array))

    # Create consistent colormap
    cmap = LinearSegmentedColormap.from_list("light_to_strong_blue", ["#add8e6", "#00008b"])  # #00008b = darkblue

    # Apply colormap to normalized index (with alpha manually)
    index_colored = cmap(index_norm)
    index_colored[..., 3] = alpha  # Add uniform alpha

    # Mask: where to overlay
    mask = masked >= 2

    # Create RGBA image from RGB
    rgba_img = np.zeros((*rgb.shape[:2], 4), dtype='float32')
    rgba_img[..., :3] = rgb  # Copy RGB
    rgba_img[..., 3] = 0.5    # More transparent background

    # Overlay colored index where mask is True
    for i in range(3):  # Only R, G, B channels
        rgba_img[..., i] = np.where(
            mask,
            (1 - alpha) * rgba_img[..., i] + alpha * index_colored[..., i],
            rgba_img[..., i]
        )

    # Set alpha channel: more opaque where mask is True
    rgba_img[..., 3] = np.where(mask, 1.0, rgba_img[..., 3])  # 1.0 = fully opaque in masked areas

    # Normalize index values for colorbar
    norm = Normalize(vmin=np.nanmin(index_array), vmax=np.nanmax(index_array))

    # Get pixel dimensions of the image
    img_height, img_width = rgba_img.shape[:2]

    # Set figure size to match image dimensions exactly
    dpi = 300  # Use any consistent DPI
    figsize = (img_width / dpi, img_height / dpi)
    print(width, height)
    print(img_height, img_width)
    print(figsize)

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    # Show the overlay image
    ax.imshow(rgba_img, extent=extent, origin='upper', aspect='auto')
    #ax.set_axis_off()
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(True, linestyle='--', alpha=0.5)

    # # Create colorbar
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # Required dummy array
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.03, pad=0.04)
    cbar.set_label("Index Value")

    plt.tight_layout()
    plt.savefig(out_path.replace(".png", "_with_colorbar.png"), bbox_inches='tight', pad_inches=0, dpi=dpi)
    plt.close()

def get_mask(val, type='cloud'):
    bits = {'cloud': 3, 'shadow': 4, 'dilated_cloud': 1, 'cirrus': 2}
    return 0 if '{0:016b}'.format(val)[::-1][bits[type]] == '1' else 1

def to_rgb_high_contrast(path, image_name, output):
    blue = tiff.imread(os.path.join(path, f'{image_name}_B2.TIF'))
    green = tiff.imread(os.path.join(path, f'{image_name}_B3.TIF'))
    red = tiff.imread(os.path.join(path, f'{image_name}_B4.TIF'))
    rgb = np.stack([red, green, blue], axis=-1)
    rgb = np.clip(rgb*0.0000275-0.2, 0, 1)
    rgb = np.clip(rgb,0,0.3)/0.3
    rgb_norm = normalize(rgb) * 255
    Image.fromarray(rgb_norm.astype(np.uint8)).save(output)

    return rgb_norm


def generate_indexes(path, imagename, output=None):
    """Run all index generation functions based on band paths."""
    def make_path(band):
        return os.path.join(path, f"{imagename}_B{band}.TIF")
    
    def make_output(name):
        return os.path.join(output or path, f"{imagename}_{name}.png")

    rgb_path = make_output("RGB")

    meta = load_band(make_path(1))[1]

    
    #ndvi_img = ndvi(make_path(5), make_path(4), make_output("NDVI"))
    #savi_img = savi(make_path(5), make_path(4), make_output("SAVI"))
    ndwi_img, ndwi_masked = ndwi(make_path(3), make_path(5), make_output("NDWI"), ["gray", "lightskyblue", "skyblue", "b", "darkblue"])
    #evi_img = evi(make_path(2), make_path(4), make_path(5), make_output("EVI"))
    
    false_color(make_path(5), make_path(4), make_path(3), make_output("false_color"))
    rgb = to_rgb_high_contrast(path, imagename, rgb_path)

    # << NEW: Overlay masks
    #overlay_index_on_rgb(ndvi_img, rgb_path, make_output("RGB_NDVI_overlay"))
    #overlay_index_on_rgb(savi_img, rgb_path, make_output("RGB_SAVI_overlay"))

    extent = [-101.306667, -100.839748, 19.871558, 20.076776]


    overlay_index_on_rgb(ndwi_img, rgb, ndwi_masked, make_output("RGB_NDWI_overlay"), meta["width"], meta["height"], extent)
    #overlay_index_on_rgb(evi_img, rgb_path, make_output("RGB_EVI_overlay"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='LandSat8ToRGB',
        description='Creates vegetation and water index PNGs from LandSat 8 bands.')

    parser.add_argument('path', help='Directory containing band files')
    parser.add_argument('imagename', help='Base name of the image, e.g., LC08_L1TP_...')
    parser.add_argument('-o', '--output', help='Output directory for PNGs and TIFFs')

    args = parser.parse_args()
    generate_indexes(args.path, args.imagename, output=args.output)