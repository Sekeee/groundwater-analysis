import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import itertools
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

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
    
    # Prepare unique markers and colors
    markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h', 'H', '+', 'x', 'X', 'd', '|', '_']
    colors = plt.cm.tab20.colors  # 20 unique colors
    marker_cycler = itertools.cycle(markers)
    color_cycler = itertools.cycle(colors)

    # Get unique dates (sorted)
    unique_dates = sorted(station_data['Date'].unique())

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))
    ax_top = ax.twiny()
    ax_top.set_xlim(ax.get_xlim())

    legend_handles = []

    for i, date in enumerate(unique_dates):
        date_str = pd.Timestamp(date).strftime('%b-%Y')
        marker = markers[i % len(markers)]
        color = colors[i % len(colors)]
        data = station_data[station_data['Date'] == date]
        data = data.sort_values('Depths (m)')
        # Plot points only (no line)
        sc = ax.scatter(data['EC (μS/cm)'], data['Depths (m)'],
                        marker=marker, color=color, edgecolors='black', s=100, label=date_str, zorder=3)
        legend_handles.append(plt.Line2D([0], [0], marker=marker, color='w', markerfacecolor=color, markeredgecolor='black', markersize=10, label=date_str, linestyle='--'))

    # Axis labels and title
    ax_top.set_xlabel('EC (μS/cm)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Depth (m)', fontsize=12, fontweight='bold')
    ax.set_xlabel('')
    ax.xaxis.set_ticks([])
    ax.invert_yaxis()
    plt.title('EC vs Depth Relationship for SS-01 Stations', fontsize=14, fontweight='bold', pad=30)

    # Add legend below the plot
    ax.legend(handles=legend_handles, loc='upper center', bbox_to_anchor=(0.5, -0.13), ncol=4, fontsize=10, frameon=False)

    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout(rect=[0, 0.08, 1, 1])

    # Linear regression (EC vs Depth)
    X = station_data['EC (μS/cm)'].values.reshape(-1, 1)
    y = station_data['Depths (m)'].values
    reg = LinearRegression().fit(X, y)
    y_pred = reg.predict(X)
    r2 = r2_score(y, y_pred)

    # Plot regression line
    ec_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    depth_pred = reg.predict(ec_range)
    ax.plot(ec_range, depth_pred, color='red', linewidth=2, linestyle='-', label='Regression')
    legend_handles.append(plt.Line2D([0], [0], color='red', linewidth=2, label='Regression'))

    # Print regression equation and R^2
    print(f"\nRegression equation: Depth = {reg.coef_[0]:.3f} * EC + {reg.intercept_:.3f}")
    print(f"R^2: {r2:.3f}")

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