import sys
import pandas as pd
from pathlib import Path

def extract_population_data(directory):
    """
    Recursively search through directory for xlsx files and extract population data.
    Returns a list of tuples containing (neighbourhood_name, population).
    """
    population_data = []
    
    # Use pathlib to recursively find all xlsx files
    for excel_file in Path(directory).rglob('*.xlsx'):
        try:
            # Get neighbourhood name from filename (without extension)
            neighbourhood = excel_file.stem
            
            # Read the Excel file
            df = pd.read_excel(excel_file, header=None)
            
            # Extract population from cell B55 (0-based indexing, so row 54, column 1)
            population = df.iloc[54, 1]
            
            # Convert to integer and handle any potential NaN values
            if pd.notna(population):
                population = int(population)
                population_data.append((neighbourhood, population))
                print(f"Processed {neighbourhood}: Population = {population}")
            else:
                print(f"Warning: No population data found in {excel_file}")
                
        except Exception as e:
            print(f"Error processing {excel_file}: {str(e)}")
            continue
    
    return population_data

def create_summary_spreadsheet(population_data, output_file):
    """
    Create a summary spreadsheet with neighbourhood and population data.
    """
    # Create DataFrame from population data
    df = pd.DataFrame(population_data, columns=['Neighbourhood', 'Population'])
    
    # Sort by neighbourhood name
    df = df.sort_values('Neighbourhood')
    
    # Save to Excel
    df.to_excel(output_file, index=False)
    
    # Print summary statistics
    total_population = df['Population'].sum()
    avg_population = df['Population'].mean()
    print("\nSummary Statistics:")
    print(f"Total Neighbourhoods: {len(df)}")
    print(f"Total Population: {total_population:,.0f}")
    print(f"Average Neighbourhood Population: {avg_population:,.1f}")

def main():
    # Directory containing the census data
    args = sys.argv[1:]
    input_dir = args[0] if args else 'winnipeg_census_2021'
    output_file = 'winnipeg_neighbourhood_populations.xlsx'
    
    print(f"Searching for Excel files in {input_dir}...")
    
    # Extract population data
    population_data = extract_population_data(input_dir)
    
    if population_data:
        print(f"\nCreating summary spreadsheet...")
        create_summary_spreadsheet(population_data, output_file)
        print(f"\nSummary spreadsheet created: {output_file}")
    else:
        print("No population data found.")

if __name__ == "__main__":
    main()