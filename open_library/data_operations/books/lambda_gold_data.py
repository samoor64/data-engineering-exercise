import os
import pandas as pd

def process_csv_files(input_directory, output_directory):
    """

    Cleans CSV files in the input directory by removing duplicates by author key and title and rows with missing author keys.

    """
    if not os.path.exists(input_directory):
        print(f"Directory {input_directory} does not exist.")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # List all CSV files in the directory
    csv_files = [f for f in os.listdir(input_directory) if f.endswith(".csv")]
    
    if not csv_files:
        print("No CSV files found in the directory.")
        return
    
    for file in csv_files:
        file_path = os.path.join(input_directory, file)
        
        # Read CSV into DataFrame
        df = pd.read_csv(file_path)
        
        if 'author_key' not in df.columns:
            print(f"Skipping {file}: 'author_key' column not found.")
            continue
        
        df = df.dropna(subset=['author_key'])
        
        df = df.drop_duplicates(subset=['author_key', 'title'])
        
        # Open Library seems to be returning bad data that concats author keys with commas - this cleans that up
        df = df[~df['author_key'].str.contains(',', na=False)]

        print(f"Processed {file}: {df.shape[0]} rows after cleaning.")
        
        new_file_name = file.replace("silver_", "gold_")
        output_file = os.path.join(output_directory, new_file_name)
        
        df.to_csv(output_file, index=False)
        print(f"Saved cleaned file: {output_file}")

if __name__ == "__main__":
    input_directory_path = os.path.expanduser("~/Desktop/openlibrary/silver")
    output_directory_path = os.path.expanduser("~/Desktop/openlibrary/gold")
    process_csv_files(input_directory_path, output_directory_path)