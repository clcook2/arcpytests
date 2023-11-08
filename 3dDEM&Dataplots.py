import geopandas as gpd
import numpy as np
import numpy.ma as ma
import rasterio
from rasterio.transform import from_origin
from rasterio.enums import Resampling
from rasterio.plot import show
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image

# Load DEM data
dem_path = r"C:\Users\clcook2\Documents\GLRC_TobaccoRiver_2023\20230802_TobaccoRiver_M1_Morning_DEM_DepthCorr1\20230802_TobaccoRiver_M1_Morning_DEM_DepthCorr1.tif"
dem_data = rasterio.open(dem_path)
dem_array = dem_data.read(1, masked=True)
dem_width, dem_height = dem_array.shape
print(dem_width, dem_height)
#dem_masked = np.ma.masked_where(dem_array == -9999,
#                          dem_array,
#                          copy=True)
#dem_array == dem_masked

# Load shapefile data
shapefile_path = r"C:\Users\clcook2\Documents\GLRC_TobaccoRiver_2023\3DviewFiles\GPS\TobaccoRiver_812023_GPSpts_FINAL.shp"

gdf = gpd.read_file(shapefile_path)

# Load TIFF image
tiff_path = r"C:\Users\clcook2\Documents\GLRC_TobaccoRiver_2023\3DviewFiles\Ortho\test.tif"
#tiff_image = Image.open(tiff_path)
#tiff_image = rasterio.open(tiff_path)
#tiff_array = tiff_image.read(1, masked=True)
#tiff_image = ma.resize(tiff_array, (dem_array.shape[1], dem_array.shape[0]))
#tiff_resize = tiff_array.resize((dem_width, dem_height), Image.LANCZOS)
with rasterio.open(tiff_path) as tiff_data:
    # Resize TIFF image to match DEM dimensions using rasterio
    tiff_resized = tiff_data.read(
        out_shape=(tiff_data.count, dem_array.shape[0], dem_array.shape[1]),
        resampling=Resampling.bilinear
    )

# Create 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot DEM surface
x = range(dem_array.shape[1])
y = range(dem_array.shape[0])
X, Y = np.meshgrid(x, y)
ax.plot_surface(X, Y, dem_array, cmap='terrain', linewidth=0, antialiased=False, shade=True, alpha=0.7,
                facecolors=tiff_resized)

# Plot 3D shapefile overlay
for geom in gdf['geometry']:
    if geom.geom_type == 'Polygon':
        xs, ys = geom.exterior.xy
        zs = dem_data.sample([(x, y) for x, y in zip(xs, ys)])
        ax.plot(xs, ys, zs, color='red', linewidth=2)
    elif geom.geom_type == 'MultiPolygon':
        for polygon in geom:
            xs, ys = polygon.exterior.xy
            zs = dem_data.sample([(x, y) for x, y in zip(xs, ys)])
            ax.plot(xs, ys, zs, color='red', linewidth=2)

# Overlay TIFF image
#ax.imshow(tiff_array, extent=[0, tiff_array.shape[1], 0, tiff_array.shape[0]], origin='upper', alpha=0.5)

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Elevation')
ax.set_title('3D Visualization of DEM with Shapefile Overlay and TIFF Image')

# Show the plot
plt.show()
