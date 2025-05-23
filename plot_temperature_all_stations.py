import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# File and sheet names
excel_file = 'UZM_Precipitation_Combined - 22_05_2025.xlsx'
sheets = ['Selmun', 'Valletta', 'Zebbug', 'Luqa']
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']

plt.figure(figsize=(14, 7))

for sheet, color in zip(sheets, colors):
    df = pd.read_excel(excel_file, sheet_name=sheet)
    df['Date & Time [UTC]'] = pd.to_datetime(df['Date & Time [UTC]'])
    df['Mean Temperature'] = pd.to_numeric(df['Mean Temperature'], errors='coerce')
    df = df.dropna(subset=['Mean Temperature'])
    df = df.sort_values('Date & Time [UTC]')
    # Resample to daily mean, only for 'Mean Temperature'
    df_daily = df.set_index('Date & Time [UTC]')['Mean Temperature'].resample('D').mean().reset_index()
    plt.plot(
        df_daily['Date & Time [UTC]'],
        df_daily['Mean Temperature'],
        label=sheet,
        color=color,
        linewidth=2,
        marker='o',
        markersize=3
    )

plt.xlabel('Date')
plt.ylabel('Mean Temperature (°C)')
plt.title('Daily Mean Temperature vs Date')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.gca().xaxis.set_major_formatter(DateFormatter('%d.%m.%Y'))
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig('mean_temperature_all_stations.png', dpi=300)
plt.show() 