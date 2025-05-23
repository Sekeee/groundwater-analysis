import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter
import re
import os

def create_station_plot(water_content_data, precip_data, station_num):
    station_name = f'Station {station_num}'
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Get date range for plotting
    min_date = water_content_data['Time'].min()
    max_date = water_content_data['Time'].max()
    ax1.set_xlim(min_date, max_date)
    
    # Plot water content data with different line styles on the LEFT Y-axis
    depths = water_content_data.columns[1:]  # Skip Time column
    styles = ['-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--', '-.']
    
    # Use different colors for water content lines
    water_colors = plt.cm.nipy_spectral(np.linspace(0, 1, len(depths)))
    
    # Map station identifiers based on column position rather than specific depth values
    station_ids = ['EX1', 'EX2', 'S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10']
    
    for i, depth in enumerate(depths):
        # Check for valid data in this column
        if not water_content_data[depth].isnull().all():
            # Get station identifier based on column position
            station_id = station_ids[i] if i < len(station_ids) else f'S{i+1:02d}'
            
            line = ax1.plot(water_content_data['Time'], water_content_data[depth], 
                    label=f'{station_id}', 
                    color=water_colors[i], 
                    linestyle=styles[i % len(styles)],
                    linewidth=2)
            
            # Add text label directly on the line for the depth
            # Get last valid point for placing the label
            valid_data = water_content_data[depth].notna()
            if valid_data.any():
                last_idx = valid_data.values.nonzero()[0][-1]
                x_pos = water_content_data['Time'].iloc[last_idx]
                y_pos = water_content_data[depth].iloc[last_idx]
                ax1.annotate(depth, xy=(x_pos, y_pos), 
                            xytext=(5, 0), textcoords='offset points',
                            color=water_colors[i], fontsize=9, 
                            fontweight='bold', va='center')
    
    ax1.set_ylabel('Water Content (%)', fontsize=12)
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylim(bottom=0)
    
    ax1.xaxis.set_major_formatter(DateFormatter('%m/%Y'))
    plt.xticks(rotation=30)
    
    # RIGHT Y-axis shows precipitation data
    ax2 = ax1.twinx()
    
    # Filter precipitation data to match the date range of water content data
    filtered_precip = precip_data[(precip_data['Date & Time [UTC]'] >= min_date) & 
                               (precip_data['Date & Time [UTC]'] <= max_date)]
    
    print(f"  Precipitation data points in date range: {len(filtered_precip)}")
    
    if not filtered_precip.empty:
        # Plot precipitation data but don't include it in the legend
        ax2.bar(filtered_precip['Date & Time [UTC]'], filtered_precip['Precipitation'], 
                width=2, color='black', alpha=0.1)  # Reduced alpha for less prominence
        ax2.set_ylabel('Rain (mm day$^{-1}$)', fontsize=12)
        ax2.set_ylim(0, 21)
    
    # Only include water content lines in the legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    
    if lines1:
        ax1.legend(lines1, labels1, loc='upper left', ncol=2, fontsize=9, frameon=False)
    
    plt.title(f'Water Content and Precipitation Time Series for {station_name}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    os.makedirs('station_plots_water_content_2', exist_ok=True)
    output_file = f'station_plots_water_content_2/station_{station_num}_water_content_precip.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"  Plot saved to {output_file}")
    plt.close()

print('Loading data...')
water_content = pd.read_csv('1.csv')
precip = pd.read_excel('UZM_Precipitation_Combined-Climate data.xlsx')
print('Data loaded.')

water_content['Time'] = pd.to_datetime(water_content['Time'], format='%d/%m/%Y %H:%M')
precip['Date & Time [UTC]'] = pd.to_datetime(precip['Date & Time [UTC]'])

print(f"Water content data date range: {water_content['Time'].min()} to {water_content['Time'].max()}")
print(f"Precipitation data date range: {precip['Date & Time [UTC]'].min()} to {precip['Date & Time [UTC]'].max()}")

# Process for each CSV file (1.csv to 16.csv for different stations)
for station_num in range(1, 17):
    print(f'Processing station: {station_num}')
    # Check if this station's data file exists
    if station_num == 1:
        # We already loaded station 1 data
        station_data = water_content
    else:
        try:
            station_data = pd.read_csv(f'{station_num}.csv')
            station_data['Time'] = pd.to_datetime(station_data['Time'], format='%d/%m/%Y %H:%M')
            print(f'  Loaded data for Station {station_num}')
        except FileNotFoundError:
            print(f'  No data file found for Station {station_num}')
            continue
    
    print(f'  Data points for Station {station_num}: {len(station_data)}')
    if not station_data.empty:
        create_station_plot(station_data, precip, station_num)
        print(f'  Processing complete for Station {station_num}')
    else:
        print(f'  No data for Station {station_num}') 