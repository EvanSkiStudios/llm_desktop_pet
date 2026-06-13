import pyttsx3

# Initialize the engine
engine = pyttsx3.init()

# Retrieve list of available voices
voices = engine.getProperty('voices')

# Print details of each voice
for index, voice in enumerate(voices):
    print(f"Index: {index}")
    print(f"ID: {voice.id}")
    print(f"Name: {voice.name}")
    print(f"Languages: {voice.languages}")
    print("-" * 20)

