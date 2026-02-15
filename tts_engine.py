import time

import pyttsx3
from pathlib import Path


def create_tts_engine(voice_index=0, rate=150, volume=0.9):
    # Initialize the engine
    engine = pyttsx3.init()

    # Optional: Configure properties
    engine.setProperty('rate', rate)    # Speed: slower (100) or faster (200)
    engine.setProperty('volume', volume)  # Volume: 0.0 to 1.0

    # Choose a voice (0 for male, 1 for female typically)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_index].id)
    return engine


def tts_speak(text, voice_index=0):
    # Speak text
    engine = create_tts_engine(voice_index)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def tts_generate(text, voice_index=0):
    file_name = f"speech_{int(time.time()*1000)}.wav"
    file_path = Path(__file__).parent / file_name
    # Speak text
    engine = create_tts_engine(voice_index)
    engine.save_to_file(text, file_name)
    engine.runAndWait()
    engine.stop()
    return file_path


if __name__ == "__main__":
    while True:
        user_input = input('> ').lower()
        if user_input == 'exit':
            break
        tts_speak(user_input, 0)
