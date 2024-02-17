import csv
from collections import defaultdict

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'yearly_avg_relative_humidity.csv'

# Dictionary to store temperature and dew point readings for each year
temperature_data = defaultdict(list)
dew_point_data = defaultdict(list)

# Read METAR data and aggregate temperature and dew point readings
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        year = int(row['date'][:4])  # Extract the year from the date
        metar_parts = row['metar'].split()
        # Find the temperature and dew point parts in the METAR string
        for part in metar_parts:
            if '/' in part and part.count('/') == 1:
                temperature_str, dew_point_str = part.split('/')
                if temperature_str.isdigit() and dew_point_str.isdigit():
                    temperature = int(temperature_str)
                    dew_point = int(dew_point_str)
                    temperature_data[year].append(temperature)
                    dew_point_data[year].append(dew_point)
                    break  # Exit the loop once temperature and dew point are found

# Calculate the average relative humidity for each year
yearly_avg_relative_humidity = []
for year in temperature_data.keys():
    avg_temperature = sum(temperature_data[year]) / len(temperature_data[year])
    avg_dew_point = sum(dew_point_data[year]) / len(dew_point_data[year])
    # Calculate relative humidity using the formula: RH = 100 * (e^(17.625 * Td / (243.04 + Td)) / e^(17.625 * T / (243.04 + T)))
    # Where Td is dew point temperature, T is temperature
    relative_humidity = 100 * (pow(2.71828, (17.625 * avg_dew_point / (243.04 + avg_dew_point))) / pow(2.71828, (17.625 * avg_temperature / (243.04 + avg_temperature))))
    yearly_avg_relative_humidity.append({'year': year, 'avg_relative_humidity': round(relative_humidity, 2)})

# Write the yearly average relative humidity to a new CSV file
with open(output_file, 'w', newline='') as outfile:
    fieldnames = ['year', 'avg_relative_humidity']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in yearly_avg_relative_humidity:
        writer.writerow(row)

print("Yearly average relative humidity computed and saved to", output_file)
