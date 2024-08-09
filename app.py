import streamlit as st
from gtts import gTTS
import pyttsx3
from googletrans import Translator
import io
import os

# Initialize the translator
translator = Translator()

# Function to translate text
def translate_text(text, target_lang):
    translated = translator.translate(text, dest=target_lang)
    return translated.text

# Function to convert text to speech using gTTS (Google Text-to-Speech)
def convert_with_gtts(text, lang):
    text_to_speech = gTTS(text=text, lang=lang, slow=False)
    audio_stream = io.BytesIO()
    text_to_speech.write_to_fp(audio_stream)
    audio_stream.seek(0)  # Reset stream position to the beginning
    return audio_stream

# Function to convert text to speech using pyttsx3 (offline TTS)
def convert_with_pyttsx3(text, lang, voice_choice):
    text_to_speech = pyttsx3.init()
    text_to_speech.setProperty('rate', 150)
    voices = text_to_speech.getProperty('voices')

    # Set voice based on user choice and language
    if voice_choice == 'Female':
        text_to_speech.setProperty('voice', voices[1].id)  # Female voice
    else:
        text_to_speech.setProperty('voice', voices[0].id)  # Male voice

    audio_stream = io.BytesIO()
    text_to_speech.save_to_file(text, audio_stream)
    text_to_speech.runAndWait()
    audio_stream.seek(0)  # Reset stream position to the beginning
    return audio_stream

# Language code mapping for gTTS
lang_codes = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Kannada": "kn",
    "Bangla": "bn",
    "Tamil": "ta",
    "Gujarati": "gu",
    "Malayalam": "ml",
    "Telugu": "te"
}

# Reverse mapping for language codes to full names
code_to_language = {v: k for k, v in lang_codes.items()}

# Streamlit dashboard
st.markdown("""
    <style>
    .title {
        font-size: 32px;
        font-weight: bold;
    }
    .subheader {
        font-size: 16px;
    }
    .note {
        font-size: 14px;
        color: gray;
        margin-top: 20px;
    }
    </style>
    <div class="title">Multilingual Text to Speech Conversion</div>
    <div class="subheader">by <a href="https://www.linkedin.com/in/ishan-sharma-8357731a0/" target="_blank">Ishan Sharma</a></div>
    """, unsafe_allow_html=True)

# User input
user_text = st.text_input("Enter the text you want to convert to speech (in any language):")

# Dropdown to choose the language category
language_category = st.selectbox("Choose the language category:", ("International", "Regional"))

# Language options based on selected category
if language_category == "International":
    language = st.selectbox("Choose the target language:", ("English", "Spanish", "French", "German"))
elif language_category == "Regional":
    language = st.selectbox("Choose the target language:", ("Hindi", "Kannada", "Bangla", "Tamil", "Gujarati", "Malayalam", "Telugu"))

# Dropdown to choose the TTS engine
tts_engine = st.selectbox("Choose the Text-to-Speech engine:", ("Channel 1", "Channel 2"))

# Radio button to choose voice gender
voice_choice = st.radio("Choose the voice gender:", ("Male", "Female"))

# Convert button
if st.button("Convert to Speech"):
    if user_text:
        # Detect the input language and translate to the selected target language
        detected_lang_code = translator.detect(user_text).lang
        detected_language = code_to_language.get(detected_lang_code, "Unknown Language")
        translated_text = translate_text(user_text, lang_codes[language])

        st.write(f"Detected Language: {detected_language}")
        st.write(f"Translated Text ({language}): {translated_text}")

        # Convert the translated text to speech
        if tts_engine == "Channel 1":
            audio_stream = convert_with_gtts(translated_text, lang_codes[language])
        elif tts_engine == "Channel 2":
            audio_stream = convert_with_pyttsx3(translated_text, lang_codes[language], voice_choice)
        
        # Play the audio stream
        st.audio(audio_stream, format='audio/mp3')
    else:
        st.warning("Please enter some text before converting.")

# Note for users
st.markdown("""
    <div class="note">
    If you encounter issues with one channel, try switching to the other.
    </div>
    """, unsafe_allow_html=True)
