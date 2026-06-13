import asyncio
import threading

from engines.chat_bot import llm_chat
from engines.tts_engine import tts_speak, tts_generate

from utility_scripts.system_logging import setup_logger
from window_manager.pet_window_manager import DesktopPet

# --- Logger ---
logger = setup_logger(__name__)

pet = DesktopPet()


async def tts_and_animation(user_input, response):
    pet.change_image('thinking')
    tts_speak(user_input, 0)
    speech_file = tts_generate(response, 1)
    pet.change_image('idle')
    pet.speak_and_bounce(speech_file)


def input_loop():
    while True:
        user_input = input("> ").lower()
        if user_input == "/exit":
            pet.destroy()
            break

        response = asyncio.run(llm_chat(user_input))
        logger.info(response)
        asyncio.run(tts_and_animation(user_input, response))


if __name__ == "__main__":
    threading.Thread(target=input_loop, daemon=True).start()
    pet.run()


