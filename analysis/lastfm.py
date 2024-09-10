from configparser import ConfigParser
import requests
import json
from loguru import logger


config = ConfigParser()
config.read('config.ini')

LASTFM_API_KEY = config['LASTFM']['api_key']
LASTFM_SHARED_SECRET = config['LASTFM']['shared_secret']
LASTFM_USERNAME = config['LASTFM']['username']
LASTFM_PASSWORD = config['LASTFM']['password']
LASTFM_APP_NAME = config['LASTFM']['app_name']


def get_artist_info(artist_name):

    """
    Retrieves information about a specific artist from the Last.fm API.

    Parameters:
    artist_name (str): The name of the artist to retrieve information for.

    Returns:
    dict: A JSON object containing information about the artist if the request is successful, otherwise None.
    """
    url = f'http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist_name}&api_key={LASTFM_API_KEY}&format=json'
    response = requests.get(url)
    if response.status_code == 200:
        logger.info(f"Retrieved artist info for {artist_name}")
        return response.json()
    else:
        logger.error(f"Failed to retrieve artist info for {artist_name}")
        return None


def get_mbid(result: json):
    """
    Retrieves the MusicBrainz ID (MBID) of the artist from the given JSON `result` object.

    Parameters:
    result (json): The JSON object containing artist information.

    Returns:
    str: The MusicBrainz ID (MBID) of the artist, or None if the MBID is not found.
    """
    try:
        mbid = result['artist']['mbid']
        logger.info(f"Retrieved MBID for {result['artist']['name']}: {mbid}")
        return mbid
    except (KeyError, TypeError) as e:
        logger.error(f"Failed to retrieve MBID for {result['artist']['name']}: {e}")
        return None


def get_tags(result: json):
    """
    Retrieves the tags from the given JSON `result` object.

    Parameters:
    result (json): The JSON object containing artist information.

    Returns:
    list: A list of tags associated with the artist.
    """
    tags_tuples = result['artist']['tags']['tag']
    tags = [tag_tuple['name'] for tag_tuple in tags_tuples]
    return tags


def get_similar_artists(result: json):
    """
    Retrieves similar artists from the given JSON `result` object and returns them as a list of tuples.

    Parameters:
    result (json): The JSON object containing artist information.

    Returns:
    list: A list of tuples where each tuple contains the name and MusicBrainz ID (MBID) of a similar artist.
    """
    similar_artists_dict = result['artist']['similar']['artist']
    similar_artists = [artist['name'] for artist in similar_artists_dict]
    return similar_artists
