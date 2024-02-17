import csv
from collections import defaultdict
import re

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'humidity_distribution.csv'

# Dictionary to store humidity distribution
humidity_distribution = defaultdict(int)

# Regular expression pattern to match temperature and dew point data (xx/xx)
temperature_pattern = re.compile(r'(\d{2})/(\d{2})')

# Read input CSV file and extract dew point information
with open(input_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        metar = row['metar']
        temperature_match = temperature_pattern.search(metar)
        if temperature_match:
            temperature = int(temperature_match.group(1))  # Extract temperature (e.g., 23)
            dew_point = int(temperature_match.group(2))  # Extract dew point (e.g., 18)
            if metar.find('M') != -1:  # Check if 'M' is present, indicating negative value
                dew_point *= -1  # Convert to negative dew point
            # Calculate relative humidity using the formula
            relative_humidity = 100 * (2.71828 ** ((17.625 * dew_point) / (243.04 + dew_point))) / (2.71828 ** ((17.625 * temperature) / (243.04 + temperature)))
            humidity_distribution[int(round(relative_humidity))] += 1

# Write humidity distribution to output CSV file
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['relative_humidity', 'frequency'])
    for relative_humidity, frequency in sorted(humidity_distribution.items()):
        writer.writerow([relative_humidity, frequency])

print("Humidity distribution has been written to", output_file)
