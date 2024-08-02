import streamlit as st
import whisper
from langchain_community.llms import Ollama
import tempfile
import os

# Initialize models
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

@st.cache_resource
def load_ollama_model():
    return Ollama(model="gemma2:2b")

whisper_model = load_whisper_model()
llm = load_ollama_model()

def process_audio(audio_file):
    # Transcribe
    result = whisper_model.transcribe(audio_file)
    return result["text"]

st.title("Audio Transcription and Analysis App")

uploaded_file = st.file_uploader("Choose an audio file", type=['wav', 'mp3', 'ogg'])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    
    if st.button("Process Audio"):
        with st.spinner("Processing audio..."):
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            # Process the audio
            transcript = process_audio(tmp_file_path)
            
            # Remove temporary file
            os.unlink(tmp_file_path)

        st.subheader("Transcript:")
        st.text_area("", transcript, height=300)

        with st.spinner("Analyzing transcript..."):
            prompt = f"Analyze the following transcript and summarize the main points:\n\n{transcript}"
            analysis = llm.invoke(prompt)

        st.subheader("Analysis:")
        st.write(analysis)

st.sidebar.header("About")
st.sidebar.info(
    "This app uses Whisper for transcription and Ollama (Gemma 2B) for transcript analysis. "
    "Upload an audio file to get started!"
)