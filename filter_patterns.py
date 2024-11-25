import csv
import sys
import os


def filter_patterns(input_file, output_file):
    with (
        open(input_file, mode="r", newline="") as infile,
        open(output_file, mode="w", newline="") as outfile,
    ):
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            # Check if any cell ends with '_N' and any other cell ends with '_R' or '_T'
            if any(cell.endswith("_N") for cell in row) and any(
                cell.endswith("_R") or cell.endswith("_T") for cell in row
            ):
                writer.writerow(row)


if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python filter_patterns.py frequent_patterns.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = "./output/filtered_patterns.csv"

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    filter_patterns(input_file, output_file)
