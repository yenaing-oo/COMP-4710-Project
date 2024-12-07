import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
import sys


def main(dataset_csv):
    print("Loading data...")
    df = pd.read_csv(dataset_csv)

    # Drop any rows that don't have either an Open or Closed date
    df = df.dropna(subset=["Open Date", "Closed Date"])

    print("Filtering by service requests...")
    df = df[df["Subject"] == "Service Request"]

    print("Calculating case durations...")
    df["Open Date"] = pd.to_datetime(df["Open Date"], format="%m/%d/%Y %I:%M:%S %p")
    df["Closed Date"] = pd.to_datetime(df["Closed Date"], format="%m/%d/%Y %I:%M:%S %p")
    
    print("Sorting by open date...")
    df = df.sort_values(by="Open Date", ascending=True)

    print("Calculating case durations...")
    df["Case Duration (hours)"] = (
        df["Closed Date"] - df["Open Date"]
    ).dt.total_seconds() / 3600
    df = df[df["Case Duration (hours)"] > 0]
    df = df.set_index("Case ID")

    print("Grouping by request type...")
    # Group by 'Type'
    grouped = df.groupby("Type")
    anomaly_data_list = []
    
    total_groups = len(grouped)
    current_group = 0 

    for request_type, group in grouped:
        current_group += 1
        print(f"Processing group {current_group} of {total_groups}...") 
        
        group = group.set_index("Open Date")
        daily_total_case_durations = group.groupby("Open Date")["Case Duration (hours)"].sum()

        # Fill missing days with 0 case durations
        daily_total_case_durations = daily_total_case_durations.reindex(
            pd.date_range(
                start=daily_total_case_durations.index.min(),
                end=daily_total_case_durations.index.max(),
                freq="D",
            ),
            fill_value=0,
        )

        # Skip groups with less than 730 observations (need at least 730 to determine seasonal trends)
        if len(daily_total_case_durations) < 730:
            print(f"Skipping group: {request_type}")
            continue

        decomposition = seasonal_decompose(
            daily_total_case_durations, model="additive", period=365
        )
        residuals = decomposition.resid.dropna()

        # Calculate the median and MAD of the residuals
        median = residuals.median()
        mad = (residuals - median).abs().median()

        # Anomalies are points where |residual - median| > 3 * MAD
        anomaly_count = residuals[
            (residuals - median).abs() > 3 * mad
        ].count()

        # Append the results to the list
        anomaly_data_list.append(
            {
                "Request type": request_type,
                "Number of days with anomalous daily total case duration": anomaly_count,
                "Total requests": len(group),
                "Number of days in period": len(daily_total_case_durations),
                "Anomaly Rate": anomaly_count / len(daily_total_case_durations)
            }
        )

    print("Saving anomaly counts to CSV file...")
    # Save the anomaly counts for all types to a CSV file
    anomaly_data = pd.DataFrame(anomaly_data_list)
    anomaly_data.to_csv("./output/anomaly_count.csv", index=False)


if __name__ == "__main__":
    dataset_csv = sys.argv[1]
    main(dataset_csv)
