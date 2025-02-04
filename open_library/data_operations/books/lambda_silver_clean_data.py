import os
import csv

def cleanse_data(books):
    """
    Cleanses book data by removing unnecessary brackets from list-formatted fields.
    """
    for book in books:
        for key, value in book.items():
            if isinstance(value, list) and len(value) == 1:
                book[key] = value[0]  # Convert single-item lists to strings
    return books

def clean_csv(input_path, output_path):
    for filename in os.listdir(input_path):
        if filename.startswith("bronze_") and filename.endswith(".csv"):
            input_filepath = os.path.join(input_path, filename)

            # *** KEY CHANGE: Filename replacement ***
            new_filename = filename.replace("bronze_", "silver_")  
            output_filepath = os.path.join(output_path, new_filename)

            with open(input_filepath, 'r', encoding='utf-8') as infile, \
                    open(output_filepath, 'w', newline='', encoding='utf-8') as outfile:

                reader = csv.DictReader(infile)
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()

                books = []
                for row in reader:
                    books.append(row)

                cleaned_books = cleanse_data(books)

                for book in cleaned_books:
                    for key, value in book.items():
                        if isinstance(value, str):
                            cleaned_value = value.strip()
                            if cleaned_value.startswith("[") and cleaned_value.endswith("]"):
                                cleaned_value = cleaned_value[1:-1].strip()
                            cleaned_value = cleaned_value.replace('"', '')
                            cleaned_value = cleaned_value.replace("'", '')
                            book[key] = cleaned_value

                    writer.writerow(book)

            print(f"Cleaned and saved as: {new_filename}")  # Show the *new* filename


if __name__ == "__main__":
    input_directory = os.path.expanduser("~/Desktop/openlibrary/bronze")
    output_directory = os.path.expanduser("~/Desktop/openlibrary/silver")

    os.makedirs(output_directory, exist_ok=True)

    clean_csv(input_directory, output_directory)
    print("Cleaning Complete!")