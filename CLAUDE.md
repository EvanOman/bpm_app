# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit web application called "bpm-app" for detecting BPM (Beats Per Minute) from MP3 audio files using both librosa and custom from-scratch algorithms.

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
- Dependencies: streamlit, librosa, numpy, soundfile, scipy, pytest
- Always use `uv` for package management and for running things (uv run...)

## Architecture

The project is a Streamlit web application for BPM detection:
- `app.py` - Main Streamlit application with algorithm selection and file upload
- `bpm_detector.py` - Core BPM detection algorithms (both librosa and custom)
- `test_bpm_detector.py` - Unit tests with CI integration
- `test_comparison.py` - Algorithm comparison testing
- `pyproject.toml` - Python project configuration
- `.github/workflows/test.yml` - CI/CD pipeline

## Key Features

- **Two BPM Detection Algorithms:**
  - Librosa (out-of-box): Industry standard beat tracking
  - Custom (from scratch): Pure numpy/scipy implementation
- Algorithm comparison mode
- MP3 file upload via Streamlit interface
- Genre classification based on BPM ranges
- Unit testing with ±5 BPM tolerance validation