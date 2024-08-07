from analysis import bpm
import sqlite3
import csv

def update_bpm(database, track_info: list):
    """
    Iterate through the track_info list, execute the bpm function, and update
    the database with the result.
    :param database:
    :param track_info:
    :return:
    """
    conn = sqlite3.connect(database)
    for track in track_info:
        bperminute = bpm.get_bpm(track[1])
        conn.execute("UPDATE track_data SET bpm = ? WHERE id = ?", (bperminute, track[0]))
        conn.commit()
    conn.close()


def update_filepath(database, original_path: str, new_path: str):
    """
    Update the filepath in the database.
    :param database: Path to the SQLite database file
    :param original_path: The original path substring to replace
    :param new_path: The new path substring to replace with
    :return: None
    """
    update_query = """
    UPDATE track_data
    SET location = REPLACE(location, ?, ?)
    """

    # Connect to the database
    conn = sqlite3.connect(database)
    c = conn.cursor()

    try:
        # Execute the update query with parameters
        c.execute(update_query, (original_path, new_path))

        # Commit the changes
        conn.commit()
        print("File paths updated successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        conn.close()


def process_bpm(database, track_list: csv):
    """
    Read csv file and iterate through rows to update the bpm in the database.
    :param database:
    :param track_list:
    :return:
    """
    conn = sqlite3.connect(database)
    c = conn.cursor()
    with open(track_list, 'r') as f:
        reader = csv.DictReader
        for row in reader(f):
            bpm = bpm.get_bpm(row['filepath'])
            c.execute("UPDATE track_data SET bpm = ? WHERE id = ?", (bpm, row['id']))
            conn.commit()

