import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

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
y_temperature = df['next_hour_temperature']

# Split the data into training and testing sets
X_train, X_test, y_train_temperature, y_test_temperature = train_test_split(X, y_temperature, test_size=0.2, random_state=42)

# Random Forest Regression
rf_param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
rf_regressor = RandomForestRegressor()
rf_random = RandomizedSearchCV(estimator=rf_regressor, param_distributions=rf_param_grid, n_iter=100, cv=5, verbose=2, random_state=42, n_jobs=-1)
rf_random.fit(X_train, y_train_temperature)

# Extract feature importances from the trained Random Forest model
feature_importances = rf_random.best_estimator_.feature_importances_

# Create a DataFrame to organize feature importances
feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importances})

# Sort the features by importance in descending order
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

# Print the top features and their importance scores
print("Feature Importance Analysis:")
print(feature_importance_df)
