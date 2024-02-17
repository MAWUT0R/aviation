import csv
from collections import defaultdict
import re

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'yearly_avg_relative_humidity2.csv'

# Dictionary to store humidity distribution
yearly_relative_humidity = defaultdict(list)

# Regular expression pattern to match temperature and dew point data (xx/xx)
temperature_pattern = re.compile(r'(\d{2})/(\d{2})')

# Read input CSV file and extract dew point information
with open(input_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        date = row['date']
        temperature_match = temperature_pattern.search(row['metar'])
        if temperature_match:
            temperature = int(temperature_match.group(1))  # Extract temperature (e.g., 23)
            dew_point = int(temperature_match.group(2))  # Extract dew point (e.g., 18)
            if row['metar'].find('M') != -1:  # Check if 'M' is present, indicating negative value
                dew_point *= -1  # Convert to negative dew point
            # Calculate relative humidity using the formula
            relative_humidity = 100 * (2.71828 ** ((17.625 * dew_point) / (243.04 + dew_point))) / (
                        2.71828 ** ((17.625 * temperature) / (243.04 + temperature)))
            year = date[:4]  # Extract the year from the date
            yearly_relative_humidity[year].append(relative_humidity)

# Calculate the average relative humidity for each year
avg_relative_humidity_by_year = {}
for year, humidity_values in yearly_relative_humidity.items():
    avg_relative_humidity = round(sum(humidity_values) / len(humidity_values), 2)  # Round to 2 decimal places
    avg_relative_humidity_by_year[year] = avg_relative_humidity

# Write yearly average relative humidity to output CSV file
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['year', 'avg_relative_humidity'])
    for year, avg_relative_humidity in sorted(avg_relative_humidity_by_year.items()):
        writer.writerow([year, avg_relative_humidity])

print("Yearly average relative humidity has been written to", output_file)
