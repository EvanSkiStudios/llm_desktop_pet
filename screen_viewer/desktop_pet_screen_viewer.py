import asyncio
import threading

import time

from engines.chat_bot import llm_chat
from screen_grabber import print_screen
from engines.tts_engine import tts_speak, tts_generate
from window_manager import  pet_window_manager

from utility_scripts.system_logging import setup_logger
from window_manager.pet_window_manager import DesktopPet

# --- Logger ---
logger = setup_logger(__name__)

pet = DesktopPet()


async def tts_and_animation(user_input, response):
    speech_file = tts_generate(response, 1)
    pet.speak_and_bounce(speech_file)


async def input_loop():
    while True:
        time.sleep(10)

        pet.hide()
        screenshot_path = print_screen()
        pet.show()

        user_input = "Comment on what you see, like you are watching someone play a game, dont over analyse."
        response = await llm_chat(user_input, screenshot_path)

        logger.info(response)
        await tts_and_animation('', response)

        time.sleep(30)  # wait 15 seconds


def start_input_loop():
    asyncio.run(input_loop())


if __name__ == "__main__":
    pet.change_image('chibi_miku')
    threading.Thread(target=start_input_loop, daemon=True).start()
    pet.run()


