import sounddevice as sd
import soundfile as sf
import time
from pathlib import Path

vo_recordings_dir = Path(__file__).parent.parent / 'vo_recordings'
vo_recordings_dir.mkdir(parents=True, exist_ok=True)

# Todo - Get correct device automagically
# print(sd.query_devices())
# print(sd.default.device)


class AudioRecorder:
    def __init__(self, device=1, channels=1):
        self.device = 1

        dev_info = sd.query_devices(self.device, 'input')
        self.samplerate = int(dev_info['default_samplerate'])

        self.channels = min(channels, dev_info['max_input_channels'])

        self.stream = None
        self.wav_file = None
        self.file_path = None

    def _callback(self, indata, frames, time_info, status):
        if status:
            print(status)

        if self.wav_file:
            self.wav_file.write(indata)

    def start(self):
        self.file_path = vo_recordings_dir / f"recording_{time.time_ns()}.wav"

        self.wav_file = sf.SoundFile(
            str(self.file_path),
            mode="w",
            samplerate=self.samplerate,
            channels=self.channels
        )

        self.stream = sd.InputStream(
            device=self.device,
            samplerate=self.samplerate,
            channels=self.channels,
            callback=self._callback
        )

        self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        if self.wav_file:
            self.wav_file.close()
            self.wav_file = None

        return str(self.file_path)
