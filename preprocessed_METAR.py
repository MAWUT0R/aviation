import pandas as pd
import re

# Read the METAR data
metar_data = pd.read_csv('METAR_2014_2023.csv')

# Define a function to extract temperature from the METAR string
def extract_temperature(metar):
    # Regular expression pattern to match temperature data (xx/xx)
    temperature_pattern = re.compile(r'(\d{2})/(\d{2})')
    temperature_match = temperature_pattern.search(metar)
    if temperature_match:
        temperature = int(temperature_match.group(1))
    else:
        temperature = None
    return temperature

# Define a function to extract pressure from the METAR string
def extract_pressure(metar):
    # Regular expression pattern to match pressure data (A2994 or Q1001)
    pressure_pattern = re.compile(r'(A|Q)(\d{4})')
    pressure_match = pressure_pattern.search(metar)
    if pressure_match:
        pressure = int(pressure_match.group(2)) / 100 if pressure_match.group(1) == 'A' else int(pressure_match.group(2)) / 33.8639
    else:
        pressure = None
    return pressure

# Define a function to extract relative humidity from the METAR string
def extract_relative_humidity(metar):
    # Regular expression pattern to match temperature and dew point data (xx/xx)
    temperature_pattern = re.compile(r'(\d{2})/(\d{2})')
    temperature_match = temperature_pattern.search(metar)
    if temperature_match:
        temperature = int(temperature_match.group(1))  # Extract temperature (e.g., 23)
        dew_point = int(temperature_match.group(2))  # Extract dew point (e.g., 18)
        if 'M' in metar:  # Check if 'M' is present, indicating negative value
            dew_point *= -1  # Convert to negative dew point
        # Calculate relative humidity using the formula
        relative_humidity = 100 * (2.71828 ** ((17.625 * dew_point) / (243.04 + dew_point))) / (
                    2.71828 ** ((17.625 * temperature) / (243.04 + temperature)))
    else:
        relative_humidity = None
    return relative_humidity

# Define a function to extract wind speed from the METAR string
def extract_wind_speed(metar):
    # Regular expression pattern to match wind speed data (e.g., 5KT)
    wind_speed_pattern = re.compile(r'(\d+)KT')
    wind_speed_match = wind_speed_pattern.search(metar)
    if wind_speed_match:
        wind_speed = int(wind_speed_match.group(1))  # Extract wind speed
    else:
        wind_speed = None
    return wind_speed

# Define a function to extract wind direction from the METAR string
def extract_wind_direction(metar):
    # Find the substring containing the part ending with KT
    kt_index = metar.find('KT')
    if kt_index != -1:
        wind_info = metar[kt_index - 3: kt_index]
        # Check if the wind_info contains only integers
        if wind_info.isdigit():
            # Extract the first 3 characters which represent the wind direction
            wind_direction = int(wind_info)
        else:
            wind_direction = ''  # Return empty if not all characters are digits
    else:
        wind_direction = None  # Return None if 'KT' is not found
    return wind_direction



# Define a function to extract visibility from the METAR string
def extract_visibility(metar):
    # Find the substring ending with 'SM'
    visibility_info = metar.split('SM')[0]
    # Extract the integers preceding 'SM'
    visibility = int(''.join(filter(str.isdigit, visibility_info)))
    return visibility


# Apply the extraction functions to create new columns
metar_data['Temperature'] = metar_data['metar'].apply(extract_temperature)
metar_data['Pressure'] = metar_data['metar'].apply(extract_pressure)
metar_data['Relative Humidity'] = metar_data['metar'].apply(extract_relative_humidity)
metar_data['Wind Speed'] = metar_data['metar'].apply(extract_wind_speed)
metar_data['Wind Direction'] = metar_data['metar'].apply(extract_wind_direction)
metar_data['Visibility'] = metar_data['metar'].apply(extract_visibility)

# Drop the original 'metar' column
metar_data.drop(columns=['metar'], inplace=True)

# Write the preprocessed data to a new CSV file
metar_data.to_csv('preprocessed_METAR.csv', index=False)

print("Preprocessed METAR data saved to preprocessed_METAR.csv")
