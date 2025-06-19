from pathlib import Path
from bpm_detector import detect_bpm, extract_bpm_from_filename

def test_all_samples():
    """Test all sample files and show results without failing."""
    sample_dir = Path("sample_mp3s")
    mp3_files = list(sample_dir.glob("*.mp3"))
    
    tolerance = 5
    results = []
    
    print(f"BPM Detection Results:")
    print(f"{'File':<60} {'Expected':<10} {'Detected':<10} {'Diff':<10} {'Within ±5':<10}")
    print("-" * 100)
    
    for sample_file in mp3_files:
        try:
            expected_bpm = extract_bpm_from_filename(sample_file.name)
            detected_bpm, beat_count = detect_bpm(str(sample_file))
            
            difference = abs(detected_bpm - expected_bpm)
            within_tolerance = difference <= tolerance
            
            results.append({
                'file': sample_file.name,
                'expected': expected_bpm,
                'detected': detected_bpm,
                'difference': difference,
                'within_tolerance': within_tolerance
            })
            
            print(f"{sample_file.name:<60} {expected_bpm:<10} {detected_bpm:<10.1f} "
                  f"{difference:<10.1f} {'✓' if within_tolerance else '✗':<10}")
            
        except Exception as e:
            print(f"{sample_file.name:<60} ERROR: {str(e)}")
    
    # Summary
    passed = sum(1 for r in results if r['within_tolerance'])
    total = len(results)
    print(f"\nSummary: {passed}/{total} files within ±{tolerance} BPM tolerance")
    print(f"Success rate: {passed/total*100:.1f}%")

if __name__ == "__main__":
    test_all_samples()