# COMP 4710: Data Mining - Research Project
This repository contains the source code for the data preprocessing and analysis steps conducted for a research paper as part of COMP 4710: Data Mining.

# Dataset
The original dataset used by the scripts is the 311 Service Request data up until October 2, 2024, stored as a CSV file. This file can be accessed [here](https://drive.google.com/file/d/1eacVh37akPoYrC0frFga439dOGj7VbX3/view?usp=drive_link).

# Requirements
- To execute Step 3 of Finding Frequent Patterns, the SPMF library is required (https://www.philippe-fournier-viger.com/spmf/index.php?link=download.php). Download the "Release Version" of SPMF as `spmf.jar` and ensure a compatible version of Java is installed.

- To execute Step 1 of Scraping Neighbourhood Populations, the `requests` and `BeautifulSoup` libraries are required.
   To install them, run:
   ```
   pip install requests beautifulsoup4
   ```

# Finding Frequent Patterns
The following steps outline the process to extract frequent patterns within the dataset. Each script file includes comments at the top detailing its purpose and command line arguments.

1. **Clean 311 dataset**:
   ```
   python clean_for_fp.py <input_csv_file>
   ```
2. **Format cleaned dataset for SPMF library**:
   ```
   python format.py <input_csv_file>
   ```
3. **Run FP-Growth algorithm**:
   - Open the SPMF Graphical User Interface by running the `spmf.jar` file.
   - Select `FPGrowth_itemsets` as the algorithm.
   - Use the output CSV file (`formatted_data.txt`) from the previous step as the input file.
   - Set the output file location and name in .txt format (e.g., `results_alpha_0.007.txt`).
   - Set a suitable Minsup value; 0.007 was used for this project.
   - Click "Run algorithm".
4. **Format frequent pattern results**:
   ```
   python format_results.py <keys.txt> <results.txt> <output.csv>
   ```

# Scraping Winnipeg Neighbourhood Population Figures
The following steps outline how the population data for Winnipeg's neighbourhoods were gathered. Each script file includes comments at the top detailing its purpose and command line arguments.

1. **Scrape Neighbourhood Populations:**
Running this script will download all the Excel files containing census data for each neighbourhood in Winnipeg.
    ```
    python scrape_census.py
    ```
2. **Parse Populations**:
This step extracts the population figure from each Excel file and produces a CSV with all the 
neighbourhood populations at the end.
    ```
    python parse_population.py <directory_containing_excel_files>
    ```
