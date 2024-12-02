import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Input Data
chunk_size = 50000  # Adjust chunk size based on available memory
chunks = pd.read_csv('../311_Requests_20241002.csv', chunksize=chunk_size)
data_chunks = []
for chunk in chunks:
    data_chunks.append(chunk)
df = pd.concat(data_chunks, ignore_index=True)

# Convert dates and calculate case duration
df = df[df["Subject"] == "Service Request"]
df = df[df["Type"] == "Water Clean Up After Repairs"]
df = df.dropna(subset=['Open Date', 'Closed Date'])
df['Open Date'] = pd.to_datetime(df['Open Date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
df['Closed Date'] = pd.to_datetime(df['Closed Date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
df.set_index('Case ID', inplace=True)
df.sort_values(by='Open Date', inplace=True)
df['Case Duration (hours)'] = (df['Closed Date'] - df['Open Date']).dt.total_seconds() / 3600
df = df[df['Case Duration (hours)'] >= 0]

# Drop NaN values from durations
durations = df['Case Duration (hours)'].dropna()

decomposition = sm.tsa.seasonal_decompose(
            df['Case Duration (hours)'], model='additive', period=365
        )
# decomposition.plot()
# plt.show()

plt.figure(figsize=(10, 8))
            
# Original
plt.subplot(411)
plt.plot(df['Open Date'], durations, label='Original')  # Use 'Open Date' as x-axis
plt.title('Original Case Durations')
plt.xlabel('Date')  # Updated label
plt.ylabel('Duration (hours)')
plt.legend(loc='upper left')

# Trend
plt.subplot(412)
plt.plot(df['Open Date'], decomposition.trend, label='Trend')  # Use 'Open Date' as x-axis
plt.title('Trend Component')
plt.xlabel('Date')  # Updated label
plt.ylabel('Duration (hours)')
plt.legend(loc='upper left')

# Seasonal
plt.subplot(413)
plt.plot(df['Open Date'], decomposition.seasonal, label='Seasonal')  # Use 'Open Date' as x-axis
plt.title('Seasonal Component')
plt.xlabel('Date')  # Updated label
plt.ylabel('Duration (hours)')
plt.legend(loc='upper left')

# Residual
plt.subplot(414)
plt.plot(df['Open Date'], decomposition.resid, label='Residual')  # Use 'Open Date' as x-axis
plt.title('Residual Component')
plt.xlabel('Date')  # Updated label
plt.ylabel('Duration (hours)')
plt.legend(loc='upper left')

plt.tight_layout()
plt.savefig("./output/decomposition.png")  # Save the plot
plt.close()  # Close the plot to free memory

