import pytest
import plexapi
from plex import plex_functions as p
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

user = config.get('WOODSTOCK', 'username')
password = config.get('WOODSTOCK', 'password')
server_name = config.get('WOODSTOCK', 'servername')
music_library = config.get('WOODSTOCK', 'musiclibrary')

def test_plex_connect():
    server = p.plex_connect(user, password, server_name)
    assert server

@pytest.fixture
def server():
    server = p.plex_connect(user, password, server_name)
    return server


# def test_get_music_library(server, music_library):
#     library = p.get_music_library(server, music_library)
#     assert type(library) == plexapi.library.Library


@pytest.fixture
def music_library():
    library = p.get_music_library(server, music_library)
    return library


def test_get_all_tracks(server, music_library):
    tracks, library_size = p.get_all_tracks_test(server, music_library)
    assert tracks
    assert library_size == 50