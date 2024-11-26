"""
This script cleans a 311 dataset by filtering and transforming specific fields.
It reads a CSV file containing service requests, processes the data to
include only relevant entries, and outputs a cleaned version of the dataset
with modified field values.

Only the Reason, Type, Neighbourhood and Ward columns are kept from the original dataset.
Service requests without a neighbourhood value are filtered out.

Field values under Reason column are modified to be suffixed with "_R", 
Type column - "_T", Neighbourhood column "_N", 
and Ward "_W"

Usage:
    python clean_for_fp.py <input_csv_file>

Output:
    A cleaned CSV file is saved to './output/cleaned_311_dataset.csv'.
"""

import sys
import csv

def main():
    args = sys.argv[1:]
    csv_file = args[0]
    output_file = "./output/cleaned_311_dataset.csv"

    with open(csv_file, mode="r", newline="") as infile, open(
        output_file, mode="w", newline=""
    ) as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ["Reason", "Type", "Neighbourhood", "Ward"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        row_count = sum(1 for row in reader)
        infile.seek(0)
        next(reader)

        for i, row in enumerate(reader, start=1):
            if row["Subject"] == "Service Request" and row["Neighbourhood"]:
                writer.writerow({
                    "Reason": row["Reason"] + "_R",
                    "Type": row["Type"] + "_T",
                    "Neighbourhood": row["Neighbourhood"] + "_N",
                    "Ward": row["Ward"] + "_W"
                })
            print(f"Processing row {i}/{row_count}")

if __name__ == "__main__":
    main()