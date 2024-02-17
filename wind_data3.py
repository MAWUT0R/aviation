import csv

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'wind_data3.csv'

# Dictionary to store wind speeds per direction range
direction_counts = {'N': 0, 'NNE': 0, 'NE': 0, 'ENE': 0,
                    'E': 0, 'ESE': 0, 'SE': 0, 'SSE': 0,
                    'S': 0, 'SSW': 0, 'SW': 0, 'WSW': 0,
                    'W': 0, 'WNW': 0, 'NW': 0, 'NNW': 0}

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

            # Extract wind direction
            wind_direction = wind_data[:3]

            # Convert wind direction to one of the 16 cardinal points
            if wind_direction.isdigit():
                wind_direction = int(wind_direction)
                index = int((wind_direction + 11.25) % 360 / 22.5)
                cardinal_point = ['N', 'NNE', 'NE', 'ENE',
                                  'E', 'ESE', 'SE', 'SSE',
                                  'S', 'SSW', 'SW', 'WSW',
                                  'W', 'WNW', 'NW', 'NNW'][index]
                direction_counts[cardinal_point] += 1

# Open output file to write wind speeds per direction range
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['direction', 'no_of_entries'])

    # Write wind speeds per direction range
    for direction, count in direction_counts.items():
        writer.writerow([direction, count])

print("Number of entries per cardinal point calculated and saved to", output_file)
