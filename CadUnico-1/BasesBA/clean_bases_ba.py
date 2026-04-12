import pandas as pd
import os

def clean_bases_ba():
    # Define the path to the raw data files
    base_path = os.path.join('BasesBA', 'BasesAno')
    
    # List of years to process
    years = range(2012, 2019)
    
    # Initialize an empty DataFrame to hold all cleaned data
    all_data = pd.DataFrame()
    
    for year in years:
        # Construct the file path for the current year's data
        file_path = os.path.join(base_path, f'cadunico_ba_{year}.csv')
        
        # Read the raw data
        df = pd.read_csv(file_path, sep=';', low_memory=False)
        
        # Perform cleaning operations
        # Example cleaning steps (customize as needed):
        df.dropna(inplace=True)  # Drop rows with missing values
        df = df[df['vlr_renda_media_fam'] > 0]  # Keep only rows with positive income
        
        # Add a year column for reference
        df['ano'] = year
        
        # Append the cleaned data to the all_data DataFrame
        all_data = pd.concat([all_data, df], ignore_index=True)
    
    # Save the cleaned data to a new CSV file
    cleaned_file_path = os.path.join('BasesBA', 'cadunico_ba_clean.csv')
    all_data.to_csv(cleaned_file_path, sep=';', index=False)

if __name__ == "__main__":
    clean_bases_ba()