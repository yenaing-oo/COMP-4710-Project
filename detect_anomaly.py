import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from statsmodels.tsa.seasonal import seasonal_decompose


# parser = argparse.ArgumentParser(description='Detect anomalies in service requests.')
# parser.add_argument('dataset', type=str, help='Path to the dataset CSV file')
# args = parser.parse_args()

print("Reading dataset...")
# Load your dataset
df = pd.read_csv("./output/311_cleaned_for_anomaly.csv")

# Ensure output directory exists
os.makedirs('./output', exist_ok=True)

print("Parsing dates...")
# Ensure date columns are properly parsed
df['Open Date'] = pd.to_datetime(df['Open Date'], format="%m/%d/%Y %I:%M:%S %p")

print("Aggregating by dates...")
# Step 1: Aggregate data by day
daily_data = df.groupby(df['Open Date'].dt.date).size().reset_index()
daily_data.columns = ['Open Date', 'Request Count']
daily_data.set_index('Open Date', inplace=True)

# Step 2: Visualize the data
plt.figure(figsize=(12, 6))
plt.plot(daily_data.index, daily_data['Request Count'], label='Daily Request Count')
plt.xlabel('Date')
plt.ylabel('Request Count')
plt.title('Service Requests Over Time')
plt.legend()
plt.savefig('1_service_requests_time_series.png')

# Step 3: Decompose the time series
result = seasonal_decompose(daily_data['Request Count'], model='additive', period=365)

# Get the residuals (noise)
residuals = result.resid

# Visualize residuals (optional)
plt.figure(figsize=(12, 6))
plt.plot(daily_data.index, residuals, label='Residuals (Noise)')
plt.xlabel('Date')
plt.ylabel('Residuals')
plt.title('Residuals of Service Requests')
plt.legend()
plt.savefig('2_residuals.png')

# Ensure the index is a DatetimeIndex
daily_data.index = pd.to_datetime(daily_data.index)
# Step 4: Detect anomalies using Isolation Forest on residuals
daily_data['Day'] = (daily_data.index - daily_data.index[0]).days  # Numeric 'Day' column
daily_data['Residuals'] = residuals  # Add residuals as a new column
daily_data.dropna(subset=['Residuals'], inplace=True)  # Drop rows with NaN residuals
X_residuals = daily_data[['Day', 'Residuals']]  # Use the new 'Residuals' column

# Train Isolation Forest on residuals
iso_forest_residuals = IsolationForest(contamination=0.01, random_state=42)
daily_data['Anomaly'] = iso_forest_residuals.fit_predict(X_residuals)

# Mark anomalies
daily_data['Anomaly'] = daily_data['Anomaly'].apply(lambda x: 1 if x == -1 else 0)

# Step 5: Visualize anomalies
plt.figure(figsize=(12, 6))
plt.plot(daily_data.index, daily_data['Request Count'], label='Request Count')
plt.scatter(daily_data.index[daily_data['Anomaly'] == 1], daily_data['Request Count'][daily_data['Anomaly'] == 1], color='red', label='Anomaly')
plt.xlabel('Date')
plt.ylabel('Request Count')
plt.title('Anomalies in Service Requests')
plt.legend()
plt.savefig('3_anomalies_in_service_requests.png')

anomalies = daily_data[daily_data['Anomaly'] == 1]
print("Detected Anomalies:")
print(anomalies)

# Step 6: Save the results
anomalies.to_csv('3_service_request_anomalies.csv', index=True)

