import csv
from collections import defaultdict
from datetime import datetime

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'yearly_avg_wind_speed.csv'

# Dictionary to store wind speed readings for each year
wind_speed_data = defaultdict(list)

# Read METAR data and aggregate wind speed readings by year
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        # Extract date from the row
        metar_date = datetime.strptime(row['date'], '%Y-%m-%d')
        # Extract the METAR string
        metar_string = row['metar']
        # Extract wind data
        wind_data = metar_string.split()[3]
        # Check if wind data is valid and contains gust speed
        if len(wind_data) >= 7 and 'G' in wind_data:
            # Check if wind direction is variable or calm
            if wind_data.startswith('VRB') or wind_data.startswith('CALM'):
                # Skip this record if wind direction is variable or calm
                continue
            # Extract wind direction, average speed, and gust speed
            wind_direction = int(wind_data[:3])
            average_speed = int(wind_data[3:5])
            gust_index = wind_data.index('G')
            gust_speed = int(wind_data[gust_index + 1: gust_index + 3])
            # Calculate total wind speed (average + gust)
            total_speed = average_speed + gust_speed
            # Append total wind speed to wind_speed_data dictionary
            wind_speed_data[metar_date.year].append(total_speed)

# Calculate average wind speed per year
yearly_avg_wind_speed = []
for year, speeds in wind_speed_data.items():
    avg_speed_year = sum(speeds) / len(speeds)
    yearly_avg_wind_speed.append({'year': year, 'avg_wind_speed': round(avg_speed_year, 2)})

# Write yearly average wind speed to a new CSV file
with open(output_file, 'w', newline='') as outfile:
    fieldnames = ['year', 'avg_wind_speed']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in yearly_avg_wind_speed:
        writer.writerow(row)

print("Yearly average wind speed computed and saved to", output_file)
