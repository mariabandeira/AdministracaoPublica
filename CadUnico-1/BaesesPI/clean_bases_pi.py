import pandas as pd
import os

def clean_data(file_path):
    # Load the raw data
    df = pd.read_csv(file_path, sep=';', low_memory=False)

    # Perform cleaning operations
    # Example: Drop duplicates
    df.drop_duplicates(inplace=True)

    # Example: Fill missing values
    df.fillna(method='ffill', inplace=True)

    # Example: Rename columns for consistency
    df.rename(columns={'old_column_name': 'new_column_name'}, inplace=True)

    # Save the cleaned data
    cleaned_file_path = os.path.join(os.path.dirname(file_path), 'cadunico_pi_clean.csv')
    df.to_csv(cleaned_file_path, index=False)

if __name__ == "__main__":
    # Specify the path to the raw data file
    raw_data_file = os.path.join(os.path.dirname(__file__), 'BasesAno', 'cadunico_pi_combined.csv')
    clean_data(raw_data_file)