import pandas as pd
import sys

def main():
    args = sys.argv[1:]
    # Load dataset from CSV file
    file_path = args[1]

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
    with open(output_file, "w") as f:
        # Write item mappings
        f.write("@CONVERTED_FROM_TEXT\n")
        for item, idx in item_mapping.items():
            f.write(f"@ITEM={idx}={item}\n")
        
        # Write transactions
        for _, row in data.iterrows():
            transaction = sorted(item_mapping[value] for value in row)
            f.write(" ".join(map(str, transaction)) + "\n")

    print(f"Formatted data saved to {output_file}")

if __name__ == "__main__":
    main()