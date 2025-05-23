import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
from matplotlib.lines import Line2D

# Read the Excel file
df = pd.read_excel('circle-Data.xlsx')

# Convert columns to numeric, replacing any non-numeric values with NaN
df['x'] = pd.to_numeric(df['x'], errors='coerce')
df['y'] = pd.to_numeric(df['y'], errors='coerce')
df['Average Nitrates in 0-2 m (mg/L NO₃⁻) '] = pd.to_numeric(df['Average Nitrates in 0-2 m (mg/L NO₃⁻) '], errors='coerce')

# Fill NaN values with 0 for nitrate concentrations
df['Average Nitrates in 0-2 m (mg/L NO₃⁻) '] = df['Average Nitrates in 0-2 m (mg/L NO₃⁻) '].fillna(0)

# Convert coordinates to decimal degrees (assuming x/y are in 1e6 format)
df['lon'] = df['x'] / 1000000
df['lat'] = df['y'] / 1000000

# Create a figure and axis
fig, ax = plt.subplots(figsize=(12, 7))

# Assign a unique color to each station
stations = df['Station'].unique()
cmap = plt.get_cmap('tab20', len(stations))
colors = {station: cmap(i) for i, station in enumerate(stations)}

size_factor = 1  # Use your chosen size factor

# Plot each station with its unique color
for station in stations:
    station_data = df[df['Station'] == station]
    ax.scatter(
        station_data['lon'], station_data['lat'],
        s=station_data['Average Nitrates in 0-2 m (mg/L NO₃⁻) '].astype(float) * size_factor,
        color=colors[station], alpha=0.6, edgecolors=colors[station], linewidths=1.5,
        label=station
    )

# Dynamically zoom out to show all data and surroundings
lon_min, lon_max = df['lon'].min(), df['lon'].max()
lat_min, lat_max = df['lat'].min(), df['lat'].max()
lon_buffer = (lon_max - lon_min) * 2.0  
lat_buffer = (lat_max - lat_min) * 2.0
ax.set_xlim(lon_min - lon_buffer, lon_max + lon_buffer)
ax.set_ylim(lat_min - lat_buffer, lat_max + lat_buffer)

# Add OpenStreetMap background
ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)
 
# Remove axis ticks and frame for a clean look
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)

# Create custom legend handles (small squares)
legend_handles = [Line2D([0], [0], marker='s', color='w', markerfacecolor=colors[station],
                         markeredgecolor=colors[station], markersize=8, label=station, linestyle='')
                  for station in stations]
ax.legend(handles=legend_handles, loc='upper right', bbox_to_anchor=(1.25, 1), title='Station', fontsize=8, title_fontsize=10)

plt.tight_layout()
plt.savefig('nitrate_station_map.png', dpi=300, bbox_inches='tight')
plt.close() 