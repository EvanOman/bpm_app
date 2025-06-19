# BPM Detector

![App Screenshot](screenshot.png)

A Vibe-coded Streamlit web application for detecting BPM (Beats Per Minute) from MP3 audio files using librosa's beat tracking algorithms.

## Features

- MP3 file upload via Streamlit interface
- BPM detection using librosa's beat tracking algorithms
- Genre classification based on BPM ranges
- Temporary file handling for audio processing

## Installation

```bash
uv sync
```

## Usage

### Running the Streamlit App
```bash
uv run streamlit run app.py
```

### Running Tests
```bash
uv run pytest test_bpm_detector.py -v
```

## BPM Detection Accuracy

The algorithm has been tested against sample files with known BPM values:

### Test Results Summary
- ✅ **christian_krauss_soul_brothers_80_bpm.mp3**: Expected 80, detected 80.7 (0.7)
- ✅ **dream_for_you_-_mix3_proud_music_preview_100_bpm.mp3**: Expected 100, detected 99.4 (0.6)  
- ❌ **flamenco_naval_proud_music_preview_100_bpm.mp3**: Expected 100, detected 136.0 (36.0)
- ✅ **37401_franz_schubert_1797_1828_klaviersonate_in_b_flat_d_960_scherzo_allegro_vivace_80_bpm.mp3**: Expected 80, detected 80.7 (0.7)

**Overall: 75% success rate (3/4 files within �5 BPM tolerance)**

### Note on Test Samples
These are audio samples/previews, not full tracks. The BPM detection accuracy may vary between samples and full songs due to:
- Sample length and content
- Musical complexity and rhythm patterns
- Audio quality and encoding

The flamenco track shows a significant deviation, likely due to complex rhythmic patterns that can confuse beat tracking algorithms. This is a known limitation of automated BPM detection in certain musical genres.

## Requirements

- Python >=3.13
- Dependencies: streamlit, librosa, numpy, soundfile, pytest