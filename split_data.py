import pandas as pd
from sklearn.model_selection import train_test_split

# Load the processed METAR data into a DataFrame
data = pd.read_csv('processed_metar_data.csv')

# Split the data into train and temp_data (validation + test)
train_data, temp_data = train_test_split(data, test_size=0.3, random_state=42)

# Further split the temp_data into validation and test data
validation_data, test_data = train_test_split(temp_data, test_size=0.5, random_state=42)

# Write the data to CSV files
train_data.to_csv('train_data.csv', index=False)
validation_data.to_csv('validation_data.csv', index=False)
test_data.to_csv('test_data.csv', index=False)
