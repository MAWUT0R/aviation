import csv

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'air_pressure_frequency.csv'

# Dictionary to store frequency distribution of air pressure
air_pressure_frequency = {}

# Open input file to read METAR data
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)

    # Process each row in the input CSV file
    for row in reader:
        metar_string = row['metar']

        # Extract air pressure data from the METAR string
        parts = metar_string.split()
        for part in parts:
            if part.startswith('A') or part.startswith('Q'):
                # Extract the part of the string starting from the prefix (A or Q)
                pressure_string = part[1:]

                # Filter out non-digit characters and ensure it's not an empty string
                pressure_digits = ''.join(filter(str.isdigit, pressure_string))
                if pressure_digits:
                    pressure_value = int(pressure_digits)

                    # Convert pressure to inches of mercury (inHg) from hectopascals (hPa)
                    if part.startswith('Q'):
                        pressure_value /= 33.8639

                    # Move the pressure value two decimal places to the left
                    pressure_value /= 100

                    # Count the frequency of this air pressure value
                    if pressure_value in air_pressure_frequency:
                        air_pressure_frequency[pressure_value] += 1
                    else:
                        air_pressure_frequency[pressure_value] = 1

# Open output file to write air pressure frequency distribution
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['air_pressure', 'frequency'])

    # Write air pressure frequency distribution to the CSV file
    for pressure, frequency in sorted(air_pressure_frequency.items()):
        writer.writerow([pressure, frequency])

print("Air pressure frequency distribution calculated and saved to", output_file)
