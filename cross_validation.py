from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import pandas as pd

# Load the training data
data = pd.read_csv('train_data.csv')

# Split the data into features (X) and target variable (y)
X = data.drop(columns=['metar'])
y = data['metar']

# Initialize the models
linear_reg = LinearRegression()
random_forest_reg = RandomForestRegressor(n_estimators=100)
gradient_boosting_reg = GradientBoostingRegressor(n_estimators=100)

# Define the number of folds (k)
k = 5

# Evaluate Linear Regression model
linear_reg_scores = cross_val_score(linear_reg, X, y, scoring='neg_mean_absolute_error', cv=k)
linear_reg_mae = -linear_reg_scores.mean()

# Evaluate Random Forest Regressor model
random_forest_scores = cross_val_score(random_forest_reg, X, y, scoring='neg_mean_absolute_error', cv=k)
random_forest_mae = -random_forest_scores.mean()

# Evaluate Gradient Boosting Regressor model
gradient_boosting_scores = cross_val_score(gradient_boosting_reg, X, y, scoring='neg_mean_absolute_error', cv=k)
gradient_boosting_mae = -gradient_boosting_scores.mean()

# Print mean absolute errors for each model
print("Linear Regression MAE:", linear_reg_mae)
print("Random Forest Regressor MAE:", random_forest_mae)
print("Gradient Boosting Regressor MAE:", gradient_boosting_mae)
