import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter
import re
import os

def create_station_plot(station_data, precip_data, station_name):
    fig, ax1 = plt.subplots(figsize=(10, 6))
    stations = station_data['station'].unique()
    ordered_stations = []
    for s in ['SS-' + station_name.split()[-1] + '-EX1', 'SS-' + station_name.split()[-1] + '-EX2']:
        if s in stations:
            ordered_stations.append(s)
    for i in range(1, 10):
        s = f'SS-{station_name.split()[-1]}-0{i}'
        if s in stations:
            ordered_stations.append(s)
    colors = plt.cm.nipy_spectral(np.linspace(0, 1, len(ordered_stations)))
    for i, station in enumerate(ordered_stations):
        data = station_data[station_data['station'] == station].sort_values('Date')
        label = f"{station} ({data['Depths (m)'].iloc[0]} m)" if not data['Depths (m)'].isnull().all() else station
        ax1.plot(data['Date'], data['Nitrites (mg/L NO₂⁻)'], label=label, color=colors[i], linewidth=2)
    ax1.set_ylabel('Nitrites (mg/L NO₂⁻)', fontsize=12)
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylim(bottom=0)
    if not station_data.empty:
        min_date = station_data['Date'].min()
        max_date = station_data['Date'].max()
        ax1.set_xlim(min_date, max_date)
    ax1.xaxis.set_major_formatter(DateFormatter('%m/%Y'))
    plt.xticks(rotation=30)
    ax2 = ax1.twinx()
    ax2.bar(precip_data['Date & Time [UTC]'], precip_data['Precipitation'], width=2, color='black', alpha=0.18, label='Precipitation')
    ax2.set_ylabel('Rain (mm day$^{-1}$)', fontsize=12)
    ax2.set_ylim(0, 21)
    for i, station in enumerate(ordered_stations):
        data = station_data[station_data['station'] == station].sort_values('Date')
        if not data.empty and not data['Depths (m)'].isnull().all():
            last_x = data['Date'].iloc[-1]
            last_y = data['Nitrites (mg/L NO₂⁻)'].iloc[-1]
            depth = data['Depths (m)'].iloc[0]
            ax1.annotate(f'{depth} m', xy=(last_x, last_y), xytext=(5, 0), textcoords='offset points',
                         color=colors[i], fontsize=9, va='center', fontweight='bold')
    lines1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(lines1, labels1, loc='upper left', ncol=2, fontsize=9, frameon=False)
    plt.title(f'Nitrites and Precipitation Time Series for {station_name}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    os.makedirs('station_plots_nitrite', exist_ok=True)
    plt.savefig(f'station_plots_nitrite/{station_name}_nitrite_precip.png', dpi=300, bbox_inches='tight')
    plt.close()

print('Loading data...')
united = pd.read_excel('United.xlsx', header=1)
precip = pd.read_excel('UZM_Precipitation_Combined-Climate data.xlsx')
print('Data loaded.')

united['Date'] = pd.to_datetime(united['Date'])
precip['Date & Time [UTC]'] = pd.to_datetime(precip['Date & Time [UTC]'])

united['Nitrites (mg/L NO₂⁻)'] = united['Nitrites (mg/L NO₂⁻)'].astype(str).str.replace('<', '', regex=False)
united['Nitrites (mg/L NO₂⁻)'] = pd.to_numeric(united['Nitrites (mg/L NO₂⁻)'], errors='coerce')
united = united.dropna(subset=['Nitrites (mg/L NO₂⁻)'])

station_numbers = united['station'].str.extract(r'SS-(\d+)')[0].unique()
print(f'Found station numbers: {station_numbers}')

for station_num in station_numbers:
    print(f'Processing station: {station_num}')
    station_mask = united['station'].astype(str).str.match(f'SS-{station_num}-(0[1-9]|EX[12])')
    station_data = united[station_mask]
    print(f'  Data points for this station: {len(station_data)}')
    if not station_data.empty:
        create_station_plot(station_data, precip, f'Station {station_num}')
        print(f'  Plot saved for Station {station_num}')
    else:
        print(f'  No data for Station {station_num}') 