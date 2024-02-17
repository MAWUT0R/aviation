import csv

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'yearly_avg_pressure.csv'

# Dictionary to store pressure per year
pressure_data = {}

# Open input file to read pressure per year
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)
    
    # Process each row in the input CSV file
    for row in reader:
        # Extract year and pressure
        year = row['date'][:4]
        metar_string = row['metar']

        # Extract pressure data from the METAR string
        parts = metar_string.split()
        for part in parts:
            if len(part) == 5 and (part[0] == 'A' or part[0] == 'Q'):
                pressure_value = part[1:]  # Extract pressure value
                if pressure_value.isdigit():
                    pressure_value = int(pressure_value)
                    if part[0] == 'Q':
                        # Convert pressure to inches of mercury (inHg) from hectopascals (hPa)
                        pressure_value /= 33.8639
                    if year in pressure_data:
                        pressure_data[year].append(pressure_value)
                    else:
                        pressure_data[year] = [pressure_value]

# Open output file to write average pressure per year
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['year', 'avg_pressure'])

    # Calculate and write average pressure per year
    for year, pressures in pressure_data.items():
        avg_pressure = sum(pressures) / len(pressures)
        avg_pressure = round(avg_pressure, 2)  # Round to 2 decimal places
        writer.writerow([year, avg_pressure])

print("Average pressure per year calculated and saved to", output_file)
