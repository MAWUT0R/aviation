import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

# Load the weather data into a DataFrame
df = pd.read_csv('processed_metar_data.csv')

# Shift the weather data by one hour to create the next hour's weather features
next_hour_weather_features = ['temperature', 'relative_humidity', 'pressure', 'wind_speed', 'wind_direction', 'visibility']
for feature in next_hour_weather_features:
    df[f'next_hour_{feature}'] = df[feature].shift(-1)

# Drop the last row since there is no next hour weather available for it
df = df.dropna()

# Prepare the data
X = df[['temperature', 'relative_humidity', 'pressure', 'wind_speed', 'wind_direction', 'visibility']]
y = df['next_hour_pressure']

# Initialize and train the Gradient Boosting Regression model
gb_regressor = GradientBoostingRegressor()
gb_regressor.fit(X, y)

# Generate real-time predictions
predicted_pressure = gb_regressor.predict(X.iloc[[-1]])[0]

# Set the timestamp constant
timestamp = '312453Z'

# Extract wind direction and wind speed from the last row of the dataset
wind_direction = int(df['wind_direction'].iloc[-1])
wind_speed = int(df['wind_speed'].iloc[-1])

# Extract visibility from the last row of the dataset
visibility = int(df['visibility'].iloc[-1])

# Extract temperature and relative humidity from the last row of the dataset
temperature = int(df['temperature'].iloc[-1])
relative_humidity = int(df['relative_humidity'].iloc[-1])

# Construct the METAR string
metar_string = f"METAR KMIA {timestamp} {wind_direction:03d}{wind_speed:02d}KT {visibility}SM FEW250 {temperature}/{relative_humidity} A{int(predicted_pressure * 100)}"

print("Predicted METAR Data:")
print(metar_string)
