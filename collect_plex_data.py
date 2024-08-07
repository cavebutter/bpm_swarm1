import plex.plex_functions as p
import db.db_functions
import db.update_db


if __name__ == "__main__":
    server = p.plex_connect(p.PLEX_USER, p.PLEX_PASSWORD, p.PLEX_SERVER)  # Connect to the Plex server
    tracks = p.get_all_tracks(server)  # Get all tracks
    track_list = p.listify_track_data(tracks) # Listify the track data
    p.export_track_data(track_list) # Export the track data
    db.db_functions.create_track_db('track_data.db') # Create the SQLite database and table
    db.db_functions.insert_tracks('track_data.csv', 'track_data.db') # Insert the track data into the database
    db.update_db.update_filepath('track_data.db', 'volume1', 'Volumes') # Change the filepath in the database
    results = db.db_functions.get_id_location('track_data.db')
    db.db_functions.export_results(results)
    db.update_db.process_bpm('track_data.db', 'id_location.csv')