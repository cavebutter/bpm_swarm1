import sys

from analysis import bpm
import mysql.connector
import csv
from loguru import logger

def update_bpm(track_info: list):
    """
    Iterate through the track_info list, execute the bpm function, and update
    the database with the result.
    :param database:
    :param track_info:
    :return:
    """
    try:
        conn = mysql.connector.connect(
            host="athena.eagle-mimosa.ts.net",
            user="jay",
            password="d0ghouse",
            database="bpm_swarm1"
        )
        logger.info("Connected to MySQL DB")
    except Exception as e:
        logger.error(f"Could not connect to MySQL database: {e}")
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
    SET location = REPLACE(location, %s, %s)
    """

    # Connect to the database
    try:
        conn = mysql.connector.connect(
            host="athena.eagle-mimosa.ts.net",
            user="jay",
            password="d0ghouse",
            database="bpm_swarm1"
        )
        logger.info("Connected to MySQL server")
    except Exception as e:
        logger.error(f"Error connecting to MySQL: {e}")
        sys.exit()
    c = conn.cursor()

    try:
        # Execute the update query with parameters
        c.execute(update_query, (original_path, new_path))

        # Commit the changes
        conn.commit()
        logger.debug(f"File path updated successfully: {new_path}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

    finally:
        # Close the connection
        conn.close()


def process_bpm(track_list: csv):
    try:
        conn = mysql.connector.connect(
            host="athena.eagle-mimosa.ts.net",
            user="jay",
            password="d0ghouse",
            database="bpm_swarm1"
        )
        logger.info("Connected to MySQL database")
    except Exception as e:
        logger.error(f"There was an error connecting to MySQL: {e}")
    c = conn.cursor()
    with open(track_list, 'r') as f:
        reader = csv.DictReader(f)
        lib_size = sum(1 for _ in reader)
        logger.debug(f"Library size: {lib_size}")
        i = 1

    with open(track_list, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            track_bpm = bpm.get_bpm(row['location'])
            c.execute("UPDATE track_data SET bpm = %s WHERE id = %s", (track_bpm, row['id']))
            conn.commit()
            logger.info(f"Processed BPM for {row['woodstock_id']}; {i} of {lib_size}")
            i += 1


def update_second_id(filename):
    #  TODO This func needs to iterate through each row of the db, take the `filepath` and do the replace with `filepath` as string, /Volumes.../ as first sub, and `/volume1...` as second
    """
    Consume csv file.  Where csv.location == db.location, update track_data.schroeder_id = csv.id
    Args:
        filename:
    """
    try:
        conn = mysql.connector.connect(
            host="athena.eagle-mimosa.ts.net",
            user="jay",
            password="d0ghouse",
            database="bpm_swarm1"
        )
        logger.info("Connected to MySQL server")
    except Exception as e:
        logger.error(f"There was an error connecting to MySQL server: {e}")
    c = conn.cursor()
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        lib_size = sum(1 for _ in reader)
        i = 1
        with open(filename, 'r') as f:
            reader = csv.DictReader
            try:
                for row in reader(f):
                    c.execute("""
                    UPDATE track_data SET schroeder_id = %s WHERE location = %s""",
                    (row['schroeder_id'], row['location']))
                    conn.commit()
                    logger.info(f"Updated to add schroeder_id: {row['schroeder_id']}. Record {i} of {lib_size}")
                    i += 1
            except Exception as e:
                logger.error(f"Error updating schroeder_id: {row['schroeder_id']}. Record {i} of {lib_size}")
                i += 1
            conn.close()


def update_location_complete(old_str: str, new_str: str):
    # Connect to DB
    try:
        conn = mysql.connector.connect(
            host="athena.eagle-mimosa.ts.net",
            user="jay",
            password="d0ghouse",
            database="bpm_swarm1"
        )
        logger.info("Connected to MySQL server")
    except Exception as e:
        logger.error(f"There was an error connecting to MySQL server: {e}")
    c = conn.cursor()
    c.execute("""SELECT id
              , filepath
              FROM track_data
              """)
    results = c.fetchall()
    i = 1
    record_set = len(results)
    for result in results:
        try:
            c.execute("""
            UPDATE track_data SET track_data.location = REPLACE(filepath, %s, %s) WHERE track_data.id = %s
            """, (old_str, new_str, result[0]))
            conn.commit()
            logger.info(f"Updated {result[0]} to new location; {i} of {record_set}")
            i += 1
        except Exception as e:
            logger.error(f"Error processing {result[0]}: {e}")
            i += 1
    conn.close()