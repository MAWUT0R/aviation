import csv
from collections import defaultdict

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'yearly_high_low_relative_humidity.csv'

# Dictionary to store relative humidity readings for each year
humidity_data = defaultdict(list)

# Read METAR data and aggregate relative humidity readings
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        date = row['date']
        year = int(date[:4])  # Extract the year from the date
        metar_parts = row['metar'].split()
        # Find the humidity part in the METAR string
        for part in metar_parts:
            if part.startswith('A') and len(part) >= 6:
                humidity_str = part[1:3]  # Extract the relative humidity part
                if humidity_str.isdigit():
                    humidity = int(humidity_str)
                    humidity_data[year].append(humidity)
                    break  # Exit the loop once humidity is found

# Calculate the yearly high and low relative humidity
yearly_high_low_relative_humidity = []
for year, humidities in humidity_data.items():
    if humidities:  # Ensure there are humidity readings for the year
        low_humidity = min(humidities)
        high_humidity = max(humidities)
    else:
        low_humidity = 0
        high_humidity = 0
    yearly_high_low_relative_humidity.append({'year': year, 'low': low_humidity, 'high': high_humidity})

# Write the yearly high and low relative humidity to a new CSV file
with open(output_file, 'w', newline='') as outfile:
    fieldnames = ['year', 'low', 'high']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in yearly_high_low_relative_humidity:
        writer.writerow(row)

print("Yearly high and low relative humidity computed and saved to", output_file)
