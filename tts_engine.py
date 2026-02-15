import pyttsx3


def create_tts_engine():
    # Initialize the engine
    engine = pyttsx3.init()

    # Optional: Configure properties
    engine.setProperty('rate', 150)    # Speed: slower (100) or faster (200)
    engine.setProperty('volume', 0.9)  # Volume: 0.0 to 1.0

    # Choose a voice (0 for male, 1 for female typically)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    return engine


def tts_speak(text):
    # Speak text
    engine = create_tts_engine()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

