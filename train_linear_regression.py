from sklearn.linear_model import LinearRegression
import pandas as pd

# Load the training data
train_data = pd.read_csv('train_data.csv')

# Separate features and target variable
X_train = train_data.drop(columns=['metar'])
y_train = train_data['metar']

# Initialize and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)
