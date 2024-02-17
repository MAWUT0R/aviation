import csv
from datetime import datetime

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'average_seasonal_air_pressure.csv'

# Dictionary to store seasonal air pressure totals and counts
seasonal_pressure_totals = {'Spring': 0, 'Summer': 0, 'Fall': 0, 'Winter': 0}
seasonal_pressure_counts = {'Spring': 0, 'Summer': 0, 'Fall': 0, 'Winter': 0}

# Open input file to read METAR data
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)

    # Process each row in the input CSV file
    for row in reader:
        metar_string = row['metar']
        metar_date = datetime.strptime(row['date'], '%Y-%m-%d')

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

                    # Determine the season based on the month
                    month = metar_date.month
                    if month in [3, 4, 5]:  # Spring: March, April, May
                        seasonal_pressure_totals['Spring'] += pressure_value
                        seasonal_pressure_counts['Spring'] += 1
                    elif month in [6, 7, 8]:  # Summer: June, July, August
                        seasonal_pressure_totals['Summer'] += pressure_value
                        seasonal_pressure_counts['Summer'] += 1
                    elif month in [9, 10, 11]:  # Fall: September, October, November
                        seasonal_pressure_totals['Fall'] += pressure_value
                        seasonal_pressure_counts['Fall'] += 1
                    else:  # Winter: December, January, February
                        seasonal_pressure_totals['Winter'] += pressure_value
                        seasonal_pressure_counts['Winter'] += 1

# Open output file to write average seasonal air pressure
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Season', 'Average_Air_Pressure'])

    # Write average seasonal air pressure to the CSV file
    for season in seasonal_pressure_totals:
        if seasonal_pressure_counts[season] != 0:
            average_pressure = seasonal_pressure_totals[season] / seasonal_pressure_counts[season]
            # Divide the average pressure by 100
            average_pressure /= 100
            writer.writerow([season, round(average_pressure, 2)])
        else:
            writer.writerow([season, 'No data'])

print("Average seasonal air pressure calculated and saved to", output_file)
