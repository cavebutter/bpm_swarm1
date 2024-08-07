import sqlite3
import csv

database = 'track_data.db'
def create_track_db(database):
    """
    Creates a SQLite database for track data.

    Parameters:
    None

    Returns:
    None
    """
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS track_data
                 (title text, artist text, album text, genre text, added_date text,
                  filepath text, location text, id integer NOT NULL PRIMARY KEY,
                  bpm real)''')
    conn.commit()
    conn.close()


def insert_tracks(csv_file, database):
    """
    Inserts track data from a CSV file into the SQLite database.

    Parameters:
    csv_file (str): The path to the CSV file.

    Returns:
    None
    """
    conn = sqlite3.connect(database)
    c = conn.cursor()
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            c.execute("INSERT OR IGNORE INTO track_data (title, artist, album, genre, "
                      "added_date, filepath, location, id)VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (row['title'], row['artist'], row['album'], row['genre'],
                       row['added_date'], row['filepath'], row['location'], row['id']))
    conn.commit()
    conn.close()


def get_id_location(database):
    """
    Gets the track ID and location from the SQLite database.

    Parameters:
    DATABASE (str): The path to the SQLite database.

    Returns:
    list: A list of tuples containing the track ID and location.
    """
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT id, location FROM track_data")
    results = c.fetchall()
    conn.close()
    return results


import csv
import os

def export_results(results: list, file_path: str = 'id_location.csv'):
    """
    Export the results of a query to a CSV file. 'results' is a list of tuples.
    :param results: List of tuples containing the data to be written to CSV
    :param file_path: Path to the CSV file
    :return: None
    """
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as csvfile:
        fieldnames = ['id', 'location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header only if the file does not exist
        if not file_exists:
            writer.writeheader()

        # Iterate over each tuple in the results list
        for element in results:
            # Convert the tuple to a dictionary
            row_dict = dict(zip(fieldnames, element))
            # Write the dictionary to the CSV
            writer.writerow(row_dict)

