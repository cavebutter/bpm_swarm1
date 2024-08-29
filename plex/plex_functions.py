import plexapi
from plexapi.myplex import MyPlexAccount
import plexapi.exceptions
import plexapi.library
import plexapi.playlist
from plexapi.server import PlexServer
import configparser
from datetime import datetime
import csv
from loguru import logger
import sys

config = configparser.ConfigParser()
config.read('config.ini')

PLEX_USER = config['WOODSTOCK']['username']
PLEX_PASSWORD = config['WOODSTOCK']['password']
PLEX_SERVER = config['WOODSTOCK']['servername']
MUSIC_LIBRARY = config['WOODSTOCK']['musiclibrary']
SCHROEDER_LIBRARY = config['SCHROEDER']['musiclibrary']

def plex_connect(PLEX_USER, PLEX_PASSWORD, PLEX_SERVER):
    """
    Connects to a Plex server using the provided user credentials and server name.

    Parameters:
    PLEX_USER (str): The username for the Plex account.
    PLEX_PASSWORD (str): The password for the Plex account.
    PLEX_SERVER (str): The name of the Plex server to connect to.

    Returns:
    PlexServer: The connected Plex server object.
    """
    account = MyPlexAccount(PLEX_USER, PLEX_PASSWORD)
    try:
        server = account.resource(PLEX_SERVER).connect()
        logger.info(f"Connected to Plex Server:  {PLEX_SERVER}")
        return server
    except Exception as e:
        logger.error(f"Error connecting to Plex server {PLEX_SERVER}: {e}")
        sys.exit()


def get_music_library(server, library):
    """
    Finds the music library in the provided Plex server.

    Parameters:
    server (PlexServer): The connected Plex server object.

    Returns:
    plexapi.library.Library: The music library object.
    """
    try:
        music_library = server.library.section(library)
        logger.debug(f"Retrieved Woodstock music library")
        return music_library
    except Exception as e:
        logger.error(f"Could not retrieve Woodstock library: {e}")
        sys.exit()


def get_schroeder_library(server):
    """
    Finds the music library in the provided Plex server.

    Parameters:
    server (PlexServer): The connected Plex server object.

    Returns:
    plexapi.library.Library: The music library object.
    """
    try:
        sections = server.library.sections()
        music_library = sections[4]
        logger.debug(f"Retrieved Schroeder music library.")
        return music_library
    except Exception as e:
        logger.error(f"Could not retrieve Schroeder music library: {e}")
        sys.exit()

def get_all_tracks(server, library):
    #  TODO This func works fine on Woodstock but on Schroeder returns AttributeError: MusicSection object has no \
    #   attribute 'lower'.  The individual statements in this func work fine on Schroeder.
    """
    Gets all tracks from the music library in the provided Plex server.

    Parameters:
    server (PlexServer): The connected Plex server object.
    music_library (plexapi.library.Library): The music library object.

    Returns:
    list: A list of all tracks in the music library.
    int: length
    """
    try:
        library = get_music_library(server, library)
        tracks = library.searchTracks()
        library_size = len(tracks)
        logger.info(f"Retrieved tracks. {library_size} tracks in total.")
        return tracks, library_size
    except Exception as e:
        logger.error(f"There was an error getting all tracks: {e}")
        sys.exit()

def extract_track_data(track, server_name: str):
    """
    Extracts the track data from the provided track.

    Parameters:
    track (plexapi.audio.Track): The track object to extract data from.

    Returns:
    dict: A dictionary containing the track data.
    """
    server_id = server_name + '_id'
    genre_list = []
    for genre in track.genres:
        genre_list.append(genre.tag)
    added_date = track.addedAt.strftime('%Y-%m-%d')
    for media in track.media:
        for part in media.parts:
            filepath = part.file
    track_data = {
        'title': track.title,
        'artist': track.artist().title,
        'album': track.album().title,
        'genre': genre_list,
        'added_date': added_date,
        'filepath': filepath,
        'location': track.locations[0],
        server_id: int(track.ratingKey)  # This should probably be `plex_id` so we can use it for both servers.
    }
    return track_data


def listify_track_data(tracks, server_name: str):
    """
    Lists the track data from the provided list of tracks.

    Parameters:
    tracks (list): A list of track objects to extract data from.

    Returns:
    list: A list of dictionaries containing the track data.
    """
    track_list = []
    lib_size = len(tracks)
    i = 1
    for track in tracks:
        track_data = extract_track_data(track, server_name)
        track_list.append(track_data)
        logger.debug(f"Added {track.title} - {track.ratingKey}. {i} of {lib_size}")
        i += 1
    logger.info(f"Made a list of all track data: {lib_size} in all")
    return track_list


#  TODO export_track_data() and others specify Woodstock.  Make these funcs usable for both servers
def export_track_data(track_data, filename, server_name: str):
    """
    Exports the track data to a CSV file.

    Parameters:
    track_data (list): A list of dictionaries containing track data.

    Returns:
    None
    """
    server_id = server_name + '_id'
    with open(filename, 'a') as csvfile:
        fieldnames = ['title', 'artist', 'album', 'genre', 'added_date', 'filepath',
                      'location', server_id]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for element in track_data:
            writer.writerow(element)
    logger.info("Exported all track data to csv!")