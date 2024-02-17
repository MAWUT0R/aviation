import csv

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'windrose_data.csv'

# Dictionary to store wind speeds per direction range
direction_ranges = {'N': [0, 0, 0, 0, 0],
                    'S': [0, 0, 0, 0, 0],
                    'E': [0, 0, 0, 0, 0],
                    'W': [0, 0, 0, 0, 0]}

# Open input file to read METAR data
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)

    # Process each row in the input CSV file
    for row in reader:
        # Extract METAR string
        metar = row['metar']

        # Find wind data ending with 'KT'
        wind_data_index = metar.find('KT')
        if wind_data_index != -1:
            wind_data = metar[wind_data_index - 5: wind_data_index]  # Extract the 5 characters before 'KT'

            # Extract wind direction and speed
            wind_direction = wind_data[:3]
            wind_speed = int(wind_data[3:])

            # Convert wind direction to one of N, S, E, W
            if wind_direction.isdigit():
                wind_direction = int(wind_direction)
                if wind_direction >= 0 and wind_direction < 90:
                    direction = 'N'
                elif wind_direction >= 90 and wind_direction < 180:
                    direction = 'E'
                elif wind_direction >= 180 and wind_direction < 270:
                    direction = 'S'
                else:
                    direction = 'W'

                # Categorize wind speed range
                if wind_speed < 2:
                    direction_ranges[direction][0] += 1
                elif 2 <= wind_speed < 4:
                    direction_ranges[direction][1] += 1
                elif 4 <= wind_speed < 6:
                    direction_ranges[direction][2] += 1
                elif 6 <= wind_speed < 8:
                    direction_ranges[direction][3] += 1
                elif wind_speed >= 8:
                    direction_ranges[direction][4] += 1

# Open output file to write wind speeds per direction range
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['direction', '0-2', '2-4', '4-6', '6-8', '8-10'])

    # Write wind speeds per direction range
    for direction, speeds in direction_ranges.items():
        writer.writerow([direction] + speeds)

print("Wind speeds per direction range calculated and saved to", output_file)
