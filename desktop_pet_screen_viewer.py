import asyncio
import os
import threading

import time

import random

from chat_bot import llm_chat
from screen_grabber import print_screen
from tts_engine import tts_speak, tts_generate
import window_manager as pet

from utility_scripts.system_logging import setup_logger

# --- Logger ---
logger = setup_logger(__name__)


async def tts_and_animation(user_input, response):
    pet.change_image('thinking')
    tts_speak(user_input, 0)
    speech_file = tts_generate(response, 1)
    pet.change_image('idle')
    pet.speak_and_bounce(speech_file)


async def input_loop():
    while True:
        time.sleep(10)

        pet.toggle_window()
        screenshot_path = print_screen()
        pet.toggle_window()

        user_input = "Comment on what you see, like you are watching someone play a game, dont over analyse."
        response = await llm_chat(user_input, screenshot_path)

        logger.info(response)
        await tts_and_animation('', response)

        time.sleep(30)  # wait 15 seconds


def start_input_loop():
    asyncio.run(input_loop())


if __name__ == "__main__":
    threading.Thread(target=start_input_loop, daemon=True).start()
    pet.window_gui()


