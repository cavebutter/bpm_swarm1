import pytest
from analysis.bpm import get_bpm


@pytest.fixture
def audio_file_mp3():
    return "/Users/Jayco/projects/bpm_swarm1/music_library/The White Stripes - Get Behind Me Satan [2005]/01 - Blue Orchid.mp3", 151

@pytest.fixture
def audio_file_m4a():
    return "/Users/Jayco/projects/bpm_swarm1/music_library/Tom Petty & The Heartbreakers/Into The Great Wide Open/01 Learning To Fly.m4a"


def test_get_bpm_mp3(audio_file_mp3):
    bpm =get_bpm(audio_file_mp3[0])
    assert bpm == audio_file_mp3[1]


def test_ivalid_file_type(audio_file_m4a):
    bpm = get_bpm(audio_file_m4a)
    assert bpm is None