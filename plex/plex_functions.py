import plexapi
from plexapi.myplex import MyPlexAccount
import plexapi.exceptions
import plexapi.library
import plexapi.playlist
from plexapi.server import PlexServer
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read('/Users/Jayco/projects/bpm_swarm1/config.ini')

PLEX_USER = config['PLEX']['username']
PLEX_PASSWORD = config['PLEX']['password']
PLEX_SERVER = config['PLEX']['servername']
MUSIC_LIBRARY = config['PLEX']['musiclibrary']

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
    server = account.resource(PLEX_SERVER).connect()
    return server

def find_music_library(server):
    """
    Finds the music library in the provided Plex server.

    Parameters:
    server (PlexServer): The connected Plex server object.

    Returns:
    plexapi.library.Library: The music library object.
    """
    music_library = server.library.section('Music - Schroeder')
    return music_library

def get_all_tracks(server):
    """
    Gets all tracks from the music library in the provided Plex server.

    Parameters:
    server (PlexServer): The connected Plex server object.
    music_library (plexapi.library.Library): The music library object.

    Returns:
    list: A list of all tracks in the music library.
    """
    library = find_music_library(server)
    tracks = library.searchTracks()
    return tracks

def extract_track_data(track):
    """
    Extracts the track data from the provided track.

    Parameters:
    track (plexapi.audio.Track): The track object to extract data from.

    Returns:
    dict: A dictionary containing the track data.
    """
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
        'id': track.ratingKey
    }
    return track_data

