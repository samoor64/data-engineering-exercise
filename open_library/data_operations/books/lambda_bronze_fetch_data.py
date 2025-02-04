import requests
import csv
import boto3
from io import StringIO
import os
import datetime

# Get the current timestamp
current_datetime = datetime.datetime.now()
timestamp_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

DATA_LAYER = "bronze"

# List of subjects to query
SUBJECTS = ["love", "science", "history", "technology"]

S3_BUCKET = "<your-s3-bucket-name>"
S3_FILE_KEY = f"openlibrary_books_{timestamp_str}.csv"

# Define local file path (single CSV file for all subjects)
DESKTOP_PATH = os.path.expanduser("~/Desktop")
OPENLIBRARY_FOLDER = os.path.join(DESKTOP_PATH, f"openlibrary/{DATA_LAYER}")
LOCAL_FILE_PATH = os.path.join(OPENLIBRARY_FOLDER, f"{DATA_LAYER}_openlibrary_books_{timestamp_str}.csv")

# Ensure the folder exists
os.makedirs(OPENLIBRARY_FOLDER, exist_ok=True)

def fetch_data(subjects):
    """
    Fetches data from the Open Library API for multiple subjects.
    Returns a flat list of book records with the subject included.
    """
    results = []

    for subject in subjects:
        api_url = f"https://openlibrary.org/search.json?subject={subject}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            books = data.get("docs", [])

            # Add the subject field to each book record
            for book in books:
                book["subject"] = subject

            results.extend(books)
        else:
            print(f"Failed to fetch data for subject: {subject}")

    return results

def write_to_csv(file_path, books):
    """
    Writes book data to a single CSV file.
    Dynamically determines column names from available keys.
    """
    if not books:
        print("No book data to write")
        return
    
    # Determine all unique keys in the book data
    all_keys = set()
    for book in books:
        if isinstance(book, dict):  # Ensure book is a dictionary before accessing keys
            all_keys.update(book.keys())

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=sorted(all_keys))
        writer.writeheader()
        writer.writerows(books)
    
    print(f"Data successfully written to {file_path}")

def write_to_s3(bucket, file_key, books):
    """
    Uploads the CSV file to an S3 bucket.
    """
    if not books:
        print("No book data available to write to S3.")
        return
    
    s3 = boto3.client('s3')
    csv_buffer = StringIO()
    
    all_keys = set()
    for book in books:
        if isinstance(book, dict):
            all_keys.update(book.keys())
    
    writer = csv.DictWriter(csv_buffer, fieldnames=sorted(all_keys))
    writer.writeheader()
    writer.writerows(books)
    
    s3.put_object(Bucket=bucket, Key=file_key, Body=csv_buffer.getvalue())
    print(f"Data successfully uploaded to s3://{bucket}/{file_key}")

def main():
    """
    Main function to fetch data, write it to a single CSV, and upload to S3.
    """
    books_data = fetch_data(SUBJECTS)
    write_to_csv(LOCAL_FILE_PATH, books_data)
    
    # Uncomment below line to enable S3 upload
    # write_to_s3(S3_BUCKET, S3_FILE_KEY, books_data)

if __name__ == "__main__":
    main()
