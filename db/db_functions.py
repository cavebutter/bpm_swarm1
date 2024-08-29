import sys

import mysql.connector
import csv
import os
import configparser
from loguru import logger

#  TODO Find a way to use the config to provide database connection info
#  TODO Recreate the connect func

config = configparser.ConfigParser()
config.read('config.ini')

database = config['MYSQL']['db_database']
db_path = config['MYSQL']['db_path']
db_user = config['MYSQL']['db_user']
db_password = config['MYSQL']['db_pwd']


def create_track_db():
    """
    Creates a SQLite database for track data.

    Parameters:
    None

    Returns:
    None
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
        sys.exit()
    c = conn.cursor()
    try:
        c.execute("DROP TABLE IF EXISTS track_data")
        logger.debug("Dropped track_data table")
    except Exception as e:
        logger.error(f"There was an error dropping table `track_data`: {e}")
        sys.exit()
    c.execute('''CREATE TABLE IF NOT EXISTS track_data
                 (id INTEGER AUTO_INCREMENT PRIMARY KEY
                 , title VARCHAR (1000)
                 , artist VARCHAR (1000)
                 , album VARCHAR (1000)
                 , genre VARCHAR (500)
                 , added_date VARCHAR (500)
                 , filepath VARCHAR (1000)
                 , location VARCHAR (1000)
                 , schroeder_id INTEGER
                 , woodstock_id INTEGER
                 , bpm FLOAT )''')
    logger.debug("Created track_data table")
    c.execute('''CREATE INDEX ws_ix
    ON track_data (woodstock_id)''')
    logger.debug("Created index `woodstock_ix")
    c.execute('''CREATE INDEX schroeder_ix
    ON track_data (schroeder_id)''')
    logger.debug("Created index `schroeder_ix")
#   c.execute('''CREATE INDEX loc_ix
#    ON track_data (location)''')
#    logger.debug("Created index loc_ix")
    conn.commit()
    conn.close()


def restart():
    conn = mysql.connector.connect(
        host="athena.eagle-mimosa.ts.net",
        user="jay",
        password="d0ghouse",
        database="bpm_swarm1"
    )
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS track_data")
    c.close()


def insert_tracks(csv_file):
    """
    Inserts track data from a CSV file into the SQLite database.

    Parameters:
    csv_file (str): The path to the CSV file.

    Returns:
    None
    """
    conn = mysql.connector.connect(
        host="athena.eagle-mimosa.ts.net",
        user="jay",
        password="d0ghouse",
        database="bpm_swarm1"
    )
    c = conn.cursor()
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            c.execute("INSERT INTO track_data (title, artist, album, genre, "
                      "added_date, filepath, location, woodstock_id)VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                      (row['title'], row['artist'], row['album'], row['genre'],
                       row['added_date'], row['filepath'], row['location'], row['woodstock_id']))
    conn.commit()
    conn.close()
    print("Inserted track records in database!")


def get_id_location():
    """
    Gets the track ID and location from the SQLite database.

    Parameters:
    DATABASE (str): The path to the SQLite database.

    Returns:
    list: A list of tuples containing the track ID and location.
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
        sys.exit()
    c = conn.cursor()
    c.execute("SELECT id, woodstock_id, location FROM track_data")
    results = c.fetchall()
    conn.close()
    logger.debug("Queried DB for id and location")
    return results


def export_results(results: list, file_path: str = 'id_location.csv'):
    """
    Export the results of a query to a CSV file. 'results' is a list of tuples.
    :param results: List of tuples containing the data to be written to CSV
    :param file_path: Path to the CSV file
    :return: None
    """
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as csvfile:
        fieldnames = ['id', 'woodstock_id', 'location']
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
    logger.info("Exported ID and Location to CSV")


def create_artists_table():
    """
    Creates an artists table in the MySQL database. Should only be called once
    at the beginning of the program.
    Returns:

    """
    try:
        conn = mysql.connector.connect(
        host="athena.eagle-mimosa.ts.net",
        user="jay",
        password="d0ghouse",
        database="bpm_swarm1"
    )
        logger.debug("Connected to MySQL server")
    except Exception as e:
        logger.error(f"There was an error connecting to MySQL server: {e}")
        sys.exit()
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS artists''')
    c.execute('''CREATE TABLE IF NOT EXISTS artists
                 (id INTEGER PRIMARY KEY AUTO_INCREMENT
                 , artist VARCHAR(255) NOT NULL
                 , last_fm_id VARCHAR(255)
                 , discogs_id VARCHAR(255)
                 , musicbrainz_id VARCHAR(255))''')
    conn.commit()
    conn.close()
    logger.debug("Created artists table")


def populate_artists_table():
    """
    Populates the artists table with artist names from the track_data table.
    Should only be called once at the beginning of the program.
    Returns:

    """
    try:
        conn = mysql.connector.connect(
        host="athena.eagle-mimosa.ts.net",
        user="jay",
        password="d0ghouse",
        database="bpm_swarm1"
    )
        logger.debug("Connected to MySQL server")
    except Exception as e:
        logger.error(f"There was an error connecting to MySQL server: {e}")
        sys.exit()
    c = conn.cursor()
    c.execute("""
    SELECT DISTINCT artist
    FROM track_data
    """)
    artists = c.fetchall()
    artists_len = len(artists)
    for artist in artists:
        c.execute("INSERT INTO artists (artist) VALUES (%s)", (artist[0],))
        logger.info(f"Inserted {artist[0]} into artists table; {artists.index(artist) + 1} of {artists_len}")
    conn.commit()
    conn.close()
    logger.debug("Populated artists table")


def add_artist_id_column():
    """
    Replaces the artist column in the track_data table with the artist id from the artists table.
    Should only be called once at the beginning of the program.
    Returns:

    """
    try:
        conn = mysql.connector.connect(
        host="athena.eagle-mimosa.ts.net",
        user="jay",
        password="d0ghouse",
        database="bpm_swarm1"
    )
        logger.debug("Connected to MySQL server")
    except Exception as e:
        logger.error(f"There was an error connecting to MySQL server: {e}")
        sys.exit()
    c = conn.cursor()
    c.execute("""
    ALTER TABLE track_data
    ADD COLUMN artist_id INTEGER,
    ADD FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE
    """)
    conn.commit()
    conn.close()
    logger.debug("Replaced artist column in track_data table")


def populate_artist_id_column():
    """
    Populates the artist_id column in the track_data table with the artist id from the artists table.
    Should only be called once at the beginning of the program.
    Returns:

    """
    try:
        conn = mysql.connector.connect(
        host="athena.eagle-mimosa.ts.net",
        user="jay",
        password="d0ghouse",
        database="bpm_swarm1"
    )
        logger.debug("Connected to MySQL server")
    except Exception as e:
        logger.error(f"There was an error connecting to MySQL server: {e}")
        sys.exit()
    c = conn.cursor()
    c.execute("""
    SELECT id, artist
    FROM artists
    """)
    artists = c.fetchall()
    logger.debug("Queried DB for id and artist")
    for artist in artists:
        c.execute("UPDATE track_data SET artist_id = %s WHERE artist = %s", (artist[0], artist[1]))
        logger.info(f"Updated {artist[1]} in track_data table; {artists.index(artist) + 1} of {len(artists)}")
    conn.commit()
    logger.debug("Updated artist_id column in track_data table")
    conn.close()
    logger.debug("Closed Connection")