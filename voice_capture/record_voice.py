import asyncio
import os

import keyboard

from voice_capture.audio_recorder import AudioRecorder
from voice_capture.whisper_transcription import whisper_transcribe


async def record_until_f8_release(device=4):
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    recorder = AudioRecorder(device=device)
    recorder.start()

    def on_release(event):
        path = recorder.stop()

        if not future.done():
            loop.call_soon_threadsafe(
                future.set_result,
                path
            )

    hook = keyboard.on_release_key("f8", on_release)

    try:
        return await future
    finally:
        keyboard.unhook(hook)


async def record_voice():
    await keyboard_wait_for_f8_press()
    print("Starting recording...")
    path = await record_until_f8_release()

    text = whisper_transcribe(path)

    # DANGER
    os.remove(path)

    print(text)
    return text


async def keyboard_wait_for_f8_press():
    await asyncio.to_thread(keyboard.wait, "f8")


if __name__ == "__main__":
    asyncio.run(record_voice())
