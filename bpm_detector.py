import librosa
import numpy as np
import soundfile as sf
from scipy import signal
from pathlib import Path
import re

def detect_bpm_from_lib(audio_file_path):
    """
    Detect BPM from audio file using librosa (out-of-box solution).
    
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

def detect_bpm_custom(audio_file_path):
    """
    Custom BPM detection algorithm implemented completely from scratch.
    
    Uses only numpy and scipy for signal processing - no librosa dependencies.
    
    Args:
        audio_file_path: Path to the audio file
        
    Returns:
        tuple: (bpm, beat_count) where bpm is the detected tempo and beat_count is number of beats
    """
    try:
        # Load audio using soundfile (no librosa)
        y, sr = sf.read(audio_file_path)
        
        # Convert stereo to mono if needed
        if len(y.shape) > 1:
            y = np.mean(y, axis=1)
        
        # Normalize audio
        y = y / (np.max(np.abs(y)) + 1e-10)
        
        # Primary method: Pure numpy/scipy autocorrelation
        bpm_autocorr = _detect_bpm_pure_autocorr(y, sr)
        
        # Fallback method: Spectral peak detection
        bpm_spectral = _detect_bpm_pure_spectral(y, sr)
        
        # Choose best result
        if bpm_autocorr is not None:
            final_bpm = bpm_autocorr
        elif bpm_spectral is not None:
            final_bpm = bpm_spectral
        else:
            return None, 0
        
        # Estimate beat count
        duration = len(y) / sr
        beat_count = int((final_bpm / 60.0) * duration)
        
        return float(final_bpm), beat_count
        
    except Exception as e:
        raise Exception(f"Error processing audio file {audio_file_path}: {str(e)}")

def _detect_bpm_pure_autocorr(y, sr):
    """
    Pure numpy/scipy autocorrelation-based BPM detection.
    No librosa dependencies.
    """
    # Create onset strength using spectral flux
    hop_length = 512
    frame_length = 2048
    
    # Compute STFT manually using scipy
    f, t, stft = signal.stft(y, sr, nperseg=frame_length, noverlap=frame_length-hop_length)
    magnitude = np.abs(stft)
    
    # Compute spectral flux (onset strength)
    flux = np.sum(np.diff(magnitude, axis=1) ** 2, axis=0)
    flux = np.maximum(0, flux)  # Half-wave rectification
    
    # Smooth the flux
    window_size = 5
    flux = np.convolve(flux, np.ones(window_size)/window_size, mode='same')
    
    # Normalize
    flux = flux / (np.max(flux) + 1e-10)
    
    # Compute autocorrelation
    autocorr = np.correlate(flux, flux, mode='full')
    autocorr = autocorr[len(autocorr)//2:]
    
    # Normalize autocorrelation
    autocorr = autocorr / (autocorr[0] + 1e-10)
    
    # Convert lag to BPM range
    frame_rate = sr / hop_length
    
    # Look for peaks in BPM range 60-180
    min_lag = int(frame_rate * 60 / 180)  # 180 BPM
    max_lag = int(frame_rate * 60 / 60)   # 60 BPM
    
    if max_lag >= len(autocorr):
        max_lag = len(autocorr) - 1
    
    if min_lag >= max_lag:
        return None
    
    # Find peaks in autocorrelation
    search_range = autocorr[min_lag:max_lag]
    if len(search_range) == 0:
        return None
    
    # Simple peak detection
    peaks = []
    for i in range(1, len(search_range) - 1):
        if (search_range[i] > search_range[i-1] and 
            search_range[i] > search_range[i+1] and
            search_range[i] > 0.1):  # Minimum prominence
            actual_lag = i + min_lag
            peaks.append((actual_lag, search_range[i]))
    
    if not peaks:
        return None
    
    # Get the strongest peak
    best_lag = max(peaks, key=lambda x: x[1])[0]
    bpm = 60.0 * frame_rate / best_lag
    
    return _normalize_bpm(bpm)

def _detect_bpm_pure_spectral(y, sr):
    """
    Pure numpy/scipy spectral-based BPM detection.
    No librosa dependencies.
    """
    # Apply high-pass filter to focus on percussive elements
    sos = signal.butter(4, 100, btype='high', fs=sr, output='sos')
    y_filtered = signal.sosfilt(sos, y)
    
    # Create envelope using Hilbert transform
    analytic_signal = signal.hilbert(y_filtered)
    envelope = np.abs(analytic_signal)
    
    # Downsample envelope for efficiency
    downsample_factor = 32
    envelope_ds = envelope[::downsample_factor]
    sr_ds = sr // downsample_factor
    
    # Find peaks in envelope
    # Use scipy's find_peaks for robust peak detection
    peaks, properties = signal.find_peaks(
        envelope_ds,
        height=np.mean(envelope_ds) + np.std(envelope_ds),
        distance=int(sr_ds * 0.2)  # Minimum 0.2s between peaks
    )
    
    if len(peaks) < 4:
        return None
    
    # Convert peaks to time
    peak_times = peaks / sr_ds
    
    # Calculate intervals
    intervals = np.diff(peak_times)
    
    # Filter reasonable intervals (30-200 BPM range)
    min_interval = 60.0 / 200  # 200 BPM
    max_interval = 60.0 / 30   # 30 BPM
    
    valid_intervals = intervals[
        (intervals >= min_interval) & (intervals <= max_interval)
    ]
    
    if len(valid_intervals) < 2:
        return None
    
    # Use median interval
    median_interval = np.median(valid_intervals)
    bpm = 60.0 / median_interval
    
    return _normalize_bpm(bpm)

def _normalize_bpm(bpm):
    """Normalize BPM to reasonable range and handle harmonics."""
    if bpm is None:
        return None
    
    # Handle harmonics - if BPM is too high, try half/quarter tempo
    while bpm > 180:
        bpm /= 2
    
    while bpm < 60:
        bpm *= 2
    
    # Ensure reasonable range
    if 60 <= bpm <= 180:
        return bpm
    
    return None

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
    match = re.search(r'_(\d+)_bpm', filename_str)
    if match:
        return int(match.group(1))
    
    # Fallback: look for any number followed by bpm
    match = re.search(r'(\d+)_?bpm', filename_str)
    if match:
        return int(match.group(1))
    
    raise ValueError(f"Could not extract BPM from filename: {filename}")

# Backward compatibility
def detect_bpm(audio_file_path):
    """Default BPM detection - uses librosa for now."""
    return detect_bpm_from_lib(audio_file_path)