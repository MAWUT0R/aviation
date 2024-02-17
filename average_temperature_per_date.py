import csv
from collections import defaultdict

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'average_temperature_per_year.csv'

# Dictionary to store temperature readings for each year
temperature_data = defaultdict(list)

# Read METAR data and aggregate temperature readings
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        year = row['date'][:4]  # Extract the year from the date
        metar_parts = row['metar'].split()
        # Find the temperature part in the METAR string
        for part in metar_parts:
            if '/' in part and part.count('/') == 1:
                temperature_str = part.split('/')[0]
                if temperature_str.isdigit():
                    temperature = int(temperature_str)
                    temperature_data[year].append(temperature)
                    break  # Exit the loop once temperature is found

# Calculate average temperature for each year
average_temperature_data = []
for year, temperatures in temperature_data.items():
    avg_temperature = round(sum(temperatures) / len(temperatures), 2)
    average_temperature_data.append({'year': year, 'avg_temperature': avg_temperature})

# Write average temperature data to a new CSV file
with open(output_file, 'w', newline='') as outfile:
    fieldnames = ['year', 'avg_temperature']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in average_temperature_data:
        writer.writerow(row)

print("Average temperature per year computed and saved to", output_file)
