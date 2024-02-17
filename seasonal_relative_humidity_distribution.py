import csv
import re
from collections import defaultdict

# Input file containing METAR data for KMIA
input_file = 'METAR_2014_2023.csv'
# Output CSV file
output_file = 'average_seasonal_relative_humidity.csv'

# Regular expression pattern to match temperature and dew point data (xx/xx)
temperature_pattern = re.compile(r'(\d{2})/(\d{2})')

# Dictionary to store sum of relative humidity data for each season
seasonal_relative_humidity_sum = {'Spring': 0, 'Summer': 0, 'Fall': 0, 'Winter': 0}
# Dictionary to store count of relative humidity data for each season
seasonal_relative_humidity_count = {'Spring': 0, 'Summer': 0, 'Fall': 0, 'Winter': 0}

# Read METAR data and extract temperature and relative humidity
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        date = row['date']
        month = int(date.split('-')[1])
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
                    # Determine the season based on the month
                    if 3 <= month <= 5:
                        season = 'Spring'
                    elif 6 <= month <= 8:
                        season = 'Summer'
                    elif 9 <= month <= 11:
                        season = 'Fall'
                    else:
                        season = 'Winter'
                    # Accumulate sum and count of relative humidity for each season
                    seasonal_relative_humidity_sum[season] += relative_humidity
                    seasonal_relative_humidity_count[season] += 1
                    break  # Exit the loop once temperature and dew point are found

# Calculate the average relative humidity for each season
average_seasonal_relative_humidity = {}
for season in seasonal_relative_humidity_sum:
    if seasonal_relative_humidity_count[season] != 0:
        average_seasonal_relative_humidity[season] = seasonal_relative_humidity_sum[season] / seasonal_relative_humidity_count[season]
    else:
        average_seasonal_relative_humidity[season] = 0

# Write average relative humidity for each season to the output CSV file
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Season', 'Average Relative Humidity'])
    for season, average_humidity in average_seasonal_relative_humidity.items():
        writer.writerow([season, round(average_humidity, 2)])

print("Average seasonal relative humidity computed and saved to", output_file)
