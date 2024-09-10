import sys
from db.database import Database
from analysis import bpm, lastfm
import mysql.connector
import csv
from loguru import logger
import json

def update_bpm(database: Database, track_info: list):
    """
    Iterate through the track_info list, execute the bpm function, and update
    the db with the result.
    :param db:
    :param track_info:
    :return:
    """
    db = database.connect()
    for track in track_info:
        bperminute = bpm.get_bpm(track[1])
        query = "UPDATE track_data SET bpm = %s WHERE woodstock_id = %s"
        params = (bperminute, track[0])
        db.execute_query(query, params)
        logger.info(f"Updated bpm for track {track[0]}")
    db.close()


def update_filepath(database: Database, original_path: str, new_path: str):
    """
    Updates the filepath in the track_data table by replacing the original_path with the new_path.

    :param database: The Database object used to connect to the database.
    :param original_path: The original path to be replaced.
    :param new_path: The new path that will replace the original_path.
    """
    update_query = """
    UPDATE track_data
    SET location = REPLACE(location, %s, %s)
    """
    db = database.connect()
    db.execute_query(update_query, (original_path, new_path))
    db.close()

def process_bpm(database: Database, track_list: csv):
    """
    Process the BPM for each track in the track list and update the 'bpm' field in the database.

    Parameters:
    database (Database): The database connection object.
    track_list (csv): The list of tracks to process BPM for.

    Returns:
    None
    """
    db = database.connect()
    with open(track_list, 'r') as f:
        reader = csv.DictReader(f)
        lib_size = sum(1 for _ in reader)
        logger.debug(f"Library size: {lib_size}")
        i = 1

    with open(track_list, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            track_bpm = bpm.get_bpm(row['location'])
            db.execute_query("UPDATE track_data SET bpm = %s WHERE id = %s", (track_bpm, row['id']))
            logger.info(f"Processed BPM for {row['woodstock_id']}; {i} of {lib_size}")
            i += 1
    db.close()

def update_second_id(database: Database, filename: str):
    """
    Updates the second ID in the track_data table based on the provided schroeder_id and location.

    Parameters:
    database (Database): The database connection object.
    filename (str): The name of the file containing the data to update.

    Returns:
    None
    """
    db = database.connect()
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        lib_size = sum(1 for _ in reader)
        i = 1
        with open(filename, 'r') as f:
            reader = csv.DictReader
            query = "UPDATE track_data SET schroeder_id = %s WHERE location = %s"
            try:
                for row in reader(f):
                    params = (row['schroeder_id'], row['location'])
                    db.execute_query(query, params)
                    logger.info(f"Updated to add schroeder_id: {row['schroeder_id']}. Record {i} of {lib_size}")
                    i += 1
            except Exception as e:
                logger.error(f"Error updating schroeder_id: {row['schroeder_id']}. Record {i} of {lib_size}")
                i += 1
    db.close()


def update_location_complete(database: Database, old_str: str, new_str: str):
    """
    Updates the location in the track_data table by replacing the old_str with the new_str.

    Parameters:
    database (Database): The Database object used to connect to the database.
    old_str (str): The original string to be replaced.
    new_str (str): The new string that will replace the old_str.

    Returns:
    None
    """
    db = database.connect()
    query = """SELECT id
              , filepath
              FROM track_data
              """
    results = db.execute_select_query(query)
    i = 1
    record_set = len(results)
    for result in results:
        try:
            update_query = """
            UPDATE track_data SET track_data.location = REPLACE(filepath, %s, %s) WHERE track_data.id = %s
            """
            params = (old_str, new_str, result[0])
            db.execute_query(update_query, params)
            logger.info(f"Updated {result[0]} to new location; {i} of {record_set}")
            i += 1
        except Exception as e:
            logger.error(f"Error processing {result[0]}: {e}")
            i += 1
        finally:
            db.close()


def insert_artist_mbid(database: Database, result: json, artist_name: str):
    """
    Updates the MusicBrainz ID (MBID) of the artist in the database if it is not already present.

    Parameters:
    database (Database): The Database object used to connect to the database.
    result (json): The JSON object containing information about the artist.
    artist_name (str): The name of the artist.

    Returns:
    None
    """
    database.connect()

    # Check if MBID is already in the database
    current_mbid = get_current_mbid_from_db(database, artist_name)
    if current_mbid is not None:
        logger.info(
            f"MBID for {artist_name} already exists in the database. Skipping update.")
        database.close()
        return

    # If MBID is not in the database, update it
    mbid = lastfm.get_mbid(result)
    query = "UPDATE artists SET musicbrainz_id = %s WHERE artist = %s"
    params = (mbid, artist_name)
    database.execute_query(query, params)
    logger.info(f"Updated {artist_name} to new MBID: {mbid}")

    database.close()


def get_current_mbid_from_db(database: Database, artist_name: str) -> str:
    """
    Retrieves the current MusicBrainz ID (MBID) for the artist from the database.

    Parameters:
    database (Database): The Database object used to connect to the database.
    artist_name (str): The name of the artist.

    Returns:
    str: The current MusicBrainz ID (MBID) if found, None otherwise.
    """
    query = "SELECT musicbrainz_id FROM artists WHERE artist = %s"
    params = (artist_name,)
    result = database.execute_select_query(query, params)

    if result:
        return result[0][0]
    return None


def insert_artist_genres(database: Database, new_tags: list, artist_id: int):
    database.connect()
    for tag in new_tags:
        genre_id = get_genre_id(database, tag)  # Assuming a function get_genre_id is implemented to retrieve genre_id
        if genre_id is not None:
            query = "INSERT INTO tags (artist_id, tag) VALUES (%s, %s)"
            params = (artist_id, genre_id)
            database.execute_query(query, params)
            logger.info(f"Inserted {tag} for {artist_id}")
        else:
            logger.warning(f"Genre ID not found for tag: {tag}")
    database.close()

def get_genre_id(database: Database, tag: str) -> int:
    query = "SELECT id FROM genres WHERE genre = %s"
    params = [tag]
    result = database.execute_select_query(query, params)
    if result:
        return result[0][0]
    else:
        logger.warning(f"Genre ID not found for genre: {tag}")
        return None


def get_artist_id(database: Database, artist_name: str) -> int:
    """
    Retrieves the ID of an artist from the database based on the artist name.

    Parameters:
    database (Database): The Database object used to connect to the database.
    artist_name (str): The name of the artist.

    Returns:
    int: The ID of the artist if found, None otherwise.
    """
    database.connect()
    query = "SELECT id FROM artists WHERE artist = %s"
    params = [artist_name]
    result = database.execute_select_query(query, params)
    if not result:
        result = None
        logger.debug(f"No artist id found for {artist_name}")
    else:
        result = result[0][0]
        logger.debug(f"Got artist id: {result}")
    database.close()
    return result


def process_tags(database: Database, tags_list: list):
    """
    Query the tags table.  Compare tags in list to tags in database. If tag is
    not in database, convert it to .lower() and insert it into the database.
    Args:
        database:
        tags:

    Returns: bool

    """
    database.connect()
#    tags = lastfm.get_tags(result)
    processed_tags = [tag.lower() for tag in tags_list]
    for tag in processed_tags:
        query = "SELECT id FROM genres WHERE genre = %s"
        params = [tag]
        tags_query = database.execute_select_query(query, params)
        logger.debug(f"Result: {tags_query}")
        if not tags_query:
            insert_query = "INSERT INTO genres (genre) VALUES (%s)"
            insert_params = [tag]
            database.execute_query(insert_query, insert_params)
            logger.info(f"Inserted new tag: {tag}")
    database.close()
    return processed_tags
