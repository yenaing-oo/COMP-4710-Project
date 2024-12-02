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
    df = df[df["Case Duration (hours)"] >= 0]
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
        
        # Skip groups with less than 730 observations (need at least 730 to determine seasonal trends)
        if len(group) < 730:
            print(f"Skipping group: {request_type}")
            continue
        
        durations = group["Case Duration (hours)"].dropna()

        if not durations.empty:
            decomposition = seasonal_decompose(durations, model="additive", period=365)
            residuals = decomposition.resid.dropna()

            # Calculate the mean and standard deviation of the residuals
            residual_mean = residuals.mean()
            residual_std = residuals.std()

            # Count the number of anomalies
            anomaly_count = residuals[
                (residuals > residual_mean + 3 * residual_std)
            ].count()

            # Append the results to the list
            anomaly_data_list.append(
                {
                    "Request Type": request_type,
                    "Count of anomalous case duration": anomaly_count,
                    "Total Requests": len(group),
                    "Anomaly Rate": anomaly_count/len(group)
                }
            )

    print("Saving anomaly counts to CSV file..")
    # Save the anomaly counts for all types to a CSV file
    anomaly_data = pd.DataFrame(anomaly_data_list)
    anomaly_data.to_csv("./output/anomaly_count.csv", index=False)


if __name__ == "__main__":
    dataset_csv = sys.argv[1]
    main(dataset_csv)
