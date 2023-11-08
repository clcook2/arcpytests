import fiona
import rasterio
from rasterio.plot import show
import numpy as np
from rasterio.merge import merge
import matplotlib.pyplot as plt

shapefile_path = r"C:\Users\clcook2\Documents\GLRC_TobaccoRiver_2023\3DviewFiles\GPS\TobaccoRiver_812023_GPSpts_FINAL.shp"
tiff_path = r"C:\Users\clcook2\Documents\GLRC_TobaccoRiver_2023\3DviewFiles\Ortho\test.tif"

# Read points from the shapefile
points = []
with fiona.open(shapefile_path, 'r') as shapefile:
    for feature in shapefile:
        point = feature['geometry']['coordinates']
        points.append(point)

# Read the RGB GeoTIFF image
with rasterio.open(tiff_path) as tiff:
    # Read all three bands (R, G, B)
    red, green, blue = tiff.read(1), tiff.read(2), tiff.read(3)

# Stack the bands to create an RGB image
image = np.dstack((red, green, blue))


plt.figure(figsize=(10, 10))
#show(image)  # You can change the colormap as needed
plt.imshow(image)

x, y = zip(*points)
plt.scatter(x, y, color='red', marker='o', s=50)  # Plotting points as red circles

# Display the plot
plt.show()