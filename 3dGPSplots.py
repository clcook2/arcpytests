import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the 3D shapefile
shapefile_path = r"C:\Users\clcook2\Documents\GLRC_TobaccoRiver_2023\3DviewFiles\GPS\TobaccoRiver_812023_GPSpts_FINAL.shp"
gdf = gpd.read_file(shapefile_path)

# Create a 3D figure
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Extract X, Y, Z coordinates from the shapefile geometry
xs = gdf.geometry.apply(lambda geom: geom.x)
ys = gdf.geometry.apply(lambda geom: geom.y)
zs = gdf.geometry.apply(lambda geom: geom.z)  # assuming your shapefile has Z coordinates

# Get absolute latitude and longitude values
absolute_latitudes = gdf.geometry.apply(lambda geom: geom.coords[0][1])  # Assuming the first point represents latitude
absolute_longitudes = gdf.geometry.apply(lambda geom: geom.coords[0][0])  # Assuming the first point represents longitude

# Extract another parameter from the shapefile (replace 'parameter_column' with the actual column name)
parameter_values = gdf['GNSS_Heigh']

# Plot the 3D points with size and color dependent on the parameter values
scatter = ax.scatter(absolute_longitudes, absolute_latitudes, zs, c=parameter_values, cmap='viridis', s=parameter_values*10, marker='o', label='3D Shapefile Points')

# Set labels for each axis
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Elevation (m)')

# Add a legend
ax.legend()

# Show the 3D plot
plt.show()