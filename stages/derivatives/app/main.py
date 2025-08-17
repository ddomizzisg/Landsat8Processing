import numpy as np
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import os
from PIL import Image
import tifffile as tiff
import earthpy.spatial as es
import argparse
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable

# Landsat 8 band reminder:
# B2=Blue, B3=Green, B4=Red, B5=NIR, B6=SWIR1, B7=SWIR2

pt = 1./72.27
jour_sizes = {"PRD": {"onecol": 246.*pt, "twocol": 510.*pt}, "CQG": {"onecol": 374.*pt}}
my_width = jour_sizes["PRD"]["twocol"]
golden = (1 + 5 ** 0.5) / 2
plt.rcParams.update({
    'axes.labelsize': 14,
    'legend.fontsize': 14,
    'xtick.labelsize': 12,
})

# === Generic helpers ===

def load_band(path, dtype='float32', replace_zeros=True):
    with rasterio.open(path) as band:
        arr = band.read(1).astype(dtype)
        meta = band.meta.copy()
    if replace_zeros:
        arr[arr == 0] = np.nan
    return arr, meta

def save_geotiff(path, array, meta):
    meta = meta.copy()
    meta.update(count=1, dtype='float32')
    with rasterio.open(path, 'w', **meta) as dst:
        dst.write(array.astype('float32'), 1)

def normalize_array(arr, a=0, b=255):
    amin, amax = np.nanmin(arr), np.nanmax(arr)
    if np.isclose(amax, amin):
        return np.zeros_like(arr) + a
    return a + ((arr - amin) * (b - a)) / (amax - amin)

def normalize(array):
    amin, amax = np.nanmin(array), np.nanmax(array)
    if np.isclose(amax, amin):
        return np.zeros_like(array)
    return (array - amin) / (amax - amin)

def create_index(band_a, band_b, formula="nd", L=1.0):
    if formula == "nd":  # Normalized Difference: (A-B)/(A+B)
        return es.normalized_diff(band_a, band_b)
    elif formula == "savi":
        return ((band_a - band_b) / (band_a + band_b + L)) * (1 + L)
    else:
        raise ValueError(f"Unknown formula {formula}")

def plot_index(index, output, meta, colormap, bins, class_names=None, overlay=None):
    idx = index.copy()
    nan_mask = np.isnan(idx)
    # push NaNs to a dedicated bin by temporarily filling with very small number
    idx[nan_mask] = -1e9
    classified = np.digitize(idx, bins)
    classified[nan_mask] = 0  # 0 = NoData
    cmap = ListedColormap(colormap)
    px = 1 / plt.rcParams['figure.dpi']
    fig, ax = plt.subplots(figsize=(my_width, my_width / golden))
    ax.imshow(classified, cmap=cmap)
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(output, dpi=300)
    plt.close()
    return classified

# === Vegetation/Water Indices ===

def compute_index_and_save(band_paths, output, formula, bins, colormap, tif=True, L=1.0):
    bands = [load_band(p)[0] for p in band_paths]
    meta = load_band(band_paths[0])[1]
    index = create_index(*bands, formula=formula, L=L)
    norm_index = normalize_array(index)

    if tif:
        save_geotiff(output.replace(".png", ".tif"), norm_index, meta)

    masked = plot_index(index, output, meta, colormap, bins)
    return index, masked, meta

def ndvi(nir_path, red_path, output):
    return compute_index_and_save(
        [nir_path, red_path],
        output,
        formula="nd",
        bins=[-np.inf, 0, 0.1, 0.25, 0.4, np.inf],
        colormap=["black", "gray", "y", "yellowgreen", "g", "darkgreen"]
    )

def savi(nir_path, red_path, output, L=0.5):
    return compute_index_and_save(
        [nir_path, red_path],
        output,
        formula="savi",
        bins=[-np.inf, 0, 0.1, 0.25, 0.4, np.inf],
        colormap=["black", "gray", "y", "yellowgreen", "g", "darkgreen"],
        L=L
    )

def evi(blue_path, red_path, nir_path, output, L=1.0):
    blue = load_band(blue_path)[0]
    red = load_band(red_path)[0]
    nir = load_band(nir_path)[0]
    evi_arr = (nir - red) / (nir + 6 * red - 7.5 * blue + L)
    evi_norm = normalize_array(evi_arr)
    plt.imshow(evi_norm, cmap='RdYlGn')
    plt.colorbar()
    plt.savefig(output, dpi=300)
    plt.close()
    return evi_arr

def ndwi(green_path, nir_path, output, colormap):
    return compute_index_and_save(
        [green_path, nir_path],
        output,
        formula="nd",
        bins=[-np.inf, -0.05, 0, 0.1, 0.25, np.inf],
        colormap=colormap
    )

# === Urban / Built-up Indices ===

def mndwi(green_path, swir1_path, output):
    """Modified NDWI = (Green - SWIR1)/(Green + SWIR1) -> better water discrimination in urban scenes."""
    green = load_band(green_path)[0]
    swir1 = load_band(swir1_path)[0]
    idx = es.normalized_diff(green, swir1)
    meta = load_band(green_path)[1]
    bins = [-np.inf, -0.05, 0, 0.1, 0.25, np.inf]
    colors = ["black", "lightgray", "lightskyblue", "deepskyblue", "b", "navy"]
    masked = plot_index(idx, output, meta, colors, bins)
    save_geotiff(output.replace(".png", ".tif"), idx, meta)
    return idx, masked, meta

def ndbi(swir1_path, nir_path, output):
    """Normalized Difference Built-up Index = (SWIR1 - NIR)/(SWIR1 + NIR)"""
    swir1 = load_band(swir1_path)[0]
    nir = load_band(nir_path)[0]
    idx = es.normalized_diff(swir1, nir)
    meta = load_band(swir1_path)[1]
    # Classes: NoData / strong negative / slight negative / neutral / built-up / very built-up
    bins = [-np.inf, -0.2, -0.05, 0.05, 0.2, np.inf]
    colors = ["black", "darkseagreen", "palegreen", "wheat", "orange", "red"]
    masked = plot_index(idx, output, meta, colors, bins)
    save_geotiff(output.replace(".png", ".tif"), idx, meta)
    return idx, masked, meta

def built_up_mask(ndbi_arr, ndvi_arr, mndwi_arr,
                  ndbi_thr=0.0, ndvi_thr=0.3, mndwi_thr=0.0):
    """
    Robust built-up boolean mask:
      - NDBI > 0 (built-up tends to be positive)
      - NDVI < 0.3 (suppress vegetation)
      - MNDWI < 0 (suppress water)
    """
    return (ndbi_arr > ndbi_thr) & (ndvi_arr < ndvi_thr) & (mndwi_arr < mndwi_thr)

def false_color(band_r_path, band_g_path, band_b_path, output):
    band_r = load_band(band_r_path, replace_zeros=False)[0]
    band_g = load_band(band_g_path, replace_zeros=False)[0]
    band_b = load_band(band_b_path, replace_zeros=False)[0]
    rgb_stack = np.dstack([band_r, band_g, band_b])
    rgb_norm = normalize(rgb_stack) * 255
    Image.fromarray(rgb_norm.astype(np.uint8)).save(output)

# === Miscellaneous (overlay) ===

def overlay_index_on_rgb(index_array, rgb, masked, out_path, width, height, extent, alpha=0.6):
    rgb = rgb / 255.0
    idx = index_array.copy()
    idx_norm = (idx - np.nanmin(idx)) / (np.nanmax(idx) - np.nanmin(idx) + 1e-12)
    cmap = LinearSegmentedColormap.from_list("light_to_strong_blue", ["#add8e6", "#00008b"])
    index_colored = cmap(idx_norm)
    index_colored[..., 3] = alpha

    mask = masked >= 2  # show from class 2 upwards
    rgba_img = np.zeros((*rgb.shape[:2], 4), dtype='float32')
    rgba_img[..., :3] = rgb
    rgba_img[..., 3] = 0.6

    for i in range(3):
        rgba_img[..., i] = np.where(mask,
                                    (1 - alpha) * rgba_img[..., i] + alpha * index_colored[..., i],
                                    rgba_img[..., i])
    rgba_img[..., 3] = np.where(mask, 1.0, rgba_img[..., 3])

    norm = Normalize(vmin=np.nanmin(index_array), vmax=np.nanmax(index_array))
    fig, ax = plt.subplots(figsize=(my_width, my_width / golden))
    ax.imshow(rgba_img, extent=extent)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(True, linestyle='--', alpha=0.5)
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.03, pad=0.04)
    cbar.set_label("Index Value")
    plt.tight_layout()
    plt.savefig(out_path.replace(".png", "_with_colorbar.png"), bbox_inches='tight', pad_inches=0, dpi=800)
    plt.close()

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

# === Change detection helpers (ΔNDBI) ===

def ndbi_change(ndbi_before, ndbi_after, thr=0.05):
    """
    Delta NDBI map and classes:
      class 0 = NoData
      class 1 = Built-up loss (ΔNDBI <= -thr)
      class 2 = Stable (|ΔNDBI| < thr)
      class 3 = Built-up growth (ΔNDBI >= thr)
    """
    delta = ndbi_after - ndbi_before
    cls = np.zeros_like(delta, dtype=np.uint8)
    cls[np.isnan(delta)] = 0
    cls[(~np.isnan(delta)) & (delta <= -thr)] = 1
    cls[(~np.isnan(delta)) & (np.abs(delta) < thr)] = 2
    cls[(~np.isnan(delta)) & (delta >= thr)] = 3
    return delta, cls

def save_change_map(cls, meta, out_png, out_tif):
    colors = ["black", "royalblue", "lightgray", "crimson"]  # NoData / Loss / Stable / Growth
    bins = [-np.inf, 0.5, 1.5, 2.5, np.inf]
    px = 1 / plt.rcParams['figure.dpi']
    fig, ax = plt.subplots(figsize=(my_width, my_width / golden))
    ax.imshow(cls, cmap=ListedColormap(colors))
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.close()
    save_geotiff(out_tif, cls.astype('float32'), meta)

# === Pipeline ===

def generate_indexes(path, imagename, output=None, extent=None):
    """Run index generation functions based on band paths."""
    def make_path(band):
        return os.path.join(path, f"{imagename}_B{band}.TIF")
    def make_output(name):
        return os.path.join(output or path, f"{imagename}_{name}.png")

    rgb_path = make_output("RGB")
    meta = load_band(make_path(1))[1]

    # Indices
    ndvi_img, ndvi_masked, _ = ndvi(make_path(5), make_path(4), make_output("NDVI"))
    mndwi_img, mndwi_masked, _ = mndwi(make_path(3), make_path(6), make_output("MNDWI"))
    ndbi_img, ndbi_masked, _ = ndbi(make_path(6), make_path(5), make_output("NDBI"))

    # Built-up mask (robust)
    built_mask = built_up_mask(ndbi_img, ndvi_img, mndwi_img, ndbi_thr=0.0, ndvi_thr=0.3, mndwi_thr=0.0)
    built_mask_png = make_output("BUILT_MASK")
    fig, ax = plt.subplots(figsize=(my_width, my_width / golden))
    ax.imshow(built_mask, cmap=ListedColormap(["black", "white"]))
    ax.set_title("Built-up mask")
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(built_mask_png, dpi=300)
    plt.close()
    save_geotiff(built_mask_png.replace(".png", ".tif"), built_mask.astype('float32'), meta)

    # Visuals
    false_color(make_path(5), make_path(4), make_path(3), make_output("false_color"))
    rgb = to_rgb_high_contrast(path, imagename, rgb_path)

    # If you know geospatial extent, overlay indices (optional)
    if extent is not None:
        overlay_index_on_rgb(ndbi_img, rgb, ndbi_masked, make_output("RGB_NDBI_overlay"),
                             meta.get("width"), meta.get("height"), extent)

    return {
        "ndvi": ndvi_img,
        "mndwi": mndwi_img,
        "ndbi": ndbi_img,
        "built_mask": built_mask
    }

def generate_change(path_before, name_before, path_after, name_after, output=None):
    """Compute ΔNDBI change map between two scenes (same area, coregistered)."""
    def m(o, n): return os.path.join(o or path_after, f"{n}")
    # Load NDBI for both dates
    before_ndbi, _, meta_b = ndbi(os.path.join(path_before, f"{name_before}_B6.TIF"),
                                  os.path.join(path_before, f"{name_before}_B5.TIF"),
                                  m(output, f"{name_before}_NDBI.png"))
    after_ndbi, _, meta_a = ndbi(os.path.join(path_after, f"{name_after}_B6.TIF"),
                                 os.path.join(path_after, f"{name_after}_B5.TIF"),
                                 m(output, f"{name_after}_NDBI.png"))

    # Align meta (assumes same grid; if not, resample beforehand)
    meta = meta_a

    delta, cls = ndbi_change(before_ndbi, after_ndbi, thr=0.05)
    out_png = m(output, f"{name_before}_to_{name_after}_NDBI_CHANGE.png")
    out_tif = m(output, f"{name_before}_to_{name_after}_NDBI_CHANGE.tif")
    save_change_map(cls, meta, out_png, out_tif)
    return delta, cls

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Landsat8Indices',
        description='Creates vegetation, water, and urban indices from Landsat 8 bands.')
    parser.add_argument('path', help='Directory containing band files')
    parser.add_argument('imagename', help='Base name of the image, e.g., LC08_L1TP_...')
    parser.add_argument('-o', '--output', help='Output directory for PNGs and TIFFs')
    parser.add_argument('--extent', nargs=4, type=float, metavar=("xmin","xmax","ymin","ymax"),
                        help="Geospatial extent for overlays (lon/lat).")
    # Optional change detection
    parser.add_argument('--before', nargs=2, metavar=("PATH", "IMAGENAME"),
                        help="Before scene (path and basename) for ΔNDBI change map")
    parser.add_argument('--after', nargs=2, metavar=("PATH", "IMAGENAME"),
                        help="After scene (path and basename) for ΔNDBI change map")
    args = parser.parse_args()

    # Per-scene indices + built-up mask
    generate_indexes(args.path, args.imagename, output=args.output,
                     extent=tuple(args.extent) if args.extent else None)

    # Optional change detection
    if args.before and args.after:
        generate_change(args.before[0], args.before[1],
                        args.after[0], args.after[1],
                        output=args.output)
