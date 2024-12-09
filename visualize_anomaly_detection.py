import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import sys


def main(dataset_csv):
    # Input Data
    df = pd.read_csv(dataset_csv)

    # Convert dates and calculate case duration
    df = df[df["Subject"] == "Service Request"]
    df = df[df["Type"] == "Turn Off Water - Repairs Emergency"]
    df = df.dropna(subset=['Open Date', 'Closed Date'])
    df['Open Date'] = pd.to_datetime(df['Open Date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
    df['Closed Date'] = pd.to_datetime(df['Closed Date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
    df.sort_values(by='Open Date', inplace=True)
    df['Case Duration (hours)'] = (df['Closed Date'] - df['Open Date']).dt.total_seconds() / 3600
    df = df[df['Case Duration (hours)'] > 0]

    df.set_index('Open Date', inplace=True)
    daily_total_case_durations = df.groupby(df.index.date)["Case Duration (hours)"].sum()
    # Fill missing days with 0 case durations
    daily_total_case_durations = daily_total_case_durations.reindex(
        pd.date_range(
            start=daily_total_case_durations.index.min(),
            end=daily_total_case_durations.index.max(),
            freq="D",
        ),
        fill_value=0,
    )

    decomposition = sm.tsa.seasonal_decompose(
                daily_total_case_durations, model='additive', period=365
            )
    fig = decomposition.plot()
    plt.show()

    residuals = decomposition.resid.dropna()

    if not residuals.empty:
        # Calculate the median and MAD of the residuals
        median = residuals.median()
        mad = (residuals - median).abs().median()

        # Identify anomalous points using the index of the residuals
        anomaly_indices = residuals.index[residuals - median > 3 * mad]
        anomalies = daily_total_case_durations.loc[anomaly_indices]
        # Calculate the threshold above which a day is considered an anomaly
        threshold = median + 3 * mad

        # Plot daily total case durations
        plt.figure(figsize=(15, 6))
        plt.bar(daily_total_case_durations.index, daily_total_case_durations, color='blue', label='Daily Total Case Durations for "Turn Off Water - Repairs Emergency" Service Requests')
        plt.bar(anomalies.index, anomalies, color='red', label='Anomalies')

        # Add a horizontal line for the anomaly threshold
        plt.axhline(y=threshold, color='green', linestyle='--', label=f'Anomaly Threshold ({threshold:.2f})')

        # Add labels and legend
        plt.title('Daily Total Case Durations with Anomalies')
        plt.xlabel('Date')
        plt.ylabel('Case Duration (hours)')
        plt.legend()

        plt.ylim(0, 100000)

        plt.show()

if __name__ == "__main__":
    dataset_csv = sys.argv[1]
    main(dataset_csv)