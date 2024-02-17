import csv

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'parsed_metar_2014_2023.csv'

# Function to parse METAR string and extract relevant information
def parse_metar(metar_string):
    metar_parts = metar_string.split()
    wind_speed = None

    # Search for wind speed in the METAR string
    for part in metar_parts:
        if part.endswith('KT'):
            wind_speed = part[3:5]  # Extract 4th and 5th characters as wind speed
            break

    return wind_speed

# Open input and output files
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ['date', 'wind_speed']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    # Process each row in the input CSV file
    for row in reader:
        wind_speed = parse_metar(row['metar'])
        if wind_speed:  # Check if wind_speed is not empty
            writer.writerow({'date': row['date'], 'wind_speed': wind_speed})

print("METAR data parsed and saved to", output_file)
