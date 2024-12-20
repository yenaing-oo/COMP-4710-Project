"""
This script formats the cleaned dataset from a CSV file into a specific text format compatible with
SPMF library's implementation of the FP-Growth algorithm
(https://www.philippe-fournier-viger.com/spmf/FPGrowth.php). It reads a CSV file, extracts unique
items from each column, maps each unique item to a unique integer ID, and writes the item mappings
and transactions to two separate text files. The output files are saved to
'./output/formatted_data.txt' and './output/keys.txt'.

Usage:
    python format.py <input_csv_file>

Output:
    `./output/keys.txt' - A mapping of domain item IDs to their names
    './output/formatted_data.txt' - The transactions, with the item names replaced with their item
    IDs
"""

import pandas as pd
import sys


def main():
    args = sys.argv[1:]
    # Load dataset from CSV file
    file_path = args[0]

    print("Loading dataset...")
    data = pd.read_csv(file_path)

    print("Extracting unique items...")
    # Extract unique items from each column
    unique_items = pd.unique(data.values.ravel())

    print("Creating item mappings...")
    # Create a dictionary to map each unique item to a unique integer ID
    item_mapping = {item: idx + 1 for idx, item in enumerate(unique_items)}

    print("Formatting data...")
    # Write the mapping and transactions to a text file
    output_file = "./output/formatted_data.txt"
    key_file = "./output/keys.txt"
    with open(output_file, "w") as f1, open(key_file, "w") as f2:
        # Write item mappings
        f2.write("@CONVERTED_FROM_TEXT\n")
        for item, idx in item_mapping.items():
            line = f"@ITEM={idx}={item}\n"
            f2.write(line)

        # Write transactions
        for _, row in data.iterrows():
            transaction = sorted(item_mapping[value] for value in row)
            f1.write(" ".join(map(str, transaction)) + "\n")

    print(f"Formatted data saved to {output_file}")


if __name__ == "__main__":
    main()
