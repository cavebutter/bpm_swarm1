import sys
from db.database import Database
import mysql.connector
import csv
import os
import configparser
from loguru import logger
import datetime

#  TODO Find a way to use the config to provide db connection info
#  TODO Recreate the connect func

config = configparser.ConfigParser()
config.read('config.ini')

database = config['MYSQL']['db_database']
db_path = config['MYSQL']['db_path']
db_user = config['MYSQL']['db_user']
db_password = config['MYSQL']['db_pwd']
db_port = config['MYSQL']['db_port']



def insert_tracks(database: Database, csv_file):
    database.connect()
    query = """
    INSERT INTO track_data (title, artist, album, genre, added_date, filepath, location, woodstock_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            values = (row['title'], row['artist'], row['album'], row['genre'],
                      row['added_date'], row['filepath'], row['location'],
                      row['woodstock_id'])
            database.execute_query(query, values)
            logger.info(f"Inserted track record for {row['woodstock_id']}")


def get_id_location(database: Database, cutoff=None):
    """
    Query the database for the id and location of each track. Replace the beginning of the location
    Args:
        database: Database object
        cutoff: String representing the date to use as a cutoff for the query in 'mmddyyyy' format

    Returns:
        list: List of tuples containing id, woodstock_id, and updated location
    """
    database.connect()
    query_wo_cutoff = "SELECT id, woodstock_id, location FROM track_data"
    query_w_cutoff = "SELECT id, woodstock_id, location FROM track_data WHERE added_date > %s"

    if cutoff is None:
        results = database.execute_select_query(query_wo_cutoff)
        logger.info("Queried db without cutoff")
    else:
        try:
            # Convert cutoff from 'mmddyyyy' to 'yyyy-mm-dd'
            cutoff_date = datetime.datetime.strptime(cutoff, '%m%d%Y').strftime('%Y-%m-%d')
            results = database.execute_select_query(query_w_cutoff, (cutoff_date,))
            logger.info("Queried db with cutoff")
        except Exception as e:
            logger.error(f"There was an error querying db with cutoff: {e}")
            results = []
        finally:
            database.close()

    # Replace the beginning of the location field
    updated_results = [(id, woodstock_id, location.replace('/Volumes/media/Music/Music/', '/mnt/triton/music/')) for id, woodstock_id, location in results]

    logger.debug("Queried DB for id and location with updated paths")
    return updated_results

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


def populate_artists_table(database: Database):
    """
    Populates the artists table with artist names from the track_data table.
    Should only be called once at the beginning of the program.
    Returns:

    """
    db = database.connect()
    query = """
    SELECT DISTINCT artist
    FROM track_data
    """
    artists = db.execute_select_query(query)
    artists_len = len(artists)
    for artist in artists:
        db.execute_query("INSERT INTO artists (artist) VALUES (%s)", (artist[0],))
        logger.info(f"Inserted {artist[0]} into artists table; {artists.index(artist) + 1} of {artists_len}")
    logger.debug("Populated artists table")


def add_artist_id_column(database: Database):
    """
    Replaces the artist column in the track_data table with the artist id from the artists table.
    Should only be called once at the beginning of the program.
    Returns:

    """
    db = database.connect()
    query = """
    ALTER TABLE track_data
    ADD COLUMN artist_id INTEGER,
    ADD FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE
    """
    result = db.execute_query(query)
    logger.debug("Replaced artist column in track_data table")
    return result


def populate_artist_id_column(database: Database):
    """
    Populates the artist_id column in the track_data table with the artist id from the artists table.
    Should only be called once at the beginning of the program.
    Returns:

    """
    db = database.connect()
    query = """
    SELECT id, artist
    FROM artists
    """
    artists = db.execute_select_query(query) # fetchall()
    logger.debug("Queried DB for id and artist")
    update_query = "UPDATE track_data SET artist_id = %s WHERE artist = %s"

    for artist in artists:
        params = (artist[0], artist[1])
        db.execute_query(update_query, params)
        logger.info(f"Updated {artist[1]} in track_data table; {artists.index(artist) + 1} of {len(artists)}")
    logger.debug("Updated artist_id column in track_data table")


def get_last_update_date(database: Database):
    db = database.connect()
    query = "SELECT MAX(date) FROM history"
    result = db.execute_select_query(query)
    result = result[0][0]
    return result