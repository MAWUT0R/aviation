import csv
from collections import defaultdict

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'average_temperature_per_season.csv'

# Dictionary to store temperature readings for each season
temperature_data = defaultdict(list)

# Read METAR data and aggregate temperature readings
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        month = int(row['date'][5:7])  # Extract the month from the date
        temperature = None
        metar_parts = row['metar'].split()
        # Find the temperature part in the METAR string
        for part in metar_parts:
            if '/' in part and part.count('/') == 1:
                temperature_str = part.split('/')[0]
                if temperature_str.isdigit():
                    temperature = int(temperature_str)
                    break  # Exit the loop once temperature is found
        if temperature is not None:
            # Determine the season based on the month
            if 3 <= month <= 5:
                season = 'Spring'
            elif 6 <= month <= 8:
                season = 'Summer'
            elif 9 <= month <= 11:
                season = 'Autumn'
            else:
                season = 'Winter'
            temperature_data[season].append(temperature)

# Calculate average temperature for each season
average_temperature_data = []
for season, temperatures in temperature_data.items():
    avg_temperature = round(sum(temperatures) / len(temperatures), 2)
    average_temperature_data.append({'season': season, 'avg_temperature': avg_temperature})

# Write average temperature data to a new CSV file
with open(output_file, 'w', newline='') as outfile:
    fieldnames = ['season', 'avg_temperature']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in average_temperature_data:
        writer.writerow(row)

print("Average temperature per season computed and saved to", output_file)
