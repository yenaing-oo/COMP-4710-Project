import pandas as pd
import sys

def find_and_mark_overlaps(file_path):
    try:
        # Load the CSV file
        data = pd.read_csv(file_path)

        # Check if required columns exist
        if "Neighbourhood" not in data.columns or "Ward" not in data.columns:
            raise ValueError("The file must contain 'Neighbourhood' and 'Ward' columns.")

        # Convert columns to sets for faster comparison
        neighbourhood_set = set(data["Neighbourhood"].dropna())
        ward_set = set(data["Ward"].dropna())

        # Find overlapping values
        overlapping_values = neighbourhood_set.intersection(ward_set)

        if overlapping_values:
            print("Overlapping values:")
            for value in overlapping_values:
                print(value)

            # Update overlapping values in the DataFrame
            data["Neighbourhood"] = data["Neighbourhood"].apply(
                lambda x: f"{x}_N" if x in overlapping_values else x
            )
            data["Ward"] = data["Ward"].apply(
                lambda x: f"{x}_W" if x in overlapping_values else x
            )

            # Save the updated DataFrame back to a new CSV
            output_path = file_path.replace(".csv", "_updated.csv")
            data.to_csv(output_path, index=False)
            print(f"Updated file saved as: {output_path}")
        else:
            print("No overlapping values found.")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Check if a file path is provided
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    # Get the file path from CLI arguments
    file_path = sys.argv[1]

    # Call the function
    find_and_mark_overlaps(file_path)