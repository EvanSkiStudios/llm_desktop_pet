import asyncio
import threading

from chat_bot import llm_chat
from tts_engine import tts_speak
from window_manager import pet_window_gui, pet_window_end, pet_start_bounce, pet_stop_bounce

from utility_scripts.system_logging import setup_logger

# --- Logger ---
logger = setup_logger(__name__)


async def tts_and_animation(response):
    pet_start_bounce()
    tts_speak(response)
    pet_stop_bounce()


def input_loop():
    while True:
        user_input = input("> ").lower()
        if user_input == "exit":
            pet_window_end()
            break

        response = asyncio.run(llm_chat(user_input))
        logger.info(response)
        asyncio.run(tts_and_animation(response))


if __name__ == "__main__":
    threading.Thread(target=input_loop, daemon=True).start()
    pet_window_gui()


