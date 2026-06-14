import asyncio
import threading
import time

from elevenlabs_voice import text_to_speech
from engines.chat_bot import llm_chat
from engines.tts_engine import tts_speak, tts_generate

from utility_scripts.system_logging import setup_logger
from voice_capture.record_voice import record_voice
from window_manager.pet_window_manager import DesktopPet

# --- Logger ---
logger = setup_logger(__name__)

pet = DesktopPet()


async def tts_and_animation(user_input, response):
    pet.change_image('thinking')
    # tts_speak(user_input, 0)
    # speech_file = tts_generate(response, 1)
    speech_file = await text_to_speech(response, file_name=f"speech_{int(time.time()*1000)}", voice="default", stability=0.5)

    pet.change_image('idle')
    pet.speak_and_bounce(speech_file)


async def input_loop():
    while True:
        user_input = await record_voice()

        response = await llm_chat(user_input)
        logger.info(response)

        await tts_and_animation(user_input, response)


def start_async_loop():
    asyncio.run(input_loop())


if __name__ == "__main__":
    threading.Thread(target=start_async_loop, daemon=True).start()
    pet.run()


