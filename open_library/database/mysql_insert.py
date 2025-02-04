import mysql.connector
import csv
import os
import argparse

def insert_data_into_mysql(csv_filepath, db_config, table_name):
    """Inserts data from a CSV file into a MySQL database."""

    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()

        with open(csv_filepath, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames

            placeholders = ", ".join(["%s"] * len(fieldnames))
            sql = f"INSERT INTO {table_name} ({', '.join(fieldnames)}) VALUES ({placeholders})"


            for row in reader:
                values = [row[field] for field in fieldnames]
                try:
                    mycursor.execute(sql, values)
                except mysql.connector.Error as err:
                    print(f"Error inserting row: {row}")
                    print(f"MySQL Error: {err}")
                    mydb.rollback()
                    return

            mydb.commit()
            print(f"Data from {csv_filepath} inserted successfully into {table_name}")

    except mysql.connector.Error as err:
        print(f"MySQL connection error: {err}")

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert CSV data into MySQL.")
    parser.add_argument("--csv_file", required=True, help="Path to the CSV file")
    parser.add_argument("--table_name", required=True, help="Name of the MySQL table")
    parser.add_argument("--db_user", required=True, help="MySQL database user")
    parser.add_argument("--db_password", required=True, help="MySQL database password")
    parser.add_argument("--db_host", required=True, help="MySQL database host")
    parser.add_argument("--db_name", required=True, help="MySQL database name")

    args = parser.parse_args()

    db_config = {
        "user": args.db_user,
        "password": args.db_password,
        "host": args.db_host,
        "database": args.db_name,
    }

    insert_data_into_mysql(args.csv_file, db_config, args.table_name)