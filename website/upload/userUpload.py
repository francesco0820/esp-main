import csv
import sys
import os
import sqlite3

# Ensure the esp module can be found by adding the parent directory to sys.path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, parent_dir)

from esp import app
from esp.model import get_db

def upload_users_from_csv(file_path):
    """Upload users to the database from a CSV file."""
    with app.app_context():
        connection = get_db()
        
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            header = reader.fieldnames
            if header[0].startswith('\ufeff'):
                header[0] = header[0].replace('\ufeff', '')
            reader.fieldnames = header

            for row in reader:
                first_name = row.get('First Name')
                last_name = row.get('Last Name')
                company = row.get('Company')
                industry = row.get('Industry')
                position = row.get('Title')
                profile_url = row.get('LinkedIn Profile URL')
                
                # if profile_url:
                #    print(f"Inserting user with profile URL: {profile_url}")

                try:
                    connection.execute(
                        "INSERT OR IGNORE INTO Users (firstName, lastName, company, industry, position, profileUrl) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (first_name, last_name, company, industry, position, profile_url)
                    )
                except sqlite3.IntegrityError:
                    print(f"User {first_name} {last_name} with profile URL {profile_url} already exists.")

        connection.commit()
        print("Users uploaded successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python upload/userUpload.py <path_to_csv_file>")
    else:
        file_path = sys.argv[1]
        upload_users_from_csv(file_path)
