import csv

# Input and output file paths
input_file = 'parsed_metar_2014_2023.csv'
output_file = 'yearly_avg_wind_speed.csv'

# Dictionary to store wind speeds per year
wind_speeds = {}

# Open input file to read wind speeds per year
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)
    
    # Process each row in the input CSV file
    for row in reader:
        # Extract year and wind speed
        year = row['date'][:4]
        wind_speed_str = row['wind_speed']

        # Extract numerical wind speed
        wind_speed_parts = wind_speed_str.split('G')  # Split at 'G' if present

        # Check if wind speed parts list is not empty and contains a valid wind speed
        if wind_speed_parts and wind_speed_parts[0].isdigit():
            wind_speed = int(wind_speed_parts[0])  # Extract wind speed

            # Exclude rows with wind speed 0 or 00
            if wind_speed != 0:
                # Update wind speeds dictionary
                if year in wind_speeds:
                    wind_speeds[year].append(wind_speed)
                else:
                    wind_speeds[year] = [wind_speed]

# Open output file to write average wind speeds per year
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['year', 'avg_wind_speed'])

    # Calculate and write average wind speed per year
    for year, speeds in wind_speeds.items():
        avg_speed = round(sum(speeds) / len(speeds), 2)  # Round to 2 decimal places
        writer.writerow([year, avg_speed])

print("Average wind speeds per year calculated and saved to", output_file)
