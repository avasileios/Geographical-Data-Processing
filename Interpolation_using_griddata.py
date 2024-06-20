'''Antonopoulos Va Chasapis Ch'''
import numpy as np
import pandas as pd
import geopandas as gpd
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

# Δεδομένα
csv_file_path = r"C:\Users\Vasilis Ant\Downloads\111.csv"
shp_file_path = r"C:\Users\Vasilis Ant\Downloads\xartis_tel_.shp"  

df = pd.read_csv(csv_file_path, delimiter=';', encoding='utf-8')

# Debug: Print the first few rows of the dataframe
print("DataFrame Head:\n", df.head())

# Ensure the necessary columns are present
if 'longitude' not in df.columns or 'latitude' not in df.columns or 'Μέγιστο (0.1C)' not in df.columns:
    raise ValueError("DataFrame must contain 'longitude', 'latitude', and 'Μέγιστο (0.1C)' columns")

# GeoDataFrame με τα σημεία και τις θερμοκρασίες
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

# Debug: Print the GeoDataFrame info
print("GeoDataFrame Info:\n", gdf.info())

# Εξαγωγή συντεταγμένων και τιμών θερμοκρασίας
coords = np.array(list(zip(gdf.geometry.x, gdf.geometry.y)))
values = gdf["Μέγιστο (0.1C)"].values

# Debug: Print the coordinates and values
print("Coordinates:\n", coords)
print("Values:\n", values)

# Ορισμός του πλέγματος (grid) για την πρόβλεψη
gridx = np.linspace(coords[:, 0].min(), coords[:, 0].max(), 100)
gridy = np.linspace(coords[:, 1].min(), coords[:, 1].max(), 100)
gridx, gridy = np.meshgrid(gridx, gridy)

# Interpolation using griddata
z = griddata(coords, values, (gridx, gridy), method='cubic')

# Debug: Print the grid and z values
print("Grid X Shape:", gridx.shape)
print("Grid Y Shape:", gridy.shape)
print("Z Values Shape:", z.shape)

# Debug: Check for NaN values in Z
print("Z contains NaN values:", np.isnan(z).any())

# Load the shapefile
map_gdf = gpd.read_file(shp_file_path)

# Εμφάνιση των αποτελεσμάτων
plt.figure(figsize=(12, 8))

# Plot the map from the shapefile
map_gdf.boundary.plot(ax=plt.gca(), linewidth=1, color='black')

# Plot the interpolation result using imshow
plt.imshow(z, extent=(coords[:, 0].min() - 0.5, coords[:, 0].max() + 0.5, coords[:, 1].min() - 0.5, coords[:, 1].max() + 0.5), origin='lower', cmap='viridis', alpha=0.75)
plt.colorbar(label="Temperature (0.1°C)")

# Overlay the data points with better visibility
plt.scatter(coords[:, 0], coords[:, 1], c='white', edgecolors='black', s=100, zorder=10, label='Stations')

# Add contour lines
contour = plt.contour(gridx, gridy, z, colors='k', linewidths=0.5)
plt.clabel(contour, inline=True, fontsize=8)

plt.title("Interpolation using griddata", fontsize=16)
plt.xlabel("Longitude", fontsize=14)
plt.ylabel("Latitude", fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.show()
