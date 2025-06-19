from pathlib import Path
from bpm_detector import detect_bpm_from_lib, detect_bpm_custom, extract_bpm_from_filename

def compare_bpm_algorithms():
    """Compare both BPM detection algorithms against sample files."""
    sample_dir = Path("sample_mp3s")
    mp3_files = list(sample_dir.glob("*.mp3"))
    
    tolerance = 5
    results = []
    
    print(f"BPM Algorithm Comparison Results:")
    print(f"{'File':<60} {'Expected':<10} {'Librosa':<10} {'Custom':<10} {'Lib Diff':<10} {'Custom Diff':<10} {'Lib OK':<8} {'Custom OK':<10}")
    print("-" * 140)
    
    for sample_file in mp3_files:
        try:
            expected_bpm = extract_bpm_from_filename(sample_file.name)
            
            # Test librosa-based detection
            try:
                lib_bpm, lib_beats = detect_bpm_from_lib(str(sample_file))
                lib_diff = abs(lib_bpm - expected_bpm)
                lib_ok = lib_diff <= tolerance
            except Exception as e:
                lib_bpm, lib_diff, lib_ok = None, None, False
                print(f"Librosa error for {sample_file.name}: {e}")
            
            # Test custom detection
            try:
                custom_bpm, custom_beats = detect_bpm_custom(str(sample_file))
                if custom_bpm is not None:
                    custom_diff = abs(custom_bpm - expected_bpm)
                    custom_ok = custom_diff <= tolerance
                else:
                    custom_bpm, custom_diff, custom_ok = None, None, False
            except Exception as e:
                custom_bpm, custom_diff, custom_ok = None, None, False
                print(f"Custom error for {sample_file.name}: {e}")
            
            results.append({
                'file': sample_file.name,
                'expected': expected_bpm,
                'lib_bpm': lib_bpm,
                'custom_bpm': custom_bpm,
                'lib_diff': lib_diff,
                'custom_diff': custom_diff,
                'lib_ok': lib_ok,
                'custom_ok': custom_ok
            })
            
            # Format output
            lib_str = f"{lib_bpm:.1f}" if lib_bpm is not None else "None"
            custom_str = f"{custom_bpm:.1f}" if custom_bpm is not None else "None"
            lib_diff_str = f"{lib_diff:.1f}" if lib_diff is not None else "N/A"
            custom_diff_str = f"{custom_diff:.1f}" if custom_diff is not None else "N/A"
            
            print(f"{sample_file.name:<60} {expected_bpm:<10} {lib_str:<10} {custom_str:<10} "
                  f"{lib_diff_str:<10} {custom_diff_str:<10} {'✓' if lib_ok else '✗':<8} {'✓' if custom_ok else '✗':<10}")
            
        except Exception as e:
            print(f"{sample_file.name:<60} ERROR: {str(e)}")
    
    # Summary
    valid_results = [r for r in results if r['lib_bpm'] is not None or r['custom_bpm'] is not None]
    
    lib_passed = sum(1 for r in valid_results if r['lib_ok'])
    custom_passed = sum(1 for r in valid_results if r['custom_ok'])
    total = len(valid_results)
    
    print(f"\nSummary:")
    print(f"Librosa algorithm: {lib_passed}/{total} files within ±{tolerance} BPM tolerance ({lib_passed/total*100:.1f}%)")
    print(f"Custom algorithm:  {custom_passed}/{total} files within ±{tolerance} BPM tolerance ({custom_passed/total*100:.1f}%)")
    
    # Detailed analysis
    print(f"\nDetailed Analysis:")
    for result in valid_results:
        print(f"\n{result['file']}:")
        print(f"  Expected: {result['expected']} BPM")
        if result['lib_bpm'] is not None:
            print(f"  Librosa:  {result['lib_bpm']:.1f} BPM (±{result['lib_diff']:.1f})")
        if result['custom_bpm'] is not None:
            print(f"  Custom:   {result['custom_bpm']:.1f} BPM (±{result['custom_diff']:.1f})")

if __name__ == "__main__":
    compare_bpm_algorithms()