import librosa

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
    try:
        y, sr = librosa.load(audio_file, duration=180)
        bpm = librosa.beat.beat_track(y=y, sr=sr)[0]
        #bpm = round(bpm,0)
        bpm = int(bpm)
        return bpm
    except Exception as e:
        print(f"Error calculating BPM: {e}")
        return None