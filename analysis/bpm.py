import librosa
from loguru import logger
import os

#  TODO Deal with why/when PySoundFile fails.
#  TODO audioread works when PySoundFile fails, but it is deprecated.  Is there a new way?
#  TODO Suppress audioread deprecation warnings in stdout

def get_bpm(audio_file):
    """
    Calculate the beats per minute (BPM) of the provided audio file.

    Parameters:
    audio_file (str): The path to the audio file.

    Returns:
    float: The BPM value calculated from the audio file.
    """
    invalid_extensions = {'.m4b', '.m4a'}
    file_extension = os.path.splitext(audio_file)[1].lower()
    if file_extension in invalid_extensions:
        logger.error(f"{audio_file} is invalid type: {file_extension}")
        return None
    try:
        y, sr = librosa.load(audio_file, duration=180)
        bpm = librosa.beat.beat_track(y=y, sr=sr)[0]
        #bpm = round(bpm,0)
        bpm = int(bpm)
        return bpm
    except Exception as e:
        logger.error(f"Error: {e}")
        return None
    except UserWarning as w:
        logger.warning(f"User Warning: {w}")
        return None
    except FutureWarning as f:
        logger.warning(f"Future Warning: {f}")
        return None