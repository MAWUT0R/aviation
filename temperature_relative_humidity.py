import csv
import re
from collections import defaultdict

# Input file containing METAR data for KMIA
input_file = 'METAR_2014_2023.csv'
# Output CSV file
output_file = 'temperature_relative_humidity.csv'

# Regular expression pattern to match temperature and dew point data (xx/xx)
temperature_pattern = re.compile(r'(\d{2})/(\d{2})')

# Dictionary to store temperature and relative humidity data
temperature_relative_humidity_data = defaultdict(list)

# Read METAR data and extract temperature and relative humidity
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        metar = row['metar']
        # Extract temperature and dew point parts in the METAR string
        for part in metar.split():
            if '/' in part and part.count('/') == 1:
                temperature_str, dew_point_str = part.split('/')
                if temperature_str.isdigit() and dew_point_str.isdigit():
                    temperature = int(temperature_str)
                    dew_point = int(dew_point_str)
                    # Calculate relative humidity using the formula
                    relative_humidity = 100 * (2.71828 ** ((17.625 * dew_point) / (243.04 + dew_point))) / (2.71828 ** ((17.625 * temperature) / (243.04 + temperature)))
                    temperature_relative_humidity_data[temperature].append(relative_humidity)
                    break  # Exit the loop once temperature and dew point are found

# Calculate the average relative humidity for each unique temperature
average_temperature_relative_humidity_data = []
for temperature, humidities in temperature_relative_humidity_data.items():
    average_relative_humidity = sum(humidities) / len(humidities)
    average_temperature_relative_humidity_data.append([temperature, round(average_relative_humidity, 2)])

# Write temperature and average relative humidity data to the output CSV file
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Temperature (°C)', 'Average Relative Humidity (%)'])
    writer.writerows(average_temperature_relative_humidity_data)

print("Temperature and average relative humidity data written to", output_file)
