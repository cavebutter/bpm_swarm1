from configparser import ConfigParser
from db.database import Database
import db.update_db as db
import time
from analysis import lastfm as lastfm
from loguru import logger
import sys

config = ConfigParser()
config.read('config.ini')


def configure_logging():
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")
#    logger.add('run.log', level="DEBUG")


LASTFM_API_KEY = config['LASTFM']['api_key']
DATABASE_HOST = config['MYSQL']['db_path']
DATABASE_USER = config['MYSQL']['db_user']
DATABASE_PASSWORD = config['MYSQL']['db_pwd']
DATABASE_DB = config['MYSQL']['db_database']



# Test search and update funcs
if __name__ == '__main__':
    cxn = Database(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, "sandbox")
    cxn.connect()
    configure_logging() # STEP 1
    logger.debug("Step 1: Configure logging")
    lastfm_data = lastfm.get_artist_info('Jethro Tull') # STEP 2
    logger.debug("Step 2: Get artist info")
    query_artist_id = db.get_artist_id(cxn, 'Jethro Tull') # STEP 3
    logger.debug("Step 3: Get artist id")
    mbid = lastfm.get_mbid(lastfm_data) # STEP 4
    logger.debug("Step 4: Get mbid")
    db.insert_artist_mbid(cxn, lastfm_data, 'Jethro Tull') # STEP 5
    logger.debug("Step 5: Insert artist mbid")
    db.insert_artist_genres(cxn, lastfm_data, query_artist_id)  # STEP 6
    logger.debug("Step 6: Insert artist genres")
    similar_artists = lastfm.get_similar_artists(lastfm_data) # STEP 7
    logger.debug("Step 7: Get similar artists")
    for result_artist in similar_artists:
        result_artist_id = db.get_artist_id(cxn, result_artist) # STEP 8
        logger.debug("Step 8: Get artist id")
        if result_artist_id is None: # create row for artist if not exist, fetch mbid, insert into similar_artists
            cxn.execute_query("INSERT INTO artists (artist) VALUES (%s)", (result_artist,)) # STEP 9
            logger.debug("Step 9: Insert artist")
            result_artist_id = db.get_artist_id(cxn, result_artist) # STEP 10
            logger.debug("Step 10: Get artist id")
            result_artist_info = lastfm.get_artist_info(result_artist) # STEP 11
            logger.debug("Step 11: Get artist info")
            result_artist_mbid = lastfm.get_mbid(result_artist_info) # STEP 12
            logger.debug("Step 12: Get mbid")
            db.insert_artist_mbid(cxn, result_artist_info, result_artist)    # STEP 13
            logger.debug("Step 13: Insert artist mbid")
            cxn.execute_query("INSERT INTO similar_artists VALUES (%s, %s)", (result_artist_id, query_artist_id)) # STEP 14
            logger.debug("Step 14: Insert similar artists")
        else:
            params = (result_artist_id, query_artist_id) # STEP 15
            logger.debug("Step 15: Insert similar artists")
            cxn.execute_query("INSERT INTO similar_artists VALUES (%s, %s)", params) # STEP 16
            logger.debug("Step 16: Insert similar artists")