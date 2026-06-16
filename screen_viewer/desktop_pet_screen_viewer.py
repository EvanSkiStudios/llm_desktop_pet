import asyncio
import threading
import time
from unittest.mock import DEFAULT

from ollama_llm.llm_module import llm_chat
from screen_grabber import print_screen
from text_to_speech.elevenlabs_voice import text_to_speech
from text_to_speech.tts_engine import tts_generate

from utility_scripts.system_logging import setup_logger
from window_manager.pet_window_manager import DesktopPet

# --- Logger ---
logger = setup_logger(__name__)

pet = DesktopPet()


async def tts_and_animation(user_input, response):
    pet.show()
    speech_file = tts_generate(response, 1)
    # speech_file = await text_to_speech(response, file_name=f"speech_{int(time.time()*1000)}", voice="SAM", stability=0.5)

    pet.speak_and_bounce(speech_file)


screenshots = []


# todo - have screenshots be got while bot is talking

async def input_loop():
    await asyncio.sleep(7.5)

    while True:
        print('taking picture')
        await asyncio.sleep(3)

        pet.hide()
        screenshot_path = await asyncio.to_thread(print_screen)
        screenshots.append(screenshot_path)

        if len(screenshots) < 6:
            continue
        
        print('pictures done')
        pet.show()

        user_input = (
            'here is a few screen shots of whats happening.'
        )

        system_prompt = (
                "The user will give you screenshots of whats happening. The time between each picture is exactly 3 seconds."
                "Comment on what you see, like you are watching someone play a game, "
                "speak like you are talking to the person that is playing the game, "
                "dont narrate what is happening."
                "dont over analyse the images."
                "Dont back seat game."
            )

        response = await llm_chat(user_input, screenshots, system_prompt)
        logger.info(response)

        await tts_and_animation('', response)

        while pet.is_speaking:
            await asyncio.sleep(0.05)

        screenshots.clear()


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


