import librosa

def get_bpm(audio_file):
    """
    Calculate the beats per minute (BPM) of the provided audio file.

    Parameters:
    audio_file (str): The path to the audio file.

    Returns:
    float: The BPM value calculated from the audio file.
    """
    try:
        y, sr = librosa.load(audio_file)
        bpm = librosa.beat.tempo(y=y, sr=sr)[0]
        return bpm
    except Exception as e:
        print(f"Error calculating BPM: {e}")
        return None