import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import sys

def main(csv_filename):
    chunk_size = 200000
    chunks = pd.read_csv(csv_filename, chunksize=chunk_size)
    data_chunks = []
    for chunk in chunks:
        data_chunks.append(chunk)
    df = pd.concat(data_chunks, ignore_index=True)

    df = df[df['Subject'] == 'Service Request']
    df['Open Date'] = pd.to_datetime(df['Open Date'], errors='coerce',format="%m/%d/%Y %I:%M:%S %p")
    df = df.dropna(subset=['Open Date'])

    #Find uniques by Type
    unique_types = df['Type'].unique()
    print(unique_types)

    #Find case_count by Type
    type_counts = df.groupby('Type').size().reset_index(name='count').sort_values(by='count', ascending=False)
    #print(type_counts)

    # Bar chart of types
    type_counts.plot(kind='bar', x='Type', y='count', title='Count by Reason')
    plt.xlabel('Reason')
    plt.ylabel('Count')
    plt.show()


    #Find anomalies among different Types
    anomalies_summary = {}
    anomaly_counts = {}

    for unique_type in unique_types:
        df_type = df[df['Type']== unique_type]

        daily_cases_type = df_type.groupby(df['Open Date'].dt.date).size().to_frame(name='case_count').reset_index()
        # Ensure date is in datetime format for decomposition
        daily_cases_type['date'] = pd.to_datetime(daily_cases_type['Open Date'])
        daily_cases_type.set_index('date', inplace=True)

        if len(daily_cases_type) < 730:
            #print(f"Skipping decomposition for {unique_type}: insufficient data ({len(daily_cases_type)} points).")
            continue


        try:
            # Perform seasonal decomposition
            decomposition = sm.tsa.seasonal_decompose(
                daily_cases_type['case_count'], model='additive', period=365
            )

            # Detect anomalies based on residuals
            residuals = decomposition.resid.dropna()
            mean_residual = residuals.mean()
            std_residual = residuals.std()
            threshold_upper = mean_residual + 3 * std_residual
            threshold_lower = mean_residual - 3 * std_residual
            anomalies = residuals[(residuals > threshold_upper) | (residuals < threshold_lower)]

            # Store anomalies for this type
            anomalies_summary[unique_type] = anomalies
            anomaly_counts[unique_type] = len(anomalies)

            #print(f"Anomalies for {unique_type}:")
            #print(anomalies)

        except ValueError as e:
            #print(f"Decomposition failed for {unique_type}: {e}")
            anomaly_counts[unique_type] = 0

    anomaly_df = pd.DataFrame(list(anomaly_counts.items()), columns=['Type', 'Anomaly Count'])
    anomaly_df = anomaly_df.sort_values(by='Anomaly Count', ascending=False)

    plt.figure(figsize=(20, 10))
    plt.bar(anomaly_df['Type'], anomaly_df['Anomaly Count'], color='skyblue')
    plt.xlabel('Type')
    plt.ylabel('Anomaly Count')
    plt.title('Number of Anomalies by Type')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    anomalies_summary_df = pd.DataFrame(list(anomalies_summary.items()), columns=['Type', 'Anomaly Count'])
    anomalies_summary_df = anomalies_summary_df.sort_values(by='Anomaly Count', ascending=False)

    anomalies_summary.to_csv('type_counts_anomalies_sorted.csv', index=False)
    anomaly_counts.to_csv('type_counts_anomalies_count_sorted.csv', index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_model_types.py <csv_filename>")
        sys.exit(1)
    main(sys.argv[1])