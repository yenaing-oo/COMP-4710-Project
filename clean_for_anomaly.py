import sys
import csv

def main():
    args = sys.argv[1:]
    csv_file = args[0]
    output_file = "./output/311_cleaned_for_anomaly.csv"

    with open(csv_file, mode="r", newline="") as infile, open(
        output_file, mode="w", newline=""
    ) as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ["Open Date"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        row_count = sum(1 for row in reader)
        infile.seek(0)
        next(reader)

        for i, row in enumerate(reader, start=1):
            if row["Subject"] == "Service Request" and row["Open Date"]:
                writer.writerow({
                    "Open Date": row["Open Date"],
                })
            print(f"Processing row {i}/{row_count}")

if __name__ == "__main__":
    main()