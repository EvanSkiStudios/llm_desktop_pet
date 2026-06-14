import asyncio
import threading

from ollama_llm.llm_module import llm_chat
from screen_grabber import print_screen
from text_to_speech.tts_engine import tts_generate

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
        pet.show()

        await asyncio.sleep(15)

        pet.hide()
        screenshot_path = await asyncio.to_thread(print_screen)
        await asyncio.sleep(1)
        pet.show()

        user_input = (
            "Comment on what you see, like you are watching someone play a game, "
            "dont over analyse."
        )

        response = await llm_chat(user_input, screenshot_path)
        logger.info(response)

        await tts_and_animation('', response)

        while pet.is_speaking:
            pet.show()
            await asyncio.sleep(0.05)


async def main():
    await asyncio.gather(
        input_loop(),
    )


def start_async_loop():
    asyncio.run(main())


if __name__ == "__main__":
    pet.change_image('chibi_miku')
    threading.Thread(target=start_async_loop, daemon=True).start()
    pet.run()


