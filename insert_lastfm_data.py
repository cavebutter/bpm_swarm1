from configparser import ConfigParser
from db.database import Database
import db.update_db as db
from analysis import exponential_backoff as exponential_backoff
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
    configure_logging()
    logger.debug("Step 1: Configure logging")
    all_artists = [artist[0] for artist in cxn.execute_select_query("SELECT artist FROM artists")]
    for artist in all_artists:
        retry_num = 0
        while retry_num < 5:
            exponential_backoff(retry_num)
            try:
                lastfm_data = lastfm.get_artist_info(artist)
                query_artist_id = db.get_artist_id(cxn, artist)
                mbid = lastfm.get_mbid(lastfm_data)
                db.insert_artist_mbid(cxn, lastfm_data, artist)
                new_tags = db.process_tags(cxn, lastfm.get_tags(lastfm_data))
                db.insert_artist_genres(cxn, new_tags, query_artist_id)
                similar_artists = lastfm.get_similar_artists(lastfm_data)
                for result_artist in similar_artists:
                    result_artist_id = db.get_artist_id(cxn, result_artist)
                    if result_artist_id is None:
                        cxn.execute_query("INSERT INTO artists (artist) VALUES (%s)", (result_artist,))
                        result_artist_id = db.get_artist_id(cxn, result_artist)
                        result_artist_info = lastfm.get_artist_info(result_artist)
                        result_artist_mbid = lastfm.get_mbid(result_artist_info)
                        if result_artist_mbid is None:
                            continue
                        db.insert_artist_mbid(cxn, result_artist_info, result_artist)
                        cxn.execute_query("INSERT INTO similar_artists (artist_id, similar_artist_id)VALUES (%s, %s)", (query_artist_id, result_artist_id)) # STEP 14
                    else:
                        params = (result_artist_id, query_artist_id)
                        cxn.execute_query("INSERT INTO similar_artists VALUES (%s, %s)", params)
            except Exception as e:
                logger.error(f"Error processing artist data: {e}")
                retry_num += 1
            db.maitain_tags_table(cxn)
        else:
            logger.error(f"Maxium number of retries reached. Skipping artist: {artist}")

    cxn.close()
    logger.debug("Done")