import speech_recognition as sr

# Initialize recognizer
rec = sr.Recognizer()

# Use the microphone as a source
with sr.Microphone() as source:
    print("Say something:")
    audio = rec.listen(source)  # Listen for the first phrase

    try:
        # Use Google Web Speech API to recognize the audio
        print("You said: " + rec.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"Error: {e}")
