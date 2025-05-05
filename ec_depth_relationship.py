import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Set style for better visualization
plt.style.use('default')

try:
    # Read the Excel file
    df = pd.read_excel('United.xlsx')  
    
    # Rename columns based on first row
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)
    
    # Convert date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Filter for stations starting with SS-01
    station_data = df[df['station'].str.startswith('SS-01')].copy()
    
    print(f"\nNumber of records: {len(station_data)}")
    
    # Convert EC and Depths to numeric, handling any non-numeric values
    station_data['EC (μS/cm)'] = pd.to_numeric(station_data['EC (μS/cm)'], errors='coerce')
    station_data['Depths (m)'] = pd.to_numeric(station_data['Depths (m)'], errors='coerce')
    
    # Remove any rows with NaN values
    station_data = station_data.dropna(subset=['EC (μS/cm)', 'Depths (m)'])
    print(f"\nNumber of valid records after removing NaN: {len(station_data)}")
    
    if len(station_data) == 0:
        raise ValueError("No valid data found for SS-01 stations")
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create single scatter plot for all data
    scatter = ax.scatter(station_data['EC (μS/cm)'], 
                        station_data['Depths (m)'],
                        c=station_data['Date'].astype(np.int64),
                        cmap='viridis',
                        s=100,  # Point size
                        alpha=0.6,
                        marker='o')  # Using circles for all points
    
    # Customize axes
    ax.set_xlabel('EC (μS/cm)', fontsize=12)
    ax.set_ylabel('Depth (m)', fontsize=12)
    
    # Invert y-axis since depth increases downward
    ax.invert_yaxis()
    
    # Add title
    plt.title('EC vs Depth Relationship for SS-01 Stations\nColored by Date', fontsize=14)
    
    # Add colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label('Date', fontsize=10)
    
    # Format colorbar ticks to show actual dates
    tick_locations = np.linspace(station_data['Date'].astype(np.int64).min(),
                               station_data['Date'].astype(np.int64).max(),
                               5)
    cbar.set_ticks(tick_locations)
    cbar.set_ticklabels([pd.Timestamp(ts).strftime('%Y-%m-%d') 
                        for ts in tick_locations])
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('ec_depth_relationship_ss01.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\nPlot has been saved as 'ec_depth_relationship_ss01.png'")
    
    # Print summary statistics for all SS-01 stations combined
    print("\nSummary statistics for all SS-01 stations:")
    print(f"Total number of measurements: {len(station_data)}")
    print("\nDepth range:")
    print(f"Min depth: {station_data['Depths (m)'].min():.2f} m")
    print(f"Max depth: {station_data['Depths (m)'].max():.2f} m")
    print("\nEC range:")
    print(f"Min EC: {station_data['EC (μS/cm)'].min():.0f} μS/cm")
    print(f"Max EC: {station_data['EC (μS/cm)'].max():.0f} μS/cm")
    print(f"Mean EC: {station_data['EC (μS/cm)'].mean():.0f} μS/cm")
    
except Exception as e:
    print(f"An error occurred: {str(e)}")
    print("\nPlease check if:")
    print("1. The Excel file contains stations starting with 'SS-01'")
    print("2. The columns 'EC (μS/cm)' and 'Depths (m)' exist")
    print("3. The data in these columns can be converted to numbers")