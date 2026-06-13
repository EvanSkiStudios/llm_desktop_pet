import asyncio
import threading

from engines.chat_bot import llm_chat
from screen_grabber import print_screen
from engines.tts_engine import tts_speak, tts_generate

from utility_scripts.system_logging import setup_logger
from window_manager.pet_window_manager import DesktopPet

# --- Logger ---
logger = setup_logger(__name__)

pet = DesktopPet()


async def tts_and_animation(user_input, response):
    speech_file = tts_generate(response, 1)
    pet.speak_and_bounce(speech_file)


latest_screenshot = None
lock = asyncio.Lock()
last_used = None


async def screenshot_loop():
    global latest_screenshot

    while True:
        await asyncio.sleep(10)

        pet.hide()
        path = await asyncio.to_thread(print_screen)
        pet.show()

        async with lock:
            latest_screenshot = path


async def input_loop():
    global latest_screenshot, last_used

    while True:
        # grab whatever screenshot is currently available
        async with lock:
            screenshot_path = latest_screenshot

        # nothing available yet
        if screenshot_path is None:
            await asyncio.sleep(1)
            continue

        # skip if we already processed this exact screenshot
        if screenshot_path == last_used:
            await asyncio.sleep(1)
            continue

        # we are using the screenshot, store it for the next loop
        last_used = screenshot_path

        user_input = (
            "Comment on what you see, like you are watching someone play a game, "
            "dont over analyse."
        )

        response = await llm_chat(user_input, screenshot_path)
        logger.info(response)

        await tts_and_animation('', response)

        while pet.is_speaking:
            await asyncio.sleep(0.05)


async def main():
    await asyncio.gather(
        screenshot_loop(),
        input_loop(),
    )


def start_async_loop():
    asyncio.run(main())


if __name__ == "__main__":
    pet.change_image('chibi_miku')
    threading.Thread(target=start_async_loop, daemon=True).start()
    pet.run()


