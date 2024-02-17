import csv
from collections import defaultdict
import re

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'temperature_distribution.csv'

# Dictionary to store temperature distribution
temperature_distribution = defaultdict(int)

# Regular expression pattern to match temperature data (xx/xx)
temperature_pattern = re.compile(r'(\d{2})/(\d{2})')

# Read input CSV file and extract temperature information
with open(input_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        metar = row['metar']
        temperature_match = temperature_pattern.search(metar)
        if temperature_match:
            temperature = int(temperature_match.group(1))  # Extract temperature (e.g., 23)
            temperature_distribution[temperature] += 1

# Write temperature distribution to output CSV file
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['temperature', 'no_of_entries'])
    for temperature, count in sorted(temperature_distribution.items()):
        writer.writerow([temperature, count])

print("Temperature distribution has been written to", output_file)
