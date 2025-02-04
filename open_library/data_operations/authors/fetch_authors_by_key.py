import os
import json
import pandas as pd
import requests

# Set file paths
DESKTOP_PATH = os.path.expanduser("~/Desktop")
OPENLIBRARY_FOLDER = os.path.join(DESKTOP_PATH, "openlibrary/gold")
input_csv_path = os.path.join(OPENLIBRARY_FOLDER, "gold_openlibrary_books_2025-02-03_20-33-25.csv")  # Change if the file has a different name
output_csv_path = os.path.join(OPENLIBRARY_FOLDER, "authors_data.csv")

# Read distinct author_keys from CSV
df = pd.read_csv(input_csv_path)
author_keys = df['author_key'].drop_duplicates().tolist()

# Function to get selected author data from OpenLibrary API
def fetch_author_data(author_key):
    url = f"https://openlibrary.org/authors/{author_key}.json"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for non-200 responses
        data = response.json()
        return {
            "name": data.get("name"),
            "death_date": data.get("death_date"),
            "key": data.get("key").split("/")[-1],
            "birth_date": data.get("birth_date"),
            "isni": data.get("remote_ids", {}).get("isni"),
            "viaf": data.get("remote_ids", {}).get("viaf"),
            "wikidata": data.get("remote_ids", {}).get("wikidata"),
            "created": data.get("created", {}).get("value"),
            "last_modified": data.get("last_modified", {}).get("value")
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {author_key}: {e}")
        return None

# Fetch data for all authors
author_data_list = [fetch_author_data(key) for key in author_keys]

# Remove None values (failed API calls)
author_data_list = [data for data in author_data_list if data]

# Convert to DataFrame and save as CSV
if author_data_list:
    df_output = pd.DataFrame(author_data_list)
    df_output.to_csv(output_csv_path, index=False)
    print(f"Data saved to {output_csv_path}")
else:
    print("No valid data retrieved.")
