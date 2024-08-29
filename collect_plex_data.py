import sys

import plex.plex_functions as p
import db.db_functions
import db.update_db
import configparser
from loguru import logger

config = configparser.ConfigParser()
config.read('config.ini')

def configure_logging():
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")
    logger.add('run.log', level="DEBUG")


configure_logging()

# Plex
# PLEX_USER = config['SCHROEDER']['username']
# PLEX_PASSWORD = config['SCHROEDER']['password']
# WOODSTOCK = config['WOODSTOCK']['servername']
# SCHROEDER = config['SCHROEDER']['servername']
# WOODSTOCK_LIBRARY = config['WOODSTOCK']['musiclibrary']
# #SCHROEDER_LIBRARY = config['SCHROEDER']['musiclibrary']

if __name__ == "__main__":
    #  Get tracks from Woodstock and populate db with Woodstock data and BPM
#    server = p.plex_connect(PLEX_USER, PLEX_PASSWORD, WOODSTOCK)  # Connect to the Woodstock server
#    tracks = p.get_all_tracks(server, WOODSTOCK_LIBRARY)  # Get all tracks
#    lib_size = tracks[1]
#    track_list = p.listify_track_data(tracks[0], 'woodstock')  # Listify the track data
#    p.export_track_data(track_list, 'track_data.csv', 'woodstock')  # Export the track data
#    db.db_functions.create_track_db()  # Create the SQLite database and table
#    db.db_functions.insert_tracks('track_data.csv')  # Insert the track data into the database
#    db.update_db.update_filepath('track_data.db', 'volume1', 'Volumes') # Change the filepath in the database
#    results = db.db_functions.get_id_location()
#    db.db_functions.export_results(results)
#    db.update_db.process_bpm('id_location.csv')
    #  Get tracks from Schroeder and update db with Schroeder_ids for each track
#    server = p.plex_connect(PLEX_USER, PLEX_PASSWORD, SCHROEDER)  # Connect to Schroeder
#    schroeder_library = p.get_schroeder_library(server)
#    tracks = schroeder_library.searchTracks()  # Get all tracks from Schroeder instead of using get_all_tracks func
#    track_list = p.listify_track_data(tracks, 'schroeder')  # Listify the track data
#    p.export_track_data(track_list, 'second_track_data.csv', 'schroeder')
#    db.update_db.update_filepath("Volumes/Franklin/Media", "volume1/media/Music/Music")
#    db.update_db.update_location_complete("/Volumes/Franklin/Media/Music", "volume1/media/Music/Music")
    db.update_db.update_second_id('second_track_data.csv')
