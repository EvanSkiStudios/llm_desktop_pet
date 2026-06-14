import warnings

import whisper


# Suppress FP16 CPU warning
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

model = whisper.load_model("base")


# Whisper transcription
def whisper_transcribe(file_path):
    result = model.transcribe(file_path)
    text = result["text"].strip()

    return text

