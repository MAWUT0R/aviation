import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
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
y_relative_humidity = df['next_hour_relative_humidity']
y_pressure = df['next_hour_pressure']
y_wind_speed = df['next_hour_wind_speed']
y_wind_direction = df['next_hour_wind_direction']
y_visibility = df['next_hour_visibility']

# Split the data into training and testing sets
X_train, X_test, y_train_temperature, y_test_temperature = train_test_split(X, y_temperature, test_size=0.2, random_state=42)
X_train, X_test, y_train_relative_humidity, y_test_relative_humidity = train_test_split(X, y_relative_humidity, test_size=0.2, random_state=42)
X_train, X_test, y_train_pressure, y_test_pressure = train_test_split(X, y_pressure, test_size=0.2, random_state=42)
X_train, X_test, y_train_wind_speed, y_test_wind_speed = train_test_split(X, y_wind_speed, test_size=0.2, random_state=42)
X_train, X_test, y_train_wind_direction, y_test_wind_direction = train_test_split(X, y_wind_direction, test_size=0.2, random_state=42)
X_train, X_test, y_train_visibility, y_test_visibility = train_test_split(X, y_visibility, test_size=0.2, random_state=42)

# Model Selection and Hyperparameter Tuning

# Linear Regression
linear_reg = LinearRegression()
linear_reg.fit(X_train, y_train_temperature)

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

# Gradient Boosting Regression
gb_param_grid = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.1, 0.05, 0.01],
    'max_depth': [3, 4, 5],
    'min_samples_split': [2, 5, 10]
}
gb_regressor = GradientBoostingRegressor()
gb_random = RandomizedSearchCV(estimator=gb_regressor, param_distributions=gb_param_grid, n_iter=100, cv=5, verbose=2, random_state=42, n_jobs=-1)
gb_random.fit(X_train, y_train_temperature)

# Cross-Validation

# Linear Regression
linear_scores = cross_val_score(linear_reg, X_train, y_train_temperature, scoring='neg_mean_squared_error', cv=5)
linear_rmse_scores = (-linear_scores)**0.5

# Random Forest Regression
rf_cv_scores = cross_val_score(rf_random.best_estimator_, X_train, y_train_temperature, scoring='neg_mean_squared_error', cv=5)
rf_rmse_scores = (-rf_cv_scores)**0.5

# Gradient Boosting Regression
gb_cv_scores = cross_val_score(gb_random.best_estimator_, X_train, y_train_temperature, scoring='neg_mean_squared_error', cv=5)
gb_rmse_scores = (-gb_cv_scores)**0.5

# Model Evaluation

# Linear Regression
y_pred_linear = linear_reg.predict(X_test)
linear_rmse = mean_squared_error(y_test_temperature, y_pred_linear, squared=False)

# Random Forest Regression
y_pred_rf = rf_random.best_estimator_.predict(X_test)
rf_rmse = mean_squared_error(y_test_temperature, y_pred_rf, squared=False)

# Gradient Boosting Regression
y_pred_gb = gb_random.best_estimator_.predict(X_test)
gb_rmse = mean_squared_error(y_test_temperature, y_pred_gb, squared=False)

# Print results
print("Linear Regression RMSE:", linear_rmse)
print("Random Forest Regression RMSE:", rf_rmse)
print("Gradient Boosting Regression RMSE:", gb_rmse)
