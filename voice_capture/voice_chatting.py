import asyncio
import threading
import time

from text_to_speech.elevenlabs_voice import text_to_speech
from ollama_llm.llm_module import llm_chat
from text_to_speech.piper.piper_tts import TTS
from text_to_speech.tts_engine import tts_generate

from utility_scripts.system_logging import setup_logger
from voice_capture.record_voice import record_voice
from window_manager.pet_window_manager import DesktopPet

# --- Logger ---
logger = setup_logger(__name__)

pet = DesktopPet()
pet.change_image('isabel')

tts = TTS()


async def tts_and_animation(user_input, response):
    pet.change_image('isabel')
    # tts_speak(user_input, 0)
    # speech_file = tts_generate(response, 1)
    # speech_file = await text_to_speech(response, file_name=f"speech_{int(time.time()*1000)}", voice="DEFAULT", stability=0.5)

    speech_file = tts.generate(response, f"speech_{int(time.time()*1000)}.wav")

    pet.speak_and_bounce(speech_file)


async def input_loop():
    while True:
        user_input = await record_voice()

        prompt = "Do not format your response in Markdown, use natural language formatting."

        response = await llm_chat(user_input, system_prompt=prompt)
        logger.info(response)

        await tts_and_animation(user_input, response)


def start_async_loop():
    asyncio.run(input_loop())


if __name__ == "__main__":
    threading.Thread(target=start_async_loop, daemon=True).start()
    pet.run()


