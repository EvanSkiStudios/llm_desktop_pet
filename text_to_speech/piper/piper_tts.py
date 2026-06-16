import tempfile
import os
import wave

from pathlib import Path
from piper import PiperVoice

from text_to_speech.piper.ffmpreg import ffmpeg_reverb

voices_dir = Path(__file__).parent / "voices"
voices_dir.mkdir(parents=True, exist_ok=True)

output_dir = Path(__file__).parent / "tts_output"
output_dir.mkdir(parents=True, exist_ok=True)

voice_onnx = str(voices_dir / 'amy' / 'en_US-amy-medium.onnx')


class TTS:
    def __init__(self):
        self.voice = PiperVoice.load(voice_onnx)

    def generate(self, text, filename):
        output_file = str(output_dir / filename)

        tmp_path = None

        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp_path = tmp.name

            with wave.open(tmp_path, "wb") as wav_file:
                self.voice.synthesize_wav(text, wav_file)

            final_file = ffmpeg_reverb(tmp_path)

            # If ffmpeg_reverb returns a new file, move it to your intended path
            os.replace(final_file, output_file)

            return output_file

        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)


def main():
    tts = TTS()

    test_text = (
        "I’ve noticed you’re struggling with your laces. Would you like me to buy you some Velcro straps?"
        " They're much more your speed."
        " Do you want me to walk you through it, or are we still in the 'trial and error' phase of your journey?"
        " I have a very simple set of instructions if your brain can handle the complexity of a double-knot."
        " Need a YouTube tutorial, or are we just pretending the 'loose-lace look' is a bold fashion choice this season?"
        " Oh, look at you! You’re almost there! Just one more loop and you’ve officially mastered a preschooler's curriculum."
        " I’m so proud of your growth today."
    )

    output = tts.generate(test_text, "output.wav")
    print(output)


if __name__ == '__main__':
    main()

