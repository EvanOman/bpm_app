# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit web application called "bpm-app" for detecting BPM (Beats Per Minute) from MP3 audio files.

## Development Commands

### Running the Streamlit App
```bash
uv run streamlit run app.py
```

### Installing Dependencies
```bash
uv sync
```

### Running Tests
```bash
uv run pytest test_bpm_detector.py -v
```

### Python Environment
- Requires Python >=3.13
- Dependencies: streamlit, librosa, numpy, soundfile
- Always use `uv` for package management and for running things (uv run...)

## Architecture

The project is a Streamlit web application for BPM detection:
- `app.py` - Main Streamlit application with file upload and BPM detection
- `main.py` - Original entry point (legacy)
- `pyproject.toml` - Python project configuration with audio processing dependencies

## Key Features

- MP3 file upload via Streamlit interface
- BPM detection using librosa's beat tracking algorithms
- Genre classification based on BPM ranges
- Temporary file handling for audio processing