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