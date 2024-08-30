from loguru import logger
import sys
import plex.plex_functions as p
import db.db_functions
import db.update_db
import configparser


def configure_logging():
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")
    logger.add('run.log', level="DEBUG")

configure_logging()

config = configparser.ConfigParser()
config.read('config.ini')

PLEX_USER = config['WOODSTOCK']['username']
PLEX_PASSWORD = config['WOODSTOCK']['password']
WOODSTOCK = config['WOODSTOCK']['servername']
WOODSTOCK_LIBRARY = config['WOODSTOCK']['musiclibrary']
SCHROEDER_LIBRARY = config['SCHROEDER']['musiclibrary']

if __name__ == '__main__':
    #  Get new tracks from Woodstock and insert into db
    server = p.plex_connect(PLEX_USER, PLEX_PASSWORD, WOODSTOCK)
    results, cutoff = p.fetch_recent(server, WOODSTOCK_LIBRARY)
    track_list = p.listify_track_data(results, 'woodstock')
    p.export_track_data(track_list, 'woodstock_update.csv', 'woodstock')
    db.db_functions.insert_tracks('woodstock_update.csv')
    # Track Analysis
    results = db.db_functions.get_id_location(cutoff)
    db.db_functions.export_results(results, 'woodstock_id_location_update.csv')
    db.update_db.process_bpm('woodstock_id_location_update.csv')
    #  Update artists table
    db.db_functions.populate_artists_table()
    #  Update artist_id column
    db.db_functions.populate_artist_id_column()
