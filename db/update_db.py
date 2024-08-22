from analysis import bpm
import mysql.connector
import csv

def update_bpm(track_info: list):
    """
    Iterate through the track_info list, execute the bpm function, and update
    the database with the result.
    :param database:
    :param track_info:
    :return:
    """
    conn = mysql.connector.connect(
        host="athena.eagle-mimosa.ts.net",
        user="jay",
        password="d0ghouse",
        database="bpm_swarm1"
    )
    c = conn.cursor()
    for track in track_info:
        bperminute = bpm.get_bpm(track[1])
        c.execute("UPDATE track_data SET bpm = %s WHERE woodstock_id = %s", (bperminute, track[0]))
        c.commit()
    conn.close()


def update_filepath(original_path: str, new_path: str):
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
    conn = mysql.connector.connect(
        host="athena.eagle-mimosa.ts.net",
        user="jay",
        password="d0ghouse",
        database="bpm_swarm1"
    )
    c = conn.cursor()

    try:
        # Execute the update query with parameters
        c.execute(update_query, (original_path, new_path))

        # Commit the changes
        conn.commit()
        print("File paths updated successfully.")

    except:
        print("An error occurred")

    finally:
        # Close the connection
        conn.close()


def process_bpm(track_list: csv):
    """
    Read csv file and iterate through rows to update the bpm in the database.
    :param database:
    :param track_list:
    :return:
    """
    conn = mysql.connector.connect(
        host="athena.eagle-mimosa.ts.net",
        user="jay",
        password="d0ghouse",
        database="bpm_swarm1"
    )
    c = conn.cursor()
    with open(track_list, 'r') as f:
        reader = csv.DictReader
        for row in reader(f):
            track_bpm = bpm.get_bpm(row['location'])
            c.execute("UPDATE track_data SET bpm = %s WHERE id = %s", (track_bpm, row['id']))
            conn.commit()

    print("Updated BPM!")