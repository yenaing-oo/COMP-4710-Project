import folium
from folium.plugins import HeatMap
import pandas as pd
import sys

def main(csv_filename):
    print("Reading CSV...")
    # Load data from CSV
    df = pd.read_csv(csv_filename)

    print("Filtering data...")
    df = df[
        (df["Subject"] == "Service Request")
        & df["Geometry"].notna()
    ]

    print("Extracting geolocation..")
    # Extract latitude and longitude from "Geometry"
    df[["longitude", "latitude"]] = df["Geometry"].str.extract(
        r"POINT \(([^ ]+) ([^ ]+)\)"
    )
    df["latitude"] = df["latitude"].astype(float)
    df["longitude"] = df["longitude"].astype(float)

    print("Creating heat map...")
    # Create a base map
    if not df.empty:
        base_map = folium.Map(
            location=[df["latitude"].mean(), df["longitude"].mean()], zoom_start=12
        )

        # Add heat map with adjusted radius and blur
        heat_data = df[["latitude", "longitude"]].values.tolist()
        HeatMap(heat_data, radius=60, blur=55).add_to(base_map)

        # Save or display the map
        base_map.save("heatmap.html")

    else:
        print("No data available for the specified filters.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python visualize_service_requests_by_geolocation.py <csv_filename>"
        )
    else:
        main(sys.argv[1])
