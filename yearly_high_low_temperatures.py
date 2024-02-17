import csv
from collections import defaultdict

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'yearly_high_low_temperatures.csv'

# Dictionary to store temperature readings for each year
temperature_data = defaultdict(list)

# Read METAR data and aggregate temperature readings
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        year = int(row['date'][:4])  # Extract the year from the date
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
            temperature_data[year].append(temperature)

# Calculate yearly low and high temperatures
yearly_temperatures = []
for year, temperatures in temperature_data.items():
    low_temperature = min(temperatures)
    high_temperature = max(temperatures)
    yearly_temperatures.append({'year': year, 'low': low_temperature, 'high': high_temperature})

# Write yearly low and high temperatures to a new CSV file
with open(output_file, 'w', newline='') as outfile:
    fieldnames = ['year', 'low', 'high']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in yearly_temperatures:
        writer.writerow(row)

print("Yearly high and low temperatures computed and saved to", output_file)
