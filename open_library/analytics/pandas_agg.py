import os
import glob
import pandas as pd

def get_most_recent_csv(path: str) -> str:
    """
    Returns the most recent CSV file in the given directory.
    
    :param path: Path to the directory to search for CSV files.
    :return: Path to the most recent CSV file or None if no CSV files are found.
    """
    path = os.path.expanduser(path)
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    if not csv_files:
        print("No CSV files found in the directory.")
        return None

    return max(csv_files, key=os.path.getmtime)

def read_csv_from_desktop():
    """Reads the most recent CSV file from the Desktop using pandas."""

    csv_filepath = get_most_recent_csv("~/Desktop/openlibrary/silver")

    if csv_filepath:
        try:
            df = pd.read_csv(csv_filepath)

            print(f"\nReading CSV File: {csv_filepath}")
            print("\nFirst 5 rows:")
            print(df.head())

            print("\nDataFrame Info:")
            df.info()

            print("\nDescriptive Statistics (for numeric columns):")
            print(df.describe())

        except FileNotFoundError:
            print(f"Error: CSV file not found at {csv_filepath}")
        except pd.errors.ParserError:
            print(f"Error parsing the CSV file at {csv_filepath}. Check the file format.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    read_csv_from_desktop()
