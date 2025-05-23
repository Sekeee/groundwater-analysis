import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

plt.style.use('default')

def plot_station_no2(station_code, df):
    station_data = df[df['station'].str.startswith(station_code)].copy()
    print(f"\n--- {station_code} ---")
    print(f"Number of records: {len(station_data)}")

    station_data['NO2'] = pd.to_numeric(df.iloc[station_data.index, 48], errors='coerce')  # AW column
    station_data['Depths (m)'] = pd.to_numeric(station_data['Depths (m)'], errors='coerce')
    station_data = station_data.dropna(subset=['NO2', 'Depths (m)'])
    print(f"Number of valid records after removing NaN: {len(station_data)}")
    if len(station_data) == 0:
        print(f"No valid data found for {station_code} stations\n")
        return
    fig = plt.figure(figsize=(9, 8))
    ax = fig.add_axes([0.15, 0.1, 0.7, 0.8])
    ax_top = ax.twiny()
    scatter = ax.scatter(station_data['NO2'], 
                        station_data['Depths (m)'],
                        c=station_data['Date'].astype(np.int64),
                        cmap='jet',
                        s=100,
                        alpha=0.8,
                        marker='o',
                        edgecolors='black')
    ax_top.set_xlim(ax.get_xlim())
    ax_top.set_xlabel('NO₂⁻ (mg/L)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Depth (m)', fontsize=12, fontweight='bold')
    ax.set_xlabel('')
    ax.xaxis.set_ticks([])
    ax.invert_yaxis()
    plt.title(f'NO₂⁻ vs Depth Relationship for {station_code} Stations', 
             fontsize=14, 
             fontweight='bold',
             pad=30)
    cax = fig.add_axes([0.85, 0.1, 0.03, 0.8])
    cbar = plt.colorbar(scatter, cax=cax)
    cbar.set_label('Date', fontsize=10, fontweight='bold')
    tick_locations = np.linspace(station_data['Date'].astype(np.int64).min(),
                               station_data['Date'].astype(np.int64).max(),
                               8)
    cbar.set_ticks(tick_locations)
    cbar.set_ticklabels([pd.Timestamp(ts).strftime('%Y-%m-%d') 
                        for ts in tick_locations])
    ax.grid(True, linestyle='--', alpha=0.7)
    
    unique_dates = station_data['Date'].unique()
    norm = plt.Normalize(station_data['Date'].astype(np.int64).min(), station_data['Date'].astype(np.int64).max())
    cmap = plt.get_cmap('jet')
    for date in unique_dates:
        data = station_data[station_data['Date'] == date].sort_values('Depths (m)')
        color = cmap(norm(pd.to_datetime(date).to_datetime64().astype(np.int64)))
        ax.plot(data['NO2'], data['Depths (m)'], color=color, linewidth=1, alpha=0.6)

    median_data = station_data.groupby('Depths (m)', as_index=False)['NO2'].median().sort_values('Depths (m)')
    ax.plot(median_data['NO2'], median_data['Depths (m)'], color='black', linewidth=2, linestyle='--', label='Median')
    print(f"Plotted median NO₂⁻ line for {station_code}.")
    outname = f'no2_depth_relationship_{station_code.lower()}.png'
    plt.savefig(outname, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Plot has been saved as '{outname}'")
    print(f"Summary statistics for all {station_code} stations:")
    print(f"Total number of measurements: {len(station_data)}")
    print("Depth range:")
    print(f"Min depth: {station_data['Depths (m)'].min():.2f} m")
    print(f"Max depth: {station_data['Depths (m)'].max():.2f} m")
    print("NO₂⁻ range:")
    print(f"Min NO₂⁻: {station_data['NO2'].min():.2f} mg/L")
    print(f"Max NO₂⁻: {station_data['NO2'].max():.2f} mg/L")
    print(f"Mean NO₂⁻: {station_data['NO2'].mean():.2f} mg/L\n")

if __name__ == '__main__':
    df = pd.read_excel('United.xlsx')  
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)
    df['Date'] = pd.to_datetime(df['Date'])
    for i in range(1, 17):
        station_code = f'SS-{i:02d}'
        plot_station_no2(station_code, df) 