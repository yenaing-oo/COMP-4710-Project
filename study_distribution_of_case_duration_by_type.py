import pandas as pd
import sys
import matplotlib.pyplot as plt


def main(dataset_csv):
    print("Loading data...")
    df = pd.read_csv(dataset_csv)

    # Drop any rows that don't have either an Open or Closed date
    df = df.dropna(subset=["Open Date", "Closed Date"])

    print("Filtering by service requests...")
    df = df[df["Subject"] == "Service Request"]

    print("Converting date columns to datetime...")
    df["Open Date"] = pd.to_datetime(df["Open Date"], format="%m/%d/%Y %I:%M:%S %p")
    df["Closed Date"] = pd.to_datetime(df["Closed Date"], format="%m/%d/%Y %I:%M:%S %p")

    print("Calculating case durations...")
    df["Case Duration (hours)"] = (
        df["Closed Date"] - df["Open Date"]
    ).dt.total_seconds() / 3600
    df = df[df["Case Duration (hours)"] >= 0]

    df = df.dropna(subset=["Case Duration (hours)"])

    print("Grouping by request type...")
    grouped = df.groupby("Type")

    total_groups = len(grouped)
    current_group = 0

    for request_type, group in grouped:
        current_group += 1
        print(f"Processing group {current_group} of {total_groups}...")

        # Group by Open Date (day) and sum the case durations
        group["Open Date (day)"] = group["Open Date"].dt.date
        daily_totals = group.groupby("Open Date (day)")["Case Duration (hours)"].sum()

        # Sort daily totals in ascending order
        daily_totals = daily_totals.sort_values()
        print(daily_totals)

        # Ensure min_duration and max_duration are not NaN
        min_duration = daily_totals.min()
        max_duration = daily_totals.max()
        
        # Calculate bin width with a check for potential division by zero
        if max_duration > min_duration:
            bin_width = (max_duration - min_duration) / max(1, len(daily_totals) - 1)
            bins = max(10, int(bin_width))  # Ensure at least 10 bins
        else:
            bins = 10

        plt.figure(figsize=(12, 6))
        plt.hist(daily_totals, bins=bins, color="blue", alpha=0.7)
        plt.title(f"Distribution of Daily Total Case Durations for {request_type}")
        plt.xlabel("Daily Total Case Duration (hours)")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()
    print("Processing completed!")


if __name__ == "__main__":
    dataset_csv = sys.argv[1]
    main(dataset_csv)
