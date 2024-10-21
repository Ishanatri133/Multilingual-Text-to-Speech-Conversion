import streamlit as st
from gtts import gTTS
from googletrans import Translator

# Initialize translator
translator = Translator()

# Function to translate and convert text to speech
def translate_and_speak(text, target_language):
    # Translate text to the selected language
    translated_text = translator.translate(text, dest=target_language).text
    
    # Convert translated text to speech
    tts = gTTS(text=translated_text, lang=target_language)
    tts.save("translated_output.mp3")
    return translated_text, "translated_output.mp3"

# Streamlit App
def main():
    st.title("Text-to-Speech with Translation")

    # Text input from the user
    text_input = st.text_area("Enter text to convert to speech", "")

    # Language selection: International and Regional
    category = st.selectbox("Select Language Category", ["International", "Regional"])

    # Dropdowns for international and regional languages
    if category == "International":
        language = st.selectbox("Select International Language", 
                                ["English", "Spanish", "French", "German", "Italian"])

        language_map = {
            "English": "en",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Italian": "it"
        }
        
    elif category == "Regional":
        language = st.selectbox("Select Regional Language", 
                                ["Hindi", "Bengali", "Tamil", "Telugu", "Kannada", 
                                 "Malayalam", "Marathi", "Gujarati", "Punjabi", "Urdu"])

        language_map = {
            "Hindi": "hi",
            "Bengali": "bn",
            "Tamil": "ta",
            "Telugu": "te",
            "Kannada": "kn",
            "Malayalam": "ml",
            "Marathi": "mr",
            "Gujarati": "gu",
            "Punjabi": "pa",
            "Urdu": "ur"
        }

    if st.button("Translate and Convert to Speech"):
        if text_input:
            # Get the language code from the map
            language_code = language_map[language]
            
            # Translate and generate speech
            translated_text, audio_file = translate_and_speak(text_input, language_code)
            
            # Display translated text
            st.write(f"Translated Text: {translated_text}")
            
            # Playing the translated speech in the app
            audio_file_path = open(audio_file, 'rb')
            audio_bytes = audio_file_path.read()
            st.audio(audio_bytes, format='audio/mp3')

            # Option to download the audio file
            st.download_button("Download Speech", data=audio_bytes, file_name="speech.mp3")
        else:
            st.warning("Please enter text to convert.")

if __name__ == "__main__":
    main()
