import streamlit as st
import tempfile
import os
from bpm_detector import detect_bpm_from_lib, detect_bpm_custom

def main():
    st.title("🎵 BPM Detector")
    st.write("Upload an MP3 file to detect its BPM (Beats Per Minute)")
    
    # Algorithm selection
    algorithm = st.selectbox(
        "Choose BPM Detection Algorithm:",
        ("Librosa (Out-of-box)", "Custom (From Scratch)", "Both")
    )
    
    uploaded_file = st.file_uploader("Choose an MP3 file", type=['mp3'])
    
    if uploaded_file is not None:
        st.write("Processing audio file...")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name
        
        try:
            if algorithm == "Both":
                # Run both algorithms
                with st.spinner("Analyzing with both algorithms..."):
                    try:
                        lib_bpm, lib_beats = detect_bpm_from_lib(tmp_file_path)
                    except Exception as e:
                        st.error(f"Librosa error: {str(e)}")
                        lib_bpm, lib_beats = None, 0
                    
                    try:
                        custom_bpm, custom_beats = detect_bpm_custom(tmp_file_path)
                    except Exception as e:
                        st.error(f"Custom algorithm error: {str(e)}")
                        custom_bpm, custom_beats = None, 0
                
                st.success("Analysis Complete!")
                
                # Display both results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🔬 Librosa (Out-of-box)")
                    if lib_bpm is not None:
                        st.metric("BPM", f"{lib_bpm:.1f}")
                        st.metric("Beats", lib_beats)
                    else:
                        st.error("Failed to detect BPM")
                
                with col2:
                    st.subheader("⚙️ Custom (From Scratch)")
                    if custom_bpm is not None:
                        st.metric("BPM", f"{custom_bpm:.1f}")
                        st.metric("Beats", custom_beats)
                    else:
                        st.error("Failed to detect BPM")
                
                # Show comparison
                if lib_bpm is not None and custom_bpm is not None:
                    diff = abs(lib_bpm - custom_bpm)
                    st.write(f"**Difference:** {diff:.1f} BPM")
                    
                    if diff < 2:
                        st.success("🎯 Both algorithms agree!")
                    elif diff < 10:
                        st.warning("⚠️ Moderate difference between algorithms")
                    else:
                        st.error("❗ Significant difference - complex rhythm detected")
            
            else:
                # Single algorithm
                algo_name = "Librosa" if algorithm == "Librosa (Out-of-box)" else "Custom"
                detect_func = detect_bpm_from_lib if algorithm == "Librosa (Out-of-box)" else detect_bpm_custom
                
                with st.spinner(f"Analyzing with {algo_name} algorithm..."):
                    try:
                        bpm, beat_count = detect_func(tmp_file_path)
                    except Exception as e:
                        st.error(f"Error processing audio: {str(e)}")
                        bpm, beat_count = None, None
                
                if bpm is not None:
                    st.success("Analysis Complete!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Estimated BPM", f"{bpm:.1f}")
                    
                    with col2:
                        st.metric("Beats Detected", beat_count)
                    
                    # Genre categorization
                    bpm_category = ""
                    if bpm < 60:
                        bpm_category = "Very Slow (Ballad)"
                    elif bpm < 90:
                        bpm_category = "Slow (Folk/Blues)"
                    elif bpm < 120:
                        bpm_category = "Moderate (Pop/Rock)"
                    elif bpm < 140:
                        bpm_category = "Fast (Dance/Electronic)"
                    else:
                        bpm_category = "Very Fast (Drum & Bass/Hardcore)"
                    
                    st.info(f"**Genre Suggestion:** {bpm_category}")
            
            st.write(f"**File:** {uploaded_file.name}")
            st.write(f"**Algorithm:** {algorithm}")
            
        finally:
            os.unlink(tmp_file_path)

if __name__ == "__main__":
    main()