import librosa
import numpy as np
from pathlib import Path

def detect_bpm(audio_file_path):
    """
    Detect BPM from audio file using librosa.
    
    Args:
        audio_file_path: Path to the audio file
        
    Returns:
        tuple: (bpm, beat_count) where bpm is the detected tempo and beat_count is number of beats
    """
    try:
        y, sr = librosa.load(audio_file_path)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        return float(tempo), len(beats)
    except Exception as e:
        raise Exception(f"Error processing audio file {audio_file_path}: {str(e)}")

def extract_bpm_from_filename(filename):
    """
    Extract BPM value from filename that contains '_XXX_bpm' pattern.
    
    Args:
        filename: Name of the file
        
    Returns:
        int: BPM value extracted from filename
    """
    filename_str = str(filename).lower()
    
    # Look for pattern like '_80_bpm' or '_100_bpm'
    import re
    match = re.search(r'_(\d+)_bpm', filename_str)
    if match:
        return int(match.group(1))
    
    # Fallback: look for any number followed by bpm
    match = re.search(r'(\d+)_?bpm', filename_str)
    if match:
        return int(match.group(1))
    
    raise ValueError(f"Could not extract BPM from filename: {filename}")