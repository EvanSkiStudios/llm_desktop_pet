import whisper

model = whisper.load_model("base")


# Whisper transcription
def whisper_transcribe(file_path):
    result = model.transcribe(file_path)
    text = result["text"].strip()

    return text

