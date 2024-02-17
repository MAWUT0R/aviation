import csv
from datetime import datetime

# Input and output file paths
input_file = 'METAR_2014_2023.csv'
output_file = 'seasonal_visibility_stats.csv'

# Dictionary to store seasonal visibility totals, counts, highs, and lows
seasonal_visibility_stats = {'Spring': {'total': 0, 'count': 0, 'high': float('-inf'), 'low': float('inf')},
                             'Summer': {'total': 0, 'count': 0, 'high': float('-inf'), 'low': float('inf')},
                             'Fall': {'total': 0, 'count': 0, 'high': float('-inf'), 'low': float('inf')},
                             'Winter': {'total': 0, 'count': 0, 'high': float('-inf'), 'low': float('inf')}}

# Open input file to read METAR data
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)

    # Process each row in the input CSV file
    for row in reader:
        metar_string = row['metar']
        metar_date = datetime.strptime(row['date'], '%Y-%m-%d')

        # Extract visibility data from the METAR string
        parts = metar_string.split()
        for part in parts:
            if 'SM' in part:  # Check for visibility (SM)
                visibility_str = part.replace('SM', '')

                try:
                    # Convert fractional visibility to decimal
                    if '/' in visibility_str:
                        numerator, denominator = map(int, visibility_str.split('/'))
                        visibility_value = numerator / denominator
                    else:
                        visibility_value = float(visibility_str)

                    # Determine the season based on the month
                    month = metar_date.month
                    season = None
                    if month in [3, 4, 5]:  # Spring: March, April, May
                        season = 'Spring'
                    elif month in [6, 7, 8]:  # Summer: June, July, August
                        season = 'Summer'
                    elif month in [9, 10, 11]:  # Fall: September, October, November
                        season = 'Fall'
                    else:  # Winter: December, January, February
                        season = 'Winter'

                    # Update seasonal visibility stats
                    seasonal_visibility_stats[season]['total'] += visibility_value
                    seasonal_visibility_stats[season]['count'] += 1
                    seasonal_visibility_stats[season]['high'] = max(seasonal_visibility_stats[season]['high'], visibility_value)
                    seasonal_visibility_stats[season]['low'] = min(seasonal_visibility_stats[season]['low'], visibility_value)
                except ValueError:
                    # Skip invalid visibility values
                    pass

# Open output file to write seasonal visibility statistics
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Season', 'Average_Visibility', 'High_Visibility', 'Low_Visibility'])

    # Write seasonal visibility statistics to the CSV file
    for season, stats in seasonal_visibility_stats.items():
        if stats['count'] != 0:
            average_visibility = stats['total'] / stats['count']
            writer.writerow([season, round(average_visibility, 2), round(stats['high'], 2), round(stats['low'], 2)])
        else:
            writer.writerow([season, 'No data', 'No data', 'No data'])

print("Seasonal visibility statistics calculated and saved to", output_file)
