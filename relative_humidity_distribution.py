import csv
from collections import defaultdict
import math

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'relative_humidity_distribution.csv'

# Dictionary to store relative humidity distribution
relative_humidity_distribution = defaultdict(int)

# Read METAR data and calculate relative humidity
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        metar_parts = row['metar'].split()
        for part in metar_parts:
            if '/' in part and part.count('/') == 1:
                temperature_str, dew_point_str = part.split('/')
                if temperature_str.isdigit() and dew_point_str.isdigit():
                    temperature = int(temperature_str)
                    dew_point = int(dew_point_str)
                    # Calculate relative humidity using the formula
                    e1 = 17.625 * dew_point / (243.04 + dew_point)
                    e2 = 17.625 * temperature / (243.04 + temperature)
                    relative_humidity = 100 * (math.exp(e1) / math.exp(e2))
                    relative_humidity_distribution[int(round(relative_humidity))] += 1
                    break  # Exit the loop once temperature and dew point are found

# Write relative humidity distribution to output CSV file
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['relative_humidity', 'frequency'])
    for humidity, frequency in sorted(relative_humidity_distribution.items()):
        writer.writerow([humidity, frequency])

print("Relative humidity distribution computed and saved to", output_file)
