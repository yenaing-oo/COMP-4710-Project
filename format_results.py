import sys
import csv

item_sort_order = {"_R": 0, "_T": 1, "_N": 2, "_W": 3}

def parse_keys(keys_txt):
    keys = {}
    with open(keys_txt, 'r') as f:
        for line in f:
            if line.startswith('@ITEM='):
                parts = line.split('=')
                item_number = int(parts[1])
                item_name = parts[2].strip()
                keys[item_number] = item_name
    return keys

def parse_frequent_patterns(fp_txt):
    patterns = []
    with open(fp_txt, 'r') as f:
        for line in f:
            parts = line.split('#SUP:')
            items = list(map(int, parts[0].strip().split()))
            support = int(parts[1].strip())
            patterns.append((items, support))
    return patterns

def format_patterns(patterns, keys):
    formatted_patterns = []
    for items, support in patterns:
        item_names = [keys[item] for item in items]
        item_names.sort(key=lambda name: item_sort_order[name[-2:]])
        formatted_patterns.append((item_names, support))
    
    formatted_patterns.sort(key=lambda x: (len(x[0]), -x[1]))
    
    return formatted_patterns

def write_to_csv(formatted_patterns, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item_names, support in formatted_patterns:
            writer.writerow(item_names + [support])

def main():
    args = sys.argv[1:]
    if len(args) < 3:
        print("Usage: python format_results.py <keys.txt> <frequent_patterns.txt> <output.csv>")
        sys.exit(1)
    keys_txt = args[0]
    fp_txt = args[1]
    output_csv = args[2]

    keys = parse_keys(keys_txt)
    patterns = parse_frequent_patterns(fp_txt)
    formatted_patterns = format_patterns(patterns, keys)
    write_to_csv(formatted_patterns, output_csv)

if __name__ == "__main__":
    main()