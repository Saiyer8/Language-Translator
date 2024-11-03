import os
import pygame
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from googletrans import LANGUAGES, Translator

# Initialize the translator and mixer modules
translator = Translator()
pygame.mixer.init()

# Create a mapping between language names and language codes
language_mapping = {name: code for code, name in LANGUAGES.items()}

# Function to get language code from language name
def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

# Function to translate spoken text
def translator_function(spoken_text, from_language, to_language):
    return translator.translate(spoken_text, src=from_language, dest=to_language)

# Function to convert text to voice
def text_to_voice(text_data, to_language):
    myobj = gTTS(text=text_data, lang=to_language, slow=False)
    myobj.save("cache_file.mp3")  # Save the audio to a file
    audio = pygame.mixer.Sound("cache_file.mp3")  # Load the sound
    audio.play()  # Play the sound
    os.remove("cache_file.mp3")  # Remove the temporary audio file

# Main process function to handle translation
def main_process(output_placeholder, from_language, to_language):
    rec = sr.Recognizer()  # Initialize recognizer once
    print("Main process started")  # Debugging statement
    
    while st.session_state.isTranslateOn:  # Use session state for translation status
        with sr.Microphone() as source:
            output_placeholder.text("Listening...")
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=10)
            print("Listening complete")  # Debugging statement
        
        try:
            output_placeholder.text("Processing...")
            spoken_text = rec.recognize_google(audio, language=from_language)
            print(f"Recognized: {spoken_text}")  # Debugging statement
            
            output_placeholder.text("Translating...")
            translated_text = translator_function(spoken_text, from_language, to_language)

            text_to_voice(translated_text.text, to_language)

        except sr.UnknownValueError:
            output_placeholder.text("Could not understand audio, please try again.")
            print("Could not understand audio")  # Debugging statement
        except sr.RequestError as e:
            output_placeholder.text(f"Could not request results; {e}")
            print(f"Request Error: {e}")  # Debugging statement
        except Exception as e:
            print(f"Exception: {e}")  # Debugging statement

# UI layout
st.title("Language Translator")

# Dropdowns for selecting languages
from_language_name = st.selectbox("Select Source Language:", list(LANGUAGES.values()))
to_language_name = st.selectbox("Select Target Language:", list(LANGUAGES.values()))

# Convert language names to language codes
from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

# Initialize session state for translation status
if 'isTranslateOn' not in st.session_state:
    st.session_state.isTranslateOn = False

# Button to trigger translation
start_button = st.button("Start")
stop_button = st.button("Stop")

# Placeholder for output messages
output_placeholder = st.empty()  # Initialize placeholder here

# Check if "Start" button is clicked
if start_button and not st.session_state.isTranslateOn:
    st.session_state.isTranslateOn = True
    main_process(output_placeholder, from_language, to_language)

# Check if "Stop" button is clicked
if stop_button:
    st.session_state.isTranslateOn = False
    output_placeholder.text("Translation stopped.")
