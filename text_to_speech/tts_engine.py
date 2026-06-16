import time

import pyttsx3
from pathlib import Path

gen_files_dir = Path(__file__).parent.parent / 'generated_files'
gen_files_dir.mkdir(parents=True, exist_ok=True)


def create_tts_engine(voice_index=0, rate=175, volume=0.9):
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
    file_path = gen_files_dir / file_name
    # Speak text
    engine = create_tts_engine(voice_index)
    engine.save_to_file(text, str(file_path))
    engine.runAndWait()
    engine.stop()
    return file_path


if __name__ == "__main__":
    while True:
        user_input = input('> ').lower()
        if user_input == 'exit':
            break
        tts_speak(user_input, 0)
