import streamlit as st
import speech_recognition as sr
import os
from pydub import AudioSegment
import subprocess

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True, shell=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def convert_to_wav(input_file, output_file):
    try:
        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format="wav")
    except Exception as e:
        st.error(f"Error converting audio: {str(e)}. Please ensure FFmpeg is installed and added to your system PATH.")
        return False
    return True

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

def main():
    st.title("Audio Transcription App for Windows")

    if not check_ffmpeg():
        st.warning("FFmpeg is not installed or not in PATH. Please install FFmpeg and add it to your system PATH.")
        st.info("Download FFmpeg from https://github.com/BtbN/FFmpeg-Builds/releases and add the 'bin' folder to your system PATH.")

    # Language selection
    languages = st.multiselect(
        "Select the languages present in the audio:",
        ["English", "Norwegian", "Spanish", "French", "German", "Mandarin", "Japanese", "Other"]
    )

    # Audio upload
    st.header("Upload Audio")
    uploaded_file = st.file_uploader("Choose an audio file", type=['wav', 'mp3', 'ogg'])
    
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        with open("temp_audio_file", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Convert to WAV if necessary
        if uploaded_file.name.endswith(('.mp3', '.ogg')):
            if not convert_to_wav("temp_audio_file", "temp_audio_file.wav"):
                st.error("Audio conversion failed. Please ensure FFmpeg is installed correctly.")
                if os.path.exists("temp_audio_file"):
                    os.remove("temp_audio_file")
                return
        else:
            os.rename("temp_audio_file", "temp_audio_file.wav")

        st.audio("temp_audio_file.wav", format='audio/wav')

        # Transcribe uploaded audio
        if st.button("Transcribe Audio"):
            with st.spinner("Transcribing..."):
                transcription = transcribe_audio("temp_audio_file.wav")
            st.write("Transcription:")
            st.write(transcription)

        # Clean up the temporary file
        if os.path.exists("temp_audio_file.wav"):
            os.remove("temp_audio_file.wav")

    # Display selected languages
    if languages:
        st.write("Selected languages:", ", ".join(languages))

if __name__ == "__main__":
    main()