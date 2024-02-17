import csv

# Input and output file paths
input_file = 'parsed_metar_2014_2023.csv'
output_file = 'average_seasonal_wind_speed.csv'

# Dictionary to store wind speeds per season
seasonal_wind_speeds = {'Spring': [], 'Summer': [], 'Fall': [], 'Winter': []}

# Open input file to read wind speeds
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)
    
    # Process each row in the input CSV file
    for row in reader:
        # Extract date and wind speed
        date = row['date']
        wind_speed_str = row['wind_speed']

        # Extract numerical wind speed
        wind_speed_parts = wind_speed_str.split('G')  # Split at 'G' if present

        # Check if wind speed parts list is not empty and contains a valid wind speed
        if wind_speed_parts and wind_speed_parts[0].isdigit():
            wind_speed = int(wind_speed_parts[0])  # Extract wind speed

            # Exclude rows with wind speed 0 or 00
            if wind_speed != 0:
                # Determine the season based on the month
                month = int(date[5:7])
                if 3 <= month <= 5:
                    season = 'Spring'
                elif 6 <= month <= 8:
                    season = 'Summer'
                elif 9 <= month <= 11:
                    season = 'Fall'
                else:
                    season = 'Winter'
                
                # Update wind speeds dictionary
                seasonal_wind_speeds[season].append(wind_speed)

# Open output file to write average wind speeds per season
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Season', 'Average Wind Speed'])

    # Calculate and write average wind speed per season
    for season, speeds in seasonal_wind_speeds.items():
        if speeds:
            avg_speed = round(sum(speeds) / len(speeds), 2)  # Round to 2 decimal places
        else:
            avg_speed = 0
        writer.writerow([season, avg_speed])

print("Average wind speeds per season calculated and saved to", output_file)
