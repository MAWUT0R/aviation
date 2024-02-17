import csv
import re

# Define a regular expression pattern to extract METAR components
METAR_PATTERN = re.compile(r'(?P<place>\w{4}) \d{6}Z (?P<wind_direction>\d{3})(?P<wind_speed>\d{2})KT (?P<visibility>\d+/\d+|\d+)SM (?P<weather>[\w\-\+]+) (?P<clouds>[\w\-\+]+) (?P<temperature>M?\d{2})/(?P<dew_point>M?\d{2}) (?P<pressure>A\d{4})')

# Function to extract METAR components and return as a dictionary
def parse_metar(metar_str):
    match = METAR_PATTERN.match(metar_str)
    if match:
        return match.groupdict()
    else:
        return None

# Function to calculate relative humidity
def calculate_relative_humidity(temperature, dew_point):
    # Calculate relative humidity using the formula
    # RH = 100 * (e^(17.625 * Td / (243.04 + Td)) / e^(17.625 * T / (243.04 + T)))
    # Where Td is dew point temperature and T is temperature in Celsius
    T = temperature
    Td = dew_point
    rh = 100 * (pow(2.71828, (17.625 * Td / (243.04 + Td))) / pow(2.71828, (17.625 * T / (243.04 + T))))
    return round(rh, 2)

# Function to convert visibility denominated in fraction to decimals
def convert_visibility_to_decimal(visibility_str):
    if '/' in visibility_str:
        fraction_parts = visibility_str.split('/')
        visibility_decimal = int(fraction_parts[0]) / int(fraction_parts[1])
        return visibility_decimal
    else:
        return int(visibility_str)

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'processed_metar_data.csv'

# Process the METAR data and write to a new CSV file
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ['date', 'temperature', 'relative_humidity', 'pressure', 'wind_speed', 'wind_direction', 'visibility']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        metar_info = parse_metar(row['metar'])
        if metar_info:
            temperature = int(metar_info['temperature'].lstrip('M')) if metar_info['temperature'] != 'M' else None
            dew_point = int(metar_info['dew_point'].lstrip('M')) if metar_info['dew_point'] != 'M' else None
            if temperature is not None and dew_point is not None:
                relative_humidity = calculate_relative_humidity(temperature, dew_point)
            else:
                relative_humidity = None

            # Adjust pressure: Remove 'A' and move decimal 2 places to the left
            pressure = int(metar_info['pressure'][1:]) / 100
            
            # Convert visibility denominated in fraction to decimals
            visibility = convert_visibility_to_decimal(metar_info['visibility'])

            data_row = {
                'date': row['date'],
                'temperature': temperature,
                'relative_humidity': relative_humidity,
                'pressure': pressure,
                'wind_speed': metar_info['wind_speed'],
                'wind_direction': metar_info['wind_direction'],
                'visibility': visibility
            }
            writer.writerow(data_row)
