import pytest
import os
from pathlib import Path
from bpm_detector import detect_bpm, extract_bpm_from_filename

class TestBPMDetector:
    
    @pytest.fixture
    def sample_files(self):
        """Get all MP3 files from sample_mp3s directory."""
        sample_dir = Path("sample_mp3s")
        if not sample_dir.exists():
            pytest.skip("sample_mp3s directory not found")
        
        mp3_files = list(sample_dir.glob("*.mp3"))
        if not mp3_files:
            pytest.skip("No MP3 files found in sample_mp3s directory")
        
        # Skip flamenco file in CI environment
        if os.environ.get("PYTEST_SKIP_FLAMENCO"):
            mp3_files = [f for f in mp3_files if "flamenco" not in f.name.lower()]
        
        return mp3_files
    
    def test_extract_bpm_from_filename(self):
        """Test BPM extraction from various filename patterns."""
        test_cases = [
            ("christian_krauss_soul_brothers_80_bpm.mp3", 80),
            ("dream_for_you_-_mix3_proud_music_preview_100_bpm.mp3", 100),
            ("37401_franz_schubert_1797_1828_klaviersonate_in_b_flat_d_960_scherzo_allegro_vivace_80_bpm.mp3", 80),
            ("flamenco_naval_proud_music_preview_100_bpm.mp3", 100),
        ]
        
        for filename, expected_bpm in test_cases:
            actual_bpm = extract_bpm_from_filename(filename)
            assert actual_bpm == expected_bpm, f"Expected {expected_bpm} BPM from {filename}, got {actual_bpm}"
    
    def test_bpm_detection_accuracy(self, sample_files):
        """Test that BPM detection is within +/- 5 BPM of labeled values."""
        tolerance = 5
        results = []
        
        for sample_file in sample_files:
            # Extract expected BPM from filename
            try:
                expected_bpm = extract_bpm_from_filename(sample_file.name)
            except ValueError as e:
                pytest.fail(f"Could not extract BPM from filename {sample_file.name}: {e}")
            
            # Detect BPM from audio
            try:
                detected_bpm, beat_count = detect_bpm(str(sample_file))
            except Exception as e:
                pytest.fail(f"Failed to detect BPM from {sample_file.name}: {e}")
            
            # Check if detection is within tolerance
            difference = abs(detected_bpm - expected_bpm)
            within_tolerance = difference <= tolerance
            
            results.append({
                'file': sample_file.name,
                'expected': expected_bpm,
                'detected': detected_bpm,
                'difference': difference,
                'within_tolerance': within_tolerance
            })
            
            # Assert individual file is within tolerance
            assert within_tolerance, (
                f"BPM detection for {sample_file.name} failed: "
                f"expected {expected_bpm}, detected {detected_bpm:.1f}, "
                f"difference {difference:.1f} > tolerance {tolerance}"
            )
        
        # Print summary for debugging
        print(f"\nBPM Detection Results:")
        print(f"{'File':<50} {'Expected':<10} {'Detected':<10} {'Diff':<10} {'OK':<5}")
        print("-" * 85)
        for result in results:
            print(f"{result['file']:<50} {result['expected']:<10} {result['detected']:<10.1f} "
                  f"{result['difference']:<10.1f} {'✓' if result['within_tolerance'] else '✗':<5}")
        
        # Overall summary
        passed = sum(1 for r in results if r['within_tolerance'])
        total = len(results)
        print(f"\nSummary: {passed}/{total} files within ±{tolerance} BPM tolerance")
        
        # All files should pass
        assert passed == total, f"Only {passed}/{total} files passed BPM detection accuracy test"
    
    def test_detect_bpm_with_invalid_file(self):
        """Test that detect_bpm raises appropriate error for invalid files."""
        with pytest.raises(Exception):
            detect_bpm("nonexistent_file.mp3")
    
    def test_extract_bpm_from_invalid_filename(self):
        """Test that extract_bpm_from_filename raises error for invalid filenames."""
        with pytest.raises(ValueError):
            extract_bpm_from_filename("no_bpm_in_this_filename.mp3")