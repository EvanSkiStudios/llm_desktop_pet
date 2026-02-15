import asyncio
import threading

from chat_bot import llm_chat
from tts_engine import tts_speak
import window_manager as pet

from utility_scripts.system_logging import setup_logger

# --- Logger ---
logger = setup_logger(__name__)


async def tts_and_animation(user_input, response):
    pet.change_image('thinking')
    tts_speak(user_input, 0)
    pet.change_image('idle')
    pet.start_bounce()
    tts_speak(response, 1)
    pet.stop_bounce()


def input_loop():
    while True:
        user_input = input("> ").lower()
        if user_input == "exit":
            pet.window_end()
            break

        response = asyncio.run(llm_chat(user_input))
        logger.info(response)
        asyncio.run(tts_and_animation(user_input, response))


if __name__ == "__main__":
    threading.Thread(target=input_loop, daemon=True).start()
    pet.window_gui()


