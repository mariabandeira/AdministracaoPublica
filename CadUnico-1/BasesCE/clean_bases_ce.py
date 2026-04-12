import pandas as pd
import os

def clean_data(input_file, output_file):
    # Load the dataset
    df = pd.read_csv(input_file, sep=';', low_memory=False)

    # Perform data cleaning operations
    # Example: Drop duplicates
    df.drop_duplicates(inplace=True)

    # Example: Fill missing values
    df.fillna(method='ffill', inplace=True)

    # Example: Rename columns for consistency
    df.rename(columns={'old_column_name': 'new_column_name'}, inplace=True)

    # Save the cleaned dataset
    df.to_csv(output_file, sep=';', index=False)

if __name__ == "__main__":
    input_file = 'BasesAno/cadunico_ce_combined.csv'  # Adjust the path as necessary
    output_file = 'cadunico_CE_clean.csv'
    
    clean_data(input_file, output_file)