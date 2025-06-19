import streamlit as st
import tempfile
import os
from bpm_detector import detect_bpm

def main():
    st.title("🎵 BPM Detector")
    st.write("Upload an MP3 file to detect its BPM (Beats Per Minute)")
    
    uploaded_file = st.file_uploader("Choose an MP3 file", type=['mp3'])
    
    if uploaded_file is not None:
        st.write("Processing audio file...")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name
        
        try:
            with st.spinner("Analyzing BPM..."):
                try:
                    bpm, beat_count = detect_bpm(tmp_file_path)
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
                
                st.write(f"**File:** {uploaded_file.name}")
                
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
                
        finally:
            os.unlink(tmp_file_path)

if __name__ == "__main__":
    main()