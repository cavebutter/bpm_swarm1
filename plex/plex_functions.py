import plexapi
from plexapi.myplex import MyPlexAccount
import plexapi.exceptions
import plexapi.library
import plexapi.playlist
from plexapi.server import PlexServer
import configparser
from datetime import datetime
import csv

config = configparser.ConfigParser()
config.read('/Users/jay/Documents/python_projects/bpm_swarm1/config.ini')

PLEX_USER = config['WOODSTOCK']['username']
PLEX_PASSWORD = config['WOODSTOCK']['password']
PLEX_SERVER = config['WOODSTOCK']['servername']
MUSIC_LIBRARY = config['WOODSTOCK']['musiclibrary']

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
    print(f"Connected to Plex Server:  {PLEX_SERVER}")
    return server

def find_music_library(server):
    """
    Finds the music library in the provided Plex server.

    Parameters:
    server (PlexServer): The connected Plex server object.

    Returns:
    plexapi.library.Library: The music library object.
    """
    music_library = server.library.section(MUSIC_LIBRARY)
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
    tracks = library.searchTracks(limit=50)
    print("Got all tracks!")
    return tracks

def extract_track_data_woodstock(track):
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
        'woodstock_id': track.ratingKey
    }
    return track_data


def listify_track_data(tracks):
    """
    Lists the track data from the provided list of tracks.

    Parameters:
    tracks (list): A list of track objects to extract data from.

    Returns:
    list: A list of dictionaries containing the track data.
    """
    track_list = []
    for track in tracks:
        track_data = extract_track_data_woodstock(track)
        track_list.append(track_data)
    print("Made a list of all track data!")
    return track_list


#  TODO export_track_data() and others specify Woodstock.  Make these funcs usable for both servers
def export_track_data(track_data):
    """
    Exports the track data to a CSV file.

    Parameters:
    track_data (list): A list of dictionaries containing track data.

    Returns:
    None
    """
    with open('track_data.csv', 'a') as csvfile:
        fieldnames = ['title', 'artist', 'album', 'genre', 'added_date', 'filepath',
                      'location', 'woodstock_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for element in track_data:
            writer.writerow(element)
    print("Exported all track data to csv!")